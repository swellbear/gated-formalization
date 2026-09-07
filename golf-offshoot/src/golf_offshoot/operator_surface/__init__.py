"""Phase 1 operator surface. Observation only. Never auto-bets. Never moves cash."""

from golf_offshoot.operator_surface.modes import (
    CASH_BADGE,
    MODE_MOCK,
    MODE_OPERATING,
    ModeWalls,
    build_mode_walls,
    is_mock_or_demo_text,
)

__all__ = [
    "CASH_BADGE",
    "MODE_MOCK",
    "MODE_OPERATING",
    "ModeWalls",
    "build_mode_walls",
    "is_mock_or_demo_text",
]
