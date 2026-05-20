#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
usage: verify.sh [options]

Run the local bisect verification corpus stored in manifest.tsv.

Examples:
  verify.sh --list
  verify.sh
  verify.sh --issue 183747
  verify.sh --issue 183747 --dry-run

Options:
  --manifest PATH       Manifest path. Default: <script-dir>/manifest.tsv
  --bisect PATH         bisect driver. Default: <script-dir>/bisect.sh
  --llvm-checkout PATH  Use this checkout directly for bisect state.
  --llvm-source PATH    Source repo used to create a disposable shared bare
                        checkout when --llvm-checkout is omitted.
                        Default: ~/llvm-project
  --manyclangs PATH     Passed through to bisect.sh
  --elfshaker-data PATH Passed through to bisect.sh
  --log-dir PATH        Parent log directory for selected runs
  --issue ID            Run or list only a specific issue id. May be repeated.
  --list                Print cases and whether they are verified/pending
  --run                 Run full verification bisects. This is the default.
  --dry-run             Smoke-test bound resolution only; do not verify commits.
  -h, --help            Show this help text
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

resolve_self_dir() {
  local self=$1
  if [[ $self != /* ]]; then
    self=$(command -v "$self") || die "unable to resolve script path for $1"
  fi
  cd "$(dirname "$self")" && pwd
}

resolve_path() {
  local path=$1
  local base_dir=$2
  if [[ $path == /* ]]; then
    printf '%s\n' "$path"
  else
    printf '%s/%s\n' "$base_dir" "$path"
  fi
}

ensure_git_checkout() {
  local repo=$1
  git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 \
    || die "not a git checkout: $repo"
}

prepare_llvm_checkout() {
  if [[ -n $LLVM_CHECKOUT ]]; then
    ensure_git_checkout "$LLVM_CHECKOUT"
    return 0
  fi

  ensure_git_checkout "$LLVM_SOURCE"
  LLVM_CHECKOUT=$LOG_DIR_PARENT/llvm-bisect.git
  if [[ -e $LLVM_CHECKOUT ]]; then
    ensure_git_checkout "$LLVM_CHECKOUT"
    return 0
  fi
  git clone --quiet --bare --shared "$LLVM_SOURCE" "$LLVM_CHECKOUT"
}

is_selected_issue() {
  local issue=$1
  if [[ ${#SELECTED_ISSUES[@]} -eq 0 ]]; then
    return 0
  fi
  local selected
  for selected in "${SELECTED_ISSUES[@]}"; do
    if [[ $selected == "$issue" ]]; then
      return 0
    fi
  done
  return 1
}

case_is_runnable() {
  local mode=$1
  local good_ref=$2
  local bad_ref=$3
  local testcase=$4
  local run_script=$5

  [[ $mode == fix ]] || return 1
  [[ -n $good_ref && -n $bad_ref && -n $testcase && -n $run_script ]] || return 1
  [[ -e $testcase && -e $run_script ]] || return 1
  return 0
}

case_is_verified() {
  local mode=$1
  local good_ref=$2
  local bad_ref=$3
  local testcase=$4
  local run_script=$5
  local expected_kind=$6
  local expected_value=$7

  case_is_runnable "$mode" "$good_ref" "$bad_ref" "$testcase" "$run_script" || return 1
  [[ $expected_kind == fixed_commit ]] || return 1
  [[ -n $expected_value ]] || return 1
  return 0
}

field() {
  printf '%s\n' "$1" | cut -f"$2"
}

list_cases() {
  local line issue mode good_ref bad_ref testcase resolved_testcase run_script resolved_run_script expected_kind expected_value notes
  printf 'issue\tmode\tstatus\ttestcase\texpected\tnotes\n'
  while IFS= read -r line; do
    issue=$(field "$line" 1)
    [[ -n $issue && ${issue:0:1} != "#" ]] || continue
    mode=$(field "$line" 2)
    good_ref=$(field "$line" 3)
    bad_ref=$(field "$line" 4)
    testcase=$(field "$line" 5)
    run_script=$(field "$line" 6)
    expected_kind=$(field "$line" 7)
    expected_value=$(field "$line" 8)
    notes=$(field "$line" 9)
    resolved_testcase=$(resolve_path "$testcase" "$MANIFEST_DIR")
    resolved_run_script=$(resolve_path "$run_script" "$MANIFEST_DIR")
    is_selected_issue "$issue" || continue
    if case_is_verified "$mode" "$good_ref" "$bad_ref" "$resolved_testcase" "$resolved_run_script" "$expected_kind" "$expected_value"; then
      printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$issue" "$mode" verified "$testcase" "$expected_value" "$notes"
    elif case_is_runnable "$mode" "$good_ref" "$bad_ref" "$resolved_testcase" "$resolved_run_script"; then
      printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$issue" "$mode" runnable "$testcase" "-" "$notes"
    else
      printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$issue" "$mode" pending "$testcase" "-" "$notes"
    fi
  done <"$MANIFEST"
}

run_case() {
  local issue=$1
  local mode=$2
  local good_ref=$3
  local bad_ref=$4
  local testcase=$5
  local run_script=$6
  local expected_kind=$7
  local expected_value=$8
  local notes=$9
  local -a cmd
  local case_log_dir rc actual_outcome actual_commit actual_subject actual_show resolved_run_script resolved_testcase result_file driver_log

  resolved_testcase=$(resolve_path "$testcase" "$MANIFEST_DIR")
  resolved_run_script=$(resolve_path "$run_script" "$MANIFEST_DIR")

  if ! case_is_runnable "$mode" "$good_ref" "$bad_ref" "$resolved_testcase" "$resolved_run_script"; then
    printf 'skip %s: incomplete case metadata\n' "$issue"
    return 0
  fi
  if ! $DRY_RUN && ! case_is_verified "$mode" "$good_ref" "$bad_ref" "$resolved_testcase" "$resolved_run_script" "$expected_kind" "$expected_value"; then
    printf 'skip %s: no verified expected result yet\n' "$issue"
    return 0
  fi

  cmd=("$BISECT" --good-ref "$good_ref" --bad-ref "$bad_ref" --testcase "$resolved_testcase" --run-script "$resolved_run_script")
  if [[ -n ${LLVM_CHECKOUT:-} ]]; then
    cmd+=(--llvm-checkout "$LLVM_CHECKOUT")
  fi
  if [[ -n ${MANYCLANGS:-} ]]; then
    cmd+=(--manyclangs "$MANYCLANGS")
  fi
  if [[ -n ${ELFSHAKER_DATA:-} ]]; then
    cmd+=(--elfshaker-data "$ELFSHAKER_DATA")
  fi
  case_log_dir=$LOG_DIR_PARENT/$issue
  mkdir -p "$case_log_dir"
  driver_log=$case_log_dir/verify-driver.log
  cmd+=(--log-dir "$case_log_dir")
  if $DRY_RUN; then
    cmd+=(--dry-run)
  fi

  printf '== %s ==\n' "$issue"
  printf 'log: %s\n' "$driver_log"

  set +e
  "${cmd[@]}" 2>&1 | tee "$driver_log" | awk '/^Bisecting: / { print; fflush() }'
  rc=${PIPESTATUS[0]}
  set -e

  if [[ $rc -ne 0 ]]; then
    printf 'FAIL %s: bisect driver exited with %d; see %s\n' "$issue" "$rc" "$driver_log" >&2
    return 1
  fi

  if $DRY_RUN; then
    printf 'PASS %s: dry-run completed\n' "$issue"
    return 0
  fi

  result_file=$case_log_dir/result.txt
  [[ -f $result_file ]] || {
    printf 'FAIL %s: missing result file %s\n' "$issue" "$result_file" >&2
    return 1
  }

  actual_outcome=$(sed -n 's/^outcome=//p' "$result_file")
  actual_commit=$(sed -n 's/^commit=//p' "$result_file")
  actual_subject=$(sed -n 's/^subject=//p' "$result_file")
  actual_show=
  if [[ -n $actual_commit ]]; then
    actual_show=$(git -C "$LLVM_CHECKOUT" show --stat --summary --format=medium --no-patch "$actual_commit" 2>/dev/null || true)
  fi

  if [[ $actual_outcome == "$expected_kind" && $actual_commit == "$expected_value" ]]; then
    if [[ -n $actual_show ]]; then
      printf 'PASS %s: %s %s\n' "$issue" "$actual_outcome" "$actual_commit"
      printf '%s\n' "$actual_show"
    elif [[ -n $actual_subject ]]; then
      printf 'PASS %s: %s %s %s\n' "$issue" "$actual_outcome" "$actual_commit" "$actual_subject"
    else
      printf 'PASS %s: %s %s\n' "$issue" "$actual_outcome" "$actual_commit"
    fi
    return 0
  fi

  if [[ -n $actual_show ]]; then
    printf 'FAIL %s: expected %s %s, got %s %s\n' \
      "$issue" "$expected_kind" "$expected_value" "$actual_outcome" "$actual_commit" >&2
    printf '%s\n' "$actual_show" >&2
  elif [[ -n $actual_subject ]]; then
    printf 'FAIL %s: expected %s %s, got %s %s %s\n' \
      "$issue" "$expected_kind" "$expected_value" "$actual_outcome" "$actual_commit" "$actual_subject" >&2
  else
    printf 'FAIL %s: expected %s %s, got %s %s\n' \
      "$issue" "$expected_kind" "$expected_value" "$actual_outcome" "$actual_commit" >&2
  fi
  return 1
}

SELF_DIR=$(resolve_self_dir "$0")
MANIFEST=$SELF_DIR/manifest.tsv
BISECT=$SELF_DIR/bisect.sh
LLVM_CHECKOUT=
LLVM_SOURCE=${LLVM_SOURCE:-$HOME/llvm-project}
MANYCLANGS=
ELFSHAKER_DATA=
LOG_DIR_PARENT=
DRY_RUN=false
DO_LIST=false
declare -a SELECTED_ISSUES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --manifest)
      MANIFEST=$2
      shift 2
      ;;
    --bisect)
      BISECT=$2
      shift 2
      ;;
    --llvm-checkout)
      LLVM_CHECKOUT=$2
      shift 2
      ;;
    --llvm-source)
      LLVM_SOURCE=$2
      shift 2
      ;;
    --manyclangs)
      MANYCLANGS=$2
      shift 2
      ;;
    --elfshaker-data)
      ELFSHAKER_DATA=$2
      shift 2
      ;;
    --log-dir)
      LOG_DIR_PARENT=$2
      shift 2
      ;;
    --issue)
      SELECTED_ISSUES+=("$2")
      shift 2
      ;;
    --list)
      DO_LIST=true
      shift
      ;;
    --run)
      DRY_RUN=false
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

[[ -f $MANIFEST ]] || die "manifest not found: $MANIFEST"
[[ -x $BISECT ]] || die "bisect driver not executable: $BISECT"
MANIFEST=$(resolve_path "$MANIFEST" "$PWD")
MANIFEST_DIR=$(cd "$(dirname "$MANIFEST")" && pwd)
MANIFEST=$MANIFEST_DIR/$(basename "$MANIFEST")

if $DO_LIST; then
  list_cases
  exit 0
fi

run_count=0
local_failures=0
if [[ -z $LOG_DIR_PARENT ]]; then
  LOG_DIR_PARENT=$(mktemp -d "${TMPDIR:-/tmp}/bisect-cases.XXXXXX")
fi
prepare_llvm_checkout
while IFS= read -r line; do
  issue=$(field "$line" 1)
  [[ -n $issue && ${issue:0:1} != "#" ]] || continue
  mode=$(field "$line" 2)
  good_ref=$(field "$line" 3)
  bad_ref=$(field "$line" 4)
  testcase=$(field "$line" 5)
  run_script=$(field "$line" 6)
  expected_kind=$(field "$line" 7)
  expected_value=$(field "$line" 8)
  notes=$(field "$line" 9)
  is_selected_issue "$issue" || continue
  run_count=$((run_count + 1))
  if ! run_case "$issue" "$mode" "$good_ref" "$bad_ref" "$testcase" "$run_script" "$expected_kind" "$expected_value" "$notes"; then
    local_failures=$((local_failures + 1))
  fi
done <"$MANIFEST"

if [[ $run_count -eq 0 ]]; then
  die "no matching cases"
fi

if [[ $local_failures -ne 0 ]]; then
  die "$local_failures case(s) failed"
fi
