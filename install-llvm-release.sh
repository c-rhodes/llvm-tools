#!/usr/bin/env bash
set -euo pipefail

# Linux ARM64 only.
# Installs official LLVM release archives named like:
#   LLVM-22.1.4-Linux-ARM64.tar.xz

usage() {
  echo "usage: install-llvm-release.sh [VERSION]" >&2
  echo "example: install-llvm-release.sh 22.1.4" >&2
  echo "with no VERSION, installs the latest GitHub release" >&2
}

if [[ $# -gt 1 ]]; then
  usage
  exit 2
fi

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "aarch64" ]]; then
  echo "error: this script only supports Linux ARM64" >&2
  exit 1
fi

if [[ $# -eq 1 ]]; then
  version="$1"
else
  latest_url="$(curl -fsIL -o /dev/null -w '%{url_effective}' \
    https://github.com/llvm/llvm-project/releases/latest)"
  tag="${latest_url##*/}"
  version="${tag#llvmorg-}"
fi

tag="llvmorg-$version"
name="LLVM-$version-Linux-ARM64"
archive="$name.tar.xz"
url="https://github.com/llvm/llvm-project/releases/download/$tag/$archive"
dst="/opt/llvm-$version"
tmp="$(mktemp -d)"

trap 'rm -rf "$tmp"' EXIT

if [[ -e "$dst" ]]; then
  echo "error: destination already exists: $dst" >&2
  exit 1
fi

cd "$tmp"

echo "Downloading $url"
curl -fLO "$url"

echo "Extracting $archive"
tar -xf "$archive"

echo "Installing to $dst"
sudo mv "$name" "$dst"
sudo chown -R root:root "$dst"

path_line="export PATH=$dst/bin:\$PATH"
if ! grep -Fxq "$path_line" "$HOME/.zshrc"; then
  {
    echo
    echo "# LLVM $version"
    echo "$path_line"
  } >> "$HOME/.zshrc"
fi

echo
echo "Installed:"
PATH="$dst/bin:$PATH" clang --version
echo
echo "Open a new shell, or run:"
echo "  source ~/.zshrc"
