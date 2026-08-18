"""Operator footguns. Display only. Do not change theta or ticket size."""

from __future__ import annotations

from datetime import date

from golf_offshoot.localtime import now as eastern_now


def current_pga_event(*, refresh: bool = False) -> tuple[str, str] | None:
    """ESPN current PGA event (id, name). Fail open."""
    try:
        from golf_offshoot.data_feeds.espn import EspnClient, parse_event_payload
        from golf_offshoot.data_feeds.http import HttpCache

        payload = EspnClient(HttpCache(), refresh=refresh).current_leaderboard()
        event = parse_event_payload(payload)
        eid = str(event.get("id") or "").strip()
        name = str(event.get("name") or "current PGA event").strip()
        if not eid:
            return None
        return eid, name
    except Exception:
        return None


def pinned_event_hint(
    pinned_id: str | None,
    *,
    settled: bool = False,
    current: tuple[str, str] | None = None,
    lookup: bool = True,
) -> str | None:
    """If the pin is last week's museum, name this week's ESPN event."""
    pid = str(pinned_id or "").strip()
    if not pid:
        return None
    cur = current if current is not None else (current_pga_event() if lookup else None)
    if cur is None:
        return "this event is settled (museum)." if settled else None
    cid, cname = cur
    if pid == str(cid):
        return "this event is settled (museum)." if settled else None
    if settled:
        return f"this event is settled (museum). this week is {cname} {cid}"
    return f"pinned {pid} is not ESPN's current week. this week is {cname} {cid}"


def pre_thursday_opening_warning(
    start_date: str | None,
    opening_quotes: int | None,
    *,
    today: date | None = None,
    odds_book: str | None = None,
) -> str | None:
    """Warn while tee day is still ahead and no distinct prematch coupon was stored."""
    if int(opening_quotes or 0) > 0:
        return None
    raw = (start_date or "").strip()[:10]
    if not raw:
        return None
    try:
        tee = date.fromisoformat(raw)
    except ValueError:
        return None
    day = today if today is not None else eastern_now().date()
    if day >= tee:
        return None
    book = (odds_book or "").strip().lower()
    if book == "polymarket":
        how = "ingest again while Polymarket still lists Yes asks on the winner card."
    else:
        how = "ingest again while Bovada still shows Winner, not Winner Live."
    return (
        f"no opening coupon stored yet; tee is {tee.isoformat()} (still pre-Thursday). "
        + how
    )


def is_empty_field(ranked) -> bool:
    return not list(ranked or [])
