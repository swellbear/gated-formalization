"""Public/read Kalshi adapter for ONE series: KXBTC15M.

Live API: https://api.elections.kalshi.com/trade-api/v2/ (events/markets only).
No trade keys. No order placement. No private account endpoints.
Settlement SOURCE is CF Benchmarks as documented on event settlement_sources.
"""

from __future__ import annotations

import re
from typing import Any

from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.learning_lane_15m.paths import PRIMARY_SERIES
from golf_offshoot.localtime import format_eastern, now
from golf_offshoot.models.enums import DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality

KALSHI_PUBLIC_BASE = "https://api.elections.kalshi.com/trade-api/v2"
ALLOWED_SERIES = PRIMARY_SERIES
EXPECTED_SOURCE_NAME = "CF Benchmarks"
EXPECTED_SOURCE_HOST = "cfbenchmarks.com"

# Hard NO: any private / cash / order path. Public events+markets only.
_FORBIDDEN_PATH_FRAGMENTS = (
    "/portfolio",
    "/orders",
    "/order_groups",
    "/exchange/deposit",
    "/exchange/withdraw",
    "/exchange/transfers",
    "/exchange/transfer",
    "/login",
    "/api_keys",
    "/api-keys",
)

_PUBLIC_PATH_PREFIXES = (
    "/trade-api/v2/events",
    "/trade-api/v2/markets",
    "/trade-api/v2/series/",
)

TRADING_ARMED = False
# Pinned from KXBTC15M rules_primary (CF Benchmarks Bitcoin Real-Time Index).
# A CFB websocket / DIY 60s average is observe-only — never official settle.
CF_INDEX_ID = "BRTI"
CFB_WS_AVERAGE_ROLE = "observe_only"
# Event: KXBTC15M-YYMONDDHHMM. Market may append -MM (minute label, not series).
_EVENT_TICKER_RE = re.compile(r"^KXBTC15M-(\d{2}[A-Z]{3}\d{6})$")
_MARKET_TICKER_RE = re.compile(r"^KXBTC15M-(\d{2}[A-Z]{3}\d{6})(?:-(\d{2}))?$")
_FORBIDDEN_SERIES = frozenset({"KXBTC", "KXETH15M", "KXETH", "KXAG15M", "KXAU15M", "KXMETAL"})
FEE_TYPE = "quadratic"
FEE_MULTIPLIER = 1
PRICE_LEVEL_STRUCTURE = "tapered_deci_cent"
DISPLAY_ONLY_FIELDS = ("yes_bid", "yes_ask", "last", "volume")


class SeriesNotAllowedError(FeedError):
    """This adapter ships KXBTC15M only. Other series stay out of this PR."""


class PrivateEndpointRefused(FeedError):
    """Trade / cash / account endpoints are never called."""


def assert_public_read_url(url: str, *, series: str = ALLOWED_SERIES) -> None:
    """Refuse trade/private URLs and any series other than KXBTC15M."""
    low = str(url or "").lower()
    if any(frag in low for frag in _FORBIDDEN_PATH_FRAGMENTS):
        raise PrivateEndpointRefused(
            f"Kalshi private/trade endpoint refused (trading NOT ARMED): {url}"
        )
    if not any(prefix in low for prefix in _PUBLIC_PATH_PREFIXES):
        raise PrivateEndpointRefused(f"Kalshi URL is not a public events/markets read: {url}")
    if "series_ticker=" in low:
        want = f"series_ticker={series.lower()}"
        if want not in low:
            raise SeriesNotAllowedError(
                f"refusing series other than {series} (do not widen this PR): {url}"
            )
    if "/series/" in low and f"/series/{series.lower()}" not in low:
        raise SeriesNotAllowedError(
            f"refusing series other than {series} (do not widen this PR): {url}"
        )
    if "pyth" in low or any(s.lower() in low for s in _FORBIDDEN_SERIES if s != "KXBTC"):
        raise SeriesNotAllowedError(f"no multi-series / no Pyth metals in this PR: {url}")


def parse_optional_float(raw: Any) -> float | None:
    """Numeric helper. Missing stays missing — never invented."""
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def parse_dollar_unit(raw: Any) -> float | None:
    """Kalshi *_dollars fields are contract prices in (0, 1)."""
    if raw is None or raw == "":
        return None
    try:
        p = float(raw)
    except (TypeError, ValueError):
        return None
    if p <= 0.0 or p >= 1.0:
        return None
    return p


def parse_settlement_sources(raw: Any) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    if not isinstance(raw, list):
        return out
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        url = str(item.get("url") or "").strip()
        if name or url:
            out.append({"name": name, "url": url})
    return out


def source_is_cf_benchmarks(sources: list[dict[str, str]]) -> bool:
    """True when Kalshi documents CF Benchmarks on the event/series."""
    for src in sources:
        blob = f"{src.get('name', '')} {src.get('url', '')}".lower()
        if EXPECTED_SOURCE_NAME.lower() in blob or EXPECTED_SOURCE_HOST in blob:
            return True
    return False


class TickerParseError(FeedError):
    """KXBTC15M ticker did not match the locked window grammar."""


def refuse_btc_substring_series(raw: str) -> None:
    """Hard NO: do not treat 'BTC' or threshold series KXBTC as KXBTC15M."""
    token = str(raw or "").strip().upper()
    if token == "KXBTC" or token.startswith("KXBTC-"):
        raise SeriesNotAllowedError("do not use threshold series KXBTC; this PR is KXBTC15M only")
    if "BTC" in token and not token.startswith("KXBTC15M"):
        raise SeriesNotAllowedError("do not substring-match BTC; series id is exactly KXBTC15M")


def parse_event_ticker(raw: str) -> dict[str, str]:
    """Event ticker KXBTC15M-YYMONDDHHMM. Trailing -15 is not valid here."""
    ticker = str(raw or "").strip().upper()
    refuse_btc_substring_series(ticker)
    if ticker in _FORBIDDEN_SERIES:
        raise SeriesNotAllowedError(f"no multi-series in this PR: {ticker}")
    hit = _EVENT_TICKER_RE.fullmatch(ticker)
    if not hit:
        raise TickerParseError(
            f"event ticker must be KXBTC15M-YYMONDDHHMM (got {raw!r}). "
            "Do not treat a market suffix like -15 as the series."
        )
    return {
        "ticker": ticker,
        "series_ticker": ALLOWED_SERIES,
        "window_token": hit.group(1),
    }


def parse_market_ticker(raw: str) -> dict[str, str]:
    """Market ticker KXBTC15M-YYMONDDHHMM[-MM]. Trailing -15 is the minute label."""
    ticker = str(raw or "").strip().upper()
    refuse_btc_substring_series(ticker)
    hit = _MARKET_TICKER_RE.fullmatch(ticker)
    if not hit:
        raise TickerParseError(
            f"market ticker must be KXBTC15M-YYMONDDHHMM or …-MM (got {raw!r}). "
            "Trailing -15 is not a series id."
        )
    window = hit.group(1)
    suffix = hit.group(2) or ""
    return {
        "ticker": ticker,
        "series_ticker": ALLOWED_SERIES,
        "event_ticker": f"{ALLOWED_SERIES}-{window}",
        "window_token": window,
        "minute_suffix": suffix,
    }


def window_id(
    *,
    event_ticker: str,
    open_time: str = "",
    close_time: str = "",
) -> str:
    """UTC open/close journal key. If close_time moves, the window re-keys."""
    ev = str(event_ticker or "").strip()
    open_utc = str(open_time or "").strip()
    close_utc = str(close_time or "").strip()
    if open_utc or close_utc:
        return f"{ev}__{open_utc}__{close_utc}"
    return ev


def parse_kalshi_result(raw: Any) -> str:
    """Official Kalshi result token. Empty means not yet official."""
    token = str(raw or "").strip().lower()
    if token in {"yes", "no"}:
        return token
    return ""


def public_mid_or_last(
    *,
    yes_bid: float | None,
    yes_ask: float | None,
    last: float | None,
) -> float | None:
    """Paper mark from public mid, else last. Display-only — never settle evidence."""
    if yes_bid is not None and yes_ask is not None:
        mid = (yes_bid + yes_ask) / 2.0
        if 0.0 < mid < 1.0:
            return mid
    if last is not None and 0.0 < last < 1.0:
        return last
    if yes_ask is not None and 0.0 < yes_ask < 1.0:
        return yes_ask
    return None


def market_is_open(market: dict[str, Any]) -> bool:
    status = str(market.get("status") or "").strip().lower()
    if status in {"finalized", "settled", "closed", "determined", "initialized", "unopened"}:
        return False
    if status in {"active", "open"}:
        return True
    # Tradable ask is enough to treat as live observation.
    return parse_dollar_unit(market.get("yes_ask_dollars")) is not None


def is_paper_autobet_candidate(market: dict[str, Any]) -> bool:
    """Open/active book with a usable mark. Skip initialized / null-price rows."""
    status = str(market.get("status") or "").strip().lower()
    if status == "initialized":
        return False
    if not market.get("is_open") and status not in {"active", "open"}:
        return False
    mark = market.get("paper_mark")
    if mark is None:
        mark = market.get("yes_ask")
    try:
        yes_f = float(mark) if mark is not None else None
    except (TypeError, ValueError):
        return False
    return yes_f is not None and 0.0 < yes_f < 1.0


def parse_event(raw: dict[str, Any]) -> dict[str, Any]:
    ticker = str(raw.get("event_ticker") or raw.get("ticker") or "").strip()
    series = str(raw.get("series_ticker") or "").strip()
    if series and series != ALLOWED_SERIES:
        raise SeriesNotAllowedError(f"event series {series!r} is not {ALLOWED_SERIES}")
    parsed_tick = parse_event_ticker(ticker)
    sources = parse_settlement_sources(raw.get("settlement_sources"))
    return {
        "event_ticker": parsed_tick["ticker"],
        "series_ticker": ALLOWED_SERIES,
        "window_token": parsed_tick["window_token"],
        "title": str(raw.get("title") or ""),
        "sub_title": str(raw.get("sub_title") or ""),
        "strike_date": str(raw.get("strike_date") or ""),
        "category": str(raw.get("category") or ""),
        "settlement_sources": sources,
        "source_is_cf_benchmarks": source_is_cf_benchmarks(sources),
        "product_metadata": raw.get("product_metadata") or {},
        "fee_type": str(raw.get("fee_type") or FEE_TYPE),
        "fee_multiplier": parse_optional_float(raw.get("fee_multiplier")) or FEE_MULTIPLIER,
    }


def parse_market(raw: dict[str, Any], *, event: dict[str, Any] | None = None) -> dict[str, Any]:
    parsed_m = parse_market_ticker(str(raw.get("ticker") or ""))
    ticker = parsed_m["ticker"]
    raw_event = str(raw.get("event_ticker") or (event or {}).get("event_ticker") or "").strip()
    if raw_event:
        event_ticker = parse_event_ticker(raw_event)["ticker"]
    else:
        event_ticker = parsed_m["event_ticker"]
    yes_ask = parse_dollar_unit(raw.get("yes_ask_dollars"))
    yes_bid = parse_dollar_unit(raw.get("yes_bid_dollars"))
    last = parse_dollar_unit(raw.get("last_price_dollars"))
    mark = public_mid_or_last(yes_bid=yes_bid, yes_ask=yes_ask, last=last)
    result = parse_kalshi_result(raw.get("result"))
    status = str(raw.get("status") or "").strip().lower()
    sources = parse_settlement_sources(
        raw.get("settlement_sources") or (event or {}).get("settlement_sources") or []
    )
    decimal = (1.0 / mark) if mark else None
    floor_strike = parse_optional_float(raw.get("floor_strike"))
    open_utc = str(raw.get("open_time") or "")
    close_utc = str(raw.get("close_time") or "")
    return {
        "ticker": ticker,
        "event_ticker": event_ticker,
        "series_ticker": ALLOWED_SERIES,
        "window_token": parsed_m["window_token"],
        "minute_suffix": parsed_m["minute_suffix"],
        "window_id": window_id(event_ticker=event_ticker, open_time=open_utc, close_time=close_utc),
        "title": str(raw.get("title") or ""),
        "yes_sub_title": str(raw.get("yes_sub_title") or ""),
        "no_sub_title": str(raw.get("no_sub_title") or ""),
        "status": status,
        "result": result,
        "yes_ask": yes_ask,
        "yes_bid": yes_bid,
        "last": last,
        "volume": parse_optional_float(raw.get("volume_fp") or raw.get("volume")),
        "paper_mark": mark,
        "implied_yes": mark,
        "decimal_odds": decimal,
        "display_only_prices": True,
        "open_time": open_utc,
        "close_time": close_utc,
        "open_time_et": format_eastern(open_utc) if open_utc else "n/a",
        "close_time_et": format_eastern(close_utc) if close_utc else "n/a",
        "can_close_early": bool(raw.get("can_close_early")),
        "rules_primary": str(raw.get("rules_primary") or ""),
        "rules_secondary": str(raw.get("rules_secondary") or ""),
        "cf_index_id": CF_INDEX_ID,
        "cfb_ws_average_role": CFB_WS_AVERAGE_ROLE,
        "et_title_display_only": True,
        "floor_strike": floor_strike,
        "expiration_value": str(raw.get("expiration_value") or ""),
        "settlement_ts": str(raw.get("settlement_ts") or ""),
        "settlement_value_dollars": parse_optional_float(raw.get("settlement_value_dollars")),
        "settlement_sources": sources,
        "source_is_cf_benchmarks": source_is_cf_benchmarks(sources),
        "fee_type": str((event or {}).get("fee_type") or raw.get("fee_type") or FEE_TYPE),
        "fee_multiplier": parse_optional_float(
            (event or {}).get("fee_multiplier") or raw.get("fee_multiplier")
        )
        or FEE_MULTIPLIER,
        "price_level_structure": str(
            raw.get("price_level_structure") or PRICE_LEVEL_STRUCTURE
        ),
        "is_open": market_is_open(raw),
        "trading_armed": TRADING_ARMED,
    }


class Kalshi15mFeed(DataFeed[dict[str, Any]]):
    """Read-only KXBTC15M events + markets. Observation only."""

    name = "kalshi_15m"
    role = DataRole.PRIMARY

    def __init__(self, cache: HttpCache | None = None, refresh: bool = False) -> None:
        self.cache = cache or HttpCache()
        self.refresh = refresh
        self._last_meta: dict[str, Any] = {}

    def fetch(self, **kwargs: Any) -> tuple[dict[str, Any], DataQuality]:
        series = str(kwargs.get("series") or ALLOWED_SERIES)
        if series != ALLOWED_SERIES:
            raise SeriesNotAllowedError(
                f"do not widen past {ALLOWED_SERIES} in this PR (got {series!r})"
            )
        limit = int(kwargs.get("limit") or 20)
        refresh = bool(kwargs.get("refresh", self.refresh))
        ttl = float(kwargs.get("ttl_seconds") or 15.0)
        series_meta = self._get_series(ttl_seconds=ttl, refresh=refresh)
        events = self._get_events(limit=limit, ttl_seconds=ttl, refresh=refresh)
        markets = self._get_markets(limit=limit, ttl_seconds=ttl, refresh=refresh)
        by_event = {ev["event_ticker"]: ev for ev in events if ev.get("event_ticker")}
        series_sources = series_meta.get("settlement_sources") or []
        joined: list[dict[str, Any]] = []
        for mkt in markets:
            ev = by_event.get(mkt["event_ticker"])
            if not mkt["settlement_sources"]:
                mkt = dict(mkt)
                if ev is not None and ev.get("settlement_sources"):
                    mkt["settlement_sources"] = ev["settlement_sources"]
                    mkt["source_is_cf_benchmarks"] = ev["source_is_cf_benchmarks"]
                elif series_sources:
                    mkt["settlement_sources"] = series_sources
                    mkt["source_is_cf_benchmarks"] = source_is_cf_benchmarks(series_sources)
            joined.append(mkt)
        payload = {
            "series": ALLOWED_SERIES,
            "series_meta": series_meta,
            "cf_index_id": CF_INDEX_ID,
            "cfb_ws_average_role": CFB_WS_AVERAGE_ROLE,
            "fee_type": series_meta.get("fee_type") or FEE_TYPE,
            "fee_multiplier": series_meta.get("fee_multiplier") or FEE_MULTIPLIER,
            "price_level_structure": PRICE_LEVEL_STRUCTURE,
            "events": events,
            "markets": joined,
            "trading_armed": TRADING_ARMED,
            "public_read_only": True,
            "fetched_at": now().isoformat(),
        }
        meta = self._last_meta or {}
        age_s = float(meta.get("age_seconds") or 0.0)
        if not events and not joined:
            q = unavailable_quality(
                self.name,
                f"no public {ALLOWED_SERIES} events/markets (not invented)",
            )
            q.lag_hours = age_s / 3600.0
            return payload, q
        notes = (
            f"public {ALLOWED_SERIES} events={len(events)} markets={len(joined)}; "
            "read-only Kalshi elections API; no keys; no orders; "
            "settlement SOURCE = CF Benchmarks via event settlement_sources; "
            f"fetched_at={meta.get('fetched_at')}; cached={meta.get('cached')}"
        )
        q = DataQuality(
            score=0.70 if not meta.get("stale_fallback") else 0.50,
            role=self.role,
            source_name=self.name,
            as_of=now(),
            n_observations=len(joined) or len(events),
            lag_hours=age_s / 3600.0,
            notes=notes,
            source_kind=SourceKind.REAL_LIVE,
        )
        return payload, q

    def _get_series(self, *, ttl_seconds: float, refresh: bool) -> dict[str, Any]:
        url = f"{KALSHI_PUBLIC_BASE}/series/{ALLOWED_SERIES}?include_volume=true"
        body = self._get(url, label="kalshi_15m_series", ttl_seconds=ttl_seconds, refresh=refresh)
        raw = body.get("series") if isinstance(body, dict) else None
        if not isinstance(raw, dict):
            return {
                "ticker": ALLOWED_SERIES,
                "settlement_sources": [],
                "fee_type": FEE_TYPE,
                "fee_multiplier": FEE_MULTIPLIER,
                "cf_index_id": CF_INDEX_ID,
            }
        sources = parse_settlement_sources(raw.get("settlement_sources"))
        return {
            "ticker": str(raw.get("ticker") or ALLOWED_SERIES),
            "title": str(raw.get("title") or ""),
            "settlement_sources": sources,
            "source_is_cf_benchmarks": source_is_cf_benchmarks(sources),
            "fee_type": str(raw.get("fee_type") or FEE_TYPE),
            "fee_multiplier": parse_optional_float(raw.get("fee_multiplier")) or FEE_MULTIPLIER,
            "contract_terms_url": str(raw.get("contract_terms_url") or ""),
            "cf_index_id": CF_INDEX_ID,
            "volume": parse_optional_float(raw.get("volume_fp") or raw.get("volume")),
        }

    def _get_events(self, *, limit: int, ttl_seconds: float, refresh: bool) -> list[dict[str, Any]]:
        return self._get_status_pages(
            path="events",
            list_key="events",
            parse=parse_event,
            id_field="event_ticker",
            limit=limit,
            ttl_seconds=ttl_seconds,
            refresh=refresh,
            label_prefix="kalshi_15m_events",
        )

    def _get_markets(self, *, limit: int, ttl_seconds: float, refresh: bool) -> list[dict[str, Any]]:
        return self._get_status_pages(
            path="markets",
            list_key="markets",
            parse=parse_market,
            id_field="ticker",
            limit=limit,
            ttl_seconds=ttl_seconds,
            refresh=refresh,
            label_prefix="kalshi_15m_markets",
        )

    def _get_status_pages(
        self,
        *,
        path: str,
        list_key: str,
        parse,
        id_field: str,
        limit: int,
        ttl_seconds: float,
        refresh: bool,
        label_prefix: str,
    ) -> list[dict[str, Any]]:
        """Prefer status=open, then merge settled for settle-join."""
        seen: dict[str, dict[str, Any]] = {}
        order: list[str] = []
        for status in ("open", "settled"):
            url = (
                f"{KALSHI_PUBLIC_BASE}/{path}"
                f"?series_ticker={ALLOWED_SERIES}&status={status}&limit={limit}"
            )
            body = self._get(
                url,
                label=f"{label_prefix}_{status}",
                ttl_seconds=ttl_seconds,
                refresh=refresh,
            )
            rows = body.get(list_key) if isinstance(body, dict) else None
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                try:
                    parsed = parse(row)
                except (TickerParseError, SeriesNotAllowedError):
                    continue
                key = str(parsed.get(id_field) or "")
                if not key or key in seen:
                    continue
                seen[key] = parsed
                order.append(key)
        return [seen[key] for key in order]

    def _get(self, url: str, *, label: str, ttl_seconds: float, refresh: bool) -> Any:
        assert_public_read_url(url)
        try:
            body, meta = self.cache.get_json(
                url,
                headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
                ttl_seconds=ttl_seconds,
                refresh=refresh,
                label=label,
                allow_stale_on_error=True,
            )
        except FeedError:
            return None
        self._last_meta = meta
        return body
