"""Publish / load the factory KXBTC15M snapshot. No HTTP here."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from golf_offshoot.localtime import now, to_eastern
from golf_offshoot.quote_bus.paths import SERIES, assert_quote_bus_path, snapshot_path

MAX_AGE_S = 180.0


def completeness(markets: list[Any]) -> dict[str, Any]:
    n = 0
    with_ba = 0
    for row in markets:
        if not isinstance(row, dict):
            continue
        n += 1
        if row.get("yes_bid") is not None and row.get("yes_ask") is not None:
            with_ba += 1
    missing = n - with_ba
    return {
        "n": n,
        "with_bid_and_ask": with_ba,
        "missing": missing,
        "rate": (missing / n) if n else 1.0,
    }


def _parse_when(raw: str) -> datetime | None:
    text = str(raw or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return to_eastern(datetime.fromisoformat(text))
    except ValueError:
        return None


def is_fresh(payload: dict[str, Any] | None, *, max_age_s: float = MAX_AGE_S) -> bool:
    if not payload:
        return False
    parsed = _parse_when(str(payload.get("fetched_at") or ""))
    if parsed is None:
        return False
    age = (now() - parsed).total_seconds()
    return age <= float(max_age_s)


def load_latest() -> dict[str, Any] | None:
    path = snapshot_path()
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def publish(live_state: dict[str, Any]) -> dict[str, Any]:
    markets = list(live_state.get("markets") or [])
    events = list(live_state.get("events") or [])
    fetched_at = str(live_state.get("fetched_at") or "")
    if not fetched_at:
        quality = live_state.get("quality") or {}
        if isinstance(quality, dict):
            fetched_at = str(quality.get("as_of") or "")
    if not fetched_at:
        fetched_at = now().isoformat()
    complete = completeness(markets)
    digest = hashlib.sha256(
        json.dumps(
            {"at": fetched_at, "tickers": [m.get("ticker") for m in markets if isinstance(m, dict)]},
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:16]
    payload = {
        "lane": "quote_bus",
        "series": SERIES,
        "source": "factory_paperwatch",
        "fetched_at": fetched_at,
        "fetch_id": digest,
        "markets": markets,
        "events": events,
        "quality": live_state.get("quality"),
        "quote_completeness": complete,
    }
    path = snapshot_path()
    assert_quote_bus_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return payload


def clock_line(payload: dict[str, Any] | None = None) -> str:
    snap = payload if payload is not None else load_latest()
    if not snap:
        return "Quote bus: missing — honer waits; does not fetch"
    parsed = _parse_when(str(snap.get("fetched_at") or ""))
    if parsed is None:
        return "Quote bus: unreadable fetched_at"
    age = int(max(0, (now() - parsed).total_seconds()))
    fresh = "fresh" if is_fresh(snap) else "stale"
    qc = snap.get("quote_completeness") or {}
    have = int(qc.get("with_bid_and_ask") or 0)
    n = int(qc.get("n") or 0)
    return f"Quote bus: {fresh} {age}s ago · {have}/{n} markets have bid/ask"
