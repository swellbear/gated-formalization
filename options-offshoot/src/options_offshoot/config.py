"""Tunable constants. Nerves (t) stay frozen until a named holdout."""

from __future__ import annotations

MODEL_VERSION = "options-offshoot-0.1.0"
DEFAULT_N_SIMS = 2000
DEFAULT_RNG_SEED = 20260816
DEFAULT_SIGMA = 0.20  # A/current fill only; honest path does not use this
MIN_EDGE_TO_CONSIDER = 0.03  # dollars of premium: model fair minus ask (or mid)
MIN_OPEN_INTEREST = 100
MIN_VOLUME = 0
MAX_SPREAD_REL = 0.25  # (ask-bid)/mid; wider → n/a
MIN_RELIABILITY = 0.45
MAX_RANGE_WIDTH = 0.50  # on P(ITM) scale; wider blocks tickets
PAPER_DIR = "data/paper"
EXPORT_DIR = "data/exports"
SNAPSHOT_DIR = "data/snapshots"
CACHE_DIR = "data/cache"
FIELDS_DIR = "data/fields"
