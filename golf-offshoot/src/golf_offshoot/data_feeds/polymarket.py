"""Polymarket golf outrights. Read-only. Never Bovada. Never CLOB orders."""

from __future__ import annotations

import json
import re
from typing import Any

from golf_offshoot.config import ODDS_TTL_LIVE_SECONDS, ODDS_TTL_PRE_SECONDS
from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.localtime import now
from golf_offshoot.models.enums import BetType, DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality, MarketQuote

US_GATEWAY = "https://gateway.polymarket.us"
POLYMARKET_PATH_ID = "polymarket"
_MAX_EVENTS = 12
_SKIP_TITLES = {"other", "field", "the field", "any other", "rest of field"}
_SKIP_QUESTION = (
    "2-ball",
    "2 ball",
    "3-ball",
    "3 ball",
    "matchup",
    "group betting",
    "head to head",
    "h2h",
)
_SLUG_MARKET_TAILS = (
    "winner",
    "first-round-leader",
    "second-round-leader",
    "third-round-leader",
)
_ROUND_LEADER_PATTERNS: tuple[tuple[BetType, tuple[str, ...]], ...] = (
    (
        BetType.WIN_AFTER_R1,
        (
            r"after\s+round\s*1\b",
            r"win\s+after\s+round\s*1\b",
            r"end of round\s*1\b",
            r"end of (?:the\s+)?(?:1st|first) round",
            r"-r1l(?:-|$)",
            r"following the (?:1st|first) round",
            r"(?:1st|first)[- ]round[- ]leader",
            r"(?:1st|first)\s+round\s+(?:leader|winner|win)",
            r"round\s*1\s+(?:leader|winner)",
            r"18[\s-]*hole\s+leader",
            r"leader\s+after\s+(?:the\s+)?(?:1st|first)\s+round",
        ),
    ),
    (
        BetType.WIN_AFTER_R2,
        (
            r"after\s+round\s*2\b",
            r"win\s+after\s+round\s*2\b",
            r"end of round\s*2\b",
            r"end of (?:the\s+)?(?:2nd|second) round",
            r"-r2l(?:-|$)",
            r"following the (?:2nd|second) round",
            r"(?:2nd|second)[- ]round[- ]leader",
            r"(?:2nd|second)\s+round\s+(?:leader|winner|win)",
            r"round\s*2\s+(?:leader|winner)",
            r"36[\s-]*hole\s+leader",
            r"leader\s+after\s+(?:the\s+)?(?:2nd|second)\s+round",
        ),
    ),
    (
        BetType.WIN_AFTER_R3,
        (
            r"after\s+round\s*3\b",
            r"win\s+after\s+round\s*3\b",
            r"end of round\s*3\b",
            r"end of (?:the\s+)?(?:3rd|third) round",
            r"-r3l(?:-|$)",
            r"following the (?:3rd|third) round",
            r"(?:3rd|third)[- ]round[- ]leader",
            r"(?:3rd|third)\s+round\s+(?:leader|winner|win)",
            r"round\s*3\s+(?:leader|winner)",
            r"54[\s-]*hole\s+leader",
            r"leader\s+after\s+(?:the\s+)?(?:3rd|third)\s+round",
        ),
    ),
)


def slug_candidates(tournament_name: str, *, year: int | None = None) -> list[str]:
    slug = re.sub(r"[^a-z0-9]+", "-", normalize_name(tournament_name)).strip("-")
    if not slug:
        return []
    yr = int(year if year is not None else now().year)
    out: list[str] = []
    for tail in _SLUG_MARKET_TAILS:
        for item in (f"{yr}-{slug}-{tail}", f"{slug}-{tail}"):
            if item not in out:
                out.append(item)
    for item in (f"{yr}-{slug}", slug):
        if item not in out:
            out.append(item)
    return out


def _round_leader_bet(text: str) -> BetType | None:
    low = str(text or "").lower()
    if not low:
        return None
    for bet, patterns in _ROUND_LEADER_PATTERNS:
        if any(re.search(pat, low) for pat in patterns):
            return bet
    return None


def _finish_or_round(text: str) -> BetType | None:
    low = str(text or "").lower()
    if not low:
        return None
    round_bet = _round_leader_bet(low)
    if round_bet is not None:
        return round_bet
    if re.search(r"top[\s-]*20\b|top twenty|\btop20\b", low):
        return BetType.TOP_20
    if re.search(r"top[\s-]*10\b|top ten|\btop10\b", low):
        return BetType.TOP_10
    if re.search(r"top[\s-]*5\b|top five|\btop5\b", low):
        return BetType.TOP_5
    if "make the cut" in low or "make cut" in low:
        return BetType.MAKE_CUT
    return None


def classify_market(question: str, *, sports_type: str = "", context: str = "") -> BetType | None:
    """Map a Polymarket question to a bet type. Never synthesizes missing markets."""
    q = str(question or "").lower().strip()
    ctx = str(context or "").lower().strip()
    blob = f"{q} {ctx}".strip()
    if not blob:
        return None
    if any(s in q for s in _SKIP_QUESTION) or any(s in ctx for s in _SKIP_QUESTION):
        return None
    hit = _finish_or_round(q)
    if hit is not None:
        return hit
    question_names_market = bool(re.search(r"\b(win|lead|finish|top|cut)\b", q))
    if not question_names_market:
        hit = _finish_or_round(ctx)
        if hit is not None:
            return hit
    if "win" in q or str(sports_type or "").lower() == "moneyline":
        return BetType.WIN
    if "winner" in ctx:
        return BetType.WIN
    return None


def _player_label(market: dict[str, Any]) -> str:
    return str(
        market.get("groupItemTitle")
        or market.get("title")
        or market.get("titleShort")
        or ""
    ).strip()


def event_is_live_for_tournament(
    event: dict[str, Any],
    tournament_name: str,
    *,
    year: int | None = None,
) -> bool:
    """Current-year open Polymarket US golf card for this tournament."""
    if not event or event.get("closed"):
        return False
    yr = int(year if year is not None else now().year)
    slug = str(event.get("slug") or "")
    title = str(event.get("title") or "")
    end = str(event.get("endDate") or event.get("end_date") or "")
    start = str(event.get("startDate") or event.get("startTime") or "")
    if _title_hits(title or slug, tournament_name) < 2:
        return False
    if _foreign_tour(f"{title} {slug}", tournament_name):
        return False
    if (
        str(yr) not in slug
        and str(yr) not in title
        and str(yr) not in end
        and str(yr) not in start
    ):
        return False
    return event_has_mapped_market(event)


def _market_tradable(market: dict[str, Any]) -> bool:
    if market.get("closed") or market.get("archived") or market.get("hidden"):
        return False
    status = str(market.get("status") or "")
    if status and status not in {"MARKET_STATUS_OPEN", "open"}:
        return False
    if market.get("enableOrderBook") is False:
        return False
    if market.get("acceptingOrders") is False:
        return False
    return yes_price(market, tradable_only=True) is not None


def event_has_mapped_market(event: dict[str, Any]) -> bool:
    """True when at least one open contract maps to a known bet type."""
    context = f"{event.get('title') or ''} {event.get('slug') or ''}"
    for market in event.get("markets") or []:
        if not isinstance(market, dict):
            continue
        if market.get("closed") or market.get("archived"):
            continue
        if market.get("enableOrderBook") is False or market.get("acceptingOrders") is False:
            continue
        title = _player_label(market)
        if normalize_name(title) in _SKIP_TITLES or bool(market.get("negRiskOther")):
            continue
        bet = classify_market(
            str(market.get("question") or ""),
            sports_type=str(market.get("sportsMarketType") or ""),
            context=context,
        )
        if bet is not None:
            return True
    return False


def yes_price(market: dict[str, Any], *, tradable_only: bool = False) -> float | None:
    """Posted Yes ask if tradable. Displayed outcomePrices are not a ticket."""
    p = _quote_unit(market.get("bestAskQuote"))
    if p is None:
        p = _unit_price(market.get("bestAsk"))
    if p is None:
        p = _yes_side_quote(market)
    if p is not None:
        return p
    if tradable_only:
        return None
    prices = market.get("outcomePrices")
    if isinstance(prices, str):
        try:
            prices = json.loads(prices)
        except json.JSONDecodeError:
            prices = None
    if isinstance(prices, list) and prices:
        return _unit_price(prices[0])
    return None


def yes_bid(market: dict[str, Any]) -> float | None:
    """Yes bestBid if tradable. Sell side. Never synthesized from the ask."""
    p = _quote_unit(market.get("bestBidQuote"))
    if p is not None:
        return p
    p = _unit_price(market.get("bestBid"))
    if p is not None:
        return p
    return _yes_side_price(market)


def quotes_from_event(
    event: dict[str, Any],
    name_to_id: dict[str, str],
) -> tuple[list[MarketQuote], int, list[str]]:
    """One event's tradable Yes contracts. 'Other' is not a player."""
    candidates = {normalize_name(n): pid for n, pid in name_to_id.items()}
    for n, pid in list(name_to_id.items()):
        candidates.setdefault(normalize_name(n), pid)
    quotes: list[MarketQuote] = []
    unmatched = 0
    seen_markets: list[str] = []
    as_of = now()
    context = f"{event.get('title') or ''} {event.get('slug') or ''}"
    if event.get("closed"):
        return [], 0, []
    for market in event.get("markets") or []:
        if not isinstance(market, dict):
            continue
        if not _market_tradable(market):
            continue
        title = _player_label(market)
        question = str(market.get("question") or "")
        if normalize_name(title) in _SKIP_TITLES or bool(market.get("negRiskOther")):
            unmatched += 1
            continue
        bet = classify_market(
            question,
            sports_type=str(market.get("sportsMarketType") or ""),
            context=context,
        )
        if bet is None:
            continue
        pid = match_name(title or question, candidates)
        if not pid:
            unmatched += 1
            continue
        price = yes_price(market, tradable_only=True)
        if price is None:
            continue
        card = str(event.get("slug") or event.get("title") or bet.value).strip()
        if card and card not in seen_markets:
            seen_markets.append(card)
        quotes.append(
            MarketQuote(
                player_id=pid,
                bet_type=bet,
                decimal_odds=1.0 / price,
                implied_raw=price,
                bid_raw=yes_bid(market),
                book="polymarket",
                as_of=as_of,
                line_role="current",
            )
        )
    return quotes, unmatched, seen_markets


def winner_outcome_names(events: list[dict[str, Any]]) -> list[str]:
    """Winner-contract names. 'Other' is not a player."""
    names: list[str] = []
    seen: set[str] = set()
    for event in events:
        for market in event.get("markets") or []:
            if not isinstance(market, dict):
                continue
            if market.get("closed") or market.get("archived"):
                continue
            title = _player_label(market)
            question = str(market.get("question") or "")
            if normalize_name(title) in _SKIP_TITLES or bool(market.get("negRiskOther")):
                continue
            bet = classify_market(
                question,
                sports_type=str(market.get("sportsMarketType") or ""),
                context=f"{event.get('title') or ''} {event.get('slug') or ''}",
            )
            if bet != BetType.WIN:
                continue
            nm = title or question
            key = normalize_name(nm)
            if not key or key in seen:
                continue
            seen.add(key)
            names.append(nm)
    return names


class PolymarketOddsFeed(DataFeed[list[MarketQuote]]):
    """Pinned Polymarket US golf futures via gateway.polymarket.us. Not Gamma international. No orders."""

    name = "polymarket"
    role = DataRole.PRIMARY

    def __init__(self, cache: HttpCache | None = None, refresh: bool = False) -> None:
        self.cache = cache or HttpCache()
        self.refresh = refresh
        self._last_meta: dict[str, Any] = {}

    def fetch(self, **kwargs: Any) -> tuple[list[MarketQuote], DataQuality]:
        name_to_id: dict[str, str] = kwargs.get("name_to_id") or {}
        tournament_name = str(kwargs.get("tournament_name") or "")
        live = bool(kwargs.get("live", False))
        ttl = kwargs.get("ttl_seconds")
        if ttl is None:
            ttl = ODDS_TTL_LIVE_SECONDS if live else ODDS_TTL_PRE_SECONDS
        refresh = bool(kwargs.get("refresh", self.refresh))
        events = self._discover_events(
            tournament_name,
            ttl_seconds=float(ttl),
            refresh=refresh,
        )
        if not events:
            q = unavailable_quality(
                self.name,
                f"no Polymarket US golf futures matching {tournament_name!r} "
                "(not filled from Gamma international or Bovada)",
            )
            return [], q
        quotes: list[MarketQuote] = []
        unmatched = 0
        markets_seen: list[str] = []
        by_player_bet: dict[tuple[str, BetType], MarketQuote] = {}
        for event in events:
            qs, um, mk = quotes_from_event(event, name_to_id)
            unmatched += um
            for label in mk:
                if label not in markets_seen:
                    markets_seen.append(label)
            for q in qs:
                by_player_bet[(q.player_id, q.bet_type)] = q
        quotes = list(by_player_bet.values())
        meta = self._last_meta or {}
        age_s = float(meta.get("age_seconds") or 0.0)
        titles = ", ".join(str(ev.get("title") or ev.get("slug") or "") for ev in events)
        slugs = ",".join(markets_seen)
        if not quotes:
            q = unavailable_quality(
                self.name,
                f"Polymarket US {titles} had no matchable Yes prices "
                f"(unmatched={unmatched}; not filled from Gamma international or Bovada)",
            )
            q.lag_hours = age_s / 3600.0
            return [], q
        by_type: dict[BetType, int] = {}
        for q in quotes:
            by_type[q.bet_type] = by_type.get(q.bet_type, 0) + 1
        notes = (
            f"Polymarket US {titles}; winner matched {by_type.get(BetType.WIN, 0)}/{len(name_to_id)}; "
            f"unmatched names {unmatched}; us_slugs={slugs}; events={len(events)}; "
            f"top10={'yes' if by_type.get(BetType.TOP_10) else 'unavailable on this card'}; "
            f"top5={'yes' if by_type.get(BetType.TOP_5) else 'unavailable'}; "
            f"top20={'yes' if by_type.get(BetType.TOP_20) else 'unavailable'}; "
            f"make_cut={'yes' if by_type.get(BetType.MAKE_CUT) else 'unavailable'}; "
            f"win_after_r1={'yes' if by_type.get(BetType.WIN_AFTER_R1) else 'unavailable'}; "
            f"win_after_r2={'yes' if by_type.get(BetType.WIN_AFTER_R2) else 'unavailable'}; "
            f"win_after_r3={'yes' if by_type.get(BetType.WIN_AFTER_R3) else 'unavailable'}; "
            f"read-only Polymarket US golf futures; not gamma-api.polymarket.com; no CLOB orders; Bovada not used; "
            f"bid={'yes' if any(q.bid_raw for q in quotes) else 'unavailable'}; "
            f"fetched_at={meta.get('fetched_at')}; cached={meta.get('cached')}; age_s={age_s:.0f}"
        )
        if meta.get("stale_fallback"):
            notes += "; STALE_FALLBACK"
        q = DataQuality(
            score=0.55 if meta.get("stale_fallback") else 0.74,
            role=self.role,
            source_name=self.name,
            as_of=now(),
            n_observations=len(quotes),
            lag_hours=age_s / 3600.0,
            notes=notes,
            source_kind=SourceKind.REAL_LIVE,
        )
        return quotes, q

    def list_winner_names(self, tournament_name: str, *, refresh: bool = False) -> list[str]:
        events = self._discover_events(
            tournament_name,
            ttl_seconds=float(ODDS_TTL_PRE_SECONDS),
            refresh=refresh,
        )
        return winner_outcome_names(events)

    def _discover_events(
        self,
        tournament_name: str,
        *,
        ttl_seconds: float,
        refresh: bool,
    ) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        seen: set[str] = set()
        for ev in self._golf_futures_events(ttl_seconds=ttl_seconds, refresh=refresh):
            if ev is None or len(found) >= _MAX_EVENTS:
                break
            key = str(ev.get("id") or ev.get("slug") or "").strip()
            if not key or key in seen:
                continue
            title = str(ev.get("title") or ev.get("slug") or "")
            blob = f"{title} {ev.get('slug') or ''}"
            if _title_hits(title or blob, tournament_name) < 2:
                continue
            if _international_place_card(blob):
                continue
            if not event_is_live_for_tournament(ev, tournament_name):
                continue
            seen.add(key)
            found.append(ev)
        return found

    def _golf_futures_events(
        self,
        *,
        ttl_seconds: float,
        refresh: bool,
    ) -> list[dict[str, Any]]:
        url = f"{US_GATEWAY}/v2/sports/golf/events?type=futures&limit=50"
        body = self._get(
            url,
            label="polymarket_us_golf_futures",
            ttl_seconds=ttl_seconds,
            refresh=refresh,
        )
        if isinstance(body, dict):
            rows = body.get("events") or []
            return [row for row in rows if isinstance(row, dict)]
        if isinstance(body, list):
            return [row for row in body if isinstance(row, dict)]
        return []

    def _get(
        self,
        url: str,
        *,
        label: str,
        ttl_seconds: float,
        refresh: bool,
    ) -> Any:
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


def _unit_price(raw: Any) -> float | None:
    try:
        p = float(raw)
    except (TypeError, ValueError):
        return None
    if p <= 0.0 or p >= 1.0:
        return None
    return p


def _quote_unit(raw: Any) -> float | None:
    if isinstance(raw, dict):
        return _unit_price(raw.get("value"))
    return _unit_price(raw)


def _yes_side(market: dict[str, Any]) -> dict[str, Any] | None:
    for side in market.get("marketSides") or []:
        if not isinstance(side, dict):
            continue
        if side.get("long") is True or str(side.get("description") or "").lower() == "yes":
            return side
    return None


def _yes_side_quote(market: dict[str, Any]) -> float | None:
    side = _yes_side(market)
    if side is None:
        return None
    return _quote_unit(side.get("quote"))


def _yes_side_price(market: dict[str, Any]) -> float | None:
    side = _yes_side(market)
    if side is None:
        return None
    return _unit_price(side.get("price"))


def _tokens(name: str) -> set[str]:
    return {t for t in normalize_name(name).split() if len(t) > 2}


def _title_hits(blob: str, tournament_name: str) -> int:
    want = _tokens(tournament_name)
    if not want:
        return 0
    return len(want & _tokens(blob))


def _international_place_card(blob: str) -> bool:
    """Gamma-international Top 5/10/20. Not listed on Polymarket US golf futures."""
    low = str(blob or "").lower()
    return bool(re.search(r"top[\s-]*(?:5|10|20)\b|\btop(?:5|10|20)\b", low))


def _foreign_tour(blob: str, tournament_name: str) -> bool:
    t = (tournament_name or "").lower()
    low = blob.lower()
    if "champions" in low and "champions" not in t:
        return True
    if "lpga" in low and "lpga" not in t:
        return True
    if ("liv-" in low or " liv " in f" {low} ") and "liv" not in t:
        return True
    if "dpwt" in low and "dp world" not in t and "european" not in t:
        return True
    if "korn ferry" in low and "korn" not in t:
        return True
    return False
