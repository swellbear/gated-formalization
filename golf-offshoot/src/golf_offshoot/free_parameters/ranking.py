"""Importance ranking: impact × constrainingability, course-type adjusted."""

from __future__ import annotations

from golf_offshoot.free_parameters.catalog import CATALOG
from golf_offshoot.models.enums import CourseType, RunMode
from golf_offshoot.models.schemas import FreeParameterDef


def course_impact(defn: FreeParameterDef, course_type: CourseType) -> float:
    mult = defn.course_multipliers.get(course_type.value, 1.0)
    return defn.base_impact * mult


def importance(defn: FreeParameterDef, course_type: CourseType) -> float:
    return course_impact(defn, course_type) * defn.base_constrainingability


def ranked_parameters(
    course_type: CourseType,
    mode: RunMode = RunMode.PRE_TOURNAMENT,
    *,
    include_parked: bool = False,
) -> list[tuple[FreeParameterDef, float, float, float]]:
    """Return (def, impact, constrainingability, importance) high → low."""
    rows: list[tuple[FreeParameterDef, float, float, float]] = []
    for d in CATALOG:
        if d.live_only and mode != RunMode.LIVE:
            if not include_parked:
                continue
        imp = course_impact(d, course_type)
        c = d.base_constrainingability
        rows.append((d, imp, c, imp * c))
    rows.sort(key=lambda r: r[3], reverse=True)
    return rows


def top_open_questions(
    course_type: CourseType,
    unconstrained_ids: set[str],
    n: int = 5,
) -> list[str]:
    ranked = ranked_parameters(course_type)
    out: list[str] = []
    for d, _imp, _c, impn in ranked:
        if d.factor_id in unconstrained_ids:
            out.append(f"{d.name} still open (importance {impn:.2f})")
        if len(out) >= n:
            break
    return out
