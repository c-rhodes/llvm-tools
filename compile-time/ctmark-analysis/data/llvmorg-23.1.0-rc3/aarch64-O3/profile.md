# CTMark workload profile

Build: `build-compiletime-O3-llvmorg-23.1.0-rc3`

Dynamic metric: `instructions:u`

## Compiler instructions retired

```text
workload           files  compile      link     total
7zip                 212  145.12B   341.98M   145.46B
Bullet               121   74.73B   217.69M    74.95B
ClamAV                98   38.56B    88.52M    38.65B
consumer-typeset      51   24.14B    85.68M    24.23B
kimwitu++             14   27.93B   218.53M    28.15B
lencod                55   51.45B    95.64M    51.55B
mafft                 27   27.03B    67.52M    27.09B
SPASS                 51   30.86B    91.51M    30.95B
sqlite3                2   25.43B    52.34M    25.48B
tramp3d-v4             1   53.23B   188.32M    53.42B
```

## Generated code

```text
workload           funcs inst-count inst-count/funcs instructions:u/inst-count
7zip               4,030    239.06K            59.32                   607.04K
Bullet             2,393    142.95K            59.74                   522.78K
ClamAV               637    123.35K           193.65                   312.63K
consumer-typeset     371    106.37K           286.70                   227.00K
kimwitu++          3,482    119.36K            34.28                   233.98K
lencod               632    164.73K           260.65                   312.36K
mafft                331     87.16K           263.31                   310.08K
SPASS              1,087    118.88K           109.36                   259.61K
sqlite3              642    118.12K           184.00                   215.27K
tramp3d-v4         1,146    168.96K           147.44                   315.06K
```

## Instruction mix

Percent of static instructions. The groups account for every
instruction; `data` contains those not matched by another group.

```text
workload             load  store   branch   call     ret     fp   data
7zip                21.4%  12.8%    14.0%   7.7%    1.5%   0.1%  42.4%
Bullet              22.7%  13.3%     8.5%   3.9%    1.4%  22.4%  27.8%
ClamAV              16.2%   8.7%    16.6%   7.0%    0.9%   0.0%  50.5%
consumer-typeset    26.6%  17.6%    10.6%   4.8%    0.5%   0.6%  39.3%
kimwitu++           26.1%   7.8%     9.0%  10.6%    2.7%   0.0%  43.8%
lencod              30.7%  10.5%     9.3%   2.9%    0.5%   2.0%  44.2%
mafft               22.4%  10.6%    11.2%   4.7%    0.4%   9.8%  41.0%
SPASS               30.9%  12.5%    14.0%   6.6%    1.1%   0.0%  35.0%
sqlite3             22.1%  11.8%    16.5%   5.0%    1.0%   0.5%  43.0%
tramp3d-v4          23.0%  18.2%    10.5%   5.7%    0.6%   0.7%  41.3%
```
