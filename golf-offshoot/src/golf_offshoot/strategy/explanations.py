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


def win_proxy_stack() -> str:
    return "Already holding Win, R2 leader, or R3 leader on this player"


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


def pre_tee_hold() -> str:
    return "Tournament has not started; quote drift is not a sell"


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


def flip_heat_new() -> str:
    return (
        "Flip heat: chance this card's early model % clears ask plus spread. "
        "Small Yes, not hold-to-settle, one flip per player"
    )


def flip_take_pop() -> str:
    return "Take the pop: offer still clears fill plus 20% on a following live run"


def flip_hurdle_armed() -> str:
    return "Flip hurdle is green this live; confirm still green on the next live run"


def flip_failed() -> str:
    return (
        "Flip failed: this card's hole clock ran out and fill plus 20% never "
        "cleared; exit at bid"
    )


def flip_dead() -> str:
    return "Flip is dead (WD or missed cut) after a board mark; exit at bid"


def flip_waiting_fill() -> str:
    return "Flip sleeve waiting for a paper-fill; quote drift is not a sell"


def flip_hold() -> str:
    return "Flip sleeve: offer has not cleared fill plus 20%; not keep-to-win"
