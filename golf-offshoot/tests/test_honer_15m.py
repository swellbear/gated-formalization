"""Isolation, θ, freeze, and futility for honer_15m."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from golf_offshoot.honer_15m import books, decide, freeze, loop, score, theta, watch
from golf_offshoot.honer_15m.paths import (
    LIVE_15M_NAME,
    honer_root,
    set_honer_root_override,
)
from golf_offshoot.honer_15m.policy import START_THETA
from golf_offshoot.operator_surface.lanes import parse_lane


FORBIDDEN_IMPORTS = {
    "golf_offshoot.learning_lane_15m.paper",
    "golf_offshoot.learning_lane_15m.rules",
    "golf_offshoot.learning_lane_15m.learn",
    "golf_offshoot.learning_lane_15m.watch",
    "golf_offshoot.learning_lane_15m.illustrate",
    "golf_offshoot.learning_lane_15m.runner",
    "golf_offshoot.learning_lane_15m.crew_tick",
    "golf_offshoot.learning_lane_15m.evidence_bar",
}

PKG = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "honer_15m"


@pytest.fixture
def honer_tmp(tmp_path, monkeypatch):
    root = tmp_path / "honer_15m"
    set_honer_root_override(root)
    yield root
    set_honer_root_override(None)


def test_parse_lane_stays_two_values():
    assert parse_lane("learning_lane_15m") == "learning_lane_15m"
    assert parse_lane("honer_15m") == "golf"
    assert parse_lane("15m") == "golf"


def test_import_whitelist():
    for path in PKG.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert node.module not in FORBIDDEN_IMPORTS, path.name
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in FORBIDDEN_IMPORTS, path.name


def test_tick_does_not_write_live_15m(honer_tmp, tmp_path):
    live = tmp_path / LIVE_15M_NAME
    live.mkdir()
    marker = live / "ledger.json"
    marker.write_text("keep", encoding="utf-8")
    markets = [
        {
            "ticker": "KXBTC15M-26SEP091400-00",
            "window_id": "w1",
            "paper_mark": 0.60,
            "yes_ask": 0.60,
            "is_open": True,
            "status": "active",
            "close_time": "2026-09-09T18:15:00Z",
            "result": "",
        }
    ]
    loop.run_tick(markets)
    assert marker.read_text(encoding="utf-8") == "keep"
    assert LIVE_15M_NAME not in {p.name for p in honer_tmp.rglob("*")}
    assert honer_root() == honer_tmp.resolve()


def test_decide_skip_and_fill():
    assert decide.decide_yes_or_skip(0.80, 0.75)[0] == "skip"
    assert decide.decide_yes_or_skip(0.70, 0.75)[0] == "fill"


def test_theta_steps_and_clip(honer_tmp):
    st = theta.step_search_theta(action="fill", kalshi_result="no")
    assert st["theta"] == pytest.approx(0.77)
    theta.step_search_theta(action="skip", kalshi_result="yes")
    st = theta.load_theta()
    assert st["theta"] == pytest.approx(0.75)
    st = theta.load_theta()
    st["theta"] = 0.90
    theta.save_theta(st)
    st = theta.step_search_theta(action="fill", kalshi_result="no")
    assert st["theta"] == pytest.approx(0.90)


def test_pending_does_not_step(honer_tmp):
    with pytest.raises(ValueError):
        theta.step_search_theta(action="fill", kalshi_result="")
    assert theta.load_theta()["theta"] == pytest.approx(START_THETA)


def test_restart_reloads_theta(honer_tmp):
    theta.step_search_theta(action="fill", kalshi_result="no")
    again = theta.load_theta()
    assert again["theta"] == pytest.approx(0.77)


def test_exam_settle_does_not_step_theta(honer_tmp):
    books.record_action(
        "exam",
        ticker="T1",
        window_id="w",
        action="fill",
        reason="x",
        posted_yes=0.6,
        theta=0.75,
        close_at="t",
    )
    books.apply_settle("exam", "T1", kalshi_result="no", step_theta=False)
    assert theta.load_theta()["theta"] == pytest.approx(START_THETA)


def test_freeze_gates(honer_tmp):
    st = theta.load_theta()
    st["search_settled_since_freeze"] = 19
    st["theta"] = 0.81
    theta.save_theta(st)
    assert freeze.freeze_ready() is False
    st["search_settled_since_freeze"] = 20
    st["theta"] = 0.76
    theta.save_theta(st)
    assert freeze.freeze_ready() is False
    st["theta"] = 0.81
    theta.save_theta(st)
    assert freeze.freeze_ready() is True
    exam = freeze.fire_freeze()
    assert exam and exam["open"] is True
    assert freeze.freeze_ready() is False
    assert freeze.load_trials()["trials_to_date"] == 1


def test_one_ticket_per_ticker(honer_tmp):
    loop.run_tick(
        [
            {
                "ticker": "KXBTC15M-X",
                "window_id": "w",
                "paper_mark": 0.60,
                "is_open": True,
                "status": "active",
                "close_time": "t",
                "result": "",
            }
        ]
    )
    loop.run_tick(
        [
            {
                "ticker": "KXBTC15M-X",
                "window_id": "w",
                "paper_mark": 0.60,
                "is_open": True,
                "status": "active",
                "close_time": "t",
                "result": "",
            }
        ]
    )
    assert books.load_ledger("search")["entries"] == 1


def test_fill_all_and_d():
    assert books.fill_all_pnl(0.50, "no") == -1.0
    win = books.fill_all_pnl(0.50, "yes")
    assert win == pytest.approx(1.0)


def test_futility_impossible_clause4():
    assert score.futility_impossible(20, d_sum=10.0, exam_pnl_sum=-1.0, exam_n=70) is True
    assert score.futility_impossible(20, d_sum=10.0, exam_pnl_sum=1.0, exam_n=70) is False
    assert score.futility_impossible(20, d_sum=-60.0, exam_pnl_sum=5.0, exam_n=70) is True


def test_alpha_k():
    assert score.alpha_k(0) == pytest.approx(0.025)
    assert score.alpha_k(1) == pytest.approx(0.05 / 6)


def test_watch_exception_does_not_raise(honer_tmp, monkeypatch):
    hw = watch.HonerWatch(interval_s=0.01, first_sleep_s=0.0)

    def boom():
        hw._stop.set()
        raise RuntimeError("boom")

    monkeypatch.setattr(watch, "run_tick", boom)
    hw._run()
    assert "boom" in hw.last_error


def test_sandbox_has_no_combined_bankroll(honer_tmp):
    from golf_offshoot.honer_15m.hub_block import sandbox_html

    html = sandbox_html()
    assert "combined" not in html.lower()
    assert "winner" not in html.lower()
    assert "Lineage A" in html
    assert "do not merge" in html.lower() or "do not add" in html.lower()


def test_reload_pkg_dirs_omit_honer():
    from golf_offshoot.operator_surface.reload import _CODE_PKG_DIRS

    assert "honer_15m" not in _CODE_PKG_DIRS
    assert "learning_lane_15m" in _CODE_PKG_DIRS


def test_illustrate_uses_exact_live_root():
    src = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "golf_offshoot"
        / "learning_lane_15m"
        / "illustrate.py"
    )
    text = src.read_text(encoding="utf-8")
    assert "learning_lane_15m*" not in text
    assert "honer_15m" not in text
