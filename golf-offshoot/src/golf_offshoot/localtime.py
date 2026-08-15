"""America/New_York clocks for display, JSON storage, and filenames.

Naive timestamps are treated as UTC (legacy writes). Instants from feeds are
converted to Eastern before they are stored.
"""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")


def now() -> datetime:
    return datetime.now(EASTERN)


def to_eastern(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(EASTERN)


def _parse_iso(value: str) -> datetime | None:
    text = value.strip()
    if not text or text == "n/a":
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def format_eastern(value: datetime | str | None, *, with_seconds: bool = False) -> str:
    """Human clock in America/New_York. EDT in summer, EST in winter. n/a if missing."""
    if value is None or value == "":
        return "n/a"
    if isinstance(value, str):
        parsed = _parse_iso(value)
        if parsed is None:
            return value
        value = parsed
    local = to_eastern(value)
    fmt = "%Y-%m-%d %H:%M:%S %Z" if with_seconds else "%Y-%m-%d %H:%M %Z"
    return local.strftime(fmt)


def now_eastern_text(*, with_seconds: bool = False) -> str:
    return format_eastern(now(), with_seconds=with_seconds)


def isoformat_now(value: datetime | None = None) -> str:
    """JSON timestamp in Eastern, with offset (-04:00 / -05:00)."""
    dt = to_eastern(value) if value is not None else now()
    return dt.isoformat()


def filename_stamp(value: datetime | None = None) -> str:
    """Path-safe Eastern stamp. Offset instead of Z (Z means UTC)."""
    local = to_eastern(value) if value is not None else now()
    return local.strftime("%Y%m%dT%H%M%S%z")
