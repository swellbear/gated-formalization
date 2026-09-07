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


def test_paper_deposit_refused_on_15m(capsys):
    assert main(["paper-deposit", "--lane", "learning_lane_15m", "--amount", "10"]) == 2
    assert "never deposit/withdraw/transfer" in capsys.readouterr().out.lower()
