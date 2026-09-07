"""15-min series registry. This PR ships KXBTC15M only.

Later CRYPTO15M tickers plug in here as unshipped specs. Fetch/parse still
refuse anything that is not shipped. Researcher hire is deferred — no
researcher docs live here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern


SHIPPED_SERIES = "KXBTC15M"
WINDOW_TOKEN = r"(\d{2}[A-Z]{3}\d{6})"


@dataclass(frozen=True)
class SeriesSpec:
    """Config hook for one 15-min Kalshi series."""

    series_ticker: str
    cf_index_id: str
    cfb_ws_average_role: str = "observe_only"
    expected_source_name: str = "CF Benchmarks"
    expected_source_host: str = "cfbenchmarks.com"
    fee_type: str = "quadratic"
    fee_multiplier: int = 1
    price_level_structure: str = "tapered_deci_cent"
    shipped: bool = False
    event_ticker_re: Pattern[str] | None = None
    market_ticker_re: Pattern[str] | None = None

    def compiled_event_re(self) -> Pattern[str]:
        if self.event_ticker_re is not None:
            return self.event_ticker_re
        return re.compile(rf"^{re.escape(self.series_ticker)}-{WINDOW_TOKEN}$")

    def compiled_market_re(self) -> Pattern[str]:
        if self.market_ticker_re is not None:
            return self.market_ticker_re
        return re.compile(rf"^{re.escape(self.series_ticker)}-{WINDOW_TOKEN}(?:-(\d{{2}}))?$")


class SeriesNotShippedError(ValueError):
    """Series is unknown or registered but not shipped in this PR."""


_REGISTRY: dict[str, SeriesSpec] = {}


def _kxbtc15m() -> SeriesSpec:
    return SeriesSpec(
        series_ticker=SHIPPED_SERIES,
        cf_index_id="BRTI",
        cfb_ws_average_role="observe_only",
        shipped=True,
    )


def register_series(spec: SeriesSpec) -> None:
    """Config hook. Only KXBTC15M may be marked shipped in this PR."""
    ticker = str(spec.series_ticker or "").strip().upper()
    if not ticker:
        raise SeriesNotShippedError("series_ticker is required")
    if spec.shipped and ticker != SHIPPED_SERIES:
        raise SeriesNotShippedError(
            f"{ticker} cannot be shipped in this PR; ship {SHIPPED_SERIES} only"
        )
    _REGISTRY[ticker] = spec


def get_series(ticker: str) -> SeriesSpec | None:
    return _REGISTRY.get(str(ticker or "").strip().upper())


def require_shipped_series(ticker: str | None = None) -> SeriesSpec:
    """Return the shipped spec. Any other ticker is refused."""
    want = str(ticker or SHIPPED_SERIES).strip().upper() or SHIPPED_SERIES
    spec = _REGISTRY.get(want)
    if spec is None:
        raise SeriesNotShippedError(
            f"unknown 15-min series {want!r}; this PR ships {SHIPPED_SERIES} only"
        )
    if not spec.shipped or want != SHIPPED_SERIES:
        raise SeriesNotShippedError(
            f"{want} is not shipped; this PR is {SHIPPED_SERIES} only"
        )
    return spec


def shipped_series_ticker() -> str:
    return require_shipped_series().series_ticker


def registered_tickers() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY))


register_series(_kxbtc15m())
