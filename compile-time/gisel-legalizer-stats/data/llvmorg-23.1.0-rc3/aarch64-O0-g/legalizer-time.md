# CTMark GlobalISel legalizer time

Compiler: `/opt/llvm-23.1.0-rc3/bin/clang`
LLVM version: `clang version 23.1.0-rc3 (https://github.com/llvm/llvm-project 7196f931f212fc7c406066b2628a0ff4ea0ee344)`
CTMark configuration: `aarch64-O0-g`
Target: `aarch64-unknown-linux-gnu`
Runs: `3` (serial compilation)

Times come from Clang's `-ftime-report`. CPU time is user plus system time accumulated by LLVM's pass timers. Percentages are computed from the accumulated times, not averaged per-file percentages.

## Summary

```text
workload           files       visits    legalizer    pass%   clang%   ns/visit
7zip                 212      416,874      0.156 s    5.08%    0.52%      374.4
Bullet               121      334,130      0.113 s    4.09%    0.83%      337.4
ClamAV                98      284,588      0.082 s    8.73%    2.34%      288.8
consumer-typeset      51      326,316      0.109 s   10.79%    3.91%      333.4
kimwitu++             14      212,129      0.078 s    4.70%    1.24%      367.1
lencod                55      329,950      0.084 s    8.85%    2.79%      254.4
mafft                 27      160,644      0.039 s    8.10%    2.49%      245.3
SPASS                 51      182,235      0.063 s    5.03%    1.55%      344.4
sqlite3                2      181,305      0.050 s    7.96%    4.04%      277.8
tramp3d-v4             1      160,791      0.072 s    3.11%    1.06%      446.1
TOTAL                632    2,588,962      0.846 s    5.62%    1.16%      326.7
```

`pass%` is the Legalizer share of LLVM pass CPU time. `clang%` is the Legalizer share of total Clang CPU time. `ns/visit` pairs the timer with the legalizer visit counts from the companion profile.

## Run-to-run totals

```text
run    legalizer   pass total  clang total
  1      0.846 s     15.057 s     73.101 s
  2      0.847 s     15.070 s     73.163 s
  3      0.844 s     15.051 s     73.093 s
```
