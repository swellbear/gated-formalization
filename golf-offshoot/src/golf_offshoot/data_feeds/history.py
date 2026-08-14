"""Pre-event history index. Features for event T use only events that started before T."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Iterable

from golf_offshoot.data_feeds.espn import (
    _finish_place,
    _iso_date,
    _score_to_par,
    _status_name,
    iter_competitors,
    parse_course,
    parse_event_payload,
    parse_tournament,
)
from golf_offshoot.models.enums import SourceKind
from golf_offshoot.models.schemas import DataQuality, Tournament


def _parse_date(s: str) -> date:
    return date.fromisoformat(s[:10])


def norm_ppf(p: float) -> float:
    """Acklam inverse-normal approximation. p in (0,1)."""
    p = min(max(p, 1e-12), 1.0 - 1e-12)
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577459590117e02,
        -3.066479806138284e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464858e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )
    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
    ) / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def finish_skill(finish: int, field_size: int, made_cut: bool) -> float:
    """Higher is better. Based on finish percentile only (no future info)."""
    n = max(int(field_size), 2)
    place = min(max(int(finish), 1), n)
    u = (place - 0.5) / n
    z = -norm_ppf(u)
    if not made_cut:
        z -= 0.10
    return float(max(-4.0, min(4.0, z)))


@dataclass
class FinishRow:
    player_id: str
    name: str
    finish: int | None
    made_cut: bool
    withdrawn: bool
    won: bool
    top_5: bool
    top_10: bool
    top_20: bool
    score_to_par: float | None
    skill: float | None


@dataclass
class HistoricalEvent:
    event_id: str
    name: str
    start_date: str
    course_id: str
    course_name: str
    city: str
    state: str
    yardage: int
    par: int
    has_cut: bool
    cut_place: int
    field_size: int
    is_major: bool
    status_state: str
    finishes: list[FinishRow]
    wind_kph: float | None = None
    rain_mm: float | None = None
    tournament: Tournament | None = None

    @property
    def start(self) -> date:
        return _parse_date(self.start_date)


def event_from_espn(payload: dict[str, Any]) -> HistoricalEvent:
    event = parse_event_payload(payload) if "events" in payload else payload
    course, _q = parse_course(event)
    tournament = parse_tournament(event, course)
    comps = iter_competitors(event)
    field_n = max(len(comps), 1)
    rows: list[FinishRow] = []
    for comp in comps:
        ath = comp.get("athlete") or {}
        pid = str(ath.get("id") or comp.get("id"))
        name = str(ath.get("displayName") or pid)
        st = _status_name(comp)
        withdrawn = "WITHDRAW" in st
        made = st in ("STATUS_FINISH", "STATUS_FINAL", "STATUS_PLAYOFF") or (
            not tournament.has_cut and st not in ("STATUS_CUT",) and not withdrawn
        )
        if st == "STATUS_CUT":
            made = False
        finish = _finish_place(comp)
        if finish is None:
            finish = field_n if withdrawn or not made else field_n
        skill = None if withdrawn else finish_skill(finish, field_n, made)
        place = finish or field_n
        rows.append(
            FinishRow(
                player_id=pid,
                name=name,
                finish=finish,
                made_cut=bool(made and not withdrawn),
                withdrawn=withdrawn,
                won=place == 1 and made and not withdrawn,
                top_5=place <= 5 and made and not withdrawn,
                top_10=place <= 10 and made and not withdrawn,
                top_20=place <= 20 and made and not withdrawn,
                score_to_par=_score_to_par(comp),
                skill=skill,
            )
        )
    addr = ((event.get("courses") or [{}])[0].get("address") or {})
    status_state = str(((event.get("status") or {}).get("type") or {}).get("state") or "")
    return HistoricalEvent(
        event_id=str(event.get("id")),
        name=str(event.get("name") or ""),
        start_date=tournament.start_date,
        course_id=course.course_id,
        course_name=course.name,
        city=str(addr.get("city") or ""),
        state=str(addr.get("state") or ""),
        yardage=course.yardage,
        par=course.par,
        has_cut=tournament.has_cut,
        cut_place=tournament.cut_place,
        field_size=field_n,
        is_major=tournament.is_major,
        status_state=status_state,
        finishes=rows,
        tournament=tournament,
    )


@dataclass
class PlayerFeatures:
    talent_prior: float
    talent_prior_sd: float
    n_starts: int
    recent_form: float | None
    n_form: int
    trend: float | None
    n_trend: int
    course_history: float | None
    course_history_rounds: int
    weather_fit: float | None
    n_weather: int
    rest_days: int | None
    is_lesser_known: bool
    last_finish_skill: float | None = None


@dataclass
class HistoryIndex:
    events: list[HistoricalEvent] = field(default_factory=list)

    def sorted(self) -> "HistoryIndex":
        self.events.sort(key=lambda e: (e.start, e.event_id))
        return self

    def completed(self) -> list[HistoricalEvent]:
        return [e for e in self.events if e.status_state == "post"]

    def prior(self, before: str, *, exclude_event_id: str | None = None) -> list[HistoricalEvent]:
        b = _parse_date(before)
        out = []
        for e in self.events:
            if e.status_state != "post":
                continue
            if e.start >= b:
                continue
            if exclude_event_id and e.event_id == exclude_event_id:
                continue
            out.append(e)
        return out

    def features_for(
        self,
        player_id: str,
        *,
        before: str,
        course_id: str,
        event_wind_kph: float | None,
        exclude_event_id: str | None = None,
    ) -> PlayerFeatures:
        prior = self.prior(before, exclude_event_id=exclude_event_id)
        starts: list[tuple[HistoricalEvent, FinishRow]] = []
        for ev in prior:
            for row in ev.finishes:
                if row.player_id == player_id and not row.withdrawn and row.skill is not None:
                    starts.append((ev, row))
                    break
        n = len(starts)
        talent, sd = _decaying_talent(starts, before)
        form, n_form = _window_form(starts, k=5)
        trend, n_trend = _trend(starts)
        ch, ch_r = _course_hist(starts, course_id)
        wfit, n_w = _weather_fit(starts, event_wind_kph)
        rest = None
        if starts:
            last = starts[-1][0].start
            rest = (_parse_date(before) - last).days
        lesser = n < 8
        last_skill = starts[-1][1].skill if starts else None
        return PlayerFeatures(
            talent_prior=talent,
            talent_prior_sd=sd,
            n_starts=n,
            recent_form=form,
            n_form=n_form,
            trend=trend,
            n_trend=n_trend,
            course_history=ch,
            course_history_rounds=ch_r,
            weather_fit=wfit,
            n_weather=n_w,
            rest_days=rest,
            is_lesser_known=lesser,
            last_finish_skill=last_skill,
        )


def _decaying_talent(starts: list[tuple[HistoricalEvent, FinishRow]], before: str) -> tuple[float, float]:
    if not starts:
        return 0.0, 0.95
    b = _parse_date(before)
    num = den = 0.0
    for ev, row in starts:
        weeks = max((b - ev.start).days / 7.0, 0.0)
        w = math.exp(-weeks / 26.0) * math.log(ev.field_size + 1.0)
        if ev.is_major:
            w *= 1.15
        num += w * float(row.skill)
        den += w
    mean = num / den if den else 0.0
    sd = 0.28 + 0.55 / math.sqrt(len(starts))
    if len(starts) < 8:
        sd += 0.15
    return float(mean), float(min(1.2, sd))


def _window_form(starts: list[tuple[HistoricalEvent, FinishRow]], k: int) -> tuple[float | None, int]:
    if not starts:
        return None, 0
    window = starts[-k:]
    skills = [float(r.skill) for _, r in window]
    # residual vs longer-run mean so form is not double-counted talent
    long = sum(float(r.skill) for _, r in starts) / len(starts)
    form = sum(skills) / len(skills) - long
    return float(max(-3, min(3, form * 1.4))), len(window)


def _trend(starts: list[tuple[HistoricalEvent, FinishRow]]) -> tuple[float | None, int]:
    if len(starts) < 4:
        return None, len(starts)
    recent = [float(r.skill) for _, r in starts[-2:]]
    older = [float(r.skill) for _, r in starts[-5:-2]]
    if not older:
        return None, len(starts)
    t = sum(recent) / len(recent) - sum(older) / len(older)
    return float(max(-3, min(3, t * 1.2))), len(starts)


def _course_hist(
    starts: list[tuple[HistoricalEvent, FinishRow]], course_id: str
) -> tuple[float | None, int]:
    same = [(e, r) for e, r in starts if e.course_id == course_id]
    if not same:
        return None, 0
    skills = [float(r.skill) for _, r in same]
    mean = sum(skills) / len(skills)
    rounds = 4 * len(same)
    return float(max(-3, min(3, mean))), rounds


def _weather_fit(
    starts: list[tuple[HistoricalEvent, FinishRow]], event_wind_kph: float | None
) -> tuple[float | None, int]:
    if event_wind_kph is None:
        return None, 0
    pairs = []
    long = sum(float(r.skill) for _, r in starts) / len(starts) if starts else 0.0
    for ev, row in starts:
        if ev.wind_kph is None:
            continue
        pairs.append((float(ev.wind_kph), float(row.skill) - long))
    if len(pairs) < 4:
        return None, len(pairs)
    winds = [p[0] for p in pairs]
    res = [p[1] for p in pairs]
    w_mean = sum(winds) / len(winds)
    r_mean = sum(res) / len(res)
    var_w = sum((w - w_mean) ** 2 for w in winds)
    if var_w < 1e-6:
        return None, len(pairs)
    cov = sum((w - w_mean) * (r - r_mean) for w, r in zip(winds, res))
    beta = cov / var_w  # residual skill per kph wind
    wind_z = (event_wind_kph - w_mean) / math.sqrt(var_w / len(winds))
    fit = beta * (event_wind_kph - w_mean)
    return float(max(-3, min(3, fit + 0.15 * wind_z))), len(pairs)


def attach_outcomes(ev: HistoricalEvent) -> dict[str, FinishRow]:
    return {r.player_id: r for r in ev.finishes}


def quality_for_feature(
    *,
    n: int,
    source: str,
    kind: SourceKind,
    notes: str,
    missing: bool,
    score_if_present: float,
) -> DataQuality:
    from datetime import datetime, timezone

    return DataQuality(
        score=0.0 if missing else min(0.92, score_if_present),
        source_name=source,
        as_of=datetime.now(timezone.utc),
        n_observations=n,
        notes=notes,
        missing=missing,
        source_kind=kind if not missing else SourceKind.UNAVAILABLE,
    )
