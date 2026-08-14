"""Free-parameter board: start broad, constrain where evidence allows."""

from __future__ import annotations

from golf_offshoot.config import MIN_QUALITY_TO_UPDATE, THIN_SAMPLE_N
from golf_offshoot.free_parameters.catalog import CATALOG, CATALOG_BY_ID
from golf_offshoot.free_parameters.ranking import importance, ranked_parameters
from golf_offshoot.models.enums import CourseType, FactorStatus, RunMode, SourceKind
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
    sq = player.source_qualities

    def q(
        score: float,
        source: str,
        n: int,
        missing: bool = False,
        kind: SourceKind = SourceKind.UNSPECIFIED,
        factor_id: str | None = None,
    ) -> DataQuality:
        from datetime import datetime, timezone

        if factor_id and factor_id in sq:
            return sq[factor_id]
        return DataQuality(
            score=score,
            source_name=source,
            as_of=datetime.now(timezone.utc),
            n_observations=n,
            missing=missing,
            source_kind=kind,
        )

    seeds: dict[str, tuple[float, DataQuality]] = {}
    seeds["talent_prior"] = (
        player.talent_prior,
        q(
            0.85 if not player.player.is_lesser_known else 0.45,
            "talent_model",
            40,
            kind=SourceKind.UNSPECIFIED,
            factor_id="talent_prior",
        ),
    )
    if player.course_fit_signal is not None:
        seeds["course_fit"] = (
            player.course_fit_signal,
            q(0.55, "course_fit", max(player.course_history_rounds, 1), factor_id="course_fit"),
        )
    if player.course_history_sg is not None:
        seeds["course_history"] = (
            player.course_history_sg,
            q(
                min(0.9, 0.25 + 0.08 * player.course_history_rounds),
                "course_history",
                player.course_history_rounds,
                missing=player.course_history_rounds == 0,
                factor_id="course_history",
            ),
        )
    recent_sg = player.recent_sg
    recent_sg_ok = (
        recent_sg is not None
        and recent_sg.quality is not None
        and not recent_sg.quality.missing
    )
    if recent_sg_ok:
        # True as-of EVENT_ONLY (or Data Golf) window. Do not blend with finish residuals.
        seeds["recent_form"] = (float(recent_sg.total), recent_sg.quality)
    elif player.recent_form_sg is not None:
        seeds["recent_form"] = (player.recent_form_sg, q(0.70, "recent_sg", 8, factor_id="recent_form"))
    if player.short_term_trend is not None:
        seeds["short_term_trend"] = (player.short_term_trend, q(0.55, "trend", 4, factor_id="short_term_trend"))
    if player.weather_fit is not None:
        seeds["weather_suitability"] = (
            player.weather_fit,
            q(0.50, "weather_splits", 6, factor_id="weather_suitability"),
        )
    health_q = sq.get("health_setup")
    if health_q is not None or player.health_flag != 0:
        seeds["health_setup"] = (
            player.health_flag,
            health_q
            or q(
                0.35 if player.health_flag != 0 else 0.20,
                "injury_notes",
                1,
                missing=player.health_flag == 0,
            ),
        )
    if abs(player.narrative_momentum) > 0 or "narrative_momentum" in sq:
        seeds["narrative_momentum"] = (
            player.narrative_momentum,
            q(0.25, "narrative", 1, factor_id="narrative_momentum"),
        )
    sg_q = player.sg.quality
    sg_real = sg_q is not None and not sg_q.missing
    if sg_real:
        seeds["sg_match"] = (player.sg.total, sg_q)
        seeds["approach_sg"] = (player.sg.app, sg_q)
        seeds["around_green"] = (player.sg.arg, sg_q)
    putting_q = sq.get("putting") or (sg_q if sg_real else None)
    if putting_q is not None and not putting_q.missing and (sg_real or player.sg.putt != 0.0 or "putting" in sq):
        seeds["putting"] = (player.sg.putt, putting_q if putting_q else sg_q)
    dist_q = sq.get("driving_distance") or (sg_q if sg_real else None)
    if player.sg.driving_distance_yd is not None and dist_q is not None and not dist_q.missing:
        seeds["driving_distance"] = (
            ((player.sg.driving_distance_yd or 295) - 295) / 12.0,
            dist_q,
        )
    acc_q = sq.get("driving_accuracy") or (sg_q if sg_real else None)
    if player.sg.driving_accuracy_pct is not None and acc_q is not None and not acc_q.missing:
        seeds["driving_accuracy"] = (
            ((player.sg.driving_accuracy_pct or 60) - 60) / 8.0,
            acc_q,
        )

    if player.live_score_to_par is not None and mode == RunMode.LIVE:
        from golf_offshoot.bayesian_engine.live_dampen import live_position_evidence

        ev, prog = live_position_evidence(
            player.live_score_to_par,
            player.live_holes_completed,
        )
        live_q = sq.get("live_position")
        note = (
            f"dampen={prog['dampen']:.4f} tournament_frac={prog['tournament_frac']:.3f} "
            f"holes={int(prog['holes'])}/{int(prog['total_holes'])}"
        )
        if live_q is not None:
            live_q = live_q.model_copy(
                update={
                    "score": float(prog["quality"]),
                    "n_observations": max(int(prog["holes"]), 1),
                    "notes": (live_q.notes + "; " + note).strip("; "),
                }
            )
        else:
            from datetime import datetime, timezone

            live_q = DataQuality(
                score=float(prog["quality"]),
                source_name="espn_leaderboard_live",
                as_of=datetime.now(timezone.utc),
                n_observations=max(int(prog["holes"]), 1),
                notes=note,
                source_kind=SourceKind.REAL_LIVE,
            )
        seeds["live_position"] = (ev, live_q)

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
