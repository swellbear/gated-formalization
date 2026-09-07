from pathlib import Path

from golf_offshoot.data_feeds.kalshi_15m import (
    CF_INDEX_ID,
    CFB_WS_AVERAGE_ROLE,
    PrivateEndpointRefused,
    TRADING_ARMED,
    assert_public_read_url,
)
from golf_offshoot.learning_lane_15m.paper import refuse_cash_transfer
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.settle import (
    DemoFillSettleRefused,
    DiyCfbAverageRefused,
    SETTLE_NEVER,
    SETTLE_PENDING,
    classify_settle,
    refuse_diy_cfb_average,
)
from golf_offshoot.operator_surface.hub import render_hub


def test_trading_never_armed():
    assert TRADING_ARMED is False


def test_no_trade_or_cash_endpoints():
    for url in (
        "https://api.elections.kalshi.com/trade-api/v2/orders",
        "https://api.elections.kalshi.com/trade-api/v2/exchange/withdraw",
        "https://api.elections.kalshi.com/trade-api/v2/exchange/transfers",
        "https://api.elections.kalshi.com/trade-api/v2/login",
    ):
        try:
            assert_public_read_url(url)
            raise AssertionError(url)
        except PrivateEndpointRefused:
            pass


def test_refuse_deposit_withdraw_transfer():
    for kind in ("deposit", "withdraw", "transfer"):
        try:
            refuse_cash_transfer(kind)
            raise AssertionError(kind)
        except RuntimeError as exc:
            assert "never deposit/withdraw/transfer" in str(exc)


def test_diy_cfb_average_is_not_official_settle():
    try:
        refuse_diy_cfb_average([79100.1] * 60)
        raise AssertionError("DIY average must be refused")
    except DiyCfbAverageRefused:
        pass


def test_demo_fill_is_not_a_settle():
    try:
        classify_settle({"ticker": "demo", "result": "yes"}, demo=True)
        raise AssertionError("demo settle must be refused")
    except DemoFillSettleRefused:
        pass


def test_no_invent_win_lose_without_kalshi_result():
    pending = classify_settle(
        {
            "ticker": "KXBTC15M-26SEP071415-15",
            "event_ticker": "KXBTC15M-26SEP071415",
            "result": "",
            "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
        }
    )
    assert pending.settle_status == SETTLE_PENDING
    assert pending.won is None
    never = classify_settle(
        {
            "ticker": "KXBTC15M-26SEP071415-15",
            "result": "yes",
            "settlement_sources": [],
        }
    )
    assert never.settle_status == SETTLE_NEVER
    assert never.won is None


def test_hub_has_no_kalshi_cash_ui(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = render_hub("learning_lane_15m")
    finally:
        set_15m_root_override(None)
    low = page.lower()
    assert "deposit" not in low
    assert "withdraw" not in low
    assert "transfer" not in low
    assert "trading not armed" in low
    assert "ai: no cash in/out" in low
    assert "learning lane" in low


def test_leftovers_stay_proposed_not_softened():
    text = Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M.md"
    body = text.read_text(encoding="utf-8")
    leftovers = body.split("Week-1 leftovers")[1].split("## Commands")[0]
    assert "PROPOSED" in leftovers
    assert "not Softened" in leftovers
    assert "\n### Softened" not in leftovers and "status: Softened" not in leftovers
    expansion = body.split("Expansion shortlist")[1].split("This PR implements")[0]
    assert "PROPOSED" in expansion
    assert "not Softened" in expansion


def test_cf_index_pinned_brti_and_cfb_ws_observe_only():
    assert CF_INDEX_ID == "BRTI"
    assert CFB_WS_AVERAGE_ROLE == "observe_only"
