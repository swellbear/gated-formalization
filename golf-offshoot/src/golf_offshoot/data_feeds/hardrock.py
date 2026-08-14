"""Hard Rock Bet winner quotes. Never copied from Bovada. Never invented.

Hard Rock Bet has no Bovada-style public winner coupon that the CLI can ingest.
The labeled path is The Odds API with bookmakers pinned to Hard Rock keys
(us / us2). Unmatched names stay unmatched. Place/top markets stay unavailable
unless that coupon actually lists them.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.config import ODDS_TTL_LIVE_SECONDS, ODDS_TTL_PRE_SECONDS
from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.data_feeds.local_env import load_local_env
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.data_feeds.odds_api import ODDS_BASE, OddsApiFeed
from golf_offshoot.models.enums import BetType, DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality, MarketQuote

# The Odds API keys for Hard Rock Bet (national + state skins). Do not average them.
HARDROCK_BOOKMAKER_KEYS = (
    "hardrockbet",
    "hardrockbet_fl",
    "hardrockbet_az",
    "hardrockbet_oh",
)

_MISSING_KEY_NOTES = (
    "THE_ODDS_API_KEY not set. Hard Rock Bet has no public CLI winner coupon "
    "analogous to Bovada; Hard Rock prices stay unavailable and are not copied "
    "from Bovada or any other book."
)


def resolve_odds_book(raw: str | None = None) -> str:
    """Return auto | bovada | hardrockbet. Unknown values stay auto (Bovada path)."""
    text = (raw if raw is not None else os.environ.get("GOLF_ODDS_BOOK", "")).strip().lower()
    compact = text.replace("_", " ").replace("-", " ").replace(" ", "")
    if compact in {"hardrock", "hardrockbet", "hrb"}:
        return "hardrockbet"
    if compact == "bovada":
        return "bovada"
    return "auto"


def _tokens(name: str) -> set[str]:
    return {t for t in normalize_name(name).split() if len(t) > 2}


def _event_blob(event: dict[str, Any]) -> str:
    parts = [
        str(event.get("id") or ""),
        str(event.get("sport_key") or ""),
        str(event.get("sport_title") or ""),
        str(event.get("home_team") or ""),
        str(event.get("away_team") or ""),
        str(event.get("commence_time") or ""),
    ]
    return " ".join(parts)


def _preferred_bookmaker(bookmakers: list[dict[str, Any]]) -> dict[str, Any] | None:
    by_key = {str(b.get("key") or ""): b for b in bookmakers or []}
    for key in HARDROCK_BOOKMAKER_KEYS:
        if key in by_key:
            return by_key[key]
    return None


class HardRockBetOddsFeed(DataFeed[list[MarketQuote]]):
    """Pinned Hard Rock Bet outrights via The Odds API. Not a Bovada fallback."""

    name = "hardrockbet"
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
        tournament_name = str(kwargs.get("tournament_name") or "")
        self._live = bool(kwargs.get("live", False))
        self._ttl = kwargs.get("ttl_seconds")
        self._refresh = bool(kwargs.get("refresh", False))
        if not self.api_key:
            return [], unavailable_quality(self.name, _MISSING_KEY_NOTES)
        catalog = OddsApiFeed(cache=self.cache, api_key=self.api_key)
        catalog._live = self._live
        catalog._ttl = self._ttl
        catalog._refresh = self._refresh
        try:
            sports = catalog._sports()
        except FeedError as exc:
            return [], unavailable_quality(self.name, f"Hard Rock Odds API sports catalog failed: {exc}")
        golf = [
            s
            for s in sports
            if "golf" in str(s.get("key", "")).lower() or "golf" in str(s.get("group", "")).lower()
        ]
        if not golf:
            return [], unavailable_quality(self.name, "Odds API sports catalog has no golf keys right now")
        quotes: list[MarketQuote] = []
        used = None
        unmatched_total = 0
        book_used = ""
        for sport in golf:
            key = sport.get("key")
            if not key:
                continue
            try:
                payload = self._odds(str(key))
            except FeedError:
                continue
            used = key
            parsed, unmatched, book_used = self._parse_quotes(payload, name_to_id, tournament_name)
            unmatched_total += unmatched
            quotes.extend(parsed)
            if quotes:
                break
        if not quotes:
            return [], unavailable_quality(
                self.name,
                f"Hard Rock Bet returned no matchable golf outrights "
                f"(tried group size {len(golf)}; unmatched={unmatched_total}). "
                "Not filled from Bovada.",
            )
        meta = self._last_meta or {}
        age_s = float(meta.get("age_seconds") or 0.0)
        notes = (
            f"Hard Rock Bet winner decimals via The Odds API bookmakers="
            f"{','.join(HARDROCK_BOOKMAKER_KEYS)} pinned (not averaged, not Bovada); "
            f"book_key={book_used or 'hardrockbet'}; sport={used}; "
            f"unmatched names dropped; place/top never synthesized from winner; "
            f"opening unavailable unless a distinct prematch coupon was archived; "
            f"fetched_at={meta.get('fetched_at')}; cached={meta.get('cached')}; age_s={age_s:.0f}"
        )
        if meta.get("stale_fallback"):
            notes += "; STALE_FALLBACK"
        q = DataQuality(
            score=0.55 if meta.get("stale_fallback") else 0.74,
            role=self.role,
            source_name=f"{self.name}:{used}",
            as_of=datetime.now(timezone.utc),
            n_observations=len(quotes),
            lag_hours=age_s / 3600.0,
            notes=notes,
            source_kind=SourceKind.REAL_LIVE,
        )
        return quotes, q

    def _odds(self, sport_key: str) -> Any:
        keys = ",".join(HARDROCK_BOOKMAKER_KEYS)
        url = (
            f"{ODDS_BASE}/sports/{sport_key}/odds/?apiKey={self.api_key}"
            f"&regions=us2,us&markets=outrights&oddsFormat=decimal"
            f"&bookmakers={keys}"
        )
        ttl = float(self._ttl) if self._ttl is not None else (
            ODDS_TTL_LIVE_SECONDS if self._live else ODDS_TTL_PRE_SECONDS
        )
        body, meta = self.cache.get_json(
            url,
            headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
            ttl_seconds=ttl,
            refresh=self._refresh,
            label=f"hardrockbet_{sport_key}",
            allow_stale_on_error=True,
        )
        self._last_meta = meta
        return body

    def _parse_quotes(
        self,
        payload: Any,
        name_to_id: dict[str, str],
        tournament_name: str = "",
    ) -> tuple[list[MarketQuote], int, str]:
        events = payload if isinstance(payload, list) else []
        candidates = {normalize_name(n): pid for n, pid in name_to_id.items()}
        chosen = _pick_event(events, tournament_name, candidates)
        if chosen is None:
            return [], 0, ""
        book = _preferred_bookmaker(chosen.get("bookmakers") or [])
        if book is None:
            return [], 0, ""
        as_of = datetime.now(timezone.utc)
        quotes: list[MarketQuote] = []
        unmatched = 0
        for market in book.get("markets") or []:
            mkey = str(market.get("key") or "").lower()
            if mkey not in ("outrights", "winner", "outright"):
                continue
            for oc in market.get("outcomes") or []:
                nm = str(oc.get("name") or "").strip()
                pid = match_name(nm, candidates)
                if not pid:
                    unmatched += 1
                    continue
                try:
                    dec = float(oc.get("price"))
                except (TypeError, ValueError):
                    continue
                if dec <= 1.0:
                    continue
                quotes.append(
                    MarketQuote(
                        player_id=pid,
                        bet_type=BetType.WIN,
                        decimal_odds=dec,
                        implied_raw=1.0 / dec,
                        book="hardrockbet",
                        as_of=as_of,
                        line_role="current",
                    )
                )
        return quotes, unmatched, str(book.get("key") or "hardrockbet")


def _pick_event(
    events: list[dict[str, Any]],
    tournament_name: str,
    candidates: dict[str, str],
) -> dict[str, Any] | None:
    """Prefer title token overlap; else the card with the most matched field names."""
    want = _tokens(tournament_name)
    scored: list[tuple[int, int, dict[str, Any]]] = []
    for ev in events:
        blob = _event_blob(ev)
        title_hits = len(want & _tokens(blob)) if want else 0
        player_hits = 0
        for book in ev.get("bookmakers") or []:
            if str(book.get("key") or "") not in HARDROCK_BOOKMAKER_KEYS:
                continue
            for market in book.get("markets") or []:
                for oc in market.get("outcomes") or []:
                    if match_name(str(oc.get("name") or ""), candidates):
                        player_hits += 1
        if title_hits < 2 and player_hits < 8:
            continue
        scored.append((title_hits, player_hits, ev))
    if not scored:
        return None
    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    return scored[0][2]
