import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.consult_honer import compose_and_skip, express_frozen_honer
from golf_offshoot.learning_lane_15m.paper import consult_registry, load_decisions, paper_autobet_open_markets
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, set_15m_root_override
from golf_offshoot.learning_lane_15m.rules import decide


FACTORY_FILL = {
    "rule_id": "R-SKIP-2TO1-FAVORITE",
    "action": "fill",
    "reason": "factory fill",
    "eligible": True,
    "execution": True,
}
FACTORY_SKIP = {
    "rule_id": "R-SKIP-2TO1-FAVORITE",
    "action": "skip",
    "reason": "factory skip",
    "eligible": True,
    "execution": True,
}
SRC = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot"


def test_compose_dark_missing_snapshot_returns_same_object():
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=None)
    assert out is FACTORY_FILL
    assert out["action"] == "fill"
    assert "consult" not in out


def test_compose_enabled_false_does_not_skip():
    snap = {"consult_enabled": False, "family": "H-SKIP-RICH-YES", "theta": 0.10}
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=snap)
    assert out is FACTORY_FILL
    assert out["action"] == "fill"


def test_compose_string_true_is_not_enabled():
    snap = {"consult_enabled": "true", "family": "H-SKIP-RICH-YES", "theta": 0.10}
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=snap)
    assert out is FACTORY_FILL


def test_and_skip_factory_skip_stays_skip():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES", "theta": 0.99}
    out = compose_and_skip(FACTORY_SKIP, posted_yes=0.40, snapshot=snap)
    assert out is FACTORY_SKIP
    assert out["action"] == "skip"
    assert out["reason"] == "factory skip"


def test_and_skip_honer_skip_wins_on_factory_fill():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES", "theta": 0.75}
    out = compose_and_skip(dict(FACTORY_FILL), posted_yes=0.80, snapshot=snap)
    assert out["action"] == "skip"
    assert "honer consult" in out["reason"]
    assert out["consult"] == "honer_and_skip"
    assert FACTORY_FILL["action"] == "fill"


def test_and_skip_honer_fill_keeps_factory_fill():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES", "theta": 0.90}
    base = dict(FACTORY_FILL)
    out = compose_and_skip(base, posted_yes=0.50, snapshot=snap)
    assert out is base
    assert out["action"] == "fill"


def test_spread_family_skips_wide_book():
    snap = {
        "consult_enabled": True,
        "family": "H-SKIP-WIDE-SPREAD",
        "theta": 0.99,
        "delta": 0.03,
    }
    out = compose_and_skip(dict(FACTORY_FILL), posted_yes=0.40, spread=0.05, snapshot=snap)
    assert out["action"] == "skip"
    action, _reason = express_frozen_honer(snap, posted_yes=0.40, spread=0.01)
    assert action == "fill"


def test_consult_registry_dark_matches_decide(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        rule = {
            "id": "R-SKIP-2TO1-FAVORITE",
            "declared_at": "2026-09-08T16:53:00-04:00",
            "kind": "selection",
            "selects": True,
            "execution": True,
            "params": {"favorite_odds": 2},
        }
        decided = decide(rule, posted_yes=0.50, close_at="2026-09-08T17:00:00-04:00")
        composed = consult_registry(
            rule, posted_yes=0.50, close_at="2026-09-08T17:00:00-04:00"
        )
        assert composed == decided
    finally:
        set_15m_root_override(None)


def test_paper_autobet_ignores_live_honer_theta_when_consult_off(tmp_path, monkeypatch):
    from golf_offshoot.data_feeds.kalshi_15m import parse_event, parse_market
    from golf_offshoot.honer_15m.paths import set_honer_root_override

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
        "yes_ask_dollars": "0.4000",
        "yes_bid_dollars": "0.3800",
        "title": "BTC price up in next 15 mins?",
    }
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_honer_root_override(tmp_path / "honer_15m")
    try:
        latest = latest_dir_15m()
        (latest / "honer_consult.json").write_text(
            json.dumps(
                {
                    "consult_enabled": False,
                    "family": "H-SKIP-RICH-YES",
                    "theta": 0.10,
                    "delta": 0.0,
                }
            ),
            encoding="utf-8",
        )
        honer_latest = tmp_path / "honer_15m" / "latest"
        honer_latest.mkdir(parents=True, exist_ok=True)
        (honer_latest / "theta.json").write_text(
            json.dumps({"theta": 0.10}), encoding="utf-8"
        )
        rule = {
            "id": "R-SKIP-2TO1-FAVORITE",
            "declared_at": "2026-09-08T16:53:00-04:00",
            "kind": "selection",
            "selects": True,
            "execution": True,
            "params": {"favorite_odds": 2},
        }
        market = parse_market(open_raw, event=parse_event(event))
        fills = paper_autobet_open_markets([market], rule=rule)
        assert len(fills) == 1
        assert load_decisions()[market["ticker"]]["action"] == "fill"
        assert "consult" not in load_decisions()[market["ticker"]]
    finally:
        set_15m_root_override(None)
        set_honer_root_override(None)


def test_enabled_missing_theta_returns_factory_verdict():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES"}
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=snap)
    assert out is FACTORY_FILL
    assert out["action"] == "fill"


def test_factory_paper_and_rules_do_not_import_honer_package():
    paper = (SRC / "learning_lane_15m" / "paper.py").read_text(encoding="utf-8")
    rules = (SRC / "learning_lane_15m" / "rules.py").read_text(encoding="utf-8")
    consult = (SRC / "learning_lane_15m" / "consult_honer.py").read_text(encoding="utf-8")
    assert "golf_offshoot.honer_15m" not in paper
    assert "golf_offshoot.honer_15m" not in rules
    assert "golf_offshoot.honer_15m" not in consult
    assert "theta.json" not in consult or "Never reads" in consult
