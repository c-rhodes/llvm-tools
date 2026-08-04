#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run llc "$testcase" -march=aarch64 -O0 -o - | tee "$out"

grep -Eq '^[[:space:]]*mov[[:space:]]+w0,' "$out"
