import pytest

from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.operator_surface.hub import GOLF_VIZ_SLOTS, render_hub
from golf_offshoot.operator_surface.lanes import (
    DEFAULT_LANE,
    SELECTOR_FIELD,
    lane_header_name,
    parse_lane,
    parse_lane_from_mapping,
)
from golf_offshoot.__main__ import main


def test_default_lane_is_golf():
    assert DEFAULT_LANE == "golf"
    assert parse_lane(None) == "golf"
    assert parse_lane("") == "golf"
    assert parse_lane("unknown") == "golf"
    assert parse_lane("15m") == "golf"
    assert parse_lane("learning_lane_15m") == "learning_lane_15m"
    assert parse_lane_from_mapping({}) == "golf"
    assert parse_lane_from_mapping({SELECTOR_FIELD: "learning_lane_15m"}) == "learning_lane_15m"
    assert parse_lane_from_mapping({SELECTOR_FIELD: "15m"}) == "golf"


def test_hub_golf_default_chrome(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = render_hub()
        golf = render_hub("golf")
    finally:
        set_15m_root_override(None)
    assert page == golf
    assert "Active lane: Golf Phase 1" in page
    assert 'data-lane="golf"' in page
    assert 'data-journal="golf"' in page
    assert "Journal: golf" in page
    assert "PHASE 1 OBSERVATION" in page
    assert "Trading NOT ARMED" in page
    assert "PAPER OBSERVATION ONLY" in page
    assert "AI: NO CASH IN/OUT" in page
    assert "LEARNING LANE" not in page
    assert "WC1" in page
    assert "Ill" in page
    assert 'name="lane"' in page
    assert 'value="golf"' in page
    assert 'value="learning_lane_15m"' in page
    assert 'value="15m"' not in page
    assert "15-min Kalshi (learning)" in page


def test_hub_15m_no_golf_viz(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = render_hub("learning_lane_15m")
    finally:
        set_15m_root_override(None)
    assert "Active lane: 15-min Kalshi (learning)" in page
    assert 'data-lane="learning_lane_15m"' in page
    assert 'data-journal="15m"' in page
    assert "Journal: 15m" in page
    assert "LEARNING LANE" in page
    assert "not yet available" in page
    assert "not a golf WC1 edge" in page.lower() or "not a golf WC1 edge" in page
    for slot in GOLF_VIZ_SLOTS:
        assert f">{slot}<" not in page and f"{slot}</h3>" not in page
    assert "golf viz slot" not in page
    assert "Journal: golf" not in page
    assert "combined" in page.lower() or "No combined" in page


def test_lane_header_copy():
    assert lane_header_name("golf") == "Golf Phase 1"
    assert lane_header_name("learning_lane_15m") == "15-min Kalshi (learning)"
    assert lane_header_name("15m") == "Golf Phase 1"


def test_hub_cli_prints_golf_html(capsys):
    assert main(["hub"]) == 0
    out = capsys.readouterr().out
    assert "Active lane: Golf Phase 1" in out
    assert "Trading NOT ARMED" in out


def test_hub_cli_lane_15m(capsys, tmp_path):
    set_15m_root_override(tmp_path)
    try:
        assert main(["hub", "--lane", "learning_lane_15m"]) == 0
    finally:
        set_15m_root_override(None)
    out = capsys.readouterr().out
    assert "Active lane: 15-min Kalshi (learning)" in out
    assert "LEARNING LANE" in out


def test_hub_cli_rejects_short_15m_alias():
    with pytest.raises(SystemExit) as exc:
        main(["hub", "--lane", "15m"])
    assert exc.value.code == 2


def test_paper_deposit_refused_on_15m(capsys):
    assert main(["paper-deposit", "--lane", "learning_lane_15m", "--amount", "10"]) == 2
    assert "never deposit/withdraw/transfer" in capsys.readouterr().out.lower()


def test_desktop_shell_html_has_lane_selector_and_hides_golf_viz_on_15m(tmp_path):
    from golf_offshoot.operator_surface.app import build_surface, render_html, render_text

    set_15m_root_override(tmp_path)
    try:
        golf = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))
        page = render_html(
            build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="learning_lane_15m")
        )
        text = render_text(
            build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="learning_lane_15m")
        )
    finally:
        set_15m_root_override(None)
    assert 'name="lane"' in golf
    assert 'value="learning_lane_15m"' in golf
    assert 'value="15m"' not in golf
    assert 'value="15m"' not in page
    assert "LEARNING LANE" in page
    assert "KXBTC15M" in page
    assert "paper autobet" in page.lower()
    assert "No golf WC1" in page
    assert "Two boxes" in page
    assert "Factory — live 70" in page
    assert 'id="honer"' in page
    assert 'id="farm"' in page
    assert "This window" in page
    assert 'name="deposit"' not in page
    assert 'name="withdraw"' not in page
    assert "lane=learning_lane_15m" in text


def test_desktop_15m_loop_notifies_once_and_keeps_paper_settle(tmp_path, monkeypatch):
    from golf_offshoot.data_feeds.kalshi_15m import Kalshi15mFeed
    from golf_offshoot.operator_surface.runner import run_15m_loop

    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.observability.hub_manifest_path",
        lambda: tmp_path / "hub" / "manifest.json",
    )
    monkeypatch.setenv("NTFY_TOPIC", "golf-bmw-test")
    set_15m_root_override(tmp_path / "kalshi_15m")
    calls = []

    def _fake(body, **kwargs):
        calls.append(body)
        return "https://ntfy.sh/golf-bmw-test"

    monkeypatch.setattr("golf_offshoot.operator_surface.notify.publish_ntfy", _fake)
    feed = Kalshi15mFeed()

    def fake_get(url, *, label, ttl_seconds, refresh):
        if "events" in url:
            return {
                "events": [
                    {
                        "event_ticker": "KXBTC15M-26SEP071400",
                        "series_ticker": "KXBTC15M",
                        "settlement_sources": [
                            {"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}
                        ],
                    }
                ]
            }
        return {
            "markets": [
                {
                    "ticker": "KXBTC15M-26SEP071400-00",
                    "event_ticker": "KXBTC15M-26SEP071400",
                    "status": "active",
                    "result": "yes",
                    "yes_ask_dollars": "0.6100",
                }
            ]
        }

    monkeypatch.setattr(feed, "_get", fake_get)
    try:
        rec = run_15m_loop(notify=True, refresh=False, feed=feed)
    finally:
        set_15m_root_override(None)
    assert rec.ok
    assert rec.extras["lane"] == "learning_lane_15m"
    assert rec.extras["paper_fills"] == 1
    assert rec.notice is not None
    assert rec.notice.sent is True
    assert len(calls) == 1
    assert "LEARNING LANE" in calls[0]
    assert "learning_lane_15m" in calls[0]
    assert "NOT ARMED" in calls[0]


def test_notify_golf_completion_does_not_use_15m_title(monkeypatch):
    from golf_offshoot.operator_surface.notify import notify_run_complete

    monkeypatch.setenv("NTFY_TOPIC", "golf-bmw-test")
    calls = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.notify.publish_ntfy",
        lambda body, **kwargs: calls.append(body) or "https://ntfy.sh/x",
    )
    notice = notify_run_complete(command="live", ok=True, event_id="401811963", detail="done")
    assert notice.sent is True
    assert "LEARNING LANE" not in calls[0]
    assert "learning_lane_15m" not in calls[0]
