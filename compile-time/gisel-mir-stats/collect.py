#!/usr/bin/env python3

"""Collect CTMark generic MIR statistics using an existing LLVM build."""

import argparse
import json
import os
import re
import shlex
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


STAGES = (
    (
        "prelegalizer",
        "Before legalizer",
        "Input to the legalizer, after target pre-legalizer passes.",
    ),
    (
        "preregbankselect",
        "Before register-bank selection",
        "Input to register-bank selection, after target preparation passes.",
    ),
    (
        "preinstructionselect",
        "Before instruction selection",
        "Input to instruction selection, after target preparation passes.",
    ),
)
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
    parser.add_argument(
        "--output-dir",
        type=Path,
    )
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
    source = source_dir / "lib/CodeGen/MachineInstCount.cpp"
    if not source.is_file() or "mir-instcount-prelegalizer" not in source.read_text():
        fail(
            f"generic MIR statistics are missing from {checkout}; "
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
        ["ninja", "-C", str(build_dir), "-t", "compdb"],
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
        fail(f"output is outside build directory: {path}")


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


def stage_histograms(stats):
    result = {}
    for stage, _, _ in STAGES:
        prefix = f"mir-instcount-{stage}."
        opcode_prefix = prefix + "Num"
        opcodes = {}
        for name, count in stats.items():
            if name.startswith(opcode_prefix) and name.endswith("Inst"):
                opcodes[name[len(opcode_prefix) : -len("Inst")]] = count
        total_key = prefix + "TotalInsts"
        if opcodes or total_key in stats:
            result[stage] = {
                "generic_instructions": stats.get(total_key, 0),
                "opcodes": opcodes,
            }
    return result


def read_records(build_dir, selected):
    records = []
    seen_outputs = set()
    found_counters = False
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

        stats_path = (
            build_dir
            / output.parent
            / Path(entry["file"]).with_suffix(".stats").name
        )
        if not stats_path.is_file():
            fail(f"statistics file is missing: {stats_path}")
        stats = json.loads(stats_path.read_text())
        stages = stage_histograms(stats)
        found_counters |= bool(stages)
        for stage in stages.values():
            if (
                sum(stage["opcodes"].values())
                != stage["generic_instructions"]
            ):
                fail(f"incomplete MIR opcode histogram in {stats_path}")
        records.append(
            {
                "workload": workload,
                "source": source_label(entry["file"], workload),
                "object": output.as_posix(),
                "stats_file": stats_path.relative_to(build_dir).as_posix(),
                "stages": stages,
            }
        )
    if not found_counters:
        fail("no generic MIR statistics found")
    found_stages = {
        stage for record in records for stage in record["stages"]
    }
    for record in records:
        for stage in found_stages:
            record["stages"].setdefault(
                stage,
                {"generic_instructions": 0, "opcodes": {}},
            )
    return records


def aggregate(records):
    grouped = defaultdict(list)
    for record in records:
        grouped[record["workload"]].append(record)

    result = []
    for stage, title, description in STAGES:
        workloads = []
        for workload in sorted(grouped, key=str.casefold):
            files = [
                record
                for record in grouped[workload]
                if stage in record["stages"]
            ]
            if not files:
                continue
            opcodes = Counter()
            for record in files:
                opcodes.update(record["stages"][stage]["opcodes"])
            workloads.append(
                {
                    "workload": workload,
                    "files": len(files),
                    "generic_instructions": sum(opcodes.values()),
                    "opcodes": dict(opcodes),
                }
            )
        if workloads:
            result.append(
                {
                    "stage": stage,
                    "title": title,
                    "description": description,
                    "workloads": workloads,
                }
            )
    return result


def markdown(build_dir, compiler, release, ctmark, stages):
    lines = [
        "# CTMark generic MIR instruction mix",
        "",
        f"Build: `{build_dir.name}`",
        f"LLVM revision: `{compiler['revision']}`",
        f"LLVM release: `{release['tag']}` (`{release['revision'][:12]}`)",
        f"CTMark configuration: `{ctmark['configuration_id']}`",
        f"Target: `{ctmark['target']}`",
        "",
        "## Summary",
        "",
        "```text",
        f"{'stage':<28} {'files':>5} {'generic-instructions':>20}",
    ]
    for stage in stages:
        lines.append(
            f"{stage['stage']:<28} "
            f"{sum(item['files'] for item in stage['workloads']):>5} "
            f"{sum(item['generic_instructions'] for item in stage['workloads']):>20,}"
        )
    lines.append("```")
    for stage in stages:
        opcodes = Counter()
        for workload in stage["workloads"]:
            opcodes.update(workload["opcodes"])
        total = sum(opcodes.values())
        lines.extend(
            [
                "",
                f"## {stage['title']}",
                "",
                stage["description"],
                "",
                "### Workloads",
                "",
                "```text",
                f"{'workload':<18} {'files':>5} {'generic-instructions':>20}",
            ]
        )
        for workload in stage["workloads"]:
            lines.append(
                f"{workload['workload']:<18} {workload['files']:>5} "
                f"{workload['generic_instructions']:>20,}"
            )
        lines.append(
            f"{'TOTAL':<18} "
            f"{sum(item['files'] for item in stage['workloads']):>5} "
            f"{total:>20,}"
        )
        lines.extend(
            [
                "```",
                "",
                "### Overall opcode detail",
                "",
                "```text",
                f"{'opcode':<28} {'count':>12} {'share':>8}",
            ]
        )
        for opcode, count in sorted(
            opcodes.items(), key=lambda pair: (-pair[1], pair[0])
        ):
            lines.append(
                f"{opcode:<28} {count:>12,} {count / total:>8.2%}"
            )
        lines.extend(
            [
                f"{'TOTAL':<28} {total:>12,} {1:>8.2%}",
                "```",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def write_tsv(path, stages):
    lines = ["stage\tworkload\topcode\tcount\tshare"]
    for stage in stages:
        overall = Counter()
        for workload in stage["workloads"]:
            overall.update(workload["opcodes"])
        groups = [("TOTAL", overall)]
        groups.extend(
            (item["workload"], item["opcodes"])
            for item in stage["workloads"]
        )
        for workload, opcodes in groups:
            total = sum(opcodes.values())
            for opcode, count in sorted(
                opcodes.items(), key=lambda pair: (-pair[1], pair[0])
            ):
                lines.append(
                    f"{stage['stage']}\t{workload}\t{opcode}\t{count}\t"
                    f"{count / total:.6f}"
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


def main():
    args = parse_args()
    llvm_build = args.llvm_build_dir.expanduser().resolve()
    test_suite = args.test_suite.expanduser().resolve()
    check_checkout(test_suite, "CTMark/CMakeLists.txt", "llvm-test-suite")
    checkout, clang = validate_llvm_build(llvm_build)
    build_dir = (
        args.ctmark_build_dir.expanduser().resolve()
        if args.ctmark_build_dir
        else Path.cwd() / "build-ctmark-gisel-mir-stats"
    )
    output_dir = (
        args.output_dir.expanduser().resolve()
        if args.output_dir
        else Path.cwd()
    )

    if not args.aggregate_only:
        configure_and_build_ctmark(
            test_suite,
            build_dir,
            clang,
            args.jobs,
            not args.no_clean,
        )
    elif not (build_dir / "build.ninja").is_file():
        fail(f"not a Ninja build directory: {build_dir}")

    selected = set(args.workload)
    records = read_records(build_dir, selected)
    if not records:
        fail("no matching CTMark statistics found")
    found_workloads = {record["workload"] for record in records}
    missing = selected - found_workloads
    if missing:
        fail("unknown workload(s): " + ", ".join(sorted(missing)))

    stages = aggregate(records)
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
        "stages": stages,
        "files": records,
    }
    (output_dir / "profile.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n"
    )
    report = markdown(build_dir, compiler, release, ctmark, stages)
    (output_dir / "profile.md").write_text(report)
    write_tsv(output_dir / "opcodes.tsv", stages)

    print(output_dir / "profile.json")
    print(output_dir / "profile.md")
    print(output_dir / "opcodes.tsv")


if __name__ == "__main__":
    main()
