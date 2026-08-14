"""Offline calibration. Real historical ESPN data; no future leakage; never bets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from golf_offshoot.audit.journal import load_audit
from golf_offshoot.calibration.run import run_calibration
from golf_offshoot.learning.loop import PlayerResult, evaluate_run, suggest_alpha_update


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--audit", type=Path, help="optional single-audit Brier (legacy)")
    p.add_argument("--winner", help="player_id who won (legacy with --audit)")
    p.add_argument("--refresh", action="store_true")
    args = p.parse_args()
    if args.audit:
        if not args.winner:
            raise SystemExit("--winner required with --audit")
        audit = load_audit(args.audit)
        results = [
            PlayerResult(player_id=o.player_id, won=(o.player_id == args.winner))
            for o in audit.outputs
        ]
        report = evaluate_run(audit, results)
        alpha = suggest_alpha_update([(audit, results)])
        print(json.dumps({"brier_win": report.brier_win, "n": report.n, "alpha_preview": alpha}, indent=2))
        return
    payload = run_calibration(refresh=args.refresh)
    print(json.dumps({
        "artifact_path": payload.get("artifact_path"),
        "recommendation": payload.get("recommendation"),
        "metrics": payload.get("metrics"),
        "bounds_hit": payload.get("bounds_hit"),
        "ard_relevance": payload.get("ard_relevance"),
    }, indent=2))


if __name__ == "__main__":
    main()
