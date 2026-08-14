"""Market coverage report. Winner vs place markets stay separate; never synthesized."""

from __future__ import annotations

from golf_offshoot.market.odds import is_current_quote
from golf_offshoot.models.enums import BetType
from golf_offshoot.models.schemas import MarketQuote

_ALL = (BetType.WIN, BetType.TOP_5, BetType.TOP_10, BetType.TOP_20, BetType.MAKE_CUT)


def market_coverage_report(
    quotes: list[MarketQuote],
    n_field: int,
    *,
    synthesized: bool = False,
) -> dict:
    """Counts of real coupons only. `synthesized` must stay False on the operating path."""
    by_type: dict[str, int] = {bt.value: 0 for bt in _ALL}
    books: dict[str, set[str]] = {bt.value: set() for bt in _ALL}
    as_of: dict[str, str | None] = {bt.value: None for bt in _ALL}
    opening_n = sum(1 for q in quotes if not is_current_quote(q))
    for q in quotes:
        if not is_current_quote(q):
            continue
        key = q.bet_type.value
        if key not in by_type:
            by_type[key] = 0
            books[key] = set()
            as_of[key] = None
        by_type[key] += 1
        if q.book:
            books.setdefault(key, set()).add(q.book)
        if q.as_of and (as_of.get(key) is None or str(q.as_of) > str(as_of[key])):
            as_of[key] = q.as_of.isoformat()
    available = [k for k, n in by_type.items() if n > 0]
    unavailable = [k for k, n in by_type.items() if n == 0]
    return {
        "field_size": n_field,
        "synthesized": synthesized,
        "by_market": {
            k: {
                "n": n,
                "available": n > 0,
                "coverage": f"{n}/{n_field}" if n_field else f"{n}",
                "books": sorted(books.get(k) or []),
                "as_of": as_of.get(k),
            }
            for k, n in by_type.items()
        },
        "available_markets": available,
        "unavailable_markets": unavailable,
        "opening_quotes": opening_n,
        "opening_available": opening_n > 0,
        "notes": (
            "Place/top-10 ingested only when the source coupon lists them. "
            "Winner odds are never converted into place prices. "
            "Opening lines counted only when a distinct prematch coupon exists "
            "alongside the current (usually live) price."
        ),
    }
