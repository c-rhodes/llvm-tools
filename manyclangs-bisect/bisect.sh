#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
usage: bisect.sh --good-ref REF --bad-ref REF [options] [-- <binary> <args...>...]

Automate an LLVM fix bisect using `git bisect --no-checkout` plus manyclangs
snapshots. The script resolves snapshot-backed bounds, validates that the newer
bound is fixed and the older bound is broken, then lets `git bisect run`
classify each midpoint by command exit status.

Examples:
  bisect.sh \
    --good-ref main \
    --bad-ref llvmorg-22.1.5 \
    -- llc ~/llvm-dirty-files/183747.ll -o -

  bisect.sh \
    --good-ref main \
    --bad-ref llvmorg-17.0.6 \
    --testcase ~/llvm-dirty-files/60369.ll \
    --run-script /path/to/run.sh

Options:
  --llvm-checkout PATH   LLVM checkout to bisect. Default: $LLVM_CHECKOUT or ~/llvm-project
  --manyclangs PATH      manyclangs checkout. Default: $MANYCLANGS or ~/manyclangs
  --elfshaker-data PATH  elfshaker data dir. Default: <manyclangs>/elfshaker_data
  --good-ref REF         Requested newer ref. Required.
  --bad-ref REF          Requested older ref. Required.
  --strict-ancestry      Reject divergent refs instead of bisecting the
                         mainline path from their merge-base to --good-ref.
  --pathspec PATH        Pathspec passed to git bisect start. Default: llvm
  --testcase PATH        Optional testcase path passed to --run-script
  --run-script PATH      Optional script run from the manyclangs root as:
                         <run-script> <link_sh> <testcase> <snapshot> <commit>
                         When omitted, the command after -- is executed as:
                         bash link.sh --and-run <binary> <args...>
  --log-dir PATH         Output dir for metadata, per-step logs, and the ledger.
  --dry-run              Resolve and print effective bounds without probing or bisecting
  -h, --help             Show this help text
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

shell_quote() {
  printf '%q' "$1"
}

quote_words() {
  local out=()
  local word
  for word in "$@"; do
    out+=("$(shell_quote "$word")")
  done
  printf '%s' "${out[*]}"
}

resolve_self() {
  local self=$1
  if [[ $self != /* ]]; then
    self=$(command -v "$self") || die "unable to resolve script path for $1"
  fi
  local dir
  dir=$(cd "$(dirname "$self")" && pwd)
  printf '%s/%s\n' "$dir" "$(basename "$self")"
}

make_absolute_path() {
  local path=$1
  if [[ $path == /* ]]; then
    printf '%s\n' "$path"
  else
    printf '%s/%s\n' "$PWD" "$path"
  fi
}

ensure_checkout() {
  git -C "$LLVM_CHECKOUT" rev-parse --git-dir >/dev/null 2>&1 \
    || die "$LLVM_CHECKOUT is not a git checkout"
  [[ -f "$MANYCLANGS/link.sh" ]] || die "$MANYCLANGS does not look like a manyclangs checkout"
  [[ -d "$ELFSHAKER_DATA" ]] || die "elfshaker data dir does not exist: $ELFSHAKER_DATA"
  command -v flock >/dev/null 2>&1 || die "required tool flock not found in PATH"
}

ensure_no_active_bisect() {
  local bisect_log
  bisect_log=$(git -C "$LLVM_CHECKOUT" rev-parse --git-path BISECT_LOG)
  [[ ! -e "$bisect_log" ]] || die "git bisect is already active in $LLVM_CHECKOUT"
}

build_snapshot_table() {
  local list_file=$LOG_DIR/snapshots.list
  local abbrev_file=$LOG_DIR/snapshot-abbrevs.txt
  local object_file=$LOG_DIR/snapshot-objects.txt
  local snapshot_count

  printf '[setup] collecting snapshot inventory...\n'
  ELFSHAKER_DATA="$ELFSHAKER_DATA" elfshaker list >"$list_file"
  [[ -s "$list_file" ]] || die "elfshaker list returned no snapshots"

  awk -F- '{print $NF}' "$list_file" >"$abbrev_file"
  git -C "$LLVM_CHECKOUT" cat-file --batch-check='%(objectname)' <"$abbrev_file" >"$object_file"

  paste "$object_file" "$list_file" | awk '
    $1 ~ /^[0-9a-f]{40}$/ { latest[$1] = $2 }
    END {
      for (commit in latest)
        print commit "\t" latest[commit]
    }
  ' >"$SNAPSHOT_TABLE"

  [[ -s "$SNAPSHOT_TABLE" ]] || die "failed to resolve any snapshot commits against $LLVM_CHECKOUT"
  snapshot_count=$(wc -l <"$SNAPSHOT_TABLE")
  printf '[setup] mapped %s snapshot-backed commits\n' "$snapshot_count"
}

load_snapshot_table() {
  declare -gA SNAPSHOT_FOR_COMMIT=()
  local commit snapshot
  while IFS=$'\t' read -r commit snapshot; do
    SNAPSHOT_FOR_COMMIT["$commit"]=$snapshot
  done <"$SNAPSHOT_TABLE"
}

snapshot_for_commit() {
  local commit=$1
  [[ -n ${SNAPSHOT_FOR_COMMIT[$commit]:-} ]] || return 1
  printf '%s\n' "${SNAPSHOT_FOR_COMMIT[$commit]}"
}

nearest_snapshot_backed_ancestor() {
  local ref=$1
  local commit
  while IFS= read -r commit; do
    if [[ -n ${SNAPSHOT_FOR_COMMIT[$commit]:-} ]]; then
      printf '%s\n' "$commit"
      return 0
    fi
  done < <(git -C "$LLVM_CHECKOUT" rev-list "$ref")
  return 1
}

commit_subject() {
  git -C "$LLVM_CHECKOUT" show -s --format='%s' "$1"
}

commit_date() {
  git -C "$LLVM_CHECKOUT" show -s --format='%cs' "$1"
}

run_test_command() {
  local snapshot=$1
  local commit=$2
  local link_sh=$3
  local target
  local -a target_args

  (
    cd "$MANYCLANGS"
    export LINKSCRIPT_CC="$HOST_CLANG"
    export LINKSCRIPT_CXX="$HOST_CLANGXX"
    export LINKSCRIPT_LLD="$HOST_LLD"
    if [[ -n $RUN_SCRIPT ]]; then
      bash "$RUN_SCRIPT" "$link_sh" "$TESTCASE" "$snapshot" "$commit"
    else
      target=${COMMAND_ARGS[0]}
      target_args=("${COMMAND_ARGS[@]:1}")
      rm -f "bin/$target"
      bash "$link_sh" "$target"
      (
        cd "$INVOCATION_CWD"
        exec "$MANYCLANGS/bin/$target" "${target_args[@]}"
      )
    fi
  )
}

is_infrastructure_failure_log() {
  local log_file=$1

  if grep -Eq "no such file or directory: '([^']+/)?[^']+\\.o'|ld\\.lld(-[0-9]+)?: .*cannot open .*\\.o: No such file or directory|^bash: .*link\\.sh: No such file or directory$" "$log_file"; then
    return 0
  fi

  if grep -q 'link_sh:' "$log_file" \
    && ! grep -q 'Program arguments: bin/' "$log_file" \
    && grep -Eq "ld\\.lld(-[0-9]+)?: error:|clang\\+\\+: .*linker command failed|clang\\+\\+: .*unable to execute command:" "$log_file"; then
    return 0
  fi

  return 1
}

write_metadata() {
  local command_summary
  if [[ -n $RUN_SCRIPT ]]; then
    command_summary=$(quote_words "$RUN_SCRIPT" "$TESTCASE")
  else
    command_summary=$(quote_words "${COMMAND_ARGS[@]}")
  fi

  cat >"$LOG_DIR/run.txt" <<EOF
requested_good_ref=$REQUESTED_GOOD_REF
requested_bad_ref=$REQUESTED_BAD_REF
initial_good_commit=$INITIAL_GOOD_COMMIT
initial_good_snapshot=$INITIAL_GOOD_SNAPSHOT
effective_good_commit=$EFFECTIVE_GOOD_COMMIT
effective_good_snapshot=$EFFECTIVE_GOOD_SNAPSHOT
good_skipped_count=$GOOD_SKIPPED_COUNT
initial_bad_commit=$INITIAL_BAD_COMMIT
initial_bad_snapshot=$INITIAL_BAD_SNAPSHOT
effective_bad_commit=$EFFECTIVE_BAD_COMMIT
effective_bad_snapshot=$EFFECTIVE_BAD_SNAPSHOT
bad_skipped_count=$BAD_SKIPPED_COUNT
effective_bad_anchor=$EFFECTIVE_BAD_ANCHOR
llvm_checkout=$LLVM_CHECKOUT
manyclangs=$MANYCLANGS
elfshaker_data=$ELFSHAKER_DATA
strict_ancestry=$STRICT_ANCESTRY
active_link_sh=$ACTIVE_LINK_SH
pathspec=$PATHSPEC
testcase=$TESTCASE
command=$command_summary
EOF
}

write_result() {
  local outcome=$1
  local commit=${2:-}
  local subject=

  if [[ -n $commit ]]; then
    subject=$(commit_subject "$commit")
  fi

  cat >"$LOG_DIR/result.txt" <<EOF
outcome=$outcome
commit=$commit
subject=$subject
EOF
}

classify_snapshot_commit_unlocked() {
  local commit=$1
  local snapshot=$2
  local log_file=$3
  local label=$4
  local rc status link_sh_to_use

  {
    if [[ -s "$log_file" ]]; then
      printf '\n%s\n\n' '--------------------------------------------------------------------------------'
    fi
    printf 'label: %s\n' "$label"
    printf 'commit: %s\n' "$commit"
    printf 'date: %s\n' "$(commit_date "$commit")"
    printf 'subject: %s\n' "$(commit_subject "$commit")"
    printf 'snapshot: %s\n' "$snapshot"
    printf '\n== extract ==\n'
  } >>"$log_file"

  if ! (
    cd "$MANYCLANGS"
    ELFSHAKER_DATA="$ELFSHAKER_DATA" elfshaker extract --force "$snapshot"
  ) >>"$log_file" 2>&1; then
    {
      printf '\n== result ==\n'
      printf 'status=skip\n'
      printf 'exit_code=125\n'
    } >>"$log_file"
    return 125
  fi

  if [[ -e "$MANYCLANGS/BUILD_FAILED" ]]; then
    {
      printf '\n== build status ==\n'
      printf 'Detected BUILD_FAILED marker in extracted snapshot.\n'
      if [[ -f "$MANYCLANGS/build.log" ]]; then
        printf '\nLast lines of build.log:\n'
        tail -n 40 "$MANYCLANGS/build.log"
      fi
      printf '\n== result ==\n'
      printf 'status=skip\n'
      printf 'exit_code=125\n'
    } >>"$log_file"
    return 125
  fi

  if [[ -f "$MANYCLANGS/link.sh" ]]; then
    link_sh_to_use=$MANYCLANGS/link.sh
  else
    if ! cp "$LINK_SH_SOURCE" "$ACTIVE_LINK_SH" >>"$log_file" 2>&1; then
      {
        printf '\n== result ==\n'
        printf 'status=skip\n'
        printf 'exit_code=125\n'
      } >>"$log_file"
      return 125
    fi
    chmod +x "$ACTIVE_LINK_SH" >>"$log_file" 2>&1 || true
    link_sh_to_use=$ACTIVE_LINK_SH
  fi

  printf '\n== command ==\n' >>"$log_file"
  printf 'link_sh: %s\n' "$link_sh_to_use" >>"$log_file"
  if run_test_command "$snapshot" "$commit" "$link_sh_to_use" >>"$log_file" 2>&1; then
    rc=0
  else
    rc=$?
  fi

  if [[ $rc -ne 0 ]]; then
    if is_infrastructure_failure_log "$log_file"; then
      rc=125
    fi
  fi

  if [[ $rc -eq 0 ]]; then
    status=fixed
  elif [[ $rc -eq 125 ]]; then
    status=skip
  else
    status=broken
  fi

  {
    printf '\n== result ==\n'
    printf 'status=%s\n' "$status"
    printf 'exit_code=%d\n' "$rc"
  } >>"$log_file"

  return "$rc"
}

classify_snapshot_commit() {
  local commit=$1
  local snapshot=$2
  local log_file=$3
  local label=$4

  {
    printf '\n== lock ==\n'
    printf 'lock_file: %s\n' "$LOCK_FILE"
    printf 'waiting for exclusive access to %s\n' "$MANYCLANGS"
  } >>"$log_file"

  (
    flock 9
    printf 'acquired lock\n' >>"$log_file"
    classify_snapshot_commit_unlocked "$commit" "$snapshot" "$log_file" "$label"
  ) 9>"$LOCK_FILE"
}

resolve_effective_bounds() {
  DIVERGENT_REFS=false
  EFFECTIVE_GOOD_COMMIT=$(nearest_snapshot_backed_ancestor "$REQUESTED_GOOD_REF") \
    || die "no snapshot-backed ancestor found for good ref $REQUESTED_GOOD_REF"
  EFFECTIVE_GOOD_SNAPSHOT=$(snapshot_for_commit "$EFFECTIVE_GOOD_COMMIT")
  INITIAL_GOOD_COMMIT=$EFFECTIVE_GOOD_COMMIT
  INITIAL_GOOD_SNAPSHOT=$EFFECTIVE_GOOD_SNAPSHOT

  EFFECTIVE_BAD_ANCHOR=$REQUESTED_BAD_REF
  if ! git -C "$LLVM_CHECKOUT" merge-base --is-ancestor "$EFFECTIVE_BAD_ANCHOR" "$EFFECTIVE_GOOD_COMMIT"; then
    local merge_base
    merge_base=$(git -C "$LLVM_CHECKOUT" merge-base "$REQUESTED_BAD_REF" "$EFFECTIVE_GOOD_COMMIT")
    if $STRICT_ANCESTRY; then
      die "requested refs are divergent; re-run without --strict-ancestry to bisect trunk from merge-base $merge_base to $REQUESTED_GOOD_REF, or choose ancestor/descendant bounds"
    fi
    DIVERGENT_REFS=true
    EFFECTIVE_BAD_ANCHOR=$merge_base
  fi

  EFFECTIVE_BAD_COMMIT=$(nearest_snapshot_backed_ancestor "$EFFECTIVE_BAD_ANCHOR") \
    || die "no snapshot-backed ancestor found for bad ref anchor $EFFECTIVE_BAD_ANCHOR"
  EFFECTIVE_BAD_SNAPSHOT=$(snapshot_for_commit "$EFFECTIVE_BAD_COMMIT")
  INITIAL_BAD_COMMIT=$EFFECTIVE_BAD_COMMIT
  INITIAL_BAD_SNAPSHOT=$EFFECTIVE_BAD_SNAPSHOT
  [[ $EFFECTIVE_GOOD_COMMIT != "$EFFECTIVE_BAD_COMMIT" ]] \
    || die "effective good and bad bounds collapsed to the same snapshot-backed commit: $EFFECTIVE_GOOD_COMMIT"
}

print_effective_bounds() {
  if $DIVERGENT_REFS; then
    cat <<EOF
Divergent refs detected.
Bisecting mainline from merge-base $EFFECTIVE_BAD_ANCHOR to $REQUESTED_GOOD_REF.
This is not a release-to-release bisect.

EOF
  fi
  if [[ $EFFECTIVE_GOOD_COMMIT != "$INITIAL_GOOD_COMMIT" ]]; then
    cat <<EOF
Requested good ref was not directly runnable with the current test command.
Using earlier runnable snapshot-backed ancestor after skipping $GOOD_SKIPPED_COUNT unrunnable snapshot(s):
  initial:  $INITIAL_GOOD_COMMIT ($(commit_date "$INITIAL_GOOD_COMMIT")) $(commit_subject "$INITIAL_GOOD_COMMIT")
  fallback: $EFFECTIVE_GOOD_COMMIT ($(commit_date "$EFFECTIVE_GOOD_COMMIT")) $(commit_subject "$EFFECTIVE_GOOD_COMMIT")

EOF
  fi
  if [[ $EFFECTIVE_BAD_COMMIT != "$INITIAL_BAD_COMMIT" ]]; then
    cat <<EOF
Requested bad bound was not directly runnable with the current test command.
Using earlier runnable snapshot-backed ancestor after skipping $BAD_SKIPPED_COUNT unrunnable snapshot(s):
  initial:  $INITIAL_BAD_COMMIT ($(commit_date "$INITIAL_BAD_COMMIT")) $(commit_subject "$INITIAL_BAD_COMMIT")
  fallback: $EFFECTIVE_BAD_COMMIT ($(commit_date "$EFFECTIVE_BAD_COMMIT")) $(commit_subject "$EFFECTIVE_BAD_COMMIT")

EOF
  fi
  cat <<EOF
Requested good ref: $REQUESTED_GOOD_REF
Effective good:     $EFFECTIVE_GOOD_COMMIT ($(commit_date "$EFFECTIVE_GOOD_COMMIT")) $(commit_subject "$EFFECTIVE_GOOD_COMMIT")
Good snapshot:      $EFFECTIVE_GOOD_SNAPSHOT

Requested bad ref:  $REQUESTED_BAD_REF
Bad anchor:         $EFFECTIVE_BAD_ANCHOR
Effective bad:      $EFFECTIVE_BAD_COMMIT ($(commit_date "$EFFECTIVE_BAD_COMMIT")) $(commit_subject "$EFFECTIVE_BAD_COMMIT")
Bad snapshot:       $EFFECTIVE_BAD_SNAPSHOT

Log dir:            $LOG_DIR
EOF
}

resolve_runnable_bound() {
  local role=$1
  local anchor_ref=$2
  local commit snapshot rc log_file skipped_count

  log_file=$LOG_DIR/probe-$role.log
  : >"$log_file"
  skipped_count=0
  printf '[probe:%s] searching from %s; log: %s\n' "$role" "$anchor_ref" "$log_file"

  while IFS= read -r commit; do
    snapshot=${SNAPSHOT_FOR_COMMIT[$commit]:-}
    [[ -n $snapshot ]] || continue

    printf '[probe:%s] trying %s %s %s\n' \
      "$role" \
      "${commit:0:12}" \
      "$(commit_date "$commit")" \
      "$(commit_subject "$commit")"

    set +e
    classify_snapshot_commit "$commit" "$snapshot" "$log_file" "probe-$role"
    rc=$?
    set -e

    if [[ $rc -eq 125 ]]; then
      skipped_count=$((skipped_count + 1))
      printf '[probe:%s] skip  %s %s\n' "$role" "${commit:0:12}" "$snapshot"
      continue
    fi

    if [[ $rc -eq 0 ]]; then
      printf '[probe:%s] fixed %s %s\n' "$role" "${commit:0:12}" "$snapshot"
    else
      printf '[probe:%s] broken %s %s\n' "$role" "${commit:0:12}" "$snapshot"
    fi

    case "$role" in
      good)
        EFFECTIVE_GOOD_COMMIT=$commit
        EFFECTIVE_GOOD_SNAPSHOT=$snapshot
        GOOD_PROBE_RC=$rc
        GOOD_SKIPPED_COUNT=$skipped_count
        ;;
      bad)
        EFFECTIVE_BAD_COMMIT=$commit
        EFFECTIVE_BAD_SNAPSHOT=$snapshot
        BAD_PROBE_RC=$rc
        BAD_SKIPPED_COUNT=$skipped_count
        ;;
      *)
        die "unknown bound role: $role"
        ;;
    esac
    return 0
  done < <(git -C "$LLVM_CHECKOUT" rev-list "$anchor_ref")

  die "no runnable snapshot-backed ancestor found for $role bound anchor $anchor_ref; see $log_file"
}

next_step_number() {
  local counter_file=$LOG_DIR/step-counter.txt
  local current=1
  if [[ -f "$counter_file" ]]; then
    current=$(<"$counter_file")
  fi
  printf '%03d\n' "$current"
  printf '%d\n' "$((current + 1))" >"$counter_file"
}

run_step_mode() {
  LOG_DIR=${LLVM_MANYCLANGS_BISECT_LOG_DIR:-}
  LLVM_CHECKOUT=${LLVM_MANYCLANGS_BISECT_LLVM_CHECKOUT:-}
  MANYCLANGS=${LLVM_MANYCLANGS_BISECT_MANYCLANGS:-}
  ELFSHAKER_DATA=${LLVM_MANYCLANGS_BISECT_ELFSHAKER_DATA:-}
  INVOCATION_CWD=${LLVM_MANYCLANGS_BISECT_INVOCATION_CWD:-}
  LOCK_FILE=${LLVM_MANYCLANGS_BISECT_LOCK_FILE:-${MANYCLANGS:+$MANYCLANGS/.bisect-lock}}
  TESTCASE=${LLVM_MANYCLANGS_BISECT_TESTCASE:-}
  ACTIVE_LINK_SH=${LLVM_MANYCLANGS_BISECT_ACTIVE_LINK_SH:-}
  LINK_SH_SOURCE=${LLVM_MANYCLANGS_BISECT_LINK_SH_SOURCE:-}
  HOST_CLANG=${LLVM_MANYCLANGS_BISECT_HOST_CLANG:-}
  HOST_CLANGXX=${LLVM_MANYCLANGS_BISECT_HOST_CLANGXX:-}
  HOST_LLD=${LLVM_MANYCLANGS_BISECT_HOST_LLD:-}

  [[ -n $LOG_DIR && -n $LLVM_CHECKOUT && -n $MANYCLANGS && -n $ELFSHAKER_DATA ]] \
    || die "step mode requires exported LLVM_MANYCLANGS_BISECT_* state"
  [[ -n $INVOCATION_CWD ]] || die "step mode requires invocation cwd state"
  [[ -n $LOCK_FILE ]] || die "step mode requires lock state"
  [[ -n $ACTIVE_LINK_SH && -n $LINK_SH_SOURCE ]] || die "step mode requires link.sh state"
  [[ -f $LINK_SH_SOURCE ]] || die "stable link.sh source missing: $LINK_SH_SOURCE"
  [[ -n $HOST_CLANG && -n $HOST_CLANGXX && -n $HOST_LLD ]] \
    || die "step mode requires host toolchain state"

  local command_file=$LOG_DIR/command-argv.txt
  local run_script_file=$LOG_DIR/run-script.txt
  local map_file=$LOG_DIR/snapshot-map.tsv
  declare -a COMMAND_ARGS=()
  RUN_SCRIPT=
  if [[ -f "$command_file" ]]; then
    mapfile -t COMMAND_ARGS <"$command_file"
  fi
  if [[ -f "$run_script_file" ]]; then
    RUN_SCRIPT=$(<"$run_script_file")
  fi

  local commit snapshot step log_file probe_rc bisect_rc status
  commit=$(git -C "$LLVM_CHECKOUT" rev-parse BISECT_HEAD^{commit})
  snapshot=$(awk -F'\t' -v commit="$commit" '$1 == commit { snapshot = $2 } END { if (snapshot == "") exit 1; print snapshot }' "$map_file") || {
    printf 'skip: no snapshot recorded for %s\n' "$commit" >&2
    return 125
  }

  step=$(next_step_number)
  log_file=$LOG_DIR/steps/$step-${commit:0:12}.log
  probe_rc=0
  set +e
  classify_snapshot_commit "$commit" "$snapshot" "$log_file" "bisect-step-$step"
  probe_rc=$?
  set -e

  if [[ $probe_rc -eq 0 ]]; then
    status=fixed
    bisect_rc=1
  elif [[ $probe_rc -eq 125 ]]; then
    status=skip
    bisect_rc=125
  else
    status=broken
    bisect_rc=0
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$step" \
    "$status" \
    "$commit" \
    "$snapshot" \
    "$(commit_date "$commit")" \
    "$(commit_subject "$commit")" >>"$LEDGER_FILE"

  printf '[%s] %s %s %s\n' "$step" "${commit:0:12}" "$status" "$snapshot"
  return "$bisect_rc"
}

if [[ ${1:-} == "--run-step" ]]; then
  LOG_DIR=${LLVM_MANYCLANGS_BISECT_LOG_DIR:-}
  LEDGER_FILE=$LOG_DIR/ledger.tsv
  run_step_mode
  exit $?
fi

SELF=$(resolve_self "$0")
INVOCATION_CWD=$PWD
LLVM_CHECKOUT=${LLVM_CHECKOUT:-$HOME/llvm-project}
MANYCLANGS=${MANYCLANGS:-$HOME/manyclangs}
ELFSHAKER_DATA=
REQUESTED_GOOD_REF=
REQUESTED_BAD_REF=
PATHSPEC=llvm
TESTCASE=
RUN_SCRIPT=
LOG_DIR=
STRICT_ANCESTRY=false
DRY_RUN=false
INITIAL_GOOD_COMMIT=
INITIAL_GOOD_SNAPSHOT=
INITIAL_BAD_COMMIT=
INITIAL_BAD_SNAPSHOT=
GOOD_SKIPPED_COUNT=0
BAD_SKIPPED_COUNT=0
declare -a COMMAND_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --llvm-checkout)
      LLVM_CHECKOUT=$2
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
    --good-ref)
      REQUESTED_GOOD_REF=$2
      shift 2
      ;;
    --bad-ref)
      REQUESTED_BAD_REF=$2
      shift 2
      ;;
    --strict-ancestry)
      STRICT_ANCESTRY=true
      shift
      ;;
    --pathspec)
      PATHSPEC=$2
      shift 2
      ;;
    --testcase)
      TESTCASE=$2
      shift 2
      ;;
    --run-script)
      RUN_SCRIPT=$2
      shift 2
      ;;
    --log-dir)
      LOG_DIR=$2
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      COMMAND_ARGS=("$@")
      break
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

[[ -n $REQUESTED_GOOD_REF ]] || die "--good-ref is required"
[[ -n $REQUESTED_BAD_REF ]] || die "--bad-ref is required"
if [[ -n $RUN_SCRIPT ]]; then
  [[ -n $TESTCASE ]] || die "--testcase is required with --run-script"
else
  [[ ${#COMMAND_ARGS[@]} -gt 0 ]] || die "provide either --run-script or a command after --"
fi

if [[ -z $ELFSHAKER_DATA ]]; then
  ELFSHAKER_DATA=$MANYCLANGS/elfshaker_data
fi

if [[ -n $TESTCASE ]]; then
  TESTCASE=$(make_absolute_path "$TESTCASE")
fi
if [[ -n $RUN_SCRIPT ]]; then
  RUN_SCRIPT=$(make_absolute_path "$RUN_SCRIPT")
  [[ -f $RUN_SCRIPT ]] || die "run script not found: $RUN_SCRIPT"
fi

ensure_checkout
ensure_no_active_bisect

HOST_CLANG=$(command -v clang) || die "required host tool clang not found in PATH"
HOST_CLANGXX=$(command -v clang++) || die "required host tool clang++ not found in PATH"
HOST_LLD=$(command -v ld.lld) || die "required host tool ld.lld not found in PATH"

if [[ -z $LOG_DIR ]]; then
  label=${TESTCASE:-${COMMAND_ARGS[1]:-bisect}}
  label=$(basename "$label")
  label=${label%%.*}
  label=${label//[^A-Za-z0-9._-]/_}
  LOG_DIR=$MANYCLANGS/bisect-logs/$(date -u +%Y%m%d-%H%M%S)-$label
fi

LOCK_FILE=$MANYCLANGS/.bisect-lock
SNAPSHOT_TABLE=$LOG_DIR/snapshot-map.tsv
LEDGER_FILE=$LOG_DIR/ledger.tsv
LINK_SH_SOURCE=$LOG_DIR/link.sh.source
mkdir -p "$LOG_DIR/steps"
printf 'step\tstatus\tcommit\tsnapshot\tdate\tsubject\n' >"$LEDGER_FILE"
printf '%s\n' "${COMMAND_ARGS[@]}" >"$LOG_DIR/command-argv.txt"
printf '%s' "$RUN_SCRIPT" >"$LOG_DIR/run-script.txt"
cp "$MANYCLANGS/link.sh" "$LINK_SH_SOURCE"
chmod +x "$LINK_SH_SOURCE"
ACTIVE_LINK_SH=$MANYCLANGS/.bisect-link-$(basename "$LOG_DIR").sh

build_snapshot_table
load_snapshot_table
printf '[setup] resolving effective bounds...\n'
resolve_effective_bounds
GOOD_PROBE_RC=125
BAD_PROBE_RC=125
printf '[setup] probing requested good bound...\n'
resolve_runnable_bound good "$REQUESTED_GOOD_REF"
if [[ $GOOD_PROBE_RC -ne 0 ]]; then
  write_metadata
  print_effective_bounds
  write_result good_not_fixed "$EFFECTIVE_GOOD_COMMIT"
  die "effective good bound is not fixed; see $LOG_DIR/probe-good.log"
fi
printf '[setup] probing requested bad bound...\n'
resolve_runnable_bound bad "$EFFECTIVE_BAD_ANCHOR"
write_metadata
print_effective_bounds

if $DRY_RUN; then
  exit 0
fi

if [[ $BAD_PROBE_RC -eq 0 ]]; then
  write_result bad_already_fixed "$EFFECTIVE_BAD_COMMIT"
  die "effective bad bound is already fixed; choose an older broken ref or a newer snapshot-backed bad anchor"
fi
if [[ $BAD_PROBE_RC -eq 125 ]]; then
  write_result bad_unclassifiable "$EFFECTIVE_BAD_COMMIT"
  die "effective bad bound could not be classified; see $LOG_DIR/probe-bad.log"
fi

BISECT_STARTED=false
cleanup() {
  if $BISECT_STARTED; then
    git -C "$LLVM_CHECKOUT" bisect reset >/dev/null 2>&1 || true
  fi
  if [[ -n ${ACTIVE_LINK_SH:-} && -e $ACTIVE_LINK_SH ]]; then
    rm -f "$ACTIVE_LINK_SH" || true
  fi
}
trap cleanup EXIT

git -C "$LLVM_CHECKOUT" bisect start \
  --no-checkout \
  "$EFFECTIVE_GOOD_COMMIT" \
  "$EFFECTIVE_BAD_COMMIT" \
  -- "$PATHSPEC"
BISECT_STARTED=true
printf '[setup] starting git bisect run...\n'

export LLVM_MANYCLANGS_BISECT_LOG_DIR=$LOG_DIR
export LLVM_MANYCLANGS_BISECT_LLVM_CHECKOUT=$LLVM_CHECKOUT
export LLVM_MANYCLANGS_BISECT_MANYCLANGS=$MANYCLANGS
export LLVM_MANYCLANGS_BISECT_ELFSHAKER_DATA=$ELFSHAKER_DATA
export LLVM_MANYCLANGS_BISECT_INVOCATION_CWD=$INVOCATION_CWD
export LLVM_MANYCLANGS_BISECT_TESTCASE=$TESTCASE
export LLVM_MANYCLANGS_BISECT_ACTIVE_LINK_SH=$ACTIVE_LINK_SH
export LLVM_MANYCLANGS_BISECT_LINK_SH_SOURCE=$LINK_SH_SOURCE
export LLVM_MANYCLANGS_BISECT_HOST_CLANG=$HOST_CLANG
export LLVM_MANYCLANGS_BISECT_HOST_CLANGXX=$HOST_CLANGXX
export LLVM_MANYCLANGS_BISECT_HOST_LLD=$HOST_LLD
export LLVM_MANYCLANGS_BISECT_LOCK_FILE=$LOCK_FILE

git -C "$LLVM_CHECKOUT" bisect run "$SELF" --run-step
RESULT_COMMIT=$(git -C "$LLVM_CHECKOUT" bisect log | sed -n 's/^# first bad commit: \[\([0-9a-f]\+\)\].*/\1/p' | tail -n 1)
if [[ -z $RESULT_COMMIT ]]; then
  RESULT_COMMIT=$(git -C "$LLVM_CHECKOUT" bisect log | sed -n 's/^# first good commit: \[\([0-9a-f]\+\)\].*/\1/p' | tail -n 1)
fi
if [[ -z $RESULT_COMMIT ]]; then
  RESULT_COMMIT=$(git -C "$LLVM_CHECKOUT" rev-parse BISECT_HEAD^{commit})
fi
write_result fixed_commit "$RESULT_COMMIT"

cat <<EOF

First fixed commit:
$RESULT_COMMIT $(commit_subject "$RESULT_COMMIT")

Ledger:
$LEDGER_FILE
EOF
