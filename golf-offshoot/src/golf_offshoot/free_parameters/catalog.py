"""Standard golf free-parameter catalog.

Start broad, then constrain. Course type rescales impact. Importance =
impact × constrainingability after that rescale.

The eight required families are present; additional structural factors
are included so the board is comprehensive rather than a slogan list.
"""

from __future__ import annotations

from golf_offshoot.models.enums import CourseType
from golf_offshoot.models.schemas import FreeParameterDef

_CT = {c.value: 1.0 for c in CourseType}


def _m(**overrides: float) -> dict[str, float]:
    out = dict(_CT)
    out.update(overrides)
    return out


# Course-type keys use enum values.
CATALOG: list[FreeParameterDef] = [
    FreeParameterDef(
        factor_id="talent_prior",
        name="Long-term talent / prior",
        description="Stable skill from multi-year results (OWGR / SG-total baseline).",
        family="prior",
        base_impact=0.95,
        base_constrainingability=0.80,
        course_multipliers=_m(major_setup=1.05),
        correlated_with=["sg_match", "approach_sg"],
    ),
    FreeParameterDef(
        factor_id="course_fit",
        name="Course fit",
        description="How the player's game matches this layout (history + style).",
        family="venue",
        base_impact=0.78,
        base_constrainingability=0.55,
        course_multipliers=_m(links=1.15, desert=1.10, major_setup=1.20, mountain=1.10),
        correlated_with=["sg_match", "venue_cluster_borrow", "course_history"],
    ),
    FreeParameterDef(
        factor_id="recent_form",
        name="Recent form",
        description="Strokes-gained / finishes over a recent window (e.g. 5–12 starts).",
        family="form",
        base_impact=0.70,
        base_constrainingability=0.62,
        course_multipliers=_m(),
        correlated_with=["short_term_trend", "sg_match"],
    ),
    FreeParameterDef(
        factor_id="short_term_trend",
        name="Short-term trend",
        description="Direction of form (improving vs fading), distinct from level.",
        family="form",
        base_impact=0.48,
        base_constrainingability=0.40,
        course_multipliers=_m(),
        correlated_with=["recent_form"],
    ),
    FreeParameterDef(
        factor_id="sg_match",
        name="Strokes-gained match",
        description="SG category mix vs what this course historically rewards.",
        family="skill_mix",
        base_impact=0.82,
        base_constrainingability=0.58,
        course_multipliers=_m(links=1.12, parkland=1.05, stadium=1.08, major_setup=1.15),
        correlated_with=["approach_sg", "driving_accuracy", "putting", "course_fit"],
    ),
    FreeParameterDef(
        factor_id="weather_suitability",
        name="Weather suitability",
        description="Wind, rain, temperature, altitude vs player's observed weather splits.",
        family="conditions",
        base_impact=0.58,
        base_constrainingability=0.42,
        course_multipliers=_m(links=1.35, mountain=1.20, tropical=1.15, heathland=1.18),
        correlated_with=["wind_history"],
    ),
    FreeParameterDef(
        factor_id="health_setup",
        name="Health / setup notes",
        description="Injury, equipment, coach, withdrawal risk. Often low quality.",
        family="status",
        base_impact=0.65,
        base_constrainingability=0.28,
        course_multipliers=_m(),
        correlated_with=["narrative_momentum"],
    ),
    FreeParameterDef(
        factor_id="narrative_momentum",
        name="Constrained narrative momentum",
        description="Media/hot-hand story. Hard-capped so it cannot dominate talent or SG.",
        family="narrative",
        base_impact=0.22,
        base_constrainingability=0.18,
        course_multipliers=_m(),
        correlated_with=["recent_form", "health_setup"],
        narrative_capped=True,
    ),
    FreeParameterDef(
        factor_id="course_history",
        name="This-course / this-event history",
        description="Player's own rounds at this venue. Thin samples borrow from cluster.",
        family="venue",
        base_impact=0.60,
        base_constrainingability=0.50,
        course_multipliers=_m(major_setup=1.10),
        correlated_with=["course_fit", "venue_cluster_borrow"],
    ),
    FreeParameterDef(
        factor_id="driving_distance",
        name="Driving distance",
        description="Length vs course yardage; crowding-adjusted in field-interaction layer.",
        family="skill_mix",
        base_impact=0.55,
        base_constrainingability=0.70,
        course_multipliers=_m(mountain=1.20, desert=1.10, parkland=0.95, links=0.85, major_setup=0.80),
        correlated_with=["sg_match"],
    ),
    FreeParameterDef(
        factor_id="driving_accuracy",
        name="Driving accuracy",
        description="Fairways / missed-fairway penalty vs tightness and rough.",
        family="skill_mix",
        base_impact=0.58,
        base_constrainingability=0.68,
        course_multipliers=_m(major_setup=1.30, parkland=1.15, desert=1.20, links=1.05, stadium=0.90),
        correlated_with=["sg_match", "bogey_avoidance"],
    ),
    FreeParameterDef(
        factor_id="approach_sg",
        name="Approach (SG:APP)",
        description="Iron play / proximity — usually a large share of scoring.",
        family="skill_mix",
        base_impact=0.80,
        base_constrainingability=0.72,
        course_multipliers=_m(parkland=1.10, stadium=1.12, major_setup=1.08),
        correlated_with=["sg_match", "talent_prior"],
    ),
    FreeParameterDef(
        factor_id="around_green",
        name="Around the green",
        description="SG:ARG / short-game when missing greens is likely.",
        family="skill_mix",
        base_impact=0.50,
        base_constrainingability=0.60,
        course_multipliers=_m(links=1.20, heathland=1.15, major_setup=1.18),
        correlated_with=["scrambling", "sg_match"],
    ),
    FreeParameterDef(
        factor_id="putting",
        name="Putting",
        description="SG:PUTT. High variance; quality of recent putting sample matters.",
        family="skill_mix",
        base_impact=0.52,
        base_constrainingability=0.45,
        course_multipliers=_m(stadium=1.15, tropical=1.10),
        correlated_with=["sg_match", "recent_form"],
    ),
    FreeParameterDef(
        factor_id="scrambling",
        name="Scrambling / bogey avoidance mix",
        description="Save rate when off-plan; related to ARG + putting under pressure.",
        family="skill_mix",
        base_impact=0.42,
        base_constrainingability=0.48,
        course_multipliers=_m(major_setup=1.22, links=1.12),
        correlated_with=["around_green", "bogey_avoidance"],
    ),
    FreeParameterDef(
        factor_id="bogey_avoidance",
        name="Bogey avoidance",
        description="Mistake suppression on severe setups.",
        family="skill_mix",
        base_impact=0.50,
        base_constrainingability=0.50,
        course_multipliers=_m(major_setup=1.35, parkland=1.05),
        correlated_with=["driving_accuracy", "scrambling"],
    ),
    FreeParameterDef(
        factor_id="par5_scoring",
        name="Par-5 scoring",
        description="Birdie/eagle rate on par 5s vs field; more load on long courses.",
        family="skill_mix",
        base_impact=0.38,
        base_constrainingability=0.55,
        course_multipliers=_m(desert=1.10, mountain=1.12, major_setup=0.90),
        correlated_with=["driving_distance"],
    ),
    FreeParameterDef(
        factor_id="wind_history",
        name="Wind / firm-and-fast splits",
        description="Observed performance in wind above a threshold.",
        family="conditions",
        base_impact=0.44,
        base_constrainingability=0.35,
        course_multipliers=_m(links=1.40, heathland=1.22, mountain=1.10),
        correlated_with=["weather_suitability"],
    ),
    FreeParameterDef(
        factor_id="rest_travel",
        name="Rest / travel / schedule",
        description="Fatigue, transoceanic travel, consecutive starts.",
        family="status",
        base_impact=0.28,
        base_constrainingability=0.40,
        course_multipliers=_m(),
        correlated_with=["health_setup"],
    ),
    FreeParameterDef(
        factor_id="comparable_player_borrow",
        name="Comparable-player borrowed strength",
        description="When own sample is thin, shrink toward similar-player means.",
        family="borrow",
        base_impact=0.40,
        base_constrainingability=0.35,
        course_multipliers=_m(),
        correlated_with=["course_fit", "sg_match"],
    ),
    FreeParameterDef(
        factor_id="venue_cluster_borrow",
        name="Venue-cluster borrowed strength",
        description="Similar-course cluster history when this tee sheet is new-ish.",
        family="borrow",
        base_impact=0.42,
        base_constrainingability=0.38,
        course_multipliers=_m(major_setup=0.85),
        correlated_with=["course_fit", "course_history"],
    ),
    FreeParameterDef(
        factor_id="field_interaction",
        name="Field-composition relative value",
        description="Player traits vs this week's field mix (not a global strength add-on).",
        family="field",
        base_impact=0.45,
        base_constrainingability=0.40,
        course_multipliers=_m(),
        correlated_with=["driving_distance", "putting", "sg_match"],
    ),
    FreeParameterDef(
        factor_id="live_position",
        name="Live scoring position",
        description="In-tournament: current score, holes left, cut status.",
        family="live",
        base_impact=0.90,
        base_constrainingability=0.85,
        course_multipliers=_m(),
        live_only=True,
        start_broad=False,
    ),
    FreeParameterDef(
        factor_id="live_tee_pairing",
        name="Live tee time / pairing",
        description="Wave, weather window, pairing difficulty. Live or late pre-tee.",
        family="live",
        base_impact=0.25,
        base_constrainingability=0.30,
        course_multipliers=_m(links=1.15),
        live_only=True,
    ),
]


REQUIRED_FACTOR_IDS = (
    "talent_prior",
    "course_fit",
    "recent_form",
    "short_term_trend",
    "sg_match",
    "weather_suitability",
    "health_setup",
    "narrative_momentum",
)

CATALOG_BY_ID: dict[str, FreeParameterDef] = {d.factor_id: d for d in CATALOG}


def get_def(factor_id: str) -> FreeParameterDef:
    return CATALOG_BY_ID[factor_id]
