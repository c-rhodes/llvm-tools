#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run clang -target aarch64-linux-gnu -Ofast \
  -mcpu=neoverse-v2 -fno-unroll-loops -S "$testcase" -o - | tee "$out"

grep -Eq '^[[:space:]]*fmaxnm[[:space:]]' "$out"
