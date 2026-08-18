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
    assert rows[0].multiplier == 100
    assert rows[0].multiplier_defaulted is True


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


def test_snapshot_paginates_next_url(monkeypatch):
    from options_offshoot.data_feeds.polygon import PolygonClient
    from options_offshoot.models.enums import RunMode

    pages = {
        "first": {
            "results": [{"details": {"ticker": "O:A", "expiration_date": "2026-08-21", "strike_price": 1, "contract_type": "call"}, "last_quote": {"bid": 1, "ask": 1.1}, "open_interest": 200, "day": {"volume": 10}}],
            "next_url": "https://api.polygon.io/v3/snapshot/options/TEST?cursor=2",
            "underlying_asset": {"price": 10},
        },
        "second": {
            "results": [{"details": {"ticker": "O:B", "expiration_date": "2026-08-21", "strike_price": 2, "contract_type": "call"}, "last_quote": {"bid": 1, "ask": 1.1}, "open_interest": 200, "day": {"volume": 10}}],
            "underlying_asset": {"price": 10},
        },
    }

    def fake_get(url, **kwargs):
        if "cursor=2" in url:
            return pages["second"]
        return pages["first"]

    monkeypatch.setattr("options_offshoot.data_feeds.polygon.get_json", fake_get)
    cli = PolygonClient(api_key="x", use_cache=False, pause_s=0, mode=RunMode.INGEST)
    payload = cli.snapshot("TEST", expiry="2026-08-21")
    assert len(payload["results"]) == 2
    assert payload["_pages"] == 2
    from options_offshoot.data_feeds.polygon import contracts_from_snapshot
    from datetime import date

    rows = contracts_from_snapshot(payload, underlying="TEST", expiry=date(2026, 8, 21))
    assert {r.contract_id for r in rows} == {"O:A", "O:B"}


def test_rest_bases_default_massive(monkeypatch):
    monkeypatch.delenv("MASSIVE_API_BASE", raising=False)
    from options_offshoot.data_feeds.polygon import (
        MASSIVE_BASE,
        POLYGON_LEGACY_BASE,
        rest_bases,
    )

    bases = rest_bases()
    assert bases[0] == MASSIVE_BASE
    assert POLYGON_LEGACY_BASE in bases


def test_snapshot_403_names_starter_plan(monkeypatch):
    from options_offshoot.data_feeds.http import HttpError
    from options_offshoot.data_feeds.polygon import PolygonClient
    from options_offshoot.models.enums import RunMode

    calls = []

    def fake_get(url, **kwargs):
        calls.append(url)
        raise HttpError("forbidden", status=403)

    monkeypatch.setattr("options_offshoot.data_feeds.polygon.get_json", fake_get)
    cli = PolygonClient(api_key="x", use_cache=False, pause_s=0, mode=RunMode.INGEST)
    with pytest.raises(HttpError) as exc:
        cli.snapshot("AAPL", expiry="2026-08-21")
    assert exc.value.status == 403
    assert any("Options Starter+" in n for n in cli.last_notes)
    assert any("api.massive.com" in u for u in calls)
    assert not any("api.polygon.io" in u for u in calls)


def test_day_close_is_not_an_ask():
    payload = {
        "results": [
            {
                "details": {
                    "ticker": "O:TEST",
                    "expiration_date": "2026-08-21",
                    "strike_price": 105,
                    "contract_type": "call",
                },
                "day": {"close": 9.99, "volume": 20},
                "open_interest": 400,
                "bid": 1.0,
                "ask": 1.1,
            }
        ],
    }
    rows = contracts_from_snapshot(
        payload, underlying="TEST", expiry=date(2026, 8, 21)
    )
    assert rows[0].quote.ask is None
    assert rows[0].quote.bid is None


def test_select_ibkr_overlay_oi_floor():
    from options_offshoot.data_feeds.ibkr import select_ibkr_overlay
    from options_offshoot.data_feeds.mocks import demo_contracts

    rows = demo_contracts(expiry=date(2026, 8, 21))
    picked, notes = select_ibkr_overlay(rows)
    assert all((c.quote.open_interest or 0) >= 100 for c in picked)
    assert isinstance(notes, list)
    ids = {c.contract_id for c in picked}
    assert "O:AAPL250000C00300000" not in ids


def test_demo_ingest_not_operating():
    run = ingest_field("spx_this_friday", demo=True, operating=True)
    assert run.operating is False
    assert run.rows
    assert any(r.n_a_reason for r in run.rows)

