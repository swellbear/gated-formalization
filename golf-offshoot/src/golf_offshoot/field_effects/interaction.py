"""Field-interaction effects: value vs this week's composition, not a global add-on.

If the field is packed with bombers, extra distance is worth less.
If the field is weak on putting and greens are fast, putting is worth more.
"""

from __future__ import annotations

import numpy as np

from golf_offshoot.models.enums import CourseType
from golf_offshoot.models.schemas import Course, PlayerInputs


def _profile(p: PlayerInputs) -> dict[str, float | None]:
    sg = p.sg
    sg_ok = sg.quality is not None and not sg.quality.missing
    dist = sg.driving_distance_yd
    acc = sg.driving_accuracy_pct
    return {
        "distance": None if dist is None else (dist - 295.0) / 12.0,
        "accuracy": None if acc is None else (acc - 60.0) / 8.0,
        "approach": sg.app if sg_ok else None,
        "putting": sg.putt if sg_ok else None,
        "arg": sg.arg if sg_ok else None,
        "ott": sg.ott if sg_ok else None,
    }


def course_demand(course: Course, *, honest: bool = False) -> dict[str, float]:
    ct = course.course_type
    demand = {
        "distance": 0.35 + 0.4 * (course.yardage - 7000) / 800.0,
        "accuracy": 0.30 + 0.55 * course.tightness + 0.25 * course.rough_severity,
        "approach": 0.70,
        "putting": 0.35 + 0.40 * course.green_speed,
        "arg": 0.25 + 0.40 * course.rough_severity,
        "ott": 0.40,
    }
    if honest:
        demand["accuracy"] = 0.30
        demand["putting"] = 0.35
        demand["arg"] = 0.25
        demand["distance"] = 0.35 + 0.4 * (course.yardage - 7000) / 800.0
    if ct == CourseType.LINKS:
        demand["distance"] *= 0.75
        demand["accuracy"] *= 1.05
        demand["arg"] *= 1.25
        demand["ott"] *= 0.85
    elif ct == CourseType.MAJOR_SETUP:
        demand["accuracy"] *= 1.35
        demand["distance"] *= 0.80
        demand["arg"] *= 1.20
    elif ct == CourseType.MOUNTAIN:
        demand["distance"] *= 1.25
    elif ct == CourseType.STADIUM:
        demand["putting"] *= 1.20
        demand["approach"] *= 1.10
    return demand


def field_interaction_adjustments(
    field: list[PlayerInputs],
    course: Course,
    scale: float = 0.22,
    *,
    honest: bool = False,
) -> dict[str, float]:
    """Return Δθ per player_id from relative-to-field × course demand × crowding."""
    if len(field) < 4:
        return {p.player.player_id: 0.0 for p in field}
    profiles = [_profile(p) for p in field]
    keys_all = ["distance", "accuracy", "approach", "putting", "arg", "ott"]
    keys = []
    min_frac = 0.9 if honest else 0.5
    for k in keys_all:
        n_have = sum(pr[k] is not None for pr in profiles)
        if n_have >= max(4, int(min_frac * len(field))):
            keys.append(k)
    if not keys:
        return {p.player.player_id: 0.0 for p in field}
    mats = np.array(
        [[float("nan") if pr[k] is None else float(pr[k]) for k in keys] for pr in profiles],
        dtype=float,
    )
    if honest:
        mean = np.nanmean(mats, axis=0)
        std = np.nanstd(mats, axis=0)
        std = np.where(~np.isfinite(std) | (std < 1e-6), 1.0, std)
        crowding = np.exp(-std)
        demand = course_demand(course, honest=True)
        dvec = np.array([demand.get(k, 0.4) for k in keys])
        rel = mats - mean
        rel = np.where(np.isfinite(rel), rel, 0.0)
        adj = (rel * dvec * (1.0 - 0.55 * crowding)).sum(axis=1) * scale
        return {field[i].player.player_id: float(adj[i]) for i in range(len(field))}
    mats = np.where(np.isfinite(mats), mats, 0.0)
    mean = mats.mean(axis=0)
    std = mats.std(axis=0)
    std = np.where(std < 1e-6, 1.0, std)
    crowding = np.exp(-std)
    demand = course_demand(course, honest=False)
    dvec = np.array([demand.get(k, 0.4) for k in keys])
    rel = mats - mean
    adj = (rel * dvec * (1.0 - 0.55 * crowding)).sum(axis=1) * scale
    return {field[i].player.player_id: float(adj[i]) for i in range(len(field))}


def apply_field_interactions(
    field: list[PlayerInputs],
    course: Course,
    *,
    honest: bool = False,
) -> dict[str, float]:
    from golf_offshoot.models.enums import FactorStatus
    from golf_offshoot.models.schemas import DataQuality, FreeParameterState
    from golf_offshoot.localtime import now

    adjs = field_interaction_adjustments(field, course, honest=honest)
    as_of = now()
    n_skill = sum(
        1
        for p in field
        if (p.sg.quality is not None and not p.sg.quality.missing)
        or p.sg.driving_distance_yd is not None
        or p.sg.driving_accuracy_pct is not None
    )
    usable = n_skill >= 4
    from golf_offshoot.models.enums import SourceKind

    for p in field:
        delta = adjs.get(p.player.player_id, 0.0)
        p.factors["field_interaction"] = FreeParameterState(
            factor_id="field_interaction",
            status=FactorStatus.CONSTRAINED if usable else FactorStatus.UNCONSTRAINED,
            standardized_evidence=float(np.clip(delta / 0.22, -3, 3)) if usable else 0.0,
            quality=DataQuality(
                score=0.70 if usable else 0.0,
                source_name="field_composition",
                as_of=as_of,
                n_observations=len(field) if usable else 0,
                missing=not usable,
                source_kind=SourceKind.DERIVED_FROM_REAL if usable else SourceKind.UNAVAILABLE,
                notes="relative-to-field from observed traits only; no SG fill-in",
            ),
            n_obs=len(field) if usable else 0,
            importance=0.18,
            open_question="" if usable else "field interaction parked: no real skill-mix coverage",
            notes=f"relative-to-field Δθ proxy {delta:+.3f}" if usable else "unavailable",
        )
    return adjs
