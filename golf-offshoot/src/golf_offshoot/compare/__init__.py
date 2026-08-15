"""Parallel A/B ranking+strategy. Method law steers B. Never mutates lived paper."""

from golf_offshoot.compare.law import METHOD_LAW_V1, law_hash, learner_may_move_t
from golf_offshoot.compare.paths import (
    ComparePath,
    allowed_compare_bets,
    compare_allows_place,
    config_for,
    ledger_id,
)

__all__ = [
    "ComparePath",
    "METHOD_LAW_V1",
    "allowed_compare_bets",
    "compare_allows_place",
    "law_hash",
    "learner_may_move_t",
    "config_for",
    "ledger_id",
]
