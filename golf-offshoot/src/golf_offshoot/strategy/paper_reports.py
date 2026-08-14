"""Full reports for players currently in the paper book.

Open positions are user-recorded. This module never places a bet.
"""

from __future__ import annotations

from pathlib import Path

from golf_offshoot.models.schemas import PlayerOutput, TournamentRunResult
from golf_offshoot.models.strategy import (
    PortfolioState,
    PositionMark,
    StrategyAction,
    StrategyPosition,
    StrategyRecommendation,
)
from golf_offshoot.ranking.report import format_player_reports, paper_table
from golf_offshoot.strategy.engine import format_recommendation
from golf_offshoot.strategy.path import mark_position


def load_paper_book(path: str | Path) -> PortfolioState:
    raw = Path(path).read_text(encoding="utf-8")
    return PortfolioState.model_validate_json(raw)


def save_paper_book(book: PortfolioState, path: str | Path) -> Path:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(book.model_dump_json(indent=2), encoding="utf-8")
    return dest


def recorded_positions(book: PortfolioState, *, include_proposed: bool = False) -> list[StrategyPosition]:
    out = []
    for p in book.positions:
        if p.proposed and not include_proposed:
            continue
        if p.stake <= 0:
            continue
        out.append(p)
    return out


def proposed_positions(rec: StrategyRecommendation | None) -> list[StrategyPosition]:
    if rec is None:
        return []
    return [p for p in rec.proposed_new_positions if p.stake > 0]


def positions_by_player(
    positions: list[StrategyPosition],
) -> dict[str, list[StrategyPosition]]:
    grouped: dict[str, list[StrategyPosition]] = {}
    for p in positions:
        grouped.setdefault(p.player_id, []).append(p)
    return grouped


def paper_rows(
    ranked: list[PlayerOutput],
    positions: list[StrategyPosition],
) -> list[PlayerOutput]:
    wanted = {p.player_id for p in positions}
    return [r for r in ranked if r.player_id in wanted]


def marks_for_positions(
    positions: list[StrategyPosition],
    ranked: list[PlayerOutput],
    rec: StrategyRecommendation | None = None,
) -> list[PositionMark]:
    by_id = {r.player_id: r for r in ranked}
    existing = {}
    if rec:
        for m in rec.marks:
            existing[m.position_id] = m
    out: list[PositionMark] = []
    for p in positions:
        if p.position_id in existing:
            out.append(existing[p.position_id])
        else:
            out.append(mark_position(p, by_id.get(p.player_id)))
    return out


def actions_for_positions(
    positions: list[StrategyPosition],
    rec: StrategyRecommendation | None,
) -> list[StrategyAction]:
    if rec is None:
        return []
    ids = {p.position_id for p in positions}
    players = {p.player_id for p in positions}
    return [
        a
        for a in rec.actions
        if (a.position_id and a.position_id in ids) or a.player_id in players
    ]


def missing_paper_players(
    positions: list[StrategyPosition],
    ranked: list[PlayerOutput],
) -> list[str]:
    have = {r.player_id for r in ranked}
    seen: list[str] = []
    for p in positions:
        if p.player_id not in have and p.player_id not in seen:
            seen.append(p.player_id)
    return seen


def format_paper_reports(
    result: TournamentRunResult,
    book: PortfolioState,
    *,
    field=None,
    include_proposed: bool = False,
) -> str:
    """Full cards for every player currently in the paper (and optional proposals)."""
    recorded = recorded_positions(book, include_proposed=False)
    extra: list[StrategyPosition] = []
    if include_proposed:
        extra = proposed_positions(result.strategy)
        already = {p.player_id for p in recorded}
        extra = [p for p in extra if p.player_id not in already]

    sections: list[str] = []
    header = [
        f"Paper reports  run_id={result.run_id}  mode={result.mode.value}  "
        f"never_auto_bet={result.never_auto_bet}",
        f"book {book.session_label or '(unlabeled)'}  "
        f"bankroll {book.bankroll:.2f}  recorded positions {len(recorded)}",
    ]
    if result.strategy:
        header.append(format_recommendation(result.strategy))
    sections.append("\n".join(header))

    if not recorded and not extra:
        sections.append(
            "No players in the current paper. "
            "Pass --paper-file with a PortfolioState JSON, or use the demo book."
        )
        return "\n\n".join(sections)

    if recorded:
        rows = paper_rows(result.ranked, recorded)
        missing = missing_paper_players(recorded, result.ranked)
        grouped = positions_by_player(recorded)
        marks = marks_for_positions(recorded, result.ranked, result.strategy)
        acts = actions_for_positions(recorded, result.strategy)
        sections.append("Paper field (recorded):")
        sections.append(paper_table(rows))
        if missing:
            sections.append("Missing from this run (not in field): " + ", ".join(missing))
        if rows:
            sections.append(
                format_player_reports(
                    rows,
                    field,
                    positions_by_player=grouped,
                    marks=marks,
                    actions=acts,
                )
            )

    if extra:
        rows = paper_rows(result.ranked, extra)
        grouped = positions_by_player(extra)
        marks = marks_for_positions(extra, result.ranked, result.strategy)
        acts = actions_for_positions(extra, result.strategy)
        sections.append("Proposed (not booked — suggestions only):")
        sections.append(paper_table(rows))
        if rows:
            sections.append(
                format_player_reports(
                    rows,
                    field,
                    positions_by_player=grouped,
                    marks=marks,
                    actions=acts,
                )
            )
    return "\n\n".join(sections)


def paper_reports_payload(
    result: TournamentRunResult,
    book: PortfolioState,
    *,
    field=None,
    include_proposed: bool = False,
) -> dict:
    """JSON-friendly dump of the same paper-scoped reports."""
    recorded = recorded_positions(book, include_proposed=include_proposed)
    if include_proposed:
        seen = {p.player_id for p in recorded_positions(book, include_proposed=False)}
        for p in proposed_positions(result.strategy):
            if p.player_id not in seen:
                recorded.append(p)
                seen.add(p.player_id)
    rows = paper_rows(result.ranked, recorded)
    by_id = {p.player.player_id: p for p in field.players} if field else {}
    grouped = positions_by_player(recorded)
    marks = marks_for_positions(recorded, result.ranked, result.strategy)
    acts = actions_for_positions(recorded, result.strategy)
    from golf_offshoot.ranking.report import input_snapshot

    players = []
    for row in rows:
        players.append(
            {
                "player": row.model_dump(mode="json"),
                "inputs": input_snapshot(by_id[row.player_id]) if row.player_id in by_id else None,
                "paper_positions": [p.model_dump(mode="json") for p in grouped.get(row.player_id, [])],
                "marks": [
                    m.model_dump(mode="json")
                    for m in marks
                    if m.player_id == row.player_id
                ],
                "actions": [
                    a.model_dump(mode="json")
                    for a in acts
                    if a.player_id == row.player_id
                ],
            }
        )
    return {
        "run_id": result.run_id,
        "mode": result.mode.value,
        "never_auto_bet": result.never_auto_bet,
        "book": book.model_dump(mode="json"),
        "missing_player_ids": missing_paper_players(recorded, result.ranked),
        "players": players,
    }
