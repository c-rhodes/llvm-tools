#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run llc "$testcase" -mtriple=aarch64 -o - | tee "$out"

grep -Eq '^[[:space:]]*rev16[[:space:]]+w0, w0$' "$out"
! grep -Eq '^[[:space:]]*lsr[[:space:]]+w0, w[0-9]+, #16$' "$out"
