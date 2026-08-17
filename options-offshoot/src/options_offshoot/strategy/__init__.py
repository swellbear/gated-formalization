"""Strategy advice. Never auto-trades."""

from options_offshoot.strategy.engine import format_advice, recommend
from options_offshoot.strategy.paper_book import advice_for_book, lock_paper_positions

__all__ = ["recommend", "format_advice", "advice_for_book", "lock_paper_positions"]
