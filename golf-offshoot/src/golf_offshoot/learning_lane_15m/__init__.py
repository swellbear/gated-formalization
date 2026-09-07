"""15-min Kalshi learning lane (KXBTC15M). Paper observation only.

Not a golf sidecar. Golf θ / artifacts stay primary for golf Amb.
Trading is never armed. AI never deposit / withdraw / transfer.
"""

from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    LANE_GOLF,
    LANE_NAME,
    PRIMARY_SERIES,
    artifact_root_15m,
    golf_data_root,
)
from golf_offshoot.learning_lane_15m.series_registry import (
    SHIPPED_SERIES,
    SeriesSpec,
    register_series,
    require_shipped_series,
)

__all__ = [
    "LANE_15M",
    "LANE_GOLF",
    "LANE_NAME",
    "PRIMARY_SERIES",
    "SHIPPED_SERIES",
    "SeriesSpec",
    "artifact_root_15m",
    "golf_data_root",
    "register_series",
    "require_shipped_series",
]
