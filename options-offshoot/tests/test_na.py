from datetime import date

from options_offshoot.data_feeds.mocks import demo_contracts
from options_offshoot.ranking.rank import mark_liquid, rank_contract


def test_no_ask_is_n_a():
    expiry = date(2026, 8, 21)
    msft_call = [c for c in demo_contracts(expiry=expiry) if c.underlying == "MSFT" and c.contract_type.value == "call"][0]
    mark_liquid(msft_call)
    assert msft_call.liquid is False
    row = rank_contract(msft_call, honest=False, today=date(2026, 8, 16))
    assert row.n_a_reason
    assert row.vs_ask is None
    assert row.clears_ask is False


def test_wide_otm_size_floor_is_n_a():
    expiry = date(2026, 8, 21)
    otm = [c for c in demo_contracts(expiry=expiry) if c.strike == 300][0]
    row = rank_contract(otm, honest=False, today=date(2026, 8, 16))
    assert row.n_a_reason
    assert "size" in (row.n_a_reason or "") or "spread" in (row.n_a_reason or "")
