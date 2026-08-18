from datetime import date

from golf_offshoot.operator_hints import (
    is_empty_field,
    pinned_event_hint,
    pre_thursday_opening_warning,
)


def test_pinned_settled_names_current_week():
    note = pinned_event_hint(
        "401811962",
        settled=True,
        current=("401811963", "BMW Championship"),
        lookup=False,
    )
    assert note == "this event is settled (museum). this week is BMW Championship 401811963"


def test_pinned_unsettled_wrong_week():
    note = pinned_event_hint(
        "401811962",
        settled=False,
        current=("401811963", "BMW Championship"),
        lookup=False,
    )
    assert note == (
        "pinned 401811962 is not ESPN's current week. this week is BMW Championship 401811963"
    )


def test_pin_matching_current_week_is_quiet_unless_settled():
    assert (
        pinned_event_hint(
            "401811963",
            settled=False,
            current=("401811963", "BMW Championship"),
            lookup=False,
        )
        is None
    )
    assert (
        pinned_event_hint(
            "401811963",
            settled=True,
            current=("401811963", "BMW Championship"),
            lookup=False,
        )
        == "this event is settled (museum)."
    )


def test_pre_thursday_opening_warning():
    warn = pre_thursday_opening_warning(
        "2026-08-20",
        0,
        today=date(2026, 8, 17),
    )
    assert warn is not None
    assert "2026-08-20" in warn
    assert "pre-Thursday" in warn
    assert "Bovada" in warn
    poly = pre_thursday_opening_warning(
        "2026-08-20",
        0,
        today=date(2026, 8, 17),
        odds_book="polymarket",
    )
    assert poly is not None
    assert "Polymarket" in poly
    assert "Bovada" not in poly
    assert pre_thursday_opening_warning("2026-08-20", 12, today=date(2026, 8, 17)) is None
    assert pre_thursday_opening_warning("2026-08-20", 0, today=date(2026, 8, 20)) is None


def test_empty_field():
    assert is_empty_field([]) is True
    assert is_empty_field(None) is True
    assert is_empty_field([object()]) is False
