import numpy as np

from golf_offshoot.bayesian_engine.simulate import SimConfig, simulate_field
from golf_offshoot.models.enums import Horizon


def test_no_cut_everyone_makes_except_withdrawn():
    n = 8
    ids = [f"p{i}" for i in range(n)]
    mean = np.linspace(1.0, -0.2, n)
    sd = np.full(n, 0.3)
    wd = np.zeros(n, dtype=bool)
    wd[7] = True
    bundles = simulate_field(
        ids,
        mean,
        sd,
        withdrawn=wd,
        config=SimConfig(n_sims=400, seed=4, cut_place=n, cut_after=0),
    )
    for i, pid in enumerate(ids):
        p_cut = bundles[pid].p(Horizon.MAKE_CUT).central
        if i == 7:
            assert p_cut == 0.0
        else:
            assert p_cut > 0.95
        w = bundles[pid].p(Horizon.WIN)
        t5 = bundles[pid].p(Horizon.TOP_5)
        assert w.central <= t5.central + 1e-9
        assert t5.central <= bundles[pid].p(Horizon.MAKE_CUT).central + 1e-9
