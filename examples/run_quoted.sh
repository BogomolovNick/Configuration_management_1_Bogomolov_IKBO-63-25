#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec ./run.sh --vfs examples/other.csv --script examples/quoted.script
