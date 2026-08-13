# CTMark workload analysis

`collect.py` summarizes an existing CTMark build using its per-command perf
statistics, object files, and Ninja compilation database. It does not invoke
the compiler or rebuild CTMark.

See the checked-in example analyses for LLVM 23:
[AArch64 `-O3`](data/llvmorg-23.1.0-rc3/aarch64-O3/profile.md) and
[AArch64 `-O0 -g`](data/llvmorg-23.1.0-rc3/aarch64-O0-g/profile.md).

This analysis was motivated by revisiting
[llvm/llvm-project#215752](https://github.com/llvm/llvm-project/pull/215752)
and noticing that the patch made a larger difference in workloads with higher
function density, prompting the question of whether workload statistics could
expose that characteristic.

## Usage

Run the collector from the directory where the reports should be written:

```text
./collect.py CTMARK_BUILD
```

Outputs are written to the current working directory by default. Override this
with `--output-dir`.

- `profile.json`: complete per-file and aggregate data.
- `profile.md`: compact workload summary.

Use `--workload NAME` to restrict collection; the option may be repeated. Use
`--verbose` to include complete per-workload mnemonic histograms in Markdown.

## Derived statistics

`inst-count/funcs` is the average number of generated instructions per defined
function. Lower values indicate workloads with more small functions (higher
function density), where fixed per-function compiler costs are likely to be
more visible.

`instructions:u/inst-count` approximates compiler work per instruction of
output. Higher values identify workloads where compilation is disproportionately
expensive relative to the amount of generated code.
