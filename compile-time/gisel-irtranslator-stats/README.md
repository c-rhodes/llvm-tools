# GlobalISel IRTranslator statistics

`collect.py` takes an existing instrumented LLVM build, compiles CTMark at
`-O0 -g`, and aggregates the IR instructions presented to GlobalISel's
IRTranslator. It records exact IR opcode/result/operand type signatures and
GEP lowering shapes, along with detailed non-intrinsic call-lowering
signatures, including original and ABI-split argument types and flags.

The counters live on the `compile-time-instrumentation` branch. Configure and
build Clang with statistics enabled and the AArch64 target, for example:

```text
cd ~/llvm-worktrees/compile-time-instrumentation
cmake -G Ninja -S llvm -B build -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_PROJECTS=clang -DLLVM_TARGETS_TO_BUILD=AArch64 -DLLVM_ENABLE_ASSERTIONS=ON
ninja -C build clang
```

Run the collector from the worktree root so its CTMark directory also remains
inside the worktree:

```text
~/llvm-tools/compile-time/gisel-irtranslator-stats/collect.py build --output-dir gisel-irtranslator-stats-output
```

The CTMark build defaults to `build-ctmark-gisel-irtranslator-stats` in the
current directory. Override it with `--ctmark-build-dir`. The script cleans and
rebuilds CTMark by default; use `--no-clean` for an incremental run or
`--aggregate-only` to regenerate reports from existing statistics.

Outputs are written to the current directory by default. The example uses
`--output-dir` to keep generated reports together.

- `profile.json`: per-file totals and complete aggregate/workload data.
- `profile.md`: workload, opcode/type, and concise call/flag summaries.
- `gep.md`: GEP category descriptions and human-readable summaries.
- `instructions.tsv`: complete workload/opcode/type matrix.
- `calls.tsv`: complete workload/call-signature matrix.
- `gep.tsv`: complete workload/GEP-lowering-shape matrix.
- `gep-i8-ptr-adds.tsv`: scalar single-index i8 and emitted-pointer-add data.

Checked-in snapshots are organized by release and target/configuration:

```text
data/<release>/<target-architecture>-<configuration>/
```

Counts describe IRTranslator inputs, not all IR instructions in the module:
intrinsics translated by dedicated paths are included in the instruction
tables, while the detailed call tables contain only call/invoke sites that
reach generic call lowering.
