"""Duration sleeves inside one golf wallet. Not extra tabs. Not a 15m n-count."""

from __future__ import annotations

from typing import Any

SLEEVES = ("fast", "week", "slow")

_FAST_TOKENS = (
    "round leader",
    "round 1 leader",
    "round 2 leader",
    "round 3 leader",
    "end of round",
    "after round 1",
    "after round 2",
    "after round 3",
    "leader after",
    "thru ",
    "same day",
    "today",
    "r1 leader",
    "r2 leader",
    "r3 leader",
)
_SLOW_TOKENS = (
    "season",
    "fedex cup",
    "fedex",
    "race to dubai",
    "this year",
    "this season",
    "win a major",
    "major this year",
    "outright 2026",
    "outright 2027",
    "annual",
    "player of the year",
    "captain",
    "ryder",
    "presidents cup",
    "2027",
)


def classify_sleeve(market: dict[str, Any] | None = None, *, title: str = "") -> str:
    blob = " ".join(
        [
            title,
            str((market or {}).get("title") or ""),
            str((market or {}).get("event_title") or ""),
            str((market or {}).get("yes_sub_title") or ""),
        ]
    ).lower()
    if any(tok in blob for tok in _SLOW_TOKENS):
        return "slow"
    if any(tok in blob for tok in _FAST_TOKENS):
        return "fast"
    return "week"


def market_horizon(market: dict[str, Any] | None = None, *, title: str = "") -> str:
    blob = " ".join(
        [
            title,
            str((market or {}).get("title") or ""),
            str((market or {}).get("event_title") or ""),
            str((market or {}).get("yes_sub_title") or ""),
        ]
    ).lower()
    if any(tok in blob for tok in _SLOW_TOKENS):
        return "season"
    if "make the cut" in blob or "make cut" in blob or "made cut" in blob:
        return "make_cut"
    if "top 5" in blob or "top five" in blob:
        return "top_5"
    if "top 10" in blob or "top ten" in blob:
        return "top_10"
    if "top 20" in blob or "top twenty" in blob:
        return "top_20"
    if "round 1" in blob or "after round 1" in blob or "r1 leader" in blob:
        return "win_after_r1"
    if "round 2" in blob or "after round 2" in blob or "r2 leader" in blob:
        return "win_after_r2"
    if "round 3" in blob or "after round 3" in blob or "r3 leader" in blob:
        return "win_after_r3"
    if "win" in blob or "winner" in blob or "outright" in blob:
        return "win"
    return "win"
