"""CLI: golf-offshoot demo | table | explain | strategy"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.demo import demo_field, demo_odds, demo_open_book, demo_tournament
from golf_offshoot.free_parameters.board import board_summary
from golf_offshoot.models.enums import CourseType, Horizon, RiskPreference, StrategyMode
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.pipeline import GolfOffshootPipeline
from golf_offshoot.ranking.display import format_table
from golf_offshoot.strategy.engine import format_recommendation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Golf Betting Offshoot (never auto-bets)")
    parser.add_argument(
        "command",
        nargs="?",
        default="demo",
        choices=["demo", "board", "explain", "strategy"],
    )
    parser.add_argument("--course-type", default="parkland")
    parser.add_argument("--player", default="p01")
    parser.add_argument("--sims", type=int, default=1500)
    parser.add_argument("--snapshot-dir", default="")
    parser.add_argument("--strategy", action="store_true", help="enable strategy layer on demo/explain")
    parser.add_argument("--mode", default="stay_selective", help="protect_profits | press_edges | stay_selective")
    parser.add_argument("--risk", default="conservative")
    parser.add_argument("--bankroll", type=float, default=2000.0)
    parser.add_argument("--live", action="store_true", help="strategy command: after pre-run, manage a demo book live")
    args = parser.parse_args(argv)

    ct = CourseType(args.course_type)
    if args.command == "board":
        rows = board_summary(ct)
        print(json.dumps(rows, indent=2))
        return 0

    strat_cfg = StrategyConfig(
        enabled=args.command == "strategy" or args.strategy,
        mode=StrategyMode(args.mode),
        risk=RiskPreference(args.risk),
        bankroll=args.bankroll,
    )

    engine = BayesianEngine(sim=SimConfig(n_sims=args.sims, seed=20260813))
    snap = Path(args.snapshot_dir) if args.snapshot_dir else Path(__file__).resolve().parents[2] / "data" / "snapshots"
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=snap, strategy_config=strat_cfg)
    tournament = demo_tournament(ct)
    field = demo_field()
    result = pipe.run(tournament, field, market_quotes=demo_odds(field), persist=bool(args.snapshot_dir))

    print(f"run_id={result.run_id} mode={result.mode.value} never_auto_bet={result.never_auto_bet}")
    print(format_table(result.ranked))
    print("\nWarnings:")
    for w in result.warnings[:12]:
        print(" -", w)
    if args.command == "explain":
        row = next((r for r in result.ranked if r.player_id == args.player), result.ranked[0])
        print("\n--- explain ---")
        print(row.explain.narrative if row.explain else "")
        print("open:", row.open_questions)
        print("flags:", row.flags)
        print("decision:", row.decision.action.value if row.decision else None)
        print("win range:", row.probabilities.p(Horizon.WIN).model_dump())
    if result.strategy:
        print("\n--- strategy ---")
        print(format_recommendation(result.strategy))
    if args.command == "strategy" and args.live:
        book = demo_open_book(result, bankroll=args.bankroll)
        live_field = demo_field()
        for i, p in enumerate(live_field.players):
            p.live_score_to_par = -3 + i * 0.4
            p.live_holes_completed = 18
        live = pipe.rerun_live(
            tournament,
            live_field,
            previous=result.audit,
            market_quotes=demo_odds(live_field),
            open_book=book,
            strategy_config=strat_cfg,
        )
        print("\n--- live strategy ---")
        if live.strategy:
            print(format_recommendation(live.strategy))
    return 0


if __name__ == "__main__":
    sys.exit(main())
