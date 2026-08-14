"""ESPN public golf connectors (real live / real historical).

Uses the site.web and sports.core APIs. site.api.espn.com currently 403s
without extra cookies; we do not scrape HTML and we do not fabricate fields.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_BROWSER_UA, HttpCache
from golf_offshoot.models.enums import CourseType, DataRole, SourceKind
from golf_offshoot.models.schemas import Course, DataQuality, Player, Tournament

ESPN_WEB = "https://site.web.api.espn.com"
ESPN_CORE = "https://sports.core.api.espn.com"
ESPN_WEB_COMMON = "https://site.web.api.espn.com/apis/common/v3"


def _espn_headers() -> dict[str, str]:
    return {
        "User-Agent": DEFAULT_BROWSER_UA,
        "Accept": "application/json",
        "Referer": "https://www.espn.com/golf/",
        "Accept-Language": "en-US,en;q=0.9",
    }


def _event_id_from_ref(ref: str) -> str:
    m = re.search(r"/events/(\d+)", ref)
    if not m:
        raise FeedError(f"cannot parse event id from {ref}")
    return m.group(1)


def _iso_date(value: str | None) -> str:
    if not value:
        return ""
    return value[:10]


def _now_q(
    score: float,
    source: str,
    n: int,
    *,
    kind: SourceKind,
    notes: str = "",
    missing: bool = False,
    lag_hours: float = 0.0,
) -> DataQuality:
    return DataQuality(
        score=score,
        role=DataRole.PRIMARY,
        source_name=source,
        as_of=datetime.now(timezone.utc),
        n_observations=n,
        lag_hours=lag_hours,
        notes=notes,
        missing=missing,
        source_kind=kind,
    )


def classify_course_type(name: str, city: str, state: str, coastal: bool) -> tuple[CourseType, str]:
    blob = f"{name} {city} {state}".lower()
    if any(k in blob for k in ("links", "troon", "st andrews", "royal")):
        return CourseType.LINKS, "name heuristic"
    if any(k in blob for k in ("desert", "scottsdale", "tucson", "phoenix", "palm")):
        return CourseType.DESERT, "location heuristic"
    if "mountain" in blob:
        return CourseType.MOUNTAIN, "name heuristic"
    if coastal and any(k in blob for k in ("beach", "ocean", "harbour", "harbor", "pebble")):
        return CourseType.LINKS, "coastal name heuristic"
    return CourseType.PARKLAND, "default inland parkland heuristic"


class EspnClient:
    def __init__(self, cache: HttpCache | None = None, refresh: bool = False) -> None:
        self.cache = cache or HttpCache()
        self.refresh = refresh

    def get(self, url: str, *, ttl: float | None, label: str) -> Any:
        body, _meta = self.cache.get_json(
            url,
            headers=_espn_headers(),
            ttl_seconds=ttl,
            refresh=self.refresh,
            label=label,
        )
        return body

    def current_leaderboard(self) -> dict[str, Any]:
        url = f"{ESPN_WEB}/apis/site/v2/sports/golf/leaderboard?league=pga"
        return self.get(url, ttl=600, label="espn_current_leaderboard")

    def event_leaderboard(self, event_id: str, *, live: bool = False) -> dict[str, Any]:
        url = f"{ESPN_WEB}/apis/site/v2/sports/golf/leaderboard?event={event_id}"
        ttl = 600.0 if live else None
        return self.get(url, ttl=ttl, label=f"espn_event_{event_id}")

    def season_event_ids(self, year: int, season_type: int = 2) -> list[str]:
        url = (
            f"{ESPN_CORE}/v2/sports/golf/leagues/pga/seasons/{year}"
            f"/types/{season_type}/events?limit=200"
        )
        payload = self.get(url, ttl=None, label=f"espn_season_{year}_{season_type}")
        ids = []
        for item in payload.get("items") or []:
            ref = item.get("$ref") if isinstance(item, dict) else None
            if ref:
                ids.append(_event_id_from_ref(ref.replace("http://", "https://")))
        return ids

    def athlete_overview(self, athlete_id: str) -> dict[str, Any]:
        url = f"{ESPN_WEB_COMMON}/sports/golf/athletes/{athlete_id}/overview"
        return self.get(url, ttl=3600, label=f"espn_athlete_{athlete_id}")


def parse_event_payload(payload: dict[str, Any]) -> dict[str, Any]:
    events = payload.get("events") or []
    if not events:
        raise FeedError("ESPN leaderboard returned no events")
    return events[0]


def parse_course(event: dict[str, Any]) -> tuple[Course, DataQuality]:
    courses = event.get("courses") or []
    raw = courses[0] if courses else {}
    addr = raw.get("address") or {}
    name = raw.get("name") or "Unknown course"
    city = addr.get("city") or ""
    state = addr.get("state") or ""
    coastal = False
    ctype, why = classify_course_type(name, city, state, coastal)
    yards = int(raw.get("totalYards") or 7200)
    par = int(raw.get("shotsToPar") or 72)
    course = Course(
        course_id=str(raw.get("id") or name.lower().replace(" ", "-")),
        name=name,
        course_type=ctype,
        par=par,
        yardage=yards,
        coastal=coastal,
        altitude_m=0.0,
        firmness=0.5,
        rough_severity=0.5,
        green_speed=0.5,
        tightness=0.5,
        wind_exposure=0.5,
        grass="unknown",
        venue_cluster_id=None,
    )
    q = _now_q(
        0.85,
        "espn_event_courses",
        1,
        kind=SourceKind.REAL_LIVE if (event.get("status") or {}).get("type", {}).get("state") != "post" else SourceKind.REAL_HISTORICAL,
        notes=f"yards/par/name from ESPN; course_type {ctype.value} is {why}; "
        "firmness/rough/green_speed/tightness unavailable (defaults not used as evidence)",
    )
    return course, q


def parse_tournament(event: dict[str, Any], course: Course) -> Tournament:
    tmeta = event.get("tournament") or {}
    cut_round = int(tmeta.get("cutRound") or 0)
    has_cut = cut_round > 0
    cut_count = int(tmeta.get("cutCount") or 0)
    n_rounds = int(tmeta.get("numberOfRounds") or event.get("tournament", {}).get("numberOfRounds") or 4)
    purse = event.get("purse")
    start = _iso_date(event.get("date"))
    return Tournament(
        tournament_id=str(event.get("id")),
        name=str(event.get("name") or event.get("shortName") or "PGA event"),
        course=course,
        start_date=start,
        tour="PGA",
        n_rounds=n_rounds or 4,
        cut_place=cut_count if has_cut and cut_count else 65,
        cut_after_round=cut_round if has_cut else 0,
        has_cut=has_cut,
        is_major=bool(tmeta.get("major")),
        purse_usd=float(purse) if purse else None,
        espn_event_id=str(event.get("id")),
    )


def _status_name(comp: dict[str, Any]) -> str:
    return str(((comp.get("status") or {}).get("type") or {}).get("name") or "")


def _finish_place(comp: dict[str, Any]) -> int | None:
    pos = (comp.get("status") or {}).get("position") or {}
    raw = pos.get("id") or pos.get("displayName")
    if raw in (None, "", "-"):
        return None
    try:
        return int(str(raw).lstrip("T"))
    except ValueError:
        return None


def _place_display(comp: dict[str, Any]) -> str:
    pos = (comp.get("status") or {}).get("position") or {}
    raw = pos.get("displayName") or pos.get("id")
    if raw in (None, "", "-"):
        return ""
    return str(raw)


def _score_to_par(comp: dict[str, Any]) -> float | None:
    for st in comp.get("statistics") or []:
        if st.get("name") == "scoreToPar":
            try:
                return float(st.get("value"))
            except (TypeError, ValueError):
                return None
    score = comp.get("score") or {}
    try:
        return float(score.get("value"))
    except (TypeError, ValueError):
        return None


def _thru_holes(comp: dict[str, Any], n_rounds: int) -> int:
    """Holes completed in the event.

    ESPN golf uses STATUS_FINISH when a player has holed out the *current*
    round, not when the tournament is over. Treating that as 72 holes banks
    a Round-1 score as a final total. Use period (round number) + thru.
    """
    st = comp.get("status") or {}
    typ = (st.get("type") or {}).get("name") or ""
    try:
        period = int(st.get("period") or 0)
    except (TypeError, ValueError):
        period = 0
    total = max(int(n_rounds), 1) * 18
    thru = st.get("thru")
    if thru is not None:
        try:
            holes = int(thru) + max(period - 1, 0) * 18
            return max(0, min(int(holes), total))
        except (TypeError, ValueError):
            pass
    if typ == "STATUS_CUT":
        return min(max(period, 2), 2) * 18
    if typ in ("STATUS_FINISH", "STATUS_FINAL", "STATUS_PLAYOFF"):
        if 0 < period < n_rounds:
            return min(period * 18, total)
        return total
    return 0


def iter_competitors(event: dict[str, Any]) -> list[dict[str, Any]]:
    comps_block = event.get("competitions") or []
    if not comps_block or not isinstance(comps_block, list):
        return []
    first = comps_block[0]
    if not isinstance(first, dict):
        return []
    comps = first.get("competitors") or []
    if not isinstance(comps, list):
        return []
    return [c for c in comps if isinstance(c, dict)]


def competitor_to_player(comp: dict[str, Any]) -> Player:
    ath = comp.get("athlete") or {}
    flag = ath.get("flag") or {}
    country = flag.get("alt") or (ath.get("birthPlace") or {}).get("countryAbbreviation")
    return Player(
        player_id=str(ath.get("id") or comp.get("id")),
        name=str(ath.get("displayName") or "Unknown"),
        country=country,
    )


def event_completed(event: dict[str, Any]) -> tuple[bool, str]:
    """True when ESPN marks the event post/final. Playoff unresolved is not complete."""
    typ = (event.get("status") or {}).get("type") or {}
    state = str(typ.get("state") or "").lower()
    name = str(typ.get("name") or "").upper()
    desc = str(typ.get("description") or "")
    completed = state == "post" or name in {"STATUS_FINAL", "STATUS_OFFICIAL"}
    return completed, f"state={state or 'n/a'} name={name or 'n/a'} {desc}".strip()


def competitor_finish_place(comp: dict[str, Any]) -> int | None:
    return _finish_place(comp)


def event_finish_table(event: dict[str, Any]) -> dict[str, tuple[int | None, str]]:
    """player_id -> (finish place or None, display name)."""
    out: dict[str, tuple[int | None, str]] = {}
    for comp in iter_competitors(event):
        ath = comp.get("athlete") or {}
        pid = str(ath.get("id") or comp.get("id") or "")
        if not pid:
            continue
        name = str(ath.get("displayName") or ath.get("shortName") or pid)
        out[pid] = (_finish_place(comp), name)
    return out


def official_winner_ids(finishes: dict[str, tuple[int | None, str]]) -> list[str]:
    return [pid for pid, (place, _name) in finishes.items() if place == 1]


class EspnFieldFeed(DataFeed[list[Player]]):
    name = "espn_field"
    role = DataRole.PRIMARY

    def __init__(self, client: EspnClient, event_id: str | None = None) -> None:
        self.client = client
        self.event_id = event_id

    def fetch(self, **kwargs: Any) -> tuple[list[Player], DataQuality]:
        event_id = kwargs.get("event_id", self.event_id)
        live = bool(kwargs.get("live", event_id is None))
        payload = (
            self.client.current_leaderboard()
            if not event_id
            else self.client.event_leaderboard(str(event_id), live=live)
        )
        event = parse_event_payload(payload)
        players = [competitor_to_player(c) for c in iter_competitors(event) if c.get("athlete")]
        kind = SourceKind.REAL_LIVE if live else SourceKind.REAL_HISTORICAL
        q = _now_q(
            0.92,
            self.name,
            len(players),
            kind=kind,
            notes=f"ESPN leaderboard field for {event.get('name')} id={event.get('id')}",
        )
        return players, q


def espn_course_weather(event: dict[str, Any]) -> tuple[dict[str, Any] | None, DataQuality]:
    courses = event.get("courses") or []
    raw = (courses[0] if courses else {}).get("weather")
    if not raw:
        return None, unavailable_quality("espn_course_weather", "no weather object on ESPN course")
    payload = {
        "temperature_f": raw.get("temperature"),
        "wind_mph": raw.get("windSpeed"),
        "gust_mph": raw.get("gust"),
        "precip": raw.get("precipitation"),
        "condition": raw.get("conditionId") or raw.get("displayValue"),
        "last_updated": raw.get("lastUpdated"),
        "source": "espn_accuweather",
    }
    q = _now_q(
        0.72,
        "espn_accuweather",
        1,
        kind=SourceKind.REAL_LIVE,
        notes="current conditions attached to ESPN course object (AccuWeather)",
    )
    return payload, q


def parse_season_rankings(overview: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    cats = ((overview.get("seasonRankings") or {}).get("categories")) or []
    for c in cats:
        name = c.get("name")
        val = c.get("value")
        rank = c.get("rank")
        if name and val is not None:
            try:
                out[str(name)] = float(val)
            except (TypeError, ValueError):
                pass
        if name and rank is not None:
            try:
                out[f"{name}_rank"] = float(rank)
            except (TypeError, ValueError):
                pass
    return out
