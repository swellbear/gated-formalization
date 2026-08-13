"""Ranked field display. Always includes range, confidence, edge, reliability, open questions."""

from __future__ import annotations

from golf_offshoot.bayesian_engine.updates import ThetaState
from golf_offshoot.market.odds import edges_for_player
from golf_offshoot.models.enums import Horizon
from golf_offshoot.models.schemas import (
    FieldSnapshot,
    MarketSnapshot,
    PlayerOutput,
    ProbabilityBundle,
)
from golf_offshoot.ranking.explain import explain_player
from golf_offshoot.ranking.reliability import reliability_for


def rank_field(
    field: FieldSnapshot,
    bundles: dict[str, ProbabilityBundle],
    thetas: dict[str, ThetaState],
    market: MarketSnapshot | None = None,
    flags: dict[str, list[str]] | None = None,
    borrow_notes: dict[str, list[str]] | None = None,
    field_notes: dict[str, str] | None = None,
    prev_theta: dict[str, float] | None = None,
) -> list[PlayerOutput]:
    flags = flags or {}
    borrow_notes = borrow_notes or {}
    field_notes = field_notes or {}
    prev_theta = prev_theta or {}
    by_id = {p.player.player_id: p for p in field.players}
    rows: list[PlayerOutput] = []
    for pid, bundle in bundles.items():
        p = by_id[pid]
        th = thetas[pid]
        rel = reliability_for(p, prev_theta.get(pid), th.mean)
        edge, implied = ({}, {})
        if market:
            edge, implied = edges_for_player(bundle, market)
        expl = explain_player(
            p,
            th,
            borrowed=borrow_notes.get(pid, []),
            field_note=field_notes.get(pid, ""),
        )
        rows.append(
            PlayerOutput(
                player_id=pid,
                name=p.player.name,
                rank=0,
                probabilities=bundle,
                reliability=rel,
                edge_by_bet=edge,
                market_implied_by_bet=implied,
                open_questions=expl.open_questions,
                flags=flags.get(pid, []),
                explain=expl,
            )
        )
    rows.sort(key=lambda r: r.probabilities.p(Horizon.WIN).central, reverse=True)
    for i, r in enumerate(rows, start=1):
        r.rank = i
    return rows


def format_table(rows: list[PlayerOutput], n: int = 25) -> str:
    lines = [
        f"{'#':>3} {'Player':<22} {'Win':>10} {'T10':>10} {'Cut':>10} {'EdgeW':>8} {'Rel':>5} {'Flags'}",
        "-" * 88,
    ]
    for r in rows[:n]:
        w = r.probabilities.p(Horizon.WIN)
        t10 = r.probabilities.p(Horizon.TOP_10)
        cut = r.probabilities.p(Horizon.MAKE_CUT)
        ew = r.edge_by_bet.get("win")
        edge_s = f"{ew:+.3f}" if ew is not None else "  n/a"
        flag = ",".join(r.flags[:2]) if r.flags else ""
        win_s = f"{w.central:.3f}[{w.low:.2f}-{w.high:.2f}]"
        lines.append(
            f"{r.rank:3d} {r.name:<22} {win_s:>10} {t10.central:10.3f} {cut.central:10.3f} "
            f"{edge_s:>8} {r.reliability.score:5.2f} {flag}"
        )
    return "\n".join(lines)
