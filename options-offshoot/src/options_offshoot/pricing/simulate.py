"""v1 terminal-spot Monte Carlo. Provisional. Not a vol surface."""

from __future__ import annotations

import math
from datetime import date

import numpy as np

from options_offshoot.config import DEFAULT_N_SIMS, DEFAULT_RNG_SEED, DEFAULT_SIGMA
from options_offshoot.models.enums import ContractType
from options_offshoot.models.schemas import Contract, ModelView


def years_to_expiry(expiry: date, today: date) -> float:
    days = (expiry - today).days
    return max(days, 1) / 365.0


def simulate_view(
    contract: Contract,
    *,
    honest: bool,
    n_sims: int = DEFAULT_N_SIMS,
    seed: int = DEFAULT_RNG_SEED,
    today: date | None = None,
) -> ModelView:
    t = contract.years_to_expiry
    if t is None:
        t = years_to_expiry(contract.expiry, today or contract.expiry)
    spot = contract.spot
    sigma = contract.realized_vol
    unconstrained = sigma is None or sigma <= 0
    if unconstrained:
        if honest:
            return ModelView(
                fair=None,
                p_itm=None,
                p_itm_low=None,
                p_itm_high=None,
                reliability=0.25,
                honest=True,
                sigma_used=None,
                unconstrained_vol=True,
            )
        sigma = DEFAULT_SIGMA
    if spot is None or spot <= 0 or t <= 0:
        return ModelView(
            fair=None,
            p_itm=None,
            p_itm_low=None,
            p_itm_high=None,
            reliability=0.20,
            honest=honest,
            sigma_used=sigma,
            unconstrained_vol=unconstrained,
        )
    extra = sum(ord(ch) for ch in contract.contract_id) % 10_000
    rng = np.random.default_rng(seed + extra)
    # risk-neutral-ish: rate 0 for v1
    z = rng.standard_normal(n_sims)
    terminal = spot * np.exp((-0.5 * sigma * sigma) * t + sigma * math.sqrt(t) * z)
    k = contract.strike
    if contract.contract_type == ContractType.CALL:
        payoff = np.maximum(terminal - k, 0.0)
        itm = terminal > k
    else:
        payoff = np.maximum(k - terminal, 0.0)
        itm = terminal < k
    fair = float(payoff.mean())
    p = float(itm.mean())
    n_blocks = 10
    block = n_sims // n_blocks
    cents = []
    for b in range(n_blocks):
        sl = itm[b * block : (b + 1) * block]
        cents.append(float(sl.mean()))
    lo = float(np.percentile(cents, 10))
    hi = float(np.percentile(cents, 90))
    lo, hi = min(lo, p), max(hi, p)
    rel = 0.72 if not unconstrained else 0.40
    if honest and unconstrained:
        rel = 0.25
    return ModelView(
        fair=fair,
        p_itm=p,
        p_itm_low=max(0.0, lo),
        p_itm_high=min(1.0, hi),
        reliability=rel,
        honest=honest,
        sigma_used=float(sigma) if sigma is not None else None,
        unconstrained_vol=unconstrained,
    )
