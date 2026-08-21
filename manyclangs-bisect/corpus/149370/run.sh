#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2
tmp_dir=$(mktemp -d)
trap 'rm -rf "${tmp_dir}"' EXIT

bash "${link_sh}" --and-run clang \
  -xc "${testcase}" -E -dM -march=native >"${tmp_dir}/march"
bash "${link_sh}" --and-run clang \
  -xc "${testcase}" -E -dM -mcpu=native >"${tmp_dir}/mcpu"

diff -u "${tmp_dir}/march" "${tmp_dir}/mcpu"
