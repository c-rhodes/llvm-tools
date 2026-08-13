# CTMark workload profile

Build: `build-compiletime-O0-g-llvmorg-23.1.0-rc3`

Dynamic metric: `instructions:u`

## Compiler instructions retired

```text
workload           files  compile      link     total
7zip                 212   98.34B   720.22M    99.06B
Bullet               121   44.73B   560.80M    45.29B
ClamAV                98   10.99B   132.28M    11.12B
consumer-typeset      51    9.49B   143.72M     9.63B
kimwitu++             14   16.51B   432.61M    16.94B
lencod                55   10.03B   154.41M    10.19B
mafft                 27    5.31B    84.75M     5.39B
SPASS                 51   10.61B   131.41M    10.74B
sqlite3                2    3.62B    59.29M     3.68B
tramp3d-v4             1   14.37B   772.54M    15.14B
```

## Generated code

```text
workload           funcs inst-count inst-count/funcs instructions:u/inst-count
7zip              10,762    339.55K            31.55                   289.62K
Bullet             9,384    320.49K            34.15                   139.56K
ClamAV               956    175.30K           183.37                    62.69K
consumer-typeset     453    227.40K           501.98                    41.72K
kimwitu++          6,220    207.71K            33.39                    79.49K
lencod               830    203.86K           245.61                    49.21K
mafft                410    104.66K           255.26                    50.70K
SPASS              4,310    161.16K            37.39                    65.81K
sqlite3            1,082    110.98K           102.57                    32.60K
tramp3d-v4         9,618    224.28K            23.32                    64.06K
```

## Instruction mix

Percent of static instructions. The groups account for every
instruction; `data` contains those not matched by another group.

```text
workload             load  store   branch   call     ret     fp   data
7zip                29.2%  19.8%    15.0%   7.8%    2.8%   0.0%  25.3%
Bullet              31.8%  23.9%     8.1%   9.5%    2.8%   2.9%  21.0%
ClamAV              34.7%  13.6%    21.0%   5.8%    0.5%   0.0%  24.4%
consumer-typeset    41.3%  13.9%    16.1%   2.7%    0.2%   0.2%  25.6%
kimwitu++           33.4%  17.9%    11.9%  10.7%    2.8%   0.0%  23.3%
lencod              43.4%  12.4%    15.0%   2.5%    0.4%   0.9%  25.4%
mafft               38.5%  15.6%    16.6%   3.6%    0.4%   3.4%  22.0%
SPASS               29.9%  16.8%    16.3%  16.1%    2.7%   0.0%  18.3%
sqlite3             38.5%  15.3%    20.1%   5.6%    1.0%   0.2%  19.2%
tramp3d-v4          29.7%  22.6%     4.7%  13.4%    4.3%   0.4%  25.0%
```
