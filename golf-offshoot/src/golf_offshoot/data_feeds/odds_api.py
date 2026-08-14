"""The Odds API connector. Requires THE_ODDS_API_KEY. Never invents quotes."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.config import ODDS_TTL_LIVE_SECONDS, ODDS_TTL_PRE_SECONDS
from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.data_feeds.local_env import load_local_env
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.models.enums import BetType, DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality, MarketQuote

ODDS_BASE = "https://api.the-odds-api.com/v4"
# Common PGA keys; we probe the sports catalog when a key is present.
CANDIDATE_SPORT_KEYS = (
    "golf_pga_championship",
    "golf_pga_tour",
    "golf_masters_tournament",
    "golf_the_open_championship",
    "golf_us_open",
)


class OddsApiFeed(DataFeed[list[MarketQuote]]):
    name = "the_odds_api"
    role = DataRole.PRIMARY

    def __init__(self, cache: HttpCache | None = None, api_key: str | None = None) -> None:
        load_local_env()
        self.cache = cache or HttpCache()
        self.api_key = api_key if api_key is not None else os.environ.get("THE_ODDS_API_KEY", "").strip()
        self._live = False
        self._ttl: float | None = None
        self._refresh = False
        self._last_meta: dict[str, Any] = {}

    def fetch(self, **kwargs: Any) -> tuple[list[MarketQuote], DataQuality]:
        name_to_id: dict[str, str] = kwargs.get("name_to_id") or {}
        self._live = bool(kwargs.get("live", False))
        self._ttl = kwargs.get("ttl_seconds")
        self._refresh = bool(kwargs.get("refresh", False))
        if not self.api_key:
            q = unavailable_quality(
                self.name,
                "THE_ODDS_API_KEY not set; market odds unavailable (not mocked)",
            )
            return [], q
        sports = self._sports()
        golf = [s for s in sports if "golf" in str(s.get("key", "")).lower() or "golf" in str(s.get("group", "")).lower()]
        if not golf:
            q = unavailable_quality(self.name, "Odds API sports catalog has no golf keys right now")
            return [], q
        quotes: list[MarketQuote] = []
        used = None
        for sport in golf:
            key = sport.get("key")
            if not key:
                continue
            try:
                payload = self._odds(str(key))
            except FeedError:
                continue
            used = key
            quotes.extend(self._parse_quotes(payload, name_to_id))
            if quotes:
                break
        if not quotes:
            q = unavailable_quality(
                self.name,
                f"Odds API returned no matchable golf outrights (tried group size {len(golf)})",
            )
            return [], q
        meta = getattr(self, "_last_meta", {}) or {}
        age_s = float(meta.get("age_seconds") or 0.0)
        notes = (
            f"decimal outrights from The Odds API; unmatched names dropped; "
            f"fetched_at={meta.get('fetched_at')}; cached={meta.get('cached')}; age_s={age_s:.0f}"
        )
        if meta.get("stale_fallback"):
            notes += "; STALE_FALLBACK"
        q = DataQuality(
            score=0.55 if meta.get("stale_fallback") else 0.75,
            role=self.role,
            source_name=f"{self.name}:{used}",
            as_of=datetime.now(timezone.utc),
            n_observations=len(quotes),
            lag_hours=age_s / 3600.0,
            notes=notes,
            source_kind=SourceKind.REAL_LIVE,
        )
        return quotes, q

    def _sports(self) -> list[dict[str, Any]]:
        url = f"{ODDS_BASE}/sports/?apiKey={self.api_key}"
        ttl = float(self._ttl) if self._ttl is not None else 3600.0
        body, _ = self.cache.get_json(
            url,
            headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
            ttl_seconds=ttl if self._live else 3600.0,
            refresh=self._refresh,
            label="odds_api_sports",
            allow_stale_on_error=True,
        )
        return body if isinstance(body, list) else []

    def _odds(self, sport_key: str) -> Any:
        url = (
            f"{ODDS_BASE}/sports/{sport_key}/odds/?apiKey={self.api_key}"
            f"&regions=us&markets=outrights&oddsFormat=decimal"
        )
        ttl = float(self._ttl) if self._ttl is not None else (
            ODDS_TTL_LIVE_SECONDS if self._live else ODDS_TTL_PRE_SECONDS
        )
        body, meta = self.cache.get_json(
            url,
            headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
            ttl_seconds=ttl,
            refresh=self._refresh,
            label=f"odds_api_{sport_key}",
            allow_stale_on_error=True,
        )
        self._last_meta = meta
        return body

    def _parse_quotes(self, payload: Any, name_to_id: dict[str, str]) -> list[MarketQuote]:
        events = payload if isinstance(payload, list) else []
        candidates = {normalize_name(n): pid for n, pid in name_to_id.items()}
        by_player: dict[str, list[float]] = {}
        as_of = datetime.now(timezone.utc)
        for ev in events:
            for book in ev.get("bookmakers") or []:
                for market in book.get("markets") or []:
                    if str(market.get("key") or "") not in ("outrights", "winner", "outright"):
                        continue
                    for oc in market.get("outcomes") or []:
                        nm = str(oc.get("name") or "").strip()
                        pid = match_name(nm, candidates)
                        if not pid:
                            continue
                        try:
                            dec = float(oc.get("price"))
                        except (TypeError, ValueError):
                            continue
                        by_player.setdefault(pid, []).append(dec)
        quotes = []
        for pid, prices in by_player.items():
            dec = sum(prices) / len(prices)
            quotes.append(
                MarketQuote(
                    player_id=pid,
                    bet_type=BetType.WIN,
                    decimal_odds=dec,
                    implied_raw=1.0 / dec if dec else None,
                    book="odds_api_consensus",
                    as_of=as_of,
                )
            )
        return quotes
