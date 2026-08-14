"""CLI: golf-offshoot demo | ingest | calibrate | pressure-test | live | ..."""

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
from golf_offshoot.ranking.display import format_table, movement_note
from golf_offshoot.ranking.leaderboard import format_leaderboard
from golf_offshoot.strategy.engine import format_recommendation

DEMO_BANNER = (
    "OFFLINE DEMO — MOCK DATA. Not live, not historical, not for rankings in the "
    "operating path. Mocks are allowed here only."
)


def main(argv: list[str] | None = None) -> int:
    from golf_offshoot.data_feeds.local_env import load_local_env

    load_local_env()
    parser = argparse.ArgumentParser(description="Golf Betting Offshoot (never auto-bets)")
    parser.add_argument(
        "command",
        nargs="?",
        default="demo",
        choices=["demo", "board", "explain", "strategy", "ingest", "calibrate", "pressure-test", "live", "shadow", "paper-export", "paper-ledger", "paper-deposit", "paper-withdraw", "paper-settle"],
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
    parser.add_argument("--event", default="", help="ESPN event id (default: current PGA leaderboard)")
    parser.add_argument("--refresh", action="store_true", help="bypass HTTP cache")
    parser.add_argument("--no-season-stats", action="store_true")
    parser.add_argument(
        "--book",
        default="auto",
        choices=["auto", "bovada", "hardrockbet"],
        help="odds book for ingest/live/pressure-test (auto=Odds API then Bovada; hardrockbet never falls back to Bovada)",
    )
    parser.add_argument(
        "--lock-paper",
        action="store_true",
        help="live: lock a mock/paper book from this run so later live can mark/sell/reallocate",
    )
    parser.add_argument(
        "--apply-paper",
        action="store_true",
        help="live: apply hold/sell/add/reallocate advice to the mock paper book (still never real money)",
    )
    parser.add_argument("--amount", type=float, default=0.0, help="paper-deposit / paper-withdraw amount")
    parser.add_argument("--note", default="", help="note for paper-deposit / paper-withdraw")
    parser.add_argument(
        "--cash-out",
        action="append",
        default=None,
        dest="cash_out",
        help=(
            'live: user-typed sportsbook cash-out dollars for this snapshot, '
            'e.g. "Kurt Kitayama=12.40,Tommy Fleetwood=7.10". Not scraped. Optional.'
        ),
    )
    args = parser.parse_args(argv)

    if args.command == "board":
        rows = board_summary(CourseType(args.course_type), RunMode.PRE_TOURNAMENT)
        print(json.dumps(rows, indent=2))
        return 0

    if args.command == "ingest":
        return _cmd_ingest(args)
    if args.command == "calibrate":
        return _cmd_calibrate(args)
    if args.command == "pressure-test":
        return _cmd_pressure(args)
    if args.command == "live":
        return _cmd_live(args)
    if args.command == "shadow":
        return _cmd_shadow(args)
    if args.command == "paper-export":
        return _cmd_paper_export(args)
    if args.command == "paper-ledger":
        return _cmd_paper_ledger(args)
    if args.command == "paper-deposit":
        return _cmd_paper_deposit(args)
    if args.command == "paper-withdraw":
        return _cmd_paper_withdraw(args)
    if args.command == "paper-settle":
        return _cmd_paper_settle(args)

    print(DEMO_BANNER)
    ct = CourseType(args.course_type)
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


def _cmd_ingest(args) -> int:
    from golf_offshoot.operating import format_inventory, run_operating

    event_id = args.event or None
    result = run_operating(
        event_id=event_id,
        mode=RunMode.PRE_TOURNAMENT,
        sims=args.sims,
        enable_strategy=False,
        persist=True,
        refresh=args.refresh,
        include_season_stats=not args.no_season_stats,
        odds_book=args.book,
    )
    print(f"OPERATING ingest {result.tournament.name} id={result.tournament.tournament_id}")
    print(f"has_cut={result.tournament.has_cut} n={len(result.ranked)} run={result.run_id}")
    inv = result.audit.extra.get("source_inventory") or []
    if inv:
        from golf_offshoot.models.schemas import SourceInventoryItem

        items = [SourceInventoryItem.model_validate(x) for x in inv]
        print(format_inventory(items))
    print(format_table(result.ranked, n=len(result.ranked)))
    _print_table_export(result)
    return 0


def _cmd_calibrate(args) -> int:
    from golf_offshoot.calibration.run import run_calibration

    payload = run_calibration(refresh=args.refresh)
    print(json.dumps({
        "artifact_path": payload.get("artifact_path"),
        "recommendation": payload.get("recommendation"),
        "metrics": payload.get("metrics"),
        "bounds_hit": payload.get("bounds_hit"),
        "ard_relevance": payload.get("ard_relevance"),
        "holdout_event_ids": payload.get("holdout_event_ids"),
        "train_event_ids": payload.get("train_event_ids"),
    }, indent=2))
    return 0


def _cmd_pressure(args) -> int:
    from golf_offshoot.calibration.artifacts import load_weights
    from golf_offshoot.models.schemas import SourceInventoryItem
    from golf_offshoot.operating import (
        run_operating,
        run_strategy_modes,
        write_pressure_report,
    )

    event_id = args.event or None
    strat_mode = StrategyMode(args.mode)
    strat_risk = RiskPreference(args.risk)
    pre = run_operating(
        event_id=event_id,
        mode=RunMode.PRE_TOURNAMENT,
        sims=max(args.sims, 2000),
        enable_strategy=True,
        persist=True,
        refresh=args.refresh,
        bankroll=args.bankroll,
        odds_book=args.book,
        strategy_mode=strat_mode,
        risk=strat_risk,
    )
    print(f"PRE {pre.tournament.name} n={len(pre.ranked)} cut={pre.tournament.has_cut}")
    print(format_table(pre.ranked, n=12))
    _print_table_export(pre)
    modes = run_strategy_modes(pre, bankroll=args.bankroll, risk=strat_risk)
    for k, v in modes.items():
        print(f"\n=== strategy {k} ===")
        print(v)
    live = run_operating(
        event_id=pre.tournament.espn_event_id or pre.tournament.tournament_id,
        mode=RunMode.LIVE,
        sims=max(1200, args.sims // 2),
        enable_strategy=True,
        persist=True,
        refresh=args.refresh,
        bankroll=args.bankroll,
        odds_book=args.book,
        strategy_mode=strat_mode,
        risk=strat_risk,
    )
    print("\n=== live top 8 (movement vs this pressure-test pre) ===")
    print(movement_note(pre.run_id))
    print(format_table(live.ranked, n=8, baseline=pre.ranked))
    _print_table_export(live)
    live_modes = run_strategy_modes(live, bankroll=args.bankroll, risk=strat_risk)
    for k, v in live_modes.items():
        print(f"\n=== live strategy {k} ===")
        print(v)
    inv_raw = pre.audit.extra.get("source_inventory") or []
    inv = [SourceInventoryItem.model_validate(x) for x in inv_raw]
    report = write_pressure_report(
        pre,
        inventory=inv,
        strategy_blocks=modes,
        live=live,
        calib_summary=load_weights(),
        live_strategy_blocks=live_modes,
    )
    print(f"wrote {report}")
    return 0


def _cmd_live(args) -> int:
    from golf_offshoot.operating import run_operating
    from golf_offshoot.strategy.paper_book import (
        advice_from_recommendation,
        apply_advice,
        backfill_estimated_cashouts,
        format_paper_book,
        load_paper_book,
        load_paper_file,
        lock_paper_positions,
        save_paper_book,
    )
    from golf_offshoot.strategy.paper_pack import write_paper_pack

    from golf_offshoot.strategy.paper_ledger import (
        load_ledger,
        other_open_exposure,
        working_bankroll,
    )

    event_hint = args.event or None
    settled_ids = _report_auto_settles(args.refresh)
    paper = load_paper_book(event_hint) if event_hint else None
    from golf_offshoot.strategy.cashout import bind_cashout_quotes, parse_cashout_cli

    cash_pairs, cash_warn = parse_cashout_cli(args.cash_out)
    cash_bound, cash_bind_warn = bind_cashout_quotes(cash_pairs, paper.positions if paper else [])
    for w in cash_warn + cash_bind_warn:
        print(f"cash-out: {w}")
    if cash_pairs and not cash_bound:
        print("cash-out: no quotes attached; live MTM stays the odds-ratio proxy")
    led = load_ledger()
    if led.entries:
        reserved = other_open_exposure(except_event_id=event_hint)
        bankroll = working_bankroll(except_event_id=event_hint)
        extra = f"; ${reserved:.2f} still open on other events" if reserved else ""
        print(
            f"using paper working bankroll ${bankroll:.2f} "
            f"(ledger ${led.bankroll:.2f}{extra})"
        )
        if abs(bankroll - args.bankroll) > 0.009:
            print(
                f"(CLI --bankroll {args.bankroll:.2f} ignored; paper-deposit to add cash)"
            )
    else:
        bankroll = args.bankroll
    strat_mode = StrategyMode(args.mode)
    strat_risk = RiskPreference(args.risk)
    result = run_operating(
        event_id=event_hint,
        mode=RunMode.LIVE,
        sims=args.sims,
        enable_strategy=True,
        persist=True,
        refresh=args.refresh,
        bankroll=bankroll,
        odds_book=args.book,
        open_book=paper,
        cashout_quotes=cash_bound or None,
        strategy_mode=strat_mode,
        risk=strat_risk,
    )
    from golf_offshoot.audit.journal import latest_pre_audit
    from golf_offshoot.data_feeds.http import package_data_dir

    pre = latest_pre_audit(
        result.tournament.espn_event_id or result.tournament.tournament_id,
        package_data_dir() / "snapshots",
    )
    print(
        f"OPERATING live {result.tournament.name} "
        f"id={result.tournament.tournament_id} n={len(result.ranked)} run={result.run_id}"
    )
    print(movement_note(pre.run_id if pre else None))
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    if paper is None and tid:
        paper = load_paper_book(tid)
    held = {p.player_id for p in paper.positions} if paper else set()
    print("live scoreboard (ESPN place / to-par / thru; not model Win%)")
    print(
        format_leaderboard(
            result.ranked,
            n_rounds=int(result.tournament.n_rounds or 4),
            held_ids=held,
        )
    )
    print(format_table(result.ranked, n=len(result.ranked), baseline=pre.outputs if pre else None))
    _print_table_export(result)
    if result.strategy:
        extra_notes = [w for w in cash_warn + cash_bind_warn if w]
        if extra_notes:
            result.strategy.notes = list(result.strategy.notes) + extra_notes
        print(format_recommendation(result.strategy))
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    extras = [
        Path(p)
        for p in (
            result.audit.extra.get("export_pdf"),
            result.audit.extra.get("export_html"),
            result.audit.extra.get("export_txt"),
            result.audit.extra.get("export_leaderboard_pdf"),
            result.audit.extra.get("export_leaderboard_html"),
            result.audit.extra.get("export_leaderboard_txt"),
        )
        if p
    ]
    if args.lock_paper:
        from golf_offshoot.models.strategy import StrategyConfig

        if tid in settled_ids:
            record = load_paper_file(tid)
            print("this event just auto-settled; not locking a new paper book")
            if record:
                print(format_paper_book(record))
            return 0
        cfg = StrategyConfig(
            enabled=True,
            mode=strat_mode,
            risk=strat_risk,
            bankroll=bankroll,
        )
        record = lock_paper_positions(
            result.ranked,
            cfg,
            event_id=tid,
            event_name=result.tournament.name,
            run_id=result.run_id,
            odds_book=str(result.audit.extra.get("odds_book") or args.book),
            extra_export_files=extras,
        )
        print(format_paper_book(record))
        return 0
    record = load_paper_file(tid) if tid else None
    if record:
        record = backfill_estimated_cashouts(record)
        save_paper_book(record)
    if record and result.strategy:
        advice = advice_from_recommendation(record, result.strategy, run_id=result.run_id)
        if args.apply_paper:
            record = apply_advice(record, advice)
            print("applied paper advice (mock only; never auto-bet)")
        record.latest_advice = advice
        save_paper_book(record)
        pack = write_paper_pack(
            record,
            extra_files=extras,
            advice=advice,
            run_id=result.run_id,
        )
        print(format_paper_book(record))
        print(f"paper pack: {pack}")
    return 0


def _report_auto_settles(refresh: bool) -> list[str]:
    from golf_offshoot.strategy.paper_ledger import format_ledger, settle_finished_open_books
    from golf_offshoot.strategy.paper_pack import write_paper_pack

    settled, skipped = settle_finished_open_books(refresh=refresh)
    ids: list[str] = []
    for ledger, record, week in settled:
        print(format_ledger(ledger, week=week))
        pack = write_paper_pack(record, run_id="auto-settle")
        print(
            f"auto-settled {record.tournament_name or record.tournament_id} "
            f"P/L ${week.betting_pnl:+.2f} bankroll ${ledger.bankroll:.2f}"
        )
        print(f"paper pack: {pack}")
        ids.append(str(record.tournament_id))
    for record, why in skipped:
        print(f"paper left open: {record.tournament_name or record.tournament_id} -- {why}")
    return ids


def _cmd_paper_export(args) -> int:
    from golf_offshoot.strategy.paper_pack import export_paper_pack

    event_id = args.event
    if not event_id:
        print("paper-export requires --event <espn_id>")
        return 2
    _report_auto_settles(args.refresh)
    pack = export_paper_pack(event_id)
    print(f"paper pack: {pack}")
    print("Open PDFs in Edge, Chrome, or Adobe -- not as source in the editor.")
    return 0


def _cmd_paper_ledger(args) -> int:
    from datetime import datetime, timezone

    from golf_offshoot.strategy.paper_bankroll_export import write_bankroll_files
    from golf_offshoot.strategy.paper_book import load_paper_file
    from golf_offshoot.strategy.paper_ledger import format_ledger, load_ledger
    from golf_offshoot.strategy.paper_pack import export_paper_pack, packs_dir

    _report_auto_settles(args.refresh)
    ledger = load_ledger()
    if not ledger.entries:
        print("no paper ledger yet; lock-paper or paper-deposit to start")
        return 1
    print(format_ledger(ledger))
    if args.event:
        pack = export_paper_pack(args.event)
        print(f"paper pack: {pack}")
        return 0
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = packs_dir() / f"ledger_{stamp}"
    record = load_paper_file(args.event) if args.event else None
    paths = write_bankroll_files(root, ledger=ledger, record=record)
    print(f"paper pack: {root}")
    print(f"bankroll PDF: {paths.pdf}")
    return 0


def _cmd_paper_deposit(args) -> int:
    from golf_offshoot.strategy.paper_ledger import format_ledger, record_deposit
    from golf_offshoot.strategy.paper_pack import export_paper_pack

    if args.amount <= 0:
        print("paper-deposit requires --amount greater than 0")
        return 2
    try:
        ledger = record_deposit(args.amount, note=args.note, event_id=args.event or "")
    except ValueError as exc:
        print(str(exc))
        return 2
    print(format_ledger(ledger))
    if args.event:
        print(f"paper pack: {export_paper_pack(args.event)}")
    return 0


def _cmd_paper_withdraw(args) -> int:
    from golf_offshoot.strategy.paper_ledger import format_ledger, record_withdrawal
    from golf_offshoot.strategy.paper_pack import export_paper_pack

    if args.amount <= 0:
        print("paper-withdraw requires --amount greater than 0")
        return 2
    try:
        ledger = record_withdrawal(args.amount, note=args.note, event_id=args.event or "")
    except ValueError as exc:
        print(str(exc))
        return 2
    print(format_ledger(ledger))
    if args.event:
        print(f"paper pack: {export_paper_pack(args.event)}")
    return 0


def _cmd_paper_settle(args) -> int:
    from golf_offshoot.strategy.paper_ledger import SettleError, fetch_and_settle, format_ledger
    from golf_offshoot.strategy.paper_pack import write_paper_pack

    if not args.event:
        print("paper-settle requires --event <espn_id>")
        return 2
    try:
        ledger, record, week = fetch_and_settle(args.event, refresh=args.refresh)
    except SettleError as exc:
        print(str(exc))
        return 2
    print(format_ledger(ledger, week=week))
    pack = write_paper_pack(record, run_id="settle")
    print(f"paper pack: {pack}")
    print("Open PDFs in Edge, Chrome, or Adobe -- not as source in the editor.")
    return 0


def _print_table_export(result) -> None:
    pdf = result.audit.extra.get("export_pdf")
    html_path = result.audit.extra.get("export_html")
    txt = result.audit.extra.get("export_txt")
    if pdf:
        print(f"full-field table PDF: {pdf}")
    if html_path:
        print(f"full-field table HTML: {html_path}")
    if txt:
        print(f"full-field table txt: {txt}")
    board_pdf = result.audit.extra.get("export_leaderboard_pdf")
    board_html = result.audit.extra.get("export_leaderboard_html")
    board_txt = result.audit.extra.get("export_leaderboard_txt")
    if board_pdf:
        print(f"live leaderboard PDF: {board_pdf}")
    if board_html:
        print(f"live leaderboard HTML: {board_html}")
    if board_txt:
        print(f"live leaderboard txt: {board_txt}")


def _cmd_shadow(_args) -> int:
    from golf_offshoot.audit.shadow import format_shadow_review, load_shadow

    rows = load_shadow()
    print(format_shadow_review(rows))
    print(f"n={len(rows)} paper-observation only; never auto-bet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
