"""Field-interaction effects: value vs this week's composition, not a global add-on.

If the field is packed with bombers, extra distance is worth less.
If the field is weak on putting and greens are fast, putting is worth more.
"""

from __future__ import annotations

import numpy as np

from golf_offshoot.models.enums import CourseType
from golf_offshoot.models.schemas import Course, PlayerInputs


def _profile(p: PlayerInputs) -> dict[str, float]:
    sg = p.sg
    return {
        "distance": ((sg.driving_distance_yd or 295.0) - 295.0) / 12.0,
        "accuracy": ((sg.driving_accuracy_pct or 60.0) - 60.0) / 8.0,
        "approach": sg.app,
        "putting": sg.putt,
        "arg": sg.arg,
        "ott": sg.ott,
    }


def course_demand(course: Course) -> dict[str, float]:
    ct = course.course_type
    demand = {
        "distance": 0.35 + 0.4 * (course.yardage - 7000) / 800.0,
        "accuracy": 0.30 + 0.55 * course.tightness + 0.25 * course.rough_severity,
        "approach": 0.70,
        "putting": 0.35 + 0.40 * course.green_speed,
        "arg": 0.25 + 0.40 * course.rough_severity,
        "ott": 0.40,
    }
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
) -> dict[str, float]:
    """Return Δθ per player_id from relative-to-field × course demand × crowding."""
    if len(field) < 4:
        return {p.player.player_id: 0.0 for p in field}
    keys = ["distance", "accuracy", "approach", "putting", "arg", "ott"]
    mats = np.array([[_profile(p)[k] for k in keys] for p in field], dtype=float)
    mean = mats.mean(axis=0)
    std = mats.std(axis=0)
    std = np.where(std < 1e-6, 1.0, std)
    # crowding high when dispersion is low
    crowding = np.exp(-std)
    demand = course_demand(course)
    dvec = np.array([demand[k] for k in keys])
    rel = mats - mean
    # extra trait value shrinks when everyone has it
    adj = (rel * dvec * (1.0 - 0.55 * crowding)).sum(axis=1) * scale
    return {field[i].player.player_id: float(adj[i]) for i in range(len(field))}


def apply_field_interactions(field: list[PlayerInputs], course: Course) -> dict[str, float]:
    from golf_offshoot.models.enums import FactorStatus
    from golf_offshoot.models.schemas import DataQuality, FreeParameterState
    from datetime import datetime, timezone

    adjs = field_interaction_adjustments(field, course)
    now = datetime.now(timezone.utc)
    for p in field:
        delta = adjs.get(p.player.player_id, 0.0)
        p.factors["field_interaction"] = FreeParameterState(
            factor_id="field_interaction",
            status=FactorStatus.CONSTRAINED,
            standardized_evidence=float(np.clip(delta / 0.22, -3, 3)),
            quality=DataQuality(
                score=0.70,
                source_name="field_composition",
                as_of=now,
                n_observations=len(field),
            ),
            n_obs=len(field),
            importance=0.18,
            open_question="",
            notes=f"relative-to-field Δθ proxy {delta:+.3f}",
        )
    return adjs
