"""Single selector field: lane=golf|learning_lane_15m. Default golf. Owned by operator_surface."""

from __future__ import annotations

from typing import Any

from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF

DEFAULT_LANE = LANE_GOLF
SELECTOR_FIELD = "lane"
CANONICAL_LANES = (LANE_GOLF, LANE_15M)


def parse_lane(raw: Any) -> str:
    """Exact `golf` | `learning_lane_15m` only. Unknown or `15m` → golf."""
    key = str(raw or "").strip()
    if key == LANE_15M:
        return LANE_15M
    return LANE_GOLF


def lane_header_name(lane: str) -> str:
    if parse_lane(lane) == LANE_15M:
        return "15-min Kalshi (learning)"
    return "Golf Phase 1"


def lane_journal_label(lane: str) -> str:
    """Visual journal name. Not a selector alias."""
    return "15m" if parse_lane(lane) == LANE_15M else "golf"


def parse_lane_from_mapping(mapping: Any) -> str:
    """Read the single `lane` field from a query/form mapping."""
    if mapping is None:
        return DEFAULT_LANE
    if hasattr(mapping, "get"):
        return parse_lane(mapping.get(SELECTOR_FIELD))
    return DEFAULT_LANE
