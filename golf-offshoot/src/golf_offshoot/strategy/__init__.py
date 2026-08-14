"""Optional advisory Decision Layer + Dynamic Strategy System.

Never places bets. Disable via StrategyConfig.enabled=False for pure analysis.
"""

from golf_offshoot.strategy.engine import (
    disabled_recommendation,
    format_recommendation,
    record_user_decision,
    run_strategy,
)
from golf_offshoot.strategy.paper_reports import (
    format_paper_reports,
    load_portfolio_json,
    paper_reports_payload,
    recorded_positions,
    save_portfolio_json,
)

__all__ = [
    "disabled_recommendation",
    "format_paper_reports",
    "format_recommendation",
    "load_portfolio_json",
    "paper_reports_payload",
    "record_user_decision",
    "recorded_positions",
    "run_strategy",
    "save_portfolio_json",
]
