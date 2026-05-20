#!/usr/bin/env bash
set -euo pipefail

link_sh=$1
testcase=$2

exec bash "$link_sh" --and-run llc -mattr=+sve "$testcase" -o -
