#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec ./run.sh --vfs examples/sample.csv --script examples/demo.script
