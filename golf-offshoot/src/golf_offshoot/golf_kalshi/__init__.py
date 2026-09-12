"""Kalshi golf ingest island. Own artifact root. Trading NOT ARMED.

Harvested (catalog/matcher/paths) from gym branch ``cursor/golf-kalshi-gym``
via ``git show``. Not a merge of that branch. No paper, watch, hub tab, or
Pages ``lane_id``.
"""

from golf_offshoot.golf_kalshi.paths import LANE, set_golf_kalshi_root_override

TRADING_ARMED = False

__all__ = ["LANE", "TRADING_ARMED", "set_golf_kalshi_root_override"]
