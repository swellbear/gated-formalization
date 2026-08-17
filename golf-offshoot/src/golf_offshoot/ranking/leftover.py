"""Leftover callout after live / ingest strategy. Display only. Do not stuff into theta."""

from __future__ import annotations

from golf_offshoot.models.enums import Horizon, RunMode, SourceKind
from golf_offshoot.models.schemas import SourceInventoryItem, TournamentRunResult
from golf_offshoot.ranking.leaderboard import format_to_par


def format_leftover_callout(result: TournamentRunResult, open_book=None) -> str:
    """ASCII leftover block. No new feeds. Not a GPF residual menu."""
    inv = _inventory(result)
    by_name = {i.field_name: i for i in inv}
    used = _used_lines(result, by_name)
    unconstrained = _unconstrained_lines(by_name)
    held = _held_lines(result, open_book)
    lines = [
        "LEFTOVER CALLOUT  (display only; not GPF gates)",
        f"event={result.tournament.name}  mode={result.mode.value}  never_auto_bet=true",
        "",
        "== already used ==",
        *used,
        "",
        "== still unconstrained ==",
        *unconstrained,
        "",
        "== on held tickets ==",
        *held,
        "",
        "== do not stuff into theta ==",
        "  Overrides stay documented (HumanOverride + audit) or they do not happen.",
        "  Do not add a live delta-theta CLI from this block.",
        "  Agronomy, tee pairing, narrative, and injury rumor stay leftover, not theta.",
    ]
    return "\n".join(lines)


def _inventory(result: TournamentRunResult) -> list[SourceInventoryItem]:
    raw = result.audit.extra.get("source_inventory") or []
    out: list[SourceInventoryItem] = []
    for item in raw:
        if isinstance(item, SourceInventoryItem):
            out.append(item)
        elif isinstance(item, dict):
            out.append(SourceInventoryItem.model_validate(item))
    return out


def _present(item: SourceInventoryItem | None) -> bool:
    if item is None:
        return False
    if item.source_kind == SourceKind.UNAVAILABLE:
        return False
    cov = (item.coverage or "").strip()
    if cov in {"0", "0/0"} or cov.startswith("0/0"):
        return False
    return True


def _used_lines(result: TournamentRunResult, by_name: dict[str, SourceInventoryItem]) -> list[str]:
    lines: list[str] = []
    field = by_name.get("player_identification_field")
    if _present(field):
        src = field.source_name or "espn_field"
        lines.append(f"  ESPN field - {src} ({field.coverage or 'field'})")
    if result.mode == RunMode.LIVE:
        n_live = sum(1 for r in result.ranked if r.live_holes_completed or r.live_place is not None)
        if n_live:
            lines.append(
                "  ESPN live board - place / to-par / holes completed "
                f"({n_live} players with a board mark)"
            )
    recent = by_name.get("strokes_gained_recent_window")
    cats = by_name.get("strokes_gained_categories")
    if _present(recent):
        lines.append(
            f"  as-of SG - {recent.source_name or 'pga_tour_sg'} "
            f"({recent.coverage or 'present'})"
        )
    elif _present(cats):
        lines.append(
            f"  as-of SG - not a last-N window; long-term SG present "
            f"({cats.coverage})"
        )
    odds = by_name.get("market_odds")
    if _present(odds):
        src = odds.source_name or "odds"
        lines.append(f"  posted odds - {src} ({odds.coverage or 'quotes exist'})")
    return lines or ["  (nothing admitted this run)"]


def _unconstrained_lines(by_name: dict[str, SourceInventoryItem]) -> list[str]:
    agro = by_name.get("course_setup_agronomy")
    health = by_name.get("health_injury")
    sg = by_name.get("strokes_gained_categories")
    agro_note = (agro.notes or agro.impact_if_missing) if agro else "tightness/rough/stimp not evidence"
    health_note = (health.notes or health.impact_if_missing) if health else "no injury wire; WD status only"
    unmatched = _unmatched_note(sg)
    return [
        f"  agronomy - {agro_note}",
        "  tee/wave - live tee pairing unseeded; not in theta",
        f"  injury - {health_note} (ESPN WD is status, not a rumor feed)",
        "  narrative - forced to 0; not used",
        f"  unmatched SG - {unmatched}",
    ]


def _unmatched_note(sg: SourceInventoryItem | None) -> str:
    if sg is None:
        return "none listed this run"
    notes = sg.notes or ""
    low = notes.lower()
    if "unmatched" not in low:
        return sg.impact_if_missing or "none listed this run"
    idx = low.find("unmatched")
    return notes[idx:].strip() or "unmatched names stay unconstrained"


def _held_lines(result: TournamentRunResult, open_book) -> list[str]:
    positions = _open_positions(open_book)
    if result.mode != RunMode.LIVE or not positions:
        return ["  (none held)"]
    by_id = {r.player_id: r for r in result.ranked}
    by_name = {r.name: r for r in result.ranked}
    seen: set[str] = set()
    lines: list[str] = []
    for pos in positions:
        pid = getattr(pos, "player_id", "") or ""
        pname = getattr(pos, "player_name", "") or ""
        key = pid or pname
        if not key or key in seen:
            continue
        seen.add(key)
        row = by_id.get(pid) or by_name.get(pname)
        name = pname or (row.name if row else pid or "n/a")
        if row is None:
            lines.append(f"  {name} - no live row; residual, not extra theta")
            continue
        wp = row.probabilities.p(Horizon.WIN).central
        to_par = format_to_par(row.live_score_to_par)
        holes = int(row.live_holes_completed or 0)
        lines.append(f"  {name}  Win={wp:.3f}  to-par={to_par}  holes={holes}")
    if lines:
        lines.append(
            "  Win% is banked to-par plus remaining holes from current theta. "
            "A hot round / looking good is the operator's residual, not extra theta."
        )
    return lines or ["  (none held)"]


def _open_positions(open_book) -> list:
    if open_book is None:
        return []
    inner = getattr(open_book, "book", None)
    raw = getattr(inner, "positions", None) if inner is not None else getattr(open_book, "positions", None)
    out = []
    for pos in raw or []:
        if getattr(pos, "proposed", False):
            continue
        if float(getattr(pos, "stake", 0) or 0) <= 0:
            continue
        out.append(pos)
    return out
