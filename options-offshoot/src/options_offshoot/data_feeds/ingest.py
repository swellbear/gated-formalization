"""Assemble a field run. Mocks banned when operating=True."""

from __future__ import annotations

from datetime import date, timedelta

from options_offshoot.compare.law import law_hash
from options_offshoot.data_feeds.base import FeedError, MockOnOperatingPathError, assert_no_mocks
from options_offshoot.data_feeds.local_env import polygon_api_key
from options_offshoot.data_feeds.mocks import demo_contracts
from options_offshoot.data_feeds.polygon import PolygonClient, contracts_from_snapshot
from options_offshoot.fields.catalog import get_field, load_universe, this_friday
from options_offshoot.leftover import inventory_item
from options_offshoot.localtime import filename_stamp, now
from options_offshoot.models.enums import RunMode, SourceKind
from options_offshoot.models.schemas import FieldRun
from options_offshoot.pricing.simulate import years_to_expiry
from options_offshoot.ranking.rank import rank_contract, sort_rows


def ingest_field(
    field_id: str,
    *,
    honest: bool = False,
    operating: bool = True,
    demo: bool = False,
    max_underlyings: int | None = None,
    client: PolygonClient | None = None,
    today: date | None = None,
    mode: RunMode = RunMode.INGEST,
) -> FieldRun:
    spec = get_field(field_id)
    if demo:
        operating = False
    day = today or now().date()
    run_id = filename_stamp()
    inventory = []
    notes = []
    if not spec.allows_tickets:
        inventory.append(
            inventory_item(
                "index_only",
                used=True,
                missing=False,
                source="catalog",
                notes="map only; no tickets",
                kind=SourceKind.DERIVED_FROM_REAL,
                n=0,
            )
        )
        run = FieldRun(
            field_id=spec.field_id,
            run_id=run_id,
            mode=mode,
            honest=honest,
            operating=operating,
            inventory=inventory,
            notes=["index_only: no contracts"],
            extra={"law_hash": law_hash(), "map_only": True},
        )
        assert_no_mocks(run.inventory, operating=operating)
        return run

    expiry = this_friday(day) if spec.expiry_rule == "this_friday" else this_friday(day)
    universe = load_universe(spec)
    if spec.field_id == "earnings_us_week":
        cal = None
        if operating and not demo:
            try:
                cli = client or PolygonClient()
                cal = cli.earnings_tickers(
                    day.isoformat(), (day + timedelta(days=7)).isoformat()
                )
            except FeedError:
                cal = None
        if cal:
            universe = cal
            inventory.append(
                inventory_item(
                    "earnings_calendar",
                    used=True,
                    missing=False,
                    source="polygon",
                    notes="named vendor calendar",
                    n=len(universe),
                )
            )
        else:
            inventory.append(
                inventory_item(
                    "earnings_calendar",
                    used=False,
                    missing=True,
                    source="polygon",
                    notes="calendar unavailable; frozen ticker file used as closed fallback",
                    kind=SourceKind.UNAVAILABLE,
                )
            )
            inventory.append(
                inventory_item(
                    "frozen_earnings_universe",
                    used=True,
                    missing=False,
                    source="data/fields/earnings_us_week.txt",
                    notes="closed fallback list, not 'should be in'",
                    kind=SourceKind.DERIVED_FROM_REAL,
                    n=len(universe),
                )
            )
    else:
        inventory.append(
            inventory_item(
                "frozen_spx_universe",
                used=True,
                missing=False,
                source="data/fields/spx_this_friday.txt",
                notes="frozen v1 universe; not a live reconstitution",
                kind=SourceKind.DERIVED_FROM_REAL,
                n=len(universe),
            )
        )

    if max_underlyings is not None:
        universe = universe[: max(0, int(max_underlyings))]

    contracts = []
    if demo or not operating:
        contracts = demo_contracts(expiry=expiry)
        for c in contracts:
            c.years_to_expiry = years_to_expiry(c.expiry, day)
        inventory.append(
            inventory_item(
                "quotes",
                used=True,
                missing=False,
                source="demo_mocks",
                notes="OFFLINE DEMO — MOCK DATA",
                kind=SourceKind.MOCK,
                n=len(contracts),
            )
        )
    else:
        key = polygon_api_key() if client is None else (client.api_key or "")
        if not key and client is None:
            inventory.append(
                inventory_item(
                    "polygon_quotes",
                    used=False,
                    missing=True,
                    source="polygon",
                    notes="POLYGON_API_KEY missing; no fake mids",
                )
            )
        else:
            cli = client or PolygonClient()
            n_ok = 0
            n_vol = 0
            for und in universe:
                try:
                    vol = cli.realized_vol(und)
                except (FeedError, RuntimeError):
                    vol = None
                if vol is not None:
                    n_vol += 1
                try:
                    payload = cli.snapshot(und, expiry=expiry.isoformat())
                except (FeedError, RuntimeError) as exc:
                    notes.append(f"{und}: snapshot fail {exc}")
                    continue
                chunk = contracts_from_snapshot(
                    payload,
                    underlying=und,
                    expiry=expiry,
                    realized_vol=vol,
                    years_to_expiry=years_to_expiry(expiry, day),
                )
                n_ok += 1
                contracts.extend(chunk)
            inventory.append(
                inventory_item(
                    "polygon_quotes",
                    used=n_ok > 0,
                    missing=n_ok == 0,
                    source="polygon",
                    notes="snapshot bid/ask/OI/volume",
                    kind=SourceKind.REAL_LIVE if n_ok else SourceKind.UNAVAILABLE,
                    n=len(contracts),
                )
            )
            inventory.append(
                inventory_item(
                    "realized_vol",
                    used=n_vol > 0,
                    missing=n_vol == 0,
                    source="polygon_aggs",
                    notes="predeclared price history; honest path leaves missing unconstrained",
                    kind=SourceKind.REAL_HISTORICAL if n_vol else SourceKind.UNAVAILABLE,
                    n=n_vol,
                )
            )

    inventory.append(
        inventory_item(
            "earnings_narrative",
            used=False,
            missing=True,
            notes="forbidden in theta",
        )
    )
    inventory.append(
        inventory_item(
            "iv_from_blogs",
            used=False,
            missing=True,
            notes="forbidden in theta",
        )
    )

    rows = [
        rank_contract(c, honest=honest, today=day)
        for c in contracts
    ]
    rows = sort_rows(rows)
    run = FieldRun(
        field_id=spec.field_id,
        run_id=run_id,
        mode=mode,
        honest=honest,
        operating=operating,
        underlyings=sorted({c.underlying for c in contracts}),
        rows=rows,
        inventory=inventory,
        notes=notes,
        extra={"law_hash": law_hash(), "expiry": expiry.isoformat()},
    )
    if demo:
        run.operating = False
    assert_no_mocks(run.inventory, operating=run.operating)
    return run
