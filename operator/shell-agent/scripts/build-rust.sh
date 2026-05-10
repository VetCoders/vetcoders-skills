#!/usr/bin/env bash
set -e
cd "${SRCROOT}/../.." || exit 1
cargo build -p shell-agent-ffi --release