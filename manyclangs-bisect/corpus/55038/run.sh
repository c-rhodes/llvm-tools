#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run clang++ -emit-llvm -S -g0 "$testcase" -o - | tee "$out"

# Fixed code emits a vector select. Broken code emits ill-typed and
# instructions with <4 x i8> and <4 x i1> operands.
grep -Eq 'select <4 x i1> .*<4 x i8>' "$out"
! grep -Eq 'and <4 x i8> .*<4 x i1>' "$out"
