"""ESPN-style live scoreboard. Sorted by place/to-par, not model Win%."""

from __future__ import annotations

from dataclasses import dataclass

from golf_offshoot.models.schemas import PlayerOutput


@dataclass(frozen=True)
class LeaderboardView:
    headers: tuple[str, ...]
    aligns: tuple[str, ...]
    rows: list[list[str]]
    glossary: list[tuple[str, str]]
    n_rounds: int


def format_to_par(score: float | None) -> str:
    if score is None:
        return "-"
    if abs(score) < 1e-9:
        return "E"
    if score > 0:
        return f"+{score:.0f}"
    return f"{score:.0f}"


def format_thru(
    holes_completed: int,
    n_rounds: int,
    *,
    withdrawn: bool = False,
    missed_cut: bool = False,
) -> str:
    if withdrawn or missed_cut:
        return "-"
    total = max(int(n_rounds), 1) * 18
    h = max(0, int(holes_completed))
    if h <= 0:
        return "-"
    if h >= total or h % 18 == 0:
        return "F"
    return str(h % 18)


def format_round(holes_completed: int, n_rounds: int) -> str:
    total = max(int(n_rounds), 1) * 18
    h = max(0, int(holes_completed))
    if h <= 0:
        return "-"
    rd = min(max(int(n_rounds), 1), (h + 17) // 18)
    if h >= total:
        return str(n_rounds)
    return str(rd)


def format_status(row: PlayerOutput, n_rounds: int) -> str:
    name = (row.live_status_name or "").upper()
    if row.withdrawn or "WITHDRAW" in name:
        return "WD"
    if row.live_made_cut is False or name == "STATUS_CUT":
        return "CUT"
    total = max(int(n_rounds), 1) * 18
    h = max(0, int(row.live_holes_completed))
    if h >= total or name in ("STATUS_FINAL", "STATUS_PLAYOFF"):
        return "F"
    if h > 0 and h % 18 == 0:
        return "F"
    if h <= 0:
        return "-"
    return "playing"


def format_place(row: PlayerOutput) -> str:
    disp = (row.live_place_display or "").strip()
    if disp:
        return disp
    if row.live_place is not None:
        return str(row.live_place)
    return "-"


def _sort_key(row: PlayerOutput, n_rounds: int) -> tuple:
    status = format_status(row, n_rounds)
    if status == "WD":
        group = 3
    elif status == "CUT":
        group = 2
    else:
        group = 0
    place = row.live_place if row.live_place is not None else 999
    score = row.live_score_to_par if row.live_score_to_par is not None else 99.0
    holes = -int(row.live_holes_completed or 0)
    return (group, place, score, holes, row.name.lower())


def leaderboard_view(
    rows: list[PlayerOutput],
    *,
    n_rounds: int = 4,
    held_ids: set[str] | None = None,
) -> LeaderboardView:
    held = held_ids or set()
    ordered = sorted(rows, key=lambda r: _sort_key(r, n_rounds))
    headers = ("Pos", "Player", "ToPar", "Thru", "Rd", "Status", "Held")
    aligns = ("right", "left", "right", "right", "right", "left", "left")
    body: list[list[str]] = []
    for r in ordered:
        body.append(
            [
                format_place(r),
                r.name,
                format_to_par(r.live_score_to_par),
                format_thru(
                    r.live_holes_completed,
                    n_rounds,
                    withdrawn=r.withdrawn,
                    missed_cut=r.live_made_cut is False,
                ),
                format_round(r.live_holes_completed, n_rounds),
                format_status(r, n_rounds),
                "paper" if r.player_id in held else "",
            ]
        )
    glossary = [
        ("Pos", "ESPN leaderboard place at this snapshot (T = tied). Not model Win% rank."),
        ("ToPar", "Score to par from ESPN. E = even. Missing is '-'."),
        ("Thru", "Holes completed in the current round, or F if that round is in the clubhouse."),
        ("Rd", "Round implied by holes completed. Round-by-round scores are not ingested."),
        ("Status", "playing / F / CUT / WD from ESPN. Not a model projection."),
        ("Held", "paper = this name is on the mock book at this snapshot."),
        ("Note", "Snapshot of this live run. Not a later ESPN refresh. Observation only."),
    ]
    return LeaderboardView(headers=headers, aligns=aligns, rows=body, glossary=glossary, n_rounds=n_rounds)


def format_leaderboard(
    rows: list[PlayerOutput],
    *,
    n_rounds: int = 4,
    held_ids: set[str] | None = None,
) -> str:
    view = leaderboard_view(rows, n_rounds=n_rounds, held_ids=held_ids)
    widths = [len(h) for h in view.headers]
    for cells in view.rows:
        for i, cell in enumerate(cells):
            widths[i] = max(widths[i], len(cell))
    def _fmt(cells: list[str] | tuple[str, ...]) -> str:
        parts = []
        for i, cell in enumerate(cells):
            w = widths[i]
            if view.aligns[i] == "right":
                parts.append(f"{cell:>{w}}")
            else:
                parts.append(f"{cell:<{w}}")
        return "  ".join(parts)
    lines = [_fmt(view.headers), _fmt(["-" * w for w in widths])]
    for cells in view.rows:
        lines.append(_fmt(cells))
    return "\n".join(lines)
