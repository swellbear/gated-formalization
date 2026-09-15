#!/usr/bin/env bash
# Always-on ARM hub paper watch. Own PID. Does not touch learning_lane_15m.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}"
cd "$ROOT"
exec python -m golf_offshoot arm-hub --watch "$@"
