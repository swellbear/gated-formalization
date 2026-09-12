"""YES-or-skip. Never buy NO."""

from __future__ import annotations

from golf_offshoot.honer_15m.policy import FAMILY_SPREAD, FAMILY_THIN


def posted_mark(market: dict) -> float | None:
    mark = market.get("paper_mark")
    if mark is None:
        mark = market.get("yes_ask")
    try:
        yes_f = float(mark) if mark is not None else None
    except (TypeError, ValueError):
        return None
    if yes_f is None or yes_f <= 0.0 or yes_f >= 1.0:
        return None
    return yes_f


def market_spread(market: dict) -> float | None:
    try:
        bid = market.get("yes_bid")
        ask = market.get("yes_ask")
        if bid is None or ask is None:
            return None
        spread = float(ask) - float(bid)
    except (TypeError, ValueError):
        return None
    if spread < 0:
        return None
    return spread


def decide_yes_or_skip(posted_yes: float, theta: float) -> tuple[str, str]:
    if float(posted_yes) >= float(theta):
        return "skip", f"posted_yes >= theta {theta:g}"
    return "fill", f"posted_yes below theta {theta:g}"


def decide_ticket(
    posted_yes: float,
    theta: float,
    *,
    family: str,
    delta: float,
    spread: float | None,
    gamma: float = 0.0,
) -> tuple[str, str]:
    """Skip gates are family-named. Missing bid/ask is thin-book, not a wide-spread skip. Never buy NO."""
    if str(family) == FAMILY_THIN:
        if spread is None:
            return "skip", "thin quotes missing bid/ask"
        if float(spread) <= float(gamma):
            return "skip", f"spread {spread:g} <= gamma {gamma:g}"
        return decide_yes_or_skip(posted_yes, theta)
    if str(family) == FAMILY_SPREAD and spread is not None and float(spread) >= float(delta):
        return "skip", f"spread {spread:g} >= delta {delta:g}"
    return decide_yes_or_skip(posted_yes, theta)
