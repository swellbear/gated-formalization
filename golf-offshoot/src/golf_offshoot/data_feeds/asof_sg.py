"""True as-of SG windows from PGA Tour EVENT_ONLY / THROUGH_EVENT tables.

Long-term: StatDetails THROUGH_EVENT for the last completed PGA event that
started before the analysis tournament. Recent: mean of EVENT_ONLY tables for
the last N such events. Season-to-date is never sliced into a fake last-N window.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any, Iterable

from golf_offshoot.config import (
    RECENT_SG_EVENTS,
    RECENT_SG_MIN_EVENTS,
    RECENT_SG_PILL_YEARS,
)
from golf_offshoot.data_feeds.base import unavailable_quality
from golf_offshoot.data_feeds.names import normalize_name
from golf_offshoot.data_feeds.pga_sg import (
    QUERY_EVENT_ONLY,
    QUERY_THROUGH_EVENT,
    PgaTourSgFeed,
    SgRow,
    SgTable,
)
from golf_offshoot.models.enums import DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality, StrokesGainedProfile


def _parse_day(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


def _tokens(name: str) -> set[str]:
    return {t for t in normalize_name(name).split() if len(t) > 2}


def year_from_pill_id(tournament_id: str, default: int) -> int:
    tid = str(tournament_id or "")
    if len(tid) >= 5 and tid[0] == "R" and tid[1:5].isdigit():
        return int(tid[1:5])
    return default


@dataclass
class SgPill:
    tournament_id: str
    display_name: str
    start_date: str | None = None
    espn_event_id: str | None = None


@dataclass
class AsOfSgBundle:
    long_term: SgTable | None
    long_term_q: DataQuality
    recent: SgTable | None
    recent_q: DataQuality
    pills_used: list[SgPill] = field(default_factory=list)
    long_term_pill: SgPill | None = None


class AsOfSgIndex:
    """Bind PGA tournament pills to ESPN dates and fetch as-of windows."""

    def __init__(self, feed: PgaTourSgFeed, year: int = 2026) -> None:
        self.feed = feed
        self.year = year
        self.pills: list[SgPill] = []
        self._tables: dict[str, tuple[SgTable | None, DataQuality]] = {}

    def load_pills(self) -> list[SgPill]:
        by_id: dict[str, SgPill] = {}
        for y in range(self.year, self.year - RECENT_SG_PILL_YEARS, -1):
            table, _q = self.feed.quality_or_missing(year=y)
            raw = table.pills if isinstance(table, SgTable) else []
            for p in raw:
                tid = str(p.get("tournamentId") or "")
                if not tid or tid in by_id:
                    continue
                by_id[tid] = SgPill(tournament_id=tid, display_name=str(p.get("displayName") or ""))
        self.pills = list(by_id.values())
        return self.pills

    def bind_history(self, events: Iterable[Any]) -> int:
        """Attach ESPN start dates 1-to-1 by name. Returns how many pills dated."""
        if not self.pills:
            self.load_pills()
        catalog = []
        for ev in events:
            name = str(getattr(ev, "name", "") or "")
            start = str(getattr(ev, "start_date", "") or "")
            eid = str(getattr(ev, "event_id", "") or "")
            if name and start and eid:
                catalog.append((name, start, eid, _tokens(name)))
        pairs: list[tuple] = []
        for i, pill in enumerate(self.pills):
            want = _tokens(pill.display_name)
            pill_year = year_from_pill_id(pill.tournament_id, self.year)
            for name, start, eid, have in catalog:
                score = len(want & have)
                if score < 2:
                    continue
                try:
                    ev_year = int(str(start)[:4])
                except ValueError:
                    ev_year = 0
                year_bonus = 1 if ev_year == pill_year else 0
                pairs.append((score + year_bonus, score, year_bonus, start, i, eid))
        pairs.sort(reverse=True)
        used_pills: set[int] = set()
        used_events: set[str] = set()
        n = 0
        for _total, _score, _yb, start, i, eid in pairs:
            if i in used_pills or eid in used_events:
                continue
            self.pills[i].start_date = start
            self.pills[i].espn_event_id = eid
            used_pills.add(i)
            used_events.add(eid)
            n += 1
        return n

    def pills_before(
        self,
        before: str,
        *,
        exclude_event_id: str | None = None,
        exclude_name: str | None = None,
    ) -> list[SgPill]:
        cutoff = _parse_day(before)
        if cutoff is None:
            return []
        skip_tokens = _tokens(exclude_name or "")
        out: list[SgPill] = []
        for pill in self.pills:
            if not pill.start_date:
                continue
            start = _parse_day(pill.start_date)
            if start is None or start >= cutoff:
                continue
            if exclude_event_id and pill.espn_event_id == exclude_event_id:
                continue
            if skip_tokens and len(skip_tokens & _tokens(pill.display_name)) >= 2:
                continue
            out.append(pill)
        out.sort(key=lambda p: p.start_date or "", reverse=True)
        uniq: list[SgPill] = []
        seen: set[str] = set()
        for pill in out:
            key = pill.espn_event_id or f"{pill.start_date}:{pill.tournament_id}"
            if key in seen:
                continue
            seen.add(key)
            uniq.append(pill)
        return uniq

    def _fetch_table(self, pill: SgPill, query_type: str) -> tuple[SgTable | None, DataQuality]:
        year = year_from_pill_id(pill.tournament_id, self.year)
        key = f"{year}:{pill.tournament_id}:{query_type}"
        if key in self._tables:
            return self._tables[key]
        table, q = self.feed.quality_or_missing(
            year=year,
            tournament_id=pill.tournament_id,
            query_type=query_type,
        )
        self._tables[key] = (table if isinstance(table, SgTable) else None, q)
        return self._tables[key]

    def bundle_for(
        self,
        *,
        before: str,
        exclude_event_id: str | None = None,
        exclude_name: str | None = None,
        n_recent: int = RECENT_SG_EVENTS,
    ) -> AsOfSgBundle:
        prior = self.pills_before(
            before, exclude_event_id=exclude_event_id, exclude_name=exclude_name
        )
        long_term = None
        long_pill = None
        long_q = unavailable_quality(
            "pga_tour_sg_through_event",
            "no completed PGA StatDetails pill dated before this event start",
        )
        if prior:
            long_pill = prior[0]
            table, q = self._fetch_table(long_pill, QUERY_THROUGH_EVENT)
            if table is not None and table.rows and q and not q.missing:
                long_term = table
                long_q = q.model_copy(
                    update={
                        "notes": (
                            f"{q.notes}; THROUGH_EVENT as-of {long_pill.display_name} "
                            f"start={long_pill.start_date} (before {before})"
                        )
                    }
                )
        recent_ids = prior[:n_recent]
        recent_table = None
        recent_q = unavailable_quality(
            "pga_tour_sg_event_only",
            f"true as-of recent SG unavailable: no EVENT_ONLY pills dated before this start; "
            f"season-to-date was not used as a last-{n_recent} proxy",
        )
        if len(recent_ids) >= RECENT_SG_MIN_EVENTS:
            tables: list[SgTable] = []
            used: list[SgPill] = []
            for pill in recent_ids:
                table, q = self._fetch_table(pill, QUERY_EVENT_ONLY)
                if table is not None and table.rows and q and not q.missing:
                    tables.append(table)
                    used.append(pill)
            averaged = average_event_tables(tables)
            if averaged.rows:
                recent_table = averaged
                n_players = len(averaged.rows)
                n_ev = len(tables)
                recent_q = DataQuality(
                    score=min(0.88, 0.40 + 0.025 * n_ev),
                    role=DataRole.PRIMARY,
                    source_name="pga_tour_sg_event_only",
                    as_of=datetime.now(timezone.utc),
                    n_observations=n_players,
                    notes=(
                        f"mean of {n_ev}/{n_recent} requested PGA EVENT_ONLY SG tables before {before}: "
                        + ", ".join(
                            f"{p.display_name} ({p.start_date})" for p in used
                        )
                        + f"; {n_players} players with >=1 measured event; "
                        "missing weeks skipped not zero-filled; not a season-to-date slice"
                    ),
                    source_kind=SourceKind.DERIVED_FROM_REAL,
                )
                recent_ids = used
        return AsOfSgBundle(
            long_term=long_term,
            long_term_q=long_q,
            recent=recent_table,
            recent_q=recent_q,
            pills_used=recent_ids,
            long_term_pill=long_pill,
        )

    def profile_long_term(self, espn_name: str, bundle: AsOfSgBundle) -> StrokesGainedProfile | None:
        if bundle.long_term is None:
            return None
        return self.feed.profile_for(espn_name, bundle.long_term, bundle.long_term_q)

    def profile_recent(self, espn_name: str, bundle: AsOfSgBundle) -> StrokesGainedProfile | None:
        if bundle.recent is None or bundle.recent_q.missing:
            return None
        profile = self.feed.profile_for(espn_name, bundle.recent, bundle.recent_q)
        return scale_recent_sg_quality(profile)


def average_event_tables(tables: list[SgTable]) -> SgTable:
    """Mean SG by player across EVENT_ONLY tables. Missing weeks are skipped, not zero-filled."""
    acc: dict[str, dict[str, list[float]]] = {}
    meta: dict[str, SgRow] = {}
    year = tables[0].year if tables else 2026
    for table in tables:
        for nid, row in table.by_name.items():
            bucket = acc.setdefault(nid, {"ott": [], "app": [], "arg": [], "putt": [], "total": []})
            meta.setdefault(nid, SgRow(pga_id=row.pga_id, name=row.name))
            for key in ("ott", "app", "arg", "putt", "total"):
                val = getattr(row, key)
                if val is not None:
                    bucket[key].append(float(val))
            meta[nid].n_rounds += row.n_rounds
            meta[nid].n_events += 1
    out = SgTable(year=year, query_type="EVENT_ONLY_MEAN", last_processed="as-of EVENT_ONLY mean")
    for nid, bucket in acc.items():
        row = meta[nid]
        for key, vals in bucket.items():
            if vals:
                setattr(row, key, sum(vals) / len(vals))
        if row.total is None and row.app is None:
            continue
        out.by_name[nid] = row
    out.rows = list(out.by_name.values())
    return out


def scale_recent_sg_quality(profile: StrokesGainedProfile | None) -> StrokesGainedProfile | None:
    """Per-player quality tracks measured EVENT_ONLY weeks, not the field-wide table count."""
    if profile is None or profile.quality is None:
        return profile
    n_ev = int(profile.quality.n_observations or 0)
    score = min(0.88, 0.38 + 0.032 * max(n_ev, 1))
    return profile.model_copy(
        update={
            "quality": profile.quality.model_copy(
                update={
                    "score": score,
                    "notes": (
                        f"{profile.quality.notes}; recent_quality from {n_ev} measured "
                        "EVENT_ONLY events (not zero-filled misses)"
                    ).strip(),
                }
            )
        }
    )


def _percentile(values: list[int], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    idx = (len(ordered) - 1) * (pct / 100.0)
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    frac = idx - lo
    return float(ordered[lo] * (1.0 - frac) + ordered[hi] * frac)


def asof_coverage_report(
    bundle: AsOfSgBundle,
    field_names: list[str],
    feed: PgaTourSgFeed,
) -> dict[str, Any]:
    """Per-window / per-category coverage for the named field. Names unmatched stay unavailable."""
    n = len(field_names)
    long_hit = 0
    recent_hit = 0
    cats = {k: {"long_term": 0, "recent": 0} for k in ("ott", "app", "arg", "putt", "total")}
    recent_events: list[int] = []
    for name in field_names:
        lt = feed.profile_for(name, bundle.long_term, bundle.long_term_q) if bundle.long_term else None
        rec = feed.profile_for(name, bundle.recent, bundle.recent_q) if bundle.recent and not bundle.recent_q.missing else None
        if lt is not None:
            long_hit += 1
            for k in cats:
                if getattr(lt, k) is not None:
                    cats[k]["long_term"] += 1
        if rec is not None:
            recent_hit += 1
            recent_events.append(int(rec.quality.n_observations) if rec.quality else 0)
            for k in cats:
                if getattr(rec, k) is not None:
                    cats[k]["recent"] += 1
    median = _percentile(recent_events, 50)
    return {
        "field_size": n,
        "long_term_available": bundle.long_term is not None and not bundle.long_term_q.missing,
        "long_term_source": bundle.long_term_q.source_name,
        "long_term_kind": bundle.long_term_q.source_kind.value,
        "long_term_coverage": f"{long_hit}/{n}",
        "long_term_anchor": bundle.long_term_pill.display_name if bundle.long_term_pill else None,
        "recent_available": bundle.recent is not None and not bundle.recent_q.missing,
        "recent_source": bundle.recent_q.source_name,
        "recent_kind": bundle.recent_q.source_kind.value,
        "recent_coverage": f"{recent_hit}/{n}",
        "recent_window_requested": RECENT_SG_EVENTS,
        "recent_events_used": [f"{p.display_name} ({p.start_date})" for p in bundle.pills_used],
        "recent_events_used_n": len(bundle.pills_used),
        "recent_median_events_per_player": median,
        "recent_p10_events_per_player": _percentile(recent_events, 10),
        "recent_p50_events_per_player": median,
        "recent_p90_events_per_player": _percentile(recent_events, 90),
        "recent_mean_events_per_player": (
            sum(recent_events) / len(recent_events) if recent_events else 0.0
        ),
        "recent_players_with_window": recent_hit,
        "by_category": cats,
        "notes": (
            f"Recent window is EVENT_ONLY mean of up to {RECENT_SG_EVENTS} completed pills; "
            "missing weeks skipped not zero-filled. Season-to-date is not a last-N proxy. "
            "Depth is measured events per player, not the requested window length."
        ),
    }
