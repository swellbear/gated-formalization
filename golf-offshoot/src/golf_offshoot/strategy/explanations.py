"""Canonical plain-language reasons for strategy actions."""

from __future__ import annotations

from golf_offshoot.models.strategy import PositionMark


def collapsed() -> str:
    return "Original edge has collapsed"


def live_improved() -> str:
    return "Live probability improved after Round 1"


def live_improved_generic() -> str:
    return "Live probability improved since entry"


def concentrated_cut() -> str:
    return "Exposure too concentrated in cut-risk players"


def range_too_wide() -> str:
    return "Range still too wide to justify adding"


def reliability_low() -> str:
    return "Reliability too low to justify adding"


def runner_lock() -> str:
    return "Position has already run strongly in your favor — lock some of it"


def cooling_off() -> str:
    return "Cooling-off after sharp drawdown — no new risk"


def exposure_cap() -> str:
    return "Total exposure at the configured limit"


def fresh_edge() -> str:
    return "Fresh model-vs-market edge that is not already in the book"


def hold_edge_intact() -> str:
    return "Original edge is still intact; no path reason to change size"


def unmarked_ride_to_settle() -> str:
    return (
        "No live posted coupon for this market; edge cannot be marked. "
        "Riding to official settle. Not a cash-out."
    )


def cashout_beats_hold() -> str:
    return (
        "Quoted cash-out beats remaining winner EV; take the quote rather than "
        "ride for the full payout"
    )


def cashout_below_hold() -> str:
    return (
        "Quoted cash-out is below remaining winner EV; hold the ticket rather "
        "than sell early"
    )


def selective_not_strong() -> str:
    return "Stay Selective: remaining edge is not strong enough to act"


def noisy_inputs(mark: PositionMark | None = None) -> str:
    if mark and mark.reliability < 0.45:
        return "Strong uncertainty: recommendation rests on still-noisy inputs"
    return "Strong uncertainty: inputs are still noisy"
