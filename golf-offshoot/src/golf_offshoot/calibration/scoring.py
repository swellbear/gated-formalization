"""Fast scoring for calibration. Same θ update as production; fewer MC draws."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.calibration.dataset import EventDataset
from golf_offshoot.free_parameters.board import build_player_board
from golf_offshoot.learning.loop import brier, logloss
from golf_offshoot.models.enums import Horizon, RunMode


HORIZONS = (
    Horizon.MAKE_CUT,
    Horizon.TOP_20,
    Horizon.TOP_10,
    Horizon.TOP_5,
    Horizon.WIN,
)


@dataclass
class HorizonMetrics:
    brier: dict[str, float]
    logloss: dict[str, float]
    n: int


def _y(res, h: Horizon) -> bool:
    if h == Horizon.WIN:
        return res.won
    if h == Horizon.TOP_5:
        return res.top_5
    if h == Horizon.TOP_10:
        return res.top_10
    if h == Horizon.TOP_20:
        return res.top_20
    return res.made_cut


def score_event(
    ds: EventDataset,
    engine: BayesianEngine,
    *,
    n_sims: int = 250,
    seed: int = 7,
) -> HorizonMetrics:
    from golf_offshoot.clustering.similars import apply_player_borrow, comparable_borrows
    from golf_offshoot.field_effects.interaction import apply_field_interactions

    field = ds.field.model_copy(deep=True)
    borrows = comparable_borrows(field.players)
    apply_player_borrow(field.players, borrows)
    for p in field.players:
        p.factors = build_player_board(p, ds.tournament.course.course_type, RunMode.PRE_TOURNAMENT)
    apply_field_interactions(field.players, ds.tournament.course)
    engine.sim = SimConfig(n_sims=n_sims, seed=seed, round_sigma=engine.sim.round_sigma)
    bundles, _thetas, _warn = engine.run(ds.tournament, field)
    by_res = {r.player_id: r for r in ds.results}
    bsum = {h.value: [] for h in HORIZONS}
    lsum = {h.value: [] for h in HORIZONS}
    n = 0
    for pid, bundle in bundles.items():
        res = by_res.get(pid)
        if not res:
            continue
        n += 1
        for h in HORIZONS:
            p = bundle.p(h).central
            y = _y(res, h)
            bsum[h.value].append(brier(p, y))
            lsum[h.value].append(logloss(p, y))
    return HorizonMetrics(
        brier={k: float(np.mean(v)) if v else 1.0 for k, v in bsum.items()},
        logloss={k: float(np.mean(v)) if v else 10.0 for k, v in lsum.items()},
        n=n,
    )


def aggregate(metrics: list[HorizonMetrics]) -> HorizonMetrics:
    if not metrics:
        return HorizonMetrics(brier={h.value: 1.0 for h in HORIZONS}, logloss={h.value: 10.0 for h in HORIZONS}, n=0)
    b = {h.value: float(np.mean([m.brier[h.value] for m in metrics])) for h in HORIZONS}
    l = {h.value: float(np.mean([m.logloss[h.value] for m in metrics])) for h in HORIZONS}
    return HorizonMetrics(brier=b, logloss=l, n=sum(m.n for m in metrics))


def scalar_loss(m: HorizonMetrics) -> float:
    """Proper scoring mix. Win weighted slightly higher; all five horizons count."""
    b = m.brier
    l = m.logloss
    brier_mean = float(np.mean([b[h.value] for h in HORIZONS]))
    log_mean = float(np.mean([l[h.value] for h in HORIZONS]))
    return brier_mean + 0.15 * log_mean + 0.25 * b[Horizon.WIN.value]
