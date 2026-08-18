"""Massive (formerly Polygon) REST. Named vendor. Do not silently swap.

Follow https://massive.com/docs/rest/llms.txt — not MCP, not websocket.
"""

from __future__ import annotations

import math
import os
import time
from datetime import date, datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlparse, urlunparse

from options_offshoot.config import (
    DEFAULT_MULTIPLIER,
    MAX_SNAPSHOT_PAGES,
    TTL_INGEST_S,
    TTL_LIVE_S,
    TTL_META_S,
    TTL_VOL_S,
    UNDERLYING_PAUSE_S,
)
from options_offshoot.data_feeds.base import FeedError
from options_offshoot.data_feeds.http import HttpError, StaleCacheError, get_json
from options_offshoot.data_feeds.local_env import load_local_env, polygon_api_key
from options_offshoot.models.enums import ContractType, QuoteVenue, RunMode
from options_offshoot.models.schemas import Contract, Quote

# Same vendor after the Polygon -> Massive rebrand. Keys still work on both hosts.
MASSIVE_BASE = "https://api.massive.com"
POLYGON_LEGACY_BASE = "https://api.polygon.io"
BASE = MASSIVE_BASE

# Documented: GET /benzinga/v1/earnings (Benzinga expansion, not stocks-only).
EARNINGS_PATHS = (
    "/benzinga/v1/earnings?date.gte={start}&date.lte={end}&limit=1000",
)


def rest_bases() -> list[str]:
    load_local_env()
    override = os.environ.get("MASSIVE_API_BASE", "").strip().rstrip("/")
    if override:
        return [override]
    return [MASSIVE_BASE, POLYGON_LEGACY_BASE]


def lookback_for_dte(days: int) -> int:
    if days <= 7:
        return 10
    if days <= 30:
        return 21
    return 63


class PolygonClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        use_cache: bool = True,
        mode: RunMode = RunMode.INGEST,
        pause_s: float | None = None,
    ) -> None:
        self.api_key = (api_key if api_key is not None else polygon_api_key()).strip()
        self.use_cache = use_cache
        self.mode = mode
        self.pause_s = UNDERLYING_PAUSE_S if pause_s is None else float(pause_s)
        self.pages_truncated = False
        self.last_notes: list[str] = []
        self.base = rest_bases()[0]

    def _quote_ttl(self) -> float:
        return TTL_LIVE_S if self.mode == RunMode.LIVE else TTL_INGEST_S

    def _url(self, path: str, base: str | None = None) -> str:
        if not self.api_key:
            raise FeedError("MASSIVE_API_KEY / POLYGON_API_KEY missing")
        root = (base or self.base).rstrip("/")
        sep = "&" if "?" in path else "?"
        return f"{root}{path}{sep}apiKey={self.api_key}"

    def _get(self, path_or_url: str, *, ttl_s: float) -> dict[str, Any]:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return get_json(path_or_url, use_cache=self.use_cache, ttl_s=ttl_s)
        last_exc: Exception | None = None
        for base in rest_bases():
            try:
                data = get_json(self._url(path_or_url, base), use_cache=self.use_cache, ttl_s=ttl_s)
                self.base = base
                return data
            except HttpError as exc:
                last_exc = exc
                if exc.status in (401, 403):
                    raise
                continue
        if last_exc:
            raise last_exc
        raise FeedError("massive REST unavailable")

    def snapshot(self, underlying: str, expiry: str | None = None) -> dict[str, Any]:
        ticker = underlying.strip().upper()
        path = f"/v3/snapshot/options/{ticker}?limit=250"
        if expiry:
            path = (
                f"/v3/snapshot/options/{ticker}?expiration_date={expiry}&limit=250"
            )
        try:
            first = self._get(path, ttl_s=self._quote_ttl())
        except HttpError as exc:
            if exc.status == 403:
                self.last_notes.append(
                    f"{ticker}: option chain snapshot 403 — Massive Options Starter+ "
                    "(not Options Basic / stocks-only). last_quote only if the plan "
                    "includes quotes. No invented mid."
                )
            raise
        results = list(_results_list(first))
        pages = 1
        nxt = first.get("next_url")
        truncated = False
        while nxt and pages < MAX_SNAPSHOT_PAGES:
            pages += 1
            try:
                payload = self._get(
                    _with_key(_rewrite_host(str(nxt), self.base), self.api_key),
                    ttl_s=self._quote_ttl(),
                )
            except (HttpError, StaleCacheError, FeedError) as exc:
                self.last_notes.append(f"{ticker}: next_url fail {exc}")
                truncated = True
                break
            results.extend(_results_list(payload))
            nxt = payload.get("next_url")
        if nxt:
            truncated = True
            self.last_notes.append(f"{ticker}: chain truncated after {pages} pages")
        self.pages_truncated = self.pages_truncated or truncated
        if results and not any(
            isinstance(row, dict) and row.get("last_quote") for row in results
        ):
            self.last_notes.append(
                f"{ticker}: chain has no last_quote (quotes not on this snapshot). "
                "No invented mid from day.close."
            )
        out = dict(first)
        out["results"] = results
        out["_pages"] = pages
        out["_truncated"] = truncated
        if self.pause_s > 0:
            time.sleep(self.pause_s)
        return out

    def realized_vol(self, underlying: str, lookback: int = 20) -> float | None:
        ticker = underlying.strip().upper()
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=max(lookback, 6) * 3)
        path = (
            f"/v2/aggs/ticker/{ticker}/range/1/day/{start.isoformat()}/{end.isoformat()}"
            f"?adjusted=true&sort=desc&limit={lookback + 5}"
        )
        try:
            payload = self._get(path, ttl_s=TTL_VOL_S)
        except (HttpError, StaleCacheError, FeedError, RuntimeError):
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

    def stock_spot(self, underlying: str) -> float | None:
        """Prev daily close. Stocks snapshot/last trade 403 on this plan. Not NBBO."""
        ticker = underlying.strip().upper()
        path = f"/v2/aggs/ticker/{ticker}/prev?adjusted=true"
        try:
            payload = self._get(path, ttl_s=TTL_VOL_S)
        except (HttpError, StaleCacheError, FeedError, RuntimeError):
            return None
        rows = payload.get("results") or []
        if rows:
            px = _num(rows[0].get("c"))
            if px is not None and px > 0:
                return px
        px = _num(payload.get("close") or payload.get("c"))
        if px is not None and px > 0:
            return px
        return None

    def nearest_listed_expiry(self, underlying: str, on_or_after: date) -> date | None:
        ticker = underlying.strip().upper()
        path = (
            f"/v3/reference/options/contracts?underlying_ticker={ticker}"
            f"&expired=false&limit=50&sort=expiration_date&order=asc"
            f"&expiration_date.gte={on_or_after.isoformat()}"
        )
        try:
            payload = self._get(path, ttl_s=TTL_META_S)
        except (HttpError, StaleCacheError, FeedError, RuntimeError):
            return None
        for row in payload.get("results") or []:
            exp = _parse_date((row or {}).get("expiration_date"))
            if exp is not None and exp >= on_or_after:
                return exp
        return None

    def session_close(self, underlying: str, day: date) -> float | None:
        ticker = underlying.strip().upper()
        path = f"/v1/open-close/{ticker}/{day.isoformat()}?adjusted=true"
        try:
            payload = self._get(path, ttl_s=TTL_VOL_S)
        except (HttpError, StaleCacheError, FeedError, RuntimeError):
            payload = None
        if payload:
            close = _num(payload.get("close") or payload.get("c"))
            if close is not None and close > 0:
                return close
        path2 = (
            f"/v2/aggs/ticker/{ticker}/range/1/day/{day.isoformat()}/{day.isoformat()}"
            f"?adjusted=true&limit=1"
        )
        try:
            aggs = self._get(path2, ttl_s=TTL_VOL_S)
        except (HttpError, StaleCacheError, FeedError, RuntimeError):
            return None
        rows = aggs.get("results") or []
        if not rows:
            return None
        return _num(rows[0].get("c"))

    def earnings_tickers(self, start: str, end: str) -> list[str] | None:
        """Named Massive/Benzinga calendar. None if the plan/key cannot serve it."""
        if not self.api_key:
            return None
        for tmpl in EARNINGS_PATHS:
            path = tmpl.format(start=start, end=end)
            try:
                payload = self._get(path, ttl_s=TTL_META_S)
            except (HttpError, StaleCacheError, FeedError, RuntimeError):
                continue
            names = _tickers_from_earnings(payload)
            if names:
                return names
        return None


def contracts_from_snapshot(
    payload: dict[str, Any],
    *,
    underlying: str,
    expiry: date | None,
    spot: float | None = None,
    realized_vol: float | None = None,
    years_to_expiry: float | None = None,
    venue: QuoteVenue = QuoteVenue.POLYGON,
) -> list[Contract]:
    results = _results_list(payload)
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
        if not isinstance(lq, dict):
            lq = {}
        # last_quote only. Never promote day.close / last_trade to an ask.
        bid = _num(lq.get("bid") or lq.get("bid_price"))
        ask = _num(lq.get("ask") or lq.get("ask_price"))
        last = _num((row.get("last_trade") or {}).get("price") or row.get("last"))
        oi = _int(row.get("open_interest"))
        vol = _int((row.get("day") or {}).get("volume") or row.get("volume"))
        shares = _int(
            details.get("shares_per_contract")
            or details.get("multiplier")
            or row.get("shares_per_contract")
        )
        defaulted = shares is None or shares <= 0
        if defaulted:
            shares = DEFAULT_MULTIPLIER
        greeks = row.get("greeks") or {}
        listed_iv = _num(
            greeks.get("iv")
            or row.get("implied_volatility")
            or (row.get("implied_volatility") if False else None)
        )
        if listed_iv is None:
            listed_iv = _num(row.get("implied_volatility"))
        out.append(
            Contract(
                contract_id=ticker,
                underlying=underlying.upper(),
                expiry=exp,
                strike=float(strike),
                contract_type=ctype,
                quote=Quote(bid=bid, ask=ask, last=last, open_interest=oi, volume=vol, venue=venue),
                spot=px,
                realized_vol=realized_vol,
                years_to_expiry=years_to_expiry,
                shares_per_contract=shares,
                multiplier_defaulted=defaulted,
                listed_iv=listed_iv,
                quote_venue=venue,
                nonstandard_deliverable=bool(shares and shares != DEFAULT_MULTIPLIER),
            )
        )
    return out


def _rewrite_host(url: str, base: str) -> str:
    parsed = urlparse(url)
    root = urlparse(base)
    if not parsed.netloc:
        return url
    return urlunparse(parsed._replace(scheme=root.scheme or parsed.scheme, netloc=root.netloc))


def _with_key(url: str, api_key: str) -> str:
    if "apiKey=" in url or "apikey=" in url.lower():
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}apiKey={api_key}"


def _results_list(payload: dict[str, Any]) -> list:
    results = payload.get("results") or payload.get("option_chain") or []
    if isinstance(results, dict):
        results = results.get("results") or []
    if not isinstance(results, list):
        return []
    return results


def _tickers_from_earnings(payload: dict[str, Any]) -> list[str]:
    rows = payload.get("results") or payload.get("tickers") or []
    out: list[str] = []
    seen = set()
    for row in rows:
        if isinstance(row, str):
            name = row.strip().upper()
        elif isinstance(row, dict):
            name = str(
                row.get("ticker")
                or row.get("symbol")
                or (row.get("stock") or {}).get("ticker")
                or ""
            ).strip().upper()
        else:
            continue
        if name and name not in seen:
            seen.add(name)
            out.append(name)
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
