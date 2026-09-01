#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2

bash "${link_sh}" --and-run clang \
  -x cl --target=arm-linux-gnueabi -S "${testcase}" -o /dev/null
