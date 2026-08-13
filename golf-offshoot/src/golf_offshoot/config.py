"""Default model version, cut rules, and tunable constants.

Weights here are **expert-initialized priors for later calibration**, not
claimed-optimal. Bayesian optimization + ARD is supported by the learning loop
but is not required to run a tournament.
"""

from __future__ import annotations

MODEL_VERSION = "golf-offshoot-0.2.0"
MODEL_FAMILY = "latent-skill-plackett-mc"

# Tournament structure
DEFAULT_ROUNDS = 4
DEFAULT_CUT_PLACE = 65  # plus ties after round 2
DEFAULT_CUT_AFTER_ROUND = 2
DEFAULT_FIELD_SIZE_HINT = 156

# Monte Carlo
DEFAULT_N_SIMS = 4000
DEFAULT_RNG_SEED = 20260813

# Residual score noise (strokes per round around latent skill)
DEFAULT_ROUND_SIGMA = 2.35

# Evidence: weak quality must not move θ as much as strong quality
MIN_QUALITY_TO_UPDATE = 0.05
NARRATIVE_ABS_CAP = 0.35  # max |Δθ| from narrative momentum
THIN_SAMPLE_N = 4  # course-history rounds below this → borrow / flag

# Reliability
RELIABILITY_QUALITY_WEIGHT = 0.45
RELIABILITY_DENSITY_WEIGHT = 0.35
RELIABILITY_STABILITY_WEIGHT = 0.20

# Decision layer (never auto-bet)
MIN_EDGE_TO_CONSIDER = 0.03
MAX_RANGE_WIDTH_TO_CONSIDER = 0.18  # on win-prob scale
MIN_RELIABILITY_TO_CONSIDER = 0.45
MAX_PORTFOLIO_CORR_TO_STACK = 0.72
KELLY_FRACTION_CAP = 0.25  # of a full Kelly; suggestion only

# Strategy layer — conservative defaults; never auto-bet
STRATEGY_MAX_DAILY_LOSS_FRAC = 0.05
STRATEGY_MAX_TOTAL_EXPOSURE_FRAC = 0.20
STRATEGY_COOLING_OFF_DRAWDOWN_FRAC = 0.08
STRATEGY_MAX_SINGLE_POSITION_FRAC = 0.05
STRATEGY_MAX_CUT_RISK_CONCENTRATION = 0.40
STRATEGY_MAX_STYLE_CLUSTER_FRAC = 0.50
STRATEGY_RUNNER_PNL_FRAC = 0.25  # unrealized / stake
STRATEGY_EDGE_COLLAPSE_RATIO = 0.30
STRATEGY_EDGE_IMPROVE_ABS = 0.015
STRATEGY_WIDE_RANGE_BLOCK = 0.18
STRATEGY_LOW_RELIABILITY_BLOCK = 0.40

# Market
DEFAULT_OVERROUND_METHOD = "proportional"

# Live
LIVE_POSITION_WEIGHT = 1.0  # remaining-round MC still uses residual σ
