"""CLI: golf-offshoot demo | table | explain | strategy | paper"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.demo import demo_field, demo_odds, demo_open_book, demo_tournament
from golf_offshoot.free_parameters.board import board_summary
from golf_offshoot.models.enums import CourseType, Horizon, RiskPreference, RunMode, StrategyMode
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.pipeline import GolfOffshootPipeline
from golf_offshoot.ranking.display import format_table
from golf_offshoot.ranking.report import format_player_report
from golf_offshoot.strategy.engine import format_recommendation, run_strategy
from golf_offshoot.strategy.paper_reports import (
    format_paper_reports,
    load_paper_book,
    paper_reports_payload,
    save_paper_book,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Golf Betting Offshoot (never auto-bets)")
    parser.add_argument(
        "command",
        nargs="?",
        default="demo",
        choices=["demo", "board", "explain", "strategy", "paper"],
    )
    parser.add_argument("--course-type", default="parkland")
    parser.add_argument("--player", default="", help="player id for explain, or filter paper reports")
    parser.add_argument("--sims", type=int, default=1500)
    parser.add_argument("--snapshot-dir", default="")
    parser.add_argument("--strategy", action="store_true", help="enable strategy layer on demo/explain")
    parser.add_argument("--mode", default="stay_selective", help="protect_profits | press_edges | stay_selective")
    parser.add_argument("--risk", default="conservative")
    parser.add_argument("--bankroll", type=float, default=2000.0)
    parser.add_argument("--live", action="store_true", help="after pre-run, mark the paper book live")
    parser.add_argument(
        "--paper-file",
        default="",
        help="PortfolioState JSON of user-recorded paper positions",
    )
    parser.add_argument(
        "--write-paper",
        default="",
        help="write the paper book used this run (demo or loaded) to this path",
    )
    parser.add_argument(
        "--include-proposed",
        action="store_true",
        help="also print full reports for strategy NEW_BET suggestions",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="machine-readable paper reports")
    return parser


def _pipeline(args) -> GolfOffshootPipeline:
    strat_cfg = StrategyConfig(
        enabled=args.command in ("strategy", "paper") or args.strategy,
        mode=StrategyMode(args.mode),
        risk=RiskPreference(args.risk),
        bankroll=args.bankroll,
    )
    engine = BayesianEngine(sim=SimConfig(n_sims=args.sims, seed=20260813))
    snap = Path(args.snapshot_dir) if args.snapshot_dir else Path(__file__).resolve().parents[2] / "data" / "snapshots"
    return GolfOffshootPipeline(engine=engine, snapshot_dir=snap, strategy_config=strat_cfg), strat_cfg


def _resolve_book(args, result, strat_cfg):
    if args.paper_file:
        book = load_paper_book(args.paper_file)
        if book.bankroll <= 0:
            book.bankroll = args.bankroll
        return book
    return demo_open_book(result, bankroll=strat_cfg.bankroll)


def _maybe_live(pipe, args, tournament, result, book, strat_cfg, field=None):
    if not args.live:
        if book.positions:
            result.strategy = run_strategy(
                result.ranked,
                strat_cfg,
                run_mode=result.mode,
                field=field,
                book=book,
            )
            result.audit.strategy = result.strategy
        return result, field
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
    return live, live_field


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    ct = CourseType(args.course_type)
    if args.command == "board":
        rows = board_summary(ct, RunMode.PRE_TOURNAMENT)
        print(json.dumps(rows, indent=2))
        return 0

    pipe, strat_cfg = _pipeline(args)
    tournament = demo_tournament(ct)
    field = demo_field()
    result = pipe.run(tournament, field, market_quotes=demo_odds(field), persist=bool(args.snapshot_dir))

    if args.command == "paper":
        try:
            book = _resolve_book(args, result, strat_cfg)
        except FileNotFoundError:
            print(f"paper file not found: {args.paper_file}", file=sys.stderr)
            return 2
        except Exception as exc:  # pydantic validation etc.
            print(f"could not load paper file: {exc}", file=sys.stderr)
            return 2
        result, report_field = _maybe_live(
            pipe, args, tournament, result, book, strat_cfg, field=field
        )
        if args.player:
            book.positions = [p for p in book.positions if p.player_id == args.player]
        if args.write_paper:
            save_paper_book(book, args.write_paper)
        if args.as_json:
            payload = paper_reports_payload(
                result,
                book,
                field=report_field,
                include_proposed=args.include_proposed,
            )
            print(json.dumps(payload, indent=2, default=str))
            return 0
        print(
            format_paper_reports(
                result,
                book,
                field=report_field,
                include_proposed=args.include_proposed,
            )
        )
        return 0

    print(f"run_id={result.run_id} mode={result.mode.value} never_auto_bet={result.never_auto_bet}")
    print(format_table(result.ranked))
    print("\nWarnings:")
    for w in result.warnings[:12]:
        print(" -", w)
    if args.command == "explain":
        pid = args.player or "p01"
        row = next((r for r in result.ranked if r.player_id == pid), result.ranked[0])
        inputs = next((p for p in field.players if p.player.player_id == row.player_id), None)
        print("\n--- full report ---")
        print(format_player_report(row, inputs=inputs))
        print("open:", row.open_questions)
        print("flags:", row.flags)
        print("decision:", row.decision.action.value if row.decision else None)
        print("win range:", row.probabilities.p(Horizon.WIN).model_dump())
    if result.strategy:
        print("\n--- strategy ---")
        print(format_recommendation(result.strategy))
    if args.command == "strategy" and args.live:
        book = _resolve_book(args, result, strat_cfg)
        live, _ = _maybe_live(
            pipe, args, tournament, result, book, strat_cfg, field=field
        )
        print("\n--- live strategy ---")
        if live.strategy:
            print(format_recommendation(live.strategy))
    return 0


if __name__ == "__main__":
    sys.exit(main())
