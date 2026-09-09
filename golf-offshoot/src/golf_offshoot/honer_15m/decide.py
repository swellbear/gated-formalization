"""YES-or-skip. Never buy NO."""

from __future__ import annotations


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


def decide_yes_or_skip(posted_yes: float, theta: float) -> tuple[str, str]:
    if float(posted_yes) >= float(theta):
        return "skip", f"posted_yes >= theta {theta:g}"
    return "fill", f"posted_yes below theta {theta:g}"
