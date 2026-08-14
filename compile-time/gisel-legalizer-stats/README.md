# GlobalISel legalizer statistics

`collect.py` takes an existing instrumented LLVM build, compiles CTMark at
`-O0 -g`, and aggregates the legalization action selected for every GlobalISel
legalizer visit. It records both opcode totals and the exact legality query:
generic types, memory type/alignment/orderings, selected action and mutation,
and whether the instruction was initial or generated and first-seen or
revisited.

In generated reports, `mem=[...]` entries are `LegalityQuery::MemDesc` values
formatted as `type@alignment-in-bits@ordering@failure-ordering`. Failure
ordering is only meaningful for compare-exchange.

See the checked-in example analysis for LLVM 23:
[AArch64 `-O0 -g`](data/llvmorg-23.1.0-rc3/aarch64-O0-g/profile.md).

The counters live on the
[`compile-time-instrumentation`](https://github.com/c-rhodes/llvm-project/tree/compile-time-instrumentation)
branch. The branch is maintained directly on top of the LLVM release being
measured.

Fetch it into an existing llvm-project checkout and create a worktree:

```text
git fetch https://github.com/c-rhodes/llvm-project.git compile-time-instrumentation:compile-time-instrumentation
git worktree add ~/llvm-worktrees/compile-time-instrumentation compile-time-instrumentation
```

Configure and build Clang with statistics enabled and the AArch64 target. For
example:

```text
cd ~/llvm-worktrees/compile-time-instrumentation
cmake -G Ninja -S llvm -B build -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_PROJECTS=clang -DLLVM_TARGETS_TO_BUILD=AArch64 -DLLVM_ENABLE_ASSERTIONS=ON
ninja -C build clang
```

`-DLLVM_FORCE_ENABLE_STATS=ON` can be used instead of enabling assertions.

CTMark uses `-save-stats=obj`, so every object has its own JSON statistics file
and the build can run in parallel safely.

Pass the LLVM build directory containing `bin/clang`:

```text
./collect.py ~/llvm-worktrees/compile-time-instrumentation/build
```

The CTMark build defaults to `build-ctmark-gisel-legalizer-stats` in the
current working directory. Override it with `--ctmark-build-dir`.

The script cleans and rebuilds CTMark by default. Use `--no-clean` for an
incremental run or `--aggregate-only` to regenerate reports from existing
statistics.

Outputs are written to the current working directory by default. Override this
with `--output-dir`.

- `profile.json`: complete per-file and aggregate data.
- `profile.md`: overall and per-workload opcode summaries, plus legal query
  signatures grouped by opcode overall and per workload.
- `opcodes.tsv`: action matrix for further analysis.
- `queries.tsv`: complete type-aware legality-query counts.

The JSON and Markdown record the instrumented LLVM revision embedded in the
supplied Clang binary, its underlying LLVM release, the target triple, and the
CTMark configuration. They do not use the source checkout's current `HEAD`.

Checked-in snapshots are organized by release and target/configuration:

```text
data/<release>/<target-architecture>-<configuration>/
```

The compiler's own build type is metadata rather than part of this path because
it does not change the legalization actions being counted.

The overall legal percentage is weighted by legalizer visits. It is not an
average of the per-file or per-workload percentages.
