"""America/New_York clocks for display, JSON, and filenames."""

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


def format_eastern(value: datetime | str | None, *, with_seconds: bool = False) -> str:
    if value is None or value == "":
        return "n/a"
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            value = datetime.fromisoformat(text)
        except ValueError:
            return value
    local = to_eastern(value)
    fmt = "%Y-%m-%d %H:%M:%S %Z" if with_seconds else "%Y-%m-%d %H:%M %Z"
    return local.strftime(fmt)


def now_eastern_text(*, with_seconds: bool = False) -> str:
    return format_eastern(now(), with_seconds=with_seconds)


def isoformat_now(value: datetime | None = None) -> str:
    dt = to_eastern(value) if value is not None else now()
    return dt.isoformat()


def filename_stamp(value: datetime | None = None) -> str:
    local = to_eastern(value) if value is not None else now()
    return local.strftime("%Y%m%d_ET%H%M%S")
