#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run clang++ -target aarch64-linux-gnu -Ofast -S "$testcase" -o - | tee "$out"

# Fixed code updates the array pointers directly using post-indexed ld2/st2.
# Broken code recomputes the addresses from base + loop offset each iteration.
! grep -Eq '^[[:space:]]*add[[:space:]]+x1[0-9], x[012], x8$' "$out"
