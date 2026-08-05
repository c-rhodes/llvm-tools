#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run llc "$testcase" -mtriple=aarch64 -O2 -o - | tee "$out"

grep -Eq '^[[:space:]]*(mov|dup)[[:space:]]+d[0-9]+, v[0-9]+(\.d)?\[1\]' "$out"
