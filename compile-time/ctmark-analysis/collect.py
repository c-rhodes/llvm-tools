#!/usr/bin/env python3

"""Collect per-file workload statistics from a CTMark build."""

import argparse
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


LANGUAGES = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
}

DISASSEMBLY_LINE = re.compile(
    r"^\s*[0-9a-fA-F]+:\s+(?P<mnemonic>\S+)"
)


def fail(message):
    raise SystemExit(f"error: {message}")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="output directory (default: current working directory)",
    )
    parser.add_argument(
        "--workload",
        action="append",
        default=[],
        help="only analyze this workload; may be repeated",
    )
    parser.add_argument(
        "--metric",
        default="instructions:u",
        help="perfstat metric to read (default: instructions:u)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="include complete mnemonic histograms in the Markdown report",
    )
    parser.add_argument("--llvm-readelf", type=Path)
    parser.add_argument("--llvm-size", type=Path)
    parser.add_argument("--llvm-objdump", type=Path)
    return parser.parse_args()


def run(args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)


def load_compdb(build_dir):
    proc = run(
        ["ninja", "-C", str(build_dir), "-t", "compdb"],
        stdout=subprocess.PIPE,
    )
    return {
        entry["output"]: entry
        for entry in json.loads(proc.stdout)
        if entry.get("command") and entry.get("output")
    }


def workload_from_path(path):
    parts = path.parts
    try:
        return parts[parts.index("CTMark") + 1]
    except (ValueError, IndexError):
        fail(f"cannot determine CTMark workload from {path}")


def read_perfstat(path, metric):
    for line in path.read_text().splitlines():
        fields = line.split(";")
        if len(fields) >= 3 and fields[2] == metric:
            try:
                return int(fields[0])
            except ValueError:
                fail(f"invalid {metric} value in {path}: {fields[0]!r}")
    fail(f"metric {metric!r} not found in {path}")


def source_label(source, workload):
    parts = Path(source).parts
    try:
        index = parts.index(workload)
        return Path(*parts[index + 1 :]).as_posix()
    except ValueError:
        return Path(source).name


def tool_path(option, name):
    if option:
        if not option.is_file():
            fail(f"tool does not exist: {option}")
        return option
    found = shutil.which(name)
    if not found:
        fail(f"cannot find {name}; pass --{name}")
    return Path(found)


def count_defined_functions(readelf, obj):
    proc = run(
        [str(readelf), "--symbols", str(obj)],
        stdout=subprocess.PIPE,
    )
    count = 0
    for line in proc.stdout.splitlines():
        fields = line.split(maxsplit=7)
        if len(fields) >= 7 and fields[3] in {"FUNC", "IFUNC"}:
            if fields[6] != "UND":
                count += 1
    return count


def section_sizes(size_tool, obj):
    proc = run(
        [str(size_tool), "-A", str(obj)],
        stdout=subprocess.PIPE,
    )
    text_bytes = 0
    debug_bytes = 0
    for line in proc.stdout.splitlines():
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            size = int(fields[1])
        except ValueError:
            continue
        if fields[0].startswith((".text", "__text")):
            text_bytes += size
        if fields[0].startswith((".debug", "__debug")):
            debug_bytes += size
    return text_bytes, debug_bytes


def target_instruction_histogram(objdump, obj):
    proc = run(
        [str(objdump), "-d", "--no-show-raw-insn", str(obj)],
        stdout=subprocess.PIPE,
    )
    mnemonics = Counter()
    for line in proc.stdout.splitlines():
        match = DISASSEMBLY_LINE.match(line)
        if match:
            mnemonics[match.group("mnemonic")] += 1
    return dict(mnemonics)


def add_object_stats(record, obj, readelf, size_tool, objdump):
    text_bytes, debug_bytes = section_sizes(size_tool, obj)
    mnemonics = target_instruction_histogram(objdump, obj)
    record.update(
        {
            "defined_functions": count_defined_functions(readelf, obj),
            "target_instructions": sum(mnemonics.values()),
            "mnemonics": mnemonics,
            "text_bytes": text_bytes,
            "debug_bytes": debug_bytes,
            "object_bytes": obj.stat().st_size,
        }
    )


def format_count(value):
    if value is None:
        return "-"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.2f}K"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def format_integer(value):
    return "-" if value is None else f"{value:,}"


def ratio(numerator, denominator):
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def instruction_group(mnemonic):
    if mnemonic.startswith("ld"):
        return "loads"
    if mnemonic.startswith("st"):
        return "stores"
    if mnemonic == "bl" or mnemonic.startswith("blr"):
        return "calls"
    if mnemonic.startswith("ret"):
        return "returns"
    if (
        mnemonic in {"b", "br", "brk"}
        or mnemonic.startswith(("b.", "cb", "tb"))
    ):
        return "branches"
    if mnemonic.startswith("f") or mnemonic in {"scvtf", "ucvtf"}:
        return "fp"
    return "data"


def group_instructions(mnemonics):
    groups = Counter()
    for mnemonic, count in mnemonics.items():
        groups[instruction_group(mnemonic)] += count
    return groups


def aggregate(records, links):
    grouped = defaultdict(list)
    for record in records:
        grouped[record["workload"]].append(record)
    link_instructions = defaultdict(int)
    for link in links:
        link_instructions[link["workload"]] += link["instructions"]

    result = []
    for workload in sorted(grouped, key=str.casefold):
        files = grouped[workload]
        analyzed = [r for r in files if r["defined_functions"] is not None]
        complete = len(analyzed) == len(files)
        functions = sum(r["defined_functions"] for r in analyzed)
        target_instructions = sum(r["target_instructions"] for r in analyzed)
        mnemonics = Counter()
        for record in analyzed:
            mnemonics.update(record["mnemonics"])
        instructions = sum(r["compiler_instructions"] for r in files)
        linker_instructions = link_instructions[workload]
        result.append(
            {
                "workload": workload,
                "files": len(files),
                "analyzed_files": len(analyzed),
                "compiler_instructions": instructions,
                "linker_instructions": linker_instructions,
                "total_instructions": instructions + linker_instructions,
                "defined_functions": functions if complete else None,
                "target_instructions": target_instructions if complete else None,
                "mnemonics": dict(mnemonics) if complete else None,
                "target_instructions_per_function": ratio(
                    target_instructions if complete else None,
                    functions if complete else None,
                ),
                "compiler_instructions_per_target_instruction": ratio(
                    instructions,
                    target_instructions if complete else None,
                ),
                "text_bytes": (
                    sum(r["text_bytes"] for r in analyzed)
                    if complete
                    else None
                ),
                "debug_bytes": (
                    sum(r["debug_bytes"] for r in analyzed)
                    if complete
                    else None
                ),
            }
        )
    return result


def markdown(build_dir, metric, workloads, verbose):
    lines = [
        "# CTMark workload profile",
        "",
        f"Build: `{build_dir.name}`",
        "",
        f"Dynamic metric: `{metric}`",
        "",
        "## Compiler instructions retired",
        "",
        "```text",
        "workload           files  compile      link     total",
    ]
    for item in workloads:
        lines.append(
            f"{item['workload']:<18} {item['files']:>5}  "
            f"{format_count(item['compiler_instructions']):>7}  "
            f"{format_count(item['linker_instructions']):>8}  "
            f"{format_count(item['total_instructions']):>8}"
        )
    lines.append("```")

    lines.extend(
        [
            "",
            "## Generated code",
            "",
            "```text",
            f"{'workload':<16} {'funcs':>7} {'inst-count':>10} "
            f"{'inst-count/funcs':>16} {'instructions:u/inst-count':>25}",
        ]
    )
    for item in workloads:
        target_per_function = item["target_instructions_per_function"]
        compile_per_target = item[
            "compiler_instructions_per_target_instruction"
        ]
        lines.append(
            f"{item['workload']:<16} "
            f"{format_integer(item['defined_functions']):>7} "
            f"{format_count(item['target_instructions']):>10} "
            f"{format_count(target_per_function):>16} "
            f"{format_count(compile_per_target):>25}"
        )
    lines.append("```")

    lines.extend(
        [
            "",
            "## Instruction mix",
            "",
            "Percent of static instructions. The groups account for every",
            "instruction; `data` contains those not matched by another group.",
            "",
            "```text",
            f"{'workload':<18} {'load':>6} {'store':>6} {'branch':>8} "
            f"{'call':>6} {'ret':>7} {'fp':>6} {'data':>6}",
        ]
    )
    for item in workloads:
        mnemonics = item["mnemonics"]
        if mnemonics is None:
            continue
        total = sum(mnemonics.values())
        if total != item["target_instructions"]:
            fail(f"incomplete mnemonic histogram for {item['workload']}")
        groups = group_instructions(mnemonics)
        lines.append(
            f"{item['workload']:<18} "
            + " ".join(
                f"{groups[group] / total:>{width}.1%}"
                for group, width in (
                    ("loads", 6),
                    ("stores", 6),
                    ("branches", 8),
                    ("calls", 6),
                    ("returns", 7),
                    ("fp", 6),
                    ("data", 6),
                )
            )
        )
    lines.append("```")

    if verbose:
        lines.extend(
            [
                "",
                "## Mnemonic detail",
                "",
                "Every disassembled instruction appears in one mnemonic row.",
            ]
        )
    detail_workloads = workloads if verbose else []
    for item in detail_workloads:
        mnemonics = item["mnemonics"]
        if mnemonics is None:
            continue
        total = sum(mnemonics.values())
        lines.extend(
            [
                "",
                f"### {item['workload']}",
                "",
                "```text",
                "mnemonic             count    share",
            ]
        )
        for mnemonic, count in sorted(
            mnemonics.items(), key=lambda pair: (-pair[1], pair[0])
        ):
            lines.append(f"{mnemonic:<16} {count:>10,} {count / total:>8.2%}")
        lines.append(f"{'TOTAL':<16} {total:>10,} {1:>8.2%}")
        lines.append("```")

    if any(item["defined_functions"] is None for item in workloads):
        lines.extend(
            [
                "",
                "Function and object statistics are shown only when every object in",
                "the workload is present in the build directory.",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def main():
    args = parse_args()
    build_dir = args.build_dir.resolve()
    if not (build_dir / "build.ninja").is_file():
        fail(f"not a Ninja build directory: {build_dir}")

    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else Path.cwd()
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    compdb = load_compdb(build_dir)
    selected = set(args.workload)
    records = []
    perfstats = sorted((build_dir / "CTMark").glob("**/*.o.time.perfstats"))
    for perfstat in perfstats:
        workload = workload_from_path(perfstat)
        if selected and workload not in selected:
            continue
        relative_perfstat = perfstat.relative_to(build_dir)
        object_name = relative_perfstat.as_posix().removesuffix(
            ".time.perfstats"
        )
        entry = compdb.get(object_name)
        if entry is None:
            fail(f"no compilation database entry for {object_name}")
        source = source_label(entry["file"], workload)
        records.append(
            {
                "workload": workload,
                "source": source,
                "language": LANGUAGES.get(Path(entry["file"]).suffix, "unknown"),
                "object": object_name,
                "compiler_instructions": read_perfstat(
                    perfstat, args.metric
                ),
                "defined_functions": None,
                "target_instructions": None,
                "mnemonics": None,
                "text_bytes": None,
                "debug_bytes": None,
                "object_bytes": None,
                "_compdb": entry,
            }
        )

    if not records:
        fail("no matching CTMark object perfstats found")

    found_workloads = {record["workload"] for record in records}
    missing = selected - found_workloads
    if missing:
        fail("unknown or unmeasured workload(s): " + ", ".join(sorted(missing)))

    links = []
    for perfstat in sorted((build_dir / "CTMark").glob("**/*.link.time.perfstats")):
        workload = workload_from_path(perfstat)
        if selected and workload not in selected:
            continue
        links.append(
            {
                "workload": workload,
                "step": perfstat.name.removesuffix(".time.perfstats"),
                "instructions": read_perfstat(perfstat, args.metric),
            }
        )

    readelf = tool_path(args.llvm_readelf, "llvm-readelf")
    size_tool = tool_path(args.llvm_size, "llvm-size")
    objdump = tool_path(args.llvm_objdump, "llvm-objdump")
    for record in records:
        obj = build_dir / record["object"]
        if obj.is_file():
            add_object_stats(record, obj, readelf, size_tool, objdump)
        del record["_compdb"]

    workloads = aggregate(records, links)
    data = {
        "schema_version": 2,
        "build_dir": str(build_dir),
        "metric": args.metric,
        "workloads": workloads,
        "files": records,
        "links": links,
    }
    (output_dir / "profile.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n"
    )
    report = markdown(build_dir, args.metric, workloads, args.verbose)
    (output_dir / "profile.md").write_text(report)
    long_lines = [
        number
        for number, line in enumerate(report.splitlines(), 1)
        if len(line) > 78
    ]
    if long_lines:
        fail("Markdown lines exceed 78 columns: " + ", ".join(map(str, long_lines)))

    print(output_dir / "profile.json")
    print(output_dir / "profile.md")


if __name__ == "__main__":
    main()
