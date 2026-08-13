"""Offline calibration research. Does not place bets. Does not touch the core method."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from golf_offshoot.audit.journal import load_audit
from golf_offshoot.learning.loop import PlayerResult, evaluate_run, suggest_alpha_update


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--audit", type=Path, required=True)
    p.add_argument("--winner", required=True, help="player_id who won")
    args = p.parse_args()
    audit = load_audit(args.audit)
    results = [
        PlayerResult(player_id=o.player_id, won=(o.player_id == args.winner))
        for o in audit.outputs
    ]
    report = evaluate_run(audit, results)
    alpha = suggest_alpha_update([(audit, results)])
    print(json.dumps({"brier_win": report.brier_win, "n": report.n, "alpha_preview": alpha}, indent=2))


if __name__ == "__main__":
    main()
