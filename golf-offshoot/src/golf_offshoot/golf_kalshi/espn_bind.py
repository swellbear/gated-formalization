"""Bind a Kalshi golf series to a live ESPN event. Not PGA-only. Wrong-tour bind is worse than a miss."""

from __future__ import annotations

import re
from typing import Any

from golf_offshoot.golf_kalshi.catalog_view import catalog_family

_STOP = {
    "the",
    "and",
    "for",
    "golf",
    "tour",
    "championship",
    "open",
    "presented",
    "official",
    "betting",
    "odds",
    "kalshi",
}

FAMILY_LEAGUES: dict[str, tuple[str, ...]] = {
    "PGA Tour": ("pga",),
    "LIV": ("liv", "pga"),
    "LPGA": ("lpga",),
    "DP World": ("eur",),
    "Champions": ("champ",),
    "Masters": ("pga",),
    "US Open": ("pga",),
    "The Open": ("pga",),
    "Majors": ("pga",),
    "Ryder Cup": ("pga",),
    "Solheim Cup": ("lpga", "pga"),
    "Presidents Cup": ("pga",),
    "TGL": ("pga",),
    "Other golf": ("pga", "eur", "lpga", "liv", "champ"),
}

_LEAGUE_OK: dict[str, bool] = {}


def reset_league_probe() -> None:
    _LEAGUE_OK.clear()
    EspnLeagueBoards.clear_client_cache()


def _tokens(blob: str) -> set[str]:
    return {
        tok
        for tok in re.findall(r"[a-z0-9]+", str(blob or "").lower())
        if len(tok) > 1 and tok not in _STOP
    }


def title_overlap(left: str, right: str) -> float:
    a = _tokens(left)
    b = _tokens(right)
    if not a or not b:
        return 0.0
    return len(a & b) / float(min(len(a), len(b)))


def titles_bind(kalshi_title: str, espn_name: str) -> bool:
    shared = _tokens(kalshi_title) & _tokens(espn_name)
    return len(shared) >= 2 and title_overlap(kalshi_title, espn_name) >= 0.5


def leagues_for_family(family: str) -> tuple[str, ...]:
    return FAMILY_LEAGUES.get(str(family or ""), FAMILY_LEAGUES["Other golf"])


def event_key_for(market: dict[str, Any] | None) -> str:
    row = market or {}
    return str(row.get("event_ticker") or row.get("series_ticker") or "").strip()


def kalshi_title_blob(market: dict[str, Any] | None, series: dict[str, Any] | None = None) -> str:
    row = market or {}
    ser = series or {}
    return " ".join(
        [
            str(row.get("event_title") or ""),
            str(row.get("title") or ""),
            str(ser.get("title") or ""),
            str(row.get("series_ticker") or ""),
        ]
    )


def espn_score_rows(event: dict[str, Any] | None) -> list[dict[str, Any]]:
    from golf_offshoot.data_feeds.espn import _score_to_par, _thru_holes, iter_competitors

    rows: list[dict[str, Any]] = []
    if not event:
        return rows
    for comp in iter_competitors(event):
        ath = comp.get("athlete") or {}
        pid = str(ath.get("id") or comp.get("id") or "")
        name = str(ath.get("displayName") or ath.get("shortName") or "")
        if not pid and not name:
            continue
        rows.append(
            {
                "id": pid,
                "name": name,
                "score": _score_to_par(comp),
                "thru": _thru_holes(comp, 4),
            }
        )
    return rows


def espn_name_candidates(event: dict[str, Any] | None) -> dict[str, str]:
    from golf_offshoot.data_feeds.names import normalize_name

    out: dict[str, str] = {}
    for row in espn_score_rows(event):
        name = str(row.get("name") or "")
        pid = str(row.get("id") or "")
        if name and pid:
            out[normalize_name(name)] = pid
    return out


def _miss(family: str, tried: list[str]) -> dict[str, Any]:
    return {
        "espn_id": "",
        "espn_name": "",
        "league": "",
        "family": family,
        "field_source": "",
        "espn_rows": [],
        "candidates": {},
        "tried_leagues": tried,
        "live_competitors": 0,
    }


def _hit(event: dict[str, Any], *, league: str, family: str, tried: list[str]) -> dict[str, Any]:
    rows = espn_score_rows(event)
    return {
        "espn_id": str(event.get("id") or ""),
        "espn_name": str(event.get("name") or event.get("shortName") or ""),
        "league": league,
        "family": family,
        "field_source": "espn",
        "espn_rows": rows,
        "candidates": espn_name_candidates(event),
        "tried_leagues": tried,
        "live_competitors": len(rows),
    }


class EspnLeagueBoards:
    """One ESPN leaderboard read per league per tick. Bind is in-memory title overlap."""

    _shared_client = None

    def __init__(self, *, client=None) -> None:
        self._client = client
        self._payloads: dict[str, Any] = {}

    @classmethod
    def clear_client_cache(cls) -> None:
        cls._shared_client = None

    def client(self):
        if self._client is not None:
            return self._client
        if EspnLeagueBoards._shared_client is None:
            from golf_offshoot.data_feeds.espn import EspnClient
            from golf_offshoot.data_feeds.http import HttpCache
            from golf_offshoot.golf_kalshi.paths import cache_dir

            EspnLeagueBoards._shared_client = EspnClient(
                HttpCache(cache_dir=cache_dir()), refresh=False
            )
        return EspnLeagueBoards._shared_client

    def payload(self, league: str) -> dict[str, Any] | None:
        token = str(league or "").strip().lower()
        if not token:
            return None
        if token in self._payloads:
            return self._payloads[token]
        if token in _LEAGUE_OK and not _LEAGUE_OK[token]:
            self._payloads[token] = None
            return None
        try:
            payload = self.client().leaderboard_for_league(token)
        except Exception:
            _LEAGUE_OK[token] = False
            self._payloads[token] = None
            return None
        from golf_offshoot.data_feeds.espn import iter_events

        events = iter_events(payload if isinstance(payload, dict) else {})
        _LEAGUE_OK[token] = bool(events)
        if not events:
            self._payloads[token] = None
            return None
        parsed = payload if isinstance(payload, dict) else None
        self._payloads[token] = parsed
        return parsed

    def bind(
        self,
        market: dict[str, Any],
        *,
        series: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        from golf_offshoot.data_feeds.espn import iter_events

        family = catalog_family(str(market.get("series_ticker") or ""))
        blob = kalshi_title_blob(market, series)
        tried: list[str] = []
        for league in leagues_for_family(family):
            tried.append(league)
            payload = self.payload(league)
            if not payload:
                continue
            for event in iter_events(payload):
                name = str(event.get("name") or event.get("shortName") or "")
                if titles_bind(blob, name):
                    return _hit(event, league=league, family=family, tried=tried)
        return _miss(family, tried)


def bind_espn_event(
    market: dict[str, Any],
    *,
    client=None,
    series: dict[str, Any] | None = None,
    boards: EspnLeagueBoards | None = None,
) -> dict[str, Any]:
    """Return espn_id / name / league or a miss. Does not invent an event."""
    boards = boards or EspnLeagueBoards(client=client)
    if client is not None:
        boards._client = client
    return boards.bind(market, series=series)
