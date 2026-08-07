#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run clang -target aarch64-linux-gnu -O2 \
  -fglobal-isel -S "$testcase" -o - | tee "$out"

grep -Eq '^[[:space:]]*cset[[:space:]]+w0, ls$' "$out"
! grep -Eq '^[[:space:]]*movk[[:space:]]' "$out"
