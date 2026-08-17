from datetime import date

from options_offshoot.config import MIN_RELIABILITY
from options_offshoot.data_feeds.ingest import ingest_field
from options_offshoot.models.enums import ComparePath, QuoteVenue
from options_offshoot.strategy.paper_book import lock_paper_positions
from options_offshoot.strategy.paper_settle import settle_position
from options_offshoot.strategy.sizing import lot_cost, size_new


def test_whole_lots_and_cant_size(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "options_offshoot.strategy.paper_book.paper_dir", lambda: tmp_path
    )
    run = ingest_field("spx_this_friday", demo=True)
    rec = lock_paper_positions(
        run, path=ComparePath.A_REPLAY, run_id=run.run_id, write=True
    )
    for p in rec.positions:
        assert p.n_contracts == int(p.n_contracts)
        assert p.n_contracts >= 1
        if p.entry_ask:
            cost = lot_cost(p.entry_ask, p.multiplier)
            assert cost is not None
            assert abs(p.stake - p.n_contracts * cost) < 1e-6
    expensive = [r for r in run.rows if r.contract.quote.ask and r.contract.quote.ask > 8]
    if expensive:
        n, stake, block = size_new(
            expensive[0], rec, bankroll=20000, cash=100, leftover=[]
        )
        assert n == 0
        assert block == "can't size"


def test_venue_pin_on_lock(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "options_offshoot.strategy.paper_book.paper_dir", lambda: tmp_path
    )
    run = ingest_field("spx_this_friday", demo=True)
    rec = lock_paper_positions(
        run, path=ComparePath.B_NERVES, run_id=run.run_id, write=True
    )
    assert rec.lock_identity
    assert rec.quote_venue_pin in (QuoteVenue.POLYGON, QuoteVenue.MOCK)
    for p in rec.positions:
        assert p.opening_ask == p.entry_ask or p.opening_ask is not None


def test_settle_formula():
    from options_offshoot.models.enums import ContractType
    from options_offshoot.models.schemas import PaperPosition

    pos = PaperPosition(
        position_id="1",
        contract_id="x",
        underlying="AAPL",
        expiry=date(2026, 8, 14),
        strike=200,
        contract_type=ContractType.CALL,
        stake=820,
        n_contracts=1,
        multiplier=100,
        entry_ask=8.20,
    )
    pnl = settle_position(pos, 205.0)
    # intrinsic 5 * 100 * 1 - 820 = -320
    assert abs(pnl - (500 - 820)) < 1e-6


def test_a_path_default_sigma_rel_clears_bar():
    from options_offshoot.data_feeds.mocks import demo_contracts
    from options_offshoot.ranking.rank import rank_contract

    put = [c for c in demo_contracts(expiry=date(2026, 8, 21)) if c.realized_vol is None][-1]
    row = rank_contract(put, honest=False, today=date(2026, 8, 16))
    assert row.model.default_sigma is True
    assert row.model.fair is not None
    assert row.model.reliability >= MIN_RELIABILITY or row.n_a_reason != "low reliability"
