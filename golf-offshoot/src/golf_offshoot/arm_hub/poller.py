"""Independent KXBTC15M quote poller. Never reads learning_lane trees."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from golf_offshoot.arm_hub.paths import (
    SERIES_DEFAULT,
    assert_not_learning_lane_path,
    replay_tape_path,
)

PAPER_PUBLIC_MARKETS = (
    "https://api.elections.kalshi.com/trade-api/v2/markets"
    f"?series_ticker={SERIES_DEFAULT}&status=open"
)


@dataclass(frozen=True)
class Quote:
    ticker: str
    event_ticker: str
    yes_bid: float | None
    yes_ask: float | None
    yes_price: float
    secs_to_expiry: int | None
    status: str
    result: str
    raw: dict[str, Any]


def _mid(bid: float | None, ask: float | None, last: float | None) -> float:
    if bid is not None and ask is not None and 0.0 < bid < 1.0 and 0.0 < ask < 1.0:
        return (bid + ask) / 2.0
    if last is not None and 0.0 < last < 1.0:
        return last
    if ask is not None and 0.0 < ask < 1.0:
        return ask
    if bid is not None and 0.0 < bid < 1.0:
        return bid
    raise ValueError("quote has no usable yes price")


def _f(raw: Any) -> float | None:
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def quote_from_market(raw: dict[str, Any]) -> Quote:
    bid = _f(raw.get("yes_bid") if raw.get("yes_bid") is not None else raw.get("yes_bid_dollars"))
    ask = _f(raw.get("yes_ask") if raw.get("yes_ask") is not None else raw.get("yes_ask_dollars"))
    last = _f(raw.get("last_price") if raw.get("last_price") is not None else raw.get("last_price_dollars"))
    if bid is not None and bid > 1.0:
        bid = bid / 100.0
    if ask is not None and ask > 1.0:
        ask = ask / 100.0
    if last is not None and last > 1.0:
        last = last / 100.0
    secs = raw.get("secs_to_expiry")
    try:
        secs_i = int(secs) if secs is not None and secs != "" else None
    except (TypeError, ValueError):
        secs_i = None
    return Quote(
        ticker=str(raw.get("ticker") or ""),
        event_ticker=str(raw.get("event_ticker") or ""),
        yes_bid=bid,
        yes_ask=ask,
        yes_price=_mid(bid, ask, last),
        secs_to_expiry=secs_i,
        status=str(raw.get("status") or ""),
        result=str(raw.get("result") or "").strip().lower(),
        raw=raw,
    )


def load_replay_tape(path: Path | None = None, *, root: Path | None = None) -> list[dict[str, Any]]:
    tape = path or replay_tape_path(root)
    assert_not_learning_lane_path(tape)
    raw = json.loads(tape.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        windows = raw.get("windows") or raw.get("quotes") or []
    elif isinstance(raw, list):
        windows = raw
    else:
        raise ValueError("replay tape must be an object or list")
    if not isinstance(windows, list):
        raise ValueError("replay tape windows must be a list")
    return [w for w in windows if isinstance(w, dict)]


def quotes_from_replay_window(window: dict[str, Any]) -> list[Quote]:
    ticks = window.get("quotes")
    if isinstance(ticks, list) and ticks:
        out: list[Quote] = []
        for tick in ticks:
            if not isinstance(tick, dict):
                continue
            merged = {
                "ticker": window.get("ticker"),
                "event_ticker": window.get("event_ticker"),
                "status": window.get("status") or "active",
                "result": window.get("result") or "",
                **tick,
            }
            out.append(quote_from_market(merged))
        return out
    return [quote_from_market(window)]


def fetch_public_open_markets(*, timeout: float = 15.0) -> list[Quote]:
    """Public elections API only. No keys. No private paths."""
    req = urllib.request.Request(
        PAPER_PUBLIC_MARKETS,
        headers={"User-Agent": "golf-offshoot-arm-hub/0.1 (paper; not-armed)"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise QuoteFetchError(f"public poller failed: {exc}") from exc
    markets = payload.get("markets") if isinstance(payload, dict) else None
    if not isinstance(markets, list):
        return []
    out: list[Quote] = []
    for raw in markets:
        if not isinstance(raw, dict):
            continue
        try:
            out.append(quote_from_market(raw))
        except ValueError:
            continue
    return out


class QuoteFetchError(RuntimeError):
    """Public poller could not fetch."""
