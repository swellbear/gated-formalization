"""Bovada public golf coupon JSON. Real live outrights; never invents prices."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.config import ODDS_TTL_LIVE_SECONDS, ODDS_TTL_PRE_SECONDS
from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_BROWSER_UA, HttpCache
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.models.enums import BetType, DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality, MarketQuote

BOVADA_GOLF = "https://www.bovada.lv/services/sports/event/coupon/events/A/description/golf?lang=en"
BOVADA_PGA = (
    "https://www.bovada.lv/services/sports/event/coupon/events/A/description/golf/pga-tour?lang=en"
)
BOVADA_GOLF_PREMATCH = BOVADA_GOLF + "&preMatchOnly=true"
BOVADA_GOLF_LIVE = BOVADA_GOLF + "&liveOnly=true"

_WINNER_LABELS = {"winner", "winner live", "outright", "outright winner", "tournament winner"}
_SKIP = (
    "1st round",
    "first round",
    "2-ball",
    "2 ball",
    "3-ball",
    "3 ball",
    "leader",
    "matchup",
    "group betting",
)


def classify_market(label: str) -> BetType | None:
    """Map a coupon market label to a bet type. Never synthesizes missing markets."""
    low = str(label or "").lower().strip()
    if not low:
        return None
    if any(s in low for s in _SKIP):
        return None
    if low in _WINNER_LABELS or low.startswith("winner"):
        return BetType.WIN
    if "top 10" in low or "top ten" in low:
        return BetType.TOP_10
    if "top 5" in low or "top five" in low:
        return BetType.TOP_5
    if "top 20" in low or "top twenty" in low:
        return BetType.TOP_20
    if "make the cut" in low or low in {"make cut", "to make cut", "will make the cut"}:
        return BetType.MAKE_CUT
    return None


def book_tag_for_label(label: str) -> str:
    """Prematch vs in-play coupon. Does not invent a missing opening line."""
    if "live" in str(label or "").lower():
        return "bovada_live"
    return "bovada"


def _as_of_ms(raw: Any) -> datetime:
    try:
        ms = int(raw)
        if ms > 10_000_000_000:
            return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
        return datetime.fromtimestamp(ms, tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return datetime.now(timezone.utc)


def _tokens(name: str) -> set[str]:
    return {t for t in normalize_name(name).split() if len(t) > 2}


class BovadaOddsFeed(DataFeed[list[MarketQuote]]):
    name = "bovada"
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
        payload = self._coupon(
            tournament_name,
            ttl_seconds=float(ttl),
            refresh=refresh,
            allow_stale_on_error=True,
        )
        events = self._matching_events(payload, tournament_name)
        if not events:
            q = unavailable_quality(self.name, f"no Bovada golf event matching {tournament_name!r}")
            return [], q
        norm_to_id = {normalize_name(n): pid for n, pid in name_to_id.items()}
        for n, pid in list(name_to_id.items()):
            norm_to_id.setdefault(normalize_name(n), pid)
        quotes, unmatched, markets_seen = self._quotes_from_events(events, norm_to_id, live=live)
        as_of = max((_as_of_ms(ev.get("lastModified")) for ev in events), default=datetime.now(timezone.utc))
        meta = self._last_meta or {}
        age_s = float(meta.get("age_seconds") or 0.0)
        stale = bool(meta.get("stale_fallback"))
        if not quotes:
            q = unavailable_quality(
                self.name,
                f"Bovada event(s) {[ev.get('description') for ev in events]} had no matchable prices "
                f"(unmatched={unmatched})",
            )
            q.as_of = as_of
            q.lag_hours = age_s / 3600.0
            return [], q
        by_type = _count_by_type(quotes)
        event_names = ", ".join(str(ev.get("description") or "") for ev in events)
        opening_n = sum(1 for q in quotes if q.line_role == "opening")
        notes = (
            f"Bovada {event_names} lastModified={as_of.isoformat()}; "
            f"winner matched {by_type.get(BetType.WIN, 0)}/{len(name_to_id)}; "
            f"unmatched names {unmatched}; markets={markets_seen}; "
            f"top10={'yes' if by_type.get(BetType.TOP_10) else 'unavailable on this coupon'}; "
            f"top5={'yes' if by_type.get(BetType.TOP_5) else 'unavailable'}; "
            f"top20={'yes' if by_type.get(BetType.TOP_20) else 'unavailable'}; "
            f"make_cut={'yes' if by_type.get(BetType.MAKE_CUT) else 'unavailable'}; "
            f"opening={'yes' if opening_n else 'unavailable (no distinct prematch coupon)'}; "
            f"urls={meta.get('urls_used', [])}; "
            f"fetched_at={meta.get('fetched_at')}; cached={meta.get('cached')}; "
            f"age_s={age_s:.0f}; ttl_s={ttl:.0f}"
        )
        if stale:
            notes += f"; STALE_FALLBACK error={meta.get('error', '')}"
        score = 0.78
        if stale:
            score = min(score, 0.55)
        q = DataQuality(
            score=score,
            role=self.role,
            source_name=self.name,
            as_of=as_of,
            n_observations=len(quotes),
            lag_hours=age_s / 3600.0,
            notes=notes,
            source_kind=SourceKind.REAL_LIVE,
        )
        return quotes, q

    def _coupon(
        self,
        tournament_name: str = "",
        *,
        ttl_seconds: float = ODDS_TTL_PRE_SECONDS,
        refresh: bool = False,
        allow_stale_on_error: bool = False,
    ) -> list[dict[str, Any]]:
        headers = {"User-Agent": DEFAULT_BROWSER_UA, "Accept": "application/json"}
        slug = re.sub(r"[^a-z0-9]+", "-", normalize_name(tournament_name)).strip("-")
        urls: list[tuple[str, str]] = []
        if slug:
            urls.append(
                (
                    f"https://www.bovada.lv/services/sports/event/coupon/events/A/description/golf/pga-tour/{slug}-finishes?lang=en",
                    f"bovada_slug_finishes_{slug}",
                )
            )
            urls.append(
                (
                    f"https://www.bovada.lv/services/sports/event/coupon/events/A/description/golf/{slug}-finishes?lang=en",
                    f"bovada_golf_finishes_{slug}",
                )
            )
            urls.append(
                (
                    f"https://www.bovada.lv/services/sports/event/coupon/events/A/description/golf/pga-tour/{slug}?lang=en",
                    f"bovada_slug_{slug}",
                )
            )
        urls.append((BOVADA_GOLF_PREMATCH, "bovada_golf_prematch"))
        urls.append((BOVADA_GOLF_LIVE, "bovada_golf_live"))
        urls.append((BOVADA_PGA, "bovada_pga_coupon"))
        urls.append((BOVADA_GOLF, "bovada_golf_coupon"))
        merged: list[dict[str, Any]] = []
        urls_used: list[str] = []
        last_meta: dict[str, Any] = {}
        for url, label in urls:
            try:
                body, meta = self.cache.get_json(
                    url,
                    headers=headers,
                    ttl_seconds=ttl_seconds,
                    refresh=refresh,
                    label=label,
                    allow_stale_on_error=allow_stale_on_error,
                )
            except FeedError:
                continue
            last_meta = meta
            if isinstance(body, list) and body:
                merged.extend(body)
                urls_used.append(label)
        last_meta = dict(last_meta)
        last_meta["urls_used"] = urls_used
        self._last_meta = last_meta
        return merged

    def _matching_events(
        self, groups: list[dict[str, Any]], tournament_name: str
    ) -> list[dict[str, Any]]:
        want = _tokens(tournament_name) or {"st", "jude"}
        scored: list[tuple[int, dict[str, Any]]] = []
        seen: set[str] = set()
        for g in groups or []:
            path = " ".join(str(p.get("description") or "") for p in g.get("path") or [])
            for ev in g.get("events") or []:
                blob = f"{path} {ev.get('description') or ''}"
                low = blob.lower()
                if _foreign_tour(low, tournament_name):
                    continue
                if any(s in low for s in ("2-ball", "2 ball", "3-ball", "3 ball", "1st round", "first round")):
                    continue
                have = _tokens(blob)
                score = len(want & have)
                if score < 2:
                    continue
                eid = str(ev.get("id") or ev.get("description") or id(ev))
                if eid in seen:
                    continue
                seen.add(eid)
                scored.append((score, ev))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [ev for _, ev in scored]

    def _pick_event(self, groups: list[dict[str, Any]], tournament_name: str) -> dict[str, Any] | None:
        events = self._matching_events(groups, tournament_name)
        return events[0] if events else None

    def _quotes_from_events(
        self, events: list[dict[str, Any]], norm_to_id: dict[str, str], *, live: bool = False
    ) -> tuple[list[MarketQuote], int, list[str]]:
        live_q: dict[tuple[str, BetType], MarketQuote] = {}
        pre_q: dict[tuple[str, BetType], MarketQuote] = {}
        unmatched = 0
        markets_seen: list[str] = []
        for event in events:
            qs, um, mk = self._quotes_from_event(event, norm_to_id)
            unmatched += um
            for label in mk:
                if label not in markets_seen:
                    markets_seen.append(label)
            ev_as_of = _as_of_ms(event.get("lastModified"))
            for q in qs:
                key = (q.player_id, q.bet_type)
                dest = live_q if q.book == "bovada_live" else pre_q
                prev = dest.get(key)
                if prev is None or ev_as_of >= (prev.as_of or datetime.min.replace(tzinfo=timezone.utc)):
                    dest[key] = q
        out: list[MarketQuote] = []
        keys = set(live_q) | set(pre_q)
        for key in keys:
            live_quote = live_q.get(key)
            pre_quote = pre_q.get(key)
            if live:
                if live_quote is not None:
                    out.append(live_quote)
                    if pre_quote is not None:
                        out.append(pre_quote.model_copy(update={"line_role": "opening"}))
                elif pre_quote is not None:
                    out.append(pre_quote)
            else:
                if pre_quote is not None:
                    out.append(pre_quote)
                elif live_quote is not None:
                    out.append(live_quote)
        return out, unmatched, markets_seen

    def _quotes_from_event(
        self, event: dict[str, Any], norm_to_id: dict[str, str]
    ) -> tuple[list[MarketQuote], int, list[str]]:
        quotes: list[MarketQuote] = []
        unmatched = 0
        markets_seen: list[str] = []
        as_of = _as_of_ms(event.get("lastModified"))
        for dg in event.get("displayGroups") or []:
            for mkt in dg.get("markets") or []:
                label = str(mkt.get("description") or "")
                bet = classify_market(label)
                if bet is None:
                    continue
                markets_seen.append(label)
                for oc in mkt.get("outcomes") or []:
                    nm = str(oc.get("description") or "").strip()
                    pid = match_name(nm, norm_to_id)
                    if not pid:
                        unmatched += 1
                        continue
                    price = oc.get("price") or {}
                    dec = price.get("decimal")
                    try:
                        dec_f = float(dec)
                    except (TypeError, ValueError):
                        continue
                    if dec_f <= 1.0:
                        continue
                    quotes.append(
                        MarketQuote(
                            player_id=pid,
                            bet_type=bet,
                            decimal_odds=dec_f,
                            implied_raw=1.0 / dec_f,
                            book=book_tag_for_label(label),
                            as_of=as_of,
                            line_role="current",
                        )
                    )
        return quotes, unmatched, markets_seen


def _foreign_tour(blob: str, tournament_name: str) -> bool:
    """Do not attach Champions/LPGA/Korn Ferry cards to a PGA event."""
    t = (tournament_name or "").lower()
    if "champions" in blob and "champions" not in t:
        return True
    if "lpga" in blob and "lpga" not in t:
        return True
    if "korn ferry" in blob and "korn ferry" not in t:
        return True
    return False


def _count_by_type(quotes: list[MarketQuote]) -> dict[BetType, int]:
    out: dict[BetType, int] = {}
    for q in quotes:
        if q.line_role == "opening":
            continue
        out[q.bet_type] = out.get(q.bet_type, 0) + 1
    return out
