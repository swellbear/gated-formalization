"""Leftover callout after live / ingest strategy. Display only. No new feeds."""

from __future__ import annotations

from golf_offshoot.models.enums import Horizon, RunMode, SourceKind
from golf_offshoot.models.schemas import SourceInventoryItem, TournamentRunResult


def format_leftover_callout(result: TournamentRunResult, open_book=None) -> str:
    """ASCII leftover block. Does not change theta, screens, or tickets."""
    items = _inventory(result)
    used = _already_used(result, items)
    unconstrained = _still_unconstrained(items)
    held = _held_section(result, open_book)
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    lines = [
        "LEFTOVER CALLOUT  (display only; not GPF gates)",
        f"event={tid}  mode={result.mode.value}  never_auto_bet=true",
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
        "  Do not add a live d-theta CLI.",
    ]
    return "\n".join(lines)


def _inventory(result: TournamentRunResult) -> list[SourceInventoryItem]:
    raw = (result.audit.extra or {}).get("source_inventory") or []
    out: list[SourceInventoryItem] = []
    for x in raw:
        if isinstance(x, SourceInventoryItem):
            out.append(x)
        else:
            out.append(SourceInventoryItem.model_validate(x))
    return out


def _by_name(items: list[SourceInventoryItem], name: str) -> SourceInventoryItem | None:
    return next((i for i in items if i.field_name == name), None)


def _present(item: SourceInventoryItem | None) -> bool:
    if item is None:
        return False
    if item.source_kind in {SourceKind.UNAVAILABLE, SourceKind.MOCK}:
        return False
    cov = (item.coverage or "").strip()
    if cov in {"", "0"}:
        return False
    return True


def _already_used(result: TournamentRunResult, items: list[SourceInventoryItem]) -> list[str]:
    lines: list[str] = []
    field = _by_name(items, "player_identification_field")
    if _present(field):
        src = field.source_name if field else "espn_field"
        lines.append(f"  ESPN field ({src})")
    if result.mode == RunMode.LIVE:
        lines.append("  ESPN to-par / holes completed (live)")
    recent = _by_name(items, "strokes_gained_recent_window")
    if _present(recent):
        lines.append(f"  as-of SG (inventory present; {recent.coverage})")
    odds = _by_name(items, "market_odds")
    book = str((result.audit.extra or {}).get("odds_book") or "").strip() or "posted"
    n_quotes = (result.audit.extra or {}).get("odds_quotes")
    if _present(odds) or (isinstance(n_quotes, int) and n_quotes > 0):
        cov = odds.coverage if odds and odds.coverage else (str(n_quotes) if n_quotes else "yes")
        lines.append(f"  {book} posted quotes ({cov})")
    if not lines:
        lines = ["  (nothing listed this run)"]
    return lines


def _still_unconstrained(items: list[SourceInventoryItem]) -> list[str]:
    lines: list[str] = []
    agro = _by_name(items, "course_setup_agronomy")
    if agro:
        note = agro.notes or agro.impact_if_missing or "not evidence"
        lines.append(f"  agronomy - {note}")
    else:
        lines.append("  agronomy - no inventory row; unconstrained")
    lines.append("  tee/wave - no inventory row; unconstrained")
    health = _by_name(items, "health_injury")
    if health:
        note = health.notes or health.coverage or "WD status only"
        lines.append(f"  injury except ESPN WD - {note}")
    else:
        lines.append("  injury except ESPN WD - no injury wire")
    lines.append("  narrative forced to 0")
    sg = _by_name(items, "strokes_gained_categories")
    unmatched = _unmatched_from_notes(sg.notes if sg else "")
    if unmatched:
        lines.append(f"  unmatched SG names - {unmatched}")
    elif sg and "unmatched" in (sg.notes or "").lower():
        lines.append(f"  unmatched SG names - {sg.notes}")
    else:
        impact = sg.impact_if_missing if sg else "SG unconstrained for unmatched players"
        if "unmatched" in (impact or "").lower():
            lines.append(f"  unmatched SG names - {impact}")
    return lines


def _unmatched_from_notes(notes: str) -> str:
    if not notes:
        return ""
    key = "unmatched:"
    low = notes.lower()
    i = low.find(key)
    if i < 0:
        return ""
    return notes[i + len(key) :].strip()


def _held_section(result: TournamentRunResult, open_book) -> list[str]:
    positions = _open_positions(open_book)
    if result.mode != RunMode.LIVE or not positions:
        return ["  (none held)"]
    by_id = {r.player_id: r for r in result.ranked}
    by_name = {r.name.lower(): r for r in result.ranked}
    lines: list[str] = []
    for pos in positions:
        row = by_id.get(pos.player_id) or by_name.get((pos.player_name or "").lower())
        name = (row.name if row else None) or pos.player_name or pos.player_id
        if row is None:
            lines.append(f"  {name} - no live row; ride to official settle. Not extra theta.")
            continue
        win = row.probabilities.p(Horizon.WIN).central
        theta = row.probabilities.theta_mean
        to_par = row.live_score_to_par
        holes = row.live_holes_completed
        tp = "n/a" if to_par is None else f"{to_par:+g}" if to_par else "E"
        lines.append(
            f"  {name} win={win:.3f} to-par={tp} holes={holes} theta={theta:.2f}"
        )
    lines.append(
        "  Win% is banked to-par plus remaining holes from current theta."
    )
    lines.append(
        "  A hot round / looking good is the operator residual, not extra theta."
    )
    return lines


def _open_positions(open_book) -> list:
    if open_book is None:
        return []
    book = getattr(open_book, "book", None)
    if book is not None and getattr(book, "positions", None) is not None:
        return list(book.positions)
    if getattr(open_book, "positions", None) is not None:
        return list(open_book.positions)
    return []
