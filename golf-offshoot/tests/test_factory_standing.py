"""Factory English standing. Files only. No honer import. No invented pnl."""

from __future__ import annotations

import ast
from pathlib import Path

from golf_offshoot.learning_lane_15m.standing import collect_factory_standing


STANDING = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "learning_lane_15m" / "standing.py"


def test_factory_standing_does_not_import_honer():
    tree = ast.parse(STANDING.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "honer_15m" not in node.module
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "honer_15m" not in alias.name


def test_factory_standing_names_two_lineages_and_not_a_direction_model():
    standing = collect_factory_standing()
    text = " ".join(
        (
            standing.what_it_is,
            standing.where_it_stands,
            standing.last_happened,
            standing.this_book,
        )
    ).lower()
    assert "not predicting up or down" in text
    assert "lineage a" in text
    assert "lineage b" in text
    assert "never added" in text
    assert "not scored" in text
    assert "keep" in standing.where_it_stands.lower() or "not a keep" in text
    from golf_offshoot.learning_lane_15m.rules import active_execution_rule, clock_skip_minutes

    try:
        rule = active_execution_rule()
    except ValueError:
        rule = None
    if clock_skip_minutes(rule or {}) is not None:
        assert "2-to-1" not in standing.what_it_is
        assert "2-to-1" not in standing.current_phrase
        assert "2-to-1" not in standing.last_happened
        assert "67¢" not in standing.what_it_is
        assert "67¢" not in standing.current_phrase
        assert "67¢" not in standing.last_happened
        assert "skip" in standing.what_it_is.lower()


def test_hour_close_standing_does_not_narrate_two_to_one(monkeypatch):
    from types import SimpleNamespace

    from golf_offshoot.learning_lane_15m import standing as st

    rule = {
        "id": "R-SKIP-HOUR-CLOSE",
        "kind": "selection",
        "selects": True,
        "execution": True,
        "params": {"skip_close_minute": 0},
        "lived_paper_begins_at": "2026-09-10T13:36:00-04:00",
    }
    monkeypatch.setattr(st, "active_execution_rule", lambda: rule)
    monkeypatch.setattr(
        st,
        "load_rules",
        lambda: {"evidence_bar": {"binding": True}, "rules": [rule]},
    )
    monkeypatch.setattr(
        st,
        "load_decisions",
        lambda: {
            "KXBTC15M-26SEP120400-00": {
                "action": "skip",
                "close_at": "2026-09-12T08:00:00Z",
                "posted_yes": 0.71,
                "at": "2026-09-12T08:00:01Z",
            }
        },
    )
    monkeypatch.setattr(st, "_settle_result", lambda ticker: "yes")
    monkeypatch.setattr(st, "_journal_result", lambda ticker: "")
    monkeypatch.setattr(st, "_paper_pnl", lambda ticker: None)
    monkeypatch.setattr(
        st, "load_ledger", lambda: SimpleNamespace(bankroll=87.5, betting_pnl=-12.5)
    )
    standing = st.collect_factory_standing()
    blob = " ".join(
        (standing.what_it_is, standing.last_happened, standing.current_phrase)
    )
    assert "2-to-1" not in blob
    assert "67¢" not in blob
    assert ":00" in standing.what_it_is
    assert "skipped" in standing.current_phrase
    assert "R-SKIP-HOUR-CLOSE" in standing.where_it_stands


def test_favorite_standing_still_names_two_to_one_line(monkeypatch):
    from types import SimpleNamespace

    from golf_offshoot.learning_lane_15m import standing as st

    rule = {
        "id": "R-SKIP-2TO1-FAVORITE",
        "kind": "selection",
        "selects": True,
        "execution": True,
        "params": {"favorite_odds": 2},
    }
    monkeypatch.setattr(st, "active_execution_rule", lambda: rule)
    monkeypatch.setattr(
        st, "load_rules", lambda: {"evidence_bar": {"binding": False}, "rules": [rule]}
    )
    monkeypatch.setattr(
        st,
        "load_decisions",
        lambda: {
            "KXBTC15M-26SEP120415-15": {
                "action": "fill",
                "close_at": "2026-09-12T08:15:00Z",
                "posted_yes": 0.51,
                "at": "2026-09-12T08:15:01Z",
            }
        },
    )
    monkeypatch.setattr(st, "_settle_result", lambda ticker: "no")
    monkeypatch.setattr(st, "_journal_result", lambda ticker: "")
    monkeypatch.setattr(st, "_paper_pnl", lambda ticker: -1.0)
    monkeypatch.setattr(
        st, "load_ledger", lambda: SimpleNamespace(bankroll=99.0, betting_pnl=-1.0)
    )
    standing = st.collect_factory_standing()
    assert "2-to-1" in standing.what_it_is
    assert "67¢" in standing.current_phrase or "67¢" in standing.last_happened


def test_stopped_watch_clock_is_off_not_stale(monkeypatch):
    from golf_offshoot.learning_lane_15m.standing import factory_watch_clock

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.watch.load_watch_status",
        lambda: {
            "running": False,
            "last_at": "2026-01-01T00:00:00-04:00",
            "interval_s": 90.0,
            "cycles": 0,
            "last_summary": "",
        },
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learn.load_wake_state",
        lambda: {"board": {"note": "from wake", "stale": True, "lag_windows": 2}},
    )
    clock = factory_watch_clock()
    assert clock["running"] is False
    assert clock["stale"] is False
    assert clock["png_note"] == "from wake"
    assert clock["png_stale"] is True
    assert clock["png_lag"] == 2


def test_runner_log_trim_keeps_tail(tmp_path, monkeypatch):
    from golf_offshoot.learning_lane_15m import runner

    monkeypatch.setattr(runner, "MAX_RUNNER_LOG_BYTES", 80)
    dest = tmp_path / "learning_runner.jsonl"
    dest.write_text("\n".join(f'{{"n": {i}}}' for i in range(40)) + "\n", encoding="utf-8")
    assert dest.stat().st_size > 80
    runner._trim_runner_log(dest, keep=5)
    lines = dest.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 5
    assert lines[-1] == '{"n": 39}'
