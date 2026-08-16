from datetime import date

from options_offshoot.data_feeds.mocks import demo_contracts
from options_offshoot.ranking.rank import rank_contract


def test_honest_missing_vol_is_unconstrained():
    expiry = date(2026, 8, 21)
    put = [c for c in demo_contracts(expiry=expiry) if c.contract_id.endswith("P00400000")][0]
    assert put.realized_vol is None
    honest = rank_contract(put, honest=True, today=date(2026, 8, 16))
    current = rank_contract(put, honest=False, today=date(2026, 8, 16))
    assert honest.model.unconstrained_vol is True
    assert honest.model.fair is None
    assert current.model.fair is not None
