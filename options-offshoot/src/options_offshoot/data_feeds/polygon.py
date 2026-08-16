"""Polygon options snapshot. Frozen v1 quote vendor. Do not silently swap."""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta, timezone
from typing import Any

from options_offshoot.data_feeds.base import FeedError, unavailable_quality
from options_offshoot.data_feeds.http import get_json
from options_offshoot.data_feeds.local_env import polygon_api_key
from options_offshoot.models.enums import ContractType
from options_offshoot.models.schemas import Contract, Quote

BASE = "https://api.polygon.io"


class PolygonClient:
    def __init__(self, api_key: str | None = None, *, use_cache: bool = True) -> None:
        self.api_key = (api_key if api_key is not None else polygon_api_key()).strip()
        self.use_cache = use_cache

    def _url(self, path: str, extra: str = "") -> str:
        if not self.api_key:
            raise FeedError("POLYGON_API_KEY missing")
        sep = "&" if "?" in path else "?"
        return f"{BASE}{path}{sep}apiKey={self.api_key}{extra}"

    def snapshot(self, underlying: str, expiry: str | None = None) -> dict[str, Any]:
        ticker = underlying.strip().upper().replace(".", ".")
        path = f"/v3/snapshot/options/{ticker}"
        if expiry:
            path += f"?expiration_date={expiry}"
        return get_json(self._url(path), use_cache=self.use_cache)

    def realized_vol(self, underlying: str, lookback: int = 20) -> float | None:
        ticker = underlying.strip().upper()
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=lookback * 3)
        path = (
            f"/v2/aggs/ticker/{ticker}/range/1/day/{start.isoformat()}/{end.isoformat()}"
            f"?adjusted=true&sort=desc&limit={lookback + 5}"
        )
        try:
            payload = get_json(self._url(path), use_cache=self.use_cache)
        except RuntimeError:
            return None
        results = payload.get("results") or []
        closes = [float(r["c"]) for r in results if r.get("c")]
        if len(closes) < max(6, lookback // 2):
            return None
        closes = list(reversed(closes[: lookback + 1]))
        rets = []
        for a, b in zip(closes, closes[1:]):
            if a > 0 and b > 0:
                rets.append(math.log(b / a))
        if len(rets) < 5:
            return None
        mean = sum(rets) / len(rets)
        var = sum((x - mean) ** 2 for x in rets) / max(1, len(rets) - 1)
        return math.sqrt(max(var, 0.0) * 252.0)

    def earnings_tickers(self, start: str, end: str) -> list[str] | None:
        """Return None if the calendar endpoint is unavailable (plan/key)."""
        path = f"/vX/reference/tickers?active=true&limit=1"
        try:
            get_json(self._url(path), use_cache=self.use_cache)
        except RuntimeError:
            return None
        # Polygon earnings calendars vary by plan. v1 does not scrape the open web.
        # None → caller uses the frozen earnings_us_week.txt leash.
        _ = (start, end)
        return None


def contracts_from_snapshot(
    payload: dict[str, Any],
    *,
    underlying: str,
    expiry: date | None,
    spot: float | None = None,
    realized_vol: float | None = None,
    years_to_expiry: float | None = None,
) -> list[Contract]:
    results = payload.get("results") or payload.get("option_chain") or []
    if isinstance(results, dict):
        results = results.get("results") or []
    out: list[Contract] = []
    ua = payload.get("underlying_asset") or {}
    px = spot
    if px is None:
        px = _num(ua.get("price") or ua.get("value"))
    for row in results:
        if not isinstance(row, dict):
            continue
        details = row.get("details") or {}
        exp = _parse_date(details.get("expiration_date") or row.get("expiration_date"))
        if expiry is not None and exp is not None and exp != expiry:
            continue
        strike = _num(details.get("strike_price") or row.get("strike_price"))
        side = str(details.get("contract_type") or row.get("contract_type") or "call").lower()
        ctype = ContractType.PUT if "put" in side else ContractType.CALL
        ticker = str(details.get("ticker") or row.get("ticker") or "")
        if strike is None or exp is None or not ticker:
            continue
        lq = row.get("last_quote") or {}
        bid = _num(lq.get("bid") or lq.get("bid_price") or row.get("bid"))
        ask = _num(lq.get("ask") or lq.get("ask_price") or row.get("ask"))
        last = _num((row.get("last_trade") or {}).get("price") or row.get("last"))
        oi = _int(row.get("open_interest"))
        vol = _int((row.get("day") or {}).get("volume") or row.get("volume"))
        cid = ticker
        out.append(
            Contract(
                contract_id=cid,
                underlying=underlying.upper(),
                expiry=exp,
                strike=float(strike),
                contract_type=ctype,
                quote=Quote(bid=bid, ask=ask, last=last, open_interest=oi, volume=vol),
                spot=px,
                realized_vol=realized_vol,
                years_to_expiry=years_to_expiry,
            )
        )
    return out


def _num(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any) -> int | None:
    try:
        if value is None or value == "":
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None
    text = str(value)[:10]
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None
