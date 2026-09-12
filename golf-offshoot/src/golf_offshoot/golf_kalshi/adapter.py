"""Public Kalshi golf catalog. Does not widen kalshi_15m ALLOWED_SERIES."""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qs, quote, urlparse

from golf_offshoot.data_feeds.base import FeedError
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.data_feeds.kalshi_15m import (
    KALSHI_PUBLIC_BASE,
    PrivateEndpointRefused,
    parse_dollar_unit,
    parse_kalshi_result,
    parse_optional_float,
)
from golf_offshoot.golf_kalshi.paths import assert_golf_kalshi_path, cache_dir, catalog_path
from golf_offshoot.localtime import isoformat_now, now, to_eastern

LANE = "golf_kalshi"
TRADING_ARMED = False
SERIES_TTL_S = 20 * 60
MARKETS_TTL_S = 90.0
SETTLED_TTL_S = 5 * 60
SERIES_PAGE_LIMIT = 200
MARKETS_PAGE_LIMIT = 200
MAX_SERIES_PAGES = 20
MARKETS_MAX_PAGES = 6
SETTLED_MAX_PAGES = 1
GOLF_TAG = "golf"
# Kalshi ticker stems we have already seen on Golf-tagged series. Not an invent list.
GOLF_TICKER_PREFIXES = (
    "KXPGA",
    "KXLPGA",
    "KXLIV",
    "KXCHAMPTOUR",
)
REJECT_TAGS = frozenset(
    {
        "soccer",
        "football",
        "nfl",
        "nba",
        "mlb",
        "nhl",
        "tennis",
        "basketball",
        "baseball",
        "hockey",
        "politics",
        "crypto",
        "esports",
        "ufc",
        "mma",
        "racing",
        "f1",
    }
)
_GOLF_TITLE_RE = re.compile(
    r"\b(golf|lpga|pga\s+tour|pga\s+championship|ryder\s+cup|solheim(?:\s+cup)?|liv\s+golf)\b",
    re.I,
)
FORBIDDEN_PATH_FRAGMENTS = (
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
PUBLIC_PATH_PREFIXES = (
    "/trade-api/v2/events",
    "/trade-api/v2/markets",
    "/trade-api/v2/series",
)
FORBIDDEN_SERIES_PREFIXES = (
    "KXBTC",
    "KXETH",
    "KXAG15M",
    "KXAU15M",
    "KXMETAL",
)
CRYPTO_TOKENS = (
    "bitcoin",
    "btc",
    "ethereum",
    "eth",
    "crypto",
    "pyth",
    "kxbtc15m",
)


class GolfSeriesRefused(FeedError):
    """Crypto / 15m / non-golf series stay out of this adapter."""


def observed_fee_fields(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Series fee fields as Kalshi sent them. Missing stays missing.

    Local to this island so ``kalshi_15m.py`` is not widened.
    """
    if not isinstance(raw, dict):
        return {
            "fee_type": None,
            "fee_multiplier": None,
            "fee_type_present": False,
            "fee_multiplier_present": False,
        }
    type_raw = raw.get("fee_type")
    type_present = type_raw is not None and str(type_raw).strip() != ""
    mult_raw = raw.get("fee_multiplier")
    mult_present = "fee_multiplier" in raw and mult_raw is not None and mult_raw != ""
    return {
        "fee_type": str(type_raw).strip() if type_present else None,
        "fee_multiplier": parse_optional_float(mult_raw) if mult_present else None,
        "fee_type_present": type_present,
        "fee_multiplier_present": mult_present,
    }


def is_crypto_or_15m_series(ticker: str, *, category: str = "", title: str = "") -> bool:
    token = str(ticker or "").strip().upper()
    blob = f"{ticker} {category} {title}".lower()
    if any(token.startswith(prefix) for prefix in FORBIDDEN_SERIES_PREFIXES):
        return True
    if "kxbtc15m" in blob or "kxbeth" in blob:
        return True
    if any(word in blob for word in ("bitcoin", "ethereum", "crypto index")):
        return True
    return False


def _norm_tags(tags: list[str] | None) -> set[str]:
    return {str(t).strip().lower() for t in (tags or []) if str(t).strip()}


def is_golf_series(
    ticker: str,
    *,
    category: str = "",
    title: str = "",
    tags: list[str] | None = None,
) -> bool:
    """Kalshi Golf tag, known golf ticker stem, or golf words in the title.

    Substring ``pga`` is not enough: ``cupgame`` / ``capgain`` / Liga Pro
    tickers match that by accident. Tennis Masters and US Open Cup are not golf.
    """
    if is_crypto_or_15m_series(ticker, category=category, title=title):
        return False
    tags_l = _norm_tags(tags)
    if GOLF_TAG in tags_l:
        return True
    if str(category or "").strip().lower() in REJECT_TAGS or tags_l & REJECT_TAGS:
        return False
    token = str(ticker or "").strip().upper()
    if any(token.startswith(prefix) for prefix in GOLF_TICKER_PREFIXES):
        return True
    return bool(_GOLF_TITLE_RE.search(str(title or "")))


def assert_golf_public_url(url: str) -> None:
    """Refuse private URLs and crypto/15m series. Unarmed public reads only."""
    low = str(url or "").lower()
    if any(frag in low for frag in FORBIDDEN_PATH_FRAGMENTS):
        raise PrivateEndpointRefused(
            f"Kalshi private/trade endpoint refused (trading NOT ARMED): {url}"
        )
    if not any(prefix in low for prefix in PUBLIC_PATH_PREFIXES):
        raise PrivateEndpointRefused(f"Kalshi URL is not a public events/markets/series read: {url}")
    parsed = urlparse(url)
    path = (parsed.path or "").rstrip("/")
    qs = parse_qs(parsed.query or "")
    if path.endswith("/markets") and not qs.get("series_ticker"):
        raise GolfSeriesRefused(f"golf catalog refuses unscoped market dump: {url}")
    for prefix in FORBIDDEN_SERIES_PREFIXES:
        if f"series_ticker={prefix.lower()}" in low:
            raise GolfSeriesRefused(f"refusing 15m/crypto series: {url}")
        if f"/series/{prefix.lower()}" in low:
            raise GolfSeriesRefused(f"refusing 15m/crypto series: {url}")
    if any(tok in low for tok in CRYPTO_TOKENS if tok in {"kxbtc15m", "pyth"}):
        raise GolfSeriesRefused(f"refusing crypto/15m URL: {url}")


def _tag_list(raw: Any) -> list[str]:
    if isinstance(raw, list):
        return [str(x) for x in raw]
    if isinstance(raw, str) and raw.strip():
        return [raw.strip()]
    return []


def parse_series(raw: dict[str, Any]) -> dict[str, Any] | None:
    ticker = str(raw.get("ticker") or raw.get("series_ticker") or "").strip()
    if not ticker:
        return None
    category = str(raw.get("category") or "")
    title = str(raw.get("title") or raw.get("frequency") or "")
    tags = _tag_list(raw.get("tags") or raw.get("category_tags"))
    fees = observed_fee_fields(raw)
    if not is_golf_series(ticker, category=category, title=title, tags=tags):
        return None
    return {
        "series_ticker": ticker,
        "title": title,
        "category": category,
        "tags": tags,
        "fee_type": fees.get("fee_type"),
        "fee_multiplier": fees.get("fee_multiplier"),
        "fee_type_present": fees.get("fee_type_present"),
        "fee_multiplier_present": fees.get("fee_multiplier_present"),
    }


def parse_market(raw: dict[str, Any], *, series: dict[str, Any] | None = None) -> dict[str, Any] | None:
    ticker = str(raw.get("ticker") or "").strip()
    series_ticker = str(
        raw.get("series_ticker") or (series or {}).get("series_ticker") or ""
    ).strip()
    title = str(raw.get("title") or "")
    category = str(raw.get("category") or (series or {}).get("category") or "")
    if not series_ticker:
        return None
    if is_crypto_or_15m_series(series_ticker or ticker, category=category, title=title):
        return None
    if not is_golf_series(
        series_ticker,
        category=category,
        title=title or str((series or {}).get("title") or ""),
        tags=_tag_list((series or {}).get("tags")),
    ):
        return None
    yes_ask = parse_dollar_unit(raw.get("yes_ask_dollars") if raw.get("yes_ask_dollars") is not None else raw.get("yes_ask"))
    yes_bid = parse_dollar_unit(raw.get("yes_bid_dollars") if raw.get("yes_bid_dollars") is not None else raw.get("yes_bid"))
    last = parse_dollar_unit(raw.get("last_price_dollars") if raw.get("last_price_dollars") is not None else raw.get("last_price"))
    size = parse_optional_float(
        raw.get("yes_ask_size_fp")
        or raw.get("volume_fp")
        or raw.get("open_interest_fp")
        or raw.get("yes_ask_size")
    )
    spread = None
    if yes_ask is not None and yes_bid is not None:
        spread = round(float(yes_ask) - float(yes_bid), 6)
    fee_src = series or raw
    fees = observed_fee_fields(fee_src)
    status = str(raw.get("status") or "").strip().lower()
    result = parse_kalshi_result(raw.get("result"))
    close_time = str(raw.get("close_time") or raw.get("expiration_time") or "")
    can_close_early = bool(raw.get("can_close_early"))
    # Open is listed. In-play is Kalshi saying the contract can resolve now.
    in_play = can_close_early
    return {
        "ticker": ticker,
        "event_ticker": str(raw.get("event_ticker") or "").strip(),
        "series_ticker": series_ticker,
        "title": title,
        "yes_sub_title": str(raw.get("yes_sub_title") or raw.get("subtitle") or ""),
        "status": status,
        "result": result,
        "yes_ask": yes_ask,
        "yes_bid": yes_bid,
        "last": last,
        "displayed_size": size,
        "spread": spread,
        "fee_type": fees.get("fee_type"),
        "fee_multiplier": fees.get("fee_multiplier"),
        "fee_multiplier_present": bool(fees.get("fee_multiplier_present")),
        "open_time": str(raw.get("open_time") or ""),
        "close_time": close_time,
        "can_close_early": can_close_early,
        "in_play": in_play,
        "event_title": str(raw.get("event_title") or (series or {}).get("title") or ""),
        "trading_armed": TRADING_ARMED,
    }


def golf_only_catalog(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Drop soccer/parlay/politics rows. Fail-open never re-serves a mixed dump."""
    empty = {"lane": LANE, "series": [], "markets": []}
    if not isinstance(payload, dict):
        return empty
    series: list[dict[str, Any]] = []
    by_ticker: dict[str, dict[str, Any]] = {}
    for raw in payload.get("series") or []:
        if not isinstance(raw, dict):
            continue
        parsed = parse_series(raw)
        if parsed is None:
            continue
        series.append(parsed)
        by_ticker[parsed["series_ticker"]] = parsed
    markets: list[dict[str, Any]] = []
    for raw in payload.get("markets") or []:
        if not isinstance(raw, dict):
            continue
        st = str(raw.get("series_ticker") or "").strip()
        parsed_m = parse_market(raw, series=by_ticker.get(st))
        if parsed_m is None:
            continue
        if parsed_m["series_ticker"] not in by_ticker:
            continue
        markets.append(parsed_m)
    return {
        "lane": LANE,
        "series": series,
        "markets": markets,
        "fail_open": bool(payload.get("fail_open")),
        "saved_at": payload.get("saved_at") or "",
    }


def load_last_good_catalog() -> dict[str, Any]:
    path = catalog_path()
    if not path.is_file():
        return {"lane": LANE, "series": [], "markets": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"lane": LANE, "series": [], "markets": []}
    if not isinstance(payload, dict):
        return {"lane": LANE, "series": [], "markets": []}
    cleaned = golf_only_catalog(payload)
    raw_n = len(payload.get("series") or []) + len(payload.get("markets") or [])
    if raw_n != len(cleaned["series"]) + len(cleaned["markets"]):
        save_catalog(cleaned)
    return cleaned


def save_catalog(payload: dict[str, Any]) -> None:
    path = catalog_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    payload = golf_only_catalog(payload)
    payload = dict(payload)
    payload["lane"] = LANE
    payload["saved_at"] = isoformat_now()
    payload["trading_armed"] = TRADING_ARMED
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def catalog_is_fresh(payload: dict[str, Any] | None, *, ttl_seconds: float = MARKETS_TTL_S) -> bool:
    """Last-good catalog is still inside the markets TTL. Fail-open is never fresh."""
    if not isinstance(payload, dict) or payload.get("fail_open"):
        return False
    if not (payload.get("series") or payload.get("markets")):
        return False
    saved = str(payload.get("saved_at") or "").strip()
    if not saved:
        return False
    from datetime import datetime

    try:
        ts = datetime.fromisoformat(saved.replace("Z", "+00:00"))
    except ValueError:
        return False
    age = (now() - to_eastern(ts)).total_seconds()
    return 0 <= age < float(ttl_seconds)


class GolfKalshiFeed:
    """Public events/markets/series. One catalog fetch helper. Fail-open last-good."""

    def __init__(self, cache: HttpCache | None = None) -> None:
        self.http = cache or HttpCache(cache_dir=cache_dir())

    def _get(self, url: str, *, label: str, ttl_seconds: float, refresh: bool) -> Any:
        assert_golf_public_url(url)
        payload, _meta = self.http.get_json(
            url,
            headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
            ttl_seconds=ttl_seconds,
            refresh=refresh,
            label=label,
            allow_stale_on_error=True,
        )
        return payload

    def _page_rows(
        self,
        url: str,
        *,
        list_key: str,
        label: str,
        ttl_seconds: float,
        refresh: bool,
        max_pages: int = 1,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        cursor = ""
        for page in range(max(1, int(max_pages))):
            page_url = url if not cursor else f"{url}&cursor={quote(cursor)}"
            payload = self._get(
                page_url,
                label=f"{label}-{page}",
                ttl_seconds=ttl_seconds,
                refresh=refresh,
            )
            if isinstance(payload, dict):
                chunk = payload.get(list_key)
            else:
                chunk = payload
            if isinstance(chunk, list):
                rows.extend(row for row in chunk if isinstance(row, dict))
            nxt = ""
            if isinstance(payload, dict):
                nxt = str(payload.get("cursor") or "").strip()
            if not nxt or nxt == cursor:
                break
            cursor = nxt
        return rows

    def _golf_series_rows(self, *, refresh: bool) -> list[dict[str, Any]]:
        tagged = self._page_rows(
            f"{KALSHI_PUBLIC_BASE}/series?tags={quote('Golf')}&limit={SERIES_PAGE_LIMIT}",
            list_key="series",
            label="golf-kalshi-series",
            ttl_seconds=SERIES_TTL_S,
            refresh=refresh,
            max_pages=MAX_SERIES_PAGES,
        )
        parsed = [p for raw in tagged if (p := parse_series(raw)) is not None]
        if parsed:
            return parsed
        sports = self._page_rows(
            f"{KALSHI_PUBLIC_BASE}/series?category={quote('Sports')}&limit={SERIES_PAGE_LIMIT}",
            list_key="series",
            label="golf-kalshi-series-sports",
            ttl_seconds=SERIES_TTL_S,
            refresh=refresh,
            max_pages=MAX_SERIES_PAGES,
        )
        return [p for raw in sports if (p := parse_series(raw)) is not None]

    def _markets_for_series(
        self,
        series_ticker: str,
        *,
        status: str,
        ttl_seconds: float,
        refresh: bool,
        max_pages: int | None = None,
    ) -> list[dict[str, Any]]:
        st = quote(str(series_ticker).strip(), safe="")
        pages = MARKETS_MAX_PAGES if max_pages is None else int(max_pages)
        return self._page_rows(
            f"{KALSHI_PUBLIC_BASE}/markets?series_ticker={st}&status={quote(status)}&limit={MARKETS_PAGE_LIMIT}",
            list_key="markets",
            label=f"golf-kalshi-markets-{status}-{series_ticker}",
            ttl_seconds=ttl_seconds,
            refresh=refresh,
            max_pages=pages,
        )

    def fetch_catalog(self, *, refresh: bool = False) -> dict[str, Any]:
        """Golf-tagged series, then markets for those series only. Never the global open book."""
        last = load_last_good_catalog()
        if not refresh and catalog_is_fresh(last):
            return last
        try:
            series = self._golf_series_rows(refresh=refresh)
        except Exception:
            return last
        if not series:
            return last if last.get("series") else {"lane": LANE, "series": [], "markets": [], "fail_open": True}
        by_ticker = {row["series_ticker"]: row for row in series}
        markets: list[dict[str, Any]] = []
        seen: set[str] = set()
        any_ok = False
        for row in series:
            st = row["series_ticker"]
            try:
                open_rows = self._markets_for_series(
                    st, status="open", ttl_seconds=MARKETS_TTL_S, refresh=refresh
                )
                settled_rows = self._markets_for_series(
                    st,
                    status="settled",
                    ttl_seconds=SETTLED_TTL_S,
                    refresh=refresh,
                    max_pages=SETTLED_MAX_PAGES,
                )
                any_ok = True
            except Exception:
                for old in last.get("markets") or []:
                    if str(old.get("series_ticker") or "") == st:
                        ticker = str(old.get("ticker") or "")
                        if ticker and ticker not in seen:
                            seen.add(ticker)
                            markets.append(old)
                continue
            for raw in list(open_rows) + list(settled_rows):
                parsed_m = parse_market(raw, series=by_ticker.get(st))
                if parsed_m is None:
                    continue
                if parsed_m["series_ticker"] not in by_ticker:
                    continue
                ticker = str(parsed_m.get("ticker") or "")
                if not ticker or ticker in seen:
                    continue
                seen.add(ticker)
                markets.append(parsed_m)
        if not any_ok and not markets:
            return last
        catalog = golf_only_catalog(
            {
                "lane": LANE,
                "series": series,
                "markets": markets,
                "fail_open": False,
            }
        )
        save_catalog(catalog)
        return catalog
