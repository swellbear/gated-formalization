"""Ranked field display. Always includes range, confidence, edge, reliability, open questions."""

from __future__ import annotations

from dataclasses import dataclass

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
        posted = {}
        if market:
            edge, implied, posted = edges_for_player(bundle, market)
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
                posted_odds_by_bet=posted,
                open_questions=expl.open_questions,
                flags=flags.get(pid, []),
                explain=expl,
                live_score_to_par=p.live_score_to_par,
                live_holes_completed=p.live_holes_completed,
                live_place=p.live_place,
                live_place_display=p.live_place_display,
                live_status_name=p.live_status_name,
                live_made_cut=p.live_made_cut,
                withdrawn=p.withdrawn,
            )
        )
    rows.sort(key=lambda r: r.probabilities.p(Horizon.WIN).central, reverse=True)
    for i, r in enumerate(rows, start=1):
        r.rank = i
    return rows


def movement_note(baseline_run_id: str | None) -> str:
    """Caption for live tables. ASCII only — Windows cp1252 cannot print Delta."""
    if not baseline_run_id:
        return (
            "no pre-tournament snapshot for this event; "
            "run ingest first to show dWin / Pre# / dRnk"
        )
    return (
        f"movement vs pre-tournament snapshot {baseline_run_id} "
        "(dRnk + = climbed; dWin + = Win% up). Not opening-line movement."
    )


def column_index_items(*, show_move: bool = False, show_t10: bool = False) -> list[tuple[str, str]]:
    """Plain-language index for columns actually printed. ASCII only."""
    items: list[tuple[str, str]] = [
        ("#", "Rank by Win central. #1 is the highest Win%, not the best bet."),
        ("Player", "Player name on this field."),
        ("Win", "Chance they win. First number is the central estimate; [low-high] is the range."),
    ]
    if show_move:
        items.extend(
            [
                ("dWin", "Live Win central minus pre-ingest Win. Plus means up. Not opening-line movement."),
                ("Pre#", "Their rank on that pre-tournament ingest."),
                ("dRnk", "Pre rank minus live rank. Plus means climbed (18 to 3 is +15)."),
            ]
        )
    items.extend(
        [
            ("T10", "Chance they finish top 10 (central)."),
            ("Cut", "Chance they make the cut (central). No-cut fields stay near 1.00 except WD."),
            ("EdgeW", "Model Win minus the book's fair Win%. Not a ticket. n/a = no matching price."),
        ]
    )
    if show_t10:
        items.append(("EdgeT10", "Same as EdgeW for a real top-10 coupon when one is listed."))
    items.extend(
        [
            ("Rel", "Trust in the inputs (0-1). Not how tight the Win range is."),
            ("Flags", "Warnings. sparse_data and thin_sample_overconfidence are hard passes."),
            ("n/a", "Missing or unmatched. Not the same as zero."),
            ("Note", "Observation only. The system never auto-bets."),
        ]
    )
    return items


def format_column_index(*, show_move: bool = False, show_t10: bool = False) -> str:
    lines = ["Column index"]
    for name, meaning in column_index_items(show_move=show_move, show_t10=show_t10):
        lines.append(f"  {name:<8} {meaning}")
    return "\n".join(lines)


@dataclass(frozen=True)
class RankedTableView:
    show_move: bool
    show_t10: bool
    headers: tuple[str, ...]
    aligns: tuple[str, ...]
    rows: list[list[str]]
    glossary: list[tuple[str, str]]


def ranked_table_view(
    rows: list[PlayerOutput],
    n: int | None = None,
    baseline: list[PlayerOutput] | None = None,
) -> RankedTableView:
    show_t10 = any(r.edge_by_bet.get("top_10") is not None or r.posted_odds_by_bet.get("top_10") for r in rows)
    show_move = baseline is not None
    pre_by_id = {o.player_id: o for o in baseline} if show_move else {}
    headers = ["#", "Player", "Win"]
    aligns = ["right", "left", "right"]
    if show_move:
        headers += ["dWin", "Pre#", "dRnk"]
        aligns += ["right", "right", "right"]
    headers += ["T10", "Cut", "EdgeW"]
    aligns += ["right", "right", "right"]
    if show_t10:
        headers.append("EdgeT10")
        aligns.append("right")
    headers += ["Rel", "Flags"]
    aligns += ["right", "left"]
    body: list[list[str]] = []
    take = rows if n is None else rows[:n]
    for r in take:
        w = r.probabilities.p(Horizon.WIN)
        t10 = r.probabilities.p(Horizon.TOP_10)
        cut = r.probabilities.p(Horizon.MAKE_CUT)
        cells = [
            str(r.rank),
            r.name,
            _win_cell(w),
        ]
        if show_move:
            pre = pre_by_id.get(r.player_id)
            if pre is None:
                cells.extend(["n/a", "n/a", "n/a"])
            else:
                d_win = w.central - pre.probabilities.p(Horizon.WIN).central
                cells.extend([f"{d_win:+.3f}", str(pre.rank), f"{pre.rank - r.rank:+d}"])
        cells.extend(
            [
                f"{t10.central:.3f}",
                f"{cut.central:.3f}",
                f"{r.edge_by_bet.get('win'):+.3f}" if r.edge_by_bet.get("win") is not None else "n/a",
            ]
        )
        if show_t10:
            et = r.edge_by_bet.get("top_10")
            cells.append(f"{et:+.3f}" if et is not None else "n/a")
        cells.extend(
            [
                f"{r.reliability.score:.2f}",
                _flag_cell(r.flags),
            ]
        )
        body.append(cells)
    return RankedTableView(
        show_move=show_move,
        show_t10=show_t10,
        headers=tuple(headers),
        aligns=tuple(aligns),
        rows=body,
        glossary=column_index_items(show_move=show_move, show_t10=show_t10),
    )


def format_table(
    rows: list[PlayerOutput],
    n: int = 25,
    baseline: list[PlayerOutput] | None = None,
) -> str:
    show_t10 = any(r.edge_by_bet.get("top_10") is not None or r.posted_odds_by_bet.get("top_10") for r in rows)
    show_move = baseline is not None
    pre_by_id = {o.player_id: o for o in baseline} if show_move else {}
    header = f"{'#':>3} {'Player':<22} {'Win':>20}"
    if show_move:
        header += f" {'dWin':>7} {'Pre#':>5} {'dRnk':>5}"
    header += f" {'T10':>10} {'Cut':>10} {'EdgeW':>8}"
    if show_t10:
        header += f" {'EdgeT10':>8}"
    header += f" {'Rel':>5} {'Flags'}"
    lines = [header, "-" * len(header)]
    for r in rows[:n]:
        w = r.probabilities.p(Horizon.WIN)
        t10 = r.probabilities.p(Horizon.TOP_10)
        cut = r.probabilities.p(Horizon.MAKE_CUT)
        ew = r.edge_by_bet.get("win")
        edge_s = f"{ew:+.3f}" if ew is not None else "  n/a"
        flag = _flag_cell(r.flags)
        win_s = _win_cell(w)
        line = f"{r.rank:3d} {r.name:<22} {win_s:>20}"
        if show_move:
            pre = pre_by_id.get(r.player_id)
            if pre is None:
                line += f" {'n/a':>7} {'n/a':>5} {'n/a':>5}"
            else:
                d_win = w.central - pre.probabilities.p(Horizon.WIN).central
                d_rnk = pre.rank - r.rank
                line += f" {d_win:+7.3f} {pre.rank:5d} {d_rnk:+5d}"
        line += f" {t10.central:10.3f} {cut.central:10.3f} {edge_s:>8}"
        if show_t10:
            et = r.edge_by_bet.get("top_10")
            line += f" {et:+.3f}" if et is not None else "     n/a"
        line += f" {r.reliability.score:5.2f} {flag}"
        lines.append(line)
    lines.append("")
    lines.append(format_column_index(show_move=show_move, show_t10=show_t10))
    return "\n".join(lines)


def _win_cell(w) -> str:
    return f"{w.central:.3f}  [{w.low:.2f}-{w.high:.2f}]"


def _flag_cell(flags: list[str]) -> str:
    return ", ".join(flag.replace("_", " ") for flag in flags[:2])
