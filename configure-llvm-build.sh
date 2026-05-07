#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
usage: configure-llvm-build <config> [-- <extra-cmake-args>...]

Configs:
  dev                 daily development build
  dev-all-targets     same as previous but all targets enabled for wider testing when necessary
  compiletime         for compile-time work, intentionally based on
                      https://github.com/nikic/llvm-compile-time-tracker/blob/master/cmake_llvm_project_stage1.sh
                      to get results as close to upstream tracker as possible
  compiletime-perf    same as previous, but with debug info and -fno-omit-frame-pointer.
                      Useful for performance analysis with perf and creating flame graphs,
                      based on
                      https://clang.llvm.org/docs/analyzer/developer-docs/PerformanceInvestigation.html#performance-analysis-using-perf

Set LLVM_CHECKOUT=/path/to/llvm-project to choose a checkout explicitly.
If unset, the script uses the current directory when it is an LLVM checkout,
or ./llvm-project when run from an experiment directory.
EOF
}

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

config=$1
shift

extra_args=()
if [[ $# -gt 0 ]]; then
  if [[ $1 != "--" ]]; then
    usage >&2
    exit 2
  fi
  shift
  extra_args=("$@")
fi

find_checkout() {
  if [[ -n "${LLVM_CHECKOUT:-}" ]]; then
    printf '%s\n' "$LLVM_CHECKOUT"
    return
  fi

  if [[ -f llvm/CMakeLists.txt ]]; then
    pwd
    return
  fi

  if [[ -f llvm-project/llvm/CMakeLists.txt ]]; then
    printf '%s/llvm-project\n' "$(pwd)"
    return
  fi

  printf 'error: cannot find LLVM checkout; set LLVM_CHECKOUT\n' >&2
  exit 1
}

checkout=$(find_checkout)
if [[ ! -f "$checkout/llvm/CMakeLists.txt" ]]; then
  printf 'error: %s is not an LLVM checkout\n' "$checkout" >&2
  exit 1
fi

case "$config" in
  dev)
    build_dir=build
    # daily development build
    args=(
      -G Ninja
      -S llvm
      -B "$build_dir"
      -DCMAKE_BUILD_TYPE=RelWithDebInfo
      -DLLVM_USE_LINKER=lld
      -DLLVM_CCACHE_BUILD=ON
      -DBUILD_SHARED_LIBS=ON
      -DLLVM_ENABLE_ASSERTIONS=ON
      -DLLVM_ENABLE_PROJECTS=clang
      -DLLVM_TARGETS_TO_BUILD=AArch64
    )
    ;;
  dev-all-targets)
    build_dir=build-all-targets
    # same as previous but all targets enabled for wider testing when necessary
    args=(
      -G Ninja
      -S llvm
      -B "$build_dir"
      -DCMAKE_BUILD_TYPE=Release
      -DLLVM_USE_LINKER=lld
      -DLLVM_CCACHE_BUILD=ON
      -DBUILD_SHARED_LIBS=ON
      -DLLVM_ENABLE_ASSERTIONS=ON
      -DLLVM_ENABLE_PROJECTS=clang
      -DLLVM_TARGETS_TO_BUILD=all
    )
    ;;
  compiletime)
    build_dir=build-compiletime
    # for compile-time work, intentionally based on
    # https://github.com/nikic/llvm-compile-time-tracker/blob/master/cmake_llvm_project_stage1.sh
    # to get results as close to upstream tracker as possible
    args=(
      -G Ninja
      -S llvm
      -B "$build_dir"
      -DCMAKE_BUILD_TYPE=Release
      -DLLVM_USE_LINKER=lld
      -DLLVM_CCACHE_BUILD=true
      -DLLVM_ENABLE_PROJECTS=clang
      -DLLVM_TARGETS_TO_BUILD=AArch64
      -DLLVM_BUILD_TOOLS=false
      -DLLVM_INCLUDE_TESTS=false
      -DLLVM_INCLUDE_BENCHMARKS=false
      -DLLVM_APPEND_VC_REV=false
      -DCLANG_ENABLE_ARCMT=false
      -DCLANG_ENABLE_STATIC_ANALYZER=false
    )
    ;;
  compiletime-perf)
    build_dir=build-compiletime-perf
    # same as previous, but with debug info and -fno-omit-frame-pointer.
    # Useful for performance analysis with perf and creating flame graphs, based on
    # https://clang.llvm.org/docs/analyzer/developer-docs/PerformanceInvestigation.html#performance-analysis-using-perf
    args=(
      -G Ninja
      -S llvm
      -B "$build_dir"
      -DCMAKE_BUILD_TYPE=RelWithDebInfo
      -DCMAKE_CXX_FLAGS=-fno-omit-frame-pointer
      -DLLVM_USE_LINKER=lld
      -DLLVM_CCACHE_BUILD=true
      -DLLVM_ENABLE_PROJECTS=clang
      -DLLVM_TARGETS_TO_BUILD=AArch64
      -DLLVM_BUILD_TOOLS=false
      -DLLVM_INCLUDE_TESTS=false
      -DLLVM_INCLUDE_BENCHMARKS=false
      -DLLVM_APPEND_VC_REV=false
      -DCLANG_ENABLE_STATIC_ANALYZER=false
    )
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    printf 'error: unknown config: %s\n\n' "$config" >&2
    usage >&2
    exit 2
    ;;
esac

cd "$checkout"
cmake "${args[@]}" "${extra_args[@]}"

printf '\nConfigured %s in %s/%s\n' "$config" "$checkout" "$build_dir"
printf 'Next: ninja -C %s/%s <target>\n' "$checkout" "$build_dir"
