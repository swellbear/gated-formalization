"""Single selector field: lane=golf|learning_lane_15m. Default golf. Owned by operator_surface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF

DEFAULT_LANE = LANE_GOLF
SELECTOR_FIELD = "lane"
CANONICAL_LANES = (LANE_GOLF, LANE_15M)


@dataclass(frozen=True)
class LaneSpec:
    id: str
    display_name: str
    views: tuple[str, ...]
    session_fields: tuple[str, ...]
    blotter_columns: tuple[str, ...]
    meters: tuple[str, ...] = ()
    organs: tuple[str, ...] = ()


LANE_REGISTRY: tuple[LaneSpec, ...] = (
    LaneSpec(
        id=LANE_GOLF,
        display_name="Golf (Kalshi)",
        views=("home", "scoreboard", "ops", "farm", "honer", "museum"),
        session_fields=("watch", "clock", "bankroll", "pnl", "fees", "open", "closed", "halt"),
        blotter_columns=("player", "market", "sleeve", "stake", "quote", "live_entry_edge", "status"),
        meters=("fast", "week", "slow"),
        organs=("farm", "honer", "museum"),
    ),
    LaneSpec(
        id=LANE_15M,
        display_name="15-min Kalshi (learning)",
        views=("home", "scoreboard", "lab", "ops", "farm", "honer"),
        session_fields=("watch", "clock", "bankroll", "pnl", "open", "halt"),
        blotter_columns=("window", "factory", "honer_search", "honer_exam", "kalshi"),
        organs=("farm", "honer"),
    ),
)

VIEW_LABELS = {
    "home": "Home",
    "scoreboard": "Scoreboard",
    "lab": "Lab",
    "ops": "Ops",
    "farm": "Farm",
    "honer": "Honer",
    "museum": "Museum",
}


def registered_lanes() -> tuple[LaneSpec, ...]:
    return LANE_REGISTRY


def lookup_lane(lane_id: str) -> LaneSpec | None:
    key = str(lane_id or "").strip()
    for spec in LANE_REGISTRY:
        if spec.id == key:
            return spec
    return None


def registered_ids() -> frozenset[str]:
    return frozenset(spec.id for spec in LANE_REGISTRY)


def desk_lane_from_query(raw: Any) -> str | None:
    """Registered desk id, or None for an explicit unknown id.

    Omitted/blank is not this helper — callers default to golf. Watches still use parse_lane.
    """
    key = str(raw or "").strip()
    if not key:
        return DEFAULT_LANE
    spec = lookup_lane(key)
    return spec.id if spec is not None else None


def parse_lane(raw: Any) -> str:
    """Canonical selector only: `golf` | `learning_lane_15m`. Unknown (incl. bare `15m`) → golf."""
    key = str(raw or "").strip()
    if key == LANE_15M:
        return LANE_15M
    return LANE_GOLF


def lane_header_name(lane: str) -> str:
    spec = lookup_lane(parse_lane(lane))
    if spec is not None:
        return spec.display_name
    if parse_lane(lane) == LANE_15M:
        return "15-min Kalshi (learning)"
    return "Golf (Kalshi)"


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
