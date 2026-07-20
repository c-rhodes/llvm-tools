#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2

exec bash "$link_sh" --and-run clang \
  -target aarch64-linux-gnu \
  -march=armv9.2-a \
  -O2 \
  -Xclang -target-feature \
  -Xclang -sve \
  -c "$testcase" \
  -o /dev/null
