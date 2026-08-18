"""Default model version, cut rules, and tunable constants.

Weights here are **expert-initialized priors for later calibration**, not
claimed-optimal. Bayesian optimization + ARD is supported by the learning loop
but is not required to run a tournament.
"""

from __future__ import annotations

MODEL_VERSION = "golf-offshoot-0.7.0"
MODEL_FAMILY = "latent-skill-plackett-mc"
CALIBRATED_WEIGHTS_VERSION = "calib-v3"

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
# End-of-round leader is not Winner. Floor / scale of posted Yes; cap is Winner 3pp.
ROUND_LEADER_EDGE_FLOOR = {
    "win_after_r1": 0.015,
    "win_after_r2": 0.020,
    "win_after_r3": 0.025,
}
ROUND_LEADER_EDGE_SCALE = {
    "win_after_r1": 0.25,
    "win_after_r2": 0.30,
    "win_after_r3": 0.35,
}
ROUND_LEADER_RANGE_WIDTH = {
    "win_after_r1": 0.28,
    "win_after_r2": 0.24,
    "win_after_r3": 0.20,
}
ROUND_LEADER_SIZE_FRAC = {
    "win_after_r1": 0.35,
    "win_after_r2": 0.55,
    "win_after_r3": 0.75,
}

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
# User-typed cash-out must beat remaining win EV by this fraction (Stay Selective).
STRATEGY_CASHOUT_BUFFER_FRAC = 0.10
# Flip sleeve on listed Yes (Win / R1 / R2 / R3 / place if quoted).
# Display leftover P(); NEW if P clears. Sell at fill * hurdle if still green next live.
FLIP_HURDLE = 1.20
FLIP_NEW_MIN_P = 0.20
FLIP_SIZE_FRAC = 0.25  # of the Winner unit
FLIP_MAX_STAKE_FRAC = 0.01  # of bankroll
FLIP_NEW_MAX = 3  # per listed market, including open flip fills
FLIP_NEW_MAX_TOTAL = 6  # open flips on the book, not 6 new names every live
FLIP_HEAT_N_SIMS = 2000
# Paper lock: names that fail the 3pp posted screen but still have +posted_edge.
PAPER_OBSERVATION_STAKE_FRAC = 0.25
# Paper reduce/exit without a typed Open Bets quote: keep this fraction of the
# odds-ratio MTM gap (benefit or penalty). Labeled estimated; never scraped.
PAPER_ESTIMATED_CASHOUT_HAIRCUT = 0.20

# Market
DEFAULT_OVERROUND_METHOD = "proportional"
ODDS_TTL_PRE_SECONDS = 600.0  # 10 min — pre-tournament coupon
ODDS_TTL_LIVE_SECONDS = 45.0  # live pass must not reuse a stale Winner coupon
ODDS_LIVE_MAX_STALE_SECONDS = 900.0  # 15 min: older than this → edges suppressed

# Live: remaining-holes MC banks observed to-par; live_position evidence is
# hole-dampened so Round-1 boards cannot dominate θ.
LIVE_POSITION_WEIGHT = 1.0

# True as-of recent SG: mean of PGA EVENT_ONLY tables for the last N completed
# events before the tournament start. Not inferred from season-to-date.
# Missing weeks are skipped, not zero-filled; N is a request, not a guarantee.
RECENT_SG_EVENTS = 16
RECENT_SG_MIN_EVENTS = 1
RECENT_SG_PILL_YEARS = 3  # StatDetails pills for year, year-1, year-2
HISTORY_YEARS = (2025, 2026)
CALIB_HISTORY_YEARS = (2024, 2025, 2026)

# Recalibrate only if the as-of panel is materially stronger than calib-v2
# (median 3 measured EVENT_ONLY events/player on the 8-week window).
PREV_CALIB_MEDIAN_RECENT_EVENTS = 3
PREV_CALIB_RECENT_COVERAGE = 0.742
CALIB_MATERIAL_MEDIAN_EVENTS = 5
CALIB_MATERIAL_COVERAGE = 0.85
