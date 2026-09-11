import json

import pytest

from golf_offshoot.learning_lane_15m.evidence_bar import class_is_burned, load_mechanism_catalog
from golf_offshoot.learning_lane_15m.paper import load_decisions, paper_autobet_open_markets
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.rules import (
    RuleAlreadyInformed,
    RuleNotScorable,
    RuleSkipRateUnnamed,
    RuleTooSparse,
    close_minute,
    decide,
    declare_rule,
    expected_skip_rate,
    favorite_threshold,
    load_rules,
    min_expected_skip_rate,
    score_rule,
    selects_on_posted_yes_cut,
    window_is_lived,
    window_is_oos,
    window_is_replay,
)


def test_registry_has_dated_first_rules():
    payload = load_rules()
    ids = [row["id"] for row in payload["rules"]]
    assert ids == [
        "R-BASELINE-FILL-ALL",
        "R-SKIP-COINFLIP",
        "R-SKIP-2TO1-FAVORITE",
        "R-SKIP-HOUR-CLOSE",
    ]
    assert payload["lab_admits"] is False
    assert payload["trials_to_date"] == 2
    assert payload["evidence_bar"]["binding"] is False
    skip = next(row for row in payload["rules"] if row["id"] == "R-SKIP-COINFLIP")
    assert skip["declared_at"] == "2026-09-08T05:56:00-04:00"
    assert skip["execution"] is False
    fav = next(row for row in payload["rules"] if row["id"] == "R-SKIP-2TO1-FAVORITE")
    assert fav["execution"] is False
    assert fav["selects"] is True
    assert fav["params"]["favorite_odds"] == 2
    hour = next(row for row in payload["rules"] if row["id"] == "R-SKIP-HOUR-CLOSE")
    assert hour["execution"] is True
    assert hour["selects"] is True
    assert hour["params"]["skip_close_minute"] == 0
    assert hour["declared_at"] == "2026-09-10T13:25:00-04:00"
    log = payload["trials_log"]
    assert len(log) == 2
    assert log[0]["subject"] == "R-SKIP-2TO1-FAVORITE"
    assert log[0]["kind"] == "declaration"
    assert log[1]["subject"] == "R-SKIP-HOUR-CLOSE"
    assert log[1]["kind"] == "declaration"


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


def test_a_skip_rule_produces_no_fill_in_band_and_fills_out_of_band(tmp_path, monkeypatch):
    from golf_offshoot.data_feeds.kalshi_15m import parse_event, parse_market
    from golf_offshoot.learning_lane_15m.paper import iter_books

    event = {
        "event_ticker": "KXBTC15M-26SEP071400",
        "series_ticker": "KXBTC15M",
        "title": "BTC 15 min",
        "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
    }
    open_raw = {
        "ticker": "KXBTC15M-26SEP071415-15",
        "event_ticker": "KXBTC15M-26SEP071415",
        "status": "active",
        "result": "",
        "yes_ask_dollars": "0.5000",
        "yes_bid_dollars": "0.4800",
        "title": "BTC price up in next 15 mins?",
    }

    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        rule = {
            "id": "R-SKIP-COINFLIP",
            "declared_at": "2026-09-08T05:56:00-04:00",
            "kind": "selection",
            "selects": True,
            "execution": True,
        }
        in_band = parse_market(open_raw, event=parse_event(event))
        out_band = parse_market(
            {**open_raw, "ticker": "KXBTC15M-26SEP071430-30", "yes_ask_dollars": "0.6200"},
            event=parse_event(event),
        )
        skipped = paper_autobet_open_markets([in_band], rule=rule)
        filled = paper_autobet_open_markets([out_band], rule=rule)
        decisions = load_decisions()
        assert skipped == []
        assert decisions[in_band["ticker"]]["action"] == "skip"
        assert decisions[in_band["ticker"]]["rule_id"] == "R-SKIP-COINFLIP"
        assert len(filled) == 1
        assert decisions[out_band["ticker"]]["action"] == "fill"
        assert decisions[out_band["ticker"]]["rule_id"] == "R-SKIP-COINFLIP"
        books = iter_books()
        tickers = [p.player_id for b in books for p in b.book.positions]
        assert in_band["ticker"] not in tickers
        assert out_band["ticker"] in tickers
    finally:
        set_15m_root_override(None)


def test_two_to_one_favorite_is_burned_after_l1_falsifier():
    assert class_is_burned("SKIP-2TO1-FAVORITE") is True
    assert class_is_burned("R-SKIP-2TO1-FAVORITE") is True
    assert class_is_burned("RETUNE-COINFLIP-BAND") is True
    assert class_is_burned("FEE-AS-SIGNAL") is True
    assert class_is_burned("SKIP-HOUR-CLOSE") is False
    assert class_is_burned("R-SKIP-HOUR-CLOSE") is False
    assert class_is_burned("RETUNE-CLOCK-MINUTE") is True
    assert class_is_burned("retune-skip-close-minute") is True
    assert class_is_burned("SEAS-DIR") is True


def test_hour_close_expresses_skip_and_fill():
    assert close_minute("2026-09-10T13:00:00-04:00") == 0
    assert close_minute("2026-09-10T13:15:00-04:00") == 15
    rule = {
        "id": "R-SKIP-HOUR-CLOSE",
        "declared_at": "2026-09-10T13:25:00-04:00",
        "kind": "selection",
        "selects": True,
        "execution": False,
        "params": {"skip_close_minute": 0},
        "expression": {"skip_if": "close_minute_eq"},
    }
    assert selects_on_posted_yes_cut(rule) is False
    skip = decide(rule, posted_yes=0.50, close_at="2026-09-10T14:00:00-04:00")
    assert skip["eligible"] is True
    assert skip["action"] == "skip"
    assert skip["execution"] is False
    fill = decide(rule, posted_yes=0.80, close_at="2026-09-10T14:15:00-04:00")
    assert fill["action"] == "fill"
    historic = decide(rule, posted_yes=0.50, close_at="2026-09-10T13:00:00-04:00")
    assert historic["eligible"] is False
    assert historic["action"] == "ineligible"
    open_window = decide(rule, posted_yes=0.50, close_at="")
    assert open_window["action"] == "unknown"


def test_two_to_one_favorite_expresses_skip_and_fill():
    assert favorite_threshold(2) == 2 / 3
    rule = {
        "id": "R-SKIP-2TO1-FAVORITE",
        "declared_at": "2026-09-08T16:53:00-04:00",
        "kind": "selection",
        "selects": True,
        "execution": False,
        "params": {"favorite_odds": 2},
    }
    skip = decide(rule, posted_yes=2 / 3, close_at="2026-09-08T17:00:00-04:00")
    assert skip["eligible"] is True
    assert skip["action"] == "skip"
    assert skip["execution"] is False
    fill = decide(rule, posted_yes=0.50, close_at="2026-09-08T17:00:00-04:00")
    assert fill["action"] == "fill"
    historic = decide(rule, posted_yes=0.80, close_at="2026-09-08T16:45:00-04:00")
    assert historic["eligible"] is False
    assert historic["action"] == "ineligible"


_FAVORITE_CLOCK = {
    "id": "R-SKIP-2TO1-FAVORITE",
    "declared_at": "2026-09-08T16:53:00-04:00",
    "lived_paper_begins_at": "2026-09-08T17:11:00-04:00",
    "replay_close_after": "2026-09-08T16:53:00-04:00",
    "replay_close_at_or_before": "2026-09-08T17:11:00-04:00",
    "kind": "selection",
    "selects": True,
    "execution": True,
    "params": {"favorite_odds": 2},
}


def test_replay_interval_is_oos_but_not_lived():
    mid = "2026-09-08T17:00:00-04:00"
    flip = "2026-09-08T17:11:00-04:00"
    after = "2026-09-08T17:15:00-04:00"
    assert window_is_oos(_FAVORITE_CLOCK, close_at=mid) is True
    assert window_is_replay(_FAVORITE_CLOCK, close_at=mid) is True
    assert window_is_lived(_FAVORITE_CLOCK, close_at=mid) is False
    assert window_is_replay(_FAVORITE_CLOCK, close_at=flip) is True
    assert window_is_lived(_FAVORITE_CLOCK, close_at=flip) is False
    assert window_is_lived(_FAVORITE_CLOCK, close_at=after) is True
    assert window_is_replay(_FAVORITE_CLOCK, close_at=after) is False
    # decide() still expresses replay windows; the scorer is the lived gate.
    expressed = decide(_FAVORITE_CLOCK, posted_yes=0.50, close_at=mid)
    assert expressed["eligible"] is True
    assert expressed["action"] == "fill"


def _synthetic_lived_windows(n: int) -> list[dict]:
    out = []
    for i in range(n):
        minutes = i * 15
        h, m = divmod(minutes, 60)
        d, h = divmod(h, 24)
        out.append(
            {
                "window_id": f"SYNTH-{d:02d}{h:02d}{m:02d}",
                "close_at": f"2026-09-09T{h:02d}:{m:02d}:00-04:00",
                "posted_yes": 0.50,
                "recorded_pnl": 0.0,
                "stake": 1.0,
            }
        )
    return out


def test_score_rule_rejects_replay_window_as_lived():
    windows = _synthetic_lived_windows(69)
    windows.append(
        {
            "window_id": "REPLAY",
            "close_at": "2026-09-08T17:00:00-04:00",
            "posted_yes": 0.50,
            "recorded_pnl": 0.0,
            "stake": 1.0,
        }
    )
    with pytest.raises(RuleNotScorable, match="replay interval"):
        score_rule("R-SKIP-2TO1-FAVORITE", windows, allow_nonbinding=True)


def test_score_rule_accepts_post_flip_windows_and_labels_lived():
    windows = _synthetic_lived_windows(70)
    card = score_rule("R-SKIP-2TO1-FAVORITE", windows, allow_nonbinding=True)
    assert card["n"] == 70
    assert all(row["evidence"] == "lived" for row in card["windows"])
    assert card["look"] == "L1"


def test_declare_rule_refuses_a_selecting_rule_when_marks_exist(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        paper = tmp_path / "kalshi_15m" / "paper"
        paper.mkdir(parents=True)
        (paper / "KXBTC15M-26SEP071600-00.json").write_text("{}", encoding="utf-8")
        docs = tmp_path / "golf-offshoot" / "docs"
        docs.mkdir(parents=True)
        (docs / "LEARNING_LANE_15M_RULES.json").write_text(
            json.dumps({"rules": [], "trials_to_date": 0, "trials_log": []}),
            encoding="utf-8",
        )
        with pytest.raises(RuleAlreadyInformed, match="informing"):
            declare_rule(
                {
                    "id": "R-SKIP-NEW-CUT",
                    "kind": "selection",
                    "selects": True,
                    "params": {"favorite_odds": 3},
                },
                root=tmp_path,
            )
        row = declare_rule(
            {
                "id": "R-SKIP-HOUR-CLOSE-TEST",
                "kind": "selection",
                "selects": True,
                "params": {"skip_close_minute": 0},
                "expression": {"skip_if": "close_minute_eq"},
            },
            root=tmp_path,
            now_iso="2026-09-10T13:25:00-04:00",
        )
        assert row["id"] == "R-SKIP-HOUR-CLOSE-TEST"
        assert row["expected_skip_rate"] == 0.25
    finally:
        set_15m_root_override(None)


def test_declare_rule_refuses_unnamed_posted_yes_on_an_empty_tree(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        docs = tmp_path / "golf-offshoot" / "docs"
        docs.mkdir(parents=True)
        (docs / "LEARNING_LANE_15M_RULES.json").write_text(
            json.dumps({"rules": [], "trials_to_date": 0, "trials_log": []}),
            encoding="utf-8",
        )
        with pytest.raises(RuleSkipRateUnnamed, match="product structure"):
            declare_rule(
                {
                    "id": "R-SKIP-NEW-CUT",
                    "kind": "selection",
                    "selects": True,
                    "params": {"favorite_odds": 3},
                },
                root=tmp_path,
                now_iso="2026-09-10T09:00:00-04:00",
            )
    finally:
        set_15m_root_override(None)


def test_declare_rule_refuses_a_minute_not_on_the_quartet(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        docs = tmp_path / "golf-offshoot" / "docs"
        docs.mkdir(parents=True)
        (docs / "LEARNING_LANE_15M_RULES.json").write_text(
            json.dumps({"rules": [], "trials_to_date": 0, "trials_log": []}),
            encoding="utf-8",
        )
        with pytest.raises(RuleTooSparse, match="density floor"):
            declare_rule(
                {
                    "id": "R-SKIP-MINUTE-7",
                    "kind": "selection",
                    "selects": True,
                    "params": {"skip_close_minute": 7},
                    "expression": {"skip_if": "close_minute_eq"},
                },
                root=tmp_path,
            )
    finally:
        set_15m_root_override(None)


def test_hour_close_expected_skip_rate_clears_the_floor():
    rule = {
        "id": "R-SKIP-HOUR-CLOSE",
        "selects": True,
        "params": {"skip_close_minute": 0},
        "expression": {"skip_if": "close_minute_eq"},
    }
    assert expected_skip_rate(rule) == 0.25
    assert expected_skip_rate(rule) >= min_expected_skip_rate()
    civil = {
        "id": "R-SKIP-CIVIL",
        "selects": True,
        "params": {"skip_close_minutes": [0, 30]},
        "expression": {"skip_if": "close_minute_in"},
    }
    assert expected_skip_rate(civil) == 0.5
    fav = {
        "id": "R-SKIP-2TO1-FAVORITE",
        "selects": True,
        "params": {"favorite_odds": 2},
    }
    assert expected_skip_rate(fav) is None


def test_civil_boundaries_expresses_skip_on_named_walls():
    rule = {
        "id": "R-SKIP-CIVIL",
        "declared_at": "2026-09-10T14:00:00-04:00",
        "kind": "selection",
        "selects": True,
        "params": {"skip_close_minutes": [0, 30]},
        "expression": {"skip_if": "close_minute_in"},
    }
    assert selects_on_posted_yes_cut(rule) is False
    assert decide(rule, posted_yes=0.50, close_at="2026-09-10T15:00:00-04:00")["action"] == "skip"
    assert decide(rule, posted_yes=0.50, close_at="2026-09-10T15:30:00-04:00")["action"] == "skip"
    assert decide(rule, posted_yes=0.80, close_at="2026-09-10T15:15:00-04:00")["action"] == "fill"


def test_mechanism_catalog_seeds_the_kinds():
    kinds = [row["id"] for row in load_mechanism_catalog()["kinds"]]
    assert kinds == [
        "CLOCK-CLOSE-MINUTE",
        "CLOCK-CIVIL-BOUNDARIES",
        "CLOCK-QUARTER-BOUNDARIES",
        "CLOCK-HOUR-FIRST-HALF",
        "CLOCK-HOUR-SECOND-HALF",
        "CLOCK-HOUR-OPEN",
        "CLOCK-HOUR-WRAP",
        "CLOCK-INTRA-HOUR",
        "HONER-FROZEN-CONSULT",
        "HONER-FAMILY-AMEND",
        "HONER-FROZEN-REPLACE",
    ]


def test_existing_registry_rows_are_grandfathered():
    payload = load_rules()
    fav = next(row for row in payload["rules"] if row["id"] == "R-SKIP-2TO1-FAVORITE")
    assert fav["selects"] is True
    assert "expected_skip_rate" not in fav
    hour = next(row for row in payload["rules"] if row["id"] == "R-SKIP-HOUR-CLOSE")
    assert hour["params"]["skip_close_minute"] == 0
