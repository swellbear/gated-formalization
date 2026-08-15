"""Live compare: one ingest, two MCs, four strategy ledgers. Never mutates lived lock."""

from __future__ import annotations

from golf_offshoot.compare.apply import maybe_apply_paper
from golf_offshoot.compare.fights import fights_at, load_path_views, write_fights
from golf_offshoot.compare.law import METHOD_LAW_V1, law_hash
from golf_offshoot.compare.paths import ComparePath, config_for, ledger_id
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.enums import RunMode, RiskPreference, StrategyMode
from golf_offshoot.models.schemas import FieldSnapshot, Tournament, TournamentRunResult
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.operating import make_engine
from golf_offshoot.pipeline import GolfOffshootPipeline
from golf_offshoot.strategy.engine import run_strategy
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    advice_from_recommendation,
    load_paper_book,
    load_paper_file,
    lock_paper_positions,
    save_paper_book,
)


def _copy_field(field: FieldSnapshot) -> FieldSnapshot:
    return field.model_copy(deep=True)


def run_theta(
    tournament: Tournament,
    field: FieldSnapshot,
    quotes,
    *,
    honest: bool,
    sims: int,
    persist: bool,
    strategy_config: StrategyConfig,
    open_book=None,
    previous=None,
    cashout_quotes=None,
    compare_path: str = "",
) -> TournamentRunResult:
    engine = make_engine(sims=sims)
    snap = package_data_dir() / "snapshots"
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=snap, strategy_config=strategy_config)
    pipe.honest = bool(honest)
    result = pipe.run(
        tournament,
        _copy_field(field),
        market_quotes=quotes if quotes else None,
        persist=persist,
        previous=previous,
        open_book=open_book,
        cashout_quotes=cashout_quotes,
        strategy_config=strategy_config,
    )
    if compare_path:
        result.audit.extra["compare_path"] = compare_path
    result.audit.extra["honest_theta"] = bool(honest)
    result.audit.extra["method_law_hash"] = law_hash()
    if persist:
        from golf_offshoot.audit.journal import save_audit

        save_audit(result.audit, snap)
    return result


def _sync_path_book(
    *,
    event_id: str,
    event_name: str,
    path: ComparePath,
    rows,
    run_id: str,
    odds_book: str,
    run_mode: RunMode,
    write_exports: bool = True,
) -> tuple[PaperBookFile, bool]:
    pid = ledger_id(path)
    cfg = config_for(path, event_id=event_id)
    existing = load_paper_file(event_id, path_id=pid)
    if existing is None:
        from golf_offshoot.strategy.paper_book import paper_candidate_slots

        slots = paper_candidate_slots(
            rows,
            cfg,
            require_cleared=cfg.ticket_screen == "posted",
        )
        if not slots:
            return existing, False
        rec = lock_paper_positions(
            rows,
            cfg,
            event_id=event_id,
            event_name=event_name,
            run_id=run_id,
            odds_book=odds_book,
            path_id=pid,
            independent_bankroll=True,
            write_exports=write_exports,
            method_law_hash=law_hash(),
            require_cleared=cfg.ticket_screen == "posted",
        )
        return rec, True
    rec_strat = run_strategy(rows, cfg, run_mode=run_mode, book=existing.book)
    advice = advice_from_recommendation(existing, rec_strat, run_id=run_id)
    record, applied = maybe_apply_paper(existing, advice)
    save_paper_book(record)
    return record, applied


def run_compare_method(
    *,
    event_id: str | None,
    sims: int = 1500,
    refresh: bool = False,
    odds_book: str = "bovada",
    persist: bool = True,
    include_season_stats: bool = True,
    lived_strategy_config: StrategyConfig | None = None,
    lived_open_book=None,
    cashout_quotes=None,
    write_exports: bool = True,
) -> dict:
    """Ingest once. Lived/A θ and B-guts θ share the engine seed. Four compare books."""
    from golf_offshoot.audit.journal import latest_pre_audit
    from golf_offshoot.data_feeds.ingest import RealIngestor

    ingestor = RealIngestor(refresh=refresh)
    tournament, field, quotes, _inv = ingestor.ingest(
        event_id,
        mode=RunMode.LIVE,
        include_season_stats=include_season_stats,
        include_odds=True,
        odds_book=odds_book,
    )
    tid = tournament.espn_event_id or tournament.tournament_id
    previous = latest_pre_audit(tid, package_data_dir() / "snapshots")
    lived_cfg = lived_strategy_config or StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=float(METHOD_LAW_V1["independent_compare_bankroll"]),
        ticket_screen="both",
        never_auto_bet=True,
    )
    if lived_open_book is None:
        lived_open_book = load_paper_book(tid)
    lived_result = run_theta(
        tournament,
        field,
        quotes,
        honest=False,
        sims=sims,
        persist=persist,
        strategy_config=lived_cfg,
        open_book=lived_open_book,
        previous=previous,
        cashout_quotes=cashout_quotes,
        compare_path="",
    )
    lived_result.audit.extra["weight_source"] = getattr(
        lived_result, "_weight_source", lived_result.audit.extra.get("weight_source", "")
    )
    lived_result.audit.extra["odds_book"] = field.extra.get("odds_book") if field.extra else odds_book
    lived_result.audit.extra["bankroll"] = lived_cfg.bankroll
    if persist:
        from golf_offshoot.audit.journal import save_audit
        from golf_offshoot.ranking.export_table import export_operating_table

        paths = export_operating_table(
            lived_result,
            baseline=previous.outputs if previous else None,
            baseline_run_id=previous.run_id if previous else None,
        )
        lived_result.audit.extra["export_pdf"] = str(paths.pdf)
        lived_result.audit.extra["export_html"] = str(paths.html)
        lived_result.audit.extra["export_txt"] = str(paths.txt)
        if lived_result.mode == RunMode.LIVE:
            from golf_offshoot.ranking.export_leaderboard import export_live_leaderboard

            held = {p.player_id for p in lived_open_book.positions} if lived_open_book is not None else set()
            lb = export_live_leaderboard(lived_result, held_ids=held)
            if lb:
                lived_result.audit.extra["export_leaderboard_pdf"] = str(lb.pdf)
                lived_result.audit.extra["export_leaderboard_html"] = str(lb.html)
                lived_result.audit.extra["export_leaderboard_txt"] = str(lb.txt)
        save_audit(lived_result.audit, package_data_dir() / "snapshots")

    notes: list[str] = []
    guts_cfg = config_for(ComparePath.B_GUTS, event_id=str(tid))
    guts_result = run_theta(
        tournament,
        field,
        quotes,
        honest=True,
        sims=sims,
        persist=persist,
        strategy_config=guts_cfg,
        previous=None,
        compare_path=ComparePath.B_GUTS.value,
    )

    a_rows = lived_result.ranked
    b_rows = guts_result.ranked
    book_odds = str(lived_result.audit.extra.get("odds_book") or odds_book)
    applied: dict[str, bool] = {}
    for path, rows, run_id in (
        (ComparePath.A_REPLAY, a_rows, lived_result.run_id),
        (ComparePath.B_NERVES, a_rows, lived_result.run_id),
        (ComparePath.B_GUTS, b_rows, guts_result.run_id),
        (ComparePath.B_FULL, b_rows, guts_result.run_id),
    ):
        _rec, did = _sync_path_book(
            event_id=str(tid),
            event_name=tournament.name,
            path=path,
            rows=rows,
            run_id=run_id,
            odds_book=book_odds,
            run_mode=lived_result.mode,
            write_exports=False,
        )
        applied[ledger_id(path)] = did

    views = load_path_views(str(tid))
    events = fights_at(
        views,
        as_of=str(lived_result.audit.as_of),
        run_id=lived_result.run_id,
        live_outputs=lived_result.ranked,
        event_id=str(tid),
    )
    fights_path = write_fights(
        str(tid),
        event_name=tournament.name,
        views=views,
        events=events,
        extra_notes=notes + [f"applied={applied}", f"law_hash={law_hash()}"],
        live_outputs=lived_result.ranked,
    )
    return {
        "event_id": str(tid),
        "lived_result": lived_result,
        "guts_result": guts_result,
        "lived_run_id": lived_result.run_id,
        "guts_run_id": guts_result.run_id,
        "fights": str(fights_path),
        "applied": applied,
        "notes": notes,
        "law_hash": law_hash(),
        "bankroll": METHOD_LAW_V1["independent_compare_bankroll"],
        "never_auto_bet": True,
    }
