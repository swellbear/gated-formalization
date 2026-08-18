import numpy as np

from golf_offshoot.bayesian_engine.simulate import SimConfig, simulate_field
from golf_offshoot.models.enums import Horizon
from golf_offshoot.probability.coherence import is_coherent


def test_win_probs_sum_near_one():
    n = 12
    ids = [f"p{i:02d}" for i in range(n)]
    mean = np.linspace(1.2, -0.4, n)
    sd = np.full(n, 0.35)
    bundles = simulate_field(ids, mean, sd, config=SimConfig(n_sims=800, seed=1, cut_place=6))
    s = sum(b.p(Horizon.WIN).central for b in bundles.values())
    assert 0.85 < s < 1.15


def test_lead_after_round1_is_not_tournament_win():
    n = 10
    ids = [f"p{i:02d}" for i in range(n)]
    mean = np.linspace(1.2, -0.4, n)
    sd = np.full(n, 0.35)
    bundles = simulate_field(ids, mean, sd, config=SimConfig(n_sims=800, seed=3, cut_place=6))
    r1 = [b.p(Horizon.WIN_AFTER_R1).central for b in bundles.values()]
    assert all(0.0 <= p <= 1.0 for p in r1)
    assert 0.85 < sum(r1) < n
    favorite = bundles["p00"].p(Horizon.WIN_AFTER_R1).central
    longshot = bundles["p09"].p(Horizon.WIN_AFTER_R1).central
    assert favorite > longshot
    assert bundles["p00"].p(Horizon.WIN_AFTER_R1).central != bundles["p00"].p(Horizon.WIN).central


def test_horizons_coherent():
    n = 10
    ids = [f"p{i:02d}" for i in range(n)]
    mean = np.linspace(1.0, 0.0, n)
    sd = np.full(n, 0.3)
    bundles = simulate_field(ids, mean, sd, config=SimConfig(n_sims=600, seed=2, cut_place=5))
    for b in bundles.values():
        assert is_coherent(b, tol=0.03)
        w = b.p(Horizon.WIN)
        assert w.low <= w.central <= w.high
