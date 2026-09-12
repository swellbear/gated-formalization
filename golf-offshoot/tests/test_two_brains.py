"""Action-only two-brains journal. No money fields."""

from __future__ import annotations

from golf_offshoot.honer_15m.books import record_action
from golf_offshoot.honer_15m.paths import set_honer_root_override
from golf_offshoot.learning_lane_15m.paper import record_decision
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.two_brains import last_disagreements, load_journal, set_two_brains_root_override, sync


MONEY = ("pnl", "d", "bankroll", "winner")


def test_skip_vs_fill_disagreement_has_no_money(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_honer_root_override(tmp_path / "honer_15m")
    set_two_brains_root_override(tmp_path / "two_brains")
    try:
        record_decision(
            "KXBTC15M-26SEP091400-00",
            {
                "ticker": "KXBTC15M-26SEP091400-00",
                "window_id": "w",
                "rule_id": "R-SKIP-2TO1-FAVORITE",
                "action": "skip",
                "posted_yes": 0.81,
                "close_at": "2026-09-09T18:00:00Z",
            },
        )
        record_action(
            "search",
            ticker="KXBTC15M-26SEP091400-00",
            window_id="w",
            action="fill",
            reason="below theta",
            posted_yes=0.48,
            theta=0.81,
            close_at="2026-09-09T18:00:00Z",
        )
        rows = sync()
        assert rows
        row = next(r for r in rows if r["ticker"] == "KXBTC15M-26SEP091400-00")
        assert row["factory_action"] == "skip"
        assert row["honer_search_action"] == "fill"
        for key in MONEY:
            assert key not in row
        blob = str(row)
        assert "$" not in blob
        assert "pnl" not in blob
        disagree = last_disagreements(8)
        assert disagree
        assert disagree[0]["ticker"] == "KXBTC15M-26SEP091400-00"
        journal = load_journal()
        assert all(key not in item for item in journal for key in MONEY)
    finally:
        set_15m_root_override(None)
        set_honer_root_override(None)
        set_two_brains_root_override(None)


def test_this_window_paint_does_not_sync(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_honer_root_override(tmp_path / "honer_15m")
    set_two_brains_root_override(tmp_path / "two_brains")

    def boom(*args, **kwargs):
        raise AssertionError("hub paint must not rewrite the two-brains journal")

    monkeypatch.setattr("golf_offshoot.two_brains.journal.sync", boom)
    try:
        from golf_offshoot.operator_surface.this_window import this_window_html

        html = this_window_html()
        assert "This window" in html
        assert "This window — one clock" in html
        assert "two brains" not in html
        assert "consult is off" in html
        assert "Last disagreements" in html
        assert 'class="gk-fold"' in html
        assert "<details" in html
        assert "<summary>" in html
    finally:
        set_15m_root_override(None)
        set_honer_root_override(None)
        set_two_brains_root_override(None)


def test_this_window_two_brains_when_consult_live(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_honer_root_override(tmp_path / "honer_15m")
    set_two_brains_root_override(tmp_path / "two_brains")
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.this_window.consult_is_live", lambda: True
    )
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.this_window.factory_chair_selects", lambda: True
    )
    try:
        from golf_offshoot.operator_surface.this_window import factory_title, this_window_html

        assert factory_title() == "Factory — live 70"
        html = this_window_html()
        assert "This window — two brains, one clock" in html
        assert "consult is off" not in html
        assert "Honer search (observation)" not in html
    finally:
        set_15m_root_override(None)
        set_honer_root_override(None)
        set_two_brains_root_override(None)


def test_this_window_html_has_no_combined(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_honer_root_override(tmp_path / "honer_15m")
    set_two_brains_root_override(tmp_path / "two_brains")
    try:
        from golf_offshoot.operator_surface.this_window import this_window_html

        html = this_window_html()
        assert "combined" not in html.lower()
        assert "winner" not in html.lower()
        assert "Last disagreements" in html
        assert 'class="gk-fold"' in html
    finally:
        set_15m_root_override(None)
        set_honer_root_override(None)
        set_two_brains_root_override(None)
