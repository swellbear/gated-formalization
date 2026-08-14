"""Persist distinct prematch coupons. Never store Winner Live as an opening line."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.enums import BetType, SourceKind
from golf_offshoot.models.schemas import MarketQuote


def openings_dir() -> Path:
    d = package_data_dir() / "openings"
    d.mkdir(parents=True, exist_ok=True)
    return d


def opening_path(event_id: str, directory: Path | None = None, *, book_family: str = "") -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in str(event_id))
    fam = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in str(book_family or "").strip())
    if fam and fam not in {"auto", "bovada"}:
        safe = f"{safe}_{fam}"
    return (directory or openings_dir()) / f"{safe}.json"


def is_prematch_quote(quote: MarketQuote) -> bool:
    book = str(quote.book or "").lower()
    return "live" not in book


def _quote_to_dict(quote: MarketQuote) -> dict[str, Any]:
    return {
        "player_id": quote.player_id,
        "bet_type": quote.bet_type.value,
        "decimal_odds": quote.decimal_odds,
        "implied_raw": quote.implied_raw,
        "book": quote.book,
        "as_of": quote.as_of.isoformat() if quote.as_of else None,
        "line_role": "opening",
        "source_kind": SourceKind.REAL_LIVE.value,
    }


def _quote_from_dict(row: dict[str, Any]) -> MarketQuote | None:
    try:
        bet = BetType(str(row.get("bet_type") or "win"))
    except ValueError:
        return None
    as_of_raw = row.get("as_of")
    try:
        as_of = datetime.fromisoformat(str(as_of_raw)) if as_of_raw else datetime.now(timezone.utc)
    except ValueError:
        as_of = datetime.now(timezone.utc)
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=timezone.utc)
    dec = row.get("decimal_odds")
    try:
        dec_f = float(dec)
    except (TypeError, ValueError):
        return None
    if dec_f <= 1.0:
        return None
    implied = row.get("implied_raw")
    try:
        implied_f = float(implied) if implied is not None else 1.0 / dec_f
    except (TypeError, ValueError):
        implied_f = 1.0 / dec_f
    book = str(row.get("book") or "bovada")
    if "live" in book.lower():
        return None
    return MarketQuote(
        player_id=str(row.get("player_id") or ""),
        bet_type=bet,
        decimal_odds=dec_f,
        implied_raw=implied_f,
        book=book,
        as_of=as_of,
        line_role="opening",
    )


def load_opening_quotes(
    event_id: str | None,
    directory: Path | None = None,
    *,
    book_family: str = "",
) -> list[MarketQuote]:
    if not event_id:
        return []
    path = opening_path(event_id, directory, book_family=book_family)
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    out: list[MarketQuote] = []
    for row in payload.get("quotes") or []:
        if not isinstance(row, dict):
            continue
        q = _quote_from_dict(row)
        if q is not None and q.player_id:
            out.append(q)
    return out


def persist_prematch_openings(
    event_id: str | None,
    tournament_name: str,
    quotes: list[MarketQuote],
    directory: Path | None = None,
    book_family: str = "",
) -> Path | None:
    """Store the first distinct prematch coupon. Live prices are never written."""
    if not event_id:
        return None
    path = opening_path(event_id, directory, book_family=book_family)
    if path.exists():
        return path
    prematch = [q for q in quotes if is_prematch_quote(q)]
    if not prematch:
        return None
    payload = {
        "event_id": event_id,
        "tournament_name": tournament_name,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source_kind": SourceKind.REAL_LIVE.value,
        "notes": (
            "First distinct prematch coupon observed for this ESPN event. "
            "Winner Live / bovada_live quotes are never stored as openings."
        ),
        "quotes": [_quote_to_dict(q) for q in prematch],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def merge_archived_openings(
    quotes: list[MarketQuote],
    event_id: str | None,
    directory: Path | None = None,
    *,
    book_family: str = "",
) -> list[MarketQuote]:
    """Attach archived prematch as line_role=opening when the live coupon has none."""
    archived = load_opening_quotes(event_id, directory, book_family=book_family)
    if not archived:
        return quotes
    have_open = {
        (q.player_id, q.bet_type)
        for q in quotes
        if str(q.line_role or "current") == "opening"
    }
    extra: list[MarketQuote] = []
    for q in archived:
        key = (q.player_id, q.bet_type)
        if key in have_open:
            continue
        extra.append(q)
    return quotes + extra
