# LLVM bisection tool built on manyclangs

Example invocation bisecting issue `183747`:

```bash
./bisect.sh --good-ref eae0b6b24983 --bad-ref llvmorg-22.1.5 -- \
  llc bisect/corpus/183747/repro.ll -o -
```

The main entrypoints are:

- `bisect.sh` for one-off interactive bisects
- `verify.sh` for rerunning the local corpus in `manifest.tsv`

## Prerequisites

- an LLVM git checkout, typically `~/llvm-project`
- `elfshaker` and `manyclangs` (see below)
- `clang`, `clang++`, `ld.lld`, and `flock` in `PATH`

```bash
# Install elfshaker
wget https://github.com/elfshaker/elfshaker/releases/download/v0.9.0/elfshaker_v0.9.0_aarch64-unknown-linux-musl.tar.gz
tar xzvf elfshaker_v0.9.0_aarch64-unknown-linux-musl.tar.gz
sudo mv elfshaker/bin/elfshaker /usr/bin

# Checkout manyclangs and download pack files
git clone git@github.com:elfshaker/manyclangs.git
mkdir -p ~/manyclangs/elfshaker_data/packs ~/manyclangs/bin
cd ~/manyclangs
gh release download -p "*" -D elfshaker_data/packs -R elfshaker/manyclangs
```

Downloading all pack files is convenient when bisecting across multiple LLVM
release ranges, but it takes time and disk space. For v0.9.0 this is ~8GB and
may take a while. Alternatively, manyclangs README has instructions for getting
pack files for a single month. I'm commonly bisecting issues between major LLVM
releases which are a 6 month cadence so downloading all packs files was easier.

TODO: once released elfshaker 1.0 should have a new # clone option that could
be used instead.

## `bisect.sh`

`bisect.sh` resolves the requested bounds to snapshot-backed commits,
checks that the newer bound is fixed and the older bound is broken, and
then runs the requested reproducer against each midpoint.

For more complex reproducers, it also supports a `--run-script` mode:

```bash
./bisect.sh --good-ref GOOD --bad-ref BAD \
  --testcase corpus/NNNNNN/repro.ll \
  --run-script corpus/NNNNNN/run.sh
```

The runner interface is:

```text
<run-script> <link_sh> <testcase> <snapshot> <commit>
```

If the requested refs are divergent, `bisect.sh` bisects trunk from their
merge-base to `--good-ref` unless `--strict-ancestry` is used.

Since `manyclangs` uses a shared extracted tree, `bisect.sh` locks
snapshot extraction and execution so concurrent runs do not mix different
snapshots.

## `verify.sh`

`verify.sh` reruns the local corpus recorded in `manifest.tsv`:

```bash
./verify.sh --list
./verify.sh --issue 183747
./verify.sh --issue 183747 --dry-run
```

By default, it creates a disposable shared bare clone of the LLVM source
repo for the bisect state instead of writing `BISECT_*` files into your
main checkout.

The corpus layout is:

```text
bisect/
  bisect.sh
  verify.sh
  manifest.tsv
  corpus/
    183747/
      repro.ll
      run.sh
```

## Notes

- Snapshots from failed upstream builds are treated as `skip`, not as
  testcase outcomes.
- Run logs are written under `manyclangs/bisect-logs/` by default.
