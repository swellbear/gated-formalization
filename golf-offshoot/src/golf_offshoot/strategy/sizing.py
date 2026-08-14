"""Uncertainty-aware unit sizing. Suggestions only — never a ticket."""

from __future__ import annotations

from golf_offshoot.config import (
    STRATEGY_LOW_RELIABILITY_BLOCK,
    STRATEGY_WIDE_RANGE_BLOCK,
)
from golf_offshoot.decision.layer import fractional_kelly
from golf_offshoot.models.enums import RiskPreference, StrategyMode
from golf_offshoot.models.strategy import StrategyConfig


_RISK_SIZE = {
    RiskPreference.CONSERVATIVE: 0.40,
    RiskPreference.NORMAL: 0.70,
    RiskPreference.AGGRESSIVE: 1.00,
}

_MODE_SIZE = {
    StrategyMode.PROTECT_PROFITS: 0.55,
    StrategyMode.STAY_SELECTIVE: 0.70,
    StrategyMode.PRESS_EDGES: 1.00,
}

_RISK_EXPOSURE = {
    RiskPreference.CONSERVATIVE: 0.70,
    RiskPreference.NORMAL: 1.00,
    RiskPreference.AGGRESSIVE: 1.30,
}


def sizing_probability(central: float, low: float, risk: RiskPreference) -> float:
    """Haircut central toward the low end of the range. Conservative haircuts more."""
    span = max(0.0, central - low)
    frac = {
        RiskPreference.CONSERVATIVE: 0.65,
        RiskPreference.NORMAL: 0.45,
        RiskPreference.AGGRESSIVE: 0.25,
    }[risk]
    return float(max(0.0, min(1.0, central - frac * span)))


def uncertainty_blocks_action(range_width: float, reliability: float) -> str | None:
    if range_width > STRATEGY_WIDE_RANGE_BLOCK:
        return "Range still too wide to justify adding"
    if reliability < STRATEGY_LOW_RELIABILITY_BLOCK:
        return "Reliability too low to justify adding"
    return None


def suggested_stake(
    *,
    bankroll: float,
    model_p: float,
    low_p: float,
    decimal_odds: float,
    range_width: float,
    reliability: float,
    config: StrategyConfig,
    remaining_capacity: float,
) -> tuple[float, str | None]:
    """Return (stake, block_reason). Stake is 0 if blocked or tiny."""
    warn = uncertainty_blocks_action(range_width, reliability)
    if warn and config.mode != StrategyMode.PRESS_EDGES:
        return 0.0, warn
    p = sizing_probability(model_p, low_p, config.risk)
    kelly = fractional_kelly(p, decimal_odds, fraction=0.25)
    if kelly <= 0:
        return 0.0, "No positive Kelly after uncertainty haircut"
    haircut = max(0.15, 1.0 - min(0.85, range_width / max(STRATEGY_WIDE_RANGE_BLOCK, 1e-6)))
    rel_m = max(0.20, reliability)
    if warn and config.mode == StrategyMode.PRESS_EDGES:
        haircut *= 0.45
        rel_m *= 0.70
    raw = (
        bankroll
        * kelly
        * haircut
        * rel_m
        * _RISK_SIZE[config.risk]
        * _MODE_SIZE[config.mode]
    )
    cap = bankroll * scaled_single_cap(config)
    stake = min(raw, cap, max(0.0, remaining_capacity))
    min_unit = 0.002 * bankroll
    if kelly > 0 and 0 < stake < min_unit:
        # Conservative haircuts can crush a real posted-price edge into dust.
        # Keep a minimum advisory unit so CONSIDER does not silently vanish.
        return float(min(min_unit, max(0.0, remaining_capacity))), (
            "Kelly is tiny after uncertainty haircut; sized to minimum advisory unit"
        )
    if stake < min_unit:
        return 0.0, "Suggested size rounds to essentially zero"
    return float(stake), warn


def scaled_exposure_cap(config: StrategyConfig) -> float:
    return config.controls.max_total_exposure_frac * _RISK_EXPOSURE[config.risk]


def scaled_single_cap(config: StrategyConfig) -> float:
    return config.controls.max_single_position_frac * _RISK_EXPOSURE[config.risk]


def scaled_cut_cap(config: StrategyConfig) -> float:
    base = config.controls.max_cut_risk_concentration
    if config.mode == StrategyMode.PROTECT_PROFITS:
        return base * 0.85
    if config.mode == StrategyMode.PRESS_EDGES:
        return min(0.70, base * 1.15)
    return base


def remaining_exposure_capacity(open_exposure: float, bankroll: float, config: StrategyConfig) -> float:
    cap = bankroll * scaled_exposure_cap(config)
    return float(max(0.0, cap - open_exposure))
