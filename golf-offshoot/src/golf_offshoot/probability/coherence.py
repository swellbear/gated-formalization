"""Probability helpers (horizon labels, coherence checks)."""

from golf_offshoot.models.enums import Horizon
from golf_offshoot.models.schemas import ProbabilityBundle

CHAIN = (Horizon.WIN, Horizon.TOP_5, Horizon.TOP_10, Horizon.TOP_20, Horizon.MAKE_CUT)


def is_coherent(bundle: ProbabilityBundle, tol: float = 0.02) -> bool:
    prev = 0.0
    for h in CHAIN:
        p = bundle.p(h).central
        if p + tol < prev:
            return False
        prev = p
    return prev <= 1.0 + tol
