"""Free-parameter board: start broad, constrain where evidence allows."""

from __future__ import annotations

from golf_offshoot.config import MIN_QUALITY_TO_UPDATE, THIN_SAMPLE_N
from golf_offshoot.free_parameters.catalog import CATALOG, CATALOG_BY_ID
from golf_offshoot.free_parameters.ranking import importance, ranked_parameters
from golf_offshoot.models.enums import CourseType, FactorStatus, RunMode
from golf_offshoot.models.schemas import (
    DataQuality,
    FreeParameterState,
    PlayerInputs,
)


def _status_from_evidence(
    n_obs: int,
    quality_score: float,
    live_only: bool,
    mode: RunMode,
) -> FactorStatus:
    if live_only and mode != RunMode.LIVE:
        return FactorStatus.PARKED
    if quality_score < MIN_QUALITY_TO_UPDATE or n_obs <= 0:
        return FactorStatus.UNCONSTRAINED
    if n_obs < THIN_SAMPLE_N or quality_score < 0.45:
        return FactorStatus.PARTIALLY_CONSTRAINED
    return FactorStatus.CONSTRAINED


def build_player_board(
    player: PlayerInputs,
    course_type: CourseType,
    mode: RunMode = RunMode.PRE_TOURNAMENT,
) -> dict[str, FreeParameterState]:
    """Fill or refresh factor states from raw player inputs. Start broad."""
    board: dict[str, FreeParameterState] = dict(player.factors)

    def q(score: float, source: str, n: int, missing: bool = False) -> DataQuality:
        from datetime import datetime, timezone

        return DataQuality(
            score=score,
            source_name=source,
            as_of=datetime.now(timezone.utc),
            n_observations=n,
            missing=missing,
        )

    seeds: dict[str, tuple[float, DataQuality]] = {}
    seeds["talent_prior"] = (
        player.talent_prior,
        q(0.85 if not player.player.is_lesser_known else 0.45, "talent_model", 40),
    )
    if player.course_history_sg is not None:
        seeds["course_history"] = (
            player.course_history_sg,
            q(
                min(0.9, 0.25 + 0.08 * player.course_history_rounds),
                "course_history",
                player.course_history_rounds,
                missing=player.course_history_rounds == 0,
            ),
        )
    if player.recent_form_sg is not None:
        seeds["recent_form"] = (player.recent_form_sg, q(0.70, "recent_sg", 8))
    if player.short_term_trend is not None:
        seeds["short_term_trend"] = (player.short_term_trend, q(0.55, "trend", 4))
    if player.weather_fit is not None:
        seeds["weather_suitability"] = (player.weather_fit, q(0.50, "weather_splits", 6))
    seeds["health_setup"] = (
        player.health_flag,
        q(0.35 if player.health_flag != 0 else 0.20, "injury_notes", 1, missing=player.health_flag == 0),
    )
    seeds["narrative_momentum"] = (
        player.narrative_momentum,
        q(0.25, "narrative", 1),
    )
    if player.sg.quality:
        seeds["sg_match"] = (player.sg.total, player.sg.quality)
        seeds["approach_sg"] = (player.sg.app, player.sg.quality)
        seeds["putting"] = (player.sg.putt, player.sg.quality)
        seeds["around_green"] = (player.sg.arg, player.sg.quality)
        seeds["driving_distance"] = (
            ((player.sg.driving_distance_yd or 295) - 295) / 12.0,
            player.sg.quality,
        )
        seeds["driving_accuracy"] = (
            ((player.sg.driving_accuracy_pct or 60) - 60) / 8.0,
            player.sg.quality,
        )

    if player.live_score_to_par is not None and mode == RunMode.LIVE:
        seeds["live_position"] = (
            -player.live_score_to_par / 3.0,
            q(0.95, "live_scoreboard", player.live_holes_completed or 1),
        )

    for d in CATALOG:
        existing = board.get(d.factor_id)
        if d.factor_id in seeds:
            std, quality = seeds[d.factor_id]
            n = quality.n_observations
            st = _status_from_evidence(n, quality.score, d.live_only, mode)
            board[d.factor_id] = FreeParameterState(
                factor_id=d.factor_id,
                status=st,
                standardized_evidence=float(std),
                quality=quality,
                n_obs=n,
                importance=importance(d, course_type),
                open_question="" if st == FactorStatus.CONSTRAINED else f"{d.name} not fully pinned",
                notes=existing.notes if existing else "",
            )
        elif existing:
            existing.importance = importance(d, course_type)
            if d.live_only and mode != RunMode.LIVE:
                existing.status = FactorStatus.PARKED
            board[d.factor_id] = existing
        else:
            st = FactorStatus.PARKED if (d.live_only and mode != RunMode.LIVE) else FactorStatus.UNCONSTRAINED
            board[d.factor_id] = FreeParameterState(
                factor_id=d.factor_id,
                status=st,
                importance=importance(d, course_type),
                open_question=f"{d.name} unconstrained at start",
            )
    return board


def unconstrained_ids(board: dict[str, FreeParameterState]) -> set[str]:
    return {
        k
        for k, v in board.items()
        if v.status in (FactorStatus.UNCONSTRAINED, FactorStatus.PARTIALLY_CONSTRAINED)
    }


def board_summary(course_type: CourseType, mode: RunMode) -> list[dict]:
    rows = []
    for d, imp, c, impn in ranked_parameters(course_type, mode):
        rows.append(
            {
                "factor_id": d.factor_id,
                "name": d.name,
                "family": d.family,
                "impact": round(imp, 3),
                "constrainingability": round(c, 3),
                "importance": round(impn, 3),
                "live_only": d.live_only,
                "narrative_capped": d.narrative_capped,
            }
        )
    return rows
