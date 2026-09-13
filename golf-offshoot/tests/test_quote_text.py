"""Kalshi quote display: full source string, never cents, never invented digits."""

from golf_offshoot.data_feeds.kalshi_15m import paper_mark_quote, parse_market, quote_abs_diff, quote_text
from golf_offshoot.learning_lane_15m.illustrate import WindowRow, _mark_cell


EVENT = {
    "event_ticker": "KXBTC15M-26SEP071415",
    "series_ticker": "KXBTC15M",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

OPEN_MARKET = {
    "ticker": "KXBTC15M-26SEP071415-15",
    "event_ticker": "KXBTC15M-26SEP071415",
    "status": "active",
    "result": "",
    "yes_ask_dollars": "0.5200",
    "yes_bid_dollars": "0.4800",
    "last_price_dollars": "0.5100",
    "title": "BTC price up in next 15 mins?",
}


def test_quote_text_keeps_kalshi_string():
    assert quote_text("0.6150") == "0.6150"
    assert quote_text("0.6100") == "0.6100"
    assert quote_text("0.123456") == "0.123456"
    assert quote_text("0.123456789") == "0.123456789"
    assert quote_text(" 0.36 ") == "0.36"
    assert quote_text("") == "n/a"
    assert quote_text(None) == "n/a"


def test_quote_text_float_is_round_trip_not_cents():
    assert quote_text(0.615) == "0.615"
    assert quote_text(0.36) == "0.36"
    assert quote_text(0.01) == "0.01"
    assert quote_text(0.81) == "0.81"
    assert "¢" not in quote_text(0.36)
    assert quote_text(0.615) != "0.6150"


def test_quote_abs_diff_uses_printed_decimals():
    assert quote_abs_diff(0.81, 0.75) == "0.06"
    assert quote_abs_diff(0.81, 0.81) == "0.00"
    assert quote_abs_diff("0.47", "0.46") == "0.01"
    assert quote_abs_diff("0.5200", "0.4800") == "0.04"


def test_quote_text_does_not_dump_ieee_float_residue():
    dirty_spread = 0.47 - 0.46
    dirty_mid = 0.93 - 0.465
    assert str(dirty_spread) == "0.010000000000000009"
    assert str(dirty_mid) == "0.46499999999999997"
    assert quote_text(dirty_spread) == "0.01"
    assert quote_text(dirty_mid) == "0.465"
    assert quote_text("0.010000000000000009") == "0.01"
    assert quote_text("0.46499999999999997") == "0.465"
    assert "0.010000000000000009" not in quote_text(dirty_spread)
    assert "0.46499999999999997" not in quote_text(dirty_mid)
    assert quote_text("0.6150") == "0.6150"
    assert quote_text("0.123456") == "0.123456"
    assert quote_text(0.615) != "0.6150"
    assert "¢" not in quote_text(dirty_spread)


def test_paper_mark_quote_mid_keeps_source_places():
    assert (
        paper_mark_quote(
            yes_bid_raw="0.6100",
            yes_ask_raw="0.6200",
            last_raw="0.6100",
            mark=0.615,
        )
        == "0.6150"
    )
    assert (
        paper_mark_quote(
            yes_bid_raw="0.61",
            yes_ask_raw="0.62",
            last_raw=None,
            mark=0.615,
        )
        == "0.615"
    )
    assert (
        paper_mark_quote(
            yes_bid_raw=None,
            yes_ask_raw=None,
            last_raw="0.6150",
            mark=0.615,
        )
        == "0.6150"
    )


def test_parse_market_carries_kalshi_mid_string():
    parsed = parse_market(OPEN_MARKET, event=EVENT)
    assert parsed["paper_mark"] == 0.50
    assert parsed["paper_mark_text"] == "0.5000"


def test_honer_and_paper_print_the_same_kalshi_string():
    text = "0.6150"
    from golf_offshoot.honer_15m.board import HonerRow

    honer = HonerRow(
        ticker="KXBTC15M-26SEP091400-00",
        window_id="w",
        window_et="14:00 ET",
        action="fill",
        action_label="Filled YES",
        posted_yes=0.615,
        theta=0.79,
        why="x",
        why_short="x",
        kalshi_result="",
        pnl=None,
        pnl_text="n/a",
        source="honer",
        book="search",
        posted_yes_text=text,
    )
    paper = WindowRow(
        ticker="KXBTC15M-26SEP091400-00",
        window_id="w",
        settle_status="open",
        kalshi_result="",
        settle_src="paper/x.json",
        paper_join=True,
        paper_side="YES",
        paper_mark=0.615,
        open_at=None,
        close_at=None,
        paper_mark_text=text,
    )
    assert honer.posted_display() == text
    assert _mark_cell(paper) == text
    assert honer.posted_display() == _mark_cell(paper)
