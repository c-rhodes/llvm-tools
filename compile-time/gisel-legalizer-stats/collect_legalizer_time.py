#!/usr/bin/env python3

"""Aggregate Clang's Legalizer pass timer over a configured CTMark build."""

import argparse
import json
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


TIMER_RE = re.compile(
    r"^\s*([0-9.]+)\s+\([^)]*\)\s+"
    r"([0-9.]+)\s+\([^)]*\)\s+"
    r"([0-9.]+)\s+\([^)]*\)\s+"
    r"([0-9.]+)\s+\([^)]*\)\s+(.+?)\s*$"
)


def run(command, **kwargs):
    return subprocess.run(command, check=True, text=True, **kwargs)


def arguments(entry):
    return entry.get("arguments") or shlex.split(entry["command"])


def workload_from_output(output):
    parts = Path(output).parts
    try:
        return parts[parts.index("CTMark") + 1]
    except (ValueError, IndexError):
        return None


def compile_command(entry):
    args = arguments(entry)
    compiler_index = next(
        (i for i, arg in enumerate(args) if Path(arg).name in ("clang", "clang++")),
        None,
    )
    if compiler_index is None:
        raise RuntimeError(f"no Clang compiler in command: {args}")
    args = args[compiler_index:]
    result = []
    skip_next = False
    options_with_values = {"-MF", "-MT", "-MQ", "-o"}
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg in options_with_values:
            skip_next = True
            continue
        if arg in ("-MD", "-MMD", "-MP"):
            continue
        result.append(arg)
    result.extend(["-ftime-report", "-o", "/dev/null"])
    return result


def timer_rows(stderr):
    sections = defaultdict(dict)
    section = None
    for line in stderr.splitlines():
        if "Pass execution timing report" in line:
            section = "passes"
            continue
        if "Clang time report" in line:
            section = "clang"
            continue
        if "timing report" in line and "Pass execution" not in line:
            section = None
            continue
        if section is None:
            continue
        match = TIMER_RE.match(line)
        if not match:
            continue
        user, system, cpu, wall, name = match.groups()
        sections[section][name] = {
            "user_seconds": float(user),
            "system_seconds": float(system),
            "cpu_seconds": float(cpu),
            "wall_seconds": float(wall),
        }
    return sections


def add_timing(total, timing):
    for key, value in timing.items():
        total[key] += value


def percent(numerator, denominator):
    return 100.0 * numerator / denominator if denominator else None


def markdown(metadata, workloads, overall):
    lines = [
        "# CTMark GlobalISel legalizer time",
        "",
        f"Compiler: `{metadata['compiler']}`",
        f"LLVM version: `{metadata['llvm_version']}`",
        f"CTMark configuration: `{metadata['ctmark_configuration']}`",
        f"Target: `{metadata['target']}`",
        f"Runs: `{metadata['runs']}` (serial compilation)",
        "",
        "Times come from Clang's `-ftime-report`. CPU time is user plus system "
        "time accumulated by LLVM's pass timers. Percentages are computed from "
        "the accumulated times, not averaged per-file percentages.",
        "",
        "## Summary",
        "",
        "```text",
        f"{'workload':<18} {'files':>5} {'visits':>12} {'legalizer':>12} "
        f"{'pass%':>8} {'clang%':>8} {'ns/visit':>10}",
    ]
    for item in workloads + [overall]:
        visits = item.get("visits")
        ns_per_visit = item["legalizer_cpu_seconds"] * 1e9 / visits if visits else None
        label = item.get("workload", "TOTAL")
        lines.append(
            f"{label:<18} {item['files']:>5} "
            f"{visits if visits is not None else 0:>12,} "
            f"{item['legalizer_cpu_seconds']:>10.3f} s "
            f"{item['legalizer_pass_percent']:>7.2f}% "
            f"{item['legalizer_clang_percent']:>7.2f}% "
            f"{ns_per_visit:>10.1f}"
        )
    lines.extend(
        [
            "```",
            "",
            "`pass%` is the Legalizer share of LLVM pass CPU time. `clang%` is "
            "the Legalizer share of total Clang CPU time. `ns/visit` pairs the "
            "timer with the legalizer visit counts from the companion profile.",
            "",
            "## Run-to-run totals",
            "",
            "```text",
            f"{'run':>3} {'legalizer':>12} {'pass total':>12} {'clang total':>12}",
        ]
    )
    for run in overall["runs"]:
        lines.append(
            f"{run['run']:>3} {run['legalizer_cpu_seconds']:>10.3f} s "
            f"{run['pass_cpu_seconds']:>10.3f} s "
            f"{run['clang_cpu_seconds']:>10.3f} s"
        )
    lines.extend(["```", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", type=Path)
    parser.add_argument("--visits-profile", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    build_dir = args.build_dir.resolve()
    compdb = json.loads(
        run(
            ["ninja", "-C", str(build_dir), "-t", "compdb"],
            stdout=subprocess.PIPE,
        ).stdout
    )
    records = []
    seen = set()
    for entry in compdb:
        output = entry.get("output")
        workload = workload_from_output(output) if output else None
        if workload is None or not output.endswith(".o") or output in seen:
            continue
        seen.add(output)
        records.append(
            {
                "workload": workload,
                "source": entry.get("file"),
                "output": output,
                "directory": entry.get("directory", str(build_dir)),
                "command": compile_command(entry),
                "runs": [],
            }
        )
    records.sort(key=lambda item: (item["workload"].casefold(), item["output"]))
    if not records:
        raise SystemExit("no CTMark compilation commands found")

    for run_number in range(1, args.runs + 1):
        current_workload = None
        for index, record in enumerate(records, 1):
            if record["workload"] != current_workload:
                current_workload = record["workload"]
                print(
                    f"run {run_number}/{args.runs}: {current_workload} "
                    f"({index}/{len(records)})",
                    flush=True,
                )
            proc = subprocess.run(
                record["command"],
                cwd=record["directory"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            if proc.returncode:
                sys.stderr.write(proc.stderr)
                raise SystemExit(
                    f"compile failed for {record['output']}: {proc.returncode}"
                )
            sections = timer_rows(proc.stderr)
            zero = {
                "user_seconds": 0.0,
                "system_seconds": 0.0,
                "cpu_seconds": 0.0,
                "wall_seconds": 0.0,
            }
            pass_total = sections["passes"].get("Total", zero)
            legalizer = sections["passes"].get("Legalizer", zero)
            clang_total = sections["clang"].get("Total", zero)
            record["runs"].append(
                {
                    "run": run_number,
                    "legalizer": legalizer,
                    "pass_total": pass_total,
                    "clang_total": clang_total,
                }
            )

    visits = {}
    visits_metadata = None
    if args.visits_profile:
        profile = json.loads(args.visits_profile.read_text())
        visits = {item["workload"]: item["total"] for item in profile["workloads"]}
        visits_metadata = profile.get("metadata")

    grouped = defaultdict(list)
    for record in records:
        grouped[record["workload"]].append(record)

    def summarize(workload_records, workload=None):
        run_summaries = []
        for run_number in range(1, args.runs + 1):
            sums = {
                "run": run_number,
                "legalizer_cpu_seconds": 0.0,
                "legalizer_wall_seconds": 0.0,
                "pass_cpu_seconds": 0.0,
                "pass_wall_seconds": 0.0,
                "clang_cpu_seconds": 0.0,
                "clang_wall_seconds": 0.0,
            }
            for record in workload_records:
                timing = record["runs"][run_number - 1]
                sums["legalizer_cpu_seconds"] += timing["legalizer"]["cpu_seconds"]
                sums["legalizer_wall_seconds"] += timing["legalizer"]["wall_seconds"]
                sums["pass_cpu_seconds"] += timing["pass_total"]["cpu_seconds"]
                sums["pass_wall_seconds"] += timing["pass_total"]["wall_seconds"]
                sums["clang_cpu_seconds"] += timing["clang_total"]["cpu_seconds"]
                sums["clang_wall_seconds"] += timing["clang_total"]["wall_seconds"]
            run_summaries.append(sums)
        result = {
            "files": len(workload_records),
            "visits": visits.get(workload) if workload else sum(visits.values()),
            "runs": run_summaries,
        }
        if workload:
            result["workload"] = workload
        for key in run_summaries[0]:
            if key == "run":
                continue
            result[key] = sum(run[key] for run in run_summaries) / args.runs
        result["legalizer_pass_percent"] = percent(
            result["legalizer_cpu_seconds"], result["pass_cpu_seconds"]
        )
        result["legalizer_clang_percent"] = percent(
            result["legalizer_cpu_seconds"], result["clang_cpu_seconds"]
        )
        return result

    workloads = [
        summarize(grouped[name], name) for name in sorted(grouped, key=str.casefold)
    ]
    overall = summarize(records)
    compiler = records[0]["command"][0]
    version = run([compiler, "--version"], stdout=subprocess.PIPE).stdout.splitlines()[0]
    metadata = {
        "compiler": compiler,
        "llvm_version": version,
        "ctmark_configuration": "aarch64-O0-g",
        "target": "aarch64-unknown-linux-gnu",
        "runs": args.runs,
        "visits_profile": str(args.visits_profile) if args.visits_profile else None,
        "visits_metadata": visits_metadata,
    }
    output = {
        "metadata": metadata,
        "overall": overall,
        "workloads": workloads,
        "files": records,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "legalizer-time.json").write_text(
        json.dumps(output, indent=2) + "\n"
    )
    (args.output_dir / "legalizer-time.md").write_text(
        markdown(metadata, workloads, overall)
    )


if __name__ == "__main__":
    main()
