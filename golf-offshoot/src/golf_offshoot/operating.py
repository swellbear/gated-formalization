"""Operating-path entry: real ingest, analysis, pressure test. Never mocks."""

from __future__ import annotations

import json
from pathlib import Path

from golf_offshoot.audit.shadow import format_shadow_review, load_shadow
from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.calibration.artifacts import production_alpha
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.data_feeds.ingest import RealIngestor
from golf_offshoot.models.enums import Horizon, RiskPreference, RunMode, StrategyMode
from golf_offshoot.models.schemas import SourceInventoryItem, TournamentRunResult
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.pipeline import GolfOffshootPipeline
from golf_offshoot.localtime import now_eastern_text
from golf_offshoot.ranking.display import format_table
from golf_offshoot.ranking.leftover import format_leftover_callout
from golf_offshoot.strategy.engine import format_recommendation


def format_inventory(items: list[SourceInventoryItem]) -> str:
    lines = [
        f"{'Field':<28} {'Kind':<20} {'Src':<28} {'Q':>5}  Coverage",
        "-" * 100,
    ]
    for it in items:
        q = f"{it.quality_score:.2f}" if it.quality_score is not None else "  n/a"
        lines.append(
            f"{it.field_name:<28} {it.source_kind.value:<20} {it.source_name[:27]:<28} {q:>5}  {it.coverage}"
        )
        if it.notes:
            lines.append(f"    notes: {it.notes}")
        if it.impact_if_missing:
            lines.append(f"    if missing: {it.impact_if_missing}")
    lines += [
        "",
        "Column index",
        "  Field    What input this row is about (odds, SG, weather, cut rule, ...).",
        "  Kind     Provenance: real_live, real_historical, derived_from_real, unavailable.",
        "  Src      Where that input came from this run.",
        "  Q        Quality 0-1 when scored. n/a means not scored, not zero.",
        "  Coverage How much of the field this input actually covers.",
        "  Note     Mock is forbidden on ingest/live. Unavailable means missing, not invented.",
    ]
    return "\n".join(lines)


def make_engine(*, sims: int, seed: int = 20260813) -> BayesianEngine:
    alpha, ard, note = production_alpha()
    eng = BayesianEngine(alpha=alpha, ard_scale=ard, sim=SimConfig(n_sims=sims, seed=seed))
    eng._weight_source = note  # type: ignore[attr-defined]
    return eng


def run_operating(
    *,
    event_id: str | None = None,
    mode: RunMode = RunMode.PRE_TOURNAMENT,
    sims: int = 2500,
    strategy_mode: StrategyMode = StrategyMode.STAY_SELECTIVE,
    bankroll: float = 2000.0,
    enable_strategy: bool = True,
    persist: bool = True,
    refresh: bool = False,
    include_season_stats: bool = True,
    odds_book: str = "auto",
    open_book=None,
    cashout_quotes: dict[str, float] | None = None,
    risk: RiskPreference = RiskPreference.CONSERVATIVE,
) -> TournamentRunResult:
    ingestor = RealIngestor(refresh=refresh)
    tournament, field, quotes, _inv = ingestor.ingest(
        event_id,
        mode=mode,
        include_season_stats=include_season_stats,
        include_odds=True,
        odds_book=odds_book,
    )
    if open_book is None:
        from golf_offshoot.data_feeds.hardrock import resolve_odds_book
        from golf_offshoot.strategy.paper_book import load_paper_book, load_paper_file

        tid = tournament.espn_event_id or tournament.tournament_id
        if tid and resolve_odds_book(odds_book) == "polymarket":
            rec = load_paper_file(tid, path_id="polymarket")
            open_book = rec.book if rec else None
        else:
            open_book = load_paper_book(tid) if tid else None
    snap = package_data_dir() / "snapshots"
    engine = make_engine(sims=sims)
    tid = tournament.espn_event_id or tournament.tournament_id
    from golf_offshoot.compare.paths import allowed_bets_for_quotes

    strat = StrategyConfig(
        enabled=enable_strategy,
        mode=strategy_mode,
        risk=risk,
        bankroll=bankroll,
        allowed_bet_types=allowed_bets_for_quotes(tid, quotes),
    )
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=snap, strategy_config=strat)
    previous = None
    if mode == RunMode.LIVE:
        from golf_offshoot.audit.journal import latest_pre_audit

        tid = tournament.espn_event_id or tournament.tournament_id
        previous = latest_pre_audit(tid, snap)
    result = pipe.run(
        tournament,
        field,
        market_quotes=quotes if quotes else None,
        persist=persist,
        previous=previous,
        open_book=open_book,
        cashout_quotes=cashout_quotes,
    )
    result.audit.extra["weight_source"] = getattr(engine, "_weight_source", "")
    result.audit.extra["weather_summary"] = field.weather_summary
    result.audit.extra["odds_book"] = field.extra.get("odds_book") if field.extra else odds_book
    result.audit.extra["bankroll"] = bankroll
    if previous is not None:
        result.audit.extra["movement_baseline_run_id"] = previous.run_id
    if persist:
        from golf_offshoot.audit.journal import save_audit
        from golf_offshoot.ranking.export_table import export_operating_table

        paths = export_operating_table(
            result,
            baseline=previous.outputs if previous else None,
            baseline_run_id=previous.run_id if previous else None,
        )
        result.audit.extra["export_pdf"] = str(paths.pdf)
        result.audit.extra["export_html"] = str(paths.html)
        result.audit.extra["export_txt"] = str(paths.txt)
        if result.mode == RunMode.LIVE:
            from golf_offshoot.ranking.export_leaderboard import export_live_leaderboard

            held = set()
            if open_book is not None:
                held = {p.player_id for p in open_book.positions}
            lb = export_live_leaderboard(result, held_ids=held)
            if lb:
                result.audit.extra["export_leaderboard_pdf"] = str(lb.pdf)
                result.audit.extra["export_leaderboard_html"] = str(lb.html)
                result.audit.extra["export_leaderboard_txt"] = str(lb.txt)
        save_audit(result.audit, snap)
    return result


def run_strategy_modes(
    result_base: TournamentRunResult,
    bankroll: float = 2000.0,
    risk: RiskPreference = RiskPreference.CONSERVATIVE,
) -> dict[str, str]:
    from golf_offshoot.audit.shadow import append_shadow_advises
    from golf_offshoot.compare.paths import allowed_bets_from_rows
    from golf_offshoot.strategy.engine import run_strategy

    out = {}
    operating = bool(result_base.audit.extra.get("operating"))
    tid = result_base.tournament.espn_event_id or result_base.tournament.tournament_id
    allowed = allowed_bets_from_rows(tid, result_base.ranked)
    for mode in (StrategyMode.PROTECT_PROFITS, StrategyMode.PRESS_EDGES, StrategyMode.STAY_SELECTIVE):
        cfg = StrategyConfig(
            enabled=True,
            mode=mode,
            bankroll=bankroll,
            risk=risk,
            allowed_bet_types=allowed,
        )
        rec = run_strategy(result_base.ranked, cfg, run_mode=result_base.mode)
        out[mode.value] = format_recommendation(rec)
        if operating:
            tmp = result_base.model_copy(update={"strategy": rec})
            append_shadow_advises(tmp)
    return out


def coherence_notes(result: TournamentRunResult) -> list[str]:
    notes = []
    n_bad = 0
    for row in result.ranked:
        chain = [
            row.probabilities.p(Horizon.WIN).central,
            row.probabilities.p(Horizon.TOP_5).central,
            row.probabilities.p(Horizon.TOP_10).central,
            row.probabilities.p(Horizon.TOP_20).central,
            row.probabilities.p(Horizon.MAKE_CUT).central,
        ]
        for a, b in zip(chain, chain[1:]):
            if a > b + 1e-6:
                n_bad += 1
                break
        w = row.probabilities.p(Horizon.WIN)
        if w.low > w.central + 1e-9 or w.high < w.central - 1e-9:
            n_bad += 1
    if n_bad:
        notes.append(f"{n_bad} players failed horizon coherence or range nesting")
    else:
        notes.append("All displayed centrals satisfy Win ≤ T5 ≤ T10 ≤ T20 ≤ Make Cut")
    edges = [r.edge_by_bet.get("win") for r in result.ranked if r.edge_by_bet.get("win") is not None]
    if not edges:
        notes.append("No win edges: market odds unavailable (not mocked)")
    else:
        notes.append(f"{len(edges)} players have win edges; max {max(edges):+.3f} min {min(edges):+.3f}")
    rel = [r.reliability.score for r in result.ranked]
    notes.append(f"Reliability median {sorted(rel)[len(rel)//2]:.2f} min {min(rel):.2f}")
    return notes


def pressure_report_path(event_id: str | None) -> Path:
    """Per-event pressure artifact. Does not overwrite the named St. Jude file."""
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(event_id or "event"))
    return package_data_dir().parent / "docs" / f"PRESSURE_TEST_{safe}.md"


def write_pressure_report(
    result: TournamentRunResult,
    *,
    inventory: list[SourceInventoryItem],
    strategy_blocks: dict[str, str],
    live: TournamentRunResult | None,
    calib_summary: dict | None,
    path: Path | None = None,
    live_strategy_blocks: dict[str, str] | None = None,
    open_book=None,
) -> Path:
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    path = path or pressure_report_path(tid)
    top = result.ranked[:12]
    explains = []
    for row in result.ranked[:5]:
        sg_bits = []
        if row.explain:
            for c in row.explain.contributions:
                if c.factor_id in (
                    "sg_match",
                    "approach_sg",
                    "around_green",
                    "putting",
                    "recent_form",
                ) and abs(c.delta_theta) > 1e-6:
                    sg_bits.append(f"{c.factor_id} dtheta={c.delta_theta:+.3f} q={c.quality:.2f}")
        explains.append(
            f"### {row.rank}. {row.name}\n\n"
            f"- Win {row.probabilities.p(Horizon.WIN).central:.3f} "
            f"[{row.probabilities.p(Horizon.WIN).low:.3f}, {row.probabilities.p(Horizon.WIN).high:.3f}]\n"
            f"- T10 {row.probabilities.p(Horizon.TOP_10).central:.3f} "
            f"Make cut {row.probabilities.p(Horizon.MAKE_CUT).central:.3f}\n"
            f"- Reliability {row.reliability.score:.2f} ({', '.join(row.reliability.reasons) or '—'})\n"
            f"- Posted win odds: {row.posted_odds_by_bet.get('win', 'unavailable')}\n"
            f"- Posted top-5 odds: {row.posted_odds_by_bet.get('top_5', 'unavailable')}\n"
            f"- Posted top-10 odds: {row.posted_odds_by_bet.get('top_10', 'unavailable')}\n"
            f"- Posted top-20 odds: {row.posted_odds_by_bet.get('top_20', 'unavailable')}\n"
            f"- Posted make-cut odds: {row.posted_odds_by_bet.get('make_cut', 'unavailable')}\n"
            f"- Fair implied win: {row.market_implied_by_bet.get('win')}\n"
            f"- Edge vs fair win: {row.edge_by_bet.get('win')}\n"
            f"- Edge vs fair top-5: {row.edge_by_bet.get('top_5', 'unavailable')}\n"
            f"- Edge vs fair top-10: {row.edge_by_bet.get('top_10', 'unavailable')}\n"
            f"- Edge vs fair top-20: {row.edge_by_bet.get('top_20', 'unavailable')}\n"
            f"- Edge vs fair make-cut: {row.edge_by_bet.get('make_cut', 'unavailable')}\n"
            f"- SG factors: {'; '.join(sg_bits) or 'none active in Δθ'}\n"
            f"- Open: {'; '.join(row.open_questions[:4]) or '—'}\n"
            f"- Flags: {', '.join(row.flags) or 'none'}\n"
            f"- {row.explain.narrative if row.explain else ''}\n"
        )
    edge_rows = sorted(
        (r for r in result.ranked if r.edge_by_bet.get("win") is not None),
        key=lambda r: r.edge_by_bet.get("win") or 0.0,
        reverse=True,
    )[:10]
    edge_lines = [
        f"{r.rank:3d} {r.name:<22} model={r.probabilities.p(Horizon.WIN).central:.3f} "
        f"fair={r.market_implied_by_bet.get('win', float('nan')):.3f} "
        f"posted={r.posted_odds_by_bet.get('win', float('nan')):.2f} "
        f"edge_fair={r.edge_by_bet.get('win', 0):+.3f}"
        for r in edge_rows
    ]
    def _edge_block(bet: str, horizon: Horizon, n: int = 8) -> list[str]:
        rows = sorted(
            (r for r in result.ranked if r.edge_by_bet.get(bet) is not None),
            key=lambda r: r.edge_by_bet.get(bet) or 0.0,
            reverse=True,
        )[:n]
        if not rows:
            return [f"{bet} coupon unavailable (not synthesized from winner odds)"]
        return [
            f"{r.rank:3d} {r.name:<22} model={r.probabilities.p(horizon).central:.3f} "
            f"fair={r.market_implied_by_bet.get(bet, float('nan')):.3f} "
            f"posted={r.posted_odds_by_bet.get(bet, float('nan')):.2f} "
            f"edge_fair={r.edge_by_bet.get(bet, 0):+.3f}"
            for r in rows
            if horizon in r.probabilities.horizons
        ]

    t5_lines = _edge_block("top_5", Horizon.TOP_5)
    t10_lines = _edge_block("top_10", Horizon.TOP_10)
    t20_lines = _edge_block("top_20", Horizon.TOP_20)
    mc_lines = _edge_block("make_cut", Horizon.MAKE_CUT)
    r1_lines = _edge_block("win_after_r1", Horizon.WIN_AFTER_R1)
    r2_lines = _edge_block("win_after_r2", Horizon.WIN_AFTER_R2)
    r3_lines = _edge_block("win_after_r3", Horizon.WIN_AFTER_R3)
    cov = result.audit.extra.get("market_coverage") or {}
    lines = [
        "# Pressure test — 2026 FedEx St. Jude Championship",
        "",
        f"As of {now_eastern_text(with_seconds=True)}. **Never auto-bet.** Operating path only (no mocks). Model `{result.audit.model.version_id if result.audit.model else ''}`",
        "",
        f"- Tournament: **{result.tournament.name}** (`{result.tournament.tournament_id}`)",
        f"- Course: {result.tournament.course.name} · par {result.tournament.course.par} · {result.tournament.course.yardage} yd",
        f"- Cut: {'yes' if result.tournament.has_cut else 'no (playoff field)'} · start {result.tournament.start_date}",
        f"- Run: `{result.run_id}` mode={result.mode.value}",
        f"- Weights: {result.audit.extra.get('weight_source', '')}",
        f"- Weather: {result.audit.extra.get('weather_summary', '')}",
        f"- Odds quotes: {result.audit.extra.get('odds_quotes', 0)} · overround: {result.audit.extra.get('overround', {})}",
        f"- SG coverage: {result.audit.extra.get('sg_players', 0)}/{result.audit.extra.get('sg_field', 0)}",
        f"- Recent-SG feature players: {result.audit.extra.get('recent_sg_feature_players', 0)}",
        f"- recent_form board from as-of: {result.audit.extra.get('recent_form_board_from_asof', 0)}",
        f"- recent_form dtheta players: {result.audit.extra.get('recent_form_delta_theta_players', 0)}",
        f"- Opening quotes: {result.audit.extra.get('opening_quotes', 0)}",
        "",
        "## Source inventory",
        "",
        "```",
        format_inventory(inventory),
        "```",
        "",
        "## Ranked field (top 12)",
        "",
        "```",
        format_table(top, n=12),
        "```",
        "",
        "## Real market edges (top 10 vs de-juiced win)",
        "",
        "Proportional de-juice: `implied_fair = implied_raw / Σ implied_raw`. "
        "Decision/strategy still require beating the **posted** decimal (`model_p > 1/odds`). "
        "Unmatched players have no invented price.",
        "",
        "```",
        "\n".join(edge_lines) or "no win quotes",
        "```",
        "",
        "## Place / finish market coverage",
        "",
        "Winner, place, and after-round markets stay separated. "
        "Place and after-round prices are never synthesized from winner odds. "
        "Opening lines are counted only when a distinct prematch coupon exists beside the current price.",
        "",
        "```json",
        json.dumps(cov, indent=2) if cov else '{"available_markets": [], "unavailable_markets": ["win", "top_5", "top_10", "top_20", "make_cut"]}',
        "```",
        "",
        "### Top 5",
        "",
        "```",
        "\n".join(t5_lines),
        "```",
        "",
        "### Top 10",
        "",
        "```",
        "\n".join(t10_lines),
        "```",
        "",
        "### Top 20",
        "",
        "```",
        "\n".join(t20_lines),
        "```",
        "",
        "### Make cut",
        "",
        "```",
        "\n".join(mc_lines),
        "```",
        "",
        "### Win after round 1",
        "",
        "```",
        "\n".join(r1_lines),
        "```",
        "",
        "### Win after round 2",
        "",
        "```",
        "\n".join(r2_lines),
        "```",
        "",
        "### Win after round 3",
        "",
        "```",
        "\n".join(r3_lines),
        "```",
        "",
        "## Coherence / edges / reliability",
        "",
    ]
    for n in coherence_notes(result):
        lines.append(f"- {n}")
    lines += ["", "## Explainability (top 5)", ""]
    lines.extend(explains)
    lines += ["", "## Strategy layer (advisory, sample bankroll $2000)", ""]
    for mode, block in strategy_blocks.items():
        lines += [f"### {mode}", "", "```", block, "```", ""]
    lines += [
        "## Leftover callout (display only)",
        "",
        "Used vs unconstrained vs held-ticket residual. Not a GPF menu. Do not stuff into theta.",
        "",
        "```",
        format_leftover_callout(result),
        "```",
        "",
    ]
    if live:
        live_pos = []
        for row in live.ranked[:8]:
            live_pos.append(
                f"{row.rank}. {row.name} win={row.probabilities.p(Horizon.WIN).central:.3f} "
                f"edge={row.edge_by_bet.get('win')}"
            )
        kit = next((r for r in live.ranked if "kitayama" in r.name.lower()), None)
        kit_pre = next((r for r in result.ranked if "kitayama" in r.name.lower()), None)
        lines += [
            "## Live update (round in progress, hole-dampened)",
            "",
            "Formula: until 18 holes, `dampen = (h/H) × (h/18)`; after 18 holes `dampen = h/H` "
            "with `H = 72`. `live_position` evidence = `(-score/3) × dampen`, quality = "
            "`0.30 + 0.65 × (h/H)`. Remaining score = current to-par + `(-θ × rem_rounds)` "
            "+ `N(0, σ √rem_rounds)`. Prior un-dampened live run put Kitayama near 26% win "
            "from a Round-1 board; this run must not repeat that.",
            "",
            f"- Live run `{live.run_id}`",
            f"- Kitayama pre Win {kit_pre.probabilities.p(Horizon.WIN).central:.3f}" if kit_pre else "- Kitayama not in pre field",
            f"- Kitayama live Win {kit.probabilities.p(Horizon.WIN).central:.3f} rank {kit.rank}" if kit else "- Kitayama not in live field",
            f"- Live odds freshness: {live.audit.extra.get('odds_freshness', '')}",
            f"- Pre odds freshness: {result.audit.extra.get('odds_freshness', '')}",
            f"- Movement baseline (pre run): `{result.run_id}` "
            "(dRnk + = climbed vs that ingest; not opening-line movement)",
            "```",
            format_table(live.ranked[:8], n=8, baseline=result.ranked),
            "```",
            "",
        ]
        lines += ["### Pre vs live posted win (stale vs refreshed)", "", "```"]
        lines += _odds_refresh_example(result, live)
        lines += ["```", ""]
        if live.strategy:
            lines += ["```", format_recommendation(live.strategy), "```", ""]
        if live_strategy_blocks:
            lines += ["### Live strategy modes (empty book, advisory)", ""]
            for mode, block in live_strategy_blocks.items():
                lines += [f"#### {mode}", "", "```", block, "```", ""]
        lines += [
            "### Live leftover callout",
            "",
            "```",
            format_leftover_callout(live, open_book),
            "```",
            "",
        ]
    shadow_rows = load_shadow()
    lines += [
        "## Shadow journal (paper observation only)",
        "",
        "Logged `new_bet` / `add` / `reduce` / `exit` / `reallocate` advises. Never auto-bet. "
        "Review later with `python -m golf_offshoot shadow`.",
        "",
        "```",
        format_shadow_review(shadow_rows, n=20),
        "```",
        "",
        "## Recalibration decision",
        "",
        "0.7.0 may run Bayesian search + ARD only when the leakage-safe as-of recent SG "
        "panel is materially stronger than calib-v2 (median measured EVENT_ONLY events "
        ">= 5 or coverage >= 85%) and coverage still clears 30%. A weak 16-week request "
        "is not a reason to rerun BO. Finish-only refits are still forbidden. "
        "`calib-v1`/`calib-v2` remain stored. Production uses calibrated weights only if "
        "the new artifact says `use_calibrated`.",
        "",
    ]
    asof = result.audit.extra.get("asof_coverage") or {}
    if asof:
        lines += [
            "## As-of SG coverage (this event)",
            "",
            "```json",
            json.dumps(asof, indent=2),
            "```",
            "",
        ]
    if calib_summary:
        lines += [
            "```json",
            json.dumps(
                {
                    "recommendation": calib_summary.get("recommendation"),
                    "search_ran": calib_summary.get("search_ran", calib_summary.get("n_evals", 0) not in (None, 0)),
                    "n_evals": calib_summary.get("n_evals"),
                    "holdout": (calib_summary.get("metrics") or {}).get("holdout_fitted"),
                    "holdout_expert": (calib_summary.get("metrics") or {}).get("holdout_expert"),
                    "bounds_hit": calib_summary.get("bounds_hit"),
                    "train_event_ids": calib_summary.get("train_event_ids"),
                    "holdout_event_ids": calib_summary.get("holdout_event_ids"),
                    "notes": calib_summary.get("notes"),
                    "asof_coverage": (calib_summary.get("extra") or {}).get("asof_coverage"),
                    "fitted_keys": (calib_summary.get("extra") or {}).get("fitted_keys"),
                },
                indent=2,
            ),
            "```",
            "",
        ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _odds_refresh_example(pre: TournamentRunResult, live: TournamentRunResult) -> list[str]:
    """Show posted win decimals before vs after the live odds pass."""
    pre_map = {r.player_id: r for r in pre.ranked}
    names = []
    for needle in ("scheffler", "fitzpatrick", "kitayama", "fleetwood"):
        row = next((r for r in live.ranked if needle in r.name.lower()), None)
        if row:
            names.append(row)
    if not names:
        names = live.ranked[:4]
    out = ["player                         pre_posted  live_posted  pre_model  live_model"]
    for row in names[:6]:
        old = pre_map.get(row.player_id)
        pre_p = old.posted_odds_by_bet.get("win") if old else None
        live_p = row.posted_odds_by_bet.get("win")
        pre_m = old.probabilities.p(Horizon.WIN).central if old else float("nan")
        live_m = row.probabilities.p(Horizon.WIN).central
        moved = ""
        if pre_p and live_p and abs(pre_p - live_p) > 1e-9:
            moved = " REFRESHED"
        elif pre_p and live_p:
            moved = " same_number"
        out.append(
            f"{row.name:<28} {pre_p if pre_p else 'n/a':>10} {live_p if live_p else 'n/a':>12} "
            f"{pre_m:9.3f} {live_m:10.3f}{moved}"
        )
    out.append(
        "Live pass uses a 45s odds TTL so a Winner coupon cached from pre "
        "(10 min TTL) is refetched when it can be. If this live ingest ran "
        "within 45s of pre, a cache hit is expected and is not the old 10-min "
        "reuse bug. If refresh fails, prices older than 15 min are suppressed "
        "rather than treated as live."
    )
    return out
