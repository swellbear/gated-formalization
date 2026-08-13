"""Optional advisory Decision Layer + Dynamic Strategy System.

Never places bets. Disable via StrategyConfig.enabled=False for pure analysis.
"""

from golf_offshoot.strategy.engine import (
    disabled_recommendation,
    format_recommendation,
    record_user_decision,
    run_strategy,
)

__all__ = [
    "disabled_recommendation",
    "format_recommendation",
    "record_user_decision",
    "run_strategy",
]
