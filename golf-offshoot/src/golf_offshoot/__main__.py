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
from golf_offshoot.ranking.leftover import format_leftover_callout
from golf_offshoot.operator_hints import (
    is_empty_field,
    pinned_event_hint,
    pre_thursday_opening_warning,
)
from golf_offshoot.strategy.engine import format_recommendation

DEMO_BANNER = (
    "OFFLINE DEMO — MOCK DATA. Not live, not historical, not for rankings in the "
    "operating path. Mocks are allowed here only."
)


def _event_is_settled(event_id: str | None) -> bool:
    if not event_id:
        return False
    from golf_offshoot.strategy.paper_book import load_paper_file

    rec = load_paper_file(event_id)
    return rec is not None and rec.settled_at is not None


def _print_operator_hints(result, *, pinned_id: str | None, settled: bool) -> None:
    note = pinned_event_hint(pinned_id, settled=settled)
    if note:
        print(note)
    warn = pre_thursday_opening_warning(
        result.tournament.start_date,
        int(result.audit.extra.get("opening_quotes") or 0),
        odds_book=str(result.audit.extra.get("odds_book") or ""),
    )
    if warn:
        print(warn)


def _configure_stdio() -> None:
    """Windows cp1252 cannot print inventory notes (e.g. >=). Fail open."""
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if not callable(reconf):
            continue
        try:
            reconf(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def main(argv: list[str] | None = None) -> int:
    from golf_offshoot.data_feeds.local_env import load_local_env

    _configure_stdio()
    load_local_env()
    parser = argparse.ArgumentParser(description="Golf Betting Offshoot (never auto-bets)")
    parser.add_argument(
        "command",
        nargs="?",
        default="demo",
        choices=["demo", "board", "explain", "strategy", "ingest", "calibrate", "pressure-test", "live", "watch", "shadow", "paper-export", "paper-ledger", "paper-deposit", "paper-withdraw", "paper-settle", "paper-fill", "compare-replay"],
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
        choices=["auto", "bovada", "hardrockbet", "polymarket"],
        help="odds book for ingest/live/watch/pressure-test/paper-ledger/paper-deposit/paper-withdraw/paper-export (auto=Odds API then Bovada; polymarket never writes ledger.json)",
    )
    parser.add_argument(
        "--lock-paper",
        action="store_true",
        help="live: lock a mock/paper book from this run so later live can mark/sell/reallocate",
    )
    parser.add_argument(
        "--apply-paper",
        action="store_true",
        help="live: force-apply hold/sell/add/reallocate advice to the mock paper book (still never real money)",
    )
    parser.add_argument(
        "--no-apply-paper",
        action="store_true",
        help="live: record advice but do not apply even if the advice set changed",
    )
    parser.add_argument(
        "--compare-method",
        action="store_true",
        help="live: ingest once, run A θ + B-guts θ, auto-apply four independent paper books, write fights page",
    )
    parser.add_argument("--amount", type=float, default=0.0, help="paper-deposit / paper-withdraw amount")
    parser.add_argument("--note", default="", help="note for paper-deposit / paper-withdraw")
    parser.add_argument(
        "--cash-out",
        action="append",
        default=None,
        dest="cash_out",
        help=(
            'live: user-typed cash-out dollars for this snapshot, '
            'e.g. "Kurt Kitayama=12.40,Tommy Fleetwood=7.10". '
            "Not scraped. Optional. On --book polymarket overrides shares x bestBid."
        ),
    )
    parser.add_argument("--shares", type=float, default=0.0, help="paper-fill: Yes shares received")
    parser.add_argument(
        "--fill",
        type=float,
        default=0.0,
        help="paper-fill: Yes fill price in (0, 1), e.g. 0.034",
    )
    parser.add_argument(
        "--cost",
        type=float,
        default=None,
        help="paper-fill: USDC spent (default shares x fill)",
    )
    parser.add_argument(
        "--market",
        default="win",
        help="paper-fill: win | top_5 | top_10 | top_20 | make_cut | win_after_r1 | win_after_r2 | win_after_r3",
    )
    parser.add_argument(
        "--intent",
        default=None,
        help="paper-fill: hold | flip (default hold on new tickets; keep existing on replace)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=600,
        help="watch: seconds between in-play ticks (default 600)",
    )
    parser.add_argument(
        "--pre-tee-interval",
        type=int,
        default=1800,
        dest="pre_tee_interval",
        help="watch: seconds between ticks before anyone is on the ESPN board (default 1800)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="watch: one tick then exit (use this to confirm ntfy)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="watch: compute the trigger and print; do not POST to ntfy",
    )
    parser.add_argument(
        "--ntfy-topic",
        default=None,
        dest="ntfy_topic",
        help="watch: ntfy topic (default NTFY_TOPIC from .env)",
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
    if args.command == "watch":
        return _cmd_watch(args)
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
    if args.command == "paper-fill":
        return _cmd_paper_fill(args)
    if args.command == "compare-replay":
        return _cmd_compare_replay(args)

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
    print()
    print(format_leftover_callout(result))
    _print_operator_hints(
        result,
        pinned_id=args.event or None,
        settled=_event_is_settled(result.tournament.espn_event_id or result.tournament.tournament_id),
    )
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
    print("\n=== leftover (pre) ===")
    print(format_leftover_callout(pre))
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
    from golf_offshoot.strategy.paper_book import load_paper_book

    tid = pre.tournament.espn_event_id or pre.tournament.tournament_id
    paper = load_paper_book(tid) if tid else None
    print("\n=== leftover (live) ===")
    print(format_leftover_callout(live, paper))
    _print_operator_hints(
        live,
        pinned_id=event_id or (live.tournament.espn_event_id or live.tournament.tournament_id),
        settled=_event_is_settled(live.tournament.espn_event_id or live.tournament.tournament_id),
    )
    inv_raw = pre.audit.extra.get("source_inventory") or []
    inv = [SourceInventoryItem.model_validate(x) for x in inv_raw]
    report = write_pressure_report(
        pre,
        inventory=inv,
        strategy_blocks=modes,
        live=live,
        calib_summary=load_weights(),
        live_strategy_blocks=live_modes,
        open_book=paper,
    )
    print(f"wrote {report}")
    return 0


def _cmd_live_polymarket(args) -> int:
    """Polymarket-only live + readout. Never loads lived Bovada or the A/B batch pack."""
    from golf_offshoot.compare.apply import maybe_apply_paper
    from golf_offshoot.compare.law import METHOD_LAW_V1
    from golf_offshoot.compare.paths import allowed_bets_from_rows
    from golf_offshoot.data_feeds.polymarket import POLYMARKET_PATH_ID
    from golf_offshoot.operating import run_operating
    from golf_offshoot.models.enums import BetType, ROUND_LEADER_BETS
    from golf_offshoot.strategy.paper_book import (
        EmptyFieldLockError,
        advice_from_recommendation,
        format_paper_book,
        load_paper_file,
        lock_paper_positions,
        paper_candidate_slots,
        save_paper_book,
        void_unlisted_paper_bets,
    )
    from golf_offshoot.strategy.paper_pack import write_polymarket_pack

    if args.compare_method:
        print("compare-method is the Bovada A/B pack; this run writes a Polymarket-only readout")
    event_hint = args.event or None
    existing = load_paper_file(event_hint, path_id=POLYMARKET_PATH_ID) if event_hint else None
    if existing is not None:
        existing, dropped = void_unlisted_paper_bets(
            existing,
            {BetType.WIN, *ROUND_LEADER_BETS},
            reason_plain=(
                "Not listed on Polymarket US golf futures. Voided at cost. Not a cash-out."
            ),
            reason_technical=(
                "US gateway golf futures are Winner and end-of-round leader; "
                "Top 5/10/20 are international Gamma cards"
            ),
        )
        if dropped:
            save_paper_book(existing)
            print("voided polymarket tickets that are not on the US golf app (at cost)")
    bankroll = float(
        existing.bankroll
        if existing is not None
        else METHOD_LAW_V1["independent_compare_bankroll"]
    )
    print(
        f"polymarket path; independent ${bankroll:.0f} mock; "
        "lived Bovada ledger not used; no CLOB orders"
    )
    from golf_offshoot.strategy.cashout import bind_cashout_quotes, parse_cashout_cli

    paper = existing.book if existing else None
    cash_pairs, cash_warn = parse_cashout_cli(args.cash_out)
    cash_bound, cash_bind_warn = bind_cashout_quotes(cash_pairs, paper.positions if paper else [])
    for w in cash_warn + cash_bind_warn:
        print(f"cash-out: {w}")
    if cash_pairs and not cash_bound:
        print("cash-out: no quotes attached; live MTM stays shares x bestBid when a fill exists")
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
        odds_book="polymarket",
        open_book=paper,
        strategy_mode=strat_mode,
        risk=strat_risk,
        cashout_quotes=cash_bound or None,
    )
    from golf_offshoot.audit.journal import latest_pre_audit
    from golf_offshoot.data_feeds.http import package_data_dir

    pre = latest_pre_audit(
        result.tournament.espn_event_id or result.tournament.tournament_id,
        package_data_dir() / "snapshots",
    )
    print(
        f"OPERATING live {result.tournament.name} "
        f"id={result.tournament.tournament_id} n={len(result.ranked)} run={result.run_id} "
        "odds_book=polymarket"
    )
    print(movement_note(pre.run_id if pre else None))
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
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
        print(format_recommendation(result.strategy))
    print()
    print(format_leftover_callout(result, paper))
    _print_operator_hints(
        result,
        pinned_id=args.event or tid,
        settled=_event_is_settled(tid),
    )
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
    record = existing
    cfg = StrategyConfig(
        enabled=True,
        mode=strat_mode,
        risk=strat_risk,
        bankroll=bankroll,
        ticket_screen="both",
        never_auto_bet=True,
        allowed_bet_types=allowed_bets_from_rows(tid, result.ranked),
    )
    if is_empty_field(result.ranked):
        print("empty field; not locking polymarket paper")
    elif record is None:
        slots = paper_candidate_slots(result.ranked, cfg, require_cleared=False)
        if not slots:
            print("no polymarket names cleared the ticket screen; not locking paper")
        else:
            try:
                record = lock_paper_positions(
                    result.ranked,
                    cfg,
                    event_id=tid,
                    event_name=result.tournament.name,
                    run_id=result.run_id,
                    odds_book="polymarket",
                    extra_export_files=extras,
                    path_id=POLYMARKET_PATH_ID,
                    independent_bankroll=True,
                    write_exports=False,
                )
            except EmptyFieldLockError as exc:
                print(str(exc))
                record = None
    elif result.strategy:
        from golf_offshoot.strategy.fills import relink_paper_player_ids

        record = relink_paper_player_ids(record, result.ranked)
        advice = advice_from_recommendation(record, result.strategy, run_id=result.run_id)
        if args.no_apply_paper:
            record.latest_advice = advice
            save_paper_book(record)
        else:
            record, applied = maybe_apply_paper(record, advice)
            if applied:
                print("applied polymarket paper advice (mock only; never auto-bet)")
            save_paper_book(record)
    if record:
        print(format_paper_book(record))
    try:
        pack = write_polymarket_pack(
            event_id=tid,
            event_name=result.tournament.name,
            run_id=result.run_id,
            extra_files=extras,
            record=record,
        )
    except PermissionError as exc:
        print(f"polymarket pack blocked; close the open PDF and rerun pack. {exc}")
        return 1
    print(f"polymarket pack: {pack}")
    combo = pack / "00_full_readout.pdf"
    if combo.is_file():
        print(f"full readout: {combo}")
    return 0


def _cmd_live(args) -> int:
    from golf_offshoot.data_feeds.hardrock import resolve_odds_book

    if resolve_odds_book(args.book) == "polymarket":
        return _cmd_live_polymarket(args)
    from golf_offshoot.operating import run_operating
    from golf_offshoot.strategy.paper_book import (
        EmptyFieldLockError,
        advice_from_recommendation,
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
    if args.compare_method and args.lock_paper:
        print("compare-method will not --lock-paper the lived museum book")
        args.lock_paper = False
    if args.compare_method:
        from golf_offshoot.compare.runner import run_compare_method

        payload = run_compare_method(
            event_id=event_hint,
            sims=args.sims,
            refresh=args.refresh,
            odds_book=args.book,
            persist=True,
            include_season_stats=not args.no_season_stats,
            lived_strategy_config=StrategyConfig(
                enabled=True,
                mode=strat_mode,
                risk=strat_risk,
                bankroll=bankroll,
                ticket_screen="both",
                never_auto_bet=True,
            ),
            lived_open_book=paper,
            cashout_quotes=cash_bound or None,
        )
        result = payload["lived_result"]
        print(
            f"compare-method fights={payload['fights']} "
            f"guts={payload['guts_run_id']} law={payload['law_hash']}"
        )
        print("independent $250-start compare books; lived lock frozen (live apply still mutates)")
    else:
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
    print()
    print(format_leftover_callout(result, paper))
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    _print_operator_hints(
        result,
        pinned_id=args.event or tid,
        settled=(tid in settled_ids) or _event_is_settled(tid),
    )
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
        if is_empty_field(result.ranked):
            print("empty field; not locking paper")
            return 2
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
        try:
            record = lock_paper_positions(
                result.ranked,
                cfg,
                event_id=tid,
                event_name=result.tournament.name,
                run_id=result.run_id,
                odds_book=str(result.audit.extra.get("odds_book") or args.book),
                extra_export_files=extras,
            )
        except EmptyFieldLockError as exc:
            print(str(exc))
            return 2
        print(format_paper_book(record))
        return 0
    record = load_paper_file(tid) if tid else None
    if record:
        from golf_offshoot.strategy.paper_book import void_post_settle_open_tickets

        record, voided = void_post_settle_open_tickets(record)
        if voided:
            print(
                "voided post-settle leftover tickets at cost "
                "(not a cash-out; not week P/L)"
            )
        record = backfill_estimated_cashouts(record)
        save_paper_book(record)
    if record and result.strategy:
        advice = advice_from_recommendation(record, result.strategy, run_id=result.run_id)
        from golf_offshoot.compare.apply import maybe_apply_paper

        settled = record.settled_at is not None or (tid in settled_ids)
        if settled:
            print("event already settled; not applying new paper tickets")
        elif args.apply_paper:
            record, applied = maybe_apply_paper(record, advice, force=True)
            if applied:
                print("applied paper advice (mock only; never auto-bet)")
        elif not args.no_apply_paper:
            record, applied = maybe_apply_paper(record, advice)
            if applied:
                print("applied paper advice (mock only; never auto-bet) [advice set changed]")
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
    if args.compare_method:
        from golf_offshoot.compare.pack import write_batch_pack

        batch = write_batch_pack(
            tid,
            event_name=result.tournament.name,
            run_id=result.run_id,
            extra_files=extras,
        )
        print(f"batch pack: {batch}")
        combo = batch / "00_full_readout.pdf"
        if combo.is_file():
            print(f"full readout: {combo}")
    return 0


def _report_auto_settles(refresh: bool) -> list[str]:
    from golf_offshoot.strategy.paper_ledger import format_ledger, settle_finished_open_books
    from golf_offshoot.strategy.paper_book import scrub_settled_leftover_tickets
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
    for rec in scrub_settled_leftover_tickets():
        path = rec.path_id or "lived"
        print(
            f"voided post-settle leftover tickets at cost "
            f"({rec.tournament_id} {path}; not a cash-out; not week P/L)"
        )
    return ids


def _paper_path_id(args) -> str:
    from golf_offshoot.data_feeds.hardrock import resolve_odds_book

    book = resolve_odds_book(getattr(args, "book", None))
    if book == "polymarket":
        return "polymarket"
    return "lived"


def _cmd_paper_export(args) -> int:
    from golf_offshoot.strategy.paper_pack import export_paper_pack

    event_id = args.event
    if not event_id:
        print("paper-export requires --event <espn_id>")
        return 2
    _report_auto_settles(args.refresh)
    pack = export_paper_pack(event_id, path_id=_paper_path_id(args))
    print(f"paper pack: {pack}")
    print("Open PDFs in Edge, Chrome, or Adobe -- not as source in the editor.")
    return 0


def _cmd_paper_ledger(args) -> int:
    from golf_offshoot.localtime import filename_stamp
    from golf_offshoot.strategy.paper_bankroll_export import overlay_path_cash, write_bankroll_files
    from golf_offshoot.strategy.paper_book import load_paper_file
    from golf_offshoot.strategy.paper_ledger import format_ledger, load_ledger
    from golf_offshoot.strategy.paper_pack import export_paper_pack, packs_dir

    _report_auto_settles(args.refresh)
    path_id = _paper_path_id(args)
    if path_id == "polymarket":
        rec = load_paper_file(args.event, path_id=path_id) if args.event else None
        if rec is None:
            from golf_offshoot.strategy.paper_ledger import _path_record

            rec = _path_record(path_id, args.event)
        if rec is None:
            print("no polymarket paper book yet; live --book polymarket --lock-paper first")
            return 1
        ledger = overlay_path_cash(rec)
        print(format_ledger(ledger))
        if args.event:
            pack = export_paper_pack(args.event, path_id=path_id)
            print(f"paper pack: {pack}")
            return 0
        stamp = filename_stamp()
        root = packs_dir() / f"ledger_polymarket_{stamp}"
        paths = write_bankroll_files(
            root,
            ledger=ledger,
            record=rec,
            title=f"Polymarket paper bankroll — {rec.tournament_name or rec.tournament_id}",
        )
        print(f"paper pack: {root}")
        print(f"bankroll PDF: {paths.pdf}")
        return 0
    ledger = load_ledger()
    if not ledger.entries:
        print("no paper ledger yet; lock-paper or paper-deposit to start")
        return 1
    print(format_ledger(ledger))
    if args.event:
        pack = export_paper_pack(args.event)
        print(f"paper pack: {pack}")
        return 0
    stamp = filename_stamp()
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
        ledger = record_deposit(
            args.amount,
            note=args.note,
            event_id=args.event or "",
            path_id=_paper_path_id(args),
        )
    except ValueError as exc:
        print(str(exc))
        return 2
    print(format_ledger(ledger))
    if args.event:
        print(f"paper pack: {export_paper_pack(args.event, path_id=_paper_path_id(args))}")
    return 0


def _cmd_paper_withdraw(args) -> int:
    from golf_offshoot.strategy.paper_ledger import format_ledger, record_withdrawal
    from golf_offshoot.strategy.paper_pack import export_paper_pack

    if args.amount <= 0:
        print("paper-withdraw requires --amount greater than 0")
        return 2
    try:
        ledger = record_withdrawal(
            args.amount,
            note=args.note,
            event_id=args.event or "",
            path_id=_paper_path_id(args),
        )
    except ValueError as exc:
        print(str(exc))
        return 2
    print(format_ledger(ledger))
    if args.event:
        print(f"paper pack: {export_paper_pack(args.event, path_id=_paper_path_id(args))}")
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


def _cmd_paper_fill(args) -> int:
    from golf_offshoot.audit.journal import latest_event_audit
    from golf_offshoot.data_feeds.http import package_data_dir
    from golf_offshoot.data_feeds.polymarket import POLYMARKET_PATH_ID
    from golf_offshoot.strategy.fills import FillError, record_polymarket_fill
    from golf_offshoot.strategy.paper_book import format_paper_book
    from golf_offshoot.strategy.watch import last_pulls_from_state, load_watch_state, watch_state_path

    if not args.event:
        print("paper-fill requires --event <espn_id>")
        return 2
    if not args.player or args.player == "p01":
        print('paper-fill requires --player "Name"')
        return 2
    ranked_names = None
    audit = latest_event_audit(args.event, package_data_dir() / "snapshots")
    if audit is not None:
        ranked_names = {o.name: o.player_id for o in audit.outputs}
    watch = load_watch_state(watch_state_path(args.event, POLYMARKET_PATH_ID))
    pulls = last_pulls_from_state(watch)
    try:
        rec = record_polymarket_fill(
            event_id=args.event,
            player_name=args.player,
            shares=args.shares,
            fill=args.fill,
            cost=args.cost,
            market=args.market,
            ranked_names=ranked_names,
            intent=args.intent,
            pulls=pulls or None,
        )
    except FillError as exc:
        print(str(exc))
        return 2
    print("recorded polymarket fill (mock paper path; no CLOB order; not ledger.json)")
    last = rec.notes[-1] if rec.notes else ""
    if "last ntfy ADD" in last:
        print("attached to last ntfy ADD on this name+market")
    elif "last ntfy new_bet" in last or "last ntfy lock" in last:
        print("attached to last ntfy NEW on this name+market")
    elif "last ntfy" in last:
        print("attached to last ntfy pull on this name+market")
    print(format_paper_book(rec))
    return 0


def _cmd_compare_replay(args) -> int:
    from golf_offshoot.compare.replay import replay_event

    event_id = args.event or "401811962"
    hint = pinned_event_hint(event_id, settled=_event_is_settled(event_id))
    if hint:
        print(hint)
    payload = replay_event(event_id)
    print(
        f"compare-replay event={payload['event_id']} snapshots={payload['n_snapshots']} "
        f"law={payload['law_hash']}"
    )
    print(f"fights: {payload['fights']}")
    if payload.get("batch_pack"):
        print(f"batch pack: {payload['batch_pack']}")
        combo = Path(payload["batch_pack"]) / "00_full_readout.pdf"
        if combo.is_file():
            print(f"full readout: {combo}")
    for n in payload.get("notes") or []:
        print(f" - {n}")
    return 0 if payload.get("n_snapshots") else 1


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


def _cmd_watch(args) -> int:
    import time

    from golf_offshoot.data_feeds.hardrock import resolve_odds_book
    from golf_offshoot.data_feeds.polymarket import POLYMARKET_PATH_ID
    from golf_offshoot.operating import run_operating
    from golf_offshoot.strategy.live import golf_has_started
    from golf_offshoot.strategy.paper_book import load_paper_file
    from golf_offshoot.strategy.watch import (
        WatchConfigError,
        advice_for_watch,
        decide_watch,
        ensure_ntfy_topic_in_env,
        load_watch_state,
        ntfy_server,
        ntfy_topic,
        publish_ntfy,
        save_watch_state,
        serialize_pulls,
        watch_state_path,
    )

    event_id = (args.event or "").strip()
    if not event_id:
        print("watch requires --event <espn_id>")
        return 2
    book = resolve_odds_book(args.book)
    path_id = POLYMARKET_PATH_ID if book == "polymarket" else "lived"
    try:
        topic = ntfy_topic(args.ntfy_topic) if args.ntfy_topic else ensure_ntfy_topic_in_env()
    except WatchConfigError as exc:
        print(str(exc))
        return 2
    print(f"watch topic={topic}  subscribe in ntfy to {ntfy_server()}/{topic}")
    print("no packs, no PDFs, no snapshots, no paper apply, no CLOB")
    interval = max(60, int(args.interval or 600))
    pre_interval = max(60, int(args.pre_tee_interval or 1800))
    state_path = watch_state_path(event_id, path_id)
    while True:
        rec = load_paper_file(event_id, path_id=path_id)
        paper = rec.book if rec is not None else None
        bankroll = float(rec.bankroll) if rec is not None else args.bankroll
        result = run_operating(
            event_id=event_id,
            mode=RunMode.LIVE,
            sims=args.sims,
            enable_strategy=True,
            persist=False,
            refresh=True,
            bankroll=bankroll,
            odds_book=book if book != "auto" else args.book,
            open_book=paper,
            strategy_mode=StrategyMode(args.mode),
            risk=RiskPreference(args.risk),
        )
        if rec is not None:
            from golf_offshoot.strategy.fills import relink_paper_player_ids
            from golf_offshoot.strategy.paper_book import save_paper_book

            rec = relink_paper_player_ids(rec, result.ranked)
            save_paper_book(rec)
        tid = result.tournament.espn_event_id or result.tournament.tournament_id or event_id
        advice = advice_for_watch(rec, result)
        state = load_watch_state(state_path)
        decision = decide_watch(
            advice,
            result.ranked,
            event=result.tournament.name or tid,
            prev_signature=str(state.get("signature") or ""),
            armed=bool(state.get("armed")),
            arm_ping=True,
            positions=rec.book.positions if rec is not None else None,
        )
        if decision.should_ping:
            try:
                publish_ntfy(
                    decision.body,
                    topic=topic,
                    title=f"{result.tournament.name or tid}: {decision.headline}",
                    priority=decision.priority,
                    dry_run=bool(args.dry_run),
                )
            except WatchConfigError as exc:
                print(str(exc))
                return 2
            verb = "would ping" if args.dry_run else "ntfy ping"
            print(f"{verb} {decision.kind}: {decision.headline}")
        else:
            print(f"watch quiet: {decision.headline}")
        if not args.dry_run:
            payload = {
                "signature": decision.signature,
                "armed": True,
                "headline": decision.headline,
                "kind": decision.kind,
                "run_id": result.run_id,
                "last_pulls": (
                    serialize_pulls(list(decision.pulls))
                    if decision.kind == "pull"
                    else list(state.get("last_pulls") or [])
                ),
            }
            save_watch_state(state_path, payload)
        if args.once:
            return 0
        wait = interval if golf_has_started(result.ranked) else pre_interval
        print(f"next tick in {wait}s")
        try:
            time.sleep(wait)
        except KeyboardInterrupt:
            print("watch stopped")
            return 0


def _cmd_shadow(_args) -> int:
    from golf_offshoot.audit.shadow import format_shadow_review, load_shadow

    rows = load_shadow()
    print(format_shadow_review(rows))
    print(f"n={len(rows)} paper-observation only; never auto-bet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
