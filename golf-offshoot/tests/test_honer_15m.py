"""Isolation, θ, freeze, and futility for honer_15m."""

from __future__ import annotations

import ast
import os
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
from golf_offshoot.quote_bus import set_quote_bus_root_override
from golf_offshoot.two_brains import set_two_brains_root_override


FORBIDDEN_IMPORTS = {
    "golf_offshoot.learning_lane_15m.paper",
    "golf_offshoot.learning_lane_15m.rules",
    "golf_offshoot.learning_lane_15m.learn",
    "golf_offshoot.learning_lane_15m.watch",
    "golf_offshoot.learning_lane_15m.illustrate",
    "golf_offshoot.learning_lane_15m.runner",
    "golf_offshoot.learning_lane_15m.crew_tick",
    "golf_offshoot.learning_lane_15m.evidence_bar",
    "golf_offshoot.learning_lane_15m.standing",
}

PKG = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "honer_15m"


@pytest.fixture
def honer_tmp(tmp_path, monkeypatch):
    root = tmp_path / "honer_15m"
    set_honer_root_override(root)
    set_quote_bus_root_override(tmp_path / "quote_bus")
    set_two_brains_root_override(tmp_path / "two_brains")
    yield root
    set_honer_root_override(None)
    set_quote_bus_root_override(None)
    set_two_brains_root_override(None)


def _seed_search_quotes(*, n: int = 20, with_spread: int = 20) -> None:
    rows = {}
    for i in range(n):
        rows[f"KXBTC15M-Q{i:02d}"] = {
            "ticker": f"KXBTC15M-Q{i:02d}",
            "action": "fill",
            "spread": 0.04 if i < with_spread else None,
            "posted_yes": 0.70,
            "theta": 0.75,
            "at": f"2026-09-09T00:{i:02d}:00-04:00",
        }
    books.save_decisions("search", rows)


def test_parse_lane_stays_two_values():
    assert parse_lane("learning_lane_15m") == "learning_lane_15m"
    assert parse_lane("honer_15m") == "golf"
    assert parse_lane("15m") == "golf"


def test_import_whitelist():
    from golf_offshoot.honer_15m.invariants import ALLOWED_EVIDENCE_BAR_FILES, FORBIDDEN_IMPORTS

    for path in PKG.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if (
                    node.module == "golf_offshoot.learning_lane_15m.evidence_bar"
                    and path.name in ALLOWED_EVIDENCE_BAR_FILES
                ):
                    continue
                assert node.module not in FORBIDDEN_IMPORTS, path.name
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if (
                        alias.name == "golf_offshoot.learning_lane_15m.evidence_bar"
                        and path.name in ALLOWED_EVIDENCE_BAR_FILES
                    ):
                        continue
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


def test_v2_far_fill_loss_does_not_step(honer_tmp):
    st = theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.48)
    assert st["theta"] == pytest.approx(START_THETA)
    assert st["search_settled_since_freeze"] == 1
    assert st["in_band_settled"] == 0
    assert st["far_settled_since_freeze"] == 1
    assert st["in_band_stable"] == 0


def test_v2_inband_fill_loss_tightens(honer_tmp):
    st = theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.68)
    assert st["theta"] == pytest.approx(0.73)


def test_v2_inband_skip_yes_raises(honer_tmp):
    theta.step_search_theta(action="skip", kalshi_result="yes", posted_yes=0.80)
    assert theta.load_theta()["theta"] == pytest.approx(0.77)


def test_v2_clip_min_stays(honer_tmp):
    st = theta.load_theta()
    st["theta"] = 0.55
    theta.save_theta(st)
    st = theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.50)
    assert st["theta"] == pytest.approx(0.55)


def test_pending_does_not_step(honer_tmp):
    with pytest.raises(ValueError):
        theta.step_search_theta(action="fill", kalshi_result="")
    assert theta.load_theta()["theta"] == pytest.approx(START_THETA)


def test_restart_reloads_theta(honer_tmp):
    theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.68)
    again = theta.load_theta()
    assert again["theta"] == pytest.approx(0.73)


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


def test_freeze_needs_novelty_and_stability(honer_tmp):
    st = theta.load_theta()
    st["in_band_settled"] = 20
    st["theta"] = 0.81
    st["in_band_stable"] = 4
    theta.save_theta(st)
    assert freeze.freeze_ready() is False
    st["in_band_stable"] = 5
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


def test_exam_k_stamped(honer_tmp):
    from golf_offshoot.honer_15m.freeze import save_exam_state

    save_exam_state({"open": True, "k_after": 2, "frozen_theta": 0.81, "n": 0})
    row = books.record_action(
        "exam",
        ticker="KXBTC15M-EXAM",
        window_id="w",
        action="skip",
        reason="x",
        posted_yes=0.80,
        theta=0.81,
        close_at="t",
    )
    assert row["exam_k"] == 2


def test_standing_skip_why_and_pending_not_zero(honer_tmp):
    from golf_offshoot.honer_15m.board import collect_standing
    from golf_offshoot.honer_15m.hub_block import sandbox_html

    books.record_action(
        "search",
        ticker="KXBTC15M-26SEP091400-00",
        window_id="KXBTC15M-26SEP091400__2026-09-09T17:45:00Z__2026-09-09T18:00:00Z",
        action="skip",
        reason="posted_yes >= theta 0.75",
        posted_yes=0.80,
        theta=0.75,
        close_at="2026-09-09T18:00:00Z",
    )
    standing = collect_standing()
    assert standing.search_rows
    row = standing.search_rows[0]
    assert "skipped" in row.why.lower()
    assert row.pending is True
    assert "+0.00" not in row.pnl_text
    assert "waiting" in row.pnl_text.lower()
    html = sandbox_html()
    assert "skipped" in html.lower()
    assert "do not add" in html.lower()
    assert "combined bankroll" not in html.lower()
    assert "winner" not in html.lower()


def test_honer_png_path_stays_under_honer_root(honer_tmp):
    from golf_offshoot.honer_15m.paths import board_png_path, honer_root

    path = board_png_path()
    assert honer_root() in path.parents or path.parent == honer_root()
    assert "learning_lane_15m" not in path.as_posix()
    assert "observability-hub" not in path.as_posix()


def test_honer_illustrate_does_not_import_live_board():
    src = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "honer_15m" / "illustrate.py"
    text = src.read_text(encoding="utf-8")
    assert "golf_offshoot.learning_lane_15m.illustrate" not in text
    assert "paper_window_strip.png" not in text


def test_v2_migrate_keeps_theta_resets_clock(honer_tmp):
    import json

    from golf_offshoot.honer_15m.paths import theta_path

    payload = {"theta": 0.79, "last_declared_theta": 0.75, "search_settled_since_freeze": 4}
    theta_path().write_text(json.dumps(payload), encoding="utf-8")
    got = theta.load_theta()
    assert got["theta"] == pytest.approx(0.79)
    assert got["last_declared_theta"] == pytest.approx(0.75)
    assert got["search_settled_since_freeze"] == 0
    assert got["step_rule"] == "local_regret_v2"
    assert got["freeze_rule"] == "in_band_v1"
    assert got["stable_windows"] == 0
    assert got["in_band_settled"] == 0


def test_retired_vector_cannot_freeze(honer_tmp):
    from golf_offshoot.honer_15m.library import append_exam_row
    from golf_offshoot.honer_15m.policy import knob_vector

    append_exam_row(
        k=1,
        family="H-SKIP-RICH-YES",
        knobs=knob_vector(family="H-SKIP-RICH-YES", theta=0.81, delta=0.04),
        outcome="parked",
    )
    st = theta.load_theta()
    st["theta"] = 0.81
    st["in_band_settled"] = 20
    st["in_band_stable"] = 5
    theta.save_theta(st)
    assert freeze.freeze_ready() is False


def test_picker_has_no_pnl_parameters():
    import inspect

    from golf_offshoot.honer_15m import picker

    for name in (
        "on_exam_close",
        "maybe_advance",
        "apply_search_starvation",
        "iter_exam_queue",
        "next_freeze_brain",
        "queue_status",
    ):
        params = inspect.signature(getattr(picker, name)).parameters
        for banned in ("d", "pnl", "ledger", "exam_pnl", "betting_pnl"):
            assert banned not in params
    src = (PKG / "picker.py").read_text(encoding="utf-8")
    assert "exam_sums" not in src
    assert "load_ledger" not in src
    assert "betting_pnl" not in src
    from golf_offshoot.honer_15m import family_amend

    for name in (
        "exam_completed_dead_from_files",
        "family_amend_reasons_from_files",
        "family_amend_owed_from_files",
        "stamp_family_amend",
    ):
        params = inspect.signature(getattr(family_amend, name)).parameters
        for banned in ("d", "pnl", "ledger", "exam_pnl", "betting_pnl"):
            assert banned not in params
    amend_src = (PKG / "family_amend.py").read_text(encoding="utf-8")
    assert "exam_sums" not in amend_src
    assert "load_ledger" not in amend_src
    assert "iter_settled" not in amend_src


def test_catalog_skips_two_thirds():
    from golf_offshoot.honer_15m.catalog import catalog_ids, load_catalog

    text = str(load_catalog())
    assert "0.666" not in text
    assert "2/3" not in text
    assert catalog_ids() == ["H-SKIP-RICH-YES", "H-SKIP-WIDE-SPREAD"]


def test_clip_exhaust_does_not_switch_family(honer_tmp):
    from golf_offshoot.honer_15m.library import append_exam_row
    from golf_offshoot.honer_15m.picker import maybe_advance
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, knob_vector

    append_exam_row(
        k=1,
        family="H-SKIP-RICH-YES",
        knobs=knob_vector(family="H-SKIP-RICH-YES", theta=0.81, delta=0.04),
        outcome="completed_unscored",
    )
    st = theta.load_theta()
    st["theta"] = 0.90
    st["clip_streak"] = 20
    theta.save_theta(st)
    _seed_search_quotes(n=20, with_spread=20)
    out = maybe_advance()
    assert out and out["advanced"] is False
    assert out.get("parallel_families") is True
    live = theta.load_theta()
    assert live["active_family"] == FAMILY_RICH
    assert live["theta"] == pytest.approx(0.90)
    assert freeze.load_trials()["trials_to_date"] == 0


def test_ordinary_exam_close_does_not_reset_theta(honer_tmp):
    from golf_offshoot.honer_15m.picker import on_exam_close
    from golf_offshoot.honer_15m.policy import knob_vector

    st = theta.load_theta()
    st["theta"] = 0.79
    theta.save_theta(st)
    on_exam_close(
        outcome="completed_unscored",
        family="H-SKIP-RICH-YES",
        knobs=knob_vector(family="H-SKIP-RICH-YES", theta=0.79, delta=0.04),
        k=1,
    )
    assert theta.load_theta()["theta"] == pytest.approx(0.79)


def test_missing_quotes_do_not_invent_spread():
    from golf_offshoot.honer_15m.decide import decide_ticket, posted_mark
    from golf_offshoot.honer_15m.policy import FAMILY_SPREAD

    market = {"paper_mark": 0.60, "yes_ask": 0.62, "yes_bid": 0.50}
    assert posted_mark(market) == pytest.approx(0.60)
    action, reason = decide_ticket(
        0.60, 0.75, family=FAMILY_SPREAD, delta=0.04, spread=0.12
    )
    assert action == "skip"
    assert "spread" in reason
    action2, reason2 = decide_ticket(
        0.60, 0.75, family=FAMILY_SPREAD, delta=0.04, spread=None
    )
    assert action2 == "defer"
    assert "invent" in reason2


def test_hub_block_has_no_combined_pnl(honer_tmp):
    from golf_offshoot.honer_15m.hub_block import sandbox_html

    html = sandbox_html()
    assert "combined" not in html.lower()
    assert "library" in html.lower()
    assert "keep" in html.lower()


def test_v1_step_removed_from_policy():
    from golf_offshoot.honer_15m.policy import load_policy

    pol = load_policy()
    assert pol["step_rule"] == "local_regret_v2"
    assert pol["step_band"] == pytest.approx(0.10)
    assert pol["freeze_rule"] == "in_band_v1"
    assert pol["spread_band"] == pytest.approx(0.03)


def test_freeze_meter_matches_theta(honer_tmp):
    from golf_offshoot.honer_15m.board import collect_standing, freeze_meter

    st = theta.load_theta()
    st["theta"] = 0.81
    st["last_declared_theta"] = 0.75
    st["in_band_settled"] = 3
    st["far_settled_since_freeze"] = 1
    st["in_band_stable"] = 2
    theta.save_theta(st)
    line = freeze_meter()
    assert line == (
        "Honer freeze: 3/20 in-band · 1 far ignored · "
        "40: need a visit · 70: need 20 in-band · "
        "moved 6¢ of 5¢ · "
        "stable 2/5 · line 81¢ · skip-rich-YES"
    )
    standing = collect_standing()
    assert standing.freeze_meter == line
    assert standing.subtitle_lines[0] == line
    st["in_band_settled"] = 20
    st["in_band_stable"] = 5
    theta.save_theta(st)
    ready = freeze_meter()
    assert ready == "Honer freeze: ready — next tick can open exam. Not a keep."


def test_library_english_has_no_registry_ids(honer_tmp):
    from golf_offshoot.honer_15m.board import collect_standing, library_english
    from golf_offshoot.honer_15m.library import append_exam_row
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, knob_vector

    none_line = library_english(
        {"rows": [], "retired": []},
        family=FAMILY_RICH,
        clip_streak=0,
        clip_need=20,
    )
    assert none_line.startswith("No exam yet.")
    assert "completed_unscored" not in none_line
    assert "completed_dead" not in none_line
    append_exam_row(
        k=1,
        family=FAMILY_RICH,
        knobs=knob_vector(family=FAMILY_RICH, theta=0.81, delta=0.04),
        outcome="completed_unscored",
    )
    standing = collect_standing()
    assert "completed_unscored" not in standing.library_line
    assert "completed_dead" not in standing.library_line
    assert "Still not a keep" in standing.library_line
    assert "means were above zero" in standing.library_line
    dead = library_english(
        {"rows": [{"outcome": "completed_dead"}], "retired": [1]},
        family=FAMILY_RICH,
        clip_streak=0,
        clip_need=20,
    )
    assert "completed_dead" not in dead
    assert "mean was not above zero" in dead
    parked = library_english(
        {"rows": [{"outcome": "parked"}], "retired": [1]},
        family=FAMILY_RICH,
        clip_streak=0,
        clip_need=20,
    )
    assert parked.startswith("Last exam stopped early (futility).")
    untestable = library_english(
        {"rows": [{"outcome": "search_untestable"}], "retired": [1]},
        family=FAMILY_RICH,
        clip_streak=0,
        clip_need=20,
    )
    assert "search_untestable" not in untestable
    assert "The tape did not visit the line" in untestable
    assert "that hunt's start" in untestable
    assert "skip-wide-spread" in untestable


def test_near_line_48_vs_81_is_no(honer_tmp):
    from golf_offshoot.honer_15m.board import collect_standing, current_search_action
    from golf_offshoot.honer_15m.hub_block import sandbox_html

    books.record_action(
        "search",
        ticker="KXBTC15M-26SEP091400-00",
        window_id="w",
        action="fill",
        reason="posted_yes below theta 0.81",
        posted_yes=0.48,
        theta=0.81,
        close_at="2026-09-09T18:00:00Z",
    )
    row = collect_standing().search_rows[0]
    assert row.near_line is False
    assert row.near_line_text == "no"
    phrase = current_search_action()["phrase"]
    assert "not near the 81¢ line" in phrase
    assert "48¢" in phrase
    html = sandbox_html()
    assert "Near line" in html
    assert "Spread" in html
    assert "Wide-book" in html
    assert "+0.00" not in row.pnl_text


def test_missing_quotes_spread_na_decide_richness_only(honer_tmp):
    from golf_offshoot.honer_15m.board import collect_standing
    from golf_offshoot.honer_15m.decide import decide_ticket
    from golf_offshoot.honer_15m.policy import FAMILY_SPREAD

    books.record_action(
        "search",
        ticker="KXBTC15M-26SEP091415-15",
        window_id="w",
        action="fill",
        reason="posted_yes below theta 0.81",
        posted_yes=0.70,
        theta=0.81,
        close_at="2026-09-09T18:15:00Z",
        spread=None,
        delta=0.04,
    )
    row = collect_standing().search_rows[0]
    assert row.spread is None
    assert row.spread_text == "n/a"
    assert row.delta_text == "4¢"
    action, reason = decide_ticket(
        0.70, 0.81, family=FAMILY_SPREAD, delta=0.04, spread=None
    )
    assert action == "defer"
    assert "invent" in reason


def test_clocks_and_spine_show_meter_without_restyle(honer_tmp):
    from golf_offshoot.operator_surface.app import _clock_legend_html, _spine_html
    from golf_offshoot.operator_surface.this_window import this_window_html

    st = theta.load_theta()
    st["theta"] = 0.81
    st["last_declared_theta"] = 0.75
    st["in_band_settled"] = 3
    st["far_settled_since_freeze"] = 1
    st["in_band_stable"] = 2
    theta.save_theta(st)
    clocks = _clock_legend_html()
    assert "Honer freeze: 3/20 in-band" in clocks
    assert "1 far ignored" in clocks
    assert "moved 6¢ of 5¢" in clocks
    assert "Quote bus:" in clocks
    spine = _spine_html()
    assert "Only tickets within 10¢ of the line move it." in spine
    assert "Freeze counts only in-band tickets." in spine
    assert "Factory — live 70" in spine
    assert "Search may move a cutoff." in spine
    books.record_action(
        "search",
        ticker="KXBTC15M-26SEP091400-00",
        window_id="w",
        action="fill",
        reason="x",
        posted_yes=0.48,
        theta=0.81,
        close_at="t",
    )
    now_html = this_window_html()
    assert "not near the 81¢ line" in now_html
    assert "$" not in now_html or "Actions only" in now_html
    assert "combined" not in now_html.lower()


def test_far_settles_cannot_freeze(honer_tmp):
    st = theta.load_theta()
    st["theta"] = 0.81
    st["last_declared_theta"] = 0.75
    theta.save_theta(st)
    for _ in range(20):
        theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.48)
    live = theta.load_theta()
    live["stable_windows"] = 5
    live["search_settled_since_freeze"] = 20
    theta.save_theta(live)
    live = theta.load_theta()
    assert live["in_band_settled"] == 0
    assert live["far_settled_since_freeze"] == 20
    assert live["in_band_stable"] == 0
    assert freeze.freeze_ready() is False


def test_clip_streak_does_not_increment_on_far_at_clip(honer_tmp):
    st = theta.load_theta()
    st["theta"] = 0.90
    st["clip_streak"] = 19
    theta.save_theta(st)
    live = theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.48)
    assert live["clip_streak"] == 19
    assert live["far_settled_since_freeze"] == 1
    assert live["in_band_settled"] == 0


def test_in_band_migrate_keeps_theta_resets_clocks(honer_tmp):
    import json

    from golf_offshoot.honer_15m.paths import theta_path

    payload = {
        "theta": 0.81,
        "last_declared_theta": 0.75,
        "step_rule": "local_regret_v2",
        "search_settled_since_freeze": 1,
        "active_family": "H-SKIP-RICH-YES",
        "delta": 0.04,
    }
    theta_path().write_text(json.dumps(payload), encoding="utf-8")
    got = theta.load_theta()
    assert got["theta"] == pytest.approx(0.81)
    assert got["last_declared_theta"] == pytest.approx(0.75)
    assert got["in_band_settled"] == 0
    assert got["far_settled_since_freeze"] == 0
    assert got["freeze_rule"] == "in_band_v1"


def test_thin_quotes_do_not_invent_spread_or_switch_family(honer_tmp):
    from golf_offshoot.honer_15m.picker import maybe_advance
    from golf_offshoot.honer_15m.policy import FAMILY_RICH

    st = theta.load_theta()
    st["clip_streak"] = 20
    theta.save_theta(st)
    _seed_search_quotes(n=20, with_spread=10)
    out = maybe_advance()
    assert out and out.get("advanced") is False
    assert out.get("waiting_on_quotes") is not True
    assert theta.load_theta()["active_family"] == FAMILY_RICH


def test_no_bus_does_not_http_or_write_live_15m(honer_tmp, monkeypatch, tmp_path):
    import json

    called = []

    def boom(*_a, **_k):
        called.append(1)
        raise AssertionError("Kalshi fetch must not run")

    monkeypatch.setattr("golf_offshoot.data_feeds.kalshi_15m.Kalshi15mFeed.fetch", boom)
    src = (PKG / "loop.py").read_text(encoding="utf-8")
    assert "Kalshi15mFeed" not in src
    assert loop.fetch_markets() == []
    assert called == []
    live = tmp_path / LIVE_15M_NAME
    live.mkdir()
    marker = live / "ledger.json"
    marker.write_text("keep", encoding="utf-8")
    out = loop.run_tick()
    assert out["http_fetches"] == 0
    assert out["quote_bus_stale"] is True
    assert marker.read_text(encoding="utf-8") == "keep"
    from golf_offshoot.honer_15m.paths import last_tick_path

    last = json.loads(last_tick_path().read_text(encoding="utf-8"))
    assert last["http_fetches"] == 0
    assert last["wrote_learning_lane_15m"] is False


def test_cite_factory_pin_does_not_open_keep(tmp_path):
    import json

    from golf_offshoot.honer_15m.fee import cite_factory_pin, factory_schedule_sha256
    from golf_offshoot.honer_15m.keep import can_keep, keep_blocked_reason

    factory = tmp_path / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
    honer = tmp_path / "HONER_15M_EVIDENCE_BAR.json"
    factory.write_text(
        json.dumps({"fee_hurdle": {"schedule_sha256": "abc"}}),
        encoding="utf-8",
    )
    honer.write_text(
        json.dumps(
            {
                "binding": False,
                "fee_omitted": True,
                "founder_read_once": False,
                "lab_admits": False,
                "trading_armed": False,
            }
        ),
        encoding="utf-8",
    )
    cite = cite_factory_pin(factory_bar=factory, honer_bar=honer)
    assert cite["schedule_sha256"] == "abc"
    assert cite["fee_omitted"] is True
    payload = json.loads(honer.read_text(encoding="utf-8"))
    assert payload["fee_omitted"] is True
    assert payload["factory_fee_cite"]["schedule_sha256"] == "abc"
    assert can_keep(payload) is False
    assert keep_blocked_reason(payload) == "fee omitted"
    assert factory_schedule_sha256(bar_path=factory) == "abc"


def test_apply_factory_fee_clears_omitted_keeps_keep_closed(tmp_path):
    import json

    from golf_offshoot.honer_15m.fee import apply_factory_fee, fee_is_applied
    from golf_offshoot.honer_15m.keep import can_keep, keep_blocked_reason

    sha = "c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601"
    factory = tmp_path / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
    honer = tmp_path / "HONER_15M_EVIDENCE_BAR.json"
    factory.write_text(json.dumps({"fee_hurdle": {"schedule_sha256": sha}}), encoding="utf-8")
    honer.write_text(
        json.dumps(
            {
                "binding": False,
                "fee_omitted": True,
                "lab_admits": False,
                "trading_armed": False,
            }
        ),
        encoding="utf-8",
    )
    applied = apply_factory_fee(factory_bar=factory, honer_bar=honer)
    payload = json.loads(honer.read_text(encoding="utf-8"))
    assert applied["fee_omitted"] is False
    assert payload["fee_omitted"] is False
    assert payload["honer_fee_apply"]["schedule_sha256"] == sha
    assert fee_is_applied(payload) is True
    assert can_keep(payload) is False
    assert keep_blocked_reason(payload) == "bar not binding"
    assert payload.get("consult_enabled") is not True
    assert applied.get("pin_source") == "founder_browser_bytes"


def test_apply_short_sha_does_not_clear_omitted(tmp_path):
    import json

    from golf_offshoot.honer_15m.fee import apply_factory_fee, fee_is_applied
    from golf_offshoot.honer_15m.keep import can_keep, keep_blocked_reason

    factory = tmp_path / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
    honer = tmp_path / "HONER_15M_EVIDENCE_BAR.json"
    factory.write_text(json.dumps({"fee_hurdle": {"schedule_sha256": "abc"}}), encoding="utf-8")
    honer.write_text(
        json.dumps(
            {
                "binding": False,
                "fee_omitted": True,
                "lab_admits": False,
                "trading_armed": False,
            }
        ),
        encoding="utf-8",
    )
    applied = apply_factory_fee(factory_bar=factory, honer_bar=honer)
    payload = json.loads(honer.read_text(encoding="utf-8"))
    assert applied["fee_omitted"] is True
    assert payload["fee_omitted"] is True
    assert "honer_fee_apply" not in payload
    assert fee_is_applied(payload) is False
    assert can_keep(payload) is False
    assert keep_blocked_reason(payload) == "fee omitted"


def test_write_exam_scorecard_is_not_consult_enable(honer_tmp):
    import json

    from golf_offshoot.honer_15m.paths import exam_score_path
    from golf_offshoot.honer_15m.score import write_exam_scorecard

    exam = {
        "frozen_family": "H-SKIP-RICH-YES",
        "frozen_theta": 0.81,
        "frozen_delta": 0.04,
        "declared_at": "2026-09-10T14:00:00-04:00",
    }
    card = write_exam_scorecard(exam, outcome="completed_dead")
    assert card["consult_enabled"] is False
    assert card["survives"] is False
    path = exam_score_path()
    assert path.is_file()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["consult_enabled"] is False
    assert "learning_lane_15m" not in {p.name for p in honer_tmp.rglob("*")}


def test_can_keep_does_not_wait_on_founder_read_once():
    from golf_offshoot.honer_15m.keep import can_keep, keep_blocked_reason

    payload = {
        "binding": True,
        "fee_omitted": False,
        "lab_admits": False,
        "trading_armed": False,
        "founder_read_once": False,
    }
    assert keep_blocked_reason(payload) is None
    assert can_keep(payload) is True


def test_can_keep_false_and_exam_label_is_not_keep():
    from golf_offshoot.honer_15m.keep import can_keep, keep_blocked_reason

    assert can_keep() is False
    reason = keep_blocked_reason()
    assert reason in {"fee omitted", "bar not binding"}
    assert score.classify_completed_exam([]) == "completed_dead"
    assert "not a keep" in (score.classify_completed_exam.__doc__ or "").lower()


def test_catalog_next_none_and_burned_id_rejected():
    from golf_offshoot.honer_15m.catalog import CatalogError, _validate_item, next_family

    assert next_family("H-SKIP-WIDE-SPREAD") is None
    with pytest.raises(CatalogError):
        _validate_item({"id": "FLIP", "declared_at": "2026-09-09T15:44:00-04:00", "activate": "start"}, index=1)


def test_sidecar_cmdline_is_honer_not_shell():
    from golf_offshoot.honer_15m.watch import honer_sidecar_command

    cmd = honer_sidecar_command(executable="python")
    assert "honer-15m" in cmd
    assert "shell" not in cmd
    honesty = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "learning_lane_15m" / "honesty.py"
    trees_src = honesty.read_text(encoding="utf-8")
    start = trees_src.find("def hub_trees")
    body = trees_src[start : trees_src.find("\ndef ", start + 1)]
    assert "honer-15m" not in body
    assert " shell" in body


def test_honer_png_has_near_spread_wide_columns():
    from golf_offshoot.honer_15m.illustrate import COLUMNS

    labels = [label.lower() for _k, _x, label in COLUMNS]
    assert any("near line" in label for label in labels)
    assert any(label == "spread" for label in labels)
    assert any("wide-book" in label for label in labels)


def test_maybe_render_rebuilds_when_theta_changes(honer_tmp, monkeypatch):
    from golf_offshoot.honer_15m.illustrate import chart_png_path, maybe_render
    from golf_offshoot.honer_15m.paths import theta_path

    png = chart_png_path()
    png.write_bytes(b"old-png")
    theta.save_theta(theta.load_theta())
    later = png.stat().st_mtime + 5
    os.utime(theta_path(), (later, later))
    called: list[int] = []

    def fake_render():
        called.append(1)
        return png

    monkeypatch.setattr("golf_offshoot.honer_15m.illustrate.render_honer_window_strip", fake_render)
    maybe_render()
    assert called == [1]


def test_exam_idle_uses_freeze_meter(honer_tmp):
    from golf_offshoot.honer_15m.hub_block import sandbox_html

    html = sandbox_html()
    assert "Exam idle." in html
    assert "in-band" in html
    assert "Discovery organ" in html
    assert "consult is off" in html.lower()
    assert "combined" not in html.lower()


def test_invariants_not_on_factory_whitelist(honer_tmp):
    from golf_offshoot.honer_15m.invariants import run_invariants
    from golf_offshoot.learning_lane_15m.runner import CLERICAL_WHITELIST

    loop.run_tick([])
    payload = run_invariants()
    assert payload["not_on_factory_whitelist"] is True
    assert "honer-invariants" not in CLERICAL_WHITELIST
    assert payload["passed"] is True


def test_catalog_starvation_activate_is_file_derived():
    from golf_offshoot.honer_15m.catalog import (
        CatalogError,
        activate_allowed,
        catalog_ids,
        load_catalog,
    )

    payload = load_catalog()
    items = [item for item in payload.get("items") or [] if isinstance(item, dict)]
    assert catalog_ids() == ["H-SKIP-RICH-YES", "H-SKIP-WIDE-SPREAD"]
    assert len(items) == 2
    assert items[1]["activate"] == "start"
    assert items[0]["activate"] == "start"
    assert activate_allowed(items[1]["activate"])
    assert not activate_allowed("pnl_rank")
    assert not activate_allowed("clip_exhaustion|")
    try:
        from golf_offshoot.honer_15m.catalog import _validate_item

        _validate_item(
            {"id": "H-SKIP-WIDE-SPREAD", "declared_at": "x", "activate": "tape_sort"},
            index=1,
        )
        raise AssertionError("expected CatalogError")
    except CatalogError:
        pass


def test_deploy_does_not_zero_live_search_clocks(honer_tmp):
    import json

    from golf_offshoot.honer_15m.paths import theta_path

    payload = {
        "theta": 0.81,
        "last_declared_theta": 0.75,
        "step_rule": "local_regret_v2",
        "freeze_rule": "in_band_v1",
        "search_settled_since_freeze": 6,
        "in_band_settled": 1,
        "far_settled_since_freeze": 5,
        "in_band_stable": 1,
        "active_family": "H-SKIP-RICH-YES",
        "delta": 0.04,
    }
    theta_path().write_text(json.dumps(payload), encoding="utf-8")
    got = theta.load_theta()
    assert got["theta"] == pytest.approx(0.81)
    assert got["search_settled_since_freeze"] == 6
    assert got["in_band_settled"] == 1
    assert got["far_settled_since_freeze"] == 5
    assert got["family_starvations"] == {}
    assert got["advance_owed"] == ""


def test_n39_zero_inband_does_not_starve(honer_tmp):
    from golf_offshoot.honer_15m.picker import apply_search_starvation

    st = theta.load_theta()
    st["theta"] = 0.81
    st["last_declared_theta"] = 0.75
    st["search_settled_since_freeze"] = 39
    st["in_band_settled"] = 0
    theta.save_theta(st)
    assert apply_search_starvation() is None
    live = theta.load_theta()
    assert live["theta"] == pytest.approx(0.81)
    assert live["active_family"] == "H-SKIP-RICH-YES"


def test_n40_zero_inband_resets_to_start_and_retires(honer_tmp):
    from golf_offshoot.honer_15m.freeze import load_trials
    from golf_offshoot.honer_15m.library import is_retired, load_library
    from golf_offshoot.honer_15m.picker import apply_search_starvation
    from golf_offshoot.honer_15m.policy import knob_vector

    st = theta.load_theta()
    st["theta"] = 0.81
    st["last_declared_theta"] = 0.75
    st["search_settled_since_freeze"] = 40
    st["in_band_settled"] = 0
    st["far_settled_since_freeze"] = 40
    theta.save_theta(st)
    out = apply_search_starvation()
    assert out and out["reset"] is True
    assert out["advanced"] is False
    assert out["trials_unchanged"] is True
    live = theta.load_theta()
    assert live["theta"] == pytest.approx(START_THETA)
    assert live["last_declared_theta"] == pytest.approx(START_THETA)
    assert live["active_family"] == "H-SKIP-RICH-YES"
    assert live["search_settled_since_freeze"] == 0
    assert live["in_band_settled"] == 0
    assert live["family_starvations"]["H-SKIP-RICH-YES"] == 1
    assert load_trials()["trials_to_date"] == 0
    lib = load_library()
    assert lib["rows"][-1]["outcome"] == "search_untestable"
    assert lib["rows"][-1]["k"] == 0
    assert is_retired(knob_vector(family="H-SKIP-RICH-YES", theta=0.81, delta=0.04), lib)
    assert freeze.freeze_ready() is False


def test_n70_inband_19_starves_with_20_does_not(honer_tmp):
    from golf_offshoot.honer_15m.picker import apply_search_starvation

    st = theta.load_theta()
    st["theta"] = 0.81
    st["search_settled_since_freeze"] = 70
    st["in_band_settled"] = 20
    theta.save_theta(st)
    assert apply_search_starvation() is None
    st["in_band_settled"] = 19
    theta.save_theta(st)
    out = apply_search_starvation()
    assert out and out["reset"] is True
    assert theta.load_theta()["theta"] == pytest.approx(START_THETA)


def test_second_family1_starvation_does_not_switch_family(honer_tmp):
    from golf_offshoot.honer_15m.picker import apply_search_starvation
    from golf_offshoot.honer_15m.policy import FAMILY_RICH

    st = theta.load_theta()
    st["theta"] = 0.81
    st["search_settled_since_freeze"] = 40
    st["in_band_settled"] = 0
    st["family_starvations"] = {"H-SKIP-RICH-YES": 1}
    theta.save_theta(st)
    _seed_search_quotes(n=20, with_spread=20)
    out = apply_search_starvation()
    assert out and out.get("advanced") is False
    live = theta.load_theta()
    assert live["active_family"] == FAMILY_RICH
    assert live["theta"] == pytest.approx(START_THETA)
    assert live["advance_owed"] == ""
    assert freeze.load_trials()["trials_to_date"] == 0


def test_second_starvation_does_not_wait_on_quotes_to_start_family2(honer_tmp):
    from golf_offshoot.honer_15m.picker import apply_search_starvation, maybe_advance
    from golf_offshoot.honer_15m.policy import FAMILY_RICH

    st = theta.load_theta()
    st["theta"] = 0.81
    st["search_settled_since_freeze"] = 70
    st["in_band_settled"] = 19
    st["family_starvations"] = {"H-SKIP-RICH-YES": 1}
    theta.save_theta(st)
    _seed_search_quotes(n=20, with_spread=10)
    out = apply_search_starvation()
    assert out and out.get("reset") is True
    assert out.get("waiting_on_quotes") is not True
    live = theta.load_theta()
    assert live["active_family"] == FAMILY_RICH
    assert live["theta"] == pytest.approx(START_THETA)
    assert live["advance_owed"] == ""
    later = maybe_advance()
    assert later and later.get("advanced") is False
    assert theta.load_theta()["active_family"] == FAMILY_RICH


def test_family2_second_starvation_resets_without_incrementing_k(honer_tmp):
    from golf_offshoot.honer_15m.library import load_library
    from golf_offshoot.honer_15m.picker import apply_search_starvation
    from golf_offshoot.honer_15m.policy import FAMILY_SPREAD

    st = theta.load_theta()
    st["active_family"] = FAMILY_SPREAD
    st["delta"] = 0.09
    st["last_declared_delta"] = 0.04
    st["search_settled_since_freeze"] = 40
    st["in_band_settled"] = 0
    theta.save_theta(st)
    first = apply_search_starvation()
    assert first and first["reset"] is True
    live = theta.load_theta()
    assert live["delta"] == pytest.approx(0.04)
    assert live["active_family"] == FAMILY_SPREAD
    live["search_settled_since_freeze"] = 40
    live["in_band_settled"] = 0
    theta.save_theta(live)
    second = apply_search_starvation()
    assert second and second.get("reset") is True
    assert second.get("trials_unchanged") is True
    assert freeze.load_trials()["trials_to_date"] == 0
    assert load_library().get("catalog_exhausted") is not True


def test_starvation_skips_while_exam_open_and_does_not_increment_k(honer_tmp):
    from golf_offshoot.honer_15m.freeze import load_trials, save_exam_state
    from golf_offshoot.honer_15m.picker import apply_search_starvation

    save_exam_state(
        {
            "open": True,
            "parked": False,
            "n": 3,
            "frozen_theta": 0.79,
            "k_after": 1,
        }
    )
    st = theta.load_theta()
    st["theta"] = 0.81
    st["search_settled_since_freeze"] = 40
    st["in_band_settled"] = 0
    theta.save_theta(st)
    out = apply_search_starvation()
    assert out and out.get("deferred") is True
    assert theta.load_theta()["theta"] == pytest.approx(0.81)
    assert load_trials()["trials_to_date"] == 0
    save_exam_state({"open": False, "parked": True, "n": 3})
    acted = apply_search_starvation()
    assert acted and acted["reset"] is True
    assert load_trials()["trials_to_date"] == 0


def test_clip_wins_over_starvation_same_tick(honer_tmp):
    from golf_offshoot.honer_15m.library import load_library
    from golf_offshoot.honer_15m.picker import apply_search_starvation

    st = theta.load_theta()
    st["theta"] = 0.81
    st["search_settled_since_freeze"] = 40
    st["in_band_settled"] = 0
    st["clip_streak"] = 20
    theta.save_theta(st)
    out = apply_search_starvation()
    assert out and out.get("skipped") is True
    assert theta.load_theta()["theta"] == pytest.approx(0.81)
    assert load_library().get("rows") == []


def test_loop_search_settle_can_starve(honer_tmp):
    st = theta.load_theta()
    st["theta"] = 0.81
    st["search_settled_since_freeze"] = 39
    st["in_band_settled"] = 0
    theta.save_theta(st)
    books.record_action(
        "search",
        ticker="KXBTC15M-STARVE",
        window_id="w",
        action="fill",
        reason="x",
        posted_yes=0.48,
        theta=0.81,
        close_at="t",
    )
    loop.run_tick(
        [
            {
                "ticker": "KXBTC15M-STARVE",
                "window_id": "w",
                "paper_mark": 0.48,
                "is_open": False,
                "status": "determined",
                "close_time": "t",
                "result": "no",
            }
        ]
    )
    live = theta.load_theta()
    assert live["theta"] == pytest.approx(START_THETA)
    assert live["family_starvations"]["H-SKIP-RICH-YES"] == 1
    src = (PKG / "loop.py").read_text(encoding="utf-8")
    assert "apply_search_starvation" in src
    paper = (PKG.parent / "learning_lane_15m" / "paper.py").read_text(encoding="utf-8")
    assert "golf_offshoot.honer_15m" not in paper


FACTORY_RULES = Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_RULES.json"


def _quoted_market(ticker: str, *, posted: float = 0.60, spread: float = 0.12, result: str = "") -> dict:
    ask = posted
    bid = round(posted - spread, 2) if spread else None
    return {
        "ticker": ticker,
        "window_id": "w",
        "paper_mark": posted,
        "yes_ask": posted,
        "yes_bid": bid,
        "is_open": True,
        "status": "active",
        "close_time": "t",
        "result": result,
    }


def test_clip_starts_cover_both_family_clips():
    from golf_offshoot.honer_15m.brains import (
        family1_start_thetas,
        family2_start_deltas,
        planned_brain_items,
        spec_matches_clip,
    )

    f1 = family1_start_thetas()
    f2 = family2_start_deltas()
    assert f1[0] == pytest.approx(0.55)
    assert f1[-1] == pytest.approx(0.90)
    assert f2[0] == pytest.approx(0.02)
    assert f2[-1] == pytest.approx(0.12)
    assert len(f1) == 19
    assert len(f2) == 11
    items = planned_brain_items()
    assert len(items) == 30
    assert items[0]["id"] == "f1-start-055"
    assert items[18]["id"] == "f1-start-090"
    assert items[19]["id"] == "f2-start-002"
    assert items[-1]["id"] == "f2-start-012"
    assert spec_matches_clip()


def test_dating_clip_does_not_increment_factory_or_honer_k(honer_tmp):
    import json

    from golf_offshoot.honer_15m.brains import date_unused_clip_slots, iter_brain_ids, planned_brain_items

    factory_k = json.loads(FACTORY_RULES.read_text(encoding="utf-8"))["trials_to_date"]
    honer_k = freeze.load_trials().get("trials_to_date") or 0
    first = date_unused_clip_slots()
    assert len(first["items"]) == len(planned_brain_items())
    assert first["trials_unchanged"] is True
    assert freeze.load_trials()["trials_to_date"] == honer_k
    assert json.loads(FACTORY_RULES.read_text(encoding="utf-8"))["trials_to_date"] == factory_k
    date_unused_clip_slots()
    assert freeze.load_trials()["trials_to_date"] == honer_k
    assert len(iter_brain_ids()) == 30
    src = (PKG / "brains.py").read_text(encoding="utf-8")
    assert "LEARNING_LANE_15M_RULES" not in src
    assert "record_trial" not in src


def test_run_tick_dates_unused_clip_slots(honer_tmp):
    import json

    factory_k = json.loads(FACTORY_RULES.read_text(encoding="utf-8"))["trials_to_date"]
    out = loop.run_tick([])
    from golf_offshoot.honer_15m.brains import iter_brain_ids, planned_brain_items

    assert len(iter_brain_ids()) == len(planned_brain_items())
    assert out["search_brains"] == 30
    assert out["http_fetches"] == 0
    assert freeze.load_trials()["trials_to_date"] == 0
    assert json.loads(FACTORY_RULES.read_text(encoding="utf-8"))["trials_to_date"] == factory_k


def test_two_brains_step_independently(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots

    date_unused_clip_slots()
    ticker = "KXBTC15M-IND"
    open_m = {
        "ticker": ticker,
        "window_id": "w",
        "paper_mark": 0.70,
        "is_open": True,
        "status": "active",
        "close_time": "t",
        "result": "",
    }
    loop.run_tick([open_m])
    loop.run_tick(
        [
            {
                **open_m,
                "is_open": False,
                "status": "determined",
                "result": "no",
            }
        ]
    )
    with brain_scope("f1-start-065"):
        assert theta.load_theta()["theta"] == pytest.approx(0.65)
    with brain_scope("f1-start-075"):
        assert theta.load_theta()["theta"] == pytest.approx(0.73)
    with brain_scope("f1-start-085"):
        assert theta.load_theta()["theta"] == pytest.approx(0.85)


def test_file_order_first_ready_brain_takes_exam_chair(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots

    date_unused_clip_slots()
    with brain_scope("f1-start-065"):
        st = theta.load_theta()
        st["in_band_settled"] = 20
        st["in_band_stable"] = 5
        st["theta"] = 0.71
        theta.save_theta(st)
    exam = freeze.fire_freeze()
    assert exam and exam["open"] is True
    assert exam["brain_id"] == "f1-start-065"
    assert exam["frozen_theta"] == pytest.approx(0.71)
    assert freeze.load_trials()["trials_to_date"] == 1
    with brain_scope("f1-start-075"):
        assert theta.load_theta()["theta"] == pytest.approx(START_THETA)


def test_open_exam_blocks_second_freeze_including_family2(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots
    from golf_offshoot.honer_15m.invariants import run_invariants
    from golf_offshoot.honer_15m.policy import FAMILY_SPREAD

    date_unused_clip_slots()
    with brain_scope("f1-start-065"):
        st = theta.load_theta()
        st["in_band_settled"] = 20
        st["in_band_stable"] = 5
        st["theta"] = 0.71
        theta.save_theta(st)
    assert freeze.fire_freeze()
    with brain_scope("f2-start-004"):
        st = theta.load_theta()
        st["delta"] = 0.07
        st["in_band_settled"] = 20
        st["in_band_stable"] = 5
        theta.save_theta(st)
        assert theta.load_theta()["active_family"] == FAMILY_SPREAD
    assert freeze.freeze_ready() is False
    assert freeze.fire_freeze() is None
    assert freeze.load_trials()["trials_to_date"] == 1
    payload = run_invariants()
    one = next(row for row in payload["checks"] if row["id"] == "one_exam_open_max")
    assert one["state"] == "PASS"


def test_frozen_exam_knobs_ignore_search_steps(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots

    date_unused_clip_slots()
    with brain_scope("f1-start-075"):
        st = theta.load_theta()
        st["in_band_settled"] = 20
        st["in_band_stable"] = 5
        st["theta"] = 0.81
        theta.save_theta(st)
    exam = freeze.fire_freeze()
    assert exam["frozen_theta"] == pytest.approx(0.81)
    with brain_scope("f1-start-065"):
        theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.68)
    with brain_scope("f1-start-075"):
        theta.step_search_theta(action="fill", kalshi_result="no", posted_yes=0.68)
    assert freeze.load_exam_state()["frozen_theta"] == pytest.approx(0.81)


def test_search_ledgers_not_summed_and_hub_has_no_combined(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots
    from golf_offshoot.honer_15m.hub_block import sandbox_html
    from golf_offshoot.honer_15m.paths import brains_manifest_path

    date_unused_clip_slots()
    loop.run_tick([_quoted_market("KXBTC15M-BOTH")])
    with brain_scope("f1-start-075"):
        a = books.load_ledger("search")["betting_pnl"]
        n_a = books.load_ledger("search")["entries"]
    with brain_scope("f2-start-004"):
        b = books.load_ledger("search")["betting_pnl"]
        n_b = books.load_ledger("search")["entries"]
    exam_pnl = books.load_ledger("exam")["betting_pnl"]
    assert n_a >= 1
    assert n_b >= 1
    assert a + b != exam_pnl or exam_pnl == 0
    html = sandbox_html().lower()
    assert "combined" not in html
    assert "winner" not in html
    text = brains_manifest_path().read_text(encoding="utf-8").lower()
    assert "combined" not in text
    assert "winner" not in text
    from golf_offshoot.honer_15m import brains as brains_mod

    assert not hasattr(brains_mod, "sum_search_ledgers")


def test_both_families_search_on_one_sidecar_tick(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD

    date_unused_clip_slots()
    out = loop.run_tick([_quoted_market("KXBTC15M-PAR")])
    assert out["http_fetches"] == 0
    assert out["search_brains"] == 30
    with brain_scope("f1-start-075"):
        assert theta.load_theta()["active_family"] == FAMILY_RICH
        assert books.load_ledger("search")["entries"] == 1
        row = books.load_decisions("search")["KXBTC15M-PAR"]
        assert row["action"] == "fill"
    with brain_scope("f2-start-004"):
        assert theta.load_theta()["active_family"] == FAMILY_SPREAD
        assert books.load_ledger("search")["entries"] == 1
        row = books.load_decisions("search")["KXBTC15M-PAR"]
        assert row["action"] == "skip"
    assert freeze.load_trials()["trials_to_date"] == 0


def test_incomplete_quotes_skip_family2_tick(honer_tmp):
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots

    date_unused_clip_slots()
    market = {
        "ticker": "KXBTC15M-NOQ",
        "window_id": "w",
        "paper_mark": 0.60,
        "is_open": True,
        "status": "active",
        "close_time": "t",
        "result": "",
    }
    loop.run_tick([market])
    with brain_scope("f1-start-075"):
        assert books.load_ledger("search")["entries"] == 1
    with brain_scope("f2-start-004"):
        assert books.load_ledger("search")["entries"] == 0


def test_consult_armed_series_lane_hold(honer_tmp):
    from golf_offshoot.data_feeds.kalshi_15m import (
        ALLOWED_SERIES,
        SeriesNotAllowedError,
        TickerParseError,
        parse_event,
    )
    from golf_offshoot.honer_15m.keep import load_bar
    from golf_offshoot.operator_surface.lanes import parse_lane

    assert loop.TRADING_ARMED is False
    assert ALLOWED_SERIES == "KXBTC15M"
    try:
        parse_event(
            {
                "event_ticker": "KXETH15M-26SEP071400",
                "series_ticker": "KXETH15M",
                "ticker": "KXETH15M-26SEP071400",
            }
        )
        raise AssertionError("ETH must be refused")
    except (SeriesNotAllowedError, TickerParseError):
        pass
    assert parse_lane("honer_15m") == "golf"
    assert load_bar().get("consult_enabled") is not True
    loop.run_tick([])
    assert LIVE_15M_NAME not in {p.name for p in honer_tmp.rglob("*")}
    assert "kalshi_15m_exports" not in {p.name for p in honer_tmp.rglob("*")}


def test_freeze_meter_names_file_order_ready_brain_not_canonical(honer_tmp):
    from golf_offshoot.honer_15m.board import collect_standing, freeze_meter
    from golf_offshoot.honer_15m.brains import brain_scope, date_unused_clip_slots
    from golf_offshoot.honer_15m.hub_block import sandbox_html
    from golf_offshoot.honer_15m.picker import queue_status

    date_unused_clip_slots()
    with brain_scope("f1-start-065"):
        st = theta.load_theta()
        st["in_band_settled"] = 20
        st["in_band_stable"] = 5
        st["theta"] = 0.71
        theta.save_theta(st)
    with brain_scope("f1-start-075"):
        st = theta.load_theta()
        st["in_band_settled"] = 20
        st["in_band_stable"] = 5
        st["theta"] = 0.81
        theta.save_theta(st)
    qs = queue_status()
    assert qs["next_ready"] == "f1-start-065"
    assert qs["n_hunts"] == 30
    line = freeze_meter()
    assert "f1-start-065" in line
    assert "f1-start-075" not in line
    standing = collect_standing()
    assert standing.freeze_meter == line
    assert "f1-start-065" in standing.where_it_stands
    assert "71¢" in standing.where_it_stands
    assert "81¢" not in standing.where_it_stands
    html = sandbox_html().lower()
    assert "canonical hunt" in html
    assert "not a sum" in html
    assert "combined" not in html
    assert "winner" not in html


def test_watch_files_include_clip_spec():
    from golf_offshoot.honer_15m.watch import _honer_watch_files

    names = {path.name for path in _honer_watch_files()}
    assert "brains.py" in names
    assert "HONER_15M_SEARCH_BRAINS.json" in names
    assert "HONER_15M_CATALOG.json" in names


def test_catalog_exhausted_parks_search_and_leaves_exam_closed(honer_tmp):
    import json

    from golf_offshoot.honer_15m.library import load_library, save_library
    from golf_offshoot.honer_15m.paths import family_amend_path, last_tick_path

    lib = load_library()
    lib["catalog_exhausted"] = True
    save_library(lib)
    out = loop.run_tick([_quoted_market("KXBTC15M-PARK1")])
    assert out["search_parked"] is True
    assert out["froze"] is False
    assert freeze.exam_is_open() is False
    assert freeze.fire_freeze() is None
    assert books.load_ledger("search")["entries"] == 0
    assert books.load_ledger("exam")["entries"] == 0
    tick = json.loads(last_tick_path().read_text(encoding="utf-8"))
    assert tick["search_parked"] is True
    assert tick["family_amend_owed"] is True
    stamp = json.loads(family_amend_path().read_text(encoding="utf-8"))
    assert stamp["owed"] is True
    assert "catalog_exhausted" in stamp["reasons"]
    assert stamp["third_family"] is False
    assert "pnl" not in stamp
    assert "mean_d" not in stamp
    from golf_offshoot.honer_15m.catalog import catalog_ids

    assert catalog_ids() == ["H-SKIP-RICH-YES", "H-SKIP-WIDE-SPREAD"]


def test_catalog_exhausted_settles_existing_search_without_new_fills(honer_tmp):
    loop.run_tick([_quoted_market("KXBTC15M-KEEP")])
    assert books.load_ledger("search")["entries"] == 1
    from golf_offshoot.honer_15m.library import load_library, save_library

    lib = load_library()
    lib["catalog_exhausted"] = True
    save_library(lib)
    loop.run_tick(
        [_quoted_market("KXBTC15M-KEEP", result="yes"), _quoted_market("KXBTC15M-NEW")]
    )
    assert books.load_ledger("search")["entries"] == 1
    assert "KXBTC15M-NEW" not in books.load_decisions("search")
    assert books.load_decisions("search")["KXBTC15M-KEEP"]["kalshi_result"] == "yes"
    assert int(books.load_ledger("search")["settled"] or 0) >= 1
    assert freeze.exam_is_open() is False


def test_family_amend_owed_from_completed_dead_not_exam_pnl(honer_tmp):
    import json

    from golf_offshoot.honer_15m.family_amend import (
        family_amend_owed_from_files,
        stamp_family_amend,
    )
    from golf_offshoot.honer_15m.library import append_exam_row
    from golf_offshoot.honer_15m.paths import exam_score_path, family_amend_path
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, knob_vector

    assert family_amend_owed_from_files() is False
    exam_score_path().write_text(
        json.dumps(
            {
                "outcome": "completed_dead",
                "mean_d": 99.0,
                "exam_pnl_sum": 999.0,
                "survives": False,
            }
        ),
        encoding="utf-8",
    )
    assert family_amend_owed_from_files() is True
    stamp = stamp_family_amend()
    assert stamp["owed"] is True
    assert stamp["reasons"] == ["completed_dead"]
    assert stamp["exam_completed_dead"] is True
    assert stamp["catalog_exhausted"] is False
    assert "mean_d" not in stamp
    assert "exam_pnl_sum" not in stamp
    assert "pnl" not in stamp
    on_disk = json.loads(family_amend_path().read_text(encoding="utf-8"))
    assert "mean_d" not in on_disk
    append_exam_row(
        k=1,
        family=FAMILY_RICH,
        knobs=knob_vector(family=FAMILY_RICH, theta=0.79, delta=0.02),
        outcome="completed_dead",
    )
    standing = None
    from golf_offshoot.honer_15m.board import collect_standing

    standing = collect_standing()
    assert "99" not in standing.where_it_stands
    assert family_amend_owed_from_files() is True


def test_mark_catalog_exhausted_from_retired_hunts_not_pnl(honer_tmp):
    from golf_offshoot.honer_15m.library import (
        append_exam_row,
        hunts_cannot_freeze,
        load_library,
        mark_catalog_exhausted,
    )
    from golf_offshoot.honer_15m.picker import maybe_advance
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, knob_vector
    from golf_offshoot.honer_15m.theta import current_vector, load_theta

    st = load_theta()
    vector = current_vector(st)
    append_exam_row(k=1, family=FAMILY_RICH, knobs=vector, outcome="completed_dead")
    assert hunts_cannot_freeze() is True
    mark_catalog_exhausted()
    assert load_library().get("catalog_exhausted") is True
    assert maybe_advance() is None
    out = loop.run_tick([_quoted_market("KXBTC15M-AFTER")])
    assert out["search_parked"] is True
    assert books.load_ledger("search")["entries"] == 0
    assert freeze.exam_is_open() is False
    from golf_offshoot.honer_15m.catalog import catalog_ids

    assert catalog_ids() == ["H-SKIP-RICH-YES", "H-SKIP-WIDE-SPREAD"]


def test_live_clip_grid_not_exhausted_after_one_dead_exam(honer_tmp):
    from golf_offshoot.honer_15m.brains import date_unused_clip_slots
    from golf_offshoot.honer_15m.library import (
        append_exam_row,
        hunts_cannot_freeze,
        load_library,
        mark_catalog_exhausted,
    )
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, knob_vector

    date_unused_clip_slots()
    append_exam_row(
        k=1,
        family=FAMILY_RICH,
        knobs=knob_vector(family=FAMILY_RICH, theta=0.79, delta=0.04),
        outcome="completed_dead",
    )
    assert hunts_cannot_freeze() is False
    mark_catalog_exhausted()
    assert load_library().get("catalog_exhausted") is not True
    from golf_offshoot.honer_15m.family_amend import family_amend_owed_from_files

    assert family_amend_owed_from_files() is True
    out = loop.run_tick([_quoted_market("KXBTC15M-GRID")])
    assert out["search_parked"] is not True
    assert books.load_ledger("search")["entries"] >= 1
    assert freeze.load_trials()["trials_to_date"] == 0


