#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
out=$(mktemp)
trap 'rm -f "$out"' EXIT

bash "$link_sh" --and-run clang++ -target aarch64-linux-gnu -O3 -S "$testcase" -o - | tee "$out"

grep -Eq '^[[:space:]]*zip1[[:space:]]+v[0-9]+\.4s, v[0-9]+\.4s, v[0-9]+\.4s$' "$out"
