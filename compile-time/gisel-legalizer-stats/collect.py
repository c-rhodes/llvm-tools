#!/usr/bin/env python3

"""Collect CTMark legalizer statistics using an existing LLVM build."""

import argparse
import json
import os
import re
import shlex
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ACTIONS = (
    "Legal",
    "NarrowScalar",
    "WidenScalar",
    "FewerElements",
    "MoreElements",
    "Bitcast",
    "Lower",
    "Libcall",
    "Custom",
    "Unsupported",
    "NotFound",
)
STAT_PREFIX = "gisel-legalizer."
QUERY_STAT_PREFIX = "gisel-legalizer-query."
CTMARK_CONFIGURATION = "O0-g"
CTMARK_CACHE = "cmake/caches/O0-g.cmake"


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
        "-j",
        "--jobs",
        type=int,
        default=max(1, os.cpu_count() or 1),
        help="parallel build jobs (default: host CPU count)",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="do not clean CTMark before building",
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
        key = key_and_type.split(":", 1)[0]
        values[key] = value
    return values


def validate_llvm_build(build_dir):
    cache = load_cmake_cache(build_dir)
    source_dir = Path(cache.get("LLVM_SOURCE_DIR", ""))
    if not (source_dir / "CMakeLists.txt").is_file():
        fail(f"LLVM_SOURCE_DIR is missing or invalid in {build_dir}/CMakeCache.txt")
    checkout = source_dir.parent.resolve()
    source = source_dir / "lib/CodeGen/GlobalISel/LegalizerHelper.cpp"
    if "gisel-legalizer" not in source.read_text():
        fail(
            f"GlobalISel legalizer statistics are missing from {checkout}; "
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
        ["ninja", "-C", build_dir, "-t", "compdb"],
        stdout=subprocess.PIPE,
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


def legalizer_counts(stats, path):
    counts = {}
    for name, count in stats.items():
        if not name.startswith(STAT_PREFIX):
            continue
        suffix = name[len(STAT_PREFIX) :]
        try:
            opcode, action = suffix.rsplit(".", 1)
        except ValueError:
            fail(f"malformed legalizer statistic {name!r} in {path}")
        if action not in ACTIONS:
            fail(f"unknown legalization action {action!r} in {path}")
        counts.setdefault(opcode, {})[action] = count
    return counts


def legalizer_queries(stats, path):
    queries = []
    for name, count in stats.items():
        if not name.startswith(QUERY_STAT_PREFIX):
            continue
        suffix = name[len(QUERY_STAT_PREFIX) :]
        if not suffix.startswith("q"):
            fail(f"malformed legalizer query statistic {name!r} in {path}")
        try:
            signature = bytes.fromhex(suffix[1:]).decode()
        except (ValueError, UnicodeDecodeError):
            fail(f"malformed legalizer query encoding {name!r} in {path}")
        fields = signature.split("|")
        if len(fields) != 8:
            fail(f"malformed legalizer query statistic {name!r} in {path}")
        opcode, origin, visit, types, mem_descs, action, type_idx, new_type = (
            fields
        )
        if origin not in ("initial", "generated"):
            fail(f"unknown instruction origin {origin!r} in {path}")
        if visit not in ("first", "revisit"):
            fail(f"unknown visit kind {visit!r} in {path}")
        if action not in ACTIONS:
            fail(f"unknown legalization action {action!r} in {path}")
        try:
            type_idx = int(type_idx)
        except ValueError:
            fail(f"invalid legalization type index {type_idx!r} in {path}")

        memory = []
        if mem_descs != "-":
            for descriptor in mem_descs.split(","):
                parts = descriptor.split("@")
                if len(parts) != 4:
                    fail(f"malformed memory descriptor {descriptor!r} in {path}")
                memory_type, align_in_bits, ordering, failure_ordering = (
                    part.strip() for part in parts
                )
                try:
                    align_in_bits = int(align_in_bits)
                except ValueError:
                    fail(f"invalid memory alignment {align_in_bits!r} in {path}")
                memory.append(
                    {
                        "type": memory_type,
                        "align_in_bits": align_in_bits,
                        "ordering": ordering,
                        "failure_ordering": failure_ordering,
                    }
                )

        queries.append(
            {
                "opcode": opcode,
                "origin": origin,
                "visit": visit,
                "types": (
                    [] if types == "-" else [item.strip() for item in types.split(",")]
                ),
                "memory": memory,
                "action": action,
                "type_idx": type_idx,
                "new_type": None if new_type == "-" else new_type,
                "count": count,
            }
        )
    return queries


def read_records(build_dir):
    records = []
    seen_outputs = set()
    for entry in load_compdb(build_dir):
        if not entry.get("file") or not entry.get("output"):
            continue
        output = relative_output(build_dir, entry["output"])
        workload = workload_from_path(output)
        if workload is None or output.suffix != ".o":
            continue
        if output in seen_outputs:
            continue
        seen_outputs.add(output)
        path = stats_path(build_dir, output, entry["file"])
        if not path.is_file():
            fail(f"statistics file is missing: {path}")
        stats = json.loads(path.read_text())
        counts = legalizer_counts(stats, path)
        queries = legalizer_queries(stats, path)
        action_total = sum(
            count for actions in counts.values() for count in actions.values()
        )
        query_total = sum(query["count"] for query in queries)
        if queries and query_total != action_total:
            fail(
                f"legalizer action/query totals differ in {path}: "
                f"{action_total} != {query_total}"
            )
        records.append(
            {
                "workload": workload,
                "source": source_label(entry["file"], workload),
                "object": output.as_posix(),
                "stats_file": path.relative_to(build_dir).as_posix(),
                "opcodes": counts,
                "queries": queries,
            }
        )
    if not records:
        fail("no CTMark object statistics found")
    if not any(record["opcodes"] for record in records):
        fail(
            "no gisel-legalizer statistics found; build the instrumented "
            "compiler with LLVM_FORCE_ENABLE_STATS=ON"
        )
    if not any(record["queries"] for record in records):
        fail(
            "no gisel-legalizer-query statistics found; rebuild the "
            "compile-time-instrumentation branch with query instrumentation"
        )
    return records


def memory_key(memory):
    return tuple(
        (
            item["type"],
            item["align_in_bits"],
            item["ordering"],
            item["failure_ordering"],
        )
        for item in memory
    )


def query_key(query):
    return (
        query["opcode"],
        query["origin"],
        query["visit"],
        tuple(query["types"]),
        memory_key(query["memory"]),
        query["action"],
        query["type_idx"],
        query["new_type"],
    )


def query_from_key(key, count):
    opcode, origin, visit, types, memory, action, type_idx, new_type = key
    return {
        "opcode": opcode,
        "origin": origin,
        "visit": visit,
        "types": list(types),
        "memory": [
            {
                "type": memory_type,
                "align_in_bits": align_in_bits,
                "ordering": ordering,
                "failure_ordering": failure_ordering,
            }
            for memory_type, align_in_bits, ordering, failure_ordering in memory
        ],
        "action": action,
        "type_idx": type_idx,
        "new_type": new_type,
        "count": count,
    }


def summarize(records):
    action_counts = defaultdict(Counter)
    query_counts = Counter()
    for record in records:
        for opcode, actions in record["opcodes"].items():
            action_counts[opcode].update(actions)
        for query in record["queries"]:
            query_counts[query_key(query)] += query["count"]

    opcodes = {}
    total = 0
    legal = 0
    for opcode in sorted(action_counts):
        actions = action_counts[opcode]
        opcode_total = sum(actions.values())
        opcode_legal = actions["Legal"]
        total += opcode_total
        legal += opcode_legal
        opcodes[opcode] = {
            "total": opcode_total,
            "legal": opcode_legal,
            "legal_percent": 100.0 * opcode_legal / opcode_total,
            "actions": {action: actions[action] for action in ACTIONS},
        }
    return {
        "files": len(records),
        "files_with_actions": sum(bool(record["opcodes"]) for record in records),
        "total": total,
        "legal": legal,
        "legal_percent": 100.0 * legal / total if total else None,
        "opcodes": opcodes,
        "queries": [
            query_from_key(key, count)
            for key, count in sorted(
                query_counts.items(), key=lambda item: (-item[1], item[0])
            )
        ],
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


def percent(value):
    return "-" if value is None else f"{value:.2f}%"


def memory_signature(memory):
    return ",".join(
        f"{item['type']}@{item['align_in_bits']}@{item['ordering']}@"
        f"{item['failure_ordering']}"
        for item in memory
    ) or "-"


def query_signature(query):
    types = ",".join(query["types"]) or "-"
    mutation = ""
    if query["new_type"] is not None:
        mutation = f" {query['type_idx']}->{query['new_type']}"
    return (
        f"{query['opcode']} [{types}] mem=[{memory_signature(query['memory'])}] "
        f"{query['origin']}/{query['visit']} -> {query['action']}{mutation}"
    )


def append_opcode_table(lines, title, summary, heading_level):
    lines.extend(
        [
            "",
            f"{'#' * heading_level} {title}",
            "",
            "```text",
            f"{'opcode':<28} {'visits':>12} {'share':>8} "
            f"{'legal-count':>12} {'legal%':>8}",
        ]
    )
    ordered = sorted(
        summary["opcodes"].items(),
        key=lambda pair: (-pair[1]["total"], pair[0]),
    )
    for opcode, item in ordered:
        share = 100.0 * item["total"] / summary["total"]
        lines.append(
            f"{opcode:<28} {item['total']:>12,} {share:>7.2f}% "
            f"{item['legal']:>12,} {percent(item['legal_percent']):>8}"
        )
    lines.append("```")


def legal_queries_by_opcode(summary):
    grouped = defaultdict(Counter)
    for query in summary["queries"]:
        if query["action"] != "Legal":
            continue
        key = (tuple(query["types"]), memory_key(query["memory"]))
        grouped[query["opcode"]][key] += query["count"]
    return grouped


def semantic_query_signature(key):
    types, memory = key
    type_signature = ",".join(types) or "-"
    memory_descs = ",".join(
        f"{memory_type}@{align_in_bits}@{ordering}@{failure_ordering}"
        for memory_type, align_in_bits, ordering, failure_ordering in memory
    ) or "-"
    return f"[{type_signature}] mem=[{memory_descs}]"


def append_legal_query_detail(lines, title, summary, heading_level):
    lines.extend(["", f"{'#' * heading_level} {title}"])
    grouped = legal_queries_by_opcode(summary)
    ordered_opcodes = sorted(
        grouped,
        key=lambda opcode: (-sum(grouped[opcode].values()), opcode),
    )
    for opcode in ordered_opcodes:
        lines.extend(
            [
                "",
                f"{'#' * (heading_level + 1)} {opcode}",
                "",
                "```text",
                f"{'count':>12} {'opcode%':>8} {'total%':>8}  query",
            ]
        )
        opcode_total = summary["opcodes"][opcode]["legal"]
        for key, count in sorted(
            grouped[opcode].items(), key=lambda item: (-item[1], item[0])
        ):
            opcode_share = 100.0 * count / opcode_total
            total_share = 100.0 * count / summary["total"]
            lines.append(
                f"{count:>12,} {opcode_share:>7.2f}% {total_share:>7.2f}%  "
                f"{semantic_query_signature(key)}"
            )
        lines.append("```")


def append_query_table(lines, title, queries, total, limit=40):
    lines.extend(["", f"## {title}", "", "```text"])
    lines.append(f"{'count':>12} {'share':>8}  query")
    for query in queries[:limit]:
        share = 100.0 * query["count"] / total
        lines.append(
            f"{query['count']:>12,} {share:>7.2f}%  {query_signature(query)}"
        )
    lines.append("```")


def markdown(build_dir, compiler, release, ctmark, overall, workloads):
    lines = [
        "# CTMark GlobalISel legalizer actions",
        "",
        f"Build: `{build_dir.name}`",
        f"LLVM revision: `{compiler['revision']}`",
        f"LLVM release: `{release['tag']}` (`{release['revision']}`)",
        f"CTMark configuration: `{ctmark['configuration_id']}`",
        f"Target: `{ctmark['target']}`",
        "",
        "Counts are legalizer visits, including instructions created while "
        "legalizing.",
        "",
        "`mem=[...]` entries describe `LegalityQuery::MemDesc` values as "
        "`type@alignment-in-bits@ordering@failure-ordering`. Failure ordering "
        "is only meaningful for compare-exchange.",
        "",
        "## Summary",
        "",
        "```text",
        f"{'workload':<18} {'files':>5} {'visits':>12} "
        f"{'legal-count':>12} {'legal%':>8}",
    ]
    for item in workloads:
        lines.append(
            f"{item['workload']:<18} {item['files']:>5} "
            f"{item['total']:>12,} {item['legal']:>12,} "
            f"{percent(item['legal_percent']):>8}"
        )
    lines.append(
        f"{'TOTAL':<18} {overall['files']:>5} {overall['total']:>12,} "
        f"{overall['legal']:>12,} {percent(overall['legal_percent']):>8}"
    )
    lines.append("```")
    append_opcode_table(lines, "Overall opcode detail", overall, 2)
    lines.extend(["", "## Opcode detail by workload"])
    for item in workloads:
        append_opcode_table(lines, item["workload"], item, 3)
    append_legal_query_detail(lines, "Overall legal query detail", overall, 2)
    lines.extend(["", "## Legal query detail by workload"])
    for item in workloads:
        append_legal_query_detail(lines, item["workload"], item, 3)
    append_query_table(
        lines,
        "Top non-legal queries",
        [query for query in overall["queries"] if query["action"] != "Legal"],
        overall["total"],
    )
    return "\n".join(lines) + "\n"


def write_tsv(path, overall, workloads):
    fields = [
        "workload",
        "opcode",
        "total",
        "legal",
        "legal_percent",
        *ACTIONS,
    ]
    lines = ["\t".join(fields)]
    for workload, summary in [("TOTAL", overall), *[
        (item["workload"], item) for item in workloads
    ]]:
        for opcode, item in sorted(
            summary["opcodes"].items(),
            key=lambda pair: (-pair[1]["total"], pair[0]),
        ):
            values = [
                workload,
                opcode,
                str(item["total"]),
                str(item["legal"]),
                f"{item['legal_percent']:.6f}",
                *(str(item["actions"][action]) for action in ACTIONS),
            ]
            lines.append("\t".join(values))
    path.write_text("\n".join(lines) + "\n")


def write_query_tsv(path, overall, workloads):
    fields = [
        "workload",
        "opcode",
        "origin",
        "visit",
        "types",
        "memory",
        "action",
        "type_idx",
        "new_type",
        "count",
        "share_percent",
    ]
    lines = ["\t".join(fields)]
    summaries = [("TOTAL", overall), *[
        (item["workload"], item) for item in workloads
    ]]
    for workload, summary in summaries:
        for query in summary["queries"]:
            values = [
                workload,
                query["opcode"],
                query["origin"],
                query["visit"],
                ",".join(query["types"]) or "-",
                memory_signature(query["memory"]),
                query["action"],
                str(query["type_idx"]),
                query["new_type"] or "-",
                str(query["count"]),
                f"{100.0 * query['count'] / summary['total']:.6f}",
            ]
            lines.append("\t".join(values))
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
    data = {
        "schema_version": 3,
        "llvm_revision": compiler["revision"],
        "llvm_release": release,
        "compiler": compiler,
        "ctmark": ctmark,
        "ctmark_build_dir": str(build_dir),
        "overall": overall,
        "workloads": workloads,
        "files": records,
    }
    (output_dir / "profile.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n"
    )
    (output_dir / "profile.md").write_text(
        markdown(build_dir, compiler, release, ctmark, overall, workloads)
    )
    write_tsv(output_dir / "opcodes.tsv", overall, workloads)
    write_query_tsv(output_dir / "queries.tsv", overall, workloads)
    print(output_dir / "profile.json")
    print(output_dir / "profile.md")
    print(output_dir / "opcodes.tsv")
    print(output_dir / "queries.tsv")


def main():
    args = parse_args()
    llvm_build = args.llvm_build_dir.expanduser().resolve()
    test_suite = args.test_suite.expanduser().resolve()
    check_checkout(test_suite, "CTMark/CMakeLists.txt", "llvm-test-suite")
    checkout, clang = validate_llvm_build(llvm_build)
    ctmark_build = (
        args.ctmark_build_dir.expanduser().resolve()
        if args.ctmark_build_dir
        else Path.cwd() / "build-ctmark-gisel-legalizer-stats"
    )
    output_dir = (
        args.output_dir.expanduser().resolve()
        if args.output_dir
        else Path.cwd()
    )

    if not args.aggregate_only:
        configure_and_build_ctmark(
            test_suite,
            ctmark_build,
            clang,
            args.jobs,
            not args.no_clean,
        )
    elif not (ctmark_build / "build.ninja").is_file():
        fail(f"not a Ninja build directory: {ctmark_build}")

    write_report(
        output_dir,
        checkout,
        clang,
        ctmark_build,
        read_records(ctmark_build),
    )


if __name__ == "__main__":
    main()
