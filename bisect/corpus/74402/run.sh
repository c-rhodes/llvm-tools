#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2

exec bash "$link_sh" --and-run llc \
  "$testcase" \
  -mtriple=aarch64-none-linux-gnu \
  -mattr=-fp-armv8 \
  -o -
