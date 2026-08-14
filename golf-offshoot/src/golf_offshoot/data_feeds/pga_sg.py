"""PGA Tour public GraphQL strokes-gained (same endpoint as pgatour.com/stats).

Season tables and THROUGH_EVENT / EVENT_ONLY windows are real StatDetails
payloads. EVENT_ONLY is one completed tournament; it is never inferred by
slicing a season-to-date table.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_BROWSER_UA, HttpCache
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.models.enums import DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality, StrokesGainedProfile

PGA_GQL = "https://orchestrator.pgatour.com/graphql"
# Public AppSync key shipped by pgatour.com (browser Network tab). Not a secret vendor token.
PGA_PUBLIC_API_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"

QUERY_EVENT_ONLY = "EVENT_ONLY"
QUERY_THROUGH_EVENT = "THROUGH_EVENT"

STAT_IDS = {
    "ott": "02567",
    "app": "02568",
    "arg": "02569",
    "putt": "02564",
    "total": "02675",
}

STAT_QUERY = """
query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {
  statDetails(tourCode: $tourCode, statId: $statId, year: $year, eventQuery: $eventQuery) {
    tourCode year statId statTitle lastProcessed
    tournamentPills { tournamentId displayName }
    rows {
      ... on StatDetailsPlayer {
        playerId playerName rank
        stats { statName statValue }
      }
    }
  }
}
"""


def _avg_stat(stats: list[dict[str, Any]]) -> float | None:
    for row in stats:
        if str(row.get("statName") or "").lower() == "avg":
            try:
                return float(str(row.get("statValue")).replace(",", ""))
            except (TypeError, ValueError):
                return None
    return None


def _rounds(stats: list[dict[str, Any]]) -> int:
    for row in stats:
        if "measured" in str(row.get("statName") or "").lower():
            try:
                return int(float(str(row.get("statValue")).replace(",", "")))
            except (TypeError, ValueError):
                return 0
    return 0


@dataclass
class SgRow:
    pga_id: str
    name: str
    ott: float | None = None
    app: float | None = None
    arg: float | None = None
    putt: float | None = None
    total: float | None = None
    n_rounds: int = 0
    n_events: int = 0


@dataclass
class SgTable:
    year: int
    last_processed: str = ""
    query_type: str = "SEASON"
    tournament_id: str | None = None
    by_name: dict[str, SgRow] = field(default_factory=dict)
    rows: list[SgRow] = field(default_factory=list)
    pills: list[dict[str, str]] = field(default_factory=list)


class PgaTourSgFeed(DataFeed[SgTable]):
    name = "pga_tour_sg"
    role = DataRole.PRIMARY

    def __init__(self, cache: HttpCache | None = None, refresh: bool = False) -> None:
        self.cache = cache or HttpCache()
        self.refresh = refresh

    def fetch(self, **kwargs: Any) -> tuple[SgTable, DataQuality]:
        year = int(kwargs.get("year") or 2026)
        tournament_id = kwargs.get("tournament_id")
        query_type = kwargs.get("query_type")
        event_query = None
        if tournament_id:
            qt = str(query_type or QUERY_THROUGH_EVENT)
            event_query = {"tournamentId": str(tournament_id), "queryType": qt}
        table = SgTable(
            year=year,
            query_type=str(query_type or "SEASON"),
            tournament_id=str(tournament_id) if tournament_id else None,
        )
        processed = []
        n_rows = 0
        for key, stat_id in STAT_IDS.items():
            payload = {
                "operationName": "StatDetails",
                "variables": {
                    "tourCode": "R",
                    "statId": stat_id,
                    "year": year,
                    "eventQuery": event_query,
                },
                "query": STAT_QUERY,
            }
            label = f"pga_sg_{key}_{year}"
            if event_query:
                label += f"_{event_query['tournamentId']}_{event_query['queryType']}"
            body, _meta = self.cache.post_json(
                PGA_GQL,
                payload,
                headers={
                    "User-Agent": DEFAULT_BROWSER_UA,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "x-api-key": PGA_PUBLIC_API_KEY,
                    "Origin": "https://www.pgatour.com",
                    "Referer": "https://www.pgatour.com/stats",
                },
                ttl_seconds=6 * 3600,
                refresh=self.refresh,
                label=label,
            )
            sd = ((body.get("data") or {}).get("statDetails")) or {}
            if body.get("errors") and not sd:
                raise FeedError(str(body.get("errors")[:1]))
            if not table.pills:
                table.pills = [
                    {
                        "tournamentId": str(p.get("tournamentId") or ""),
                        "displayName": str(p.get("displayName") or ""),
                    }
                    for p in (sd.get("tournamentPills") or [])
                    if p.get("tournamentId")
                ]
            lp = str(sd.get("lastProcessed") or "")
            if lp:
                processed.append(lp)
            for raw in sd.get("rows") or []:
                if not isinstance(raw, dict) or not raw.get("playerName"):
                    continue
                name = str(raw["playerName"])
                nid = normalize_name(name)
                row = table.by_name.get(nid) or SgRow(pga_id=str(raw.get("playerId") or ""), name=name)
                val = _avg_stat(raw.get("stats") or [])
                setattr(row, key, val)
                row.n_rounds = max(row.n_rounds, _rounds(raw.get("stats") or []))
                row.n_events = max(row.n_events, 1)
                table.by_name[nid] = row
                n_rows += 1
        table.rows = list(table.by_name.values())
        table.last_processed = processed[0] if processed else ""
        if not table.rows:
            q = unavailable_quality(self.name, "PGA Tour GraphQL returned no SG rows")
            return table, q
        window = table.query_type
        if table.tournament_id:
            window = f"{table.query_type}:{table.tournament_id}"
        q = DataQuality(
            score=0.86 if table.query_type == QUERY_EVENT_ONLY else 0.88,
            role=self.role,
            source_name=self.name,
            as_of=datetime.now(timezone.utc),
            n_observations=len(table.rows),
            notes=(
                f"PGA Tour StatDetails year={year} window={window} "
                f"lastProcessed={table.last_processed!r}; {len(table.rows)} players; "
                "categories OTT/APP/ARG/PUTT/Total"
            ),
            source_kind=SourceKind.REAL_HISTORICAL,
        )
        return table, q

    def profile_for(self, espn_name: str, table: SgTable, quality: DataQuality) -> StrokesGainedProfile | None:
        nid = match_name(espn_name, {k: k for k in table.by_name})
        if nid is None:
            return None
        row = table.by_name[nid]
        if row.total is None and row.app is None:
            return None
        return StrokesGainedProfile(
            ott=float(row.ott or 0.0),
            app=float(row.app or 0.0),
            arg=float(row.arg or 0.0),
            putt=float(row.putt or 0.0),
            total=float(row.total if row.total is not None else (row.app or 0.0) + (row.ott or 0.0)),
            quality=quality.model_copy(
                update={
                    "n_observations": row.n_events or row.n_rounds or quality.n_observations,
                    "notes": (
                        quality.notes + f"; matched {row.name} pga_id={row.pga_id} n_events={row.n_events}"
                    ).strip(),
                }
            ),
        )
