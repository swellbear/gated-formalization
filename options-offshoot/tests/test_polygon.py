from datetime import date

import pytest

from options_offshoot.data_feeds.base import MockOnOperatingPathError, assert_no_mocks
from options_offshoot.data_feeds.ingest import ingest_field
from options_offshoot.data_feeds.polygon import contracts_from_snapshot
from options_offshoot.leftover import inventory_item
from options_offshoot.models.enums import SourceKind


def test_snapshot_parser_maps_bid_ask_oi():
    payload = {
        "underlying_asset": {"price": 100.0},
        "results": [
            {
                "details": {
                    "ticker": "O:TEST",
                    "expiration_date": "2026-08-21",
                    "strike_price": 105,
                    "contract_type": "call",
                },
                "last_quote": {"bid": 1.1, "ask": 1.2},
                "open_interest": 400,
                "day": {"volume": 20},
            }
        ],
    }
    rows = contracts_from_snapshot(
        payload, underlying="TEST", expiry=date(2026, 8, 21), realized_vol=0.2
    )
    assert len(rows) == 1
    assert rows[0].quote.ask == 1.2
    assert rows[0].quote.bid == 1.1
    assert rows[0].quote.open_interest == 400
    assert rows[0].spot == 100.0


def test_operating_rejects_mocks():
    items = [
        inventory_item(
            "quotes",
            used=True,
            missing=False,
            source="demo",
            kind=SourceKind.MOCK,
        )
    ]
    with pytest.raises(MockOnOperatingPathError):
        assert_no_mocks(items, operating=True)
    assert_no_mocks(items, operating=False)


def test_demo_ingest_not_operating():
    run = ingest_field("spx_this_friday", demo=True, operating=True)
    assert run.operating is False
    assert run.rows
    assert any(r.n_a_reason for r in run.rows)
