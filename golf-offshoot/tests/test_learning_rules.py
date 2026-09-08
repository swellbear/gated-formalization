from golf_offshoot.learning_lane_15m.rules import decide, load_rules, window_is_oos


def test_registry_has_dated_first_rules():
    payload = load_rules()
    ids = [row["id"] for row in payload["rules"]]
    assert ids == ["R-BASELINE-FILL-ALL", "R-SKIP-COINFLIP"]
    assert payload["lab_admits"] is False
    assert payload["trials_to_date"] == 0
    assert payload["evidence_bar"]["binding"] is False
    skip = next(row for row in payload["rules"] if row["id"] == "R-SKIP-COINFLIP")
    assert skip["declared_at"] == "2026-09-08T05:56:00-04:00"
    assert skip["execution"] is False


def test_predeclaration_window_is_not_oos():
    rule = {
        "id": "R-SKIP-COINFLIP",
        "declared_at": "2026-09-08T05:56:00-04:00",
        "kind": "selection",
    }
    assert window_is_oos(rule, close_at="2026-09-08T05:45:00-04:00") is False
    assert window_is_oos(rule, close_at="2026-09-08T06:00:00-04:00") is True


def test_skip_coinflip_expresses_skip_and_fill():
    rule = {
        "id": "R-SKIP-COINFLIP",
        "declared_at": "2026-09-08T05:56:00-04:00",
        "kind": "selection",
        "selects": True,
        "execution": False,
    }
    skip = decide(rule, posted_yes=0.50, close_at="2026-09-08T06:15:00-04:00")
    assert skip["eligible"] is True
    assert skip["action"] == "skip"
    assert skip["execution"] is False
    fill = decide(rule, posted_yes=0.62, close_at="2026-09-08T06:15:00-04:00")
    assert fill["action"] == "fill"
    historic = decide(rule, posted_yes=0.50, close_at="2026-09-08T02:45:00-04:00")
    assert historic["eligible"] is False
    assert historic["action"] == "ineligible"
