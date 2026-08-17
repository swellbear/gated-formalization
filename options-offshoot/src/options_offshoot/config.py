"""Tunable constants. Nerves (t) stay frozen until a named holdout."""

from __future__ import annotations

MODEL_VERSION = "options-offshoot-0.2.0"
DEFAULT_N_SIMS = 2000
DEFAULT_RNG_SEED = 20260816
DEFAULT_SIGMA = 0.20  # A/current fill only; honest path does not use this
MIN_EDGE_TO_CONSIDER = 0.03  # dollars of premium: model fair minus ask (or mid)
MIN_OPEN_INTEREST = 100
MIN_VOLUME = 0
MAX_SPREAD_REL = 0.25  # (ask-bid)/mid; wider → n/a
MIN_RELIABILITY = 0.45
MAX_RANGE_WIDTH = 0.50  # on P(ITM) scale; wider blocks tickets
DEFAULT_MULTIPLIER = 100
PAPER_DIR = "data/paper"
EXPORT_DIR = "data/exports"
SNAPSHOT_DIR = "data/snapshots"
CACHE_DIR = "data/cache"
FIELDS_DIR = "data/fields"

# HTTP cache
TTL_LIVE_S = 45.0
TTL_INGEST_S = 600.0
TTL_VOL_S = 6.0 * 3600.0
TTL_META_S = 600.0
MAX_STALE_QUOTE_S = 15.0 * 60.0
UNDERLYING_PAUSE_S = 0.25
HTTP_429_RETRIES = 3

# Snapshot pagination
MAX_SNAPSHOT_PAGES = 40

# Strategy caps (law; conservative Stay Selective). Not Kelly.
MAX_SINGLE_POSITION_FRAC = 0.05
MAX_SAME_UNDERLYING_FRAC = 0.10
MAX_TOTAL_EXPOSURE_FRAC = 0.40
CONSERVATIVE_HAIRCUT = 0.70
STAY_SELECTIVE_CASHOUT_BUFFER = 0.10
PRESS_CASHOUT_BUFFER = 0.20
RUNNER_MTM_FRAC = 1.25
COLLAPSE_FAIR_FRAC = 0.30

# IBKR market data only
IBKR_HOST_DEFAULT = "127.0.0.1"
IBKR_PORT_DEFAULT = 7497
IBKR_CLIENT_ID_DEFAULT = 17
