# CTMark generic MIR instruction mix

Build: `build-ctmark-gisel-mir-stats`
LLVM revision: `2b105932049c40edf98682b98c48666acad6c3fa`
LLVM release: `llvmorg-23.1.0-rc3` (`7196f931f212`)
CTMark configuration: `aarch64-O0-g`
Target: `aarch64-unknown-linux-gnu`

## Summary

```text
stage                        files generic-instructions
prelegalizer                   632            2,439,014
preregbankselect               632            2,264,048
preinstructionselect           632            2,276,958
```

## Before legalizer

Input to the legalizer, after target pre-legalizer passes.

### Workloads

```text
workload           files generic-instructions
7zip                 212              387,545
Bullet               121              325,865
ClamAV                98              259,543
consumer-typeset      51              303,353
kimwitu++             14              204,516
lencod                55              313,706
mafft                 27              155,529
SPASS                 51              165,378
sqlite3                2              167,531
tramp3d-v4             1              156,048
TOTAL                632            2,439,014
```

### Overall opcode detail

```text
opcode                              count    share
G_LOAD                            493,462   20.23%
G_FRAME_INDEX                     431,287   17.68%
G_CONSTANT                        373,340   15.31%
G_STORE                           274,581   11.26%
G_BR                              204,751    8.39%
G_PTR_ADD                         202,566    8.31%
G_GLOBAL_VALUE                     85,529    3.51%
G_BRCOND                           76,087    3.12%
G_ICMP                             75,599    3.10%
G_SHL                              32,764    1.34%
G_ADD                              32,025    1.31%
G_SEXTLOAD                         29,931    1.23%
G_ZEXTLOAD                         20,961    0.86%
G_INVOKE_REGION_START              12,072    0.49%
G_TRUNC                            10,523    0.43%
G_ZEXT                              7,891    0.32%
G_AND                               6,974    0.29%
G_FCONSTANT                         6,310    0.26%
G_SUB                               6,278    0.26%
G_MUL                               6,152    0.25%
G_PHI                               6,108    0.25%
G_SEXT                              5,925    0.24%
G_PTRTOINT                          5,531    0.23%
G_OR                                3,665    0.15%
G_ANYEXT                            3,404    0.14%
G_FMUL                              3,236    0.13%
G_LSHR                              2,676    0.11%
G_FCMP                              1,827    0.07%
G_FADD                              1,772    0.07%
G_FMA                               1,582    0.06%
G_ASHR                              1,502    0.06%
G_FSUB                              1,221    0.05%
G_SDIV                              1,173    0.05%
G_SITOFP                            1,170    0.05%
G_XOR                               1,154    0.05%
G_FDIV                              1,020    0.04%
G_SELECT                              999    0.04%
G_FNEG                                900    0.04%
G_INTTOPTR                            879    0.04%
G_FPEXT                               775    0.03%
G_MEMCPY                              575    0.02%
G_TRAP                                432    0.02%
G_FPTOSI                              366    0.02%
G_UDIV                                345    0.01%
G_UREM                                310    0.01%
G_SREM                                304    0.01%
G_FPTRUNC                             295    0.01%
G_MEMSET                              213    0.01%
G_MEMMOVE                             107    0.00%
G_UMULO                                84    0.00%
G_BRJT                                 75    0.00%
G_JUMP_TABLE                           75    0.00%
G_FABS                                 55    0.00%
G_UITOFP                               53    0.00%
G_FPTOUI                               34    0.00%
G_FFLOOR                               26    0.00%
G_VASTART                              24    0.00%
G_BUILD_VECTOR                         17    0.00%
G_UADDO                                 7    0.00%
G_DYN_STACKALLOC                        5    0.00%
G_FCEIL                                 2    0.00%
G_IS_FPCLASS                            2    0.00%
G_STACKRESTORE                          2    0.00%
G_STACKSAVE                             2    0.00%
G_ABS                                   1    0.00%
G_CTLZ                                  1    0.00%
TOTAL                           2,439,014  100.00%
```

## Before register-bank selection

Input to register-bank selection, after target preparation passes.

### Workloads

```text
workload           files generic-instructions
7zip                 212              364,328
Bullet               121              308,425
ClamAV                98              241,145
consumer-typeset      51              275,050
kimwitu++             14              181,417
lencod                55              291,841
mafft                 27              141,349
SPASS                 51              154,838
sqlite3                2              156,526
tramp3d-v4             1              149,129
TOTAL                632            2,264,048
```

### Overall opcode detail

```text
opcode                              count    share
G_LOAD                            493,462   21.80%
G_FRAME_INDEX                     386,893   17.09%
G_CONSTANT                        312,678   13.81%
G_STORE                           274,581   12.13%
G_BR                              204,751    9.04%
G_PTR_ADD                         191,068    8.44%
G_BRCOND                           76,087    3.36%
G_ICMP                             75,695    3.34%
G_SHL                              32,764    1.45%
G_ADD                              32,025    1.41%
G_SEXTLOAD                         29,931    1.32%
G_GLOBAL_VALUE                     28,596    1.26%
G_ZEXTLOAD                         20,961    0.93%
G_AND                              15,726    0.69%
G_INVOKE_REGION_START              12,072    0.53%
G_SUB                               6,898    0.30%
G_MUL                               6,850    0.30%
G_PHI                               6,109    0.27%
G_SEXT                              5,871    0.26%
G_ZEXT                              5,754    0.25%
G_PTRTOINT                          5,518    0.24%
G_FCONSTANT                         4,803    0.21%
G_OR                                3,667    0.16%
G_ANYEXT                            3,463    0.15%
G_TRUNC                             3,445    0.15%
G_FMUL                              3,221    0.14%
G_LSHR                              2,676    0.12%
G_FCMP                              1,818    0.08%
G_FADD                              1,768    0.08%
G_FMA                               1,582    0.07%
G_ASHR                              1,502    0.07%
G_SDIV                              1,477    0.07%
G_FSUB                              1,220    0.05%
G_SITOFP                            1,167    0.05%
G_XOR                               1,158    0.05%
G_FDIV                              1,018    0.04%
G_SELECT                            1,000    0.04%
G_FNEG                                898    0.04%
G_INTTOPTR                            858    0.04%
G_FPEXT                               772    0.03%
G_UDIV                                655    0.03%
G_TRAP                                432    0.02%
G_FPTOSI                              365    0.02%
G_FPTRUNC                             294    0.01%
G_UMULH                                84    0.00%
G_BRJT                                 75    0.00%
G_JUMP_TABLE                           75    0.00%
G_FABS                                 55    0.00%
G_UITOFP                               53    0.00%
G_SEXT_INREG                           40    0.00%
G_FPTOUI                               34    0.00%
G_FFLOOR                               26    0.00%
G_VASTART                              24    0.00%
G_BUILD_VECTOR                         10    0.00%
G_UADDO                                 7    0.00%
G_BITCAST                               6    0.00%
G_UNMERGE_VALUES                        4    0.00%
G_MERGE_VALUES                          3    0.00%
G_FCEIL                                 2    0.00%
G_CTLZ                                  1    0.00%
TOTAL                           2,264,048  100.00%
```

## Before instruction selection

Input to instruction selection, after target preparation passes.

### Workloads

```text
workload           files generic-instructions
7zip                 212              366,957
Bullet               121              309,812
ClamAV                98              242,705
consumer-typeset      51              277,888
kimwitu++             14              182,026
lencod                55              293,371
mafft                 27              141,681
SPASS                 51              155,388
sqlite3                2              157,442
tramp3d-v4             1              149,688
TOTAL                632            2,276,958
```

### Overall opcode detail

```text
opcode                              count    share
G_LOAD                            493,462   21.67%
G_FRAME_INDEX                     386,893   16.99%
G_CONSTANT                        315,558   13.86%
G_STORE                           274,581   12.06%
G_BR                              204,751    8.99%
G_PTR_ADD                         191,068    8.39%
G_BRCOND                           76,087    3.34%
G_ICMP                             75,695    3.32%
G_SHL                              32,764    1.44%
G_ADD                              32,025    1.41%
G_SEXTLOAD                         29,931    1.31%
G_GLOBAL_VALUE                     28,596    1.26%
G_ZEXTLOAD                         20,961    0.92%
G_AND                              15,726    0.69%
G_TRUNC                            13,810    0.61%
G_INVOKE_REGION_START              12,072    0.53%
G_SUB                               6,898    0.30%
G_MUL                               6,850    0.30%
G_PHI                               6,109    0.27%
G_ANYEXT                            6,008    0.26%
G_SEXT                              5,871    0.26%
G_ZEXT                              5,754    0.25%
G_PTRTOINT                          5,518    0.24%
G_OR                                3,667    0.16%
G_FMUL                              3,221    0.14%
G_LSHR                              2,676    0.12%
G_FCONSTANT                         1,923    0.08%
G_FCMP                              1,818    0.08%
G_FADD                              1,768    0.08%
G_FMA                               1,582    0.07%
G_ASHR                              1,502    0.07%
G_SDIV                              1,477    0.06%
G_FSUB                              1,220    0.05%
G_SITOFP                            1,167    0.05%
G_XOR                               1,158    0.05%
G_FDIV                              1,018    0.04%
G_SELECT                            1,000    0.04%
G_FNEG                                898    0.04%
G_INTTOPTR                            858    0.04%
G_FPEXT                               772    0.03%
G_UDIV                                655    0.03%
G_TRAP                                432    0.02%
G_FPTOSI                              365    0.02%
G_FPTRUNC                             294    0.01%
G_UMULH                                84    0.00%
G_BRJT                                 75    0.00%
G_JUMP_TABLE                           75    0.00%
G_FABS                                 55    0.00%
G_UITOFP                               53    0.00%
G_SEXT_INREG                           40    0.00%
G_FPTOUI                               34    0.00%
G_FFLOOR                               26    0.00%
G_VASTART                              24    0.00%
G_BUILD_VECTOR                         10    0.00%
G_UADDO                                 7    0.00%
G_BITCAST                               6    0.00%
G_UNMERGE_VALUES                        4    0.00%
G_MERGE_VALUES                          3    0.00%
G_FCEIL                                 2    0.00%
G_CTLZ                                  1    0.00%
TOTAL                           2,276,958  100.00%
```
