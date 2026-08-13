"""Orchestrate prior → evidence updates → MC probabilities."""

from __future__ import annotations

import numpy as np

from golf_offshoot.bayesian_engine.decompose import (
    attach_decomposition,
    decompose_win_range,
    scenario_thetas,
    softmax_win_share,
)
from golf_offshoot.bayesian_engine.simulate import SimConfig, simulate_field
from golf_offshoot.bayesian_engine.updates import ThetaState, update_theta
from golf_offshoot.bayesian_engine.weights import complete_alpha
from golf_offshoot.free_parameters.board import unconstrained_ids
from golf_offshoot.free_parameters.ranking import ranked_parameters
from golf_offshoot.models.enums import Horizon, RunMode
from golf_offshoot.models.schemas import FieldSnapshot, PlayerInputs, ProbabilityBundle, Tournament


class BayesianEngine:
    def __init__(
        self,
        alpha: dict[str, float] | None = None,
        ard_scale: dict[str, float] | None = None,
        sim: SimConfig | None = None,
    ) -> None:
        self.alpha = complete_alpha(alpha)
        self.ard_scale = ard_scale or {}
        self.sim = sim or SimConfig()

    def player_theta(self, player: PlayerInputs) -> ThetaState:
        return update_theta(
            player.talent_prior,
            player.talent_prior_sd,
            player.factors,
            self.alpha,
            self.ard_scale,
        )

    def run(
        self,
        tournament: Tournament,
        field: FieldSnapshot,
    ) -> tuple[dict[str, ProbabilityBundle], dict[str, ThetaState], list[str]]:
        players = [p for p in field.players if not p.withdrawn]
        warnings: list[str] = []
        if not players:
            return {}, {}, ["empty field"]

        ids = [p.player.player_id for p in players]
        thetas: dict[str, ThetaState] = {}
        means = np.zeros(len(players))
        sds = np.zeros(len(players))
        wd = np.zeros(len(players), dtype=bool)
        live_score = np.zeros(len(players))
        live_holes = np.zeros(len(players))
        has_live = field.mode == RunMode.LIVE

        for i, p in enumerate(players):
            if not p.factors:
                warnings.append(f"{p.player.player_id}: empty factor board")
            st = self.player_theta(p)
            thetas[p.player.player_id] = st
            means[i] = st.mean
            sds[i] = st.sd
            wd[i] = p.withdrawn
            if p.live_score_to_par is not None:
                live_score[i] = p.live_score_to_par
                live_holes[i] = p.live_holes_completed

        cfg = SimConfig(
            n_sims=self.sim.n_sims,
            n_rounds=tournament.n_rounds,
            cut_place=min(tournament.cut_place, max(len(players) // 2, 1)),
            cut_after=tournament.cut_after_round,
            round_sigma=self.sim.round_sigma,
            seed=self.sim.seed,
        )
        bundles = simulate_field(
            ids,
            means,
            sds,
            withdrawn=wd,
            live_score=live_score if has_live else None,
            live_holes=live_holes if has_live else None,
            config=cfg,
        )

        # Decomposition + scenarios for top importance unconstrained factors
        course_type = tournament.course.course_type
        major = [
            d.factor_id
            for d, *_ in ranked_parameters(course_type, field.mode)[:6]
        ]
        boards = [p.factors for p in players]
        priors = [(p.talent_prior, p.talent_prior_sd) for p in players]
        shares: dict[str, dict[str, float]] = {}
        opt_p: dict[str, dict[str, float]] = {}
        pes_p: dict[str, dict[str, float]] = {}
        field_theta = means.copy()
        for i, p in enumerate(players):
            pid = p.player.player_id
            try:
                shares[pid] = decompose_win_range(i, boards, priors, self.alpha, field_theta)
            except Exception as exc:  # pragma: no cover - defensive
                warnings.append(f"decompose {pid}: {exc}")
                shares[pid] = {}
            open_major = [fid for fid in major if fid in unconstrained_ids(p.factors)]
            if not open_major:
                open_major = major[:3]
            base, opt, pes = scenario_thetas(
                p.factors, p.talent_prior, p.talent_prior_sd, self.alpha, open_major
            )
            # map Δθ to Δwin via softmax perturbation
            t = field_theta.copy()
            t[i] = opt.mean
            opt_share = float(softmax_win_share(t)[i])
            t[i] = pes.mean
            pes_share = float(softmax_win_share(t)[i])
            win = bundles[pid].p(Horizon.WIN).central
            opt_p[pid] = {Horizon.WIN.value: float(max(win, opt_share))}
            pes_p[pid] = {Horizon.WIN.value: float(min(win, pes_share))}

        attach_decomposition(bundles, shares, opt_p, pes_p)
        return bundles, thetas, warnings
