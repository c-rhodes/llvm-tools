# CTMark GlobalISel legalizer actions

Build: `build-ctmark-gisel-legalizer-stats`
LLVM revision: `2b105932049c40edf98682b98c48666acad6c3fa`
LLVM release: `llvmorg-23.1.0-rc3` (`7196f931f212fc7c406066b2628a0ff4ea0ee344`)
CTMark configuration: `aarch64-O0-g`
Target: `aarch64-unknown-linux-gnu`

Counts are legalizer visits, including instructions created while legalizing.

## Summary

```text
workload           files       visits  legal-count   legal%
7zip                 212      416,874      381,881   91.61%
Bullet               121      334,130      317,654   95.07%
ClamAV                98      284,588      254,277   89.35%
consumer-typeset      51      326,316      274,237   84.04%
kimwitu++             14      212,129      188,309   88.77%
lencod                55      329,950      296,177   89.76%
mafft                 27      160,644      144,753   90.11%
SPASS                 51      182,235      161,165   88.44%
sqlite3                2      181,305      164,764   90.88%
tramp3d-v4             1      160,791      152,851   95.06%
TOTAL                632    2,588,962    2,336,068   90.23%
```

## Overall opcode detail

```text
opcode                             visits    share  legal-count   legal%
G_LOAD                            493,972   19.08%      493,462   99.90%
G_FRAME_INDEX                     386,893   14.94%      386,893  100.00%
G_CONSTANT                        328,064   12.67%      324,388   98.88%
G_STORE                           278,347   10.75%      275,693   99.05%
G_BRCOND                          224,964    8.69%      148,877   66.18%
G_BR                              204,751    7.91%      204,751  100.00%
G_PTR_ADD                         191,068    7.38%      191,068  100.00%
G_ICMP                            155,439    6.00%       76,227   49.04%
G_GLOBAL_VALUE                     64,488    2.49%            0    0.00%
G_SHL                              37,710    1.46%       32,243   85.50%
G_ADD                              32,336    1.25%       32,117   99.32%
G_SEXTLOAD                         29,956    1.16%       29,931   99.92%
G_AND                              20,987    0.81%       17,131   81.63%
G_ZEXTLOAD                         20,971    0.81%       20,961   99.95%
G_TRUNC                            15,113    0.58%       15,113  100.00%
G_INVOKE_REGION_START              12,072    0.47%       12,072  100.00%
G_PTRTOINT                          9,347    0.36%        5,518   59.03%
G_PHI                               7,950    0.31%        6,269   78.86%
G_MUL                               6,992    0.27%        6,989   99.96%
G_SUB                               6,900    0.27%        6,900  100.00%
G_LSHR                              6,617    0.26%        2,552   38.57%
G_SEXT                              5,871    0.23%        5,871  100.00%
G_ZEXT                              5,754    0.22%        5,754  100.00%
G_OR                                5,636    0.22%        4,661   82.70%
G_FCONSTANT                         4,803    0.19%        4,803  100.00%
G_FCMP                              3,654    0.14%        1,818   49.75%
G_ANYEXT                            3,463    0.13%        3,463  100.00%
G_FMUL                              3,236    0.12%        3,221   99.54%
G_SELECT                            2,870    0.11%        1,848   64.39%
G_ASHR                              2,754    0.11%        1,246   45.24%
G_FADD                              1,772    0.07%        1,768   99.77%
G_FMA                               1,582    0.06%        1,582  100.00%
G_SDIV                              1,477    0.06%        1,477  100.00%
G_XOR                               1,290    0.05%        1,211   93.88%
G_FSUB                              1,221    0.05%        1,220   99.92%
G_SITOFP                            1,177    0.05%        1,172   99.58%
G_FDIV                              1,020    0.04%        1,018   99.80%
G_FNEG                                900    0.03%          898   99.78%
G_INTTOPTR                            858    0.03%          858  100.00%
G_FPEXT                               775    0.03%          772   99.61%
G_UDIV                                655    0.03%          655  100.00%
G_MEMCPY                              575    0.02%            0    0.00%
G_TRAP                                432    0.02%          432  100.00%
G_FPTOSI                              367    0.01%          365   99.46%
G_UREM                                310    0.01%            0    0.00%
G_SREM                                304    0.01%            0    0.00%
G_FPTRUNC                             295    0.01%          294   99.66%
G_MEMSET                              213    0.01%            0    0.00%
G_MEMMOVE                             107    0.00%            0    0.00%
G_UMULH                                84    0.00%           84  100.00%
G_UMULO                                84    0.00%            0    0.00%
G_BRJT                                 75    0.00%           75  100.00%
G_JUMP_TABLE                           75    0.00%           75  100.00%
G_UITOFP                               73    0.00%           53   72.60%
G_FPTOUI                               59    0.00%           34   57.63%
G_FABS                                 55    0.00%           55  100.00%
G_SEXT_INREG                           40    0.00%           40  100.00%
G_FFLOOR                               26    0.00%           26  100.00%
G_VASTART                              24    0.00%           24  100.00%
G_BUILD_VECTOR                         17    0.00%           17  100.00%
G_UADDO                                14    0.00%            7   50.00%
G_BITCAST                               6    0.00%            6  100.00%
G_DYN_STACKALLOC                        5    0.00%            0    0.00%
G_UNMERGE_VALUES                        4    0.00%            4  100.00%
G_MERGE_VALUES                          3    0.00%            3  100.00%
G_FCEIL                                 2    0.00%            2  100.00%
G_IS_FPCLASS                            2    0.00%            0    0.00%
G_STACKRESTORE                          2    0.00%            0    0.00%
G_STACKSAVE                             2    0.00%            0    0.00%
G_ABS                                   1    0.00%            0    0.00%
G_CTLZ                                  1    0.00%            1  100.00%
```
