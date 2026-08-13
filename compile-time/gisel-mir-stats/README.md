# GlobalISel generic MIR statistics

`collect.py` takes an existing instrumented LLVM build, compiles CTMark at
`-O0 -g`, and aggregates generic MIR opcode counts at three GlobalISel pipeline
boundaries:

- before legalization;
- before register-bank selection;
- before instruction selection.

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

Run the collector from the directory where the CTMark build and reports should
be written:

```text
./collect.py ~/llvm-worktrees/compile-time-instrumentation/build
```

The CTMark build defaults to `build-ctmark-gisel-mir-stats` in the current
working directory. Override it with `--ctmark-build-dir`.

The script cleans and rebuilds CTMark by default. Use `--no-clean` for an
incremental run or `--aggregate-only` to regenerate reports from existing
statistics.

Outputs are written to the current working directory by default. Override this
with `--output-dir`.

- `profile.json`: complete per-file and aggregate data.
- `profile.md`: workload totals and overall opcode summaries for each stage.
- `opcodes.tsv`: complete stage, workload, and opcode matrix.

The JSON and Markdown record the instrumented LLVM revision embedded in the
supplied Clang binary, its underlying LLVM release, the target triple, and the
CTMark configuration. They do not use the source checkout's current `HEAD`.

Checked-in snapshots are organized by release and target/configuration:

```text
data/<release>/<target-architecture>-<configuration>/
```
