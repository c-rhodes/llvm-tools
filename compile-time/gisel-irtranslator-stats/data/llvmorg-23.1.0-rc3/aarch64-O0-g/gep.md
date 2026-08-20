# CTMark GlobalISel IRTranslator GEP statistics

Build: `build-ctmark-gisel-irtranslator-stats`
LLVM revision: `20f548fc79e7670ad64cac48fde041ddbfb30906`
Instrumentation: [`6107fc21c4b0`](https://github.com/c-rhodes/llvm-project/commit/6107fc21c4b0c6469b8edee2f9fbf68ac2310bf4)
LLVM release: `llvmorg-23.1.0-rc3` (`7196f931f212fc7c406066b2628a0ff4ea0ee344`)
CTMark configuration: `aarch64-O0-g`
Target: `aarch64-unknown-linux-gnu`

Counts cover `translateGetElementPtr` invocations and can include constant-expression GEPs. Every percentage is the share of all GEP lowerings in the same workload.

The lowering-shape and emitted-`G_PTR_ADD` categories each partition all GEPs and therefore sum to 100%. Scalar single-index i8 GEPs are a subset, so their percentages do not sum to 100%.

## Categories

### Lowering shapes

- `all-zero`: every index is zero; lowering emits a copy of the base pointer.
- `constant-offset-only`: all indices can be folded into a constant byte offset.
- `one-dynamic-unit-stride`: one dynamic sequential index has a byte stride of one.
- `one-dynamic-scaled`: one dynamic sequential index requires scaling.
- `multiple-dynamic`: more than one sequential index is dynamic.

Constant struct indices contribute to the folded byte offset; they are not dynamic sequential indices.

The examples below follow the [LangRef `getelementptr` syntax](https://llvm.org/docs/LangRef.html#getelementptr-instruction). They assume `ptr %base`, `i64 %i`, `i64 %j`, and `i64 %k` inputs.

```llvm
; all-zero
%zero = getelementptr [4 x i32], ptr %base, i64 0, i64 0

; constant-offset-only
%constant = getelementptr [4 x i32], ptr %base, i64 0, i64 3

; constant-offset-only and single-index-i8/constant-index
%i8.constant = getelementptr i8, ptr %base, i64 12

; one-dynamic-unit-stride and single-index-i8/dynamic-index
%i8.dynamic = getelementptr i8, ptr %base, i64 %i

; one-dynamic-scaled
%scaled = getelementptr i32, ptr %base, i64 %i

; multiple-dynamic
%multiple = getelementptr [16 x i32], ptr %base, i64 %i, i64 %j

; one-dynamic-scaled with a constant component
%two.adds = getelementptr [16 x i32], ptr %base, i64 1, i64 %i

; multiple-dynamic with three G_PTR_ADDs
%three.adds = getelementptr [4 x [8 x i32]], ptr %base, i64 %i,
                i64 %j, i64 %k
```

### Scalar single-index i8 GEPs

- `constant-index`: the sole IR index operand is a constant integer.
- `dynamic-index`: the sole IR index operand is not a constant integer.

This category counts only scalar GEPs whose source element type is `i8` and which have exactly one index. `%i8.constant` and `%i8.dynamic` above demonstrate its two values.

### Emitted G_PTR_ADD counts

- `zero`, `one`, and `two`: the exact number of `G_PTR_ADD` instructions emitted for one GEP.
- `three-or-more`: at least three `G_PTR_ADD` instructions are emitted.

These are Machine IR output categories, not separate LangRef forms. For the examples above, `%zero` emits no `G_PTR_ADD`; `%constant`, `%i8.constant`, `%i8.dynamic`, and `%scaled` emit one; and `%multiple` and `%two.adds` emit two. `%three.adds` emits three in the instrumented lowering.

## Overall

### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only            149,886   54.02%
all-zero                         89,805   32.36%
one-dynamic-scaled               30,956   11.16%
one-dynamic-unit-stride           6,831    2.46%
multiple-dynamic                      0    0.00%
TOTAL                           277,478  100.00%
```

### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                    8,978      3.24%
dynamic-index                     5,108      1.84%
```

### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                             187,673     67.64%
zero                             89,805     32.36%
two                                   0      0.00%
three-or-more                         0      0.00%
```

## By workload

### 7zip

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only             25,580   66.49%
all-zero                          8,744   22.73%
one-dynamic-scaled                2,592    6.74%
one-dynamic-unit-stride           1,555    4.04%
multiple-dynamic                      0    0.00%
TOTAL                            38,471  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                    3,748      9.74%
dynamic-index                     1,161      3.02%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                              29,727     77.27%
zero                              8,744     22.73%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### Bullet

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only             25,110   58.20%
all-zero                         15,084   34.96%
one-dynamic-scaled                2,859    6.63%
one-dynamic-unit-stride              90    0.21%
multiple-dynamic                      0    0.00%
TOTAL                            43,143  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                      133      0.31%
dynamic-index                        77      0.18%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                              28,059     65.04%
zero                             15,084     34.96%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### ClamAV

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only             14,758   66.10%
all-zero                          3,752   16.80%
one-dynamic-scaled                1,917    8.59%
one-dynamic-unit-stride           1,901    8.51%
multiple-dynamic                      0    0.00%
TOTAL                            22,328  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                    1,911      8.56%
dynamic-index                     1,650      7.39%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                              18,576     83.20%
zero                              3,752     16.80%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### consumer-typeset

#### Lowering shapes

```text
shape                             count  GEP share
all-zero                         38,554   53.70%
constant-offset-only             28,740   40.03%
one-dynamic-scaled                3,762    5.24%
one-dynamic-unit-stride             733    1.02%
multiple-dynamic                      0    0.00%
TOTAL                            71,789  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                      612      0.85%
dynamic-index                       157      0.22%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
zero                             38,554     53.70%
one                              33,235     46.30%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### kimwitu++

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only             11,156   62.26%
all-zero                          6,163   34.40%
one-dynamic-scaled                  448    2.50%
one-dynamic-unit-stride             150    0.84%
multiple-dynamic                      0    0.00%
TOTAL                            17,917  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                      256      1.43%
dynamic-index                        43      0.24%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                              11,754     65.60%
zero                              6,163     34.40%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### lencod

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only             21,138   54.97%
one-dynamic-scaled               11,689   30.40%
all-zero                          4,755   12.37%
one-dynamic-unit-stride             872    2.27%
multiple-dynamic                      0    0.00%
TOTAL                            38,454  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                      758      1.97%
dynamic-index                       652      1.70%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                              33,699     87.63%
zero                              4,755     12.37%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### mafft

#### Lowering shapes

```text
shape                             count  GEP share
one-dynamic-scaled                5,272   52.40%
constant-offset-only              2,661   26.45%
all-zero                          1,525   15.16%
one-dynamic-unit-stride             603    5.99%
multiple-dynamic                      0    0.00%
TOTAL                            10,061  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
dynamic-index                       558      5.55%
constant-index                      506      5.03%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                               8,536     84.84%
zero                              1,525     15.16%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### SPASS

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only              2,457   59.19%
all-zero                            815   19.63%
one-dynamic-scaled                  740   17.83%
one-dynamic-unit-stride             139    3.35%
multiple-dynamic                      0    0.00%
TOTAL                             4,151  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                      221      5.32%
dynamic-index                       112      2.70%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                               3,336     80.37%
zero                                815     19.63%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### sqlite3

#### Lowering shapes

```text
shape                             count  GEP share
constant-offset-only             10,671   70.73%
all-zero                          2,650   17.56%
one-dynamic-scaled                  981    6.50%
one-dynamic-unit-stride             785    5.20%
multiple-dynamic                      0    0.00%
TOTAL                            15,087  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
dynamic-index                       695      4.61%
constant-index                      626      4.15%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                              12,437     82.44%
zero                              2,650     17.56%
two                                   0      0.00%
three-or-more                         0      0.00%
```

### tramp3d-v4

#### Lowering shapes

```text
shape                             count  GEP share
all-zero                          7,763   48.29%
constant-offset-only              7,615   47.37%
one-dynamic-scaled                  696    4.33%
one-dynamic-unit-stride               3    0.02%
multiple-dynamic                      0    0.00%
TOTAL                            16,077  100.00%
```

#### Scalar single-index i8 GEPs

```text
value                             count  GEP share
constant-index                      207      1.29%
dynamic-index                         3      0.02%
```

#### Emitted G_PTR_ADD counts

```text
value                             count  GEP share
one                               8,314     51.71%
zero                              7,763     48.29%
two                                   0      0.00%
three-or-more                         0      0.00%
```
