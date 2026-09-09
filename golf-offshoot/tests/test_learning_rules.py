from golf_offshoot.learning_lane_15m.evidence_bar import class_is_burned
from golf_offshoot.learning_lane_15m.paper import load_decisions, paper_autobet_open_markets
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.rules import (
    decide,
    favorite_threshold,
    load_rules,
    window_is_oos,
)


def test_registry_has_dated_first_rules():
    payload = load_rules()
    ids = [row["id"] for row in payload["rules"]]
    assert ids == [
        "R-BASELINE-FILL-ALL",
        "R-SKIP-COINFLIP",
        "R-SKIP-2TO1-FAVORITE",
    ]
    assert payload["lab_admits"] is False
    assert payload["trials_to_date"] == 1
    assert payload["evidence_bar"]["binding"] is False
    skip = next(row for row in payload["rules"] if row["id"] == "R-SKIP-COINFLIP")
    assert skip["declared_at"] == "2026-09-08T05:56:00-04:00"
    assert skip["execution"] is False
    fav = next(row for row in payload["rules"] if row["id"] == "R-SKIP-2TO1-FAVORITE")
    assert fav["execution"] is True
    assert fav["selects"] is True
    assert fav["params"]["favorite_odds"] == 2
    log = payload["trials_log"]
    assert len(log) == 1
    assert log[0]["subject"] == "R-SKIP-2TO1-FAVORITE"
    assert log[0]["kind"] == "declaration"


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


def test_two_to_one_favorite_is_not_a_burned_class():
    assert class_is_burned("SKIP-2TO1-FAVORITE") is False
    assert class_is_burned("R-SKIP-2TO1-FAVORITE") is False
    assert class_is_burned("RETUNE-COINFLIP-BAND") is True
    assert class_is_burned("FEE-AS-SIGNAL") is True


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
