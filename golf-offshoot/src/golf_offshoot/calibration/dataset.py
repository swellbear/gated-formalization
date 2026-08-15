"""Build a leakage-safe historical dataset from completed ESPN events."""

from __future__ import annotations

from dataclasses import dataclass

from golf_offshoot.config import RECENT_SG_EVENTS
from golf_offshoot.data_feeds.asof_sg import AsOfSgIndex, _percentile
from golf_offshoot.data_feeds.history import FinishRow, HistoricalEvent, HistoryIndex, PlayerFeatures
from golf_offshoot.learning.loop import PlayerResult
from golf_offshoot.models.enums import DataRole, RunMode, SourceKind
from golf_offshoot.models.schemas import (
    DataQuality,
    FieldSnapshot,
    Player,
    PlayerInputs,
    StrokesGainedProfile,
    Tournament,
)


@dataclass
class EventDataset:
    event: HistoricalEvent
    tournament: Tournament
    field: FieldSnapshot
    results: list[PlayerResult]
    n_with_history: int


def _q(n: int, score: float, notes: str) -> DataQuality:
    from golf_offshoot.localtime import now

    return DataQuality(
        score=score,
        role=DataRole.PRIMARY,
        source_name="espn_leaderboard_history",
        as_of=now(),
        n_observations=n,
        notes=notes,
        missing=n <= 0,
        source_kind=SourceKind.DERIVED_FROM_REAL if n > 0 else SourceKind.UNAVAILABLE,
    )


def features_to_player(pid: str, name: str, feat: PlayerFeatures) -> PlayerInputs:
    sq = {
        "talent_prior": _q(
            feat.n_starts,
            min(0.88, 0.35 + 0.04 * feat.n_starts),
            "pre-event decaying finish skill",
        ),
    }
    if feat.recent_form is not None:
        sq["recent_form"] = _q(feat.n_form, min(0.80, 0.40 + 0.08 * feat.n_form), "pre-event form residual")
    if feat.trend is not None:
        sq["short_term_trend"] = _q(feat.n_trend, 0.52, "pre-event trend")
    if feat.course_history is not None:
        sq["course_history"] = _q(
            feat.course_history_rounds,
            min(0.85, 0.30 + 0.06 * feat.course_history_rounds),
            "pre-event same-course finishes",
        )
    if feat.weather_fit is not None:
        sq["weather_suitability"] = _q(feat.n_weather, 0.55, "pre-event wind residual")
    sg = StrokesGainedProfile(
        quality=DataQuality(
            score=0.0,
            source_name="strokes_gained",
            as_of=sq["talent_prior"].as_of,
            missing=True,
            source_kind=SourceKind.UNAVAILABLE,
            notes="SG not attached yet; as-of panel fills this when EVENT_ONLY/THROUGH_EVENT exist",
        )
    )
    return PlayerInputs(
        player=Player(player_id=pid, name=name, is_lesser_known=feat.is_lesser_known),
        talent_prior=feat.talent_prior,
        talent_prior_sd=feat.talent_prior_sd,
        sg=sg,
        course_history_rounds=feat.course_history_rounds,
        course_history_sg=feat.course_history,
        recent_form_sg=feat.recent_form,
        short_term_trend=feat.trend,
        weather_fit=feat.weather_fit,
        rest_days=feat.rest_days,
        source_qualities=sq,
        course_fit_signal=feat.course_history,
    )


def result_from_row(row: FinishRow) -> PlayerResult:
    return PlayerResult(
        player_id=row.player_id,
        won=row.won,
        top_5=row.top_5,
        top_10=row.top_10,
        top_20=row.top_20,
        made_cut=row.made_cut,
        finish=row.finish,
    )


def build_event_dataset(
    idx: HistoryIndex,
    ev: HistoricalEvent,
    asof: AsOfSgIndex | None = None,
) -> EventDataset | None:
    if ev.status_state != "post" or ev.tournament is None:
        return None
    t = ev.tournament
    players: list[PlayerInputs] = []
    results: list[PlayerResult] = []
    n_hist = 0
    for row in ev.finishes:
        if row.withdrawn:
            continue
        feat = idx.features_for(
            row.player_id,
            before=ev.start_date,
            course_id=ev.course_id,
            event_wind_kph=ev.wind_kph,
            exclude_event_id=ev.event_id,
        )
        if feat.n_starts > 0:
            n_hist += 1
        players.append(features_to_player(row.player_id, row.name, feat))
        results.append(result_from_row(row))
    if len(players) < 20:
        return None
    field = FieldSnapshot(
        tournament_id=t.tournament_id,
        mode=RunMode.PRE_TOURNAMENT,
        players=players,
        notes="calibration pre-event snapshot; no future results in features",
        operating=True,
    )
    ds = EventDataset(event=ev, tournament=t, field=field, results=results, n_with_history=n_hist)
    if asof is not None:
        attach_asof_features(ds, asof)
    return ds


def attach_asof_features(ds: EventDataset, asof: AsOfSgIndex) -> None:
    """Leakage-safe: windows use only pills dated before this event start."""
    bundle = asof.bundle_for(
        before=ds.event.start_date,
        exclude_event_id=ds.event.event_id,
        exclude_name=ds.event.name,
    )
    n_long = 0
    n_recent = 0
    for p in ds.field.players:
        lt = asof.profile_long_term(p.player.name, bundle)
        rec = asof.profile_recent(p.player.name, bundle)
        if lt is not None:
            p.sg = lt
            if lt.quality is not None:
                p.source_qualities["putting"] = lt.quality
            n_long += 1
        if rec is not None:
            p.recent_sg = rec
            if rec.quality is not None:
                p.source_qualities["recent_form"] = rec.quality
            n_recent += 1
    ds.field.extra["asof_long_term"] = n_long
    ds.field.extra["asof_recent"] = n_recent
    ds.field.extra["asof_recent_events"] = [p.display_name for p in bundle.pills_used]
    ds.field.notes = (
        ds.field.notes
        + f"; as-of THROUGH_EVENT={n_long}/{len(ds.field.players)} "
        + f"EVENT_ONLY_recent={n_recent}/{len(ds.field.players)}"
    )


def feature_coverage(datasets: list[EventDataset]) -> dict[str, float]:
    n = sum(len(d.field.players) for d in datasets) or 1
    recent = sum(
        1
        for d in datasets
        for p in d.field.players
        if p.recent_sg is not None and p.recent_sg.quality is not None and not p.recent_sg.quality.missing
    )
    long_term = sum(
        1
        for d in datasets
        for p in d.field.players
        if p.sg.quality is not None and not p.sg.quality.missing
    )
    return {
        "n_player_starts": float(n),
        "recent_sg": recent / n,
        "long_term_sg": long_term / n,
        **{k: v for k, v in recent_sg_depth_stats(datasets).items() if k != "n_player_starts"},
    }


def recent_sg_depth_stats(datasets: list[EventDataset]) -> dict[str, float]:
    """Measured EVENT_ONLY weeks per player-start. Missing weeks are not zero-filled."""
    counts: list[int] = []
    n = 0
    hit = 0
    for d in datasets:
        for p in d.field.players:
            n += 1
            rec = p.recent_sg
            if rec is not None and rec.quality is not None and not rec.quality.missing:
                hit += 1
                counts.append(int(rec.quality.n_observations or 0))
    return {
        "n_player_starts": float(n),
        "recent_coverage": (hit / n) if n else 0.0,
        "median_events": _percentile(counts, 50),
        "p10_events": _percentile(counts, 10),
        "p90_events": _percentile(counts, 90),
        "mean_events": (sum(counts) / len(counts)) if counts else 0.0,
        "window_requested": float(RECENT_SG_EVENTS),
    }


def panel_is_materially_stronger(depth: dict[str, float]) -> tuple[bool, str]:
    """True only if recent-SG depth/coverage beat the last frozen as-of panel."""
    from golf_offshoot.config import (
        CALIB_MATERIAL_COVERAGE,
        CALIB_MATERIAL_MEDIAN_EVENTS,
        PREV_CALIB_MEDIAN_RECENT_EVENTS,
        PREV_CALIB_RECENT_COVERAGE,
        RECENT_SG_EVENTS,
    )

    median = float(depth.get("median_events") or 0.0)
    coverage = float(depth.get("recent_coverage") or depth.get("recent_sg") or 0.0)
    reasons: list[str] = []
    stronger = False
    if median >= CALIB_MATERIAL_MEDIAN_EVENTS:
        stronger = True
        reasons.append(
            f"median measured EVENT_ONLY events {median:.1f} >= {CALIB_MATERIAL_MEDIAN_EVENTS} "
            f"(calib-v2 median was {PREV_CALIB_MEDIAN_RECENT_EVENTS})"
        )
    if coverage >= CALIB_MATERIAL_COVERAGE:
        stronger = True
        reasons.append(
            f"recent-SG coverage {coverage:.1%} >= {CALIB_MATERIAL_COVERAGE:.0%} "
            f"(calib-v2 was {PREV_CALIB_RECENT_COVERAGE:.1%})"
        )
    if not stronger:
        reasons.append(
            f"requested last-{RECENT_SG_EVENTS} EVENT_ONLY window is not a materially stronger "
            f"panel than calib-v2 (median={median:.1f} vs {PREV_CALIB_MEDIAN_RECENT_EVENTS}, "
            f"coverage={coverage:.1%} vs {PREV_CALIB_RECENT_COVERAGE:.1%}). "
            "Bayesian search not rerun just to show activity."
        )
    return stronger, "; ".join(reasons)


def split_events(
    idx: HistoryIndex,
    *,
    burn_in: int = 6,
    holdout_n: int = 3,
) -> tuple[list[HistoricalEvent], list[HistoricalEvent]]:
    completed = [e for e in idx.completed() if e.tournament is not None]
    completed = sorted(completed, key=lambda e: (e.start, e.event_id))
    if len(completed) <= burn_in + holdout_n:
        raise ValueError(
            f"not enough completed events ({len(completed)}) for burn_in={burn_in} holdout={holdout_n}"
        )
    usable = completed[burn_in:]
    train = usable[:-holdout_n]
    hold = usable[-holdout_n:]
    return train, hold
