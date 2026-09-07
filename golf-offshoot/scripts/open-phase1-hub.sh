#!/usr/bin/env bash
# Phase 1 observation hub. Trading NOT ARMED. PAPER OBSERVATION ONLY.
# AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH. Local only.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -d "$ROOT/src/golf_offshoot" ]]; then
  export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
fi
echo "PHASE 1 OBSERVATION. Trading NOT ARMED. PAPER OBSERVATION ONLY."
echo "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH."
echo "Starting python -m golf_offshoot shell on http://127.0.0.1:8765"
exec python3 -m golf_offshoot shell --host 127.0.0.1 --port 8765 "$@"
