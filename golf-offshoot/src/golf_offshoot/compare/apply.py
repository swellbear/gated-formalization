"""Hysteresis auto-apply for mock paper. Never a real bet."""

from __future__ import annotations

import hashlib
import json

from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement, apply_advice

_SKIP_KINDS = frozenset({"hold", "no_action", ""})


def actionable_items(advice: list[PaperMovement]) -> list[tuple[str, str, str]]:
    items: list[tuple[str, str, str]] = []
    for mv in advice:
        kind = (mv.kind or "").lower()
        if kind in _SKIP_KINDS:
            continue
        items.append((kind, str(mv.player_id or ""), str(mv.bet_type or "win")))
    items.sort()
    return items


def advice_signature(advice: list[PaperMovement]) -> str:
    payload = json.dumps(actionable_items(advice), separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def maybe_apply_paper(
    record: PaperBookFile,
    advice: list[PaperMovement],
    *,
    force: bool = False,
) -> tuple[PaperBookFile, bool]:
    """Apply when the actionable advice set changes. HOLD-only is not an apply.

    Official settle freezes the book. Leftover Winner quotes after the tournament
    are not a market; do not open new tickets, even with force.
    """
    record.latest_advice = list(advice)
    if record.settled_at is not None:
        return record, False
    sig = advice_signature(advice)
    if not force and sig == (record.last_advice_sig or ""):
        return record, False
    if not force and not actionable_items(advice):
        record.last_advice_sig = sig
        return record, False
    record = apply_advice(record, advice)
    record.last_advice_sig = sig
    record.latest_advice = list(advice)
    return record, True
