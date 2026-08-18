# CTMark GlobalISel IRTranslator statistics

Build: `build-ctmark-gisel-irtranslator-stats`
LLVM revision: `768a0d0bb370131449ed69ee90b9c47c01be5609`
LLVM release: `llvmorg-23.1.0-rc3` (`7196f931f212fc7c406066b2628a0ff4ea0ee344`)
CTMark configuration: `aarch64-O0-g`
Target: `aarch64-unknown-linux-gnu`

IR instruction counts are inputs presented to `IRTranslator::translate`. Call counts are non-intrinsic call/invoke sites reaching generic call lowering.

In IR type tables, `opcode%` is the share of that opcode and `total%` is the share of all translated IR instructions.

## Summary

```text
workload           files     IR insts      calls     direct
7zip                 212      295,264     26,903     25,162
Bullet               121      270,676     30,272     29,174
ClamAV                98      174,246      9,921      9,807
consumer-typeset      51      241,823      6,037      5,999
kimwitu++             14      166,704     22,191     17,054
lencod                55      213,919      4,882      4,678
mafft                 27      103,370      3,708      3,704
SPASS                 51      136,769     25,917     25,867
sqlite3                2      114,357      6,079      5,995
tramp3d-v4             1      168,264     30,052     30,026
TOTAL                632    1,885,392    165,962    157,466
```

## Overall call summary

```text
property             value                       count    share
kind                 call                      153,890   92.73%
kind                 invoke                     12,072    7.27%
callee               direct                    157,466   94.88%
callee               indirect                    8,496    5.12%
calling convention   0                         165,962  100.00%
vararg               no                        159,466   96.09%
vararg               yes                         6,496    3.91%
tail                 no                        165,268   99.58%
tail                 yes                           694    0.42%
musttail             no                        165,962  100.00%
lowerable return     yes                       165,962  100.00%
features             none                      165,962  100.00%
```

### `ArgFlagsTy` summary

Counts are ABI-split `ArgFlagsTy` values with the flag set, across 403,845 values. Flags can coexist, so shares do not sum to 100%.
`pointer` is type-derived. `vararg` marks non-fixed argument values, so it need not match the vararg call count above.

```text
flag                        count     share
pointer                   287,363    71.16%
vararg                      5,771     1.43%
sret                        3,192     0.79%
consecutive-last            2,799     0.69%
consecutive                   318     0.08%
byref                           0     0.00%
byval                           0     0.00%
cfguardtarget                   0     0.00%
copy-elision                    0     0.00%
hva                             0     0.00%
hva-start                       0     0.00%
inalloca                        0     0.00%
inreg                           0     0.00%
nest                            0     0.00%
noext                           0     0.00%
preallocated                    0     0.00%
returned                        0     0.00%
second-arg                      0     0.00%
sext                            0     0.00%
split                           0     0.00%
split-end                       0     0.00%
swiftasync                      0     0.00%
swifterror                      0     0.00%
swiftself                       0     0.00%
zext                            0     0.00%
```

Type-shape tables merge flags and other call properties and show the 20 most common shapes.

### Original IR type shapes

```text
       count    share  types
      33,142   19.97%  [ptr] -> void
      23,605   14.22%  [ptr] -> ptr
      14,889    8.97%  [ptr] -> i32
       9,005    5.43%  [ptr,ptr] -> void
       8,356    5.03%  [ptr,ptr,ptr] -> void
       6,810    4.10%  [ptr,ptr] -> ptr
       5,625    3.39%  [ptr,i32] -> ptr
       4,828    2.91%  [ptr,ptr] -> i32
       3,069    1.85%  [ptr,i32] -> void
       2,782    1.68%  [ptr,ptr,ptr,ptr] -> void
       2,757    1.66%  [-] -> ptr
       2,256    1.36%  [ptr,ptr] -> %class.btVector3
       2,240    1.35%  [-] -> void
       2,077    1.25%  [ptr,i64] -> void
       1,953    1.18%  [ptr] -> i64
       1,728    1.04%  [i32] -> i32
       1,633    0.98%  [i64] -> ptr
       1,584    0.95%  [ptr,i32] -> i32
       1,471    0.89%  [ptr,ptr,ptr] -> i32
       1,375    0.83%  [ptr] -> i1
```

### ABI-split type shapes

```text
       count    share  types
      33,142   19.97%  [ptr] -> void
      23,605   14.22%  [ptr] -> ptr
      14,889    8.97%  [ptr] -> i32
       9,005    5.43%  [ptr,ptr] -> void
       8,356    5.03%  [ptr,ptr,ptr] -> void
       6,810    4.10%  [ptr,ptr] -> ptr
       5,625    3.39%  [ptr,i32] -> ptr
       4,828    2.91%  [ptr,ptr] -> i32
       3,069    1.85%  [ptr,i32] -> void
       2,782    1.68%  [ptr,ptr,ptr,ptr] -> void
       2,757    1.66%  [-] -> ptr
       2,291    1.38%  [ptr,ptr] -> float,float,float,float
       2,240    1.35%  [-] -> void
       2,077    1.25%  [ptr,i64] -> void
       1,953    1.18%  [ptr] -> i64
       1,728    1.04%  [i32] -> i32
       1,633    0.98%  [i64] -> ptr
       1,584    0.95%  [ptr,i32] -> i32
       1,471    0.89%  [ptr,ptr,ptr] -> i32
       1,375    0.83%  [ptr] -> i1
```

## Overall opcode detail

```text
opcode                          count    share
load                          543,843   28.85%
getelementptr                 273,741   14.52%
store                         260,902   13.84%
br                            188,681   10.01%
call                          160,283    8.50%
alloca                        151,238    8.02%
icmp                           71,618    3.80%
ret                            42,065    2.23%
sext                           36,073    1.91%
add                            27,993    1.48%
zext                           27,560    1.46%
invoke                         12,072    0.64%
extractvalue                   11,171    0.59%
sub                            10,115    0.54%
phi                             7,980    0.42%
and                             7,223    0.38%
trunc                           5,533    0.29%
landingpad                      4,684    0.25%
unreachable                     4,180    0.22%
shl                             4,146    0.22%
mul                             4,002    0.21%
or                              3,665    0.19%
fmul                            3,234    0.17%
lshr                            2,676    0.14%
xor                             2,432    0.13%
ptrtoint                        1,854    0.10%
fcmp                            1,827    0.10%
fadd                            1,770    0.09%
switch                          1,548    0.08%
ashr                            1,502    0.08%
fsub                            1,221    0.06%
sdiv                            1,173    0.06%
sitofp                          1,170    0.06%
fdiv                            1,020    0.05%
select                          1,001    0.05%
fneg                              900    0.05%
inttoptr                          814    0.04%
fpext                             775    0.04%
fptosi                            366    0.02%
udiv                              345    0.02%
urem                              310    0.02%
srem                              304    0.02%
fptrunc                           295    0.02%
uitofp                             53    0.00%
fptoui                             34    0.00%
```

## Opcode detail by workload

### 7zip

```text
opcode                          count    share
load                           70,905   24.01%
store                          48,478   16.42%
getelementptr                  37,030   12.54%
br                             30,872   10.46%
alloca                         28,049    9.50%
call                           20,780    7.04%
icmp                           11,142    3.77%
ret                             9,601    3.25%
invoke                          7,023    2.38%
zext                            5,852    1.98%
extractvalue                    5,122    1.73%
add                             5,031    1.70%
landingpad                      2,750    0.93%
sext                            2,223    0.75%
unreachable                     1,963    0.66%
sub                             1,859    0.63%
shl                             1,034    0.35%
trunc                             932    0.32%
or                                797    0.27%
and                               673    0.23%
lshr                              655    0.22%
phi                               509    0.17%
xor                               470    0.16%
mul                               367    0.12%
switch                            288    0.10%
select                            279    0.09%
ptrtoint                          226    0.08%
sdiv                              123    0.04%
udiv                              103    0.03%
ashr                              100    0.03%
srem                               16    0.01%
urem                               11    0.00%
inttoptr                            1    0.00%
```

### Bullet

```text
opcode                          count    share
load                           64,117   23.69%
store                          43,210   15.96%
getelementptr                  42,670   15.76%
alloca                         35,155   12.99%
call                           29,156   10.77%
br                             15,712    5.80%
ret                             9,052    3.34%
extractvalue                    4,848    1.79%
icmp                            4,377    1.62%
invoke                          4,235    1.56%
sext                            2,870    1.06%
fmul                            2,298    0.85%
add                             2,047    0.76%
fcmp                            1,326    0.49%
landingpad                      1,294    0.48%
unreachable                     1,178    0.44%
fadd                              977    0.36%
zext                              916    0.34%
fsub                              818    0.30%
fneg                              806    0.30%
phi                               792    0.29%
fdiv                              510    0.19%
mul                               459    0.17%
sub                               347    0.13%
and                               345    0.13%
sitofp                            145    0.05%
trunc                             124    0.05%
or                                113    0.04%
ptrtoint                          106    0.04%
select                             97    0.04%
sdiv                               83    0.03%
fpext                              70    0.03%
srem                               69    0.03%
shl                                65    0.02%
switch                             51    0.02%
fptrunc                            42    0.02%
lshr                               39    0.01%
xor                                35    0.01%
ashr                               30    0.01%
fptoui                             27    0.01%
uitofp                             26    0.01%
fptosi                             16    0.01%
inttoptr                           10    0.00%
udiv                                8    0.00%
urem                                5    0.00%
```

### ClamAV

```text
opcode                          count    share
load                           55,676   31.95%
br                             24,635   14.14%
getelementptr                  22,296   12.80%
store                          20,667   11.86%
icmp                           11,043    6.34%
call                           10,214    5.86%
alloca                          6,656    3.82%
zext                            6,420    3.68%
add                             3,909    2.24%
sub                             1,880    1.08%
sext                            1,755    1.01%
and                             1,573    0.90%
trunc                           1,374    0.79%
shl                             1,077    0.62%
ret                               956    0.55%
or                                865    0.50%
lshr                              742    0.43%
xor                               611    0.35%
phi                               498    0.29%
mul                               384    0.22%
ptrtoint                          299    0.17%
ashr                              187    0.11%
switch                            155    0.09%
select                            111    0.06%
udiv                               96    0.06%
urem                               73    0.04%
sdiv                               40    0.02%
srem                               26    0.01%
unreachable                        22    0.01%
fdiv                                1    0.00%
fmul                                1    0.00%
fptosi                              1    0.00%
fptoui                              1    0.00%
fsub                                1    0.00%
uitofp                              1    0.00%
```

### consumer-typeset

```text
opcode                          count    share
load                           72,891   30.14%
getelementptr                  71,464   29.55%
store                          27,229   11.26%
br                             26,076   10.78%
icmp                           10,026    4.15%
zext                            6,597    2.73%
call                            6,060    2.51%
sext                            4,624    1.91%
and                             3,603    1.49%
alloca                          3,286    1.36%
phi                             2,871    1.19%
or                              1,420    0.59%
lshr                            1,124    0.46%
add                             1,090    0.45%
trunc                             736    0.30%
shl                               721    0.30%
sub                               531    0.22%
ret                               452    0.19%
mul                               156    0.06%
sitofp                            116    0.05%
sdiv                               95    0.04%
switch                             93    0.04%
fpext                              79    0.03%
select                             69    0.03%
fptosi                             68    0.03%
ptrtoint                           64    0.03%
fdiv                               54    0.02%
fmul                               52    0.02%
fcmp                               40    0.02%
srem                               35    0.01%
fptrunc                            16    0.01%
fneg                               15    0.01%
udiv                               15    0.01%
xor                                14    0.01%
urem                               11    0.00%
fadd                               10    0.00%
fsub                               10    0.00%
unreachable                         7    0.00%
ashr                                2    0.00%
inttoptr                            1    0.00%
```

### kimwitu++

```text
opcode                          count    share
load                           52,270   31.35%
store                          23,938   14.36%
call                           21,546   12.92%
alloca                         18,034   10.82%
getelementptr                  17,399   10.44%
br                             15,566    9.34%
ret                             5,843    3.51%
icmp                            4,556    2.73%
extractvalue                    1,193    0.72%
phi                             1,180    0.71%
invoke                            814    0.49%
switch                            797    0.48%
unreachable                       730    0.44%
landingpad                        640    0.38%
zext                              530    0.32%
sub                               350    0.21%
add                               310    0.19%
ptrtoint                          268    0.16%
sext                              264    0.16%
mul                               124    0.07%
sdiv                              103    0.06%
select                             63    0.04%
inttoptr                           61    0.04%
udiv                               50    0.03%
trunc                              35    0.02%
urem                               13    0.01%
xor                                12    0.01%
srem                                8    0.00%
and                                 4    0.00%
ashr                                1    0.00%
fcmp                                1    0.00%
or                                  1    0.00%
```

### lencod

```text
opcode                          count    share
load                           77,299   36.13%
getelementptr                  37,764   17.65%
br                             21,390   10.00%
store                          20,381    9.53%
sext                           14,643    6.85%
icmp                            9,030    4.22%
add                             7,731    3.61%
alloca                          5,813    2.72%
call                            5,438    2.54%
sub                             2,631    1.23%
zext                            2,270    1.06%
mul                             1,734    0.81%
ashr                            1,134    0.53%
shl                             1,080    0.50%
trunc                             991    0.46%
phi                               946    0.44%
ret                               828    0.39%
sdiv                              432    0.20%
sitofp                            402    0.19%
and                               302    0.14%
fdiv                              212    0.10%
select                            207    0.10%
fmul                              202    0.09%
fpext                             174    0.08%
or                                141    0.07%
fadd                              131    0.06%
fptosi                            120    0.06%
srem                              110    0.05%
fcmp                               80    0.04%
switch                             61    0.03%
xor                                61    0.03%
unreachable                        32    0.01%
fsub                               30    0.01%
uitofp                             24    0.01%
udiv                               22    0.01%
urem                               21    0.01%
fptrunc                            18    0.01%
fneg                               16    0.01%
lshr                               15    0.01%
fptoui                              3    0.00%
```

### mafft

```text
opcode                          count    share
load                           36,270   35.09%
store                          14,586   14.11%
br                             12,851   12.43%
getelementptr                  10,038    9.71%
sext                            5,987    5.79%
alloca                          5,026    4.86%
icmp                            4,408    4.26%
call                            3,958    3.83%
add                             3,565    3.45%
sub                             1,227    1.19%
zext                              938    0.91%
fadd                              576    0.56%
fmul                              455    0.44%
fpext                             449    0.43%
sitofp                            435    0.42%
ret                               403    0.39%
fcmp                              304    0.29%
mul                               252    0.24%
trunc                             247    0.24%
fsub                              219    0.21%
fptrunc                           218    0.21%
phi                               215    0.21%
xor                               166    0.16%
fdiv                              153    0.15%
fptosi                            125    0.12%
unreachable                        99    0.10%
ptrtoint                           86    0.08%
fneg                               37    0.04%
sdiv                               29    0.03%
and                                17    0.02%
srem                               14    0.01%
switch                              8    0.01%
select                              4    0.00%
shl                                 4    0.00%
ashr                                1    0.00%
```

### SPASS

```text
opcode                          count    share
load                           38,739   28.32%
call                           25,937   18.96%
store                          19,265   14.09%
br                             18,627   13.62%
alloca                         11,384    8.32%
icmp                            7,945    5.81%
ret                             4,271    3.12%
getelementptr                   4,109    3.00%
add                             1,497    1.09%
zext                            1,212    0.89%
xor                               991    0.72%
sext                              809    0.59%
phi                               465    0.34%
sub                               436    0.32%
inttoptr                          221    0.16%
ptrtoint                          206    0.15%
urem                              166    0.12%
trunc                             132    0.10%
mul                               100    0.07%
and                                56    0.04%
switch                             40    0.03%
unreachable                        39    0.03%
or                                 29    0.02%
select                             28    0.02%
ashr                               20    0.01%
udiv                               11    0.01%
sdiv                                8    0.01%
shl                                 8    0.01%
sitofp                              8    0.01%
fcmp                                6    0.00%
fptoui                              2    0.00%
srem                                2    0.00%
```

### sqlite3

```text
opcode                          count    share
load                           38,694   33.84%
br                             15,316   13.39%
getelementptr                  15,067   13.18%
store                          14,287   12.49%
alloca                          6,852    5.99%
icmp                            6,850    5.99%
call                            6,341    5.54%
zext                            2,316    2.03%
sext                            2,110    1.85%
add                             1,865    1.63%
ret                             1,081    0.95%
trunc                             664    0.58%
and                               619    0.54%
sub                               508    0.44%
phi                               336    0.29%
or                                295    0.26%
mul                               227    0.20%
shl                               150    0.13%
select                            130    0.11%
lshr                              101    0.09%
sdiv                               67    0.06%
ptrtoint                           66    0.06%
switch                             53    0.05%
xor                                49    0.04%
sitofp                             48    0.04%
fmul                               36    0.03%
fptosi                             34    0.03%
fadd                               31    0.03%
fcmp                               31    0.03%
ashr                               27    0.02%
fdiv                               21    0.02%
fsub                               20    0.02%
udiv                               15    0.01%
srem                               14    0.01%
urem                               10    0.01%
unreachable                         8    0.01%
fneg                                6    0.01%
inttoptr                            5    0.00%
fpext                               3    0.00%
uitofp                              2    0.00%
fptoui                              1    0.00%
fptrunc                             1    0.00%
```

### tramp3d-v4

```text
opcode                          count    share
load                           36,982   21.98%
alloca                         30,983   18.41%
call                           30,853   18.34%
store                          28,861   17.15%
getelementptr                  15,904    9.45%
ret                             9,578    5.69%
br                              7,636    4.54%
icmp                            2,241    1.33%
add                               948    0.56%
sext                              788    0.47%
ptrtoint                          533    0.32%
inttoptr                          515    0.31%
zext                              509    0.30%
sub                               346    0.21%
trunc                             298    0.18%
mul                               199    0.12%
sdiv                              193    0.11%
fmul                              190    0.11%
phi                               168    0.10%
fsub                              123    0.07%
unreachable                       102    0.06%
fdiv                               69    0.04%
fadd                               45    0.03%
fcmp                               39    0.02%
and                                31    0.02%
udiv                               25    0.01%
xor                                23    0.01%
fneg                               20    0.01%
sitofp                             16    0.01%
select                             13    0.01%
srem                               10    0.01%
extractvalue                        8    0.00%
shl                                 7    0.00%
or                                  4    0.00%
fptosi                              2    0.00%
switch                              2    0.00%
```

## Overall IR type detail

### load

```text
       count  opcode%   total%  types
     330,114   60.70%   17.51%  ptr <- [ptr]
     153,943   28.31%    8.17%  i32 <- [ptr]
      17,910    3.29%    0.95%  i8 <- [ptr]
      17,155    3.15%    0.91%  float <- [ptr]
      11,245    2.07%    0.60%  i64 <- [ptr]
       9,593    1.76%    0.51%  i16 <- [ptr]
       2,607    0.48%    0.14%  double <- [ptr]
         597    0.11%    0.03%  %class.btVector3 <- [ptr]
         510    0.09%    0.03%  i1 <- [ptr]
          92    0.02%    0.00%  [2 x i64] <- [ptr]
          37    0.01%    0.00%  fp128 <- [ptr]
          34    0.01%    0.00%  %class.btQuaternion <- [ptr]
           3    0.00%    0.00%  { i64, i64 } <- [ptr]
           2    0.00%    0.00%  [2 x ptr] <- [ptr]
           1    0.00%    0.00%  %class.btVector4 <- [ptr]
```

### getelementptr

```text
       count  opcode%   total%  types
     174,707   63.82%    9.27%  ptr <- [ptr,i32,i32]
      48,707   17.79%    2.58%  ptr <- [ptr,i64]
      47,122   17.21%    2.50%  ptr <- [ptr,i64,i64]
       3,193    1.17%    0.17%  ptr <- [ptr,i32]
          12    0.00%    0.00%  ptr <- [ptr,i32,i32,i32]
```

### store

```text
       count  opcode%   total%  types
     136,797   52.43%    7.26%  void <- [ptr,ptr]
      85,298   32.69%    4.52%  void <- [i32,ptr]
      12,665    4.85%    0.67%  void <- [float,ptr]
       8,883    3.40%    0.47%  void <- [i8,ptr]
       6,570    2.52%    0.35%  void <- [i64,ptr]
       4,431    1.70%    0.24%  void <- [i16,ptr]
       2,566    0.98%    0.14%  void <- [[4 x float],ptr]
       2,112    0.81%    0.11%  void <- [double,ptr]
       1,327    0.51%    0.07%  void <- [i1,ptr]
         149    0.06%    0.01%  void <- [[2 x i64],ptr]
          73    0.03%    0.00%  void <- [%class.btQuadWord,ptr]
          25    0.01%    0.00%  void <- [fp128,ptr]
           3    0.00%    0.00%  void <- [{ i64, i64 },ptr]
           2    0.00%    0.00%  void <- [[2 x ptr],ptr]
           1    0.00%    0.00%  void <- [%class.btVector3,ptr]
```

### br

```text
       count  opcode%   total%  types
     116,603   61.80%    6.18%  void <- [label]
      72,078   38.20%    3.82%  void <- [i1,label,label]
```

### call

```text
       count  opcode%   total%  types
      30,004   18.72%    1.59%  void <- [ptr,ptr]
      22,401   13.98%    1.19%  ptr <- [ptr,ptr]
      14,042    8.76%    0.74%  i32 <- [ptr,ptr]
       8,134    5.07%    0.43%  void <- [ptr,ptr,ptr]
       7,761    4.84%    0.41%  void <- [ptr,ptr,ptr,ptr]
       6,107    3.81%    0.32%  ptr <- [ptr,ptr,ptr]
       4,767    2.97%    0.25%  ptr <- [ptr,i32,ptr]
       4,493    2.80%    0.24%  i32 <- [ptr,ptr,ptr]
       3,707    2.31%    0.20%  void <- [ptr,ptr,i64,i1,ptr]
       2,886    1.80%    0.15%  void <- [ptr,i32,ptr]
       2,742    1.71%    0.15%  ptr <- [ptr]
       2,562    1.60%    0.14%  void <- [ptr]
       2,544    1.59%    0.13%  void <- [ptr,ptr,ptr,ptr,ptr]
       2,142    1.34%    0.11%  %class.btVector3 <- [ptr,ptr,ptr]
       2,027    1.26%    0.11%  void <- [ptr,i64,ptr]
       1,840    1.15%    0.10%  i64 <- [ptr,ptr]
       1,723    1.07%    0.09%  i32 <- [i32,ptr]
       1,507    0.94%    0.08%  ptr <- [i64,ptr]
       1,449    0.90%    0.08%  i32 <- [ptr,i32,ptr]
       1,356    0.85%    0.07%  i32 <- [ptr]
       1,346    0.84%    0.07%  i32 <- [ptr,ptr,ptr,ptr]
       1,290    0.80%    0.07%  float <- [float,float,float,ptr]
       1,128    0.70%    0.06%  ptr <- [ptr,ptr,ptr,ptr]
       1,088    0.68%    0.06%  i1 <- [ptr,ptr]
       1,059    0.66%    0.06%  i32 <- [i32,i32,ptr]
       1,057    0.66%    0.06%  ptr <- [i32,ptr]
       1,049    0.65%    0.06%  float <- [ptr,ptr,ptr]
       1,010    0.63%    0.05%  ptr <- [ptr,ptr,ptr,i64,ptr]
         835    0.52%    0.04%  void <- [ptr,i32,i32,ptr]
         770    0.48%    0.04%  ptr <- [i32,i32,ptr,i32,ptr,ptr]
         748    0.47%    0.04%  ptr <- [i32,ptr,ptr]
         745    0.46%    0.04%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr]
         649    0.40%    0.03%  float <- [ptr,ptr]
         620    0.39%    0.03%  void <- [ptr,i32,ptr,ptr]
         619    0.39%    0.03%  void <- [ptr,ptr,i32,ptr]
         602    0.38%    0.03%  float <- [float,ptr]
         573    0.36%    0.03%  void <- [i32,ptr]
         563    0.35%    0.03%  i32 <- [ptr,ptr,i32,ptr]
         480    0.30%    0.03%  i1 <- [ptr,ptr,ptr]
         464    0.29%    0.02%  ptr <- [ptr,i64,ptr]
         464    0.29%    0.02%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
         452    0.28%    0.02%  i32 <- [ptr,ptr,i64,ptr]
         394    0.25%    0.02%  ptr <- [ptr,ptr,ptr,ptr,ptr]
         392    0.24%    0.02%  i32 <- [ptr,i32,i32,i32,ptr]
         392    0.24%    0.02%  ptr <- [ptr,ptr,i32,ptr]
         386    0.24%    0.02%  i1 <- [ptr,i64,ptr]
         368    0.23%    0.02%  ptr <- [ptr,i32,ptr,ptr]
         336    0.21%    0.02%  double <- [double,double,double,ptr]
         324    0.20%    0.02%  void <- [ptr,ptr,i64,ptr]
         317    0.20%    0.02%  void <- [ptr,i8,i64,i1,ptr]
         313    0.20%    0.02%  i32 <- [i32,ptr,ptr]
         303    0.19%    0.02%  ptr <- [i64,i64,ptr]
         292    0.18%    0.02%  ptr <- [ptr,i32,i32,ptr]
         275    0.17%    0.01%  ptr <- [i32,i32,ptr]
         262    0.16%    0.01%  i32 <- [ptr,i32,i32,ptr]
         259    0.16%    0.01%  i32 <- [ptr,i32,ptr,ptr]
         252    0.16%    0.01%  void <- [ptr,ptr,i32,i32,ptr]
         248    0.15%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr]
         245    0.15%    0.01%  i32 <- [i32,ptr,i32,ptr]
         242    0.15%    0.01%  i32 <- [i32,i32,i32,ptr]
         231    0.14%    0.01%  double <- [ptr,ptr,ptr]
         223    0.14%    0.01%  ptr <- [i32,ptr,ptr,ptr]
         197    0.12%    0.01%  i32 <- [ptr,ptr,ptr,i32,ptr]
         193    0.12%    0.01%  i64 <- [i32,i64,i32,ptr]
         162    0.10%    0.01%  %class.btVector3 <- [ptr,ptr]
         162    0.10%    0.01%  void <- [ptr,i32,i1,ptr]
         162    0.10%    0.01%  void <- [ptr,ptr,ptr,i32,ptr]
         160    0.10%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
         155    0.10%    0.01%  void <- [ptr,i32,i1,i1,ptr]
         153    0.10%    0.01%  ptr <- [i64,i32,ptr]
         150    0.09%    0.01%  i32 <- [ptr,i64,ptr]
         150    0.09%    0.01%  void <- [ptr,i32,i32,ptr,ptr]
         149    0.09%    0.01%  i32 <- [ptr,i32,i32,i32,i32,ptr]
         144    0.09%    0.01%  ptr <- [ptr,ptr,i64,ptr]
         139    0.09%    0.01%  void <- [i32,ptr,ptr,ptr]
         132    0.08%    0.01%  i32 <- [ptr,ptr,i32,ptr,ptr]
         132    0.08%    0.01%  i64 <- [ptr,ptr,ptr]
         132    0.08%    0.01%  void <- [i32,ptr,ptr]
         132    0.08%    0.01%  void <- [ptr,i32,i32,i32,ptr]
         126    0.08%    0.01%  double <- [ptr,ptr]
         123    0.08%    0.01%  void <- [ptr,i16,ptr,ptr]
         119    0.07%    0.01%  i32 <- [ptr,ptr,i32,i32,ptr]
         114    0.07%    0.01%  ptr <- [ptr,i32,i32,i32,i32,i8,ptr]
         110    0.07%    0.01%  double <- [double,ptr]
         107    0.07%    0.01%  i32 <- [ptr,ptr,double,ptr]
         105    0.07%    0.01%  void <- [ptr,i8,ptr]
         100    0.06%    0.01%  i1 <- [ptr,ptr,ptr,ptr]
         100    0.06%    0.01%  i32 <- [i32,i32,i64,ptr]
         100    0.06%    0.01%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr]
         100    0.06%    0.01%  void <- [i1,ptr]
          98    0.06%    0.01%  void <- [ptr,i32,ptr,ptr,i32,ptr]
          96    0.06%    0.01%  void <- [i32,i32,ptr,i32,i32,i32,ptr]
          95    0.06%    0.01%  i1 <- [ptr,i32,ptr]
          94    0.06%    0.00%  void <- [i32,i32,ptr]
          94    0.06%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
          93    0.06%    0.00%  { i64, i1 } <- [i64,i64,ptr]
          91    0.06%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr]
          87    0.05%    0.00%  i8 <- [ptr,ptr]
          86    0.05%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
          84    0.05%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,i32,ptr]
          84    0.05%    0.00%  void <- [ptr,ptr,i8,ptr]
          83    0.05%    0.00%  void <- [ptr,float,ptr]
          82    0.05%    0.00%  void <- [ptr,ptr,i1,ptr]
          79    0.05%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr]
          78    0.05%    0.00%  void <- [ptr,i32,ptr,ptr,ptr]
          77    0.05%    0.00%  %class.btVector3 <- [ptr,i32,ptr]
          77    0.05%    0.00%  ptr <- [i16,ptr]
          76    0.05%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,ptr]
          75    0.05%    0.00%  i32 <- [ptr,i64,ptr,ptr]
          74    0.05%    0.00%  void <- [ptr,i16,ptr]
          74    0.05%    0.00%  void <- [ptr,ptr,ptr,float,ptr]
          72    0.04%    0.00%  float <- [ptr,i32,i32,i32,i32,ptr]
          71    0.04%    0.00%  void <- [ptr,i64,i64,ptr]
          70    0.04%    0.00%  double <- [ptr,ptr,ptr,ptr]
          69    0.04%    0.00%  i64 <- [i64,ptr]
          64    0.04%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr,ptr]
          64    0.04%    0.00%  ptr <- [ptr,i64,ptr,ptr]
          61    0.04%    0.00%  i16 <- [ptr,ptr]
          61    0.04%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          60    0.04%    0.00%  void <- [ptr,i1,ptr]
          59    0.04%    0.00%  double <- [double,double,ptr]
          58    0.04%    0.00%  i64 <- [ptr,i64,ptr]
          57    0.04%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr]
          57    0.04%    0.00%  i64 <- [ptr]
          56    0.03%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr]
          55    0.03%    0.00%  [2 x i64] <- [ptr,i64,ptr]
          53    0.03%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,ptr]
          53    0.03%    0.00%  void <- [ptr,i64,ptr,ptr]
          52    0.03%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr]
          52    0.03%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr]
          51    0.03%    0.00%  ptr <- [ptr,i32,i32,i32,i32,i32,i32,i32,ptr,ptr,ptr]
          49    0.03%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr]
          48    0.03%    0.00%  ptr <- [i64,ptr,ptr]
          48    0.03%    0.00%  ptr <- [ptr,i1,ptr]
          48    0.03%    0.00%  void <- [ptr,i32,ptr,i32,ptr]
          48    0.03%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr,ptr,i32,ptr]
          47    0.03%    0.00%  i32 <- [ptr,i64,i32,ptr,ptr]
          46    0.03%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr]
          45    0.03%    0.00%  i64 <- [i32,ptr,i64,ptr]
          45    0.03%    0.00%  i64 <- [ptr,i64,i64,ptr,ptr]
          44    0.03%    0.00%  void <- [i32,i32,ptr,ptr]
          42    0.03%    0.00%  i1 <- [i32,ptr]
          42    0.03%    0.00%  void <- [ptr,double,ptr]
          41    0.03%    0.00%  void <- [i32,i32,i32,ptr,ptr]
          40    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
          40    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          40    0.02%    0.00%  void <- [ptr,i32,ptr,ptr,i32,ptr,ptr,ptr]
          38    0.02%    0.00%  void <- [ptr,i64,i1,ptr]
          37    0.02%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr]
          36    0.02%    0.00%  i1 <- [ptr,i64,ptr,ptr]
          36    0.02%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr]
          35    0.02%    0.00%  %class.btQuaternion <- [ptr,ptr]
          34    0.02%    0.00%  i64 <- [ptr,ptr,ptr,ptr]
          33    0.02%    0.00%  float <- [float,float,ptr]
          33    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
          33    0.02%    0.00%  i64 <- [i64,ptr,i32,ptr]
          33    0.02%    0.00%  void <- [ptr,i64,i32,i32,ptr]
          32    0.02%    0.00%  i16 <- [i16,ptr]
          32    0.02%    0.00%  i32 <- [i32,ptr,ptr,ptr]
          32    0.02%    0.00%  ptr <- [ptr,i8,ptr]
          32    0.02%    0.00%  ptr <- [ptr,ptr,ptr,i64,i64,ptr]
          30    0.02%    0.00%  ptr <- [i32,ptr,ptr,ptr,ptr]
          30    0.02%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr]
          30    0.02%    0.00%  void <- [i32,i8,ptr]
          30    0.02%    0.00%  void <- [ptr,ptr,i32,i32,i32,ptr]
          29    0.02%    0.00%  %class.btQuaternion <- [ptr,ptr,ptr]
          29    0.02%    0.00%  i64 <- [i64,i64,ptr]
          28    0.02%    0.00%  void <- [ptr,i32,ptr,ptr,i32,ptr,ptr]
          28    0.02%    0.00%  void <- [ptr,ptr,float,ptr]
          27    0.02%    0.00%  [2 x i64] <- [ptr,ptr,ptr]
          27    0.02%    0.00%  float <- [ptr,ptr,ptr,ptr]
          27    0.02%    0.00%  i32 <- [i32,i32,i32,ptr,ptr]
          27    0.02%    0.00%  i64 <- [ptr,ptr,i64,ptr]
          27    0.02%    0.00%  ptr <- [ptr,i32,ptr,i32,ptr]
          27    0.02%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr]
          27    0.02%    0.00%  void <- [i32,i32,i32,i32,ptr,ptr]
          26    0.02%    0.00%  double <- [ptr,i32,i32,i32,ptr]
          26    0.02%    0.00%  i32 <- [i32,i8,ptr]
          26    0.02%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr]
          25    0.02%    0.00%  i32 <- [i32,ptr,i32,ptr,ptr]
          25    0.02%    0.00%  i32 <- [ptr,i64,ptr,i32,ptr]
          25    0.02%    0.00%  i64 <- [ptr,i64,ptr,ptr]
          25    0.02%    0.00%  void <- [ptr,float,float,float,ptr]
          25    0.02%    0.00%  void <- [ptr,i64,ptr,ptr,ptr]
          24    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i64,i64,i64,i32,ptr]
          24    0.01%    0.00%  void <- [ptr,i32,i64,ptr]
          23    0.01%    0.00%  void <- [i32,i32,i32,ptr,ptr,ptr,ptr]
          22    0.01%    0.00%  i32 <- [ptr,ptr,i32,i64,ptr]
          22    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
          22    0.01%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,i32,ptr]
          22    0.01%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,i32,ptr]
          22    0.01%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
          22    0.01%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
          22    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr]
          22    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i64,ptr]
          21    0.01%    0.00%  %class.btVector3 <- [ptr,ptr,ptr,ptr]
          21    0.01%    0.00%  i16 <- [i16,i32,ptr]
          21    0.01%    0.00%  i32 <- [ptr,i64,i32,ptr]
          21    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr]
          21    0.01%    0.00%  ptr <- [ptr,float,ptr,ptr,ptr]
          21    0.01%    0.00%  ptr <- [ptr,i16,ptr]
          21    0.01%    0.00%  ptr <- [ptr,i8,ptr,i8,i32,i32,i32,ptr,ptr,ptr]
          21    0.01%    0.00%  void <- [ptr,i32,i32,i32,ptr,ptr]
          21    0.01%    0.00%  void <- [ptr,i32,i32,ptr,i1,ptr]
          20    0.01%    0.00%  void <- [i32,ptr,i32,ptr]
          20    0.01%    0.00%  void <- [ptr,float,ptr,ptr]
          19    0.01%    0.00%  double <- [ptr]
          19    0.01%    0.00%  float <- [ptr,i32,ptr]
          19    0.01%    0.00%  i16 <- [ptr,ptr,ptr,i32,i32,ptr]
          19    0.01%    0.00%  i32 <- [i32,i32,ptr,ptr]
          19    0.01%    0.00%  i32 <- [i32,ptr,i64,ptr]
          19    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr]
          19    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          19    0.01%    0.00%  void <- [i32,i32,ptr,ptr,ptr]
          18    0.01%    0.00%  i16 <- [ptr,ptr,ptr]
          18    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr]
          18    0.01%    0.00%  ptr <- [i32,ptr,ptr,i32,ptr]
          18    0.01%    0.00%  ptr <- [ptr,i32,i32,i32,ptr]
          18    0.01%    0.00%  void <- [metadata,ptr]
          18    0.01%    0.00%  void <- [ptr,i64,i64,ptr,ptr]
          18    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,i1,ptr]
          18    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          17    0.01%    0.00%  i32 <- [ptr,ptr,i32,i8,ptr,ptr]
          17    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i1,ptr]
          17    0.01%    0.00%  void <- [ptr,i32,ptr,i16,ptr]
          17    0.01%    0.00%  void <- [ptr,ptr,i64,i32,ptr]
          17    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          16    0.01%    0.00%  double <- [double,double,i64,ptr]
          16    0.01%    0.00%  i1 <- [ptr,i32,ptr,ptr]
          16    0.01%    0.00%  i32 <- [ptr,i32,i8,ptr]
          16    0.01%    0.00%  i32 <- [ptr,ptr,double,double,double,ptr]
          16    0.01%    0.00%  i8 <- [i8,ptr]
          16    0.01%    0.00%  ptr <- [i8,ptr,i8,i8,i8,ptr,ptr]
          16    0.01%    0.00%  void <- [ptr,ptr,float,float,float,ptr]
          15    0.01%    0.00%  float <- [ptr,ptr,i32,ptr]
          15    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
          15    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
          15    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
          15    0.01%    0.00%  i64 <- [ptr,i64,i32,i32,ptr]
          15    0.01%    0.00%  i8 <- [ptr,i32,ptr]
          15    0.01%    0.00%  ptr <- [ptr,i32,i32,i64,i16,ptr,ptr]
          15    0.01%    0.00%  void <- [ptr,i32,float,ptr]
          14    0.01%    0.00%  [2 x i64] <- [ptr,ptr]
          14    0.01%    0.00%  i1 <- [ptr]
          14    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr]
          14    0.01%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr]
          14    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr]
          14    0.01%    0.00%  i32 <- [ptr,ptr,double,double,ptr]
          14    0.01%    0.00%  ptr <- [ptr,ptr,i8,ptr]
          14    0.01%    0.00%  void <- [ptr,float,float,float,float,ptr]
          14    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,float,ptr]
          13    0.01%    0.00%  i1 <- [ptr,ptr,i32,ptr]
          13    0.01%    0.00%  i32 <- [ptr,i8,ptr]
          13    0.01%    0.00%  ptr <- [i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          13    0.01%    0.00%  ptr <- [ptr,i8,ptr,i32,i32,ptr]
          13    0.01%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr]
          13    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          13    0.01%    0.00%  void <- [i32,i32,i32,i32,i32,ptr]
          13    0.01%    0.00%  void <- [i64,ptr,ptr]
          13    0.01%    0.00%  void <- [ptr,i64,i64,i64,ptr]
          13    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,ptr]
          12    0.01%    0.00%  float <- [i32,i32,i32,i32,i32,ptr]
          12    0.01%    0.00%  i16 <- [i16,i8,ptr]
          12    0.01%    0.00%  i32 <- [ptr,i32,i8,i32,ptr]
          12    0.01%    0.00%  i32 <- [ptr,ptr,i64,ptr,ptr]
          12    0.01%    0.00%  i64 <- [ptr,i32,ptr]
          12    0.01%    0.00%  i64 <- [ptr,ptr,ptr,ptr,ptr]
          12    0.01%    0.00%  ptr <- [ptr,ptr,i32,i32,i8,i32,ptr]
          12    0.01%    0.00%  void <- [ptr,double,ptr,ptr]
          12    0.01%    0.00%  void <- [ptr,float,float,ptr]
          12    0.01%    0.00%  void <- [ptr,i32,i16,ptr,i1,ptr]
          11    0.01%    0.00%  double <- [ptr,ptr,ptr,ptr,ptr]
          11    0.01%    0.00%  float <- [i32,i32,ptr]
          11    0.01%    0.00%  i32 <- [i8,ptr,ptr,ptr,ptr,ptr,i32,ptr]
          11    0.01%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,i32,ptr]
          11    0.01%    0.00%  i32 <- [ptr,ptr,i64,i32,ptr]
          11    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i32,i16,ptr]
          11    0.01%    0.00%  i64 <- [i32,ptr,ptr]
          11    0.01%    0.00%  ptr <- [i32,i32,i32,i32,i32,ptr]
          11    0.01%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
          11    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
          11    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i64,ptr]
          11    0.01%    0.00%  void <- [ptr,i32,i32,ptr,i32,ptr]
          11    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,float,ptr,float,ptr]
          10    0.01%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
          10    0.01%    0.00%  i32 <- [i32,i32,ptr,ptr,ptr]
          10    0.01%    0.00%  i32 <- [i64,ptr]
          10    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr]
          10    0.01%    0.00%  i32 <- [ptr,ptr,i64,double,ptr]
          10    0.01%    0.00%  i32 <- [ptr,ptr,i64,i32,ptr,ptr]
          10    0.01%    0.00%  i32 <- [ptr,ptr,i64,ptr,i32,ptr]
          10    0.01%    0.00%  i64 <- [i64,ptr,ptr]
          10    0.01%    0.00%  ptr <- [i16,i32,i32,ptr]
          10    0.01%    0.00%  ptr <- [i32,ptr,ptr,ptr,ptr,ptr]
          10    0.01%    0.00%  ptr <- [ptr,i64,ptr,i64,ptr]
          10    0.01%    0.00%  ptr <- [ptr,i64,ptr,ptr,ptr]
          10    0.01%    0.00%  void <- [i32,ptr,ptr,i32,ptr,i32,ptr,ptr,ptr]
          10    0.01%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,i16,i64,i32,i32,ptr]
          10    0.01%    0.00%  void <- [ptr,i8,i8,ptr]
          10    0.01%    0.00%  void <- [ptr,ptr,float,float,ptr,ptr,ptr]
           9    0.01%    0.00%  i16 <- [ptr,i32,ptr]
           9    0.01%    0.00%  i32 <- [i32,ptr,i8,i32,i8,ptr,ptr]
           9    0.01%    0.00%  i32 <- [i32,ptr,ptr,i32,ptr]
           9    0.01%    0.00%  i32 <- [ptr,i1,ptr]
           9    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,ptr,ptr]
           9    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,i32,ptr]
           9    0.01%    0.00%  ptr <- [ptr,i32,i32,ptr,ptr]
           9    0.01%    0.00%  void <- [ptr,float,ptr,ptr,ptr]
           9    0.01%    0.00%  void <- [ptr,float,ptr,ptr,ptr,ptr]
           9    0.01%    0.00%  void <- [ptr,i32,ptr,i8,ptr,ptr]
           9    0.01%    0.00%  void <- [ptr,i64,i32,ptr]
           9    0.01%    0.00%  void <- [ptr,ptr,i64,i64,ptr]
           9    0.01%    0.00%  void <- [ptr,ptr,ptr,i64,ptr]
           9    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i1,ptr]
           8    0.00%    0.00%  i1 <- [ptr,ptr,ptr,i32,i32,ptr]
           8    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.00%    0.00%  i32 <- [double,ptr]
           8    0.00%    0.00%  i32 <- [i1,ptr]
           8    0.00%    0.00%  i32 <- [i32,i32,i32,i32,ptr]
           8    0.00%    0.00%  i32 <- [i32,i32,i32,ptr,i32,i32,ptr]
           8    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr]
           8    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,ptr,ptr,ptr]
           8    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,ptr]
           8    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,i8,i32,i32,i32,ptr,ptr]
           8    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,ptr,ptr]
           8    0.00%    0.00%  i32 <- [ptr,ptr,i1,ptr]
           8    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i8,ptr]
           8    0.00%    0.00%  i64 <- [i32,ptr]
           8    0.00%    0.00%  i64 <- [ptr,i64,i64,i64,i32,i64,ptr]
           8    0.00%    0.00%  i8 <- [ptr,ptr,ptr]
           8    0.00%    0.00%  ptr <- [ptr,i32,i32,ptr,ptr,ptr]
           8    0.00%    0.00%  ptr <- [ptr,i32,i32,ptr,ptr,ptr,ptr]
           8    0.00%    0.00%  ptr <- [ptr,i64,i64,ptr,i32,ptr,ptr]
           8    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.00%    0.00%  void <- [i1,ptr,ptr,ptr,ptr]
           8    0.00%    0.00%  void <- [i32,i64,ptr]
           8    0.00%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.00%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           8    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,i32,ptr]
           8    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr]
           8    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           8    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i16,i32,ptr,ptr,ptr,i32,ptr]
           7    0.00%    0.00%  float <- [ptr,ptr,i32,ptr,ptr,ptr]
           7    0.00%    0.00%  i1 <- [float,ptr]
           7    0.00%    0.00%  i32 <- [i32,i32,ptr,i32,ptr]
           7    0.00%    0.00%  i32 <- [i32,ptr,i16,ptr,i64,i32,ptr]
           7    0.00%    0.00%  i32 <- [i32,ptr,i64,i64,ptr,i64,ptr]
           7    0.00%    0.00%  i32 <- [i32,ptr,i64,ptr,ptr]
           7    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,double,double,double,i32,i32,ptr,i32,ptr]
           7    0.00%    0.00%  i32 <- [ptr,i32,i64,ptr]
           7    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           7    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr]
           7    0.00%    0.00%  i64 <- [i64,i64,i64,ptr]
           7    0.00%    0.00%  i64 <- [ptr,i64,i64,ptr]
           7    0.00%    0.00%  i64 <- [ptr,ptr,ptr,ptr,ptr,ptr]
           7    0.00%    0.00%  ptr <- [i32,i32,i32,ptr]
           7    0.00%    0.00%  ptr <- [i32,i32,i32,ptr,ptr,i32,i32,i32,ptr,i32,ptr]
           7    0.00%    0.00%  ptr <- [ptr,i32,i32,i32,ptr,ptr,ptr]
           7    0.00%    0.00%  ptr <- [ptr,i64,i32,i32,i32,i64,ptr]
           7    0.00%    0.00%  void <- [ptr,i1,i1,ptr]
           7    0.00%    0.00%  void <- [ptr,i32,i8,i32,ptr,ptr]
           7    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr]
           7    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,ptr]
           7    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i32,ptr,i32,ptr]
           7    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr]
           7    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           6    0.00%    0.00%  double <- [ptr,i32,ptr]
           6    0.00%    0.00%  float <- [i32,ptr]
           6    0.00%    0.00%  float <- [ptr,ptr,i1,ptr]
           6    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  i1 <- [i32,i32,i32,i32,i32,i32,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  i1 <- [ptr,ptr,i1,ptr]
           6    0.00%    0.00%  i1 <- [ptr,ptr,ptr,i32,ptr]
           6    0.00%    0.00%  i32 <- [i16,ptr]
           6    0.00%    0.00%  i32 <- [i32,ptr,i32,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  i32 <- [i64,i64,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,i32,i32,i32,i32,ptr,ptr,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i64,i64,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i64,ptr,i32,i32,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,ptr]
           6    0.00%    0.00%  i32 <- [ptr,i8,ptr,ptr]
           6    0.00%    0.00%  i32 <- [ptr,ptr,ptr,double,ptr,double,ptr]
           6    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr]
           6    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i64,ptr]
           6    0.00%    0.00%  i64 <- [i64,ptr,i64,ptr]
           6    0.00%    0.00%  ptr <- [i16,i64,i32,ptr]
           6    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,i32,ptr]
           6    0.00%    0.00%  ptr <- [ptr,i32,ptr,ptr,i32,ptr,ptr,i32,i32,i32,ptr,ptr,ptr]
           6    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,i32,ptr]
           6    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr,ptr]
           6    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,float,ptr]
           6    0.00%    0.00%  void <- [i32,i32,i32,i32,i32,i16,i16,ptr]
           6    0.00%    0.00%  void <- [i32,i32,i32,ptr,ptr,i32,i32,i32,ptr]
           6    0.00%    0.00%  void <- [i32,ptr,i32,ptr,ptr,i32,ptr]
           6    0.00%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,i32,i16,ptr,ptr]
           6    0.00%    0.00%  void <- [i64,i64,ptr]
           6    0.00%    0.00%  void <- [i64,ptr,i32,ptr]
           6    0.00%    0.00%  void <- [ptr,float,float,float,float,float,float,ptr]
           6    0.00%    0.00%  void <- [ptr,float,i32,ptr]
           6    0.00%    0.00%  void <- [ptr,i32,i32,i32,float,ptr]
           6    0.00%    0.00%  void <- [ptr,i32,i32,i64,ptr]
           6    0.00%    0.00%  void <- [ptr,i32,i32,i8,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,i32,i32,ptr,i16,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,i32,ptr,i32,i32,ptr]
           6    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,float,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,float,ptr,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,ptr,double,ptr,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,ptr,i16,i32,i32,i32,i32,i32,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           6    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
           5    0.00%    0.00%  [2 x i64] <- [[2 x i64],[2 x i64],[2 x i64],ptr]
           5    0.00%    0.00%  [2 x i64] <- [[2 x i64],ptr]
           5    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr]
           5    0.00%    0.00%  i16 <- [i32,ptr]
           5    0.00%    0.00%  i1 <- [ptr,i32,i32,ptr]
           5    0.00%    0.00%  i1 <- [ptr,ptr,i32,ptr,ptr]
           5    0.00%    0.00%  i32 <- [i8,ptr]
           5    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,double,double,double,i32,i32,ptr,i32,i32,i32,i32,i32,ptr]
           5    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,i32,ptr]
           5    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,i32,ptr]
           5    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           5    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           5    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,ptr]
           5    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i8,i32,ptr]
           5    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           5    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.00%    0.00%  i8 <- [ptr,i32,ptr,ptr]
           5    0.00%    0.00%  ptr <- [i32,ptr,ptr,double,ptr]
           5    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i8,ptr]
           5    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
           5    0.00%    0.00%  void <- [i16,i32,i32,i32,i32,ptr]
           5    0.00%    0.00%  void <- [ptr,float,float,float,float,float,ptr]
           5    0.00%    0.00%  void <- [ptr,i16,ptr,ptr,ptr]
           5    0.00%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,ptr]
           5    0.00%    0.00%  void <- [ptr,i32,i8,ptr]
           5    0.00%    0.00%  void <- [ptr,i64,i32,ptr,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,i16,i16,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,i32,i32,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,i8,i8,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,ptr,float,ptr,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr,i32,ptr,i32,i32,ptr,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,float,float,float,ptr,i1,float,ptr]
           5    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           4    0.00%    0.00%  %class.btVector3 <- [ptr,ptr,float,ptr]
           4    0.00%    0.00%  double <- [i32,ptr]
           4    0.00%    0.00%  double <- [ptr,i32,ptr,i32,ptr]
           4    0.00%    0.00%  float <- [ptr,float,float,float,float,float,ptr]
           4    0.00%    0.00%  float <- [ptr,float,ptr,i32,i32,ptr]
           4    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  i1 <- [double,ptr]
           4    0.00%    0.00%  i1 <- [ptr,i1,ptr,i1,ptr]
           4    0.00%    0.00%  i1 <- [ptr,i64,i32,ptr,ptr]
           4    0.00%    0.00%  i1 <- [ptr,i8,ptr]
           4    0.00%    0.00%  i32 <- [double,ptr,ptr]
           4    0.00%    0.00%  i32 <- [i16,i16,ptr]
           4    0.00%    0.00%  i32 <- [i32,i32,i32,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [i32,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  i32 <- [ptr,[2 x i64],ptr]
           4    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,i32,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,ptr]
           4    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,i32,ptr,ptr,ptr]
           4    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,i8,ptr]
           4    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,i64,ptr,i64,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,i32,i16,i32,i32,i16,i16,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i16,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           4    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  i64 <- [ptr,i64,ptr,ptr,ptr]
           4    0.00%    0.00%  i8 <- [ptr,i8,ptr]
           4    0.00%    0.00%  i8 <- [ptr,ptr,i8,ptr]
           4    0.00%    0.00%  ptr <- [i32,ptr,ptr,i32,ptr,ptr]
           4    0.00%    0.00%  ptr <- [i32,ptr,ptr,i64,ptr]
           4    0.00%    0.00%  ptr <- [ptr,i32,i32,ptr,i32,i32,i32,ptr,ptr,ptr]
           4    0.00%    0.00%  ptr <- [ptr,i32,i64,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,i16,i16,ptr,ptr,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,i32,i32,ptr,ptr,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,ptr]
           4    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i32,ptr]
           4    0.00%    0.00%  void <- [double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,double,i1,i1,ptr]
           4    0.00%    0.00%  void <- [float,float,ptr]
           4    0.00%    0.00%  void <- [i32,i32,i32,ptr]
           4    0.00%    0.00%  void <- [i32,i32,i32,ptr,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  void <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  void <- [i32,i8,i32,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  void <- [i32,ptr,ptr,i32,ptr]
           4    0.00%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,i32,ptr]
           4    0.00%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  void <- [i64,ptr]
           4    0.00%    0.00%  void <- [ptr,i1,ptr,ptr]
           4    0.00%    0.00%  void <- [ptr,i32,i1,i64,ptr]
           4    0.00%    0.00%  void <- [ptr,i32,i32,float,ptr,ptr]
           4    0.00%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  void <- [ptr,i32,ptr,i64,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,double,ptr,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,float,ptr,i32,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,float,ptr,ptr,ptr,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,i32,i1,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,i32,i32,ptr,i32,i32,i32,i32,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,ptr,i1,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr,i32,i32,ptr]
           4    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           3    0.00%    0.00%  %class.btVector3 <- [ptr,ptr,i32,ptr]
           3    0.00%    0.00%  %class.btVector3 <- [ptr,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  [2 x i64] <- [float,ptr]
           3    0.00%    0.00%  double <- [ptr,i32,i32,ptr]
           3    0.00%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr,ptr,i32,ptr,ptr]
           3    0.00%    0.00%  float <- [ptr]
           3    0.00%    0.00%  float <- [ptr,i32,i32,ptr,ptr,i32,ptr]
           3    0.00%    0.00%  float <- [ptr,ptr,i32,ptr,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           3    0.00%    0.00%  i1 <- [i32,ptr,i32,ptr,ptr]
           3    0.00%    0.00%  i1 <- [i32,ptr,ptr]
           3    0.00%    0.00%  i1 <- [ptr,i32,ptr,ptr,i32,ptr,ptr]
           3    0.00%    0.00%  i1 <- [ptr,i32,ptr,ptr,ptr]
           3    0.00%    0.00%  i1 <- [ptr,ptr,i32,i32,i32,i32,i1,ptr]
           3    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,float,ptr]
           3    0.00%    0.00%  i32 <- [float,ptr]
           3    0.00%    0.00%  i32 <- [i32,i32,i32,i32,i32,ptr,i32,i32,ptr]
           3    0.00%    0.00%  i32 <- [i32,ptr,ptr,i32,ptr,ptr]
           3    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,i32,ptr]
           3    0.00%    0.00%  i32 <- [i8,ptr,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,i16,i16,ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,i32,i32,i32,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i16,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,ptr,i32,i32,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,i32,ptr,ptr,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i64,i64,ptr,ptr]
           3    0.00%    0.00%  i32 <- [ptr,i8,i8,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,i32,double,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,i8,i32,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,i8,i8,ptr,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i16,ptr,i16,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i16,i16,i16,i32,i32,ptr,i8,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i64,i32,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i64,ptr,i32,i32,ptr,ptr]
           3    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,ptr]
           3    0.00%    0.00%  i64 <- [double,ptr]
           3    0.00%    0.00%  i64 <- [i32,ptr,i64,i32,ptr]
           3    0.00%    0.00%  i64 <- [ptr,i64,i32,ptr,i32,ptr]
           3    0.00%    0.00%  i64 <- [ptr,ptr,i32,ptr]
           3    0.00%    0.00%  ptr <- [i32,i32,i32,i32,i32,i64,ptr,ptr,ptr]
           3    0.00%    0.00%  ptr <- [i32,i32,i32,i32,ptr,ptr,ptr]
           3    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,i32,i32,ptr]
           3    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,double,ptr]
           3    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,i32,i32,ptr]
           3    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  ptr <- [ptr,i32,i32,i1,ptr]
           3    0.00%    0.00%  ptr <- [ptr,i32,ptr,ptr,i64,ptr]
           3    0.00%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  ptr <- [ptr,i64,i64,ptr]
           3    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,i32,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i32,ptr]
           3    0.00%    0.00%  void <- [i32,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,i32,[2 x i64],ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,i32,i16,ptr]
           3    0.00%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,i32,ptr,i32,ptr,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,double,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i32,i32,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,i32,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i64,ptr,i32,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,i64,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i16,i16,ptr,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           3    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           2    0.00%    0.00%  %class.btVector3 <- [ptr,float,float,ptr]
           2    0.00%    0.00%  %class.btVector3 <- [ptr,float,ptr]
           2    0.00%    0.00%  %class.btVector3 <- [ptr,ptr,i32,ptr,ptr]
           2    0.00%    0.00%  double <- [double,i32,ptr]
           2    0.00%    0.00%  double <- [double,i64,ptr]
           2    0.00%    0.00%  float <- [float,float,float,ptr,ptr]
           2    0.00%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           2    0.00%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr,ptr,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  float <- [ptr,ptr,float,float,ptr]
           2    0.00%    0.00%  float <- [ptr,ptr,float,i32,i32,ptr]
           2    0.00%    0.00%  float <- [ptr,ptr,float,ptr]
           2    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,float,ptr]
           2    0.00%    0.00%  fp128 <- [fp128,fp128,fp128,ptr]
           2    0.00%    0.00%  i16 <- [ptr,ptr,ptr,ptr,i32,i32,i16,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  i1 <- [double,i32,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,float,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,i1,i1,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,i1,ptr,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,i32,i32,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,ptr,i1,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,ptr,i32,i32,i1,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,float,float,ptr]
           2    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,ptr]
           2    0.00%    0.00%  i32 <- [double,i32,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  i32 <- [i16,ptr,ptr]
           2    0.00%    0.00%  i32 <- [i32,double,ptr,ptr]
           2    0.00%    0.00%  i32 <- [i32,i32,i16,i16,i32,ptr]
           2    0.00%    0.00%  i32 <- [i32,i64,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,i16,i8,ptr,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,i32,i32,i16,i8,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,i32,i32,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,i32,i8,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,i64,ptr,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,ptr,i64,ptr]
           2    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  i32 <- [i64,ptr,ptr]
           2    0.00%    0.00%  i32 <- [i8,i8,ptr]
           2    0.00%    0.00%  i32 <- [ptr,double,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i16,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,ptr,ptr,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i64,i64,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i64,ptr,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,double,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i1,i1,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,double,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,i32,i32,i32,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,i1,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i64,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i64,i64,i64,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i64,ptr,i32,i32,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i8,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,i8,ptr,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,float,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,i32,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  i64 <- [i32,i32,ptr]
           2    0.00%    0.00%  i64 <- [i32,ptr,ptr,i64,ptr]
           2    0.00%    0.00%  i64 <- [ptr,[2 x i64],ptr]
           2    0.00%    0.00%  i8 <- [i32,ptr]
           2    0.00%    0.00%  i8 <- [i8,i8,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,double,ptr,ptr]
           2    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [i32,i32,ptr,ptr]
           2    0.00%    0.00%  ptr <- [i32,ptr,i32,i32,i32,i32,i32,i32,ptr]
           2    0.00%    0.00%  ptr <- [i32,ptr,ptr,i32,i32,i32,ptr]
           2    0.00%    0.00%  ptr <- [i32,ptr,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [i32,ptr,ptr,ptr,i64,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i16,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i32,i32,ptr,i32,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i32,ptr,i32,i32,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i32,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i8,i64,ptr]
           2    0.00%    0.00%  ptr <- [ptr,i8,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i16,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i64,i64,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,i64,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i1,i1,ptr]
           2    0.00%    0.00%  void <- [i16,i32,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  void <- [i16,i32,ptr]
           2    0.00%    0.00%  void <- [i16,i32,ptr,ptr]
           2    0.00%    0.00%  void <- [i16,ptr]
           2    0.00%    0.00%  void <- [i16,ptr,i16,ptr]
           2    0.00%    0.00%  void <- [i32,float,float,float,ptr]
           2    0.00%    0.00%  void <- [i32,i32,i32,ptr,i32,ptr,ptr]
           2    0.00%    0.00%  void <- [i32,i32,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [i8,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,float,float,float,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,float,ptr,ptr,float,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,i1,i1,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,i16,i1,i1,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,i32,ptr,i32,i16,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,i32,ptr,ptr,i16,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,i64,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,i64,i64,i32,i64,ptr]
           2    0.00%    0.00%  void <- [ptr,i64,i64,i64,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,i8,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,i1,i1,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,i1,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,double,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,i32,i64,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,float,float,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,i16,i32,i32,i32,i32,i32,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,float,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,i32,ptr,ptr,ptr]
           2    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  %class.btVector4 <- [ptr,ptr]
           1    0.00%    0.00%  [2 x i64] <- [ptr,[2 x i64],[2 x i64],[2 x i64],ptr]
           1    0.00%    0.00%  [2 x i64] <- [ptr,[2 x i64],ptr]
           1    0.00%    0.00%  double <- [ptr,i32,i32,double,double,i32,ptr]
           1    0.00%    0.00%  double <- [ptr,i32,i32,i32,double,double,i32,ptr]
           1    0.00%    0.00%  double <- [ptr,i64,ptr]
           1    0.00%    0.00%  double <- [ptr,ptr,double,i32,i32,i16,i16,i16,ptr]
           1    0.00%    0.00%  double <- [ptr,ptr,ptr,i64,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  double <- [ptr,ptr,ptr,i64,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  double <- [ptr,ptr,ptr,ptr,double,i1,ptr]
           1    0.00%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,float,float,ptr]
           1    0.00%    0.00%  float <- [ptr,float,float,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,float,ptr,float,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,float,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,i32,i32,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,float,float,float,float,i32,i32,ptr,ptr,float,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,i32,i32,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,float,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,float,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,float,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  i16 <- [ptr,ptr,ptr,ptr,i16,i16,ptr,ptr,ptr]
           1    0.00%    0.00%  i1 <- [double,double,i64,ptr]
           1    0.00%    0.00%  i1 <- [i1,i1,ptr]
           1    0.00%    0.00%  i1 <- [i16,ptr]
           1    0.00%    0.00%  i1 <- [i32,i32,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i1 <- [i8,i8,ptr]
           1    0.00%    0.00%  i1 <- [ptr,[2 x i64],[2 x i64],ptr]
           1    0.00%    0.00%  i1 <- [ptr,i1,i1,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i32,i32,float,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i1,i1,i1,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i32,i1,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i32,i32,ptr,i32,i32,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,float,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,float,ptr,ptr,ptr,float,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,float,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [double,double,i32,i32,double,ptr]
           1    0.00%    0.00%  i32 <- [float,float,i32,i32,double,ptr]
           1    0.00%    0.00%  i32 <- [i16,i16,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i16,i32,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i16,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i16,i64,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i1,ptr]
           1    0.00%    0.00%  i32 <- [i32,i32,double,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i32,i16,i16,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [i32,i32,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i64,i32,ptr,i64,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i64,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i64,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i8,i8,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,i16,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,i32,i32,i32,i32,i32,i32,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,i32,ptr,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,i64,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [i64,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i8,i32,ptr]
           1    0.00%    0.00%  i32 <- [i8,ptr,ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,float,i32,float,ptr]
           1    0.00%    0.00%  i32 <- [ptr,float,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i16,i16,i32,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i16,i16,i32,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,ptr,ptr,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,ptr,ptr,i32,i32,i32,ptr,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i16,i32,i32,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i16,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,float,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i16,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,double,double,double,i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,double,double,double,i32,i32,ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr,i32,i16,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,i32,i32,i32,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i8,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i64,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,double,double,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,i16,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,i64,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,i64,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i8,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,double,double,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,double,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,double,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,double,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,double,double,i64,double,double,double,i32,double,double,double,i64,i32,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,double,double,i64,double,double,double,i32,double,double,double,i64,i64,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,double,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i64,i64,i64,i64,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i64,i64,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,double,double,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i64,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i16,i16,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i64,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,i1,i1,ptr,i1,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i64 <- [i1,i32,ptr]
           1    0.00%    0.00%  i64 <- [i32,i32,i64,ptr]
           1    0.00%    0.00%  i64 <- [i32,i64,i64,i64,ptr]
           1    0.00%    0.00%  i64 <- [i64,i1,ptr]
           1    0.00%    0.00%  i64 <- [i64,i64,i64,i64,i32,ptr]
           1    0.00%    0.00%  i64 <- [ptr,i64,i32,ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,i64,ptr,ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i8 <- [ptr,i32,i32,ptr]
           1    0.00%    0.00%  i8 <- [ptr,ptr,i32,ptr]
           1    0.00%    0.00%  ptr <- [[2 x ptr],[2 x ptr],ptr,ptr]
           1    0.00%    0.00%  ptr <- [double,ptr]
           1    0.00%    0.00%  ptr <- [i32,i32,i32,i8,ptr]
           1    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,double,ptr]
           1    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [i32,i64,ptr,ptr]
           1    0.00%    0.00%  ptr <- [i32,ptr,ptr,i32,double,ptr]
           1    0.00%    0.00%  ptr <- [i32,ptr,ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  ptr <- [i32,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  ptr <- [i32,ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  ptr <- [ptr,double,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i32,i1,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i64,i64,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i8,i32,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i8,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,ptr,i32,ptr,i32,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i64,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [[2 x i64],ptr]
           1    0.00%    0.00%  void <- [double,ptr,ptr,double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i1,i1,ptr]
           1    0.00%    0.00%  void <- [double,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [double,ptr,ptr,ptr,double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i1,double,double,i1,i1,ptr]
           1    0.00%    0.00%  void <- [i32,i16,i32,i32,i32,i32,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i16,i32,i32,ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i32,i32,i16,i16,i32,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i16,i16,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i32,i32,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,i32,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,ptr,i32,i1,i32,ptr]
           1    0.00%    0.00%  void <- [i64,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [i8,i8,ptr]
           1    0.00%    0.00%  void <- [ptr,double,double,ptr]
           1    0.00%    0.00%  void <- [ptr,double,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,float,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,float,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i1,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i1,ptr,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,i64,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,i64,i64,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,i64,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,i64,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,i64,i64,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,i64,i64,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,ptr,i64,i32,ptr,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i8,i64,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,double,double,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,float,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,float,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,float,ptr,i32,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i1,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i1,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i16,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i16,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,i8,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,i8,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,i32,i32,ptr,i32,ptr,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i64,i64,i64,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i64,ptr,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i16,i16,i16,ptr,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,ptr,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i64,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,float,float,float,float,ptr,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr,ptr,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i16,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,float,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
```

### alloca

```text
       count  opcode%   total%  types
     151,232  100.00%    8.02%  ptr <- [i32]
           6    0.00%    0.00%  ptr <- [i64]
```

### icmp

```text
       count  opcode%   total%  types
      49,435   69.03%    2.62%  i1 <- [i32,i32]
      15,476   21.61%    0.82%  i1 <- [ptr,ptr]
       3,365    4.70%    0.18%  i1 <- [i8,i8]
       3,181    4.44%    0.17%  i1 <- [i64,i64]
         161    0.22%    0.01%  i1 <- [i16,i16]
```

### ret

```text
       count  opcode%   total%  types
      21,217   50.44%    1.13%  void <- [-]
      10,055   23.90%    0.53%  void <- [ptr]
       7,125   16.94%    0.38%  void <- [i32]
       1,180    2.81%    0.06%  void <- [i1]
         790    1.88%    0.04%  void <- [float]
         734    1.74%    0.04%  void <- [i64]
         597    1.42%    0.03%  void <- [%class.btVector3]
         196    0.47%    0.01%  void <- [double]
          60    0.14%    0.00%  void <- [i8]
          48    0.11%    0.00%  void <- [[2 x i64]]
          34    0.08%    0.00%  void <- [%class.btQuaternion]
          28    0.07%    0.00%  void <- [i16]
           1    0.00%    0.00%  void <- [%class.btVector4]
```

### sext

```text
       count  opcode%   total%  types
      32,925   91.27%    1.75%  i64 <- [i32]
       2,283    6.33%    0.12%  i32 <- [i16]
         461    1.28%    0.02%  i64 <- [i16]
         354    0.98%    0.02%  i32 <- [i8]
          46    0.13%    0.00%  i16 <- [i8]
           4    0.01%    0.00%  i64 <- [i8]
```

### add

```text
       count  opcode%   total%  types
      25,390   90.70%    1.35%  i32 <- [i32,i32]
       2,384    8.52%    0.13%  i64 <- [i64,i64]
         153    0.55%    0.01%  i16 <- [i16,i16]
          66    0.24%    0.00%  i8 <- [i8,i8]
```

### zext

```text
       count  opcode%   total%  types
      11,355   41.20%    0.60%  i32 <- [i8]
       6,245   22.66%    0.33%  i64 <- [i32]
       4,817   17.48%    0.26%  i32 <- [i16]
       1,670    6.06%    0.09%  i32 <- [i1]
       1,194    4.33%    0.06%  i64 <- [i8]
         958    3.48%    0.05%  i8 <- [i1]
         928    3.37%    0.05%  i64 <- [i1]
         311    1.13%    0.02%  i64 <- [i16]
          82    0.30%    0.00%  i16 <- [i8]
```

### invoke

```text
       count  opcode%   total%  types
       3,188   26.41%    0.17%  void <- [ptr,label,label,ptr]
       1,204    9.97%    0.06%  ptr <- [ptr,label,label,ptr]
         950    7.87%    0.05%  i32 <- [ptr,label,label,ptr]
         871    7.22%    0.05%  void <- [ptr,ptr,label,label,ptr]
         858    7.11%    0.05%  ptr <- [ptr,i32,label,label,ptr]
         703    5.82%    0.04%  ptr <- [ptr,ptr,label,label,ptr]
         595    4.93%    0.03%  void <- [ptr,ptr,ptr,label,label,ptr]
         335    2.78%    0.02%  i32 <- [ptr,ptr,label,label,ptr]
         287    2.38%    0.02%  i1 <- [ptr,label,label,ptr]
         238    1.97%    0.01%  void <- [ptr,ptr,ptr,ptr,label,label,ptr]
         183    1.52%    0.01%  void <- [ptr,i32,label,label,ptr]
         149    1.23%    0.01%  void <- [ptr,ptr,i32,label,label,ptr]
         135    1.12%    0.01%  i32 <- [ptr,i32,label,label,ptr]
         126    1.04%    0.01%  ptr <- [i64,label,label,ptr]
         125    1.04%    0.01%  i32 <- [ptr,ptr,ptr,label,label,ptr]
         114    0.94%    0.01%  %class.btVector3 <- [ptr,ptr,label,label,ptr]
         113    0.94%    0.01%  i64 <- [ptr,label,label,ptr]
         110    0.91%    0.01%  void <- [label,label,ptr]
         104    0.86%    0.01%  i1 <- [ptr,ptr,label,label,ptr]
         103    0.85%    0.01%  void <- [ptr,i32,ptr,label,label,ptr]
          72    0.60%    0.00%  ptr <- [ptr,i64,label,label,ptr]
          64    0.53%    0.00%  float <- [ptr,label,label,ptr]
          55    0.46%    0.00%  i32 <- [ptr,i64,label,label,ptr]
          53    0.44%    0.00%  i32 <- [ptr,i32,i32,ptr,label,label,ptr]
          52    0.43%    0.00%  void <- [ptr,float,label,label,ptr]
          50    0.41%    0.00%  void <- [ptr,i64,label,label,ptr]
          46    0.38%    0.00%  ptr <- [i64,i32,label,label,ptr]
          34    0.28%    0.00%  i32 <- [ptr,i64,i32,ptr,label,label,ptr]
          32    0.27%    0.00%  i32 <- [ptr,i32,ptr,label,label,ptr]
          32    0.27%    0.00%  ptr <- [ptr,i8,label,label,ptr]
          32    0.27%    0.00%  void <- [ptr,i8,label,label,ptr]
          31    0.26%    0.00%  float <- [ptr,ptr,label,label,ptr]
          29    0.24%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          29    0.24%    0.00%  void <- [ptr,i1,label,label,ptr]
          29    0.24%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          26    0.22%    0.00%  void <- [ptr,i32,i32,label,label,ptr]
          25    0.21%    0.00%  i1 <- [ptr,i32,label,label,ptr]
          23    0.19%    0.00%  i32 <- [ptr,i1,label,label,ptr]
          22    0.18%    0.00%  %class.btVector3 <- [ptr,label,label,ptr]
          22    0.18%    0.00%  i32 <- [ptr,ptr,i32,label,label,ptr]
          20    0.17%    0.00%  void <- [ptr,ptr,i1,label,label,ptr]
          19    0.16%    0.00%  i1 <- [i32,label,label,ptr]
          18    0.15%    0.00%  i32 <- [ptr,i32,i32,label,label,ptr]
          17    0.14%    0.00%  i1 <- [ptr,ptr,ptr,label,label,ptr]
          17    0.14%    0.00%  ptr <- [label,label,ptr]
          16    0.13%    0.00%  i32 <- [ptr,ptr,ptr,ptr,label,label,ptr]
          15    0.12%    0.00%  i32 <- [label,label,ptr]
          15    0.12%    0.00%  ptr <- [ptr,i1,label,label,ptr]
          15    0.12%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          14    0.12%    0.00%  i1 <- [ptr,ptr,i1,label,label,ptr]
          13    0.11%    0.00%  i32 <- [ptr,i32,ptr,i32,label,label,ptr]
          13    0.11%    0.00%  ptr <- [ptr,ptr,ptr,label,label,ptr]
          13    0.11%    0.00%  void <- [ptr,float,float,label,label,ptr]
          12    0.10%    0.00%  ptr <- [ptr,i64,ptr,label,label,ptr]
          12    0.10%    0.00%  void <- [ptr,ptr,ptr,ptr,i1,label,label,ptr]
          12    0.10%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          11    0.09%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          11    0.09%    0.00%  i32 <- [ptr,ptr,i32,ptr,label,label,ptr]
          11    0.09%    0.00%  i32 <- [ptr,ptr,i64,label,label,ptr]
          11    0.09%    0.00%  i32 <- [ptr,ptr,ptr,i32,label,label,ptr]
          11    0.09%    0.00%  void <- [ptr,i32,i32,ptr,i1,label,label,ptr]
          10    0.08%    0.00%  i1 <- [ptr,i32,ptr,label,label,ptr]
          10    0.08%    0.00%  ptr <- [ptr,i32,i32,label,label,ptr]
          10    0.08%    0.00%  void <- [ptr,i32,ptr,ptr,label,label,ptr]
           9    0.07%    0.00%  i1 <- [i32,ptr,label,label,ptr]
           9    0.07%    0.00%  i8 <- [ptr,label,label,ptr]
           9    0.07%    0.00%  void <- [ptr,ptr,i64,label,label,ptr]
           9    0.07%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,float,label,label,ptr]
           8    0.07%    0.00%  float <- [float,label,label,ptr]
           8    0.07%    0.00%  ptr <- [ptr,ptr,ptr,ptr,label,label,ptr]
           8    0.07%    0.00%  void <- [i32,ptr,label,label,ptr]
           8    0.07%    0.00%  void <- [ptr,ptr,ptr,float,label,label,ptr]
           7    0.06%    0.00%  i16 <- [ptr,label,label,ptr]
           7    0.06%    0.00%  i1 <- [ptr,ptr,ptr,ptr,label,label,ptr]
           7    0.06%    0.00%  i32 <- [ptr,ptr,i1,label,label,ptr]
           7    0.06%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           7    0.06%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           7    0.06%    0.00%  void <- [i32,i32,ptr,label,label,ptr]
           7    0.06%    0.00%  void <- [ptr,ptr,float,label,label,ptr]
           7    0.06%    0.00%  void <- [ptr,ptr,ptr,i32,label,label,ptr]
           6    0.05%    0.00%  %class.btQuaternion <- [ptr,ptr,label,label,ptr]
           6    0.05%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,label,label,ptr]
           6    0.05%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,label,label,ptr]
           6    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,label,label,ptr]
           5    0.04%    0.00%  %class.btVector3 <- [ptr,i32,label,label,ptr]
           5    0.04%    0.00%  i1 <- [ptr,ptr,i32,ptr,label,label,ptr]
           5    0.04%    0.00%  i32 <- [i32,label,label,ptr]
           5    0.04%    0.00%  i32 <- [i64,ptr,i1,label,label,ptr]
           5    0.04%    0.00%  i32 <- [ptr,[2 x i64],label,label,ptr]
           5    0.04%    0.00%  i32 <- [ptr,ptr,ptr,i1,ptr,ptr,ptr,label,label,ptr]
           5    0.04%    0.00%  i64 <- [ptr,i32,label,label,ptr]
           5    0.04%    0.00%  void <- [ptr,ptr,i32,i32,label,label,ptr]
           5    0.04%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           4    0.03%    0.00%  i32 <- [ptr,i32,ptr,ptr,label,label,ptr]
           4    0.03%    0.00%  i32 <- [ptr,i64,ptr,label,label,ptr]
           4    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,i32,ptr,label,label,ptr]
           4    0.03%    0.00%  i64 <- [label,label,ptr]
           4    0.03%    0.00%  i64 <- [ptr,i32,i32,label,label,ptr]
           4    0.03%    0.00%  i64 <- [ptr,ptr,label,label,ptr]
           4    0.03%    0.00%  ptr <- [ptr,i32,i32,i32,label,label,ptr]
           4    0.03%    0.00%  ptr <- [ptr,ptr,i32,label,label,ptr]
           4    0.03%    0.00%  void <- [i32,i32,ptr,ptr,label,label,ptr]
           4    0.03%    0.00%  void <- [i64,ptr,i32,label,label,ptr]
           4    0.03%    0.00%  void <- [ptr,i32,i32,i32,label,label,ptr]
           4    0.03%    0.00%  void <- [ptr,ptr,i1,i32,i32,label,label,ptr]
           4    0.03%    0.00%  void <- [ptr,ptr,i1,i32,label,label,ptr]
           3    0.02%    0.00%  %class.btQuaternion <- [ptr,label,label,ptr]
           3    0.02%    0.00%  %class.btVector3 <- [ptr,ptr,float,label,label,ptr]
           3    0.02%    0.00%  i1 <- [i8,i8,label,label,ptr]
           3    0.02%    0.00%  i1 <- [i8,label,label,ptr]
           3    0.02%    0.00%  i1 <- [label,label,ptr]
           3    0.02%    0.00%  i1 <- [ptr,i1,ptr,i1,label,label,ptr]
           3    0.02%    0.00%  i1 <- [ptr,i64,label,label,ptr]
           3    0.02%    0.00%  i1 <- [ptr,ptr,i32,label,label,ptr]
           3    0.02%    0.00%  i32 <- [i64,ptr,ptr,i1,label,label,ptr]
           3    0.02%    0.00%  i32 <- [ptr,i32,i1,i32,ptr,ptr,label,label,ptr]
           3    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,label,label,ptr]
           3    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,i1,ptr,ptr,ptr,label,label,ptr]
           3    0.02%    0.00%  i32 <- [ptr,ptr,i64,ptr,ptr,ptr,ptr,ptr,ptr,i1,i32,label,label,ptr]
           3    0.02%    0.00%  ptr <- [i64,ptr,label,label,ptr]
           3    0.02%    0.00%  void <- [ptr,float,ptr,label,label,ptr]
           3    0.02%    0.00%  void <- [ptr,i1,i8,ptr,label,label,ptr]
           3    0.02%    0.00%  void <- [ptr,i32,i1,label,label,ptr]
           3    0.02%    0.00%  void <- [ptr,ptr,i32,i1,label,label,ptr]
           3    0.02%    0.00%  void <- [ptr,ptr,i64,ptr,i64,ptr,label,label,ptr]
           2    0.02%    0.00%  %class.btVector3 <- [ptr,ptr,i32,label,label,ptr]
           2    0.02%    0.00%  %class.btVector3 <- [ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  float <- [ptr,ptr,i1,label,label,ptr]
           2    0.02%    0.00%  float <- [ptr,ptr,i32,ptr,i32,ptr,i32,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i1 <- [[2 x i64],i16,ptr,label,label,ptr]
           2    0.02%    0.00%  i1 <- [i64,ptr,label,label,ptr]
           2    0.02%    0.00%  i1 <- [ptr,i32,i32,ptr,label,label,ptr]
           2    0.02%    0.00%  i1 <- [ptr,ptr,i1,ptr,label,label,ptr]
           2    0.02%    0.00%  i1 <- [ptr,ptr,i64,label,label,ptr]
           2    0.02%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,float,float,label,label,ptr]
           2    0.02%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [i1,i32,label,label,ptr]
           2    0.02%    0.00%  i32 <- [i1,label,label,ptr]
           2    0.02%    0.00%  i32 <- [i32,i32,label,label,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [i64,ptr,ptr,ptr,i1,i1,label,label,ptr]
           2    0.02%    0.00%  i32 <- [i8,i8,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,i1,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,i1,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i64,i64,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i64,i64,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i8,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i32,i1,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,ptr,float,label,label,ptr]
           2    0.02%    0.00%  i64 <- [i64,i64,i64,label,label,ptr]
           2    0.02%    0.00%  i64 <- [i64,label,label,ptr]
           2    0.02%    0.00%  i8 <- [i8,label,label,ptr]
           2    0.02%    0.00%  i8 <- [ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  ptr <- [ptr,i64,i64,label,label,ptr]
           2    0.02%    0.00%  ptr <- [ptr,i64,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  ptr <- [ptr,ptr,i64,label,label,ptr]
           2    0.02%    0.00%  void <- [i64,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,float,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i1,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i16,i64,i1,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i16,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i32,float,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i32,i32,i32,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i32,i32,ptr,float,float,float,i32,i32,i1,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i64,i32,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,i64,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,float,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,float,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,i1,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,i32,i32,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,i64,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,i8,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,ptr,float,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,float,ptr,ptr,ptr,label,label,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  [2 x i64] <- [ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  [2 x i64] <- [ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  float <- [label,label,ptr]
           1    0.01%    0.00%  float <- [ptr,i32,label,label,ptr]
           1    0.01%    0.00%  float <- [ptr,ptr,float,label,label,ptr]
           1    0.01%    0.00%  float <- [ptr,ptr,ptr,float,i32,i32,label,label,ptr]
           1    0.01%    0.00%  float <- [ptr,ptr,ptr,float,i32,label,label,ptr]
           1    0.01%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i1 <- [float,label,label,ptr]
           1    0.01%    0.00%  i1 <- [i16,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,i32,i32,i32,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,i32,i32,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,i32,ptr,i32,ptr,ptr,float,ptr,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,i32,ptr,ptr,i32,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,ptr,i32,i32,i32,i32,i1,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i32,i32,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i1,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i1,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i1,ptr,ptr,ptr,i1,i1,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i1,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,i1,i1,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i64,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i64 <- [ptr,[2 x i64],label,label,ptr]
           1    0.01%    0.00%  i64 <- [ptr,ptr,i64,label,label,ptr]
           1    0.01%    0.00%  ptr <- [ptr,float,label,label,ptr]
           1    0.01%    0.00%  void <- [i32,i1,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [i32,label,label,ptr]
           1    0.01%    0.00%  void <- [i32,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,double,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,float,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i1,i32,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i1,ptr,i1,i1,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i32,i32,ptr,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i32,i64,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i32,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,ptr,i64,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,float,float,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,float,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i1,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,i8,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,float,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i16,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,float,float,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,i32,float,float,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,i64,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,i16,i16,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,i16,i16,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i1,i1,i1,ptr,ptr,i64,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i16,i16,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
```

### extractvalue

```text
       count  opcode%   total%  types
       4,684   41.93%    0.25%  ptr <- [{ ptr, i32 }]
       3,657   32.74%    0.19%  i32 <- [{ ptr, i32 }]
       2,566   22.97%    0.14%  [4 x float] <- [%class.btVector3]
          93    0.83%    0.00%  i1 <- [{ i64, i1 }]
          93    0.83%    0.00%  i64 <- [{ i64, i1 }]
          73    0.65%    0.00%  %class.btQuadWord <- [%class.btQuaternion]
           4    0.04%    0.00%  i64 <- [{ i64, i64 }]
           1    0.01%    0.00%  %class.btVector3 <- [%class.btVector4]
```

### sub

```text
       count  opcode%   total%  types
       8,192   80.99%    0.43%  i32 <- [i32,i32]
       1,923   19.01%    0.10%  i64 <- [i64,i64]
```

### phi

```text
       count  opcode%   total%  types
       3,888   48.72%    0.21%  ptr <- [ptr,ptr]
       1,978   24.79%    0.10%  i32 <- [i32,i32]
       1,422   17.82%    0.08%  i1 <- [i1,i1]
         179    2.24%    0.01%  i64 <- [i64,i64]
         170    2.13%    0.01%  i1 <- [i1,i1,i1]
         169    2.12%    0.01%  float <- [float,float]
          65    0.81%    0.00%  i1 <- [i1,i1,i1,i1]
          51    0.64%    0.00%  double <- [double,double]
          20    0.25%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1]
          18    0.23%    0.00%  i1 <- [i1,i1,i1,i1,i1]
           6    0.08%    0.00%  i16 <- [i16,i16]
           6    0.08%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1]
           3    0.04%    0.00%  i8 <- [i8,i8]
           2    0.03%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1,i1]
           2    0.03%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1]
           1    0.01%    0.00%  fp128 <- [fp128,fp128]
```

### and

```text
       count  opcode%   total%  types
       4,669   64.64%    0.25%  i32 <- [i32,i32]
       1,423   19.70%    0.08%  i16 <- [i16,i16]
         867   12.00%    0.05%  i8 <- [i8,i8]
         264    3.65%    0.01%  i64 <- [i64,i64]
```

### trunc

```text
       count  opcode%   total%  types
       1,881   34.00%    0.10%  i16 <- [i32]
       1,669   30.16%    0.09%  i32 <- [i64]
       1,642   29.68%    0.09%  i8 <- [i32]
         267    4.83%    0.01%  i8 <- [i64]
          46    0.83%    0.00%  i8 <- [i16]
          28    0.51%    0.00%  i16 <- [i64]
```

### landingpad

```text
       count  opcode%   total%  types
       3,267   69.75%    0.17%  { ptr, i32 } <- [-]
       1,090   23.27%    0.06%  { ptr, i32 } <- [ptr]
         315    6.73%    0.02%  { ptr, i32 } <- [ptr,ptr]
          11    0.23%    0.00%  { ptr, i32 } <- [ptr,ptr,ptr]
           1    0.02%    0.00%  { ptr, i32 } <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
```

### unreachable

```text
       count  opcode%   total%  types
       4,180  100.00%    0.22%  void <- [-]
```

### shl

```text
       count  opcode%   total%  types
       3,487   84.11%    0.18%  i32 <- [i32,i32]
         287    6.92%    0.02%  i16 <- [i16,i16]
         224    5.40%    0.01%  i64 <- [i64,i64]
         148    3.57%    0.01%  i8 <- [i8,i8]
```

### mul

```text
       count  opcode%   total%  types
       3,005   75.09%    0.16%  i32 <- [i32,i32]
         997   24.91%    0.05%  i64 <- [i64,i64]
```

### or

```text
       count  opcode%   total%  types
       2,554   69.69%    0.14%  i32 <- [i32,i32]
         602   16.43%    0.03%  i16 <- [i16,i16]
         364    9.93%    0.02%  i8 <- [i8,i8]
         138    3.77%    0.01%  i64 <- [i64,i64]
           7    0.19%    0.00%  i1 <- [i1,i1]
```

### fmul

```text
       count  opcode%   total%  types
       2,443   75.54%    0.13%  float <- [float,float]
         778   24.06%    0.04%  double <- [double,double]
          13    0.40%    0.00%  fp128 <- [fp128,fp128]
```

### lshr

```text
       count  opcode%   total%  types
       1,719   64.24%    0.09%  i32 <- [i32,i32]
         591   22.09%    0.03%  i16 <- [i16,i16]
         191    7.14%    0.01%  i8 <- [i8,i8]
         175    6.54%    0.01%  i64 <- [i64,i64]
```

### xor

```text
       count  opcode%   total%  types
       1,355   55.72%    0.07%  i1 <- [i1,i1]
       1,051   43.22%    0.06%  i32 <- [i32,i32]
          26    1.07%    0.00%  i64 <- [i64,i64]
```

### ptrtoint

```text
       count  opcode%   total%  types
       1,682   90.72%    0.09%  i64 <- [ptr]
         172    9.28%    0.01%  i32 <- [ptr]
```

### fcmp

```text
       count  opcode%   total%  types
       1,526   83.52%    0.08%  i1 <- [float,float]
         292   15.98%    0.02%  i1 <- [double,double]
           9    0.49%    0.00%  i1 <- [fp128,fp128]
```

### fadd

```text
       count  opcode%   total%  types
       1,410   79.66%    0.07%  float <- [float,float]
         358   20.23%    0.02%  double <- [double,double]
           2    0.11%    0.00%  fp128 <- [fp128,fp128]
```

### switch

```text
       count  opcode%   total%  types
         451   29.13%    0.02%  void <- [i32,label,label,label]
         407   26.29%    0.02%  void <- [i32,label,label]
         253   16.34%    0.01%  void <- [i32,label,label,label,label]
         136    8.79%    0.01%  void <- [i32,label,label,label,label,label]
          64    4.13%    0.00%  void <- [i32,label,label,label,label,label,label]
          49    3.17%    0.00%  void <- [i32,label,label,label,label,label,label,label]
          30    1.94%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
          19    1.23%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
          14    0.90%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
          11    0.71%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label]
           9    0.58%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label]
           8    0.52%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label]
           8    0.52%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           6    0.39%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           5    0.32%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           5    0.32%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           4    0.26%    0.00%  void <- [i32,label]
           4    0.26%    0.00%  void <- [i64,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           3    0.19%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           3    0.19%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           3    0.19%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           3    0.19%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i64,label,label,label]
           2    0.13%    0.00%  void <- [i64,label,label,label,label]
           2    0.13%    0.00%  void <- [i64,label,label,label,label,label,label,label,label]
           2    0.13%    0.00%  void <- [i64,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i64,label,label]
           1    0.06%    0.00%  void <- [i64,label,label,label,label,label,label,label]
           1    0.06%    0.00%  void <- [i64,label,label,label,label,label,label,label,label,label]
```

### ashr

```text
       count  opcode%   total%  types
       1,475   98.20%    0.08%  i32 <- [i32,i32]
          16    1.07%    0.00%  i64 <- [i64,i64]
          11    0.73%    0.00%  i8 <- [i8,i8]
```

### fsub

```text
       count  opcode%   total%  types
         834   68.30%    0.04%  float <- [float,float]
         386   31.61%    0.02%  double <- [double,double]
           1    0.08%    0.00%  fp128 <- [fp128,fp128]
```

### sdiv

```text
       count  opcode%   total%  types
         762   64.96%    0.04%  i32 <- [i32,i32]
         411   35.04%    0.02%  i64 <- [i64,i64]
```

### sitofp

```text
       count  opcode%   total%  types
         553   47.26%    0.03%  double <- [i32]
         478   40.85%    0.03%  float <- [i32]
          70    5.98%    0.00%  float <- [i64]
          64    5.47%    0.00%  double <- [i64]
           3    0.26%    0.00%  fp128 <- [i32]
           2    0.17%    0.00%  float <- [i16]
```

### fdiv

```text
       count  opcode%   total%  types
         664   65.10%    0.04%  float <- [float,float]
         354   34.71%    0.02%  double <- [double,double]
           2    0.20%    0.00%  fp128 <- [fp128,fp128]
```

### select

```text
       count  opcode%   total%  types
         730   72.93%    0.04%  i32 <- [i1,i32,i32]
         143   14.29%    0.01%  ptr <- [i1,ptr,ptr]
          87    8.69%    0.00%  i64 <- [i1,i64,i64]
          13    1.30%    0.00%  float <- [i1,float,float]
          12    1.20%    0.00%  i8 <- [i1,i8,i8]
           7    0.70%    0.00%  i1 <- [i1,i1,i1]
           6    0.60%    0.00%  double <- [i1,double,double]
           3    0.30%    0.00%  i16 <- [i1,i16,i16]
```

### fneg

```text
       count  opcode%   total%  types
         831   92.33%    0.04%  float <- [float]
          67    7.44%    0.00%  double <- [double]
           2    0.22%    0.00%  fp128 <- [fp128]
```

### inttoptr

```text
       count  opcode%   total%  types
         814  100.00%    0.04%  ptr <- [i64]
```

### fpext

```text
       count  opcode%   total%  types
         772   99.61%    0.04%  double <- [float]
           3    0.39%    0.00%  fp128 <- [double]
```

### fptosi

```text
       count  opcode%   total%  types
         261   71.31%    0.01%  i32 <- [double]
          94   25.68%    0.00%  i32 <- [float]
           8    2.19%    0.00%  i64 <- [double]
           1    0.27%    0.00%  i16 <- [double]
           1    0.27%    0.00%  i32 <- [fp128]
           1    0.27%    0.00%  i64 <- [float]
```

### udiv

```text
       count  opcode%   total%  types
         180   52.17%    0.01%  i64 <- [i64,i64]
         165   47.83%    0.01%  i32 <- [i32,i32]
```

### urem

```text
       count  opcode%   total%  types
         249   80.32%    0.01%  i32 <- [i32,i32]
          61   19.68%    0.00%  i64 <- [i64,i64]
```

### srem

```text
       count  opcode%   total%  types
         295   97.04%    0.02%  i32 <- [i32,i32]
           9    2.96%    0.00%  i64 <- [i64,i64]
```

### fptrunc

```text
       count  opcode%   total%  types
         294   99.66%    0.02%  float <- [double]
           1    0.34%    0.00%  double <- [fp128]
```

### uitofp

```text
       count  opcode%   total%  types
          14   26.42%    0.00%  float <- [i32]
          12   22.64%    0.00%  float <- [i16]
           9   16.98%    0.00%  double <- [i32]
           8   15.09%    0.00%  double <- [i16]
           8   15.09%    0.00%  float <- [i64]
           2    3.77%    0.00%  double <- [i64]
```

### fptoui

```text
       count  opcode%   total%  types
          24   70.59%    0.00%  i16 <- [float]
           3    8.82%    0.00%  i32 <- [float]
           3    8.82%    0.00%  i64 <- [float]
           2    5.88%    0.00%  i32 <- [double]
           1    2.94%    0.00%  i64 <- [double]
           1    2.94%    0.00%  i8 <- [double]
```

## IR type detail by workload

### 7zip

#### load

```text
       count  opcode%   total%  types
      36,777   51.87%   12.46%  ptr <- [ptr]
      25,997   36.66%    8.80%  i32 <- [ptr]
       3,662    5.16%    1.24%  i64 <- [ptr]
       3,508    4.95%    1.19%  i8 <- [ptr]
         700    0.99%    0.24%  i16 <- [ptr]
         250    0.35%    0.08%  i1 <- [ptr]
          11    0.02%    0.00%  [2 x i64] <- [ptr]
```

#### store

```text
       count  opcode%   total%  types
      21,850   45.07%    7.40%  void <- [ptr,ptr]
      20,983   43.28%    7.11%  void <- [i32,ptr]
       2,422    5.00%    0.82%  void <- [i64,ptr]
       2,173    4.48%    0.74%  void <- [i8,ptr]
         644    1.33%    0.22%  void <- [i1,ptr]
         399    0.82%    0.14%  void <- [i16,ptr]
           7    0.01%    0.00%  void <- [[2 x i64],ptr]
```

#### getelementptr

```text
       count  opcode%   total%  types
      25,672   69.33%    8.69%  ptr <- [ptr,i32,i32]
       8,241   22.25%    2.79%  ptr <- [ptr,i64]
       2,713    7.33%    0.92%  ptr <- [ptr,i64,i64]
         404    1.09%    0.14%  ptr <- [ptr,i32]
```

#### br

```text
       count  opcode%   total%  types
      19,930   64.56%    6.75%  void <- [label]
      10,942   35.44%    3.71%  void <- [i1,label,label]
```

#### alloca

```text
       count  opcode%   total%  types
      28,048  100.00%    9.50%  ptr <- [i32]
           1    0.00%    0.00%  ptr <- [i64]
```

#### call

```text
       count  opcode%   total%  types
       9,291   44.71%    3.15%  void <- [ptr,ptr]
       2,029    9.76%    0.69%  i32 <- [ptr,ptr]
         984    4.74%    0.33%  void <- [ptr,i64,ptr]
         703    3.38%    0.24%  ptr <- [ptr,ptr]
         676    3.25%    0.23%  i32 <- [ptr,ptr,ptr]
         661    3.18%    0.22%  void <- [ptr]
         644    3.10%    0.22%  void <- [ptr,i32,ptr]
         608    2.93%    0.21%  ptr <- [ptr,i32,ptr]
         606    2.92%    0.21%  ptr <- [ptr,ptr,ptr]
         489    2.35%    0.17%  void <- [ptr,ptr,ptr]
         468    2.25%    0.16%  ptr <- [i64,ptr]
         403    1.94%    0.14%  void <- [ptr,ptr,i64,i1,ptr]
         251    1.21%    0.09%  i32 <- [ptr,ptr,ptr,ptr]
         215    1.03%    0.07%  i1 <- [ptr,ptr]
         202    0.97%    0.07%  void <- [ptr,i32,i32,ptr]
         174    0.84%    0.06%  i32 <- [ptr,i32,ptr]
         133    0.64%    0.05%  void <- [ptr,ptr,i32,ptr]
         132    0.64%    0.04%  void <- [ptr,i32,ptr,ptr]
         119    0.57%    0.04%  i64 <- [ptr,ptr]
          95    0.46%    0.03%  i32 <- [ptr,ptr,i32,ptr]
          84    0.40%    0.03%  i32 <- [ptr,i64,ptr]
          84    0.40%    0.03%  void <- [ptr,i8,ptr]
          82    0.39%    0.03%  void <- [ptr,ptr,ptr,ptr]
          75    0.36%    0.03%  { i64, i1 } <- [i64,i64,ptr]
          67    0.32%    0.02%  i1 <- [ptr,ptr,ptr]
          67    0.32%    0.02%  i32 <- [ptr,ptr,i32,ptr,ptr]
          66    0.32%    0.02%  void <- [ptr,ptr,i64,ptr]
          65    0.31%    0.02%  void <- [ptr,ptr,i32,i32,ptr]
          63    0.30%    0.02%  ptr <- [ptr,i64,ptr]
          61    0.29%    0.02%  i8 <- [ptr,ptr]
          59    0.28%    0.02%  i1 <- [ptr,i32,ptr]
          55    0.26%    0.02%  i32 <- [ptr,ptr,i64,ptr]
          53    0.26%    0.02%  i32 <- [i32,ptr]
          45    0.22%    0.02%  i32 <- [ptr,i64,i32,ptr,ptr]
          37    0.18%    0.01%  i32 <- [ptr,i32,i32,ptr]
          36    0.17%    0.01%  void <- [ptr,i8,i64,i1,ptr]
          33    0.16%    0.01%  i32 <- [i32,i32,ptr]
          28    0.13%    0.01%  void <- [ptr,i16,ptr]
          27    0.13%    0.01%  i32 <- [ptr]
          27    0.13%    0.01%  i64 <- [i64,i64,ptr]
          27    0.13%    0.01%  void <- [i32,ptr]
          26    0.13%    0.01%  ptr <- [ptr]
          22    0.11%    0.01%  i32 <- [ptr,ptr,ptr,i32,ptr]
          22    0.11%    0.01%  void <- [ptr,i1,ptr]
          17    0.08%    0.01%  i32 <- [ptr,i32,i32,ptr,ptr]
          16    0.08%    0.01%  i1 <- [ptr,i32,ptr,ptr]
          16    0.08%    0.01%  i32 <- [ptr,i64,ptr,ptr]
          15    0.07%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr]
          15    0.07%    0.01%  i64 <- [ptr,i64,i32,i32,ptr]
          14    0.07%    0.00%  i32 <- [ptr,i32,ptr,ptr]
          13    0.06%    0.00%  i1 <- [ptr,ptr,i32,ptr]
          13    0.06%    0.00%  i32 <- [i32,ptr,i64,ptr]
          13    0.06%    0.00%  void <- [i32,ptr,ptr]
          12    0.06%    0.00%  i64 <- [ptr]
          12    0.06%    0.00%  void <- [ptr,ptr,i1,ptr]
          11    0.05%    0.00%  i16 <- [ptr,ptr]
          11    0.05%    0.00%  i1 <- [i32,ptr]
          11    0.05%    0.00%  ptr <- [ptr,i8,ptr]
          11    0.05%    0.00%  void <- [ptr,i32,i32,i32,ptr]
          11    0.05%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr]
          10    0.05%    0.00%  i1 <- [ptr]
          10    0.05%    0.00%  i64 <- [ptr,ptr,i64,ptr]
           9    0.04%    0.00%  i32 <- [ptr,i1,ptr]
           8    0.04%    0.00%  i1 <- [ptr,i64,ptr]
           8    0.04%    0.00%  i32 <- [i1,ptr]
           8    0.04%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr]
           8    0.04%    0.00%  ptr <- [i32,ptr,ptr]
           7    0.03%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,ptr,ptr]
           7    0.03%    0.00%  i32 <- [ptr,i8,ptr]
           7    0.03%    0.00%  i32 <- [ptr,ptr,i64,i32,ptr]
           7    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           7    0.03%    0.00%  i64 <- [ptr,ptr,ptr]
           7    0.03%    0.00%  ptr <- [i32,i32,i32,ptr,ptr,i32,i32,i32,ptr,i32,ptr]
           7    0.03%    0.00%  ptr <- [ptr,i32,ptr,ptr]
           7    0.03%    0.00%  void <- [i64,ptr,ptr]
           7    0.03%    0.00%  void <- [ptr,i32,ptr,ptr,ptr]
           6    0.03%    0.00%  i1 <- [ptr,ptr,i1,ptr]
           6    0.03%    0.00%  i1 <- [ptr,ptr,ptr,i32,ptr]
           6    0.03%    0.00%  i1 <- [ptr,ptr,ptr,ptr]
           6    0.03%    0.00%  i32 <- [i64,i64,ptr]
           6    0.03%    0.00%  i32 <- [ptr,i64,i64,ptr]
           6    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.03%    0.00%  i64 <- [i32,ptr,i64,ptr]
           6    0.03%    0.00%  void <- [i32,i32,i32,ptr,ptr,i32,i32,i32,ptr]
           6    0.03%    0.00%  void <- [i64,ptr,i32,ptr]
           5    0.02%    0.00%  i1 <- [ptr,ptr,i32,ptr,ptr]
           5    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,ptr]
           5    0.02%    0.00%  i32 <- [ptr,ptr,i1,ptr]
           5    0.02%    0.00%  i64 <- [i32,i64,i32,ptr]
           5    0.02%    0.00%  i8 <- [ptr,i32,ptr]
           5    0.02%    0.00%  i8 <- [ptr,ptr,ptr]
           5    0.02%    0.00%  void <- [ptr,i32,i1,ptr]
           5    0.02%    0.00%  void <- [ptr,i32,i8,ptr]
           4    0.02%    0.00%  i1 <- [ptr,i1,ptr,i1,ptr]
           4    0.02%    0.00%  i1 <- [ptr,i32,i32,ptr]
           4    0.02%    0.00%  i1 <- [ptr,i64,i32,ptr,ptr]
           4    0.02%    0.00%  i1 <- [ptr,i8,ptr]
           4    0.02%    0.00%  i32 <- [i16,i16,ptr]
           4    0.02%    0.00%  i32 <- [i64,ptr]
           4    0.02%    0.00%  i32 <- [i8,ptr]
           4    0.02%    0.00%  i32 <- [ptr,[2 x i64],ptr]
           4    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i64,ptr]
           4    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           4    0.02%    0.00%  void <- [i32,ptr,i32,ptr]
           4    0.02%    0.00%  void <- [ptr,i1,i1,ptr]
           4    0.02%    0.00%  void <- [ptr,i32,i1,i64,ptr]
           4    0.02%    0.00%  void <- [ptr,i32,ptr,i64,ptr]
           4    0.02%    0.00%  void <- [ptr,i64,i32,ptr]
           4    0.02%    0.00%  void <- [ptr,ptr,i8,ptr]
           4    0.02%    0.00%  void <- [ptr,ptr,ptr,i1,ptr]
           4    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr]
           4    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,ptr]
           3    0.01%    0.00%  i1 <- [ptr,ptr,i32,i32,i32,i32,i1,ptr]
           3    0.01%    0.00%  i32 <- [i16,ptr]
           3    0.01%    0.00%  i32 <- [i32,i32,i32,i32,i32,ptr,i32,i32,ptr]
           3    0.01%    0.00%  i32 <- [i32,ptr,i64,ptr,ptr]
           3    0.01%    0.00%  i32 <- [i32,ptr,ptr,ptr]
           3    0.01%    0.00%  i32 <- [i8,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i64,i64,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,i32,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,i64,ptr,ptr]
           3    0.01%    0.00%  i64 <- [i64,i64,i64,ptr]
           3    0.01%    0.00%  i64 <- [ptr,i64,i32,ptr,i32,ptr]
           3    0.01%    0.00%  i8 <- [i8,ptr]
           3    0.01%    0.00%  ptr <- [i32,ptr]
           3    0.01%    0.00%  ptr <- [i64,i32,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr]
           3    0.01%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr]
           3    0.01%    0.00%  void <- [ptr,i1,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,i64,ptr,i32,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  i1 <- [ptr,i64,ptr,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,i1,i1,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,i1,ptr,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  i32 <- [i16,ptr,ptr]
           2    0.01%    0.00%  i32 <- [i32,ptr,i32,i32,ptr]
           2    0.01%    0.00%  i32 <- [i8,i8,ptr]
           2    0.01%    0.00%  i32 <- [ptr,i8,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,i1,i1,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,i1,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,i64,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr]
           2    0.01%    0.00%  i64 <- [i32,i32,ptr]
           2    0.01%    0.00%  i64 <- [i64,ptr,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,i16,i1,i1,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,i64,i64,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,i64,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,i8,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i1,i1,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i1,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i64,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i1 <- [i16,ptr]
           1    0.00%    0.00%  i1 <- [i8,i8,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [i16,i16,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i16,i64,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i64,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i64,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i64,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i64,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,i64,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i8,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i64,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,i1,i1,ptr,i1,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i64 <- [i1,i32,ptr]
           1    0.00%    0.00%  i64 <- [i32,i64,i64,i64,ptr]
           1    0.00%    0.00%  i64 <- [i64,i64,i64,i64,i32,ptr]
           1    0.00%    0.00%  i64 <- [ptr,i32,ptr]
           1    0.00%    0.00%  i64 <- [ptr,i64,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i1,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i64,i32,i32,i32,i64,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [i32,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,ptr,i32,i1,i32,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i1,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i1,ptr,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,i64,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,i64,i64,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,ptr,i64,i32,ptr,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i1,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,i8,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,i8,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
```

#### icmp

```text
       count  opcode%   total%  types
       7,254   65.11%    2.46%  i1 <- [i32,i32]
       1,915   17.19%    0.65%  i1 <- [ptr,ptr]
       1,153   10.35%    0.39%  i1 <- [i8,i8]
         820    7.36%    0.28%  i1 <- [i64,i64]
```

#### ret

```text
       count  opcode%   total%  types
       5,382   56.06%    1.82%  void <- [-]
       2,016   21.00%    0.68%  void <- [i32]
       1,531   15.95%    0.52%  void <- [ptr]
         475    4.95%    0.16%  void <- [i1]
         156    1.62%    0.05%  void <- [i64]
          35    0.36%    0.01%  void <- [i8]
           6    0.06%    0.00%  void <- [i16]
```

#### invoke

```text
       count  opcode%   total%  types
       1,413   20.12%    0.48%  void <- [ptr,label,label,ptr]
         781   11.12%    0.26%  ptr <- [ptr,label,label,ptr]
         710   10.11%    0.24%  i32 <- [ptr,label,label,ptr]
         603    8.59%    0.20%  ptr <- [ptr,ptr,label,label,ptr]
         480    6.83%    0.16%  void <- [ptr,ptr,label,label,ptr]
         388    5.52%    0.13%  ptr <- [ptr,i32,label,label,ptr]
         319    4.54%    0.11%  i32 <- [ptr,ptr,label,label,ptr]
         244    3.47%    0.08%  i1 <- [ptr,label,label,ptr]
         171    2.43%    0.06%  void <- [ptr,ptr,ptr,label,label,ptr]
         143    2.04%    0.05%  void <- [ptr,i32,label,label,ptr]
         137    1.95%    0.05%  void <- [ptr,ptr,i32,label,label,ptr]
         130    1.85%    0.04%  i32 <- [ptr,i32,label,label,ptr]
         120    1.71%    0.04%  i32 <- [ptr,ptr,ptr,label,label,ptr]
         120    1.71%    0.04%  ptr <- [i64,label,label,ptr]
         113    1.61%    0.04%  i64 <- [ptr,label,label,ptr]
          93    1.32%    0.03%  i1 <- [ptr,ptr,label,label,ptr]
          63    0.90%    0.02%  ptr <- [ptr,i64,label,label,ptr]
          55    0.78%    0.02%  i32 <- [ptr,i64,label,label,ptr]
          55    0.78%    0.02%  void <- [label,label,ptr]
          53    0.75%    0.02%  i32 <- [ptr,i32,i32,ptr,label,label,ptr]
          34    0.48%    0.01%  i32 <- [ptr,i64,i32,ptr,label,label,ptr]
          34    0.48%    0.01%  void <- [ptr,i32,ptr,label,label,ptr]
          32    0.46%    0.01%  i32 <- [ptr,i32,ptr,label,label,ptr]
          32    0.46%    0.01%  void <- [ptr,i8,label,label,ptr]
          31    0.44%    0.01%  void <- [ptr,i64,label,label,ptr]
          29    0.41%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          29    0.41%    0.01%  ptr <- [ptr,i8,label,label,ptr]
          26    0.37%    0.01%  void <- [ptr,i1,label,label,ptr]
          23    0.33%    0.01%  i32 <- [ptr,i1,label,label,ptr]
          22    0.31%    0.01%  i1 <- [ptr,i32,label,label,ptr]
          21    0.30%    0.01%  i32 <- [ptr,ptr,i32,label,label,ptr]
          19    0.27%    0.01%  i1 <- [i32,label,label,ptr]
          19    0.27%    0.01%  void <- [ptr,ptr,i1,label,label,ptr]
          18    0.26%    0.01%  i32 <- [ptr,i32,i32,label,label,ptr]
          18    0.26%    0.01%  void <- [ptr,i32,i32,label,label,ptr]
          16    0.23%    0.01%  i32 <- [ptr,ptr,ptr,ptr,label,label,ptr]
          15    0.21%    0.01%  ptr <- [ptr,i1,label,label,ptr]
          14    0.20%    0.00%  i1 <- [ptr,ptr,i1,label,label,ptr]
          14    0.20%    0.00%  i32 <- [label,label,ptr]
          13    0.19%    0.00%  i32 <- [ptr,i32,ptr,i32,label,label,ptr]
          11    0.16%    0.00%  i1 <- [ptr,ptr,ptr,label,label,ptr]
          11    0.16%    0.00%  i32 <- [ptr,ptr,i32,ptr,label,label,ptr]
          11    0.16%    0.00%  i32 <- [ptr,ptr,i64,label,label,ptr]
          11    0.16%    0.00%  i32 <- [ptr,ptr,ptr,i32,label,label,ptr]
          11    0.16%    0.00%  void <- [ptr,ptr,ptr,ptr,label,label,ptr]
          10    0.14%    0.00%  i1 <- [ptr,i32,ptr,label,label,ptr]
          10    0.14%    0.00%  void <- [ptr,i32,ptr,ptr,label,label,ptr]
           9    0.13%    0.00%  i1 <- [i32,ptr,label,label,ptr]
           9    0.13%    0.00%  i8 <- [ptr,label,label,ptr]
           8    0.11%    0.00%  void <- [i32,ptr,label,label,ptr]
           7    0.10%    0.00%  i16 <- [ptr,label,label,ptr]
           7    0.10%    0.00%  i32 <- [ptr,ptr,i1,label,label,ptr]
           7    0.10%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           7    0.10%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           7    0.10%    0.00%  void <- [i32,i32,ptr,label,label,ptr]
           6    0.09%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,label,label,ptr]
           6    0.09%    0.00%  void <- [ptr,ptr,i64,label,label,ptr]
           5    0.07%    0.00%  i1 <- [ptr,ptr,i32,ptr,label,label,ptr]
           5    0.07%    0.00%  i1 <- [ptr,ptr,ptr,ptr,label,label,ptr]
           5    0.07%    0.00%  i32 <- [i32,label,label,ptr]
           5    0.07%    0.00%  i32 <- [i64,ptr,i1,label,label,ptr]
           5    0.07%    0.00%  i32 <- [ptr,[2 x i64],label,label,ptr]
           5    0.07%    0.00%  i32 <- [ptr,ptr,ptr,i1,ptr,ptr,ptr,label,label,ptr]
           5    0.07%    0.00%  i64 <- [ptr,i32,label,label,ptr]
           5    0.07%    0.00%  void <- [ptr,ptr,ptr,i32,label,label,ptr]
           4    0.06%    0.00%  i32 <- [ptr,i64,ptr,label,label,ptr]
           4    0.06%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,i32,ptr,label,label,ptr]
           4    0.06%    0.00%  i64 <- [label,label,ptr]
           4    0.06%    0.00%  i64 <- [ptr,i32,i32,label,label,ptr]
           4    0.06%    0.00%  void <- [i32,i32,ptr,ptr,label,label,ptr]
           4    0.06%    0.00%  void <- [i64,ptr,i32,label,label,ptr]
           4    0.06%    0.00%  void <- [ptr,ptr,i1,i32,i32,label,label,ptr]
           4    0.06%    0.00%  void <- [ptr,ptr,i1,i32,label,label,ptr]
           3    0.04%    0.00%  i1 <- [i8,i8,label,label,ptr]
           3    0.04%    0.00%  i1 <- [i8,label,label,ptr]
           3    0.04%    0.00%  i1 <- [label,label,ptr]
           3    0.04%    0.00%  i1 <- [ptr,i1,ptr,i1,label,label,ptr]
           3    0.04%    0.00%  i1 <- [ptr,i64,label,label,ptr]
           3    0.04%    0.00%  i1 <- [ptr,ptr,i32,label,label,ptr]
           3    0.04%    0.00%  i32 <- [i64,ptr,ptr,i1,label,label,ptr]
           3    0.04%    0.00%  i32 <- [ptr,i32,i1,i32,ptr,ptr,label,label,ptr]
           3    0.04%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,label,label,ptr]
           3    0.04%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,i1,ptr,ptr,ptr,label,label,ptr]
           3    0.04%    0.00%  i32 <- [ptr,ptr,i64,ptr,ptr,ptr,ptr,ptr,ptr,i1,i32,label,label,ptr]
           3    0.04%    0.00%  i64 <- [ptr,ptr,label,label,ptr]
           3    0.04%    0.00%  void <- [ptr,i1,i8,ptr,label,label,ptr]
           3    0.04%    0.00%  void <- [ptr,ptr,i32,i1,label,label,ptr]
           2    0.03%    0.00%  i1 <- [[2 x i64],i16,ptr,label,label,ptr]
           2    0.03%    0.00%  i1 <- [i64,ptr,label,label,ptr]
           2    0.03%    0.00%  i1 <- [ptr,i32,i32,ptr,label,label,ptr]
           2    0.03%    0.00%  i1 <- [ptr,ptr,i1,ptr,label,label,ptr]
           2    0.03%    0.00%  i1 <- [ptr,ptr,i64,label,label,ptr]
           2    0.03%    0.00%  i32 <- [i1,i32,label,label,ptr]
           2    0.03%    0.00%  i32 <- [i1,label,label,ptr]
           2    0.03%    0.00%  i32 <- [i32,i32,label,label,ptr]
           2    0.03%    0.00%  i32 <- [i32,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [i64,ptr,ptr,ptr,i1,i1,label,label,ptr]
           2    0.03%    0.00%  i32 <- [i8,i8,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,i1,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,i32,i32,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,i1,ptr,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i64,i64,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i64,i64,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i8,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i32,i1,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  i64 <- [i64,i64,i64,label,label,ptr]
           2    0.03%    0.00%  i8 <- [i8,label,label,ptr]
           2    0.03%    0.00%  i8 <- [ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  ptr <- [ptr,i64,i64,label,label,ptr]
           2    0.03%    0.00%  void <- [i64,ptr,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,i1,ptr,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,i16,i64,i1,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,i64,i32,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,ptr,i64,ptr,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,ptr,i8,label,label,ptr]
           2    0.03%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i1 <- [i16,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,i32,i32,i32,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,i32,i32,label,label,ptr]
           1    0.01%    0.00%  i1 <- [ptr,ptr,i32,i32,i32,i32,i1,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i32,i32,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i1,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i1,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i1,ptr,ptr,ptr,i1,i1,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i1,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,i1,i1,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i64,i64,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [i32,i1,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [i32,label,label,ptr]
           1    0.01%    0.00%  void <- [i32,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i1,i32,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i1,ptr,i1,i1,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i32,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i32,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,ptr,ptr,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,i8,i32,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,i64,ptr,i1,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i1,i1,i1,ptr,ptr,i64,label,label,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
```

#### zext

```text
       count  opcode%   total%  types
       2,482   42.41%    0.84%  i64 <- [i32]
       1,849   31.60%    0.63%  i32 <- [i8]
         611   10.44%    0.21%  i32 <- [i16]
         449    7.67%    0.15%  i8 <- [i1]
         212    3.62%    0.07%  i64 <- [i1]
         100    1.71%    0.03%  i32 <- [i1]
          84    1.44%    0.03%  i64 <- [i8]
          51    0.87%    0.02%  i16 <- [i8]
          14    0.24%    0.00%  i64 <- [i16]
```

#### extractvalue

```text
       count  opcode%   total%  types
       2,750   53.69%    0.93%  ptr <- [{ ptr, i32 }]
       2,222   43.38%    0.75%  i32 <- [{ ptr, i32 }]
          75    1.46%    0.03%  i1 <- [{ i64, i1 }]
          75    1.46%    0.03%  i64 <- [{ i64, i1 }]
```

#### add

```text
       count  opcode%   total%  types
       4,367   86.80%    1.48%  i32 <- [i32,i32]
         648   12.88%    0.22%  i64 <- [i64,i64]
          15    0.30%    0.01%  i8 <- [i8,i8]
           1    0.02%    0.00%  i16 <- [i16,i16]
```

#### landingpad

```text
       count  opcode%   total%  types
       1,860   67.64%    0.63%  { ptr, i32 } <- [-]
         563   20.47%    0.19%  { ptr, i32 } <- [ptr]
         315   11.45%    0.11%  { ptr, i32 } <- [ptr,ptr]
          11    0.40%    0.00%  { ptr, i32 } <- [ptr,ptr,ptr]
           1    0.04%    0.00%  { ptr, i32 } <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
```

#### sext

```text
       count  opcode%   total%  types
       2,174   97.80%    0.74%  i64 <- [i32]
          38    1.71%    0.01%  i32 <- [i16]
           6    0.27%    0.00%  i32 <- [i8]
           5    0.22%    0.00%  i64 <- [i16]
```

#### unreachable

```text
       count  opcode%   total%  types
       1,963  100.00%    0.66%  void <- [-]
```

#### sub

```text
       count  opcode%   total%  types
       1,472   79.18%    0.50%  i32 <- [i32,i32]
         387   20.82%    0.13%  i64 <- [i64,i64]
```

#### shl

```text
       count  opcode%   total%  types
         966   93.42%    0.33%  i32 <- [i32,i32]
          68    6.58%    0.02%  i64 <- [i64,i64]
```

#### trunc

```text
       count  opcode%   total%  types
         391   41.95%    0.13%  i8 <- [i32]
         321   34.44%    0.11%  i32 <- [i64]
         186   19.96%    0.06%  i16 <- [i32]
          16    1.72%    0.01%  i8 <- [i64]
          13    1.39%    0.00%  i16 <- [i64]
           5    0.54%    0.00%  i8 <- [i16]
```

#### or

```text
       count  opcode%   total%  types
         759   95.23%    0.26%  i32 <- [i32,i32]
          31    3.89%    0.01%  i64 <- [i64,i64]
           7    0.88%    0.00%  i1 <- [i1,i1]
```

#### and

```text
       count  opcode%   total%  types
         643   95.54%    0.22%  i32 <- [i32,i32]
          30    4.46%    0.01%  i64 <- [i64,i64]
```

#### lshr

```text
       count  opcode%   total%  types
         606   92.52%    0.21%  i32 <- [i32,i32]
          49    7.48%    0.02%  i64 <- [i64,i64]
```

#### phi

```text
       count  opcode%   total%  types
         176   34.58%    0.06%  i32 <- [i32,i32]
         164   32.22%    0.06%  i1 <- [i1,i1]
         110   21.61%    0.04%  ptr <- [ptr,ptr]
          38    7.47%    0.01%  i64 <- [i64,i64]
          13    2.55%    0.00%  i1 <- [i1,i1,i1]
           3    0.59%    0.00%  i1 <- [i1,i1,i1,i1]
           3    0.59%    0.00%  i8 <- [i8,i8]
           1    0.20%    0.00%  i1 <- [i1,i1,i1,i1,i1]
           1    0.20%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1]
```

#### xor

```text
       count  opcode%   total%  types
         413   87.87%    0.14%  i32 <- [i32,i32]
          50   10.64%    0.02%  i1 <- [i1,i1]
           7    1.49%    0.00%  i64 <- [i64,i64]
```

#### mul

```text
       count  opcode%   total%  types
         245   66.76%    0.08%  i32 <- [i32,i32]
         122   33.24%    0.04%  i64 <- [i64,i64]
```

#### switch

```text
       count  opcode%   total%  types
         109   37.85%    0.04%  void <- [i32,label,label]
          87   30.21%    0.03%  void <- [i32,label,label,label]
          45   15.62%    0.02%  void <- [i32,label,label,label,label]
          13    4.51%    0.00%  void <- [i32,label,label,label,label,label]
           9    3.12%    0.00%  void <- [i32,label,label,label,label,label,label]
           8    2.78%    0.00%  void <- [i32,label,label,label,label,label,label,label]
           5    1.74%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
           3    1.04%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label]
           2    0.69%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
           2    0.69%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.35%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
           1    0.35%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label]
           1    0.35%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.35%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.35%    0.00%  void <- [i64,label,label]
```

#### select

```text
       count  opcode%   total%  types
         192   68.82%    0.07%  i32 <- [i1,i32,i32]
          68   24.37%    0.02%  i64 <- [i1,i64,i64]
          12    4.30%    0.00%  i8 <- [i1,i8,i8]
           3    1.08%    0.00%  i1 <- [i1,i1,i1]
           3    1.08%    0.00%  ptr <- [i1,ptr,ptr]
           1    0.36%    0.00%  i16 <- [i1,i16,i16]
```

#### ptrtoint

```text
       count  opcode%   total%  types
         226  100.00%    0.08%  i64 <- [ptr]
```

#### sdiv

```text
       count  opcode%   total%  types
          72   58.54%    0.02%  i32 <- [i32,i32]
          51   41.46%    0.02%  i64 <- [i64,i64]
```

#### udiv

```text
       count  opcode%   total%  types
          63   61.17%    0.02%  i32 <- [i32,i32]
          40   38.83%    0.01%  i64 <- [i64,i64]
```

#### ashr

```text
       count  opcode%   total%  types
          96   96.00%    0.03%  i32 <- [i32,i32]
           4    4.00%    0.00%  i64 <- [i64,i64]
```

#### srem

```text
       count  opcode%   total%  types
          13   81.25%    0.00%  i32 <- [i32,i32]
           3   18.75%    0.00%  i64 <- [i64,i64]
```

#### urem

```text
       count  opcode%   total%  types
           8   72.73%    0.00%  i32 <- [i32,i32]
           3   27.27%    0.00%  i64 <- [i64,i64]
```

#### inttoptr

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  ptr <- [i64]
```

### Bullet

#### load

```text
       count  opcode%   total%  types
      34,775   54.24%   12.85%  ptr <- [ptr]
      14,364   22.40%    5.31%  float <- [ptr]
      12,758   19.90%    4.71%  i32 <- [ptr]
         900    1.40%    0.33%  i8 <- [ptr]
         597    0.93%    0.22%  %class.btVector3 <- [ptr]
         385    0.60%    0.14%  i16 <- [ptr]
         183    0.29%    0.07%  i64 <- [ptr]
          79    0.12%    0.03%  i1 <- [ptr]
          36    0.06%    0.01%  double <- [ptr]
          34    0.05%    0.01%  %class.btQuaternion <- [ptr]
           3    0.00%    0.00%  { i64, i64 } <- [ptr]
           2    0.00%    0.00%  [2 x i64] <- [ptr]
           1    0.00%    0.00%  %class.btVector4 <- [ptr]
```

#### store

```text
       count  opcode%   total%  types
      19,693   45.58%    7.28%  void <- [ptr,ptr]
      10,960   25.36%    4.05%  void <- [float,ptr]
       8,379   19.39%    3.10%  void <- [i32,ptr]
       2,566    5.94%    0.95%  void <- [[4 x float],ptr]
         934    2.16%    0.35%  void <- [i8,ptr]
         243    0.56%    0.09%  void <- [i1,ptr]
         220    0.51%    0.08%  void <- [i16,ptr]
         134    0.31%    0.05%  void <- [i64,ptr]
          73    0.17%    0.03%  void <- [%class.btQuadWord,ptr]
           4    0.01%    0.00%  void <- [[2 x i64],ptr]
           3    0.01%    0.00%  void <- [{ i64, i64 },ptr]
           1    0.00%    0.00%  void <- [%class.btVector3,ptr]
```

#### getelementptr

```text
       count  opcode%   total%  types
      27,771   65.08%   10.26%  ptr <- [ptr,i32,i32]
       8,849   20.74%    3.27%  ptr <- [ptr,i64,i64]
       6,015   14.10%    2.22%  ptr <- [ptr,i64]
          35    0.08%    0.01%  ptr <- [ptr,i32]
```

#### alloca

```text
       count  opcode%   total%  types
      35,155  100.00%   12.99%  ptr <- [i32]
```

#### call

```text
       count  opcode%   total%  types
       6,424   22.03%    2.37%  ptr <- [ptr,ptr]
       4,572   15.68%    1.69%  void <- [ptr,ptr]
       2,142    7.35%    0.79%  %class.btVector3 <- [ptr,ptr,ptr]
       1,809    6.20%    0.67%  void <- [ptr,ptr,i64,i1,ptr]
       1,747    5.99%    0.65%  ptr <- [ptr,i32,ptr]
       1,625    5.57%    0.60%  void <- [ptr,ptr,ptr,ptr,ptr]
       1,553    5.33%    0.57%  i32 <- [ptr,ptr]
       1,199    4.11%    0.44%  float <- [float,float,float,ptr]
       1,087    3.73%    0.40%  void <- [ptr,ptr,ptr]
       1,048    3.59%    0.39%  float <- [ptr,ptr,ptr]
         646    2.22%    0.24%  float <- [ptr,ptr]
         602    2.06%    0.22%  float <- [float,ptr]
         540    1.85%    0.20%  ptr <- [ptr,ptr,ptr]
         358    1.23%    0.13%  void <- [ptr,ptr,ptr,ptr]
         279    0.96%    0.10%  void <- [ptr,i32,i32,ptr]
         216    0.74%    0.08%  void <- [ptr,i32,ptr]
         169    0.58%    0.06%  void <- [ptr]
         162    0.56%    0.06%  %class.btVector3 <- [ptr,ptr]
         160    0.55%    0.06%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
         150    0.51%    0.06%  ptr <- [i64,i32,ptr]
         143    0.49%    0.05%  i1 <- [ptr,ptr]
         142    0.49%    0.05%  i32 <- [ptr,i32,ptr]
         132    0.45%    0.05%  void <- [ptr,i32,i32,ptr,ptr]
         123    0.42%    0.05%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
         121    0.42%    0.04%  void <- [ptr,i32,ptr,ptr]
         116    0.40%    0.04%  ptr <- [ptr,i32,ptr,ptr]
          82    0.28%    0.03%  void <- [ptr,float,ptr]
          77    0.26%    0.03%  %class.btVector3 <- [ptr,i32,ptr]
          74    0.25%    0.03%  void <- [ptr,ptr,ptr,float,ptr]
          72    0.25%    0.03%  float <- [ptr,i32,i32,i32,i32,ptr]
          72    0.25%    0.03%  ptr <- [i64,ptr]
          54    0.19%    0.02%  i1 <- [ptr,ptr,ptr]
          48    0.16%    0.02%  ptr <- [i64,ptr,ptr]
          41    0.14%    0.02%  void <- [ptr,ptr,i32,i32,ptr]
          38    0.13%    0.01%  i1 <- [ptr,ptr,ptr,ptr]
          38    0.13%    0.01%  void <- [ptr,i8,i64,i1,ptr]
          37    0.13%    0.01%  void <- [ptr,ptr,ptr,i32,ptr]
          35    0.12%    0.01%  %class.btQuaternion <- [ptr,ptr]
          33    0.11%    0.01%  i32 <- [ptr,ptr,ptr]
          31    0.11%    0.01%  ptr <- [ptr,ptr,ptr,ptr]
          30    0.10%    0.01%  float <- [float,float,ptr]
          30    0.10%    0.01%  ptr <- [ptr,i64,ptr]
          29    0.10%    0.01%  %class.btQuaternion <- [ptr,ptr,ptr]
          28    0.10%    0.01%  i1 <- [i32,ptr]
          28    0.10%    0.01%  i1 <- [ptr,i32,ptr]
          28    0.10%    0.01%  void <- [ptr,ptr,float,ptr]
          27    0.09%    0.01%  float <- [ptr,ptr,ptr,ptr]
          27    0.09%    0.01%  void <- [ptr,i64,i32,i32,ptr]
          25    0.09%    0.01%  void <- [ptr,float,float,float,ptr]
          24    0.08%    0.01%  i16 <- [i16,ptr]
          23    0.08%    0.01%  ptr <- [ptr,ptr,ptr,ptr,ptr]
          21    0.07%    0.01%  %class.btVector3 <- [ptr,ptr,ptr,ptr]
          21    0.07%    0.01%  ptr <- [ptr,float,ptr,ptr,ptr]
          21    0.07%    0.01%  ptr <- [ptr,i16,ptr]
          21    0.07%    0.01%  void <- [ptr,i32,i32,ptr,i1,ptr]
          20    0.07%    0.01%  void <- [ptr,float,ptr,ptr]
          19    0.07%    0.01%  i32 <- [i32,ptr]
          19    0.07%    0.01%  void <- [ptr,i32,ptr,ptr,ptr]
          18    0.06%    0.01%  i32 <- [ptr,ptr,ptr,ptr]
          18    0.06%    0.01%  void <- [ptr,ptr,ptr,ptr,i32,i32,i1,ptr]
          16    0.05%    0.01%  void <- [ptr,ptr,float,float,float,ptr]
          16    0.05%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          15    0.05%    0.01%  void <- [ptr,i32,float,ptr]
          14    0.05%    0.01%  float <- [ptr,i32,ptr]
          14    0.05%    0.01%  void <- [ptr,float,float,float,float,ptr]
          14    0.05%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,float,ptr]
          13    0.04%    0.00%  void <- [ptr,ptr,i1,ptr]
          13    0.04%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,ptr]
          12    0.04%    0.00%  float <- [i32,i32,i32,i32,i32,ptr]
          12    0.04%    0.00%  void <- [ptr,i32,i16,ptr,i1,ptr]
          12    0.04%    0.00%  { i64, i1 } <- [i64,i64,ptr]
          11    0.04%    0.00%  void <- [ptr,i64,ptr]
          11    0.04%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,float,ptr,float,ptr]
          10    0.03%    0.00%  ptr <- [ptr,i32,i32,ptr]
          10    0.03%    0.00%  void <- [ptr,float,float,ptr]
          10    0.03%    0.00%  void <- [ptr,ptr,float,float,ptr,ptr,ptr]
          10    0.03%    0.00%  void <- [ptr,ptr,i32,ptr]
           9    0.03%    0.00%  i32 <- [ptr,i32,i32,ptr]
           9    0.03%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr]
           9    0.03%    0.00%  void <- [ptr,float,ptr,ptr,ptr]
           9    0.03%    0.00%  void <- [ptr,float,ptr,ptr,ptr,ptr]
           9    0.03%    0.00%  void <- [ptr,i32,ptr,i32,ptr]
           9    0.03%    0.00%  void <- [ptr,ptr,ptr,ptr,i1,ptr]
           8    0.03%    0.00%  i1 <- [ptr,ptr,ptr,i32,i32,ptr]
           8    0.03%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           7    0.02%    0.00%  i16 <- [ptr,ptr]
           7    0.02%    0.00%  i1 <- [float,ptr]
           7    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr]
           7    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           7    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr]
           7    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           7    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           6    0.02%    0.00%  float <- [ptr,ptr,i1,ptr]
           6    0.02%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.02%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr]
           6    0.02%    0.00%  i32 <- [ptr]
           6    0.02%    0.00%  ptr <- [ptr]
           6    0.02%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,float,ptr]
           6    0.02%    0.00%  void <- [ptr,float,float,float,float,float,float,ptr]
           6    0.02%    0.00%  void <- [ptr,i1,ptr]
           6    0.02%    0.00%  void <- [ptr,i32,i32,i32,ptr]
           6    0.02%    0.00%  void <- [ptr,i32,i32,i32,ptr,ptr]
           6    0.02%    0.00%  void <- [ptr,ptr,float,ptr,ptr]
           6    0.02%    0.00%  void <- [ptr,ptr,float,ptr,ptr,ptr]
           5    0.02%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  i64 <- [ptr,ptr]
           5    0.02%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i1,ptr]
           5    0.02%    0.00%  void <- [ptr,float,float,float,float,float,ptr]
           5    0.02%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  void <- [ptr,ptr,i16,i16,ptr]
           5    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,i32,i32,ptr]
           5    0.02%    0.00%  void <- [ptr,ptr,ptr,float,ptr,ptr]
           5    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,float,float,float,float,ptr,i1,float,ptr]
           4    0.01%    0.00%  %class.btVector3 <- [ptr,ptr,float,ptr]
           4    0.01%    0.00%  float <- [ptr,float,float,float,float,float,ptr]
           4    0.01%    0.00%  float <- [ptr,ptr,i32,ptr]
           4    0.01%    0.00%  float <- [ptr,ptr,i32,ptr,ptr,ptr]
           4    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           4    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr]
           4    0.01%    0.00%  ptr <- [i32,ptr]
           4    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,i16,i16,ptr,ptr,ptr]
           4    0.01%    0.00%  void <- [ptr,float,i32,ptr]
           4    0.01%    0.00%  void <- [ptr,i16,ptr]
           4    0.01%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
           4    0.01%    0.00%  void <- [ptr,i64,i64,ptr]
           4    0.01%    0.00%  void <- [ptr,ptr,float,ptr,i32,ptr]
           4    0.01%    0.00%  void <- [ptr,ptr,float,ptr,ptr,ptr,ptr]
           4    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
           3    0.01%    0.00%  %class.btVector3 <- [ptr,ptr,i32,ptr]
           3    0.01%    0.00%  %class.btVector3 <- [ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  [2 x i64] <- [float,ptr]
           3    0.01%    0.00%  float <- [ptr]
           3    0.01%    0.00%  float <- [ptr,ptr,i32,ptr,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  i1 <- [ptr,i32,ptr,ptr,i32,ptr,ptr]
           3    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,float,ptr]
           3    0.01%    0.00%  i32 <- [float,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,double,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,i1,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i32,i32,i32,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i64,i64,ptr]
           3    0.01%    0.00%  void <- [ptr,i32,i1,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i16,i16,ptr,ptr]
           2    0.01%    0.00%  %class.btVector3 <- [ptr,float,float,ptr]
           2    0.01%    0.00%  %class.btVector3 <- [ptr,float,ptr]
           2    0.01%    0.00%  %class.btVector3 <- [ptr,ptr,i32,ptr,ptr]
           2    0.01%    0.00%  float <- [float,float,float,ptr,ptr]
           2    0.01%    0.00%  float <- [ptr,ptr,float,float,ptr]
           2    0.01%    0.00%  float <- [ptr,ptr,float,i32,i32,ptr]
           2    0.01%    0.00%  float <- [ptr,ptr,float,ptr]
           2    0.01%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,float,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,float,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,i32,i32,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,ptr,i1,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,ptr,i32,i32,i1,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,float,float,ptr]
           2    0.01%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,ptr]
           2    0.01%    0.00%  i32 <- [i32,i32,i32,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,float,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,i32,ptr]
           2    0.01%    0.00%  i64 <- [ptr,i64,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,float,float,float,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,float,ptr,ptr,float,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,i32,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i32,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,float,float,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,float,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  %class.btVector4 <- [ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,float,float,ptr]
           1    0.00%    0.00%  float <- [ptr,float,float,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,float,ptr,float,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,float,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,i32,i32,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,float,float,float,float,i32,i32,ptr,ptr,float,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,float,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,float,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,float,ptr,ptr,ptr]
           1    0.00%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i16 <- [ptr,ptr,ptr,ptr,i16,i16,ptr,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i32,i32,float,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i32,i1,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i32,i32,ptr,i32,i32,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,float,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,float,ptr,ptr,ptr,float,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,float,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,float,i32,float,ptr]
           1    0.00%    0.00%  i32 <- [ptr,float,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,float,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,double,double,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,double,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i16,i16,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i32,i1,ptr]
           1    0.00%    0.00%  void <- [i32,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,i32,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,float,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i16,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,float,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,float,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,float,ptr,i32,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i1,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i16,i16,i16,ptr,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,ptr,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,float,float,float,float,ptr,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr,ptr,float,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,float,float,ptr]
```

#### br

```text
       count  opcode%   total%  types
      10,141   64.54%    3.75%  void <- [label]
       5,571   35.46%    2.06%  void <- [i1,label,label]
```

#### ret

```text
       count  opcode%   total%  types
       4,844   53.51%    1.79%  void <- [-]
       1,895   20.93%    0.70%  void <- [ptr]
         716    7.91%    0.26%  void <- [float]
         686    7.58%    0.25%  void <- [i32]
         597    6.60%    0.22%  void <- [%class.btVector3]
         265    2.93%    0.10%  void <- [i1]
          34    0.38%    0.01%  void <- [%class.btQuaternion]
           7    0.08%    0.00%  void <- [i64]
           5    0.06%    0.00%  void <- [i16]
           2    0.02%    0.00%  void <- [[2 x i64]]
           1    0.01%    0.00%  void <- [%class.btVector4]
```

#### extractvalue

```text
       count  opcode%   total%  types
       2,566   52.93%    0.95%  [4 x float] <- [%class.btVector3]
       1,294   26.69%    0.48%  ptr <- [{ ptr, i32 }]
         886   18.28%    0.33%  i32 <- [{ ptr, i32 }]
          73    1.51%    0.03%  %class.btQuadWord <- [%class.btQuaternion]
          12    0.25%    0.00%  i1 <- [{ i64, i1 }]
          12    0.25%    0.00%  i64 <- [{ i64, i1 }]
           4    0.08%    0.00%  i64 <- [{ i64, i64 }]
           1    0.02%    0.00%  %class.btVector3 <- [%class.btVector4]
```

#### icmp

```text
       count  opcode%   total%  types
       2,640   60.32%    0.98%  i1 <- [i32,i32]
         952   21.75%    0.35%  i1 <- [ptr,ptr]
         738   16.86%    0.27%  i1 <- [i8,i8]
          32    0.73%    0.01%  i1 <- [i64,i64]
          15    0.34%    0.01%  i1 <- [i16,i16]
```

#### invoke

```text
       count  opcode%   total%  types
       1,706   40.28%    0.63%  void <- [ptr,label,label,ptr]
         461   10.89%    0.17%  ptr <- [ptr,i32,label,label,ptr]
         387    9.14%    0.14%  ptr <- [ptr,label,label,ptr]
         255    6.02%    0.09%  void <- [ptr,ptr,label,label,ptr]
         237    5.60%    0.09%  i32 <- [ptr,label,label,ptr]
         185    4.37%    0.07%  void <- [ptr,ptr,ptr,ptr,label,label,ptr]
         114    2.69%    0.04%  %class.btVector3 <- [ptr,ptr,label,label,ptr]
          75    1.77%    0.03%  void <- [ptr,ptr,ptr,label,label,ptr]
          73    1.72%    0.03%  ptr <- [ptr,ptr,label,label,ptr]
          68    1.61%    0.03%  void <- [ptr,i32,ptr,label,label,ptr]
          64    1.51%    0.02%  float <- [ptr,label,label,ptr]
          52    1.23%    0.02%  void <- [ptr,float,label,label,ptr]
          46    1.09%    0.02%  ptr <- [i64,i32,label,label,ptr]
          43    1.02%    0.02%  i1 <- [ptr,label,label,ptr]
          39    0.92%    0.01%  void <- [ptr,i32,label,label,ptr]
          31    0.73%    0.01%  float <- [ptr,ptr,label,label,ptr]
          22    0.52%    0.01%  %class.btVector3 <- [ptr,label,label,ptr]
          19    0.45%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          15    0.35%    0.01%  i32 <- [ptr,ptr,label,label,ptr]
          15    0.35%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          13    0.31%    0.00%  ptr <- [label,label,ptr]
          13    0.31%    0.00%  void <- [ptr,float,float,label,label,ptr]
          12    0.28%    0.00%  ptr <- [ptr,ptr,ptr,label,label,ptr]
          12    0.28%    0.00%  void <- [ptr,ptr,ptr,ptr,i1,label,label,ptr]
          11    0.26%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
          11    0.26%    0.00%  void <- [ptr,i32,i32,ptr,i1,label,label,ptr]
          11    0.26%    0.00%  void <- [ptr,ptr,i32,label,label,ptr]
          10    0.24%    0.00%  ptr <- [ptr,i32,i32,label,label,ptr]
           9    0.21%    0.00%  ptr <- [ptr,i64,label,label,ptr]
           9    0.21%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,float,label,label,ptr]
           8    0.19%    0.00%  float <- [float,label,label,ptr]
           8    0.19%    0.00%  void <- [ptr,i32,i32,label,label,ptr]
           8    0.19%    0.00%  void <- [ptr,ptr,ptr,float,label,label,ptr]
           8    0.19%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           7    0.17%    0.00%  void <- [ptr,ptr,float,label,label,ptr]
           6    0.14%    0.00%  %class.btQuaternion <- [ptr,ptr,label,label,ptr]
           6    0.14%    0.00%  i1 <- [ptr,ptr,ptr,label,label,ptr]
           6    0.14%    0.00%  ptr <- [i64,label,label,ptr]
           6    0.14%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,label,label,ptr]
           6    0.14%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,label,label,ptr]
           5    0.12%    0.00%  %class.btVector3 <- [ptr,i32,label,label,ptr]
           5    0.12%    0.00%  i1 <- [ptr,ptr,label,label,ptr]
           5    0.12%    0.00%  i32 <- [ptr,i32,label,label,ptr]
           5    0.12%    0.00%  i32 <- [ptr,ptr,ptr,label,label,ptr]
           5    0.12%    0.00%  void <- [ptr,ptr,i32,i32,label,label,ptr]
           4    0.09%    0.00%  ptr <- [ptr,i32,i32,i32,label,label,ptr]
           4    0.09%    0.00%  ptr <- [ptr,ptr,i32,label,label,ptr]
           4    0.09%    0.00%  ptr <- [ptr,ptr,ptr,ptr,label,label,ptr]
           4    0.09%    0.00%  void <- [ptr,i32,i32,i32,label,label,ptr]
           4    0.09%    0.00%  void <- [ptr,i64,label,label,ptr]
           3    0.07%    0.00%  %class.btQuaternion <- [ptr,label,label,ptr]
           3    0.07%    0.00%  %class.btVector3 <- [ptr,ptr,float,label,label,ptr]
           3    0.07%    0.00%  i1 <- [ptr,i32,label,label,ptr]
           3    0.07%    0.00%  ptr <- [i64,ptr,label,label,ptr]
           3    0.07%    0.00%  void <- [ptr,float,ptr,label,label,ptr]
           2    0.05%    0.00%  %class.btVector3 <- [ptr,ptr,i32,label,label,ptr]
           2    0.05%    0.00%  %class.btVector3 <- [ptr,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  float <- [ptr,ptr,i1,label,label,ptr]
           2    0.05%    0.00%  float <- [ptr,ptr,i32,ptr,i32,ptr,i32,ptr,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  i1 <- [ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,float,float,label,label,ptr]
           2    0.05%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  i32 <- [ptr,i32,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  i32 <- [ptr,ptr,ptr,float,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,float,ptr,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,i1,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,i16,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,i32,float,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,i32,i1,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,i32,i32,i32,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,i32,i32,ptr,float,float,float,i32,i32,i1,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,float,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,float,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,i1,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,i32,ptr,i32,i32,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,float,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,i32,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,float,ptr,ptr,ptr,label,label,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.02%    0.00%  [2 x i64] <- [ptr,ptr,i32,ptr,label,label,ptr]
           1    0.02%    0.00%  float <- [label,label,ptr]
           1    0.02%    0.00%  float <- [ptr,i32,label,label,ptr]
           1    0.02%    0.00%  float <- [ptr,ptr,float,label,label,ptr]
           1    0.02%    0.00%  float <- [ptr,ptr,ptr,float,i32,i32,label,label,ptr]
           1    0.02%    0.00%  float <- [ptr,ptr,ptr,float,i32,label,label,ptr]
           1    0.02%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           1    0.02%    0.00%  i1 <- [float,label,label,ptr]
           1    0.02%    0.00%  i1 <- [ptr,i32,ptr,i32,ptr,ptr,float,ptr,label,label,ptr]
           1    0.02%    0.00%  i1 <- [ptr,i32,ptr,ptr,i32,label,label,ptr]
           1    0.02%    0.00%  i1 <- [ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.02%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,label,label,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,label,label,ptr]
           1    0.02%    0.00%  ptr <- [ptr,float,label,label,ptr]
           1    0.02%    0.00%  void <- [label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,float,i1,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,i32,i32,ptr,i32,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,i32,i64,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,float,float,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,float,i32,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i1,i1,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i1,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr,i32,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,float,i32,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i16,ptr,i1,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,float,float,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,i32,float,float,ptr,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,i16,i16,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,i16,i16,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,float,ptr,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,i16,i16,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i1,ptr,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,float,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i1,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,label,label,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,float,label,label,ptr]
```

#### sext

```text
       count  opcode%   total%  types
       2,827   98.50%    1.04%  i64 <- [i32]
          32    1.11%    0.01%  i32 <- [i16]
          11    0.38%    0.00%  i32 <- [i8]
```

#### fmul

```text
       count  opcode%   total%  types
       2,287   99.52%    0.84%  float <- [float,float]
          11    0.48%    0.00%  double <- [double,double]
```

#### add

```text
       count  opcode%   total%  types
       2,002   97.80%    0.74%  i32 <- [i32,i32]
          27    1.32%    0.01%  i64 <- [i64,i64]
          18    0.88%    0.01%  i16 <- [i16,i16]
```

#### fcmp

```text
       count  opcode%   total%  types
       1,281   96.61%    0.47%  i1 <- [float,float]
          45    3.39%    0.02%  i1 <- [double,double]
```

#### landingpad

```text
       count  opcode%   total%  types
         886   68.47%    0.33%  { ptr, i32 } <- [-]
         408   31.53%    0.15%  { ptr, i32 } <- [ptr]
```

#### unreachable

```text
       count  opcode%   total%  types
       1,178  100.00%    0.44%  void <- [-]
```

#### fadd

```text
       count  opcode%   total%  types
         976   99.90%    0.36%  float <- [float,float]
           1    0.10%    0.00%  double <- [double,double]
```

#### zext

```text
       count  opcode%   total%  types
         270   29.48%    0.10%  i8 <- [i1]
         240   26.20%    0.09%  i64 <- [i32]
         145   15.83%    0.05%  i32 <- [i16]
          85    9.28%    0.03%  i64 <- [i1]
          74    8.08%    0.03%  i32 <- [i1]
          48    5.24%    0.02%  i64 <- [i8]
          27    2.95%    0.01%  i64 <- [i16]
          20    2.18%    0.01%  i16 <- [i8]
           7    0.76%    0.00%  i32 <- [i8]
```

#### fsub

```text
       count  opcode%   total%  types
         817   99.88%    0.30%  float <- [float,float]
           1    0.12%    0.00%  double <- [double,double]
```

#### fneg

```text
       count  opcode%   total%  types
         806  100.00%    0.30%  float <- [float]
```

#### phi

```text
       count  opcode%   total%  types
         373   47.10%    0.14%  ptr <- [ptr,ptr]
         154   19.44%    0.06%  float <- [float,float]
         148   18.69%    0.05%  i32 <- [i32,i32]
          82   10.35%    0.03%  i1 <- [i1,i1]
          13    1.64%    0.00%  i1 <- [i1,i1,i1]
           9    1.14%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1]
           6    0.76%    0.00%  i16 <- [i16,i16]
           5    0.63%    0.00%  i1 <- [i1,i1,i1,i1]
           2    0.25%    0.00%  i64 <- [i64,i64]
```

#### fdiv

```text
       count  opcode%   total%  types
         505   99.02%    0.19%  float <- [float,float]
           5    0.98%    0.00%  double <- [double,double]
```

#### mul

```text
       count  opcode%   total%  types
         305   66.45%    0.11%  i32 <- [i32,i32]
         154   33.55%    0.06%  i64 <- [i64,i64]
```

#### sub

```text
       count  opcode%   total%  types
         278   80.12%    0.10%  i32 <- [i32,i32]
          69   19.88%    0.03%  i64 <- [i64,i64]
```

#### and

```text
       count  opcode%   total%  types
         205   59.42%    0.08%  i32 <- [i32,i32]
         132   38.26%    0.05%  i8 <- [i8,i8]
           8    2.32%    0.00%  i64 <- [i64,i64]
```

#### sitofp

```text
       count  opcode%   total%  types
         144   99.31%    0.05%  float <- [i32]
           1    0.69%    0.00%  double <- [i32]
```

#### trunc

```text
       count  opcode%   total%  types
          46   37.10%    0.02%  i32 <- [i64]
          39   31.45%    0.01%  i16 <- [i32]
          23   18.55%    0.01%  i8 <- [i64]
          12    9.68%    0.00%  i8 <- [i16]
           4    3.23%    0.00%  i8 <- [i32]
```

#### or

```text
       count  opcode%   total%  types
          71   62.83%    0.03%  i8 <- [i8,i8]
          42   37.17%    0.02%  i32 <- [i32,i32]
```

#### ptrtoint

```text
       count  opcode%   total%  types
         106  100.00%    0.04%  i64 <- [ptr]
```

#### select

```text
       count  opcode%   total%  types
          71   73.20%    0.03%  i32 <- [i1,i32,i32]
          12   12.37%    0.00%  i64 <- [i1,i64,i64]
          11   11.34%    0.00%  float <- [i1,float,float]
           2    2.06%    0.00%  i16 <- [i1,i16,i16]
           1    1.03%    0.00%  i1 <- [i1,i1,i1]
```

#### sdiv

```text
       count  opcode%   total%  types
          45   54.22%    0.02%  i64 <- [i64,i64]
          38   45.78%    0.01%  i32 <- [i32,i32]
```

#### fpext

```text
       count  opcode%   total%  types
          70  100.00%    0.03%  double <- [float]
```

#### srem

```text
       count  opcode%   total%  types
          69  100.00%    0.03%  i32 <- [i32,i32]
```

#### shl

```text
       count  opcode%   total%  types
          45   69.23%    0.02%  i32 <- [i32,i32]
          20   30.77%    0.01%  i8 <- [i8,i8]
```

#### switch

```text
       count  opcode%   total%  types
          18   35.29%    0.01%  void <- [i32,label,label,label]
          10   19.61%    0.00%  void <- [i32,label,label,label,label]
           6   11.76%    0.00%  void <- [i32,label,label,label,label,label,label,label]
           5    9.80%    0.00%  void <- [i32,label,label,label,label,label,label]
           4    7.84%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
           3    5.88%    0.00%  void <- [i32,label,label]
           2    3.92%    0.00%  void <- [i32,label,label,label,label,label]
           2    3.92%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.96%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
```

#### fptrunc

```text
       count  opcode%   total%  types
          42  100.00%    0.02%  float <- [double]
```

#### lshr

```text
       count  opcode%   total%  types
          20   51.28%    0.01%  i32 <- [i32,i32]
          14   35.90%    0.01%  i8 <- [i8,i8]
           5   12.82%    0.00%  i64 <- [i64,i64]
```

#### xor

```text
       count  opcode%   total%  types
          18   51.43%    0.01%  i32 <- [i32,i32]
          12   34.29%    0.00%  i1 <- [i1,i1]
           5   14.29%    0.00%  i64 <- [i64,i64]
```

#### ashr

```text
       count  opcode%   total%  types
          17   56.67%    0.01%  i32 <- [i32,i32]
          11   36.67%    0.00%  i8 <- [i8,i8]
           2    6.67%    0.00%  i64 <- [i64,i64]
```

#### fptoui

```text
       count  opcode%   total%  types
          24   88.89%    0.01%  i16 <- [float]
           3   11.11%    0.00%  i32 <- [float]
```

#### uitofp

```text
       count  opcode%   total%  types
          12   46.15%    0.00%  float <- [i16]
          12   46.15%    0.00%  float <- [i32]
           2    7.69%    0.00%  float <- [i64]
```

#### fptosi

```text
       count  opcode%   total%  types
          14   87.50%    0.01%  i32 <- [float]
           2   12.50%    0.00%  i32 <- [double]
```

#### inttoptr

```text
       count  opcode%   total%  types
          10  100.00%    0.00%  ptr <- [i64]
```

#### udiv

```text
       count  opcode%   total%  types
           6   75.00%    0.00%  i32 <- [i32,i32]
           2   25.00%    0.00%  i64 <- [i64,i64]
```

#### urem

```text
       count  opcode%   total%  types
           4   80.00%    0.00%  i64 <- [i64,i64]
           1   20.00%    0.00%  i32 <- [i32,i32]
```

### ClamAV

#### load

```text
       count  opcode%   total%  types
      28,814   51.75%   16.54%  ptr <- [ptr]
      18,306   32.88%   10.51%  i32 <- [ptr]
       3,620    6.50%    2.08%  i64 <- [ptr]
       2,944    5.29%    1.69%  i8 <- [ptr]
       1,983    3.56%    1.14%  i16 <- [ptr]
           5    0.01%    0.00%  double <- [ptr]
           4    0.01%    0.00%  i1 <- [ptr]
```

#### br

```text
       count  opcode%   total%  types
      13,775   55.92%    7.91%  void <- [label]
      10,860   44.08%    6.23%  void <- [i1,label,label]
```

#### getelementptr

```text
       count  opcode%   total%  types
      14,850   66.60%    8.52%  ptr <- [ptr,i32,i32]
       4,734   21.23%    2.72%  ptr <- [ptr,i64]
       2,048    9.19%    1.18%  ptr <- [ptr,i64,i64]
         664    2.98%    0.38%  ptr <- [ptr,i32]
```

#### store

```text
       count  opcode%   total%  types
      10,579   51.19%    6.07%  void <- [i32,ptr]
       6,198   29.99%    3.56%  void <- [ptr,ptr]
       1,729    8.37%    0.99%  void <- [i64,ptr]
       1,358    6.57%    0.78%  void <- [i8,ptr]
         779    3.77%    0.45%  void <- [i16,ptr]
          22    0.11%    0.01%  void <- [i1,ptr]
           2    0.01%    0.00%  void <- [double,ptr]
```

#### icmp

```text
       count  opcode%   total%  types
       7,029   63.65%    4.03%  i1 <- [i32,i32]
       2,745   24.86%    1.58%  i1 <- [ptr,ptr]
         909    8.23%    0.52%  i1 <- [i64,i64]
         293    2.65%    0.17%  i1 <- [i8,i8]
          67    0.61%    0.04%  i1 <- [i16,i16]
```

#### call

```text
       count  opcode%   total%  types
       2,852   27.92%    1.64%  void <- [ptr,ptr]
         965    9.45%    0.55%  i32 <- [ptr,ptr]
         583    5.71%    0.33%  i32 <- [ptr,ptr,ptr]
         482    4.72%    0.28%  void <- [ptr,i32,ptr]
         392    3.84%    0.22%  void <- [ptr,ptr,ptr]
         300    2.94%    0.17%  i32 <- [i32,ptr]
         286    2.80%    0.16%  ptr <- [ptr,ptr]
         242    2.37%    0.14%  i64 <- [ptr,ptr]
         229    2.24%    0.13%  i32 <- [i32,ptr,i32,ptr]
         215    2.10%    0.12%  ptr <- [ptr]
         213    2.09%    0.12%  void <- [ptr,ptr,i64,i1,ptr]
         209    2.05%    0.12%  ptr <- [i64,ptr]
         205    2.01%    0.12%  i32 <- [ptr,i32,ptr]
         180    1.76%    0.10%  i64 <- [i32,i64,i32,ptr]
         177    1.73%    0.10%  i32 <- [ptr,ptr,i64,ptr]
         171    1.67%    0.10%  ptr <- [ptr,ptr,ptr]
         103    1.01%    0.06%  i32 <- [i32,ptr,ptr]
          99    0.97%    0.06%  i32 <- [ptr,ptr,ptr,i32,ptr]
          94    0.92%    0.05%  ptr <- [i64,i64,ptr]
          79    0.77%    0.05%  ptr <- [ptr,i32,ptr]
          78    0.76%    0.04%  void <- [ptr,ptr,ptr,ptr]
          77    0.75%    0.04%  void <- [ptr,ptr,i8,ptr]
          71    0.70%    0.04%  i32 <- [ptr,ptr,i32,ptr]
          61    0.60%    0.04%  i32 <- [ptr,ptr,ptr,ptr]
          60    0.59%    0.03%  void <- [ptr,i8,i64,i1,ptr]
          58    0.57%    0.03%  i32 <- [ptr,i64,ptr]
          56    0.55%    0.03%  void <- [ptr,i64,i64,ptr]
          55    0.54%    0.03%  ptr <- [ptr,i32,ptr,ptr]
          54    0.53%    0.03%  ptr <- [ptr,i64,ptr]
          54    0.53%    0.03%  void <- [ptr,ptr,i32,ptr]
          51    0.50%    0.03%  void <- [ptr,i32,i32,ptr]
          50    0.49%    0.03%  void <- [ptr,i64,ptr]
          45    0.44%    0.03%  i32 <- [ptr,i32,i32,ptr]
          41    0.40%    0.02%  ptr <- [i32,ptr]
          40    0.39%    0.02%  ptr <- [ptr,ptr,i64,ptr]
          37    0.36%    0.02%  ptr <- [ptr,i32,i32,ptr]
          34    0.33%    0.02%  void <- [ptr,i32,ptr,ptr]
          33    0.32%    0.02%  i64 <- [i64,ptr,i32,ptr]
          32    0.31%    0.02%  ptr <- [ptr,ptr,ptr,i64,i64,ptr]
          29    0.28%    0.02%  i64 <- [i32,ptr,i64,ptr]
          28    0.27%    0.02%  i32 <- [ptr,i64,ptr,ptr,ptr]
          27    0.26%    0.02%  i64 <- [ptr,i64,i64,ptr,ptr]
          25    0.24%    0.01%  i32 <- [i32,i8,ptr]
          25    0.24%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr]
          24    0.23%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
          24    0.23%    0.01%  ptr <- [ptr,ptr,ptr,i64,i64,i64,i32,ptr]
          23    0.23%    0.01%  ptr <- [ptr,ptr,i32,ptr]
          23    0.23%    0.01%  void <- [i32,ptr]
          22    0.22%    0.01%  i32 <- [i32,i32,ptr]
          22    0.22%    0.01%  void <- [ptr,i32,i64,ptr]
          21    0.21%    0.01%  i16 <- [i16,i32,ptr]
          21    0.21%    0.01%  i32 <- [ptr]
          18    0.18%    0.01%  void <- [ptr,ptr,ptr,i32,ptr]
          17    0.17%    0.01%  void <- [ptr,i32,i32,i32,ptr]
          17    0.17%    0.01%  void <- [ptr,ptr,i64,i32,ptr]
          16    0.16%    0.01%  ptr <- [i32,ptr,ptr]
          15    0.15%    0.01%  i32 <- [ptr,ptr,i32,ptr,ptr]
          14    0.14%    0.01%  i32 <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr]
          13    0.13%    0.01%  i32 <- [ptr,i32,ptr,ptr]
          13    0.13%    0.01%  i64 <- [ptr,ptr,i64,ptr]
          13    0.13%    0.01%  i64 <- [ptr,ptr,ptr]
          13    0.13%    0.01%  i8 <- [i8,ptr]
          12    0.12%    0.01%  i16 <- [i16,i8,ptr]
          12    0.12%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
          12    0.12%    0.01%  void <- [ptr,ptr,i64,ptr]
          11    0.11%    0.01%  i32 <- [i8,ptr,ptr,ptr,ptr,ptr,i32,ptr]
          11    0.11%    0.01%  i32 <- [ptr,ptr,ptr,i32,i16,ptr]
          11    0.11%    0.01%  i64 <- [i32,ptr,ptr]
          11    0.11%    0.01%  i8 <- [ptr,ptr]
          11    0.11%    0.01%  void <- [ptr,i64,i64,i64,ptr]
          11    0.11%    0.01%  void <- [ptr,ptr,i32,i32,ptr]
          10    0.10%    0.01%  i32 <- [ptr,i32,i8,ptr]
          10    0.10%    0.01%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr]
          10    0.10%    0.01%  i32 <- [ptr,ptr,i64,ptr,i32,ptr]
          10    0.10%    0.01%  ptr <- [ptr,i32,ptr,i32,ptr]
          10    0.10%    0.01%  void <- [i32,ptr,ptr,i32,ptr,i32,ptr,ptr,ptr]
          10    0.10%    0.01%  void <- [ptr,i32,ptr,ptr,ptr]
           9    0.09%    0.01%  i16 <- [ptr,i32,ptr]
           9    0.09%    0.01%  i32 <- [i32,ptr,i8,i32,i8,ptr,ptr]
           9    0.09%    0.01%  i32 <- [i32,ptr,ptr,i32,ptr]
           9    0.09%    0.01%  i32 <- [ptr,i64,ptr,i32,ptr]
           9    0.09%    0.01%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,i32,ptr]
           9    0.09%    0.01%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr]
           8    0.08%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,i8,i32,i32,i32,ptr,ptr]
           8    0.08%    0.00%  i64 <- [ptr,i64,i64,i64,i32,i64,ptr]
           8    0.08%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr]
           8    0.08%    0.00%  ptr <- [ptr,i64,i64,ptr,i32,ptr,ptr]
           8    0.08%    0.00%  ptr <- [ptr,i64,ptr,i64,ptr]
           8    0.08%    0.00%  void <- [ptr]
           7    0.07%    0.00%  i1 <- [ptr,ptr]
           7    0.07%    0.00%  i32 <- [i32,i32,ptr,ptr,ptr]
           7    0.07%    0.00%  i32 <- [i32,ptr,i16,ptr,i64,i32,ptr]
           7    0.07%    0.00%  i32 <- [i32,ptr,i64,i64,ptr,i64,ptr]
           7    0.07%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr]
           7    0.07%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           7    0.07%    0.00%  i64 <- [ptr,i64,i64,ptr]
           6    0.06%    0.00%  i32 <- [i32,i32,i32,ptr]
           6    0.06%    0.00%  i32 <- [i32,ptr,i32,ptr,ptr,ptr,ptr]
           6    0.06%    0.00%  i32 <- [i32,ptr,i64,ptr]
           6    0.06%    0.00%  i32 <- [i32,ptr,ptr,ptr]
           6    0.06%    0.00%  ptr <- [ptr,i64,i32,i32,i32,i64,ptr]
           6    0.06%    0.00%  ptr <- [ptr,ptr,ptr,ptr]
           6    0.06%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
           6    0.06%    0.00%  void <- [ptr,i64,i32,i32,ptr]
           5    0.05%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,i32,ptr]
           5    0.05%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.05%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,ptr]
           5    0.05%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
           5    0.05%    0.00%  i32 <- [ptr,ptr,ptr,i8,i32,ptr]
           5    0.05%    0.00%  i8 <- [ptr,i32,ptr,ptr]
           5    0.05%    0.00%  ptr <- [ptr,i8,ptr]
           5    0.05%    0.00%  void <- [ptr,ptr,i8,i8,ptr]
           4    0.04%    0.00%  i16 <- [ptr,ptr]
           4    0.04%    0.00%  i32 <- [i32,ptr,i64,ptr,ptr]
           4    0.04%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr]
           4    0.04%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,ptr]
           4    0.04%    0.00%  i32 <- [ptr,i64,i32,ptr]
           4    0.04%    0.00%  i32 <- [ptr,i8,ptr,ptr]
           4    0.04%    0.00%  i32 <- [ptr,ptr,ptr,i16,i32,ptr]
           4    0.04%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           4    0.04%    0.00%  i64 <- [i64,i64,i64,ptr]
           4    0.04%    0.00%  i64 <- [i64,ptr,i64,ptr]
           4    0.04%    0.00%  i8 <- [ptr,ptr,i8,ptr]
           4    0.04%    0.00%  ptr <- [ptr,i32,i64,ptr]
           4    0.04%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i1,ptr]
           4    0.04%    0.00%  void <- [ptr,i32,i32,i64,ptr]
           4    0.04%    0.00%  void <- [ptr,i64,i32,ptr]
           4    0.04%    0.00%  void <- [ptr,ptr,ptr,i64,ptr]
           4    0.04%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr]
           3    0.03%    0.00%  double <- [ptr,ptr]
           3    0.03%    0.00%  i1 <- [ptr,ptr,ptr]
           3    0.03%    0.00%  i32 <- [ptr,i16,ptr]
           3    0.03%    0.00%  i32 <- [ptr,i32,i64,ptr]
           3    0.03%    0.00%  i32 <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr,i32,ptr]
           3    0.03%    0.00%  i32 <- [ptr,i64,ptr,i64,ptr]
           3    0.03%    0.00%  i32 <- [ptr,i64,ptr,ptr]
           3    0.03%    0.00%  i32 <- [ptr,i8,i8,ptr]
           3    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i16,ptr,i16,ptr]
           3    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,i16,i16,i16,i32,i32,ptr,i8,ptr]
           3    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr]
           3    0.03%    0.00%  i64 <- [i32,ptr,i64,i32,ptr]
           3    0.03%    0.00%  i64 <- [i64,ptr]
           3    0.03%    0.00%  i64 <- [ptr,i64,ptr]
           3    0.03%    0.00%  ptr <- [i32,i32,i32,i32,i32,i64,ptr,ptr,ptr]
           3    0.03%    0.00%  ptr <- [i32,i32,i32,i32,ptr,ptr,ptr]
           3    0.03%    0.00%  ptr <- [ptr,i32,ptr,ptr,i64,ptr]
           3    0.03%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr]
           3    0.03%    0.00%  ptr <- [ptr,ptr,ptr,i64,ptr]
           3    0.03%    0.00%  void <- [ptr,i32,i16,ptr]
           3    0.03%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,ptr]
           3    0.03%    0.00%  void <- [ptr,i64,i64,ptr,ptr]
           3    0.03%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr]
           2    0.02%    0.00%  i16 <- [i16,ptr]
           2    0.02%    0.00%  i1 <- [i32,ptr,ptr]
           2    0.02%    0.00%  i32 <- [i32,i32,i64,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,i16,i8,ptr,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,i32,i32,i16,i8,ptr,ptr,ptr,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,i32,i8,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,i64,ptr,i32,ptr,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,ptr,i64,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.02%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,ptr,ptr,i32,ptr,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i64,i32,ptr,ptr]
           2    0.02%    0.00%  i32 <- [ptr,i64,i64,i32,ptr,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,i32,i32,i32,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i64,i64,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i64,ptr,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,i8,ptr,ptr,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i64,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,i32,ptr]
           2    0.02%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,ptr]
           2    0.02%    0.00%  i64 <- [i32,ptr,ptr,i64,ptr]
           2    0.02%    0.00%  i8 <- [i32,ptr]
           2    0.02%    0.00%  i8 <- [i8,i8,ptr,ptr,ptr]
           2    0.02%    0.00%  i8 <- [ptr,i32,ptr]
           2    0.02%    0.00%  ptr <- [i32,ptr,ptr,ptr,i64,ptr]
           2    0.02%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr,ptr]
           2    0.02%    0.00%  ptr <- [ptr,i64,ptr,ptr]
           2    0.02%    0.00%  ptr <- [ptr,i8,i64,ptr]
           2    0.02%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.02%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.02%    0.00%  void <- [ptr,i16,ptr]
           2    0.02%    0.00%  void <- [ptr,i32,i32,ptr,ptr]
           2    0.02%    0.00%  void <- [ptr,i64,i64,i64,ptr,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,i32,i64,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,i64,i64,ptr]
           2    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [i32,i32,i32,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [i32,i32,ptr,ptr]
           1    0.01%    0.00%  i32 <- [i32,i64,i32,ptr,i64,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [i32,i64,ptr,ptr]
           1    0.01%    0.00%  i32 <- [i32,i64,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i16,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i32,i32,i32,i32,i32,i32,ptr,ptr,i32,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i32,ptr,i32,i32,i32,i32,i32,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,i64,ptr,i64,ptr]
           1    0.01%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr,i64,ptr]
           1    0.01%    0.00%  i32 <- [i8,ptr,ptr,ptr,ptr,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,double,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i16,i16,i32,i64,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i16,i16,i32,ptr,ptr,i64,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i16,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr,i32,i16,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,ptr,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,ptr,i16,i32,i32,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,ptr,i32,i32,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,ptr,i32,i32,i32,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,double,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,i64,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,i64,ptr]
           1    0.01%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,i64,i64,i64,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i64,i32,ptr]
           1    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.01%    0.00%  i64 <- [i32,i32,i64,ptr]
           1    0.01%    0.00%  i64 <- [ptr]
           1    0.01%    0.00%  i64 <- [ptr,i32,ptr]
           1    0.01%    0.00%  i64 <- [ptr,i64,i32,ptr]
           1    0.01%    0.00%  i64 <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
           1    0.01%    0.00%  i64 <- [ptr,ptr,i32,ptr,ptr]
           1    0.01%    0.00%  ptr <- [i32,i32,i32,i8,ptr]
           1    0.01%    0.00%  ptr <- [i32,i32,ptr,ptr]
           1    0.01%    0.00%  ptr <- [i32,i64,ptr,ptr]
           1    0.01%    0.00%  ptr <- [i32,ptr,ptr,ptr]
           1    0.01%    0.00%  ptr <- [i32,ptr,ptr,ptr,ptr,ptr]
           1    0.01%    0.00%  ptr <- [ptr,i8,i32,ptr]
           1    0.01%    0.00%  ptr <- [ptr,i8,ptr,ptr]
           1    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr]
           1    0.01%    0.00%  void <- [i64,ptr,ptr]
           1    0.01%    0.00%  void <- [i8,i8,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,i64,i32,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,i64,i64,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,i64,i64,ptr,ptr,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,ptr,ptr]
           1    0.01%    0.00%  void <- [ptr,i64,ptr,ptr,ptr]
           1    0.01%    0.00%  void <- [ptr,i8,i64,ptr,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,i32,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,i32,i32,ptr,i32,ptr,i32,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i64,i64,i64,i64,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,i64,ptr,i64,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i32,ptr,ptr]
           1    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
```

#### alloca

```text
       count  opcode%   total%  types
       6,655   99.98%    3.82%  ptr <- [i32]
           1    0.02%    0.00%  ptr <- [i64]
```

#### zext

```text
       count  opcode%   total%  types
       2,268   35.33%    1.30%  i64 <- [i32]
       2,044   31.84%    1.17%  i32 <- [i8]
       1,408   21.93%    0.81%  i32 <- [i16]
         265    4.13%    0.15%  i64 <- [i8]
         197    3.07%    0.11%  i64 <- [i16]
         113    1.76%    0.06%  i32 <- [i1]
         111    1.73%    0.06%  i64 <- [i1]
           9    0.14%    0.01%  i16 <- [i8]
           5    0.08%    0.00%  i8 <- [i1]
```

#### add

```text
       count  opcode%   total%  types
       2,919   74.67%    1.68%  i32 <- [i32,i32]
         854   21.85%    0.49%  i64 <- [i64,i64]
         102    2.61%    0.06%  i16 <- [i16,i16]
          34    0.87%    0.02%  i8 <- [i8,i8]
```

#### sub

```text
       count  opcode%   total%  types
       1,211   64.41%    0.69%  i32 <- [i32,i32]
         669   35.59%    0.38%  i64 <- [i64,i64]
```

#### sext

```text
       count  opcode%   total%  types
       1,638   93.33%    0.94%  i64 <- [i32]
          92    5.24%    0.05%  i32 <- [i16]
          12    0.68%    0.01%  i64 <- [i16]
          10    0.57%    0.01%  i32 <- [i8]
           3    0.17%    0.00%  i64 <- [i8]
```

#### and

```text
       count  opcode%   total%  types
       1,384   87.98%    0.79%  i32 <- [i32,i32]
         180   11.44%    0.10%  i64 <- [i64,i64]
           9    0.57%    0.01%  i8 <- [i8,i8]
```

#### trunc

```text
       count  opcode%   total%  types
         488   35.52%    0.28%  i8 <- [i32]
         423   30.79%    0.24%  i32 <- [i64]
         387   28.17%    0.22%  i16 <- [i32]
          46    3.35%    0.03%  i8 <- [i64]
          17    1.24%    0.01%  i8 <- [i16]
          13    0.95%    0.01%  i16 <- [i64]
```

#### shl

```text
       count  opcode%   total%  types
         974   90.44%    0.56%  i32 <- [i32,i32]
         103    9.56%    0.06%  i64 <- [i64,i64]
```

#### ret

```text
       count  opcode%   total%  types
         510   53.35%    0.29%  void <- [i32]
         216   22.59%    0.12%  void <- [-]
         153   16.00%    0.09%  void <- [ptr]
          48    5.02%    0.03%  void <- [i64]
          16    1.67%    0.01%  void <- [i8]
           7    0.73%    0.00%  void <- [i16]
           5    0.52%    0.00%  void <- [i1]
           1    0.10%    0.00%  void <- [double]
```

#### or

```text
       count  opcode%   total%  types
         814   94.10%    0.47%  i32 <- [i32,i32]
          47    5.43%    0.03%  i64 <- [i64,i64]
           4    0.46%    0.00%  i8 <- [i8,i8]
```

#### lshr

```text
       count  opcode%   total%  types
         631   85.04%    0.36%  i32 <- [i32,i32]
         108   14.56%    0.06%  i64 <- [i64,i64]
           3    0.40%    0.00%  i8 <- [i8,i8]
```

#### xor

```text
       count  opcode%   total%  types
         563   92.14%    0.32%  i32 <- [i32,i32]
          41    6.71%    0.02%  i1 <- [i1,i1]
           7    1.15%    0.00%  i64 <- [i64,i64]
```

#### phi

```text
       count  opcode%   total%  types
         195   39.16%    0.11%  i32 <- [i32,i32]
         151   30.32%    0.09%  i1 <- [i1,i1]
          62   12.45%    0.04%  ptr <- [ptr,ptr]
          45    9.04%    0.03%  i64 <- [i64,i64]
          22    4.42%    0.01%  i1 <- [i1,i1,i1]
           7    1.41%    0.00%  i1 <- [i1,i1,i1,i1]
           7    1.41%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1]
           4    0.80%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1]
           3    0.60%    0.00%  i1 <- [i1,i1,i1,i1,i1]
           2    0.40%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1,i1]
```

#### mul

```text
       count  opcode%   total%  types
         270   70.31%    0.15%  i32 <- [i32,i32]
         114   29.69%    0.07%  i64 <- [i64,i64]
```

#### ptrtoint

```text
       count  opcode%   total%  types
         299  100.00%    0.17%  i64 <- [ptr]
```

#### ashr

```text
       count  opcode%   total%  types
         185   98.93%    0.11%  i32 <- [i32,i32]
           2    1.07%    0.00%  i64 <- [i64,i64]
```

#### switch

```text
       count  opcode%   total%  types
          34   21.94%    0.02%  void <- [i32,label,label,label,label]
          29   18.71%    0.02%  void <- [i32,label,label,label]
          13    8.39%    0.01%  void <- [i32,label,label,label,label,label]
           9    5.81%    0.01%  void <- [i32,label,label]
           9    5.81%    0.01%  void <- [i32,label,label,label,label,label,label]
           8    5.16%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
           7    4.52%    0.00%  void <- [i32,label,label,label,label,label,label,label]
           4    2.58%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
           4    2.58%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           4    2.58%    0.00%  void <- [i64,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           3    1.94%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label]
           3    1.94%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i64,label,label,label]
           2    1.29%    0.00%  void <- [i64,label,label,label,label]
           2    1.29%    0.00%  void <- [i64,label,label,label,label,label,label,label,label]
           2    1.29%    0.00%  void <- [i64,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.65%    0.00%  void <- [i64,label,label,label,label,label,label,label]
```

#### select

```text
       count  opcode%   total%  types
          86   77.48%    0.05%  i32 <- [i1,i32,i32]
          25   22.52%    0.01%  ptr <- [i1,ptr,ptr]
```

#### udiv

```text
       count  opcode%   total%  types
          56   58.33%    0.03%  i32 <- [i32,i32]
          40   41.67%    0.02%  i64 <- [i64,i64]
```

#### urem

```text
       count  opcode%   total%  types
          47   64.38%    0.03%  i32 <- [i32,i32]
          26   35.62%    0.01%  i64 <- [i64,i64]
```

#### sdiv

```text
       count  opcode%   total%  types
          28   70.00%    0.02%  i32 <- [i32,i32]
          12   30.00%    0.01%  i64 <- [i64,i64]
```

#### srem

```text
       count  opcode%   total%  types
          24   92.31%    0.01%  i32 <- [i32,i32]
           2    7.69%    0.00%  i64 <- [i64,i64]
```

#### unreachable

```text
       count  opcode%   total%  types
          22  100.00%    0.01%  void <- [-]
```

#### fdiv

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  double <- [double,double]
```

#### fmul

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  double <- [double,double]
```

#### fptosi

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i32 <- [double]
```

#### fptoui

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i8 <- [double]
```

#### fsub

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  double <- [double,double]
```

#### uitofp

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  double <- [i64]
```

### consumer-typeset

#### load

```text
       count  opcode%   total%  types
      54,195   74.35%   22.41%  ptr <- [ptr]
      11,133   15.27%    4.60%  i32 <- [ptr]
       5,504    7.55%    2.28%  i8 <- [ptr]
       1,845    2.53%    0.76%  i16 <- [ptr]
         144    0.20%    0.06%  float <- [ptr]
          36    0.05%    0.01%  i64 <- [ptr]
          34    0.05%    0.01%  double <- [ptr]
```

#### getelementptr

```text
       count  opcode%   total%  types
      49,911   69.84%   20.64%  ptr <- [ptr,i32,i32]
      20,762   29.05%    8.59%  ptr <- [ptr,i64,i64]
         599    0.84%    0.25%  ptr <- [ptr,i64]
         192    0.27%    0.08%  ptr <- [ptr,i32]
```

#### store

```text
       count  opcode%   total%  types
      19,912   73.13%    8.23%  void <- [ptr,ptr]
       4,772   17.53%    1.97%  void <- [i32,ptr]
       1,451    5.33%    0.60%  void <- [i8,ptr]
         988    3.63%    0.41%  void <- [i16,ptr]
          59    0.22%    0.02%  void <- [float,ptr]
          24    0.09%    0.01%  void <- [double,ptr]
          23    0.08%    0.01%  void <- [i64,ptr]
```

#### br

```text
       count  opcode%   total%  types
      16,246   62.30%    6.72%  void <- [label]
       9,830   37.70%    4.06%  void <- [i1,label,label]
```

#### icmp

```text
       count  opcode%   total%  types
       5,318   53.04%    2.20%  i1 <- [i32,i32]
       4,076   40.65%    1.69%  i1 <- [ptr,ptr]
         590    5.88%    0.24%  i1 <- [i64,i64]
          39    0.39%    0.02%  i1 <- [i8,i8]
           3    0.03%    0.00%  i1 <- [i16,i16]
```

#### zext

```text
       count  opcode%   total%  types
       4,743   71.90%    1.96%  i32 <- [i8]
         991   15.02%    0.41%  i32 <- [i16]
         435    6.59%    0.18%  i64 <- [i8]
         175    2.65%    0.07%  i32 <- [i1]
         164    2.49%    0.07%  i64 <- [i32]
          69    1.05%    0.03%  i64 <- [i1]
          20    0.30%    0.01%  i64 <- [i16]
```

#### call

```text
       count  opcode%   total%  types
         770   12.71%    0.32%  ptr <- [i32,i32,ptr,i32,ptr,ptr]
         745   12.29%    0.31%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr]
         569    9.39%    0.24%  i32 <- [ptr,ptr,ptr]
         558    9.21%    0.23%  ptr <- [i32,ptr,ptr]
         314    5.18%    0.13%  i32 <- [ptr,ptr]
         238    3.93%    0.10%  ptr <- [ptr,ptr,ptr]
         167    2.76%    0.07%  void <- [ptr,ptr]
         158    2.61%    0.07%  ptr <- [i32,ptr,ptr,ptr]
         151    2.49%    0.06%  ptr <- [ptr,ptr]
         117    1.93%    0.05%  ptr <- [i32,ptr]
         116    1.91%    0.05%  i64 <- [ptr,ptr]
         114    1.88%    0.05%  ptr <- [ptr,i32,i32,i32,i32,i8,ptr]
         110    1.82%    0.05%  void <- [ptr,ptr,ptr]
         106    1.75%    0.04%  i32 <- [ptr,ptr,ptr,ptr]
         106    1.75%    0.04%  ptr <- [ptr]
         100    1.65%    0.04%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr]
          84    1.39%    0.03%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,i32,ptr]
          84    1.39%    0.03%  void <- [ptr]
          77    1.27%    0.03%  ptr <- [i16,ptr]
          68    1.12%    0.03%  ptr <- [ptr,i32,ptr,ptr]
          68    1.12%    0.03%  void <- [i32,ptr,ptr]
          60    0.99%    0.02%  ptr <- [ptr,i32,ptr]
          59    0.97%    0.02%  i32 <- [i32,ptr,ptr]
          54    0.89%    0.02%  ptr <- [ptr,ptr,ptr,ptr]
          52    0.86%    0.02%  i32 <- [ptr]
          52    0.86%    0.02%  i32 <- [ptr,ptr,i32,ptr]
          51    0.84%    0.02%  ptr <- [ptr,i32,i32,i32,i32,i32,i32,i32,ptr,ptr,ptr]
          48    0.79%    0.02%  ptr <- [i64,ptr]
          33    0.54%    0.01%  void <- [ptr,i32,ptr]
          31    0.51%    0.01%  void <- [i32,ptr]
          31    0.51%    0.01%  void <- [ptr,i32,i32,ptr]
          30    0.50%    0.01%  void <- [ptr,ptr,i32,ptr,ptr]
          27    0.45%    0.01%  void <- [ptr,i32,i32,i32,ptr]
          26    0.43%    0.01%  i32 <- [i32,i32,i32,ptr,ptr]
          24    0.40%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr]
          22    0.36%    0.01%  ptr <- [i32,i32,ptr,i32,ptr,i32,ptr]
          22    0.36%    0.01%  ptr <- [i32,i32,ptr,i32,ptr,ptr,i32,ptr]
          22    0.36%    0.01%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
          21    0.35%    0.01%  ptr <- [ptr,i8,ptr,i8,i32,i32,i32,ptr,ptr,ptr]
          21    0.35%    0.01%  ptr <- [ptr,ptr,i32,i32,ptr]
          19    0.31%    0.01%  i16 <- [ptr,ptr,ptr,i32,i32,ptr]
          19    0.31%    0.01%  i32 <- [ptr,ptr,double,ptr]
          17    0.28%    0.01%  void <- [ptr,i32,ptr,i16,ptr]
          16    0.26%    0.01%  ptr <- [i8,ptr,i8,i8,i8,ptr,ptr]
          13    0.21%    0.01%  double <- [double,ptr]
          12    0.20%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr]
          11    0.18%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          11    0.18%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
          11    0.18%    0.00%  ptr <- [ptr,i32,ptr,i32,ptr]
          10    0.17%    0.00%  i32 <- [i32,ptr]
          10    0.17%    0.00%  ptr <- [i16,i32,i32,ptr]
          10    0.17%    0.00%  void <- [i32,i32,ptr]
          10    0.17%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,i16,i64,i32,i32,ptr]
          10    0.17%    0.00%  void <- [ptr,ptr,ptr,ptr]
           9    0.15%    0.00%  i32 <- [i32,ptr,ptr,ptr]
           9    0.15%    0.00%  ptr <- [ptr,i32,i32,ptr,ptr]
           9    0.15%    0.00%  void <- [ptr,ptr,ptr,i32,ptr]
           8    0.13%    0.00%  float <- [float,float,float,ptr]
           8    0.13%    0.00%  i32 <- [i32,i32,i32,ptr,i32,i32,ptr]
           8    0.13%    0.00%  i32 <- [ptr,i64,i32,ptr]
           8    0.13%    0.00%  i8 <- [ptr,i32,ptr]
           8    0.13%    0.00%  ptr <- [i32,ptr,ptr,ptr,ptr]
           8    0.13%    0.00%  void <- [ptr,i32,ptr,ptr,ptr]
           7    0.12%    0.00%  i16 <- [ptr,ptr,ptr]
           7    0.12%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
           7    0.12%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr]
           7    0.12%    0.00%  void <- [ptr,i32,ptr,ptr]
           7    0.12%    0.00%  void <- [ptr,ptr,i64,i1,ptr]
           6    0.10%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           6    0.10%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr]
           6    0.10%    0.00%  ptr <- [i16,i64,i32,ptr]
           6    0.10%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,i32,ptr]
           6    0.10%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,i32,ptr]
           6    0.10%    0.00%  ptr <- [ptr,ptr,i32,ptr]
           6    0.10%    0.00%  void <- [i32,ptr,i32,ptr]
           6    0.10%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.10%    0.00%  void <- [ptr,ptr,i32,ptr]
           5    0.08%    0.00%  i16 <- [i16,ptr]
           5    0.08%    0.00%  i16 <- [i32,ptr]
           5    0.08%    0.00%  i16 <- [ptr,ptr]
           5    0.08%    0.00%  i32 <- [i32,i32,ptr,ptr]
           5    0.08%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.08%    0.00%  ptr <- [ptr,i64,ptr]
           5    0.08%    0.00%  void <- [i16,i32,i32,i32,i32,ptr]
           5    0.08%    0.00%  void <- [ptr,i16,ptr,ptr,ptr]
           4    0.07%    0.00%  i32 <- [i32,i32,ptr,i32,ptr]
           4    0.07%    0.00%  i32 <- [ptr,i32,ptr]
           4    0.07%    0.00%  i32 <- [ptr,ptr,double,double,ptr]
           4    0.07%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr]
           4    0.07%    0.00%  ptr <- [ptr,i32,i32,ptr]
           4    0.07%    0.00%  void <- [float,float,ptr]
           4    0.07%    0.00%  void <- [ptr,i32,i32,float,ptr,ptr]
           4    0.07%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.07%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.07%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.05%    0.00%  float <- [i32,i32,ptr]
           3    0.05%    0.00%  float <- [ptr,ptr]
           3    0.05%    0.00%  i32 <- [i16,ptr]
           3    0.05%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,ptr]
           3    0.05%    0.00%  i64 <- [ptr]
           3    0.05%    0.00%  i8 <- [ptr,ptr,ptr]
           3    0.05%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,i32,i32,ptr]
           3    0.05%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,double,ptr]
           3    0.05%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,i32,i32,ptr]
           3    0.05%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.05%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.05%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,i32,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,i8,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i16,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,double,i32,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i64,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  ptr <- [i32,i32,ptr]
           2    0.03%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,double,ptr,ptr]
           2    0.03%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.03%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  ptr <- [i32,ptr,i32,i32,i32,i32,i32,i32,ptr]
           2    0.03%    0.00%  ptr <- [ptr,i32,i32,ptr,i32,ptr]
           2    0.03%    0.00%  ptr <- [ptr,i8,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  void <- [i16,i32,ptr,ptr]
           2    0.03%    0.00%  void <- [i32,i32,ptr,ptr]
           2    0.03%    0.00%  void <- [ptr,float,float,ptr]
           2    0.03%    0.00%  void <- [ptr,float,i32,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,i32,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,i32,ptr,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,i32,ptr,ptr,i16,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
           1    0.02%    0.00%  double <- [double,double,double,ptr]
           1    0.02%    0.00%  double <- [double,double,ptr]
           1    0.02%    0.00%  i32 <- [i16,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [i32,i8,i8,ptr]
           1    0.02%    0.00%  i32 <- [i8,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i16,ptr,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,double,double,double,double,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i64,i32,ptr,ptr]
           1    0.02%    0.00%  i64 <- [ptr,i64,i64,ptr,ptr]
           1    0.02%    0.00%  ptr <- [i32,i32,i32,ptr]
           1    0.02%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,double,ptr]
           1    0.02%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,i32,i32,i32,ptr]
           1    0.02%    0.00%  ptr <- [i32,i32,ptr,i32,ptr,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  ptr <- [i64,i64,ptr]
           1    0.02%    0.00%  ptr <- [ptr,i8,ptr]
           1    0.02%    0.00%  void <- [i16,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,float,ptr]
           1    0.02%    0.00%  void <- [ptr,i16,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,i64,i64,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,i8,i64,i1,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i16,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i16,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,i32,ptr]
```

#### sext

```text
       count  opcode%   total%  types
       4,475   96.78%    1.85%  i64 <- [i32]
         148    3.20%    0.06%  i32 <- [i16]
           1    0.02%    0.00%  i64 <- [i16]
```

#### and

```text
       count  opcode%   total%  types
       1,471   40.83%    0.61%  i32 <- [i32,i32]
       1,423   39.49%    0.59%  i16 <- [i16,i16]
         709   19.68%    0.29%  i8 <- [i8,i8]
```

#### alloca

```text
       count  opcode%   total%  types
       3,286  100.00%    1.36%  ptr <- [i32]
```

#### phi

```text
       count  opcode%   total%  types
       2,079   72.41%    0.86%  ptr <- [ptr,ptr]
         551   19.19%    0.23%  i32 <- [i32,i32]
         199    6.93%    0.08%  i1 <- [i1,i1]
          20    0.70%    0.01%  i1 <- [i1,i1,i1]
           9    0.31%    0.00%  float <- [float,float]
           4    0.14%    0.00%  double <- [double,double]
           4    0.14%    0.00%  i1 <- [i1,i1,i1,i1,i1]
           2    0.07%    0.00%  i1 <- [i1,i1,i1,i1]
           1    0.03%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1]
           1    0.03%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1]
           1    0.03%    0.00%  i64 <- [i64,i64]
```

#### or

```text
       count  opcode%   total%  types
         602   42.39%    0.25%  i16 <- [i16,i16]
         528   37.18%    0.22%  i32 <- [i32,i32]
         289   20.35%    0.12%  i8 <- [i8,i8]
           1    0.07%    0.00%  i64 <- [i64,i64]
```

#### lshr

```text
       count  opcode%   total%  types
         591   52.58%    0.24%  i16 <- [i16,i16]
         359   31.94%    0.15%  i32 <- [i32,i32]
         174   15.48%    0.07%  i8 <- [i8,i8]
```

#### add

```text
       count  opcode%   total%  types
       1,005   92.20%    0.42%  i32 <- [i32,i32]
          81    7.43%    0.03%  i64 <- [i64,i64]
           2    0.18%    0.00%  i16 <- [i16,i16]
           2    0.18%    0.00%  i8 <- [i8,i8]
```

#### trunc

```text
       count  opcode%   total%  types
         367   49.86%    0.15%  i16 <- [i32]
         291   39.54%    0.12%  i8 <- [i32]
          74   10.05%    0.03%  i32 <- [i64]
           2    0.27%    0.00%  i8 <- [i16]
           1    0.14%    0.00%  i16 <- [i64]
           1    0.14%    0.00%  i8 <- [i64]
```

#### shl

```text
       count  opcode%   total%  types
         305   42.30%    0.13%  i32 <- [i32,i32]
         287   39.81%    0.12%  i16 <- [i16,i16]
         128   17.75%    0.05%  i8 <- [i8,i8]
           1    0.14%    0.00%  i64 <- [i64,i64]
```

#### sub

```text
       count  opcode%   total%  types
         473   89.08%    0.20%  i32 <- [i32,i32]
          58   10.92%    0.02%  i64 <- [i64,i64]
```

#### ret

```text
       count  opcode%   total%  types
         251   55.53%    0.10%  void <- [-]
         135   29.87%    0.06%  void <- [ptr]
          55   12.17%    0.02%  void <- [i32]
           6    1.33%    0.00%  void <- [i16]
           2    0.44%    0.00%  void <- [float]
           2    0.44%    0.00%  void <- [i8]
           1    0.22%    0.00%  void <- [i64]
```

#### mul

```text
       count  opcode%   total%  types
         120   76.92%    0.05%  i32 <- [i32,i32]
          36   23.08%    0.01%  i64 <- [i64,i64]
```

#### sitofp

```text
       count  opcode%   total%  types
         102   87.93%    0.04%  float <- [i32]
          14   12.07%    0.01%  double <- [i32]
```

#### sdiv

```text
       count  opcode%   total%  types
          94   98.95%    0.04%  i32 <- [i32,i32]
           1    1.05%    0.00%  i64 <- [i64,i64]
```

#### switch

```text
       count  opcode%   total%  types
          23   24.73%    0.01%  void <- [i32,label,label,label,label]
          14   15.05%    0.01%  void <- [i32,label,label,label,label,label]
           8    8.60%    0.00%  void <- [i32,label,label,label,label,label,label]
           7    7.53%    0.00%  void <- [i32,label,label,label,label,label,label,label]
           7    7.53%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
           4    4.30%    0.00%  void <- [i32,label,label,label]
           3    3.23%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
           3    3.23%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label]
           2    2.15%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           2    2.15%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.08%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
```

#### fpext

```text
       count  opcode%   total%  types
          79  100.00%    0.03%  double <- [float]
```

#### select

```text
       count  opcode%   total%  types
          34   49.28%    0.01%  i32 <- [i1,i32,i32]
          34   49.28%    0.01%  ptr <- [i1,ptr,ptr]
           1    1.45%    0.00%  i64 <- [i1,i64,i64]
```

#### fptosi

```text
       count  opcode%   total%  types
          53   77.94%    0.02%  i32 <- [float]
          14   20.59%    0.01%  i32 <- [double]
           1    1.47%    0.00%  i16 <- [double]
```

#### ptrtoint

```text
       count  opcode%   total%  types
          58   90.62%    0.02%  i64 <- [ptr]
           6    9.38%    0.00%  i32 <- [ptr]
```

#### fdiv

```text
       count  opcode%   total%  types
          49   90.74%    0.02%  float <- [float,float]
           5    9.26%    0.00%  double <- [double,double]
```

#### fmul

```text
       count  opcode%   total%  types
          36   69.23%    0.01%  float <- [float,float]
          16   30.77%    0.01%  double <- [double,double]
```

#### fcmp

```text
       count  opcode%   total%  types
          26   65.00%    0.01%  i1 <- [double,double]
          14   35.00%    0.01%  i1 <- [float,float]
```

#### srem

```text
       count  opcode%   total%  types
          35  100.00%    0.01%  i32 <- [i32,i32]
```

#### fptrunc

```text
       count  opcode%   total%  types
          16  100.00%    0.01%  float <- [double]
```

#### fneg

```text
       count  opcode%   total%  types
          15  100.00%    0.01%  float <- [float]
```

#### udiv

```text
       count  opcode%   total%  types
          12   80.00%    0.00%  i64 <- [i64,i64]
           3   20.00%    0.00%  i32 <- [i32,i32]
```

#### xor

```text
       count  opcode%   total%  types
          14  100.00%    0.01%  i1 <- [i1,i1]
```

#### urem

```text
       count  opcode%   total%  types
           6   54.55%    0.00%  i32 <- [i32,i32]
           5   45.45%    0.00%  i64 <- [i64,i64]
```

#### fadd

```text
       count  opcode%   total%  types
           6   60.00%    0.00%  double <- [double,double]
           4   40.00%    0.00%  float <- [float,float]
```

#### fsub

```text
       count  opcode%   total%  types
           8   80.00%    0.00%  double <- [double,double]
           2   20.00%    0.00%  float <- [float,float]
```

#### unreachable

```text
       count  opcode%   total%  types
           7  100.00%    0.00%  void <- [-]
```

#### ashr

```text
       count  opcode%   total%  types
           2  100.00%    0.00%  i32 <- [i32,i32]
```

#### inttoptr

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  ptr <- [i64]
```

### kimwitu++

#### load

```text
       count  opcode%   total%  types
      48,576   92.93%   29.14%  ptr <- [ptr]
       1,800    3.44%    1.08%  i32 <- [ptr]
       1,107    2.12%    0.66%  i64 <- [ptr]
         656    1.26%    0.39%  i8 <- [ptr]
          51    0.10%    0.03%  i1 <- [ptr]
          44    0.08%    0.03%  i16 <- [ptr]
          26    0.05%    0.02%  [2 x i64] <- [ptr]
           8    0.02%    0.00%  double <- [ptr]
           2    0.00%    0.00%  [2 x ptr] <- [ptr]
```

#### store

```text
       count  opcode%   total%  types
      21,024   87.83%   12.61%  void <- [ptr,ptr]
       1,903    7.95%    1.14%  void <- [i32,ptr]
         488    2.04%    0.29%  void <- [i64,ptr]
         329    1.37%    0.20%  void <- [i8,ptr]
         158    0.66%    0.09%  void <- [i1,ptr]
          29    0.12%    0.02%  void <- [[2 x i64],ptr]
           4    0.02%    0.00%  void <- [double,ptr]
           2    0.01%    0.00%  void <- [[2 x ptr],ptr]
           1    0.00%    0.00%  void <- [i16,ptr]
```

#### call

```text
       count  opcode%   total%  types
       4,519   20.97%    2.71%  void <- [ptr,ptr,ptr,ptr]
       3,267   15.16%    1.96%  ptr <- [ptr,ptr]
       3,012   13.98%    1.81%  void <- [ptr,ptr]
       1,818    8.44%    1.09%  i32 <- [ptr,ptr]
       1,638    7.60%    0.98%  ptr <- [ptr,ptr,ptr]
       1,006    4.67%    0.60%  ptr <- [ptr,ptr,ptr,i64,ptr]
         859    3.99%    0.52%  void <- [ptr,ptr,ptr]
         791    3.67%    0.47%  ptr <- [ptr]
         674    3.13%    0.40%  void <- [ptr,i64,ptr]
         419    1.94%    0.25%  void <- [ptr]
         386    1.79%    0.23%  ptr <- [i64,ptr]
         360    1.67%    0.22%  ptr <- [ptr,ptr,ptr,ptr]
         350    1.62%    0.21%  ptr <- [ptr,i32,ptr]
         318    1.48%    0.19%  i1 <- [ptr,ptr]
         258    1.20%    0.15%  ptr <- [ptr,ptr,i32,ptr]
         195    0.91%    0.12%  void <- [ptr,i32,ptr,ptr]
         165    0.77%    0.10%  void <- [ptr,i32,ptr]
         164    0.76%    0.10%  i64 <- [ptr,ptr]
         143    0.66%    0.09%  i1 <- [ptr,ptr,ptr]
         127    0.59%    0.08%  void <- [i32,ptr,ptr,ptr]
         101    0.47%    0.06%  ptr <- [ptr,ptr,ptr,ptr,ptr]
          92    0.43%    0.06%  void <- [i1,ptr]
          73    0.34%    0.04%  void <- [ptr,ptr,i64,ptr]
          69    0.32%    0.04%  void <- [ptr,ptr,i64,i1,ptr]
          61    0.28%    0.04%  ptr <- [ptr,ptr,ptr,i32,ptr]
          60    0.28%    0.04%  i64 <- [i64,ptr]
          56    0.26%    0.03%  i32 <- [ptr,ptr,ptr]
          56    0.26%    0.03%  ptr <- [ptr,i64,ptr]
          43    0.20%    0.03%  i32 <- [ptr,ptr,ptr,ptr]
          34    0.16%    0.02%  ptr <- [i32,ptr]
          27    0.13%    0.02%  i1 <- [ptr,ptr,ptr,ptr]
          27    0.13%    0.02%  i64 <- [ptr]
          24    0.11%    0.01%  ptr <- [ptr,i64,ptr,ptr]
          21    0.10%    0.01%  i64 <- [ptr,ptr,ptr]
          18    0.08%    0.01%  [2 x i64] <- [ptr,ptr,ptr]
          18    0.08%    0.01%  i32 <- [ptr,ptr,i32,ptr]
          18    0.08%    0.01%  void <- [ptr,i1,ptr]
          16    0.07%    0.01%  void <- [i32,ptr]
          14    0.06%    0.01%  i32 <- [i32,ptr]
          14    0.06%    0.01%  void <- [ptr,i8,i64,i1,ptr]
          13    0.06%    0.01%  i32 <- [ptr,ptr,i64,ptr]
          13    0.06%    0.01%  ptr <- [i32,ptr,ptr]
          13    0.06%    0.01%  ptr <- [i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          12    0.06%    0.01%  void <- [ptr,i64,i1,ptr]
          10    0.05%    0.01%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           9    0.04%    0.01%  i32 <- [i32,ptr,ptr]
           9    0.04%    0.01%  i32 <- [ptr]
           8    0.04%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i1,ptr]
           8    0.04%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.04%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.04%    0.00%  void <- [ptr,i32,ptr,ptr,ptr]
           7    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr]
           7    0.03%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.03%    0.00%  i64 <- [ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.03%    0.00%  void <- [i1,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  [2 x i64] <- [ptr,ptr]
           5    0.02%    0.00%  void <- [ptr,ptr,i64,i64,ptr]
           4    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           4    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr]
           4    0.02%    0.00%  i64 <- [ptr,i64,i64,ptr,ptr]
           4    0.02%    0.00%  i64 <- [ptr,i64,ptr]
           4    0.02%    0.00%  void <- [i32,ptr,ptr]
           3    0.01%    0.00%  i64 <- [ptr,ptr,i64,ptr]
           3    0.01%    0.00%  i64 <- [ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i32,i32,i1,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i8,ptr]
           3    0.01%    0.00%  void <- [ptr,i1,i1,ptr]
           2    0.01%    0.00%  i32 <- [ptr,i32,i32,ptr]
           2    0.01%    0.00%  i32 <- [ptr,i32,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr]
           2    0.01%    0.00%  i64 <- [ptr,i64,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i32,i32,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,i64,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i64,ptr]
           2    0.01%    0.00%  void <- [metadata,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i1,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  { i64, i1 } <- [i64,i64,ptr]
           1    0.00%    0.00%  i1 <- [ptr,[2 x i64],[2 x i64],ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,double,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i64 <- [i64,ptr,ptr]
           1    0.00%    0.00%  i64 <- [ptr,[2 x i64],ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,i64,ptr,ptr]
           1    0.00%    0.00%  ptr <- [[2 x ptr],[2 x ptr],ptr,ptr]
           1    0.00%    0.00%  ptr <- [double,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i1,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i64,i64,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i64,ptr,i64,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i64,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [[2 x i64],ptr]
           1    0.00%    0.00%  void <- [double,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,i64,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i64,i64,ptr]
```

#### alloca

```text
       count  opcode%   total%  types
      18,034  100.00%   10.82%  ptr <- [i32]
```

#### getelementptr

```text
       count  opcode%   total%  types
      10,777   61.94%    6.46%  ptr <- [ptr,i32,i32]
       6,261   35.98%    3.76%  ptr <- [ptr,i64]
         253    1.45%    0.15%  ptr <- [ptr,i64,i64]
         108    0.62%    0.06%  ptr <- [ptr,i32]
```

#### br

```text
       count  opcode%   total%  types
      10,873   69.85%    6.52%  void <- [label]
       4,693   30.15%    2.82%  void <- [i1,label,label]
```

#### ret

```text
       count  opcode%   total%  types
       2,774   47.48%    1.66%  void <- [-]
       2,444   41.83%    1.47%  void <- [ptr]
         307    5.25%    0.18%  void <- [i32]
         156    2.67%    0.09%  void <- [i1]
         141    2.41%    0.08%  void <- [i64]
          21    0.36%    0.01%  void <- [[2 x i64]]
```

#### icmp

```text
       count  opcode%   total%  types
       1,976   43.37%    1.19%  i1 <- [ptr,ptr]
       1,975   43.35%    1.18%  i1 <- [i32,i32]
         377    8.27%    0.23%  i1 <- [i8,i8]
         228    5.00%    0.14%  i1 <- [i64,i64]
```

#### extractvalue

```text
       count  opcode%   total%  types
         640   53.65%    0.38%  ptr <- [{ ptr, i32 }]
         549   46.02%    0.33%  i32 <- [{ ptr, i32 }]
           2    0.17%    0.00%  i1 <- [{ i64, i1 }]
           2    0.17%    0.00%  i64 <- [{ i64, i1 }]
```

#### phi

```text
       count  opcode%   total%  types
       1,060   89.83%    0.64%  ptr <- [ptr,ptr]
          75    6.36%    0.04%  i1 <- [i1,i1]
          29    2.46%    0.02%  i64 <- [i64,i64]
           8    0.68%    0.00%  i1 <- [i1,i1,i1]
           7    0.59%    0.00%  i32 <- [i32,i32]
           1    0.08%    0.00%  i1 <- [i1,i1,i1,i1,i1]
```

#### invoke

```text
       count  opcode%   total%  types
         349   42.87%    0.21%  void <- [ptr,ptr,ptr,label,label,ptr]
         136   16.71%    0.08%  void <- [ptr,ptr,label,label,ptr]
          69    8.48%    0.04%  void <- [ptr,label,label,ptr]
          54    6.63%    0.03%  void <- [label,label,ptr]
          42    5.16%    0.03%  void <- [ptr,ptr,ptr,ptr,label,label,ptr]
          36    4.42%    0.02%  ptr <- [ptr,label,label,ptr]
          27    3.32%    0.02%  ptr <- [ptr,ptr,label,label,ptr]
          15    1.84%    0.01%  void <- [ptr,i64,label,label,ptr]
          12    1.47%    0.01%  ptr <- [ptr,i64,ptr,label,label,ptr]
          10    1.23%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           9    1.11%    0.01%  ptr <- [ptr,i32,label,label,ptr]
           6    0.74%    0.00%  i1 <- [ptr,ptr,label,label,ptr]
           4    0.49%    0.00%  ptr <- [label,label,ptr]
           4    0.49%    0.00%  ptr <- [ptr,ptr,ptr,ptr,label,label,ptr]
           3    0.37%    0.00%  i32 <- [ptr,label,label,ptr]
           3    0.37%    0.00%  ptr <- [ptr,i8,label,label,ptr]
           3    0.37%    0.00%  void <- [ptr,ptr,i64,label,label,ptr]
           3    0.37%    0.00%  void <- [ptr,ptr,i64,ptr,i64,ptr,label,label,ptr]
           3    0.37%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           3    0.37%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
           2    0.25%    0.00%  i64 <- [i64,label,label,ptr]
           2    0.25%    0.00%  ptr <- [ptr,i64,ptr,ptr,label,label,ptr]
           2    0.25%    0.00%  ptr <- [ptr,ptr,i64,label,label,ptr]
           1    0.12%    0.00%  [2 x i64] <- [ptr,ptr,ptr,label,label,ptr]
           1    0.12%    0.00%  i32 <- [label,label,ptr]
           1    0.12%    0.00%  i32 <- [ptr,ptr,label,label,ptr]
           1    0.12%    0.00%  i64 <- [ptr,[2 x i64],label,label,ptr]
           1    0.12%    0.00%  i64 <- [ptr,ptr,i64,label,label,ptr]
           1    0.12%    0.00%  i64 <- [ptr,ptr,label,label,ptr]
           1    0.12%    0.00%  ptr <- [ptr,ptr,ptr,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,double,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i1,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i32,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i32,ptr,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i64,ptr,i64,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i64,ptr,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i64,ptr,ptr,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,i64,ptr,ptr,ptr,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,ptr,i32,label,label,ptr]
           1    0.12%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,label,label,ptr]
```

#### switch

```text
       count  opcode%   total%  types
         283   35.51%    0.17%  void <- [i32,label,label,label]
         279   35.01%    0.17%  void <- [i32,label,label]
         103   12.92%    0.06%  void <- [i32,label,label,label,label]
          62    7.78%    0.04%  void <- [i32,label,label,label,label,label]
          21    2.63%    0.01%  void <- [i32,label,label,label,label,label,label]
          14    1.76%    0.01%  void <- [i32,label,label,label,label,label,label,label]
           5    0.63%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
           4    0.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
           3    0.38%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
           3    0.38%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label]
           2    0.25%    0.00%  void <- [i32,label]
           2    0.25%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    0.13%    0.00%  void <- [i64,label,label,label,label,label,label,label,label,label]
```

#### unreachable

```text
       count  opcode%   total%  types
         730  100.00%    0.44%  void <- [-]
```

#### landingpad

```text
       count  opcode%   total%  types
         521   81.41%    0.31%  { ptr, i32 } <- [-]
         119   18.59%    0.07%  { ptr, i32 } <- [ptr]
```

#### zext

```text
       count  opcode%   total%  types
         242   45.66%    0.15%  i32 <- [i8]
          95   17.92%    0.06%  i32 <- [i1]
          73   13.77%    0.04%  i64 <- [i1]
          61   11.51%    0.04%  i8 <- [i1]
          41    7.74%    0.02%  i64 <- [i32]
          14    2.64%    0.01%  i64 <- [i8]
           4    0.75%    0.00%  i32 <- [i16]
```

#### sub

```text
       count  opcode%   total%  types
         225   64.29%    0.13%  i64 <- [i64,i64]
         125   35.71%    0.07%  i32 <- [i32,i32]
```

#### add

```text
       count  opcode%   total%  types
         158   50.97%    0.09%  i32 <- [i32,i32]
         152   49.03%    0.09%  i64 <- [i64,i64]
```

#### ptrtoint

```text
       count  opcode%   total%  types
         268  100.00%    0.16%  i64 <- [ptr]
```

#### sext

```text
       count  opcode%   total%  types
         224   84.85%    0.13%  i64 <- [i32]
          35   13.26%    0.02%  i32 <- [i16]
           5    1.89%    0.00%  i64 <- [i16]
```

#### mul

```text
       count  opcode%   total%  types
         123   99.19%    0.07%  i64 <- [i64,i64]
           1    0.81%    0.00%  i32 <- [i32,i32]
```

#### sdiv

```text
       count  opcode%   total%  types
         102   99.03%    0.06%  i64 <- [i64,i64]
           1    0.97%    0.00%  i32 <- [i32,i32]
```

#### select

```text
       count  opcode%   total%  types
          60   95.24%    0.04%  i32 <- [i1,i32,i32]
           2    3.17%    0.00%  i64 <- [i1,i64,i64]
           1    1.59%    0.00%  i1 <- [i1,i1,i1]
```

#### inttoptr

```text
       count  opcode%   total%  types
          61  100.00%    0.04%  ptr <- [i64]
```

#### udiv

```text
       count  opcode%   total%  types
          50  100.00%    0.03%  i64 <- [i64,i64]
```

#### trunc

```text
       count  opcode%   total%  types
          16   45.71%    0.01%  i32 <- [i64]
           9   25.71%    0.01%  i8 <- [i32]
           9   25.71%    0.01%  i8 <- [i64]
           1    2.86%    0.00%  i16 <- [i32]
```

#### urem

```text
       count  opcode%   total%  types
          13  100.00%    0.01%  i64 <- [i64,i64]
```

#### xor

```text
       count  opcode%   total%  types
          12  100.00%    0.01%  i1 <- [i1,i1]
```

#### srem

```text
       count  opcode%   total%  types
           8  100.00%    0.00%  i32 <- [i32,i32]
```

#### and

```text
       count  opcode%   total%  types
           4  100.00%    0.00%  i32 <- [i32,i32]
```

#### ashr

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i64 <- [i64,i64]
```

#### fcmp

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i1 <- [double,double]
```

#### or

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i32 <- [i32,i32]
```

### lencod

#### load

```text
       count  opcode%   total%  types
      39,518   51.12%   18.47%  i32 <- [ptr]
      31,538   40.80%   14.74%  ptr <- [ptr]
       3,960    5.12%    1.85%  i16 <- [ptr]
         717    0.93%    0.34%  i8 <- [ptr]
         657    0.85%    0.31%  i64 <- [ptr]
         633    0.82%    0.30%  double <- [ptr]
         276    0.36%    0.13%  float <- [ptr]
```

#### getelementptr

```text
       count  opcode%   total%  types
      16,422   43.49%    7.68%  ptr <- [ptr,i32,i32]
      12,103   32.05%    5.66%  ptr <- [ptr,i64]
       8,796   23.29%    4.11%  ptr <- [ptr,i64,i64]
         443    1.17%    0.21%  ptr <- [ptr,i32]
```

#### br

```text
       count  opcode%   total%  types
      12,733   59.53%    5.95%  void <- [label]
       8,657   40.47%    4.05%  void <- [i1,label,label]
```

#### store

```text
       count  opcode%   total%  types
      14,303   70.18%    6.69%  void <- [i32,ptr]
       2,847   13.97%    1.33%  void <- [ptr,ptr]
       1,786    8.76%    0.83%  void <- [i16,ptr]
         530    2.60%    0.25%  void <- [i8,ptr]
         428    2.10%    0.20%  void <- [double,ptr]
         340    1.67%    0.16%  void <- [i64,ptr]
         147    0.72%    0.07%  void <- [float,ptr]
```

#### sext

```text
       count  opcode%   total%  types
      12,033   82.18%    5.63%  i64 <- [i32]
       1,842   12.58%    0.86%  i32 <- [i16]
         431    2.94%    0.20%  i64 <- [i16]
         291    1.99%    0.14%  i32 <- [i8]
          46    0.31%    0.02%  i16 <- [i8]
```

#### icmp

```text
       count  opcode%   total%  types
       8,424   93.29%    3.94%  i1 <- [i32,i32]
         411    4.55%    0.19%  i1 <- [ptr,ptr]
          73    0.81%    0.03%  i1 <- [i16,i16]
          72    0.80%    0.03%  i1 <- [i64,i64]
          50    0.55%    0.02%  i1 <- [i8,i8]
```

#### add

```text
       count  opcode%   total%  types
       7,592   98.20%    3.55%  i32 <- [i32,i32]
         117    1.51%    0.05%  i64 <- [i64,i64]
          22    0.28%    0.01%  i16 <- [i16,i16]
```

#### alloca

```text
       count  opcode%   total%  types
       5,813  100.00%    2.72%  ptr <- [i32]
```

#### call

```text
       count  opcode%   total%  types
         682   12.54%    0.32%  void <- [ptr,ptr]
         542    9.97%    0.25%  i32 <- [i32,i32,ptr]
         360    6.62%    0.17%  i32 <- [i32,ptr]
         342    6.29%    0.16%  void <- [ptr,ptr,i64,i1,ptr]
         244    4.49%    0.11%  void <- [ptr,i32,ptr]
         230    4.23%    0.11%  void <- [ptr]
         215    3.95%    0.10%  i32 <- [i32,i32,i32,ptr]
         209    3.84%    0.10%  i32 <- [ptr,ptr]
         193    3.55%    0.09%  i32 <- [ptr,ptr,ptr]
         148    2.72%    0.07%  i32 <- [ptr,i32,ptr,ptr]
         137    2.52%    0.06%  void <- [ptr,ptr,ptr]
         122    2.24%    0.06%  void <- [ptr,i16,ptr,ptr]
         119    2.19%    0.06%  ptr <- [i64,i64,ptr]
         100    1.84%    0.05%  void <- [ptr,i8,i64,i1,ptr]
          78    1.43%    0.04%  double <- [double,double,double,ptr]
          73    1.34%    0.03%  void <- [i32,ptr]
          69    1.27%    0.03%  double <- [double,ptr]
          66    1.21%    0.03%  ptr <- [i64,ptr]
          61    1.12%    0.03%  i32 <- [ptr]
          61    1.12%    0.03%  i32 <- [ptr,i32,i32,ptr]
          60    1.10%    0.03%  i32 <- [ptr,ptr,i32,ptr]
          56    1.03%    0.03%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr]
          48    0.88%    0.02%  i32 <- [ptr,i64,ptr,ptr]
          47    0.86%    0.02%  i32 <- [ptr,ptr,ptr,ptr]
          45    0.83%    0.02%  i32 <- [ptr,ptr,i64,ptr]
          43    0.79%    0.02%  i32 <- [ptr,ptr,double,ptr]
          43    0.79%    0.02%  ptr <- [ptr,i32,i32,ptr]
          42    0.77%    0.02%  i32 <- [ptr,i32,i32,i32,ptr]
          41    0.75%    0.02%  void <- [i32,i32,i32,ptr,ptr]
          40    0.74%    0.02%  i32 <- [ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
          39    0.72%    0.02%  void <- [ptr,i32,i32,ptr]
          34    0.63%    0.02%  double <- [ptr,ptr,ptr]
          34    0.63%    0.02%  ptr <- [ptr]
          33    0.61%    0.02%  i32 <- [ptr,i32,ptr]
          27    0.50%    0.01%  void <- [i32,i32,i32,i32,ptr,ptr]
          25    0.46%    0.01%  i32 <- [i32,ptr,i32,ptr,ptr]
          24    0.44%    0.01%  i32 <- [ptr,i32,i32,i32,i32,ptr]
          24    0.44%    0.01%  i64 <- [ptr,ptr]
          24    0.44%    0.01%  void <- [i32,i32,ptr]
          23    0.42%    0.01%  void <- [i32,i32,i32,ptr,ptr,ptr,ptr]
          21    0.39%    0.01%  void <- [i32,i32,ptr,ptr]
          20    0.37%    0.01%  ptr <- [ptr,ptr,ptr]
          19    0.35%    0.01%  void <- [i32,i32,ptr,ptr,ptr]
          18    0.33%    0.01%  i32 <- [ptr,i64,ptr,ptr,ptr]
          16    0.29%    0.01%  ptr <- [i32,ptr]
          16    0.29%    0.01%  void <- [ptr,i16,ptr]
          15    0.28%    0.01%  double <- [double,double,ptr]
          15    0.28%    0.01%  i32 <- [i32,ptr,ptr]
          13    0.24%    0.01%  i32 <- [ptr,i64,ptr,i32,ptr]
          13    0.24%    0.01%  void <- [ptr,ptr,ptr,ptr]
          12    0.22%    0.01%  i32 <- [ptr,ptr,double,double,double,ptr]
          12    0.22%    0.01%  void <- [i32,i32,i32,i32,i32,ptr]
          11    0.20%    0.01%  ptr <- [i32,i32,i32,i32,i32,ptr]
          11    0.20%    0.01%  void <- [ptr,i64,i64,ptr,ptr]
          10    0.18%    0.00%  i32 <- [ptr,ptr,i64,double,ptr]
          10    0.18%    0.00%  void <- [ptr,i32,i32,i32,ptr]
           9    0.17%    0.00%  float <- [float,float,float,ptr]
           9    0.17%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           9    0.17%    0.00%  i64 <- [ptr,i64,i64,ptr,ptr]
           8    0.15%    0.00%  i32 <- [i32,i32,i32,i32,ptr]
           8    0.15%    0.00%  i32 <- [ptr,ptr,double,double,ptr]
           8    0.15%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.15%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           8    0.15%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,i32,ptr]
           8    0.15%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i16,i32,ptr,ptr,ptr,i32,ptr]
           7    0.13%    0.00%  i32 <- [ptr,i32,i32,i32,double,double,double,i32,i32,ptr,i32,ptr]
           7    0.13%    0.00%  i64 <- [i32,ptr,i64,ptr]
           6    0.11%    0.00%  i32 <- [ptr,i64,ptr,i32,i32,ptr]
           6    0.11%    0.00%  i64 <- [i32,i64,i32,ptr]
           6    0.11%    0.00%  ptr <- [ptr,ptr]
           6    0.11%    0.00%  ptr <- [ptr,ptr,i64,ptr]
           6    0.11%    0.00%  void <- [i32,i32,i32,i32,i32,i16,i16,ptr]
           6    0.11%    0.00%  void <- [i32,ptr,i32,ptr,ptr,i32,ptr]
           6    0.11%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,i32,i16,ptr,ptr]
           6    0.11%    0.00%  void <- [i64,i64,ptr]
           6    0.11%    0.00%  void <- [ptr,i32,i32,i32,float,ptr]
           6    0.11%    0.00%  void <- [ptr,i32,i32,i32,ptr,ptr]
           6    0.11%    0.00%  void <- [ptr,i32,i32,ptr,i16,ptr,ptr]
           6    0.11%    0.00%  void <- [ptr,ptr,i32,i32,ptr]
           6    0.11%    0.00%  void <- [ptr,ptr,ptr,i16,i32,i32,i32,i32,i32,ptr]
           6    0.11%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           5    0.09%    0.00%  i32 <- [ptr,i32,i32,i32,i32,double,double,double,i32,i32,ptr,i32,i32,i32,i32,i32,ptr]
           5    0.09%    0.00%  void <- [i64,ptr,ptr]
           5    0.09%    0.00%  void <- [ptr,i32,ptr,ptr]
           4    0.07%    0.00%  double <- [i32,ptr]
           4    0.07%    0.00%  i32 <- [double,ptr,ptr]
           4    0.07%    0.00%  i32 <- [i32,i32,i32,i32,i32,i32,i32,ptr]
           4    0.07%    0.00%  i32 <- [i32,i32,i32,i32,i32,ptr]
           4    0.07%    0.00%  i32 <- [i32,i32,ptr,ptr]
           4    0.07%    0.00%  i32 <- [i32,ptr,i32,ptr]
           4    0.07%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,i32,i32,i32,ptr]
           4    0.07%    0.00%  i32 <- [ptr,i64,i32,ptr]
           4    0.07%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr,ptr]
           4    0.07%    0.00%  i32 <- [ptr,ptr,i32,i16,i32,i32,i16,i16,ptr]
           4    0.07%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
           4    0.07%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr]
           4    0.07%    0.00%  i64 <- [ptr,i64,ptr,ptr,ptr]
           4    0.07%    0.00%  ptr <- [ptr,i32,ptr]
           4    0.07%    0.00%  void <- [i32,i8,i32,i32,i32,i32,i32,ptr]
           4    0.07%    0.00%  void <- [i32,ptr,ptr,i32,ptr]
           4    0.07%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           4    0.07%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,i32,i32,i32,ptr]
           3    0.06%    0.00%  i32 <- [i32,i32,ptr,i32,ptr]
           3    0.06%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,i16,i16,ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           3    0.06%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,i32,i32,i32,i32,ptr]
           3    0.06%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr]
           3    0.06%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,i32,ptr]
           3    0.06%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr]
           3    0.06%    0.00%  void <- [i32,i32,i32,ptr]
           3    0.06%    0.00%  void <- [i32,ptr,ptr]
           3    0.06%    0.00%  void <- [i32,ptr,ptr,ptr]
           3    0.06%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr,ptr]
           3    0.06%    0.00%  void <- [ptr,i32,ptr,i32,ptr]
           3    0.06%    0.00%  void <- [ptr,ptr,i32,i32,i32,ptr]
           3    0.06%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.04%    0.00%  double <- [ptr]
           2    0.04%    0.00%  i16 <- [ptr,ptr,ptr,ptr,i32,i32,i16,ptr,ptr,ptr,ptr]
           2    0.04%    0.00%  i32 <- [double,i32,ptr,ptr,i32,ptr]
           2    0.04%    0.00%  i32 <- [double,ptr]
           2    0.04%    0.00%  i32 <- [i32,double,ptr,ptr]
           2    0.04%    0.00%  i32 <- [i32,i32,i16,i16,i32,ptr]
           2    0.04%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.04%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,i16,i16,ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.04%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.04%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,i32,ptr]
           2    0.04%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr]
           2    0.04%    0.00%  i32 <- [ptr,ptr,i64,i64,i64,i32,ptr]
           2    0.04%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,ptr]
           2    0.04%    0.00%  i64 <- [i64,i64,ptr]
           2    0.04%    0.00%  ptr <- [i32,i32,i32,ptr]
           2    0.04%    0.00%  void <- [i16,i32,i32,i32,i32,ptr,ptr]
           2    0.04%    0.00%  void <- [i16,ptr]
           2    0.04%    0.00%  void <- [i16,ptr,i16,ptr]
           2    0.04%    0.00%  void <- [i32,float,float,float,ptr]
           2    0.04%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i32,ptr]
           2    0.04%    0.00%  void <- [i32,i32,i32,ptr,i32,ptr,ptr]
           2    0.04%    0.00%  void <- [i32,i32,ptr,ptr,ptr,ptr]
           2    0.04%    0.00%  void <- [ptr,i32,i32,i32,i32,i32,ptr]
           2    0.04%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
           2    0.04%    0.00%  void <- [ptr,i32,i32,ptr,i32,i16,i32,i32,ptr]
           2    0.04%    0.00%  void <- [ptr,i32,i32,ptr,ptr]
           2    0.04%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,i32,ptr]
           2    0.04%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,ptr]
           2    0.04%    0.00%  void <- [ptr,ptr,ptr,i16,i32,i32,i32,i32,i32,ptr,ptr]
           2    0.04%    0.00%  void <- [ptr,ptr,ptr,i32,ptr]
           1    0.02%    0.00%  double <- [ptr,i32,i32,double,double,i32,ptr]
           1    0.02%    0.00%  double <- [ptr,i32,i32,i32,double,double,i32,ptr]
           1    0.02%    0.00%  double <- [ptr,ptr,double,i32,i32,i16,i16,i16,ptr]
           1    0.02%    0.00%  i16 <- [i16,ptr]
           1    0.02%    0.00%  i32 <- [double,double,i32,i32,double,ptr]
           1    0.02%    0.00%  i32 <- [float,float,i32,i32,double,ptr]
           1    0.02%    0.00%  i32 <- [i16,i32,i32,i32,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [i32,i32,double,ptr,ptr]
           1    0.02%    0.00%  i32 <- [i32,i32,i16,i16,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [i64,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i16,i32,i32,i32,i32,ptr,ptr,i32,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i16,i32,i32,ptr,ptr,i32,i32,i32,ptr,ptr,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i16,i32,i32,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,double,double,double,i32,i32,ptr,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,i32,double,double,double,i32,i32,ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i64,ptr,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i64,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i64,ptr,i64,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i64,ptr,ptr,double,double,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i64,ptr,ptr,double,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i64,ptr,ptr,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,double,double,i64,double,double,double,i32,double,double,double,i64,i32,double,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,double,double,i64,double,double,double,i32,double,double,double,i64,i64,double,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i64,i64,i64,i64,i32,ptr]
           1    0.02%    0.00%  i8 <- [ptr,i32,i32,ptr]
           1    0.02%    0.00%  void <- [i16,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i16,i32,i32,i32,i32,i32,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i16,i32,i32,ptr,ptr,i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i16,i16,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i16,i16,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,i32,ptr,ptr,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,ptr,i32,ptr]
           1    0.02%    0.00%  void <- [i64,ptr,ptr,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,double,ptr]
           1    0.02%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,i32,ptr,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
```

#### sub

```text
       count  opcode%   total%  types
       2,573   97.80%    1.20%  i32 <- [i32,i32]
          58    2.20%    0.03%  i64 <- [i64,i64]
```

#### zext

```text
       count  opcode%   total%  types
       1,113   49.03%    0.52%  i32 <- [i16]
         438   19.30%    0.20%  i64 <- [i32]
         268   11.81%    0.13%  i32 <- [i1]
         207    9.12%    0.10%  i32 <- [i8]
         207    9.12%    0.10%  i64 <- [i1]
          35    1.54%    0.02%  i64 <- [i16]
           2    0.09%    0.00%  i16 <- [i8]
```

#### mul

```text
       count  opcode%   total%  types
       1,579   91.06%    0.74%  i32 <- [i32,i32]
         155    8.94%    0.07%  i64 <- [i64,i64]
```

#### ashr

```text
       count  opcode%   total%  types
       1,131   99.74%    0.53%  i32 <- [i32,i32]
           3    0.26%    0.00%  i64 <- [i64,i64]
```

#### shl

```text
       count  opcode%   total%  types
       1,046   96.85%    0.49%  i32 <- [i32,i32]
          34    3.15%    0.02%  i64 <- [i64,i64]
```

#### trunc

```text
       count  opcode%   total%  types
         752   75.88%    0.35%  i16 <- [i32]
         162   16.35%    0.08%  i8 <- [i32]
          71    7.16%    0.03%  i32 <- [i64]
           5    0.50%    0.00%  i8 <- [i16]
           1    0.10%    0.00%  i16 <- [i64]
```

#### phi

```text
       count  opcode%   total%  types
         606   64.06%    0.28%  i32 <- [i32,i32]
         172   18.18%    0.08%  i1 <- [i1,i1]
          42    4.44%    0.02%  ptr <- [ptr,ptr]
          37    3.91%    0.02%  i1 <- [i1,i1,i1]
          32    3.38%    0.01%  i1 <- [i1,i1,i1,i1]
          30    3.17%    0.01%  i64 <- [i64,i64]
          23    2.43%    0.01%  double <- [double,double]
           2    0.21%    0.00%  i1 <- [i1,i1,i1,i1,i1]
           2    0.21%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1]
```

#### ret

```text
       count  opcode%   total%  types
         457   55.19%    0.21%  void <- [-]
         330   39.86%    0.15%  void <- [i32]
          26    3.14%    0.01%  void <- [ptr]
          12    1.45%    0.01%  void <- [double]
           1    0.12%    0.00%  void <- [i16]
           1    0.12%    0.00%  void <- [i64]
           1    0.12%    0.00%  void <- [i8]
```

#### sdiv

```text
       count  opcode%   total%  types
         420   97.22%    0.20%  i32 <- [i32,i32]
          12    2.78%    0.01%  i64 <- [i64,i64]
```

#### sitofp

```text
       count  opcode%   total%  types
         172   42.79%    0.08%  double <- [i32]
         119   29.60%    0.06%  float <- [i32]
          69   17.16%    0.03%  float <- [i64]
          40    9.95%    0.02%  double <- [i64]
           2    0.50%    0.00%  float <- [i16]
```

#### and

```text
       count  opcode%   total%  types
         283   93.71%    0.13%  i32 <- [i32,i32]
          19    6.29%    0.01%  i64 <- [i64,i64]
```

#### fdiv

```text
       count  opcode%   total%  types
         110   51.89%    0.05%  double <- [double,double]
         102   48.11%    0.05%  float <- [float,float]
```

#### select

```text
       count  opcode%   total%  types
         172   83.09%    0.08%  i32 <- [i1,i32,i32]
          27   13.04%    0.01%  ptr <- [i1,ptr,ptr]
           6    2.90%    0.00%  double <- [i1,double,double]
           2    0.97%    0.00%  float <- [i1,float,float]
```

#### fmul

```text
       count  opcode%   total%  types
         148   73.27%    0.07%  double <- [double,double]
          54   26.73%    0.03%  float <- [float,float]
```

#### fpext

```text
       count  opcode%   total%  types
         174  100.00%    0.08%  double <- [float]
```

#### or

```text
       count  opcode%   total%  types
         112   79.43%    0.05%  i32 <- [i32,i32]
          29   20.57%    0.01%  i64 <- [i64,i64]
```

#### fadd

```text
       count  opcode%   total%  types
         102   77.86%    0.05%  double <- [double,double]
          29   22.14%    0.01%  float <- [float,float]
```

#### fptosi

```text
       count  opcode%   total%  types
          95   79.17%    0.04%  i32 <- [double]
          24   20.00%    0.01%  i32 <- [float]
           1    0.83%    0.00%  i64 <- [float]
```

#### srem

```text
       count  opcode%   total%  types
         110  100.00%    0.05%  i32 <- [i32,i32]
```

#### fcmp

```text
       count  opcode%   total%  types
          66   82.50%    0.03%  i1 <- [double,double]
          14   17.50%    0.01%  i1 <- [float,float]
```

#### switch

```text
       count  opcode%   total%  types
          19   31.15%    0.01%  void <- [i32,label,label,label,label,label]
          13   21.31%    0.01%  void <- [i32,label,label,label,label]
          10   16.39%    0.00%  void <- [i32,label,label,label]
           5    8.20%    0.00%  void <- [i32,label,label,label,label,label,label,label,label]
           4    6.56%    0.00%  void <- [i32,label,label,label,label,label,label,label]
           3    4.92%    0.00%  void <- [i32,label,label]
           3    4.92%    0.00%  void <- [i32,label,label,label,label,label,label]
           2    3.28%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.64%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
           1    1.64%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
```

#### xor

```text
       count  opcode%   total%  types
          32   52.46%    0.01%  i32 <- [i32,i32]
          28   45.90%    0.01%  i1 <- [i1,i1]
           1    1.64%    0.00%  i64 <- [i64,i64]
```

#### unreachable

```text
       count  opcode%   total%  types
          32  100.00%    0.01%  void <- [-]
```

#### fsub

```text
       count  opcode%   total%  types
          23   76.67%    0.01%  double <- [double,double]
           7   23.33%    0.00%  float <- [float,float]
```

#### uitofp

```text
       count  opcode%   total%  types
           8   33.33%    0.00%  double <- [i16]
           7   29.17%    0.00%  double <- [i32]
           6   25.00%    0.00%  float <- [i64]
           2    8.33%    0.00%  float <- [i32]
           1    4.17%    0.00%  double <- [i64]
```

#### udiv

```text
       count  opcode%   total%  types
          20   90.91%    0.01%  i32 <- [i32,i32]
           2    9.09%    0.00%  i64 <- [i64,i64]
```

#### urem

```text
       count  opcode%   total%  types
          21  100.00%    0.01%  i32 <- [i32,i32]
```

#### fptrunc

```text
       count  opcode%   total%  types
          18  100.00%    0.01%  float <- [double]
```

#### fneg

```text
       count  opcode%   total%  types
          16  100.00%    0.01%  double <- [double]
```

#### lshr

```text
       count  opcode%   total%  types
           8   53.33%    0.00%  i32 <- [i32,i32]
           7   46.67%    0.00%  i64 <- [i64,i64]
```

#### fptoui

```text
       count  opcode%   total%  types
           3  100.00%    0.00%  i64 <- [float]
```

### mafft

#### load

```text
       count  opcode%   total%  types
      18,232   50.27%   17.64%  i32 <- [ptr]
      13,756   37.93%   13.31%  ptr <- [ptr]
       2,371    6.54%    2.29%  float <- [ptr]
       1,013    2.79%    0.98%  double <- [ptr]
         871    2.40%    0.84%  i8 <- [ptr]
          16    0.04%    0.02%  i16 <- [ptr]
          11    0.03%    0.01%  i64 <- [ptr]
```

#### store

```text
       count  opcode%   total%  types
       7,430   50.94%    7.19%  void <- [i32,ptr]
       4,115   28.21%    3.98%  void <- [ptr,ptr]
       1,498   10.27%    1.45%  void <- [float,ptr]
       1,084    7.43%    1.05%  void <- [double,ptr]
         448    3.07%    0.43%  void <- [i8,ptr]
          11    0.08%    0.01%  void <- [i64,ptr]
```

#### br

```text
       count  opcode%   total%  types
       8,339   64.89%    8.07%  void <- [label]
       4,512   35.11%    4.36%  void <- [i1,label,label]
```

#### getelementptr

```text
       count  opcode%   total%  types
       6,636   66.11%    6.42%  ptr <- [ptr,i64]
       1,801   17.94%    1.74%  ptr <- [ptr,i64,i64]
         875    8.72%    0.85%  ptr <- [ptr,i32,i32]
         726    7.23%    0.70%  ptr <- [ptr,i32]
```

#### sext

```text
       count  opcode%   total%  types
       5,987  100.00%    5.79%  i64 <- [i32]
```

#### alloca

```text
       count  opcode%   total%  types
       5,026  100.00%    4.86%  ptr <- [i32]
```

#### icmp

```text
       count  opcode%   total%  types
       4,045   91.76%    3.91%  i1 <- [i32,i32]
         298    6.76%    0.29%  i1 <- [ptr,ptr]
          44    1.00%    0.04%  i1 <- [i8,i8]
          21    0.48%    0.02%  i1 <- [i64,i64]
```

#### call

```text
       count  opcode%   total%  types
         752   19.00%    0.73%  void <- [ptr,ptr]
         444   11.22%    0.43%  ptr <- [i32,ptr]
         268    6.77%    0.26%  ptr <- [i32,i32,ptr]
         231    5.84%    0.22%  i32 <- [ptr,ptr,ptr]
         207    5.23%    0.20%  i64 <- [ptr,ptr]
         167    4.22%    0.16%  ptr <- [ptr,ptr,ptr]
         157    3.97%    0.15%  i32 <- [ptr,ptr]
         149    3.76%    0.14%  double <- [double,double,double,ptr]
         112    2.83%    0.11%  ptr <- [ptr,i32,ptr,ptr]
          98    2.48%    0.09%  void <- [ptr,i32,ptr,ptr,i32,ptr]
          95    2.40%    0.09%  void <- [i32,ptr]
          92    2.32%    0.09%  i32 <- [ptr,ptr,i32,ptr]
          91    2.30%    0.09%  i32 <- [ptr,ptr,i64,ptr]
          89    2.25%    0.09%  ptr <- [i64,i64,ptr]
          74    1.87%    0.07%  float <- [float,float,float,ptr]
          61    1.54%    0.06%  i32 <- [ptr,ptr,i32,i32,ptr]
          51    1.29%    0.05%  i32 <- [ptr,ptr,ptr,ptr]
          48    1.21%    0.05%  void <- [ptr,ptr,ptr,i32,i32,ptr,ptr,i32,ptr]
          43    1.09%    0.04%  void <- [ptr,ptr,ptr,i32,i32,ptr]
          41    1.04%    0.04%  i32 <- [ptr,ptr,double,ptr]
          40    1.01%    0.04%  void <- [ptr,i32,ptr,ptr,i32,ptr,ptr,ptr]
          28    0.71%    0.03%  void <- [ptr,i32,ptr,ptr,i32,ptr,ptr]
          28    0.71%    0.03%  void <- [ptr,ptr,ptr,ptr]
          27    0.68%    0.03%  void <- [ptr,ptr,i64,i1,ptr]
          23    0.58%    0.02%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
          22    0.56%    0.02%  i32 <- [ptr,ptr,i32,ptr,ptr]
          18    0.45%    0.02%  ptr <- [ptr,i64,ptr]
          18    0.45%    0.02%  ptr <- [ptr,ptr,i64,ptr]
          17    0.43%    0.02%  double <- [ptr,ptr]
          17    0.43%    0.02%  ptr <- [ptr]
          17    0.43%    0.02%  void <- [i32,ptr,ptr]
          17    0.43%    0.02%  void <- [ptr,i32,ptr]
          16    0.40%    0.02%  ptr <- [ptr,i32,ptr]
          15    0.38%    0.01%  i32 <- [ptr,i32,ptr,ptr]
          14    0.35%    0.01%  ptr <- [i64,ptr]
          12    0.30%    0.01%  i32 <- [i32,ptr,i32,ptr]
          12    0.30%    0.01%  void <- [i32,i32,ptr,ptr]
          12    0.30%    0.01%  void <- [ptr,double,ptr,ptr]
          12    0.30%    0.01%  void <- [ptr,i32,i32,ptr]
          12    0.30%    0.01%  void <- [ptr,ptr,i32,i32,ptr]
          11    0.28%    0.01%  float <- [ptr,ptr,i32,ptr]
          11    0.28%    0.01%  i32 <- [i32,ptr,ptr]
          11    0.28%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
          10    0.25%    0.01%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           9    0.23%    0.01%  void <- [ptr]
           8    0.20%    0.01%  double <- [double,ptr]
           8    0.20%    0.01%  float <- [i32,i32,ptr]
           8    0.20%    0.01%  i32 <- [i32,ptr]
           7    0.18%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr]
           7    0.18%    0.01%  ptr <- [ptr,ptr]
           7    0.18%    0.01%  void <- [i32,ptr,ptr,ptr]
           6    0.15%    0.01%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           6    0.15%    0.01%  i32 <- [double,ptr]
           6    0.15%    0.01%  i32 <- [ptr,ptr,ptr,double,ptr,double,ptr]
           6    0.15%    0.01%  void <- [ptr,i32,i32,i32,ptr,ptr]
           6    0.15%    0.01%  void <- [ptr,i32,i32,ptr,ptr]
           6    0.15%    0.01%  void <- [ptr,ptr,ptr]
           6    0.15%    0.01%  void <- [ptr,ptr,ptr,double,ptr,ptr]
           5    0.13%    0.00%  float <- [ptr,i32,ptr]
           5    0.13%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           4    0.10%    0.00%  double <- [ptr,i32,ptr,i32,ptr]
           4    0.10%    0.00%  float <- [ptr,float,ptr,i32,i32,ptr]
           4    0.10%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr]
           4    0.10%    0.00%  i32 <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.10%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr]
           4    0.10%    0.00%  i32 <- [ptr,ptr,double,double,double,ptr]
           4    0.10%    0.00%  ptr <- [ptr,i32,i32,i32,ptr]
           4    0.10%    0.00%  void <- [i32,i32,i32,ptr,ptr,ptr,ptr,ptr]
           4    0.10%    0.00%  void <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.10%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,i32,ptr]
           4    0.10%    0.00%  void <- [ptr,ptr,double,ptr,ptr]
           4    0.10%    0.00%  void <- [ptr,ptr,i32,ptr]
           4    0.10%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr]
           4    0.10%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           3    0.08%    0.00%  float <- [float,float,ptr]
           3    0.08%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr,ptr,i32,ptr,ptr]
           3    0.08%    0.00%  float <- [ptr,i32,i32,ptr,ptr,i32,ptr]
           3    0.08%    0.00%  float <- [ptr,ptr,i32,ptr,ptr,ptr]
           3    0.08%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           3    0.08%    0.00%  i32 <- [ptr,ptr,i32,double,ptr]
           3    0.08%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,ptr]
           3    0.08%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.08%    0.00%  void <- [i32,ptr,ptr,ptr,ptr]
           3    0.08%    0.00%  void <- [ptr,i32,ptr,ptr]
           3    0.08%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           3    0.08%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           3    0.08%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.05%    0.00%  double <- [double,i32,ptr]
           2    0.05%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           2    0.05%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr,ptr,i32,ptr,ptr,ptr]
           2    0.05%    0.00%  i32 <- [ptr]
           2    0.05%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.05%    0.00%  i32 <- [ptr,ptr,i32,i32,double,ptr]
           2    0.05%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr]
           2    0.05%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.05%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.05%    0.00%  ptr <- [i32,i32,i32,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,i32,i32,i32,i32,double,i32,i32,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,i32,ptr,ptr,ptr]
           2    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr,ptr]
           1    0.03%    0.00%  double <- [double,double,ptr]
           1    0.03%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.03%    0.00%  float <- [i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,i32,i32,ptr,ptr,i32,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,i32,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.03%    0.00%  float <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,double,double,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,double,i32,i32,i32,i32,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,double,i32,i32,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,i32,double,double,double,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,double,i32,i32,i32,i32,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,double,double,double,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,i32,double,double,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,double,double,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,double,double,double,double,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr]
           1    0.03%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,ptr]
           1    0.03%    0.00%  i8 <- [ptr,ptr]
           1    0.03%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.03%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  void <- [ptr,float,ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  void <- [ptr,i32,ptr,ptr,ptr]
           1    0.03%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr]
           1    0.03%    0.00%  void <- [ptr,i64,i64,ptr,ptr]
           1    0.03%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr,i32,ptr]
           1    0.03%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
```

#### add

```text
       count  opcode%   total%  types
       3,557   99.78%    3.44%  i32 <- [i32,i32]
           8    0.22%    0.01%  i64 <- [i64,i64]
```

#### sub

```text
       count  opcode%   total%  types
       1,155   94.13%    1.12%  i32 <- [i32,i32]
          72    5.87%    0.07%  i64 <- [i64,i64]
```

#### zext

```text
       count  opcode%   total%  types
         716   76.33%    0.69%  i32 <- [i8]
         198   21.11%    0.19%  i32 <- [i1]
          16    1.71%    0.02%  i32 <- [i16]
           4    0.43%    0.00%  i64 <- [i1]
           4    0.43%    0.00%  i64 <- [i32]
```

#### fadd

```text
       count  opcode%   total%  types
         401   69.62%    0.39%  float <- [float,float]
         175   30.38%    0.17%  double <- [double,double]
```

#### fmul

```text
       count  opcode%   total%  types
         389   85.49%    0.38%  double <- [double,double]
          66   14.51%    0.06%  float <- [float,float]
```

#### fpext

```text
       count  opcode%   total%  types
         449  100.00%    0.43%  double <- [float]
```

#### sitofp

```text
       count  opcode%   total%  types
         321   73.79%    0.31%  double <- [i32]
         107   24.60%    0.10%  float <- [i32]
           6    1.38%    0.01%  double <- [i64]
           1    0.23%    0.00%  float <- [i64]
```

#### ret

```text
       count  opcode%   total%  types
         235   58.31%    0.23%  void <- [-]
          71   17.62%    0.07%  void <- [float]
          53   13.15%    0.05%  void <- [i32]
          26    6.45%    0.03%  void <- [ptr]
          17    4.22%    0.02%  void <- [double]
           1    0.25%    0.00%  void <- [i8]
```

#### fcmp

```text
       count  opcode%   total%  types
         211   69.41%    0.20%  i1 <- [float,float]
          93   30.59%    0.09%  i1 <- [double,double]
```

#### mul

```text
       count  opcode%   total%  types
         219   86.90%    0.21%  i32 <- [i32,i32]
          33   13.10%    0.03%  i64 <- [i64,i64]
```

#### trunc

```text
       count  opcode%   total%  types
         224   90.69%    0.22%  i32 <- [i64]
          23    9.31%    0.02%  i8 <- [i32]
```

#### fsub

```text
       count  opcode%   total%  types
         211   96.35%    0.20%  double <- [double,double]
           8    3.65%    0.01%  float <- [float,float]
```

#### fptrunc

```text
       count  opcode%   total%  types
         218  100.00%    0.21%  float <- [double]
```

#### phi

```text
       count  opcode%   total%  types
         167   77.67%    0.16%  i32 <- [i32,i32]
          28   13.02%    0.03%  i1 <- [i1,i1]
           8    3.72%    0.01%  double <- [double,double]
           6    2.79%    0.01%  float <- [float,float]
           4    1.86%    0.00%  i1 <- [i1,i1,i1]
           2    0.93%    0.00%  i64 <- [i64,i64]
```

#### xor

```text
       count  opcode%   total%  types
         166  100.00%    0.16%  i1 <- [i1,i1]
```

#### fdiv

```text
       count  opcode%   total%  types
         145   94.77%    0.14%  double <- [double,double]
           8    5.23%    0.01%  float <- [float,float]
```

#### fptosi

```text
       count  opcode%   total%  types
         120   96.00%    0.12%  i32 <- [double]
           3    2.40%    0.00%  i32 <- [float]
           2    1.60%    0.00%  i64 <- [double]
```

#### unreachable

```text
       count  opcode%   total%  types
          99  100.00%    0.10%  void <- [-]
```

#### ptrtoint

```text
       count  opcode%   total%  types
          86  100.00%    0.08%  i64 <- [ptr]
```

#### fneg

```text
       count  opcode%   total%  types
          27   72.97%    0.03%  double <- [double]
          10   27.03%    0.01%  float <- [float]
```

#### sdiv

```text
       count  opcode%   total%  types
          27   93.10%    0.03%  i32 <- [i32,i32]
           2    6.90%    0.00%  i64 <- [i64,i64]
```

#### and

```text
       count  opcode%   total%  types
          17  100.00%    0.02%  i32 <- [i32,i32]
```

#### srem

```text
       count  opcode%   total%  types
          14  100.00%    0.01%  i32 <- [i32,i32]
```

#### switch

```text
       count  opcode%   total%  types
           2   25.00%    0.00%  void <- [i32,label,label]
           2   25.00%    0.00%  void <- [i32,label,label,label,label,label,label]
           1   12.50%    0.00%  void <- [i32,label,label,label]
           1   12.50%    0.00%  void <- [i32,label,label,label,label]
           1   12.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label]
           1   12.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
```

#### select

```text
       count  opcode%   total%  types
           4  100.00%    0.00%  ptr <- [i1,ptr,ptr]
```

#### shl

```text
       count  opcode%   total%  types
           4  100.00%    0.00%  i32 <- [i32,i32]
```

#### ashr

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i32 <- [i32,i32]
```

### SPASS

#### load

```text
       count  opcode%   total%  types
      28,214   72.83%   20.63%  ptr <- [ptr]
      10,015   25.85%    7.32%  i32 <- [ptr]
         284    0.73%    0.21%  i64 <- [ptr]
         168    0.43%    0.12%  i8 <- [ptr]
          58    0.15%    0.04%  i16 <- [ptr]
```

#### call

```text
       count  opcode%   total%  types
       6,705   25.85%    4.90%  ptr <- [ptr,ptr]
       5,146   19.84%    3.76%  i32 <- [ptr,ptr]
       1,948    7.51%    1.42%  void <- [ptr,ptr]
       1,348    5.20%    0.99%  ptr <- [ptr]
       1,265    4.88%    0.92%  ptr <- [ptr,ptr,ptr]
       1,058    4.08%    0.77%  i32 <- [ptr]
         965    3.72%    0.71%  i32 <- [ptr,ptr,ptr]
         914    3.52%    0.67%  i32 <- [i32,ptr]
         898    3.46%    0.66%  void <- [ptr,ptr,ptr]
         692    2.67%    0.51%  ptr <- [ptr,i32,ptr]
         609    2.35%    0.45%  i32 <- [ptr,i32,ptr]
         536    2.07%    0.39%  void <- [ptr,i32,ptr]
         521    2.01%    0.38%  void <- [ptr]
         448    1.73%    0.33%  i32 <- [i32,i32,ptr]
         315    1.21%    0.23%  ptr <- [i32,ptr]
         280    1.08%    0.20%  void <- [i32,ptr]
         152    0.59%    0.11%  ptr <- [i32,ptr,ptr]
         138    0.53%    0.10%  i32 <- [ptr,ptr,ptr,ptr,ptr]
         133    0.51%    0.10%  i32 <- [ptr,ptr,ptr,ptr]
         108    0.42%    0.08%  void <- [ptr,i32,i32,ptr]
          98    0.38%    0.07%  void <- [ptr,ptr,ptr,ptr]
          96    0.37%    0.07%  i32 <- [i32,ptr,ptr]
          96    0.37%    0.07%  void <- [i32,i32,ptr,i32,i32,i32,ptr]
          93    0.36%    0.07%  ptr <- [ptr,ptr,ptr,ptr]
          85    0.33%    0.06%  void <- [ptr,i32,ptr,ptr]
          81    0.31%    0.06%  ptr <- [ptr,ptr,ptr,ptr,ptr]
          64    0.25%    0.05%  i32 <- [ptr,ptr,i32,ptr]
          59    0.23%    0.04%  void <- [ptr,ptr,ptr,ptr,ptr]
          58    0.22%    0.04%  i32 <- [ptr,ptr,ptr,i32,ptr]
          52    0.20%    0.04%  void <- [i32,i32,ptr]
          51    0.20%    0.04%  void <- [ptr,ptr,i32,ptr]
          47    0.18%    0.03%  i64 <- [ptr,ptr]
          46    0.18%    0.03%  ptr <- [i32,ptr,ptr,ptr]
          45    0.17%    0.03%  i32 <- [ptr,i32,ptr,ptr,ptr]
          45    0.17%    0.03%  ptr <- [ptr,ptr,i32,ptr]
          34    0.13%    0.02%  i16 <- [ptr,ptr]
          34    0.13%    0.02%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr]
          30    0.12%    0.02%  void <- [i32,i8,ptr]
          28    0.11%    0.02%  i32 <- [ptr,i32,i32,ptr]
          24    0.09%    0.02%  void <- [ptr,i16,ptr]
          19    0.07%    0.01%  i32 <- [ptr,i32,i32,ptr,ptr]
          19    0.07%    0.01%  i32 <- [ptr,i32,ptr,ptr]
          16    0.06%    0.01%  i32 <- [ptr,ptr,i32,i32,ptr]
          16    0.06%    0.01%  void <- [i32,ptr,ptr]
          15    0.06%    0.01%  ptr <- [ptr,i32,i32,ptr]
          14    0.05%    0.01%  void <- [ptr,i32,ptr,ptr,ptr]
          14    0.05%    0.01%  void <- [ptr,ptr,i64,i1,ptr]
          13    0.05%    0.01%  i32 <- [i32,i32,i32,ptr]
          12    0.05%    0.01%  i32 <- [i32,ptr,ptr,ptr]
          12    0.05%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
          11    0.04%    0.01%  ptr <- [ptr,ptr,i32,ptr,ptr]
          11    0.04%    0.01%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr]
          11    0.04%    0.01%  ptr <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
          10    0.04%    0.01%  i32 <- [ptr,i32,i32,i32,ptr]
          10    0.04%    0.01%  i32 <- [ptr,ptr,i64,ptr]
          10    0.04%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
          10    0.04%    0.01%  void <- [i32,ptr,i32,ptr]
           9    0.03%    0.01%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.03%    0.01%  i32 <- [ptr,i32,i32,ptr,i32,i32,ptr]
           8    0.03%    0.01%  i32 <- [ptr,i32,i32,ptr,i32,ptr,ptr,ptr]
           8    0.03%    0.01%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr]
           8    0.03%    0.01%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           8    0.03%    0.01%  i64 <- [i32,ptr]
           8    0.03%    0.01%  ptr <- [i32,ptr,ptr,ptr,ptr,ptr]
           8    0.03%    0.01%  ptr <- [ptr,i32,i32,ptr,ptr,ptr]
           8    0.03%    0.01%  ptr <- [ptr,i32,i32,ptr,ptr,ptr,ptr]
           8    0.03%    0.01%  ptr <- [ptr,i32,ptr,ptr]
           8    0.03%    0.01%  void <- [i32,i32,ptr,ptr]
           8    0.03%    0.01%  void <- [i32,i64,ptr]
           7    0.03%    0.01%  i32 <- [ptr,i32,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           7    0.03%    0.01%  ptr <- [ptr,i32,i32,i32,ptr,ptr,ptr]
           7    0.03%    0.01%  void <- [ptr,i32,ptr,i32,ptr]
           7    0.03%    0.01%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr,i32,ptr,i32,ptr]
           6    0.02%    0.00%  float <- [i32,ptr]
           6    0.02%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
           6    0.02%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr]
           6    0.02%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr]
           6    0.02%    0.00%  ptr <- [ptr,i32,ptr,ptr,i32,ptr,ptr,i32,i32,i32,ptr,ptr,ptr]
           6    0.02%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr,ptr]
           6    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,ptr,ptr]
           5    0.02%    0.00%  ptr <- [i32,i32,ptr]
           5    0.02%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr]
           5    0.02%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.02%    0.00%  i32 <- [ptr,i32,ptr,i32,i32,ptr,ptr,ptr]
           4    0.02%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr]
           4    0.02%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr]
           4    0.02%    0.00%  i64 <- [ptr,i64,i64,ptr,ptr]
           4    0.02%    0.00%  ptr <- [i64,ptr]
           4    0.02%    0.00%  ptr <- [ptr,i32,i32,ptr,i32,i32,i32,ptr,ptr,ptr]
           4    0.02%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
           4    0.02%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,ptr]
           4    0.02%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,ptr,ptr,ptr,ptr]
           4    0.02%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,i32,i32,ptr,ptr,ptr]
           3    0.01%    0.00%  i32 <- [i32,ptr,ptr,i32,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,ptr,i32,i32,i32,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i32,i32,ptr,ptr,i32,ptr,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr]
           3    0.01%    0.00%  i64 <- [ptr,ptr,i32,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i32,i32,i32,ptr]
           3    0.01%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,i32,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i32,ptr]
           3    0.01%    0.00%  void <- [i32,ptr,ptr,ptr,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,i32,ptr,i32,ptr,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr,ptr,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  double <- [double,ptr]
           2    0.01%    0.00%  i32 <- [i32,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,i32,ptr,ptr,i32,i32,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,i32,i32,ptr]
           2    0.01%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [i32,i32,i32,ptr]
           2    0.01%    0.00%  ptr <- [i32,ptr,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i16,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i32,ptr,i32,i32,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i32,ptr,i32,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i32,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i32,ptr,ptr,ptr,i32,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,i64,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,i16,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,i64,i64,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,i64,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr,ptr]
           2    0.01%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [i64,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,i64,i64,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i32,i1,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i32 <- [i8,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,i32,i32,i32,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i64,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,ptr]
           1    0.00%    0.00%  i64 <- [ptr]
           1    0.00%    0.00%  ptr <- [i32,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,ptr,i32,ptr,i32,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i32,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,ptr]
           1    0.00%    0.00%  void <- [ptr,i8,i64,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,i16,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
```

#### store

```text
       count  opcode%   total%  types
      12,428   64.51%    9.09%  void <- [ptr,ptr]
       6,545   33.97%    4.79%  void <- [i32,ptr]
         204    1.06%    0.15%  void <- [i64,ptr]
          73    0.38%    0.05%  void <- [i8,ptr]
          14    0.07%    0.01%  void <- [i16,ptr]
           1    0.01%    0.00%  void <- [float,ptr]
```

#### br

```text
       count  opcode%   total%  types
      11,199   60.12%    8.19%  void <- [label]
       7,428   39.88%    5.43%  void <- [i1,label,label]
```

#### alloca

```text
       count  opcode%   total%  types
      11,380   99.96%    8.32%  ptr <- [i32]
           4    0.04%    0.00%  ptr <- [i64]
```

#### icmp

```text
       count  opcode%   total%  types
       7,051   88.75%    5.16%  i1 <- [i32,i32]
         813   10.23%    0.59%  i1 <- [ptr,ptr]
          77    0.97%    0.06%  i1 <- [i64,i64]
           4    0.05%    0.00%  i1 <- [i8,i8]
```

#### ret

```text
       count  opcode%   total%  types
       1,585   37.11%    1.16%  void <- [i32]
       1,345   31.49%    0.98%  void <- [ptr]
       1,332   31.19%    0.97%  void <- [-]
           6    0.14%    0.00%  void <- [i64]
           2    0.05%    0.00%  void <- [i16]
           1    0.02%    0.00%  void <- [float]
```

#### getelementptr

```text
       count  opcode%   total%  types
       2,664   64.83%    1.95%  ptr <- [ptr,i32,i32]
         895   21.78%    0.65%  ptr <- [ptr,i64]
         498   12.12%    0.36%  ptr <- [ptr,i64,i64]
          52    1.27%    0.04%  ptr <- [ptr,i32]
```

#### add

```text
       count  opcode%   total%  types
       1,255   83.83%    0.92%  i32 <- [i32,i32]
         236   15.76%    0.17%  i64 <- [i64,i64]
           6    0.40%    0.00%  i8 <- [i8,i8]
```

#### zext

```text
       count  opcode%   total%  types
         519   42.82%    0.38%  i64 <- [i32]
         499   41.17%    0.36%  i32 <- [i1]
         125   10.31%    0.09%  i32 <- [i8]
          39    3.22%    0.03%  i32 <- [i16]
          28    2.31%    0.02%  i64 <- [i1]
           2    0.17%    0.00%  i64 <- [i8]
```

#### xor

```text
       count  opcode%   total%  types
         991  100.00%    0.72%  i1 <- [i1,i1]
```

#### sext

```text
       count  opcode%   total%  types
         773   95.55%    0.57%  i64 <- [i32]
          24    2.97%    0.02%  i32 <- [i16]
          10    1.24%    0.01%  i32 <- [i8]
           2    0.25%    0.00%  i64 <- [i16]
```

#### phi

```text
       count  opcode%   total%  types
         340   73.12%    0.25%  i1 <- [i1,i1]
          39    8.39%    0.03%  i32 <- [i32,i32]
          33    7.10%    0.02%  ptr <- [ptr,ptr]
          29    6.24%    0.02%  i1 <- [i1,i1,i1]
          14    3.01%    0.01%  i1 <- [i1,i1,i1,i1]
           7    1.51%    0.01%  i1 <- [i1,i1,i1,i1,i1]
           2    0.43%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1]
           1    0.22%    0.00%  i1 <- [i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1,i1]
```

#### sub

```text
       count  opcode%   total%  types
         357   81.88%    0.26%  i32 <- [i32,i32]
          79   18.12%    0.06%  i64 <- [i64,i64]
```

#### inttoptr

```text
       count  opcode%   total%  types
         221  100.00%    0.16%  ptr <- [i64]
```

#### ptrtoint

```text
       count  opcode%   total%  types
         162   78.64%    0.12%  i32 <- [ptr]
          44   21.36%    0.03%  i64 <- [ptr]
```

#### urem

```text
       count  opcode%   total%  types
         162   97.59%    0.12%  i32 <- [i32,i32]
           4    2.41%    0.00%  i64 <- [i64,i64]
```

#### trunc

```text
       count  opcode%   total%  types
         110   83.33%    0.08%  i32 <- [i64]
          15   11.36%    0.01%  i8 <- [i32]
           7    5.30%    0.01%  i16 <- [i32]
```

#### mul

```text
       count  opcode%   total%  types
          85   85.00%    0.06%  i64 <- [i64,i64]
          15   15.00%    0.01%  i32 <- [i32,i32]
```

#### and

```text
       count  opcode%   total%  types
          53   94.64%    0.04%  i32 <- [i32,i32]
           3    5.36%    0.00%  i64 <- [i64,i64]
```

#### switch

```text
       count  opcode%   total%  types
          14   35.00%    0.01%  void <- [i32,label,label,label]
          14   35.00%    0.01%  void <- [i32,label,label,label,label]
           4   10.00%    0.00%  void <- [i32,label,label,label,label,label]
           2    5.00%    0.00%  void <- [i32,label]
           1    2.50%    0.00%  void <- [i32,label,label,label,label,label,label]
           1    2.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    2.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    2.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    2.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    2.50%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
```

#### unreachable

```text
       count  opcode%   total%  types
          39  100.00%    0.03%  void <- [-]
```

#### or

```text
       count  opcode%   total%  types
          19   65.52%    0.01%  i32 <- [i32,i32]
          10   34.48%    0.01%  i64 <- [i64,i64]
```

#### select

```text
       count  opcode%   total%  types
          21   75.00%    0.02%  i32 <- [i1,i32,i32]
           7   25.00%    0.01%  ptr <- [i1,ptr,ptr]
```

#### ashr

```text
       count  opcode%   total%  types
          20  100.00%    0.01%  i32 <- [i32,i32]
```

#### udiv

```text
       count  opcode%   total%  types
           6   54.55%    0.00%  i64 <- [i64,i64]
           5   45.45%    0.00%  i32 <- [i32,i32]
```

#### sdiv

```text
       count  opcode%   total%  types
           6   75.00%    0.00%  i32 <- [i32,i32]
           2   25.00%    0.00%  i64 <- [i64,i64]
```

#### shl

```text
       count  opcode%   total%  types
           6   75.00%    0.00%  i64 <- [i64,i64]
           2   25.00%    0.00%  i32 <- [i32,i32]
```

#### sitofp

```text
       count  opcode%   total%  types
           6   75.00%    0.00%  float <- [i32]
           2   25.00%    0.00%  double <- [i32]
```

#### fcmp

```text
       count  opcode%   total%  types
           6  100.00%    0.00%  i1 <- [float,float]
```

#### fptoui

```text
       count  opcode%   total%  types
           2  100.00%    0.00%  i32 <- [double]
```

#### srem

```text
       count  opcode%   total%  types
           2  100.00%    0.00%  i32 <- [i32,i32]
```

### sqlite3

#### load

```text
       count  opcode%   total%  types
      24,180   62.49%   21.14%  ptr <- [ptr]
      11,119   28.74%    9.72%  i32 <- [ptr]
       2,070    5.35%    1.81%  i8 <- [ptr]
         602    1.56%    0.53%  i16 <- [ptr]
         518    1.34%    0.45%  i64 <- [ptr]
         165    0.43%    0.14%  double <- [ptr]
          37    0.10%    0.03%  fp128 <- [ptr]
           3    0.01%    0.00%  [2 x i64] <- [ptr]
```

#### br

```text
       count  opcode%   total%  types
       8,712   56.88%    7.62%  void <- [label]
       6,604   43.12%    5.77%  void <- [i1,label,label]
```

#### getelementptr

```text
       count  opcode%   total%  types
      11,618   77.11%   10.16%  ptr <- [ptr,i32,i32]
       2,459   16.32%    2.15%  ptr <- [ptr,i64]
         681    4.52%    0.60%  ptr <- [ptr,i64,i64]
         309    2.05%    0.27%  ptr <- [ptr,i32]
```

#### store

```text
       count  opcode%   total%  types
       6,802   47.61%    5.95%  void <- [i32,ptr]
       5,722   40.05%    5.00%  void <- [ptr,ptr]
       1,035    7.24%    0.91%  void <- [i8,ptr]
         349    2.44%    0.31%  void <- [i64,ptr]
         244    1.71%    0.21%  void <- [i16,ptr]
         109    0.76%    0.10%  void <- [double,ptr]
          25    0.17%    0.02%  void <- [fp128,ptr]
           1    0.01%    0.00%  void <- [[2 x i64],ptr]
```

#### alloca

```text
       count  opcode%   total%  types
       6,852  100.00%    5.99%  ptr <- [i32]
```

#### icmp

```text
       count  opcode%   total%  types
       4,584   66.92%    4.01%  i1 <- [i32,i32]
       1,703   24.86%    1.49%  i1 <- [ptr,ptr]
         411    6.00%    0.36%  i1 <- [i8,i8]
         149    2.18%    0.13%  i1 <- [i64,i64]
           3    0.04%    0.00%  i1 <- [i16,i16]
```

#### call

```text
       count  opcode%   total%  types
         820   12.93%    0.72%  void <- [ptr,ptr]
         656   10.35%    0.57%  i32 <- [ptr,ptr]
         419    6.61%    0.37%  i32 <- [ptr,ptr,ptr]
         326    5.14%    0.29%  i32 <- [ptr,i32,i32,i32,ptr]
         313    4.94%    0.27%  void <- [ptr,i32,ptr]
         205    3.23%    0.18%  i32 <- [ptr,i32,ptr]
         175    2.76%    0.15%  ptr <- [ptr,ptr]
         172    2.71%    0.15%  ptr <- [ptr,ptr,ptr]
         163    2.57%    0.14%  void <- [ptr,ptr,i64,i1,ptr]
         161    2.54%    0.14%  void <- [ptr,ptr,ptr]
         137    2.16%    0.12%  void <- [ptr,ptr,ptr,ptr]
         127    2.00%    0.11%  i64 <- [ptr,ptr]
         121    1.91%    0.11%  i32 <- [ptr,ptr,ptr,ptr]
         120    1.89%    0.10%  i32 <- [ptr,i32,i32,i32,i32,ptr]
         110    1.73%    0.10%  ptr <- [ptr,i32,ptr]
         105    1.66%    0.09%  i32 <- [ptr,ptr,i32,ptr]
          94    1.48%    0.08%  void <- [ptr,i32,i32,ptr]
          83    1.31%    0.07%  ptr <- [i32,ptr]
          78    1.23%    0.07%  i32 <- [ptr,i32,i32,ptr]
          76    1.20%    0.07%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,ptr]
          75    1.18%    0.07%  ptr <- [ptr,ptr,ptr,ptr]
          72    1.14%    0.06%  void <- [ptr,ptr,i32,ptr]
          66    1.04%    0.06%  void <- [ptr,i8,i64,i1,ptr]
          62    0.98%    0.05%  ptr <- [ptr,i32,ptr,ptr,ptr,ptr]
          59    0.93%    0.05%  ptr <- [ptr]
          59    0.93%    0.05%  ptr <- [ptr,ptr,i32,ptr]
          55    0.87%    0.05%  i32 <- [ptr,ptr,i64,ptr]
          53    0.84%    0.05%  i32 <- [ptr,i32,i32,ptr,i32,ptr]
          50    0.79%    0.04%  i32 <- [ptr,i32,ptr,ptr]
          50    0.79%    0.04%  void <- [ptr,ptr,i32,ptr,ptr]
          42    0.66%    0.04%  ptr <- [ptr,ptr,ptr,ptr,ptr]
          40    0.63%    0.03%  i32 <- [i32,ptr]
          40    0.63%    0.03%  i32 <- [ptr,i32,ptr,i32,ptr]
          38    0.60%    0.03%  void <- [ptr,i32,ptr,ptr]
          29    0.46%    0.03%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr]
          29    0.46%    0.03%  void <- [ptr,i32,ptr,i32,ptr]
          28    0.44%    0.02%  i32 <- [ptr,i32,ptr,ptr,ptr]
          26    0.41%    0.02%  void <- [ptr,ptr,i32,i32,ptr]
          22    0.35%    0.02%  i32 <- [ptr,ptr,i32,i64,ptr]
          22    0.35%    0.02%  ptr <- [i32,ptr,ptr,ptr,ptr]
          21    0.33%    0.02%  i32 <- [ptr,ptr,ptr,ptr,ptr]
          21    0.33%    0.02%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr]
          21    0.33%    0.02%  void <- [ptr,i8,ptr]
          19    0.30%    0.02%  i32 <- [i32,ptr,ptr]
          19    0.30%    0.02%  ptr <- [ptr,ptr,i32,ptr,ptr]
          18    0.28%    0.02%  i64 <- [ptr,ptr,ptr]
          18    0.28%    0.02%  ptr <- [i32,ptr,ptr,i32,ptr]
          18    0.28%    0.02%  ptr <- [i32,ptr,ptr,ptr]
          18    0.28%    0.02%  void <- [ptr,ptr,ptr,i32,ptr]
          17    0.27%    0.01%  i32 <- [ptr,ptr,i32,i8,ptr,ptr]
          17    0.27%    0.01%  void <- [ptr]
          15    0.24%    0.01%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr,ptr]
          15    0.24%    0.01%  i32 <- [ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
          15    0.24%    0.01%  ptr <- [ptr,i32,i32,i64,i16,ptr,ptr]
          15    0.24%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr]
          14    0.22%    0.01%  i8 <- [ptr,ptr]
          14    0.22%    0.01%  ptr <- [ptr,ptr,i8,ptr]
          13    0.21%    0.01%  double <- [ptr,ptr]
          13    0.21%    0.01%  ptr <- [ptr,i8,ptr,i32,i32,ptr]
          13    0.21%    0.01%  void <- [i32,ptr]
          12    0.19%    0.01%  i32 <- [ptr,i32,i8,i32,ptr]
          12    0.19%    0.01%  i32 <- [ptr,ptr,i32,ptr,ptr]
          12    0.19%    0.01%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr]
          12    0.19%    0.01%  i32 <- [ptr,ptr,ptr,i32,ptr,ptr]
          12    0.19%    0.01%  ptr <- [i64,ptr]
          12    0.19%    0.01%  ptr <- [ptr,i8,ptr]
          12    0.19%    0.01%  ptr <- [ptr,ptr,i32,i32,i8,i32,ptr]
          12    0.19%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
          11    0.17%    0.01%  i16 <- [ptr,ptr,ptr]
          11    0.17%    0.01%  void <- [ptr,ptr,i32,i32,i32,ptr]
          10    0.16%    0.01%  i32 <- [ptr,ptr,i32,i32,ptr,ptr,ptr]
          10    0.16%    0.01%  i32 <- [ptr,ptr,i64,i32,ptr,ptr]
          10    0.16%    0.01%  ptr <- [ptr,i32,ptr,ptr,ptr]
          10    0.16%    0.01%  void <- [i32,ptr,ptr]
          10    0.16%    0.01%  void <- [ptr,i32,i32,ptr,i32,ptr]
          10    0.16%    0.01%  void <- [ptr,i8,i8,ptr]
          10    0.16%    0.01%  void <- [ptr,ptr,ptr,ptr,i32,ptr]
           9    0.14%    0.01%  double <- [double,double,double,ptr]
           9    0.14%    0.01%  i32 <- [ptr,ptr,i32,i32,ptr]
           9    0.14%    0.01%  i32 <- [ptr,ptr,i32,ptr,ptr,ptr,ptr]
           9    0.14%    0.01%  void <- [ptr,i32,ptr,i8,ptr,ptr]
           9    0.14%    0.01%  void <- [ptr,i32,ptr,ptr,ptr]
           8    0.13%    0.01%  i32 <- [i32,i32,ptr,ptr]
           8    0.13%    0.01%  i32 <- [ptr,i32,i32,ptr,ptr]
           8    0.13%    0.01%  i32 <- [ptr,i64,ptr]
           8    0.13%    0.01%  i32 <- [ptr,i64,ptr,ptr]
           8    0.13%    0.01%  i32 <- [ptr,ptr,ptr,i32,i8,ptr]
           8    0.13%    0.01%  ptr <- [ptr,i64,ptr]
           8    0.13%    0.01%  void <- [i32,i32,ptr]
           8    0.13%    0.01%  void <- [ptr,double,ptr]
           8    0.13%    0.01%  void <- [ptr,i64,ptr]
           7    0.11%    0.01%  i32 <- [ptr,i32,ptr,i32,ptr,ptr]
           7    0.11%    0.01%  void <- [ptr,i32,i8,i32,ptr,ptr]
           6    0.09%    0.01%  i32 <- [i32,i32,i32,ptr]
           6    0.09%    0.01%  i32 <- [ptr,i32,i32,ptr,ptr,ptr,ptr]
           6    0.09%    0.01%  i32 <- [ptr,i32,i8,ptr]
           6    0.09%    0.01%  i32 <- [ptr,i32,ptr,i32,ptr,i32,i32,i32,i32,ptr,ptr,ptr]
           6    0.09%    0.01%  i32 <- [ptr,i8,ptr]
           6    0.09%    0.01%  i64 <- [ptr,i32,ptr]
           6    0.09%    0.01%  void <- [ptr,i32,i32,i8,ptr,ptr]
           5    0.08%    0.00%  i32 <- [ptr,i64,i32,ptr]
           5    0.08%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr]
           5    0.08%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr]
           5    0.08%    0.00%  ptr <- [i32,ptr,ptr,double,ptr]
           5    0.08%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i8,ptr]
           5    0.08%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr]
           5    0.08%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr,ptr]
           5    0.08%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
           5    0.08%    0.00%  void <- [ptr,i32,ptr,i32,i32,ptr]
           5    0.08%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,ptr]
           5    0.08%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr,i32,ptr,i32,i32,ptr,ptr]
           4    0.06%    0.00%  double <- [double,ptr]
           4    0.06%    0.00%  i32 <- [ptr,i32,i32,i32,ptr,ptr]
           4    0.06%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,i8,ptr]
           4    0.06%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr,ptr]
           4    0.06%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr,ptr]
           4    0.06%    0.00%  i32 <- [ptr,ptr,i64,i32,ptr]
           4    0.06%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           4    0.06%    0.00%  i8 <- [ptr,i8,ptr]
           4    0.06%    0.00%  ptr <- [i32,ptr,ptr,i32,ptr,ptr]
           4    0.06%    0.00%  ptr <- [i32,ptr,ptr,i64,ptr]
           4    0.06%    0.00%  ptr <- [ptr,i32,i32,ptr]
           4    0.06%    0.00%  ptr <- [ptr,i32,ptr,i32,ptr]
           4    0.06%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr]
           4    0.06%    0.00%  void <- [ptr,i32,i32,ptr,ptr]
           4    0.06%    0.00%  void <- [ptr,ptr,i32,i32,ptr,i32,i32,i32,i32,ptr]
           4    0.06%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr]
           4    0.06%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
           4    0.06%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr,i32,i32,ptr]
           3    0.05%    0.00%  i32 <- [i64,ptr]
           3    0.05%    0.00%  i32 <- [ptr]
           3    0.05%    0.00%  i32 <- [ptr,i32,i32,ptr,i32,i32,ptr]
           3    0.05%    0.00%  i32 <- [ptr,i32,ptr,i32,ptr,i32,ptr]
           3    0.05%    0.00%  i32 <- [ptr,ptr,i8,i32,i32,ptr]
           3    0.05%    0.00%  i32 <- [ptr,ptr,i8,i8,ptr,ptr]
           3    0.05%    0.00%  i32 <- [ptr,ptr,ptr,i64,ptr,i32,i32,ptr,ptr]
           3    0.05%    0.00%  i64 <- [double,ptr]
           3    0.05%    0.00%  i64 <- [i32,ptr,i64,ptr]
           3    0.05%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr]
           3    0.05%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr,ptr,ptr]
           3    0.05%    0.00%  ptr <- [ptr,ptr,i64,ptr]
           3    0.05%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.05%    0.00%  void <- [ptr,i32,[2 x i64],ptr,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,ptr,i32,ptr,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           3    0.05%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  fp128 <- [fp128,fp128,fp128,ptr]
           2    0.03%    0.00%  i32 <- [i32,i32,ptr]
           2    0.03%    0.00%  i32 <- [i32,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,i32,i32,i32,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,i64,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i64,ptr,i32,ptr]
           2    0.03%    0.00%  i32 <- [ptr,i64,ptr,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i64,ptr,i32,i32,i32,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,i8,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,i32,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i32,i32,ptr,ptr]
           2    0.03%    0.00%  i32 <- [ptr,ptr,ptr,i64,i32,ptr]
           2    0.03%    0.00%  i64 <- [i32,i64,i32,ptr]
           2    0.03%    0.00%  ptr <- [i32,ptr,ptr,i32,i32,i32,ptr]
           2    0.03%    0.00%  ptr <- [ptr,i32,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,i64,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,ptr,i32,ptr,ptr]
           2    0.03%    0.00%  ptr <- [ptr,ptr,ptr,ptr,ptr,i32,ptr]
           2    0.03%    0.00%  void <- [i8,ptr,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,i32,i32,ptr,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,ptr,i32,ptr,ptr,ptr,ptr,ptr]
           2    0.03%    0.00%  void <- [ptr,i32,ptr,ptr,i64,ptr]
           2    0.03%    0.00%  void <- [ptr,ptr,i64,ptr]
           1    0.02%    0.00%  double <- [ptr,ptr,ptr,i64,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  double <- [ptr,ptr,ptr,i64,ptr,ptr,ptr,ptr,ptr]
           1    0.02%    0.00%  i32 <- [i32,i32,ptr,ptr,ptr]
           1    0.02%    0.00%  i32 <- [i32,i64,ptr]
           1    0.02%    0.00%  i32 <- [i32,i8,ptr]
           1    0.02%    0.00%  i32 <- [i32,ptr,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,double,double,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,i32,i32,i32,i32,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.02%    0.00%  i32 <- [ptr,i32,i32,i8,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,i32,i32,i32,ptr]
           1    0.02%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  i64 <- [ptr]
           1    0.02%    0.00%  i8 <- [ptr,ptr,i32,ptr]
           1    0.02%    0.00%  ptr <- [i32,ptr,ptr]
           1    0.02%    0.00%  ptr <- [i32,ptr,ptr,i32,double,ptr]
           1    0.02%    0.00%  ptr <- [i32,ptr,ptr,i32,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  ptr <- [i32,ptr,ptr,i32,i32,ptr]
           1    0.02%    0.00%  ptr <- [i32,ptr,ptr,ptr,i32,ptr]
           1    0.02%    0.00%  ptr <- [i32,ptr,ptr,ptr,ptr,ptr]
           1    0.02%    0.00%  ptr <- [ptr,ptr,i32,i32,ptr,ptr]
           1    0.02%    0.00%  ptr <- [ptr,ptr,ptr,i64,ptr,ptr]
           1    0.02%    0.00%  ptr <- [ptr,ptr,ptr,ptr,i32,ptr]
           1    0.02%    0.00%  void <- [i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,i64,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,i32,ptr,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,i32,i32,ptr,ptr,ptr,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr,i32,ptr,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,i32,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,i32,ptr]
           1    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i32,ptr,ptr]
```

#### zext

```text
       count  opcode%   total%  types
       1,409   60.84%    1.23%  i32 <- [i8]
         490   21.16%    0.43%  i32 <- [i16]
         147    6.35%    0.13%  i32 <- [i1]
         130    5.61%    0.11%  i64 <- [i1]
          77    3.32%    0.07%  i64 <- [i32]
          45    1.94%    0.04%  i64 <- [i8]
          18    0.78%    0.02%  i64 <- [i16]
```

#### sext

```text
       count  opcode%   total%  types
       2,006   95.07%    1.75%  i64 <- [i32]
          72    3.41%    0.06%  i32 <- [i16]
          26    1.23%    0.02%  i32 <- [i8]
           5    0.24%    0.00%  i64 <- [i16]
           1    0.05%    0.00%  i64 <- [i8]
```

#### add

```text
       count  opcode%   total%  types
       1,674   89.76%    1.46%  i32 <- [i32,i32]
         174    9.33%    0.15%  i64 <- [i64,i64]
           9    0.48%    0.01%  i8 <- [i8,i8]
           8    0.43%    0.01%  i16 <- [i16,i16]
```

#### ret

```text
       count  opcode%   total%  types
         519   48.01%    0.45%  void <- [i32]
         390   36.08%    0.34%  void <- [-]
         148   13.69%    0.13%  void <- [ptr]
          11    1.02%    0.01%  void <- [i64]
           7    0.65%    0.01%  void <- [double]
           5    0.46%    0.00%  void <- [i8]
           1    0.09%    0.00%  void <- [i16]
```

#### trunc

```text
       count  opcode%   total%  types
         258   38.86%    0.23%  i8 <- [i32]
         253   38.10%    0.22%  i32 <- [i64]
         142   21.39%    0.12%  i16 <- [i32]
           6    0.90%    0.01%  i8 <- [i64]
           5    0.75%    0.00%  i8 <- [i16]
```

#### and

```text
       count  opcode%   total%  types
         600   96.93%    0.52%  i32 <- [i32,i32]
          19    3.07%    0.02%  i64 <- [i64,i64]
```

#### sub

```text
       count  opcode%   total%  types
         438   86.22%    0.38%  i32 <- [i32,i32]
          70   13.78%    0.06%  i64 <- [i64,i64]
```

#### phi

```text
       count  opcode%   total%  types
         162   48.21%    0.14%  i1 <- [i1,i1]
          78   23.21%    0.07%  i32 <- [i32,i32]
          61   18.15%    0.05%  ptr <- [ptr,ptr]
          20    5.95%    0.02%  i1 <- [i1,i1,i1]
          11    3.27%    0.01%  i64 <- [i64,i64]
           2    0.60%    0.00%  i1 <- [i1,i1,i1,i1]
           1    0.30%    0.00%  double <- [double,double]
           1    0.30%    0.00%  fp128 <- [fp128,fp128]
```

#### or

```text
       count  opcode%   total%  types
         276   93.56%    0.24%  i32 <- [i32,i32]
          19    6.44%    0.02%  i64 <- [i64,i64]
```

#### mul

```text
       count  opcode%   total%  types
         147   64.76%    0.13%  i32 <- [i32,i32]
          80   35.24%    0.07%  i64 <- [i64,i64]
```

#### shl

```text
       count  opcode%   total%  types
         140   93.33%    0.12%  i32 <- [i32,i32]
          10    6.67%    0.01%  i64 <- [i64,i64]
```

#### select

```text
       count  opcode%   total%  types
          88   67.69%    0.08%  i32 <- [i1,i32,i32]
          42   32.31%    0.04%  ptr <- [i1,ptr,ptr]
```

#### lshr

```text
       count  opcode%   total%  types
          95   94.06%    0.08%  i32 <- [i32,i32]
           6    5.94%    0.01%  i64 <- [i64,i64]
```

#### sdiv

```text
       count  opcode%   total%  types
          60   89.55%    0.05%  i32 <- [i32,i32]
           7   10.45%    0.01%  i64 <- [i64,i64]
```

#### ptrtoint

```text
       count  opcode%   total%  types
          62   93.94%    0.05%  i64 <- [ptr]
           4    6.06%    0.00%  i32 <- [ptr]
```

#### switch

```text
       count  opcode%   total%  types
          10   18.87%    0.01%  void <- [i32,label,label,label,label]
           9   16.98%    0.01%  void <- [i32,label,label,label,label,label]
           6   11.32%    0.01%  void <- [i32,label,label,label,label,label,label]
           5    9.43%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label]
           5    9.43%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label]
           4    7.55%    0.00%  void <- [i32,label,label,label]
           3    5.66%    0.00%  void <- [i32,label,label,label,label,label,label,label]
           2    3.77%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
           1    1.89%    0.00%  void <- [i32,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label,label]
```

#### xor

```text
       count  opcode%   total%  types
          22   44.90%    0.02%  i1 <- [i1,i1]
          22   44.90%    0.02%  i32 <- [i32,i32]
           5   10.20%    0.00%  i64 <- [i64,i64]
```

#### sitofp

```text
       count  opcode%   total%  types
          32   66.67%    0.03%  double <- [i32]
          13   27.08%    0.01%  double <- [i64]
           3    6.25%    0.00%  fp128 <- [i32]
```

#### fmul

```text
       count  opcode%   total%  types
          23   63.89%    0.02%  double <- [double,double]
          13   36.11%    0.01%  fp128 <- [fp128,fp128]
```

#### fptosi

```text
       count  opcode%   total%  types
          27   79.41%    0.02%  i32 <- [double]
           6   17.65%    0.01%  i64 <- [double]
           1    2.94%    0.00%  i32 <- [fp128]
```

#### fadd

```text
       count  opcode%   total%  types
          29   93.55%    0.03%  double <- [double,double]
           2    6.45%    0.00%  fp128 <- [fp128,fp128]
```

#### fcmp

```text
       count  opcode%   total%  types
          22   70.97%    0.02%  i1 <- [double,double]
           9   29.03%    0.01%  i1 <- [fp128,fp128]
```

#### ashr

```text
       count  opcode%   total%  types
          23   85.19%    0.02%  i32 <- [i32,i32]
           4   14.81%    0.00%  i64 <- [i64,i64]
```

#### fdiv

```text
       count  opcode%   total%  types
          19   90.48%    0.02%  double <- [double,double]
           2    9.52%    0.00%  fp128 <- [fp128,fp128]
```

#### fsub

```text
       count  opcode%   total%  types
          19   95.00%    0.02%  double <- [double,double]
           1    5.00%    0.00%  fp128 <- [fp128,fp128]
```

#### udiv

```text
       count  opcode%   total%  types
          12   80.00%    0.01%  i32 <- [i32,i32]
           3   20.00%    0.00%  i64 <- [i64,i64]
```

#### srem

```text
       count  opcode%   total%  types
          12   85.71%    0.01%  i32 <- [i32,i32]
           2   14.29%    0.00%  i64 <- [i64,i64]
```

#### urem

```text
       count  opcode%   total%  types
           6   60.00%    0.01%  i64 <- [i64,i64]
           4   40.00%    0.00%  i32 <- [i32,i32]
```

#### unreachable

```text
       count  opcode%   total%  types
           8  100.00%    0.01%  void <- [-]
```

#### fneg

```text
       count  opcode%   total%  types
           4   66.67%    0.00%  double <- [double]
           2   33.33%    0.00%  fp128 <- [fp128]
```

#### inttoptr

```text
       count  opcode%   total%  types
           5  100.00%    0.00%  ptr <- [i64]
```

#### fpext

```text
       count  opcode%   total%  types
           3  100.00%    0.00%  fp128 <- [double]
```

#### uitofp

```text
       count  opcode%   total%  types
           2  100.00%    0.00%  double <- [i32]
```

#### fptoui

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  i64 <- [double]
```

#### fptrunc

```text
       count  opcode%   total%  types
           1  100.00%    0.00%  double <- [fp128]
```

### tramp3d-v4

#### load

```text
       count  opcode%   total%  types
      29,289   79.20%   17.41%  ptr <- [ptr]
       5,065   13.70%    3.01%  i32 <- [ptr]
       1,167    3.16%    0.69%  i64 <- [ptr]
         713    1.93%    0.42%  double <- [ptr]
         572    1.55%    0.34%  i8 <- [ptr]
         126    0.34%    0.07%  i1 <- [ptr]
          50    0.14%    0.03%  [2 x i64] <- [ptr]
```

#### alloca

```text
       count  opcode%   total%  types
      30,983  100.00%   18.41%  ptr <- [i32]
```

#### call

```text
       count  opcode%   total%  types
       5,908   19.15%    3.51%  void <- [ptr,ptr]
       4,677   15.16%    2.78%  ptr <- [ptr,ptr]
       3,995   12.95%    2.37%  void <- [ptr,ptr,ptr]
       2,438    7.90%    1.45%  void <- [ptr,ptr,ptr,ptr]
       1,290    4.18%    0.77%  ptr <- [ptr,ptr,ptr]
       1,195    3.87%    0.71%  i32 <- [ptr,ptr]
       1,101    3.57%    0.65%  ptr <- [ptr,i32,ptr]
         822    2.66%    0.49%  void <- [ptr,ptr,ptr,ptr,ptr]
         789    2.56%    0.47%  i64 <- [ptr,ptr]
         768    2.49%    0.46%  i32 <- [ptr,ptr,ptr]
         660    2.14%    0.39%  void <- [ptr,ptr,i64,i1,ptr]
         515    1.67%    0.31%  i32 <- [ptr,ptr,ptr,ptr]
         508    1.65%    0.30%  ptr <- [ptr,ptr,ptr,ptr]
         444    1.44%    0.26%  void <- [ptr]
         405    1.31%    0.24%  i1 <- [ptr,ptr]
         378    1.23%    0.22%  i1 <- [ptr,i64,ptr]
         311    1.01%    0.18%  void <- [ptr,ptr,ptr,ptr,ptr,ptr]
         299    0.97%    0.18%  void <- [ptr,i64,ptr]
         288    0.93%    0.17%  void <- [ptr,ptr,i32,ptr]
         236    0.76%    0.14%  void <- [ptr,i32,ptr]
         228    0.74%    0.14%  ptr <- [i64,ptr]
         228    0.74%    0.14%  ptr <- [ptr,i64,ptr]
         213    0.69%    0.13%  i1 <- [ptr,ptr,ptr]
         197    0.64%    0.12%  double <- [ptr,ptr,ptr]
         177    0.57%    0.11%  ptr <- [ptr,i32,i32,ptr]
         170    0.55%    0.10%  void <- [ptr,ptr,i64,ptr]
         155    0.50%    0.09%  void <- [ptr,i32,i1,i1,ptr]
         154    0.50%    0.09%  void <- [ptr,i32,i1,ptr]
         144    0.47%    0.09%  ptr <- [ptr,ptr,ptr,ptr,ptr]
         140    0.45%    0.08%  ptr <- [ptr]
         117    0.38%    0.07%  i32 <- [ptr]
          99    0.32%    0.06%  double <- [double,double,double,ptr]
          98    0.32%    0.06%  i32 <- [i32,i32,i64,ptr]
          93    0.30%    0.06%  double <- [ptr,ptr]
          91    0.29%    0.05%  void <- [ptr,ptr,i32,i32,ptr]
          75    0.24%    0.04%  i32 <- [ptr,i32,ptr]
          73    0.24%    0.04%  i64 <- [ptr,ptr,ptr]
          73    0.24%    0.04%  ptr <- [ptr,ptr,i64,ptr]
          72    0.23%    0.04%  void <- [ptr,ptr,ptr,i32,ptr]
          70    0.23%    0.04%  double <- [ptr,ptr,ptr,ptr]
          59    0.19%    0.04%  void <- [ptr,i32,i32,i32,ptr]
          55    0.18%    0.03%  [2 x i64] <- [ptr,i64,ptr]
          55    0.18%    0.03%  void <- [ptr,ptr,i1,ptr]
          51    0.17%    0.03%  void <- [ptr,i64,ptr,ptr]
          48    0.16%    0.03%  i64 <- [ptr,i64,ptr]
          46    0.15%    0.03%  ptr <- [ptr,i1,ptr]
          42    0.14%    0.02%  double <- [double,double,ptr]
          38    0.12%    0.02%  ptr <- [ptr,i64,ptr,ptr]
          34    0.11%    0.02%  i1 <- [ptr,i64,ptr,ptr]
          34    0.11%    0.02%  i64 <- [ptr,ptr,ptr,ptr]
          33    0.11%    0.02%  void <- [ptr,double,ptr]
          32    0.10%    0.02%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          29    0.09%    0.02%  i1 <- [ptr,ptr,ptr,ptr]
          26    0.08%    0.02%  double <- [ptr,i32,i32,i32,ptr]
          26    0.08%    0.02%  void <- [ptr,i64,i1,ptr]
          24    0.08%    0.01%  void <- [ptr,i64,ptr,ptr,ptr]
          23    0.07%    0.01%  i64 <- [ptr,i64,ptr,ptr]
          22    0.07%    0.01%  void <- [ptr,i32,i32,ptr,ptr,ptr]
          22    0.07%    0.01%  void <- [ptr,ptr,ptr,ptr,i64,ptr]
          19    0.06%    0.01%  void <- [ptr,i32,i32,ptr]
          17    0.06%    0.01%  double <- [ptr]
          16    0.05%    0.01%  double <- [double,double,i64,ptr]
          16    0.05%    0.01%  void <- [metadata,ptr]
          14    0.05%    0.01%  double <- [double,ptr]
          14    0.05%    0.01%  void <- [i32,ptr]
          14    0.05%    0.01%  void <- [ptr,i1,ptr]
          13    0.04%    0.01%  void <- [ptr,ptr,i32,i32,i32,ptr]
          12    0.04%    0.01%  i32 <- [i32,i32,ptr]
          12    0.04%    0.01%  i64 <- [ptr]
          12    0.04%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
          11    0.04%    0.01%  double <- [ptr,ptr,ptr,ptr,ptr]
          10    0.03%    0.01%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           9    0.03%    0.01%  [2 x i64] <- [ptr,ptr]
           9    0.03%    0.01%  [2 x i64] <- [ptr,ptr,ptr]
           9    0.03%    0.01%  i64 <- [i64,ptr,ptr]
           9    0.03%    0.01%  i64 <- [ptr,ptr,ptr,ptr,ptr]
           9    0.03%    0.01%  ptr <- [ptr,i64,ptr,ptr,ptr]
           9    0.03%    0.01%  ptr <- [ptr,ptr,ptr,ptr,i64,ptr]
           8    0.03%    0.00%  i1 <- [ptr,i32,ptr]
           8    0.03%    0.00%  i32 <- [ptr,i32,i32,i32,ptr]
           8    0.03%    0.00%  ptr <- [ptr,i32,i32,i32,ptr]
           8    0.03%    0.00%  void <- [i1,ptr]
           8    0.03%    0.00%  void <- [ptr,i64,i64,ptr]
           7    0.02%    0.00%  i32 <- [ptr,ptr,i64,ptr,ptr]
           6    0.02%    0.00%  double <- [ptr,i32,ptr]
           6    0.02%    0.00%  i1 <- [i32,i32,i32,i32,i32,i32,ptr,ptr,ptr,ptr]
           6    0.02%    0.00%  i32 <- [ptr,ptr,i32,ptr]
           6    0.02%    0.00%  i64 <- [i64,ptr]
           6    0.02%    0.00%  void <- [ptr,ptr,ptr,ptr,i32,ptr]
           5    0.02%    0.00%  [2 x i64] <- [[2 x i64],[2 x i64],[2 x i64],ptr]
           5    0.02%    0.00%  [2 x i64] <- [[2 x i64],ptr]
           5    0.02%    0.00%  i1 <- [ptr,ptr,ptr,ptr,ptr]
           5    0.02%    0.00%  i32 <- [i32,ptr]
           5    0.02%    0.00%  void <- [ptr,i64,i32,ptr,ptr]
           4    0.01%    0.00%  i1 <- [double,ptr]
           4    0.01%    0.00%  i1 <- [ptr]
           4    0.01%    0.00%  i32 <- [ptr,ptr,i64,ptr]
           4    0.01%    0.00%  i64 <- [ptr,i32,ptr]
           4    0.01%    0.00%  void <- [double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,double,i1,i1,ptr]
           4    0.01%    0.00%  void <- [ptr,ptr,i32,i1,ptr]
           4    0.01%    0.00%  void <- [ptr,ptr,i32,ptr,ptr]
           4    0.01%    0.00%  void <- [ptr,ptr,ptr,i64,ptr]
           4    0.01%    0.00%  { i64, i1 } <- [i64,i64,ptr]
           3    0.01%    0.00%  double <- [ptr,i32,i32,ptr]
           3    0.01%    0.00%  i1 <- [i32,ptr]
           3    0.01%    0.00%  i1 <- [i32,ptr,i32,ptr,ptr]
           3    0.01%    0.00%  i32 <- [i64,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,double,ptr]
           3    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,i32,ptr,ptr]
           2    0.01%    0.00%  double <- [double,i64,ptr]
           2    0.01%    0.00%  i1 <- [double,i32,ptr]
           2    0.01%    0.00%  i1 <- [ptr,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  i32 <- [ptr,i32,i32,i32,i32,ptr]
           2    0.01%    0.00%  void <- [double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i1,i1,ptr]
           2    0.01%    0.00%  void <- [i1,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [i64,ptr]
           2    0.01%    0.00%  void <- [ptr,i1,i1,ptr,ptr,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,i32,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,i32,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,ptr,ptr,i32,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,i32,ptr,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,i64,i64,i32,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i32,i32,ptr,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,i64,i64,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,i32,i32,i32,ptr]
           2    0.01%    0.00%  void <- [ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  [2 x i64] <- [ptr,[2 x i64],[2 x i64],[2 x i64],ptr]
           1    0.00%    0.00%  [2 x i64] <- [ptr,[2 x i64],ptr]
           1    0.00%    0.00%  double <- [ptr,i64,ptr]
           1    0.00%    0.00%  double <- [ptr,ptr,ptr,ptr,double,i1,ptr]
           1    0.00%    0.00%  i1 <- [double,double,i64,ptr]
           1    0.00%    0.00%  i1 <- [i1,i1,ptr]
           1    0.00%    0.00%  i1 <- [i32,i32,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  i1 <- [i32,ptr,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i1,i1,ptr]
           1    0.00%    0.00%  i1 <- [ptr,i32,i32,ptr]
           1    0.00%    0.00%  i1 <- [ptr,ptr,i1,i1,i1,ptr]
           1    0.00%    0.00%  i32 <- [ptr,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,i32,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,i32,ptr]
           1    0.00%    0.00%  i32 <- [ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  i64 <- [i64,i1,ptr]
           1    0.00%    0.00%  i64 <- [ptr,[2 x i64],ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  i64 <- [ptr,ptr,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,double,ptr]
           1    0.00%    0.00%  ptr <- [ptr,i64,ptr,i64,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,i32,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  ptr <- [ptr,ptr,ptr,i64,ptr]
           1    0.00%    0.00%  void <- [double,ptr,ptr,double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i1,i1,ptr]
           1    0.00%    0.00%  void <- [double,ptr,ptr,ptr,double,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,ptr,i1,double,double,i1,i1,ptr]
           1    0.00%    0.00%  void <- [i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,double,double,ptr]
           1    0.00%    0.00%  void <- [ptr,double,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,i1,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,i32,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,i32,i32,i32,ptr]
           1    0.00%    0.00%  void <- [ptr,i32,ptr,ptr,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i64,i64,i32,ptr,ptr]
           1    0.00%    0.00%  void <- [ptr,i8,i64,i1,ptr]
           1    0.00%    0.00%  void <- [ptr,ptr,double,double,ptr]
```

#### store

```text
       count  opcode%   total%  types
      23,008   79.72%   13.67%  void <- [ptr,ptr]
       3,602   12.48%    2.14%  void <- [i32,ptr]
         870    3.01%    0.52%  void <- [i64,ptr]
         552    1.91%    0.33%  void <- [i8,ptr]
         461    1.60%    0.27%  void <- [double,ptr]
         260    0.90%    0.15%  void <- [i1,ptr]
         108    0.37%    0.06%  void <- [[2 x i64],ptr]
```

#### getelementptr

```text
       count  opcode%   total%  types
      14,147   88.95%    8.41%  ptr <- [ptr,i32,i32]
         764    4.80%    0.45%  ptr <- [ptr,i64]
         721    4.53%    0.43%  ptr <- [ptr,i64,i64]
         260    1.63%    0.15%  ptr <- [ptr,i32]
          12    0.08%    0.01%  ptr <- [ptr,i32,i32,i32]
```

#### ret

```text
       count  opcode%   total%  types
       5,336   55.71%    3.17%  void <- [-]
       2,352   24.56%    1.40%  void <- [ptr]
       1,064   11.11%    0.63%  void <- [i32]
         363    3.79%    0.22%  void <- [i64]
         279    2.91%    0.17%  void <- [i1]
         159    1.66%    0.09%  void <- [double]
          25    0.26%    0.01%  void <- [[2 x i64]]
```

#### br

```text
       count  opcode%   total%  types
       4,655   60.96%    2.77%  void <- [label]
       2,981   39.04%    1.77%  void <- [i1,label,label]
```

#### icmp

```text
       count  opcode%   total%  types
       1,115   49.75%    0.66%  i1 <- [i32,i32]
         587   26.19%    0.35%  i1 <- [ptr,ptr]
         283   12.63%    0.17%  i1 <- [i64,i64]
         256   11.42%    0.15%  i1 <- [i8,i8]
```

#### add

```text
       count  opcode%   total%  types
         861   90.82%    0.51%  i32 <- [i32,i32]
          87    9.18%    0.05%  i64 <- [i64,i64]
```

#### sext

```text
       count  opcode%   total%  types
         788  100.00%    0.47%  i64 <- [i32]
```

#### ptrtoint

```text
       count  opcode%   total%  types
         533  100.00%    0.32%  i64 <- [ptr]
```

#### inttoptr

```text
       count  opcode%   total%  types
         515  100.00%    0.31%  ptr <- [i64]
```

#### zext

```text
       count  opcode%   total%  types
         301   59.14%    0.18%  i64 <- [i8]
         173   33.99%    0.10%  i8 <- [i1]
          13    2.55%    0.01%  i32 <- [i8]
          12    2.36%    0.01%  i64 <- [i32]
           9    1.77%    0.01%  i64 <- [i1]
           1    0.20%    0.00%  i32 <- [i1]
```

#### sub

```text
       count  opcode%   total%  types
         236   68.21%    0.14%  i64 <- [i64,i64]
         110   31.79%    0.07%  i32 <- [i32,i32]
```

#### trunc

```text
       count  opcode%   total%  types
         166   55.70%    0.10%  i8 <- [i64]
         131   43.96%    0.08%  i32 <- [i64]
           1    0.34%    0.00%  i8 <- [i32]
```

#### mul

```text
       count  opcode%   total%  types
         104   52.26%    0.06%  i32 <- [i32,i32]
          95   47.74%    0.06%  i64 <- [i64,i64]
```

#### sdiv

```text
       count  opcode%   total%  types
         177   91.71%    0.11%  i64 <- [i64,i64]
          16    8.29%    0.01%  i32 <- [i32,i32]
```

#### fmul

```text
       count  opcode%   total%  types
         190  100.00%    0.11%  double <- [double,double]
```

#### phi

```text
       count  opcode%   total%  types
          68   40.48%    0.04%  ptr <- [ptr,ptr]
          49   29.17%    0.03%  i1 <- [i1,i1]
          21   12.50%    0.01%  i64 <- [i64,i64]
          15    8.93%    0.01%  double <- [double,double]
          11    6.55%    0.01%  i32 <- [i32,i32]
           4    2.38%    0.00%  i1 <- [i1,i1,i1]
```

#### fsub

```text
       count  opcode%   total%  types
         123  100.00%    0.07%  double <- [double,double]
```

#### unreachable

```text
       count  opcode%   total%  types
         102  100.00%    0.06%  void <- [-]
```

#### fdiv

```text
       count  opcode%   total%  types
          69  100.00%    0.04%  double <- [double,double]
```

#### fadd

```text
       count  opcode%   total%  types
          45  100.00%    0.03%  double <- [double,double]
```

#### fcmp

```text
       count  opcode%   total%  types
          39  100.00%    0.02%  i1 <- [double,double]
```

#### and

```text
       count  opcode%   total%  types
          17   54.84%    0.01%  i8 <- [i8,i8]
           9   29.03%    0.01%  i32 <- [i32,i32]
           5   16.13%    0.00%  i64 <- [i64,i64]
```

#### udiv

```text
       count  opcode%   total%  types
          25  100.00%    0.01%  i64 <- [i64,i64]
```

#### xor

```text
       count  opcode%   total%  types
          19   82.61%    0.01%  i1 <- [i1,i1]
           3   13.04%    0.00%  i32 <- [i32,i32]
           1    4.35%    0.00%  i64 <- [i64,i64]
```

#### fneg

```text
       count  opcode%   total%  types
          20  100.00%    0.01%  double <- [double]
```

#### sitofp

```text
       count  opcode%   total%  types
          11   68.75%    0.01%  double <- [i32]
           5   31.25%    0.00%  double <- [i64]
```

#### select

```text
       count  opcode%   total%  types
           6   46.15%    0.00%  i32 <- [i1,i32,i32]
           4   30.77%    0.00%  i64 <- [i1,i64,i64]
           2   15.38%    0.00%  i1 <- [i1,i1,i1]
           1    7.69%    0.00%  ptr <- [i1,ptr,ptr]
```

#### srem

```text
       count  opcode%   total%  types
           8   80.00%    0.00%  i32 <- [i32,i32]
           2   20.00%    0.00%  i64 <- [i64,i64]
```

#### extractvalue

```text
       count  opcode%   total%  types
           4   50.00%    0.00%  i1 <- [{ i64, i1 }]
           4   50.00%    0.00%  i64 <- [{ i64, i1 }]
```

#### shl

```text
       count  opcode%   total%  types
           5   71.43%    0.00%  i32 <- [i32,i32]
           2   28.57%    0.00%  i64 <- [i64,i64]
```

#### or

```text
       count  opcode%   total%  types
           3   75.00%    0.00%  i32 <- [i32,i32]
           1   25.00%    0.00%  i64 <- [i64,i64]
```

#### fptosi

```text
       count  opcode%   total%  types
           2  100.00%    0.00%  i32 <- [double]
```

#### switch

```text
       count  opcode%   total%  types
           1   50.00%    0.00%  void <- [i32,label,label]
           1   50.00%    0.00%  void <- [i32,label,label,label]
```
