#!/usr/bin/env python3

"""Collect CTMark GlobalISel IRTranslator and call-lowering statistics."""

import argparse
import json
import os
import re
import shlex
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


INSTRUCTION_PREFIX = "gisel-irtranslator."
CALL_PREFIX = "gisel-irtranslator-call."
GEP_PREFIX = "gisel-irtranslator-gep."
GEP_I8_PREFIX = "gisel-irtranslator-gep-i8."
GEP_PTR_ADD_PREFIX = "gisel-irtranslator-gep-ptr-adds."
GEP_SHAPE_NAMES = {
    "AllZero": "all-zero",
    "ConstantOffsetOnly": "constant-offset-only",
    "OneDynamicUnitStride": "one-dynamic-unit-stride",
    "OneDynamicScaled": "one-dynamic-scaled",
    "MultipleDynamic": "multiple-dynamic",
}
GEP_I8_NAMES = {
    "SingleIndexConstant": "constant-index",
    "SingleIndexDynamic": "dynamic-index",
}
GEP_PTR_ADD_NAMES = {
    "NoPtrAdds": "zero",
    "OnePtrAdd": "one",
    "TwoPtrAdds": "two",
    "ThreeOrMorePtrAdds": "three-or-more",
}
GEP_SHAPE_ORDER = tuple(GEP_SHAPE_NAMES.values())
GEP_I8_ORDER = tuple(GEP_I8_NAMES.values())
GEP_PTR_ADD_ORDER = tuple(GEP_PTR_ADD_NAMES.values())
GEP_INSTRUMENTATION_REVISION = "6107fc21c4b0c6469b8edee2f9fbf68ac2310bf4"
GEP_INSTRUMENTATION_URL = (
    "https://github.com/c-rhodes/llvm-project/commit/"
    + GEP_INSTRUMENTATION_REVISION
)
CTMARK_CONFIGURATION = "O0-g"
CTMARK_CACHE = "cmake/caches/O0-g.cmake"
CALL_ARG_FLAG_NAMES = (
    "zext",
    "sext",
    "noext",
    "inreg",
    "sret",
    "byval",
    "byref",
    "nest",
    "returned",
    "split",
    "inalloca",
    "preallocated",
    "split-end",
    "swiftself",
    "swiftasync",
    "swifterror",
    "cfguardtarget",
    "hva",
    "hva-start",
    "second-arg",
    "consecutive-last",
    "consecutive",
    "copy-elision",
    "pointer",
    "vararg",
)


def fail(message):
    raise SystemExit(f"error: {message}")


def run(command, **kwargs):
    print("+ " + shlex.join(map(str, command)), flush=True)
    return subprocess.run(command, check=True, text=True, **kwargs)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "llvm_build_dir",
        type=Path,
        help="stats-enabled instrumented LLVM build containing bin/clang",
    )
    parser.add_argument(
        "--test-suite",
        type=Path,
        default=Path.home() / "llvm-test-suite",
        help="llvm-test-suite checkout (default: ~/llvm-test-suite)",
    )
    parser.add_argument("--ctmark-build-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--workload",
        action="append",
        default=[],
        help="only analyze this workload; may be repeated",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=max(1, os.cpu_count() or 1),
        help="parallel build jobs (default: host CPU count)",
    )
    parser.add_argument(
        "--no-clean", action="store_true", help="do not clean CTMark before building"
    )
    parser.add_argument(
        "--aggregate-only",
        action="store_true",
        help="only aggregate an existing CTMark build",
    )
    return parser.parse_args()


def check_checkout(path, marker, description):
    if not (path / marker).is_file():
        fail(f"not an {description} checkout: {path}")


def load_cmake_cache(build_dir):
    path = build_dir / "CMakeCache.txt"
    if not path.is_file():
        fail(f"not a CMake LLVM build directory: {build_dir}")
    values = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith(("//", "#")) or "=" not in line:
            continue
        key_and_type, value = line.split("=", 1)
        values[key_and_type.split(":", 1)[0]] = value
    return values


def validate_llvm_build(build_dir):
    cache = load_cmake_cache(build_dir)
    source_dir = Path(cache.get("LLVM_SOURCE_DIR", ""))
    if not (source_dir / "CMakeLists.txt").is_file():
        fail(f"LLVM_SOURCE_DIR is missing or invalid in {build_dir}/CMakeCache.txt")
    checkout = source_dir.parent.resolve()
    irtranslator = source_dir / "lib/CodeGen/GlobalISel/IRTranslator.cpp"
    call_lowering = source_dir / "lib/CodeGen/GlobalISel/CallLowering.cpp"
    if (
        "gisel-irtranslator" not in irtranslator.read_text()
        or "gisel-irtranslator-gep" not in irtranslator.read_text()
        or "gisel-irtranslator-call" not in call_lowering.read_text()
    ):
        fail(
            f"IRTranslator statistics are missing from {checkout}; "
            "build the compile-time-instrumentation branch"
        )
    if not (
        cache.get("LLVM_ENABLE_ASSERTIONS") == "ON"
        or cache.get("LLVM_FORCE_ENABLE_STATS") == "ON"
    ):
        fail(
            "LLVM statistics are disabled; configure with assertions or "
            "-DLLVM_FORCE_ENABLE_STATS=ON"
        )
    clang = build_dir / "bin/clang"
    clangxx = build_dir / "bin/clang++"
    if not clang.is_file() or not clangxx.is_file():
        fail(f"build clang and clang++ first in {build_dir}")
    return checkout, clang


def configure_and_build_ctmark(test_suite, build_dir, clang, jobs, clean):
    run(
        [
            "cmake",
            "-GNinja",
            "-S",
            test_suite,
            "-B",
            build_dir,
            "-C",
            test_suite / CTMARK_CACHE,
            f"-DCMAKE_C_COMPILER={clang}",
            f"-DCMAKE_CXX_COMPILER={clang.parent / 'clang++'}",
            "-DTEST_SUITE_SUBDIRS=CTMark",
            "-DTEST_SUITE_RUN_BENCHMARKS=OFF",
            "-DTEST_SUITE_COLLECT_CODE_SIZE=OFF",
            "-DTEST_SUITE_USE_PERF=OFF",
            "-DTEST_SUITE_EXTRA_C_FLAGS=-save-stats=obj",
            "-DTEST_SUITE_EXTRA_CXX_FLAGS=-save-stats=obj",
        ]
    )
    if clean:
        run(["ninja", "-C", build_dir, "clean"])
    run(["ninja", "-C", build_dir, f"-j{jobs}"])


def load_compdb(build_dir):
    proc = run(
        ["ninja", "-C", build_dir, "-t", "compdb"], stdout=subprocess.PIPE
    )
    return json.loads(proc.stdout)


def relative_output(build_dir, output):
    path = Path(output)
    if not path.is_absolute():
        return path
    try:
        return path.relative_to(build_dir)
    except ValueError:
        fail(f"object is outside the CTMark build directory: {path}")


def workload_from_path(path):
    try:
        return path.parts[path.parts.index("CTMark") + 1]
    except (ValueError, IndexError):
        return None


def source_label(source, workload):
    parts = Path(source).parts
    try:
        return Path(*parts[parts.index(workload) + 1 :]).as_posix()
    except ValueError:
        return Path(source).name


def stats_path(build_dir, output, source):
    return build_dir / output.parent / Path(source).with_suffix(".stats").name


def decode_hex(value, description, path):
    try:
        return bytes.fromhex(value).decode()
    except (ValueError, UnicodeDecodeError):
        fail(f"malformed {description} encoding {value!r} in {path}")


def decode_stat_signature(name, prefix, marker, description, path):
    suffix = name[len(prefix) :]
    if not suffix.startswith(marker):
        fail(f"malformed {description} statistic {name!r} in {path}")
    return decode_hex(suffix[1:], description, path)


def parse_bool(value, description, path):
    if value not in ("0", "1"):
        fail(f"invalid {description} boolean {value!r} in {path}")
    return value == "1"


def parse_instruction_stats(stats, path):
    records = []
    for name, count in stats.items():
        if not name.startswith(INSTRUCTION_PREFIX):
            continue
        signature = decode_stat_signature(
            name, INSTRUCTION_PREFIX, "i", "IR instruction", path
        )
        fields = signature.split("|")
        if len(fields) != 3:
            fail(f"malformed IR instruction signature {signature!r} in {path}")
        opcode, result_type, operand_types = fields
        records.append(
            {
                "signature": signature,
                "opcode": opcode,
                "result_type": decode_hex(result_type, "IR type", path),
                "operand_types": [
                    decode_hex(item, "IR type", path)
                    for item in operand_types.split(",")
                    if item
                ],
                "count": count,
            }
        )
    return records


def parse_named_stats(stats, path, prefix, names, description):
    counts = {name: 0 for name in names.values()}
    for name, count in stats.items():
        if not name.startswith(prefix):
            continue
        statistic_name = name[len(prefix) :]
        if statistic_name not in names:
            fail(f"unknown {description} statistic {name!r} in {path}")
        counts[names[statistic_name]] = count
    return counts


def parse_gep_stats(stats, path):
    return parse_named_stats(stats, path, GEP_PREFIX, GEP_SHAPE_NAMES, "GEP shape")


def parse_arg(spec, path):
    fields = spec.split("@")
    if len(fields) != 7:
        fail(f"malformed call argument signature {spec!r} in {path}")
    type_name, size, scalable, kind, single, registers, flag_sets = fields
    parsed_flags = []
    for item in flag_sets.split(","):
        parsed_flags.append([] if item == "-" else item.split("+"))
    return {
        "type": decode_hex(type_name, "call type", path),
        "size_in_bits": None if size == "-" else int(size),
        "scalable": None if scalable == "-" else parse_bool(scalable, "type", path),
        "kind": kind,
        "single_value": parse_bool(single, "single-value", path),
        "registers": int(registers),
        "flag_sets": parsed_flags,
    }


def parse_args_field(field, path):
    return [] if field == "-" else [parse_arg(item, path) for item in field.split(";")]


def parse_call_stats(stats, path):
    records = []
    for name, count in stats.items():
        if not name.startswith(CALL_PREFIX):
            continue
        signature = decode_stat_signature(name, CALL_PREFIX, "c", "call", path)
        fields = signature.split("|")
        if len(fields) != 12:
            fail(f"malformed call signature {signature!r} in {path}")
        (
            kind,
            callee,
            calling_conv,
            is_vararg,
            is_tail,
            is_musttail,
            can_lower_return,
            features,
            return_arg,
            args,
            split_return,
            split_args,
        ) = fields
        records.append(
            {
                "signature": signature,
                "kind": kind,
                "callee": callee,
                "calling_conv": int(calling_conv),
                "is_vararg": parse_bool(is_vararg, "vararg", path),
                "is_tail": parse_bool(is_tail, "tail", path),
                "is_musttail": parse_bool(is_musttail, "musttail", path),
                "can_lower_return": parse_bool(
                    can_lower_return, "can-lower-return", path
                ),
                "features": [] if features == "-" else features.split(","),
                "return": parse_arg(return_arg, path),
                "args": parse_args_field(args, path),
                "split_return": parse_args_field(split_return, path),
                "split_args": parse_args_field(split_args, path),
                "count": count,
            }
        )
    return records


def read_records(build_dir, selected):
    records = []
    seen_outputs = set()
    for entry in load_compdb(build_dir):
        if not entry.get("file") or not entry.get("output"):
            continue
        output = relative_output(build_dir, entry["output"])
        workload = workload_from_path(output)
        if workload is None or output.suffix != ".o":
            continue
        if selected and workload not in selected:
            continue
        if output in seen_outputs:
            continue
        seen_outputs.add(output)
        path = stats_path(build_dir, output, entry["file"])
        if not path.is_file():
            fail(f"statistics file is missing: {path}")
        stats = json.loads(path.read_text())
        records.append(
            {
                "workload": workload,
                "source": source_label(entry["file"], workload),
                "object": output.as_posix(),
                "stats_file": path.relative_to(build_dir).as_posix(),
                "instructions": parse_instruction_stats(stats, path),
                "calls": parse_call_stats(stats, path),
                "gep_shapes": parse_gep_stats(stats, path),
                "gep_i8": parse_named_stats(
                    stats, path, GEP_I8_PREFIX, GEP_I8_NAMES, "GEP i8"
                ),
                "gep_ptr_adds": parse_named_stats(
                    stats,
                    path,
                    GEP_PTR_ADD_PREFIX,
                    GEP_PTR_ADD_NAMES,
                    "GEP pointer-add",
                ),
            }
        )
    if not records:
        fail("no CTMark object statistics found")
    if not any(record["instructions"] for record in records):
        fail("no gisel-irtranslator statistics found")
    if not any(record["calls"] for record in records):
        fail("no gisel-irtranslator-call statistics found")
    if not any(sum(record["gep_shapes"].values()) for record in records):
        fail("no gisel-irtranslator-gep statistics found")
    if not any(sum(record["gep_i8"].values()) for record in records):
        fail("no gisel-irtranslator-gep-i8 statistics found")
    if not any(sum(record["gep_ptr_adds"].values()) for record in records):
        fail("no gisel-irtranslator-gep-ptr-adds statistics found")
    for record in records:
        if sum(record["gep_ptr_adds"].values()) != sum(
            record["gep_shapes"].values()
        ):
            fail(
                f"GEP pointer-add counts do not cover every GEP in "
                f"{record['stats_file']}"
            )
    return records


def flags(arg):
    return {flag for flag_set in arg["flag_sets"] for flag in flag_set}


def merge_signatures(records, field):
    counts = Counter()
    templates = {}
    for record in records:
        for item in record[field]:
            counts[item["signature"]] += item["count"]
            templates[item["signature"]] = item
    result = []
    for signature, count in sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    ):
        item = dict(templates[signature])
        item["count"] = count
        result.append(item)
    return result


def summarize(records):
    instructions = merge_signatures(records, "instructions")
    calls = merge_signatures(records, "calls")
    gep_shapes = Counter()
    gep_i8 = Counter()
    gep_ptr_adds = Counter()
    for record in records:
        gep_shapes.update(record["gep_shapes"])
        gep_i8.update(record["gep_i8"])
        gep_ptr_adds.update(record["gep_ptr_adds"])
    opcode_counts = Counter()
    for item in instructions:
        opcode_counts[item["opcode"]] += item["count"]
    total = sum(opcode_counts.values())
    call_total = sum(item["count"] for item in calls)
    return {
        "files": len(records),
        "ir_instructions": total,
        "call_lowering_sites": call_total,
        "direct_calls": sum(
            item["count"] for item in calls if item["callee"] == "direct"
        ),
        "opcodes": dict(sorted(opcode_counts.items())),
        "instructions": instructions,
        "gep_lowerings": sum(gep_shapes.values()),
        "gep_shapes": {
            shape: gep_shapes[shape] for shape in GEP_SHAPE_NAMES.values()
        },
        "gep_i8": {name: gep_i8[name] for name in GEP_I8_NAMES.values()},
        "gep_ptr_adds": {
            name: gep_ptr_adds[name] for name in GEP_PTR_ADD_NAMES.values()
        },
        "calls": calls,
    }


def aggregate(records):
    grouped = defaultdict(list)
    for record in records:
        grouped[record["workload"]].append(record)
    workloads = [
        {"workload": workload, **summarize(grouped[workload])}
        for workload in sorted(grouped, key=str.casefold)
    ]
    return summarize(records), workloads


def percent(count, total):
    return 100.0 * count / total if total else 0.0


def append_opcode_table(lines, title, summary, heading_level):
    lines.extend(
        [
            "",
            f"{'#' * heading_level} {title}",
            "",
            "```text",
            f"{'opcode':<24} {'count':>12} {'share':>8}",
        ]
    )
    for opcode, count in sorted(
        summary["opcodes"].items(), key=lambda item: (-item[1], item[0])
    ):
        lines.append(
            f"{opcode:<24} {count:>12,} "
            f"{percent(count, summary['ir_instructions']):>7.2f}%"
        )
    lines.append("```")


def type_signature(item):
    operands = ",".join(item["operand_types"]) or "-"
    return f"{item['result_type']} <- [{operands}]"


def append_type_detail(lines, title, summary, heading_level):
    lines.extend(["", f"{'#' * heading_level} {title}"])
    grouped = defaultdict(list)
    for item in summary["instructions"]:
        grouped[item["opcode"]].append(item)
    for opcode in sorted(
        grouped, key=lambda name: (-sum(item["count"] for item in grouped[name]), name)
    ):
        opcode_total = summary["opcodes"][opcode]
        lines.extend(
            [
                "",
                f"{'#' * (heading_level + 1)} {opcode}",
                "",
                "```text",
                f"{'count':>12} {'opcode%':>8} {'total%':>8}  types",
            ]
        )
        for item in grouped[opcode]:
            count = item["count"]
            lines.append(
                f"{count:>12,} {percent(count, opcode_total):>7.2f}% "
                f"{percent(count, summary['ir_instructions']):>7.2f}%  "
                f"{type_signature(item)}"
            )
        lines.append("```")


def append_gep_shape_table(lines, title, summary, heading_level):
    total = summary["gep_lowerings"]
    lines.extend(
        [
            "",
            f"{'#' * heading_level} {title}",
            "",
            "```text",
            f"{'shape':<26} {'count':>12} {'GEP share':>10}",
        ]
    )
    for shape, count in sorted_count_items(
        summary["gep_shapes"], GEP_SHAPE_ORDER
    ):
        lines.append(
            f"{shape:<26} {count:>12,} {percent(count, total):>7.2f}%"
        )
    lines.append(f"{'TOTAL':<26} {total:>12,} {percent(total, total):>7.2f}%")
    lines.append("```")


def sorted_count_items(counts, order):
    rank = {name: index for index, name in enumerate(order)}
    return sorted(counts.items(), key=lambda item: (-item[1], rank[item[0]]))


def append_gep_detail_table(lines, title, counts, order, total, heading_level):
    lines.extend(
        [
            "",
            f"{'#' * heading_level} {title}",
            "",
            "```text",
            f"{'value':<26} {'count':>12} {'GEP share':>10}",
        ]
    )
    for name, count in sorted_count_items(counts, order):
        lines.append(f"{name:<26} {count:>12,} {percent(count, total):>9.2f}%")
    lines.append("```")


def gep_markdown(build_dir, compiler, release, ctmark, overall, workloads):
    lines = [
        "# CTMark GlobalISel IRTranslator GEP statistics",
        "",
        f"Build: `{build_dir.name}`",
        f"LLVM revision: `{compiler['revision']}`",
        "Instrumentation: "
        f"[`{GEP_INSTRUMENTATION_REVISION[:12]}`]({GEP_INSTRUMENTATION_URL})",
        f"LLVM release: `{release['tag']}` (`{release['revision']}`)",
        f"CTMark configuration: `{ctmark['configuration_id']}`",
        f"Target: `{ctmark['target']}`",
        "",
        "Counts cover `translateGetElementPtr` invocations and can include "
        "constant-expression GEPs. Every percentage is the share of all GEP "
        "lowerings in the same workload.",
        "",
        "The lowering-shape and emitted-`G_PTR_ADD` categories each partition "
        "all GEPs and therefore sum to 100%. Scalar single-index i8 GEPs are "
        "a subset, so their percentages do not sum to 100%.",
        "",
        "## Categories",
        "",
        "### Lowering shapes",
        "",
        "- `all-zero`: every index is zero; lowering emits a copy of the base "
        "pointer.",
        "- `constant-offset-only`: all indices can be folded into a constant "
        "byte offset.",
        "- `one-dynamic-unit-stride`: one dynamic sequential index has a byte "
        "stride of one.",
        "- `one-dynamic-scaled`: one dynamic sequential index requires scaling.",
        "- `multiple-dynamic`: more than one sequential index is dynamic.",
        "",
        "Constant struct indices contribute to the folded byte offset; they "
        "are not dynamic sequential indices.",
        "",
        "The examples below follow the [LangRef `getelementptr` syntax]("
        "https://llvm.org/docs/LangRef.html#getelementptr-instruction). They "
        "assume `ptr %base`, `i64 %i`, `i64 %j`, and `i64 %k` inputs.",
        "",
        "```llvm",
        "; all-zero",
        "%zero = getelementptr [4 x i32], ptr %base, i64 0, i64 0",
        "",
        "; constant-offset-only",
        "%constant = getelementptr [4 x i32], ptr %base, i64 0, i64 3",
        "",
        "; constant-offset-only and single-index-i8/constant-index",
        "%i8.constant = getelementptr i8, ptr %base, i64 12",
        "",
        "; one-dynamic-unit-stride and single-index-i8/dynamic-index",
        "%i8.dynamic = getelementptr i8, ptr %base, i64 %i",
        "",
        "; one-dynamic-scaled",
        "%scaled = getelementptr i32, ptr %base, i64 %i",
        "",
        "; multiple-dynamic",
        "%multiple = getelementptr [16 x i32], ptr %base, i64 %i, i64 %j",
        "",
        "; one-dynamic-scaled with a constant component",
        "%two.adds = getelementptr [16 x i32], ptr %base, i64 1, i64 %i",
        "",
        "; multiple-dynamic with three G_PTR_ADDs",
        "%three.adds = getelementptr [4 x [8 x i32]], ptr %base, i64 %i,",
        "                i64 %j, i64 %k",
        "```",
        "",
        "### Scalar single-index i8 GEPs",
        "",
        "- `constant-index`: the sole IR index operand is a constant integer.",
        "- `dynamic-index`: the sole IR index operand is not a constant integer.",
        "",
        "This category counts only scalar GEPs whose source element type is "
        "`i8` and which have exactly one index. `%i8.constant` and "
        "`%i8.dynamic` above demonstrate its two values.",
        "",
        "### Emitted G_PTR_ADD counts",
        "",
        "- `zero`, `one`, and `two`: the exact number of `G_PTR_ADD` "
        "instructions emitted for one GEP.",
        "- `three-or-more`: at least three `G_PTR_ADD` instructions are emitted.",
        "",
        "These are Machine IR output categories, not separate LangRef forms. "
        "For the examples above, `%zero` emits no `G_PTR_ADD`; `%constant`, "
        "`%i8.constant`, `%i8.dynamic`, and `%scaled` emit one; and `%multiple` "
        "and `%two.adds` emit two. `%three.adds` emits three in the "
        "instrumented lowering.",
        "",
        "## Overall",
    ]
    append_gep_shape_table(lines, "Lowering shapes", overall, 3)
    append_gep_detail_table(
        lines,
        "Scalar single-index i8 GEPs",
        overall["gep_i8"],
        GEP_I8_ORDER,
        overall["gep_lowerings"],
        3,
    )
    append_gep_detail_table(
        lines,
        "Emitted G_PTR_ADD counts",
        overall["gep_ptr_adds"],
        GEP_PTR_ADD_ORDER,
        overall["gep_lowerings"],
        3,
    )
    lines.extend(["", "## By workload"])
    for item in workloads:
        lines.extend(["", f"### {item['workload']}"])
        append_gep_shape_table(lines, "Lowering shapes", item, 4)
        append_gep_detail_table(
            lines,
            "Scalar single-index i8 GEPs",
            item["gep_i8"],
            GEP_I8_ORDER,
            item["gep_lowerings"],
            4,
        )
        append_gep_detail_table(
            lines,
            "Emitted G_PTR_ADD counts",
            item["gep_ptr_adds"],
            GEP_PTR_ADD_ORDER,
            item["gep_lowerings"],
            4,
        )
    return "\n".join(lines) + "\n"


def arg_signature(arg):
    result = arg["type"]
    arg_flags = flags(arg)
    if arg_flags:
        result += "{" + ",".join(sorted(arg_flags)) + "}"
    return result


def call_type_shape(call, split):
    args = call["split_args"] if split else call["args"]
    arg_types = ",".join(arg["type"] for arg in args) or "-"
    if split:
        returns = call["split_return"]
        return_types = ",".join(arg["type"] for arg in returns)
        if not return_types:
            return_types = "void" if call["return"]["kind"] == "void" else "-"
    else:
        return_types = call["return"]["type"]
    return f"[{arg_types}] -> {return_types}"


def append_call_shape_table(lines, title, summary, split):
    counts = Counter()
    for call in summary["calls"]:
        counts[call_type_shape(call, split)] += call["count"]
    lines.extend(
        [
            "",
            f"### {title}",
            "",
            "```text",
            f"{'count':>12} {'share':>8}  types",
        ]
    )
    for shape, count in counts.most_common(20):
        lines.append(
            f"{count:>12,} "
            f"{percent(count, summary['call_lowering_sites']):>7.2f}%  {shape}"
        )
    lines.append("```")


def call_flag_counts(summary):
    counts = Counter()
    total = 0
    for call in summary["calls"]:
        for value in (*call["split_args"], *call["split_return"]):
            for flag_set in value["flag_sets"]:
                total += call["count"]
                for flag in flag_set:
                    counts[flag] += call["count"]
    return counts, total


def append_call_flag_table(lines, summary):
    counts, total = call_flag_counts(summary)
    flag_names = sorted(
        set(CALL_ARG_FLAG_NAMES) | set(counts),
        key=lambda flag: (-counts[flag], flag),
    )
    lines.extend(
        [
            "",
            "### `ArgFlagsTy` summary",
            "",
            f"Counts are ABI-split `ArgFlagsTy` values with the flag set, "
            f"across {total:,} values. Flags can coexist, so shares do not "
            "sum to 100%.",
            "`pointer` is type-derived. `vararg` marks non-fixed argument "
            "values, so it need not match the vararg call count above.",
            "",
            "```text",
            f"{'flag':<20} {'count':>12} {'share':>9}",
        ]
    )
    for flag in flag_names:
        lines.append(
            f"{flag:<20} {counts[flag]:>12,} "
            f"{percent(counts[flag], total):>8.2f}%"
        )
    lines.append("```")


def append_call_summary(lines, summary):
    properties = [
        ("kind", lambda call: call["kind"]),
        ("callee", lambda call: call["callee"]),
        ("calling convention", lambda call: str(call["calling_conv"])),
        ("vararg", lambda call: "yes" if call["is_vararg"] else "no"),
        ("tail", lambda call: "yes" if call["is_tail"] else "no"),
        ("musttail", lambda call: "yes" if call["is_musttail"] else "no"),
        (
            "lowerable return",
            lambda call: "yes" if call["can_lower_return"] else "no",
        ),
        (
            "features",
            lambda call: ",".join(call["features"]) if call["features"] else "none",
        ),
    ]
    lines.extend(
        [
            "",
            "## Overall call summary",
            "",
            "```text",
            f"{'property':<20} {'value':<20} {'count':>12} {'share':>8}",
        ]
    )
    for property_name, get_value in properties:
        counts = Counter()
        for call in summary["calls"]:
            counts[get_value(call)] += call["count"]
        for value, count in counts.most_common():
            lines.append(
                f"{property_name:<20} {value:<20} {count:>12,} "
                f"{percent(count, summary['call_lowering_sites']):>7.2f}%"
            )
    lines.append("```")
    append_call_flag_table(lines, summary)
    lines.extend(
        [
            "",
            "Type-shape tables merge flags and other call properties and show the "
            "20 most common shapes.",
        ]
    )
    append_call_shape_table(lines, "Original IR type shapes", summary, False)
    append_call_shape_table(lines, "ABI-split type shapes", summary, True)


def markdown(build_dir, compiler, release, ctmark, overall, workloads):
    lines = [
        "# CTMark GlobalISel IRTranslator statistics",
        "",
        f"Build: `{build_dir.name}`",
        f"LLVM revision: `{compiler['revision']}`",
        f"LLVM release: `{release['tag']}` (`{release['revision']}`)",
        f"CTMark configuration: `{ctmark['configuration_id']}`",
        f"Target: `{ctmark['target']}`",
        "",
        "IR instruction counts are inputs presented to `IRTranslator::translate`. "
        "Call counts are non-intrinsic call/invoke sites reaching generic call "
        "lowering.",
        "",
        "Detailed GEP lowering statistics are written to `gep.md`.",
        "",
        "In IR type tables, `opcode%` is the share of that opcode and `total%` "
        "is the share of all translated IR instructions.",
        "",
        "## Summary",
        "",
        "```text",
        f"{'workload':<18} {'files':>5} {'IR insts':>12} {'calls':>10} "
        f"{'direct':>10}",
    ]
    for item in workloads:
        lines.append(
            f"{item['workload']:<18} {item['files']:>5} "
            f"{item['ir_instructions']:>12,} {item['call_lowering_sites']:>10,} "
            f"{item['direct_calls']:>10,}"
        )
    lines.append(
        f"{'TOTAL':<18} {overall['files']:>5} "
        f"{overall['ir_instructions']:>12,} {overall['call_lowering_sites']:>10,} "
        f"{overall['direct_calls']:>10,}"
    )
    lines.append("```")
    append_call_summary(lines, overall)
    append_opcode_table(lines, "Overall opcode detail", overall, 2)
    lines.extend(["", "## Opcode detail by workload"])
    for item in workloads:
        append_opcode_table(lines, item["workload"], item, 3)
    append_type_detail(lines, "Overall IR type detail", overall, 2)
    lines.extend(["", "## IR type detail by workload"])
    for item in workloads:
        append_type_detail(lines, item["workload"], item, 3)
    return "\n".join(lines) + "\n"


def write_instruction_tsv(path, overall, workloads):
    fields = [
        "workload",
        "opcode",
        "result_type",
        "operand_types",
        "count",
        "share_percent",
    ]
    lines = ["\t".join(fields)]
    for workload, summary in [
        ("TOTAL", overall),
        *((item["workload"], item) for item in workloads),
    ]:
        for item in summary["instructions"]:
            lines.append(
                "\t".join(
                    [
                        workload,
                        item["opcode"],
                        item["result_type"],
                        ",".join(item["operand_types"]) or "-",
                        str(item["count"]),
                        f"{percent(item['count'], summary['ir_instructions']):.6f}",
                    ]
                )
            )
    path.write_text("\n".join(lines) + "\n")


def write_gep_shape_tsv(path, overall, workloads):
    fields = ["workload", "shape", "count", "gep_share_percent"]
    lines = ["\t".join(fields)]
    for workload, summary in [
        ("TOTAL", overall),
        *((item["workload"], item) for item in workloads),
    ]:
        for shape, count in sorted_count_items(
            summary["gep_shapes"], GEP_SHAPE_ORDER
        ):
            lines.append(
                "\t".join(
                    [
                        workload,
                        shape,
                        str(count),
                        f"{percent(count, summary['gep_lowerings']):.6f}",
                    ]
                )
            )
    path.write_text("\n".join(lines) + "\n")


def write_gep_detail_tsv(path, overall, workloads):
    fields = [
        "workload",
        "category",
        "value",
        "count",
        "gep_share_percent",
    ]
    lines = ["\t".join(fields)]
    for workload, summary in [
        ("TOTAL", overall),
        *((item["workload"], item) for item in workloads),
    ]:
        for category, counts, order in [
            ("single-index-i8", summary["gep_i8"], GEP_I8_ORDER),
            ("ptr-adds-emitted", summary["gep_ptr_adds"], GEP_PTR_ADD_ORDER),
        ]:
            for value, count in sorted_count_items(counts, order):
                lines.append(
                    "\t".join(
                        [
                            workload,
                            category,
                            value,
                            str(count),
                            f"{percent(count, summary['gep_lowerings']):.6f}",
                        ]
                    )
                )
    path.write_text("\n".join(lines) + "\n")


def write_call_tsv(path, overall, workloads):
    fields = [
        "workload",
        "kind",
        "callee",
        "calling_conv",
        "is_vararg",
        "is_tail",
        "is_musttail",
        "can_lower_return",
        "features",
        "return_type",
        "arg_types",
        "split_arg_types",
        "count",
        "share_percent",
    ]
    lines = ["\t".join(fields)]
    for workload, summary in [
        ("TOTAL", overall),
        *((item["workload"], item) for item in workloads),
    ]:
        for call in summary["calls"]:
            lines.append(
                "\t".join(
                    [
                        workload,
                        call["kind"],
                        call["callee"],
                        str(call["calling_conv"]),
                        str(int(call["is_vararg"])),
                        str(int(call["is_tail"])),
                        str(int(call["is_musttail"])),
                        str(int(call["can_lower_return"])),
                        ",".join(call["features"]) or "-",
                        arg_signature(call["return"]),
                        ",".join(arg_signature(arg) for arg in call["args"]) or "-",
                        ",".join(arg_signature(arg) for arg in call["split_args"])
                        or "-",
                        str(call["count"]),
                        f"{percent(call['count'], summary['call_lowering_sites']):.6f}",
                    ]
                )
            )
    path.write_text("\n".join(lines) + "\n")


def compiler_metadata(clang):
    proc = subprocess.run(
        [str(clang), "--version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    revisions = re.findall(r"\b[0-9a-fA-F]{40}\b", proc.stdout)
    if not revisions:
        fail(f"cannot determine the built LLVM revision from {clang} --version")
    target = re.search(r"^Target: (\S+)$", proc.stdout, re.MULTILINE)
    if not target:
        fail(f"cannot determine the target from {clang} --version")
    return {
        "path": str(clang),
        "revision": revisions[-1].lower(),
        "target": target.group(1),
        "version": proc.stdout.strip(),
    }


def release_metadata(checkout, revision):
    try:
        tag = subprocess.run(
            [
                "git",
                "-C",
                str(checkout),
                "describe",
                "--tags",
                "--abbrev=0",
                "--match=llvmorg-*",
                revision,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        release_revision = subprocess.run(
            ["git", "-C", str(checkout), "rev-list", "-n1", tag],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        fail(f"cannot determine the LLVM release base for revision {revision}")
    return {"tag": tag, "revision": release_revision}


def write_report(output_dir, checkout, clang, build_dir, records):
    overall, workloads = aggregate(records)
    compiler = compiler_metadata(clang)
    release = release_metadata(checkout, compiler["revision"])
    target_arch = compiler["target"].split("-", 1)[0]
    ctmark = {
        "configuration": CTMARK_CONFIGURATION,
        "configuration_id": f"{target_arch}-{CTMARK_CONFIGURATION}",
        "cmake_cache": CTMARK_CACHE,
        "target": compiler["target"],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    file_summaries = [
        {
            "workload": record["workload"],
            "source": record["source"],
            "object": record["object"],
            "stats_file": record["stats_file"],
            "ir_instructions": sum(
                item["count"] for item in record["instructions"]
            ),
            "call_lowering_sites": sum(item["count"] for item in record["calls"]),
            "gep_lowerings": sum(record["gep_shapes"].values()),
        }
        for record in records
    ]
    data = {
        "schema_version": 4,
        "llvm_revision": compiler["revision"],
        "llvm_release": release,
        "compiler": compiler,
        "ctmark": ctmark,
        "ctmark_build_dir": str(build_dir),
        "overall": overall,
        "workloads": workloads,
        "files": file_summaries,
    }
    (output_dir / "profile.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n"
    )
    (output_dir / "profile.md").write_text(
        markdown(build_dir, compiler, release, ctmark, overall, workloads)
    )
    (output_dir / "gep.md").write_text(
        gep_markdown(build_dir, compiler, release, ctmark, overall, workloads)
    )
    write_instruction_tsv(output_dir / "instructions.tsv", overall, workloads)
    write_call_tsv(output_dir / "calls.tsv", overall, workloads)
    write_gep_shape_tsv(output_dir / "gep.tsv", overall, workloads)
    write_gep_detail_tsv(
        output_dir / "gep-i8-ptr-adds.tsv", overall, workloads
    )
    for name in (
        "profile.json",
        "profile.md",
        "gep.md",
        "instructions.tsv",
        "calls.tsv",
        "gep.tsv",
        "gep-i8-ptr-adds.tsv",
    ):
        print(output_dir / name)


def main():
    args = parse_args()
    llvm_build = args.llvm_build_dir.expanduser().resolve()
    test_suite = args.test_suite.expanduser().resolve()
    check_checkout(test_suite, "CTMark/CMakeLists.txt", "llvm-test-suite")
    checkout, clang = validate_llvm_build(llvm_build)
    ctmark_build = (
        args.ctmark_build_dir.expanduser().resolve()
        if args.ctmark_build_dir
        else Path.cwd() / "build-ctmark-gisel-irtranslator-stats"
    )
    output_dir = (
        args.output_dir.expanduser().resolve() if args.output_dir else Path.cwd()
    )
    if not args.aggregate_only:
        configure_and_build_ctmark(
            test_suite, ctmark_build, clang, args.jobs, not args.no_clean
        )
    elif not (ctmark_build / "build.ninja").is_file():
        fail(f"not a Ninja build directory: {ctmark_build}")
    write_report(
        output_dir,
        checkout,
        clang,
        ctmark_build,
        read_records(ctmark_build, set(args.workload)),
    )


if __name__ == "__main__":
    main()
