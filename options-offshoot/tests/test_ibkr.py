from datetime import date

from options_offshoot.data_feeds.ibkr import (
    IBKR_MARKET_DATA_ONLY,
    PLACE_ORDER_FORBIDDEN,
    apply_ibkr_quote,
    ibkr_underlying,
    occ_match,
    overlay_ibkr,
)
from options_offshoot.data_feeds.mocks import demo_contracts
from options_offshoot.models.enums import QuoteVenue


def test_ibkr_is_market_data_only():
    import inspect

    import options_offshoot.data_feeds.ibkr as mod

    src = inspect.getsource(mod)
    assert "placeOrder(" not in src
    assert "ib.placeOrder" not in src
    assert IBKR_MARKET_DATA_ONLY is True
    assert PLACE_ORDER_FORBIDDEN is True


def test_occ_match_and_no_neighbor_fill():
    c = demo_contracts(expiry=date(2026, 8, 21))[0]
    assert occ_match(c, symbol="AAPL", expiry=date(2026, 8, 21), strike=200.0, right="C")
    assert ibkr_underlying("BRK.B") == "BRK B"
    assert not occ_match(c, symbol="AAPL", expiry=date(2026, 8, 21), strike=210.0, right="C")
    over = apply_ibkr_quote(c.model_copy(deep=True), bid=8.0, ask=8.1, con_id=99)
    assert over.quote_venue == QuoteVenue.IBKR
    assert over.quote.venue == QuoteVenue.IBKR
    delayed = apply_ibkr_quote(c.model_copy(deep=True), bid=8.0, ask=8.1, delayed=True)
    assert delayed.quote.ask == 8.1
    assert delayed.quote_venue == QuoteVenue.IBKR
    assert "delayed" in delayed.notes.lower()
    overlaid, _ = overlay_ibkr(
        [c.model_copy(deep=True)],
        quotes={c.contract_id: {"bid": 8.0, "ask": 8.1, "delayed": True}},
    )
    assert overlaid[0].quote.has_real_ask
    assert overlaid[0].quote_venue == QuoteVenue.IBKR
    assert "delayed" in overlaid[0].notes.lower()
