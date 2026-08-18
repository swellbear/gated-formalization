"""Assemble a field run. Mocks banned when operating=True."""

from __future__ import annotations

from datetime import date, timedelta

from options_offshoot.compare.law import law_hash
from options_offshoot.config import UNDERLYING_PAUSE_S
from options_offshoot.data_feeds.base import FeedError, assert_no_mocks
from options_offshoot.data_feeds.http import HttpError, StaleCacheError
from options_offshoot.data_feeds.ibkr import overlay_ibkr
from options_offshoot.data_feeds.local_env import feed_pause_s, polygon_api_key, quotes_mode
from options_offshoot.data_feeds.mocks import demo_contracts
from options_offshoot.data_feeds.opening import apply_opening, save_last_run
from options_offshoot.data_feeds.polygon import (
    PolygonClient,
    contracts_from_snapshot,
    lookback_for_dte,
)
from options_offshoot.fields.catalog import freeze_header, get_field, load_universe, this_friday
from options_offshoot.leftover import inventory_item
from options_offshoot.localtime import filename_stamp, now
from options_offshoot.models.enums import QuoteVenue, RunMode, SourceKind
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
    quotes: str | None = None,
    ibkr_quotes: dict | None = None,
) -> FieldRun:
    spec = get_field(field_id)
    if demo:
        operating = False
    day = today or now().date()
    run_id = filename_stamp()
    inventory = []
    notes = []
    venue_name = (quotes or quotes_mode() or "polygon").strip().lower()
    if venue_name not in {"polygon", "ibkr"}:
        venue_name = "polygon"
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
        save_last_run(run)
        return run

    friday = this_friday(day)
    universe = load_universe(spec)
    freeze = freeze_header(spec)
    universe_n = len(universe)

    if spec.field_id == "earnings_us_week":
        cal = None
        if operating and not demo:
            try:
                cli = client or PolygonClient(
                    mode=mode, pause_s=feed_pause_s(UNDERLYING_PAUSE_S)
                )
                cal = cli.earnings_tickers(
                    day.isoformat(), (day + timedelta(days=7)).isoformat()
                )
            except FeedError:
                cal = None
        if cal:
            universe = cal
            universe_n = len(universe)
            inventory.append(
                inventory_item(
                    "earnings_calendar",
                    used=True,
                    missing=False,
                    source="polygon",
                    notes="Massive/Benzinga earnings calendar; expiry=nearest listed on/after print/today",
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
                    notes="Benzinga earnings expansion unavailable; frozen ticker file used as closed fallback — not this week's earnings",
                    kind=SourceKind.UNAVAILABLE,
                )
            )
            inventory.append(
                inventory_item(
                    "frozen_earnings_universe",
                    used=True,
                    missing=False,
                    source="data/fields/earnings_us_week.txt",
                    notes="closed fallback list, not 'should be in'; not this week's earnings",
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
                notes=(
                    f"operator freeze of {universe_n} names, not the S&P "
                    f"(as_of={freeze.get('as_of') or 'n/a'}; "
                    f"source={freeze.get('source') or 'operator freeze'}). "
                    "Equity weeklies, not SPX/SPXW."
                ),
                kind=SourceKind.DERIVED_FROM_REAL,
                n=universe_n,
            )
        )

    cap = max_underlyings
    if cap is not None and int(cap) > 0:
        universe = universe[: int(cap)]
    fetched_plan = len(universe)

    contracts = []
    if demo or not operating:
        contracts = demo_contracts(expiry=friday)
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
        venue_used = QuoteVenue.MOCK
    else:
        venue_used = QuoteVenue.POLYGON
        key = polygon_api_key() if client is None else (client.api_key or "")
        if not key and client is None:
            inventory.append(
                inventory_item(
                    "polygon_quotes",
                    used=False,
                    missing=True,
                    source="polygon",
                    notes="MASSIVE_API_KEY / POLYGON_API_KEY missing; no fake mids",
                )
            )
        else:
            cli = client or PolygonClient(
                mode=mode, pause_s=feed_pause_s(UNDERLYING_PAUSE_S)
            )
            n_ok = 0
            n_vol = 0
            n_spot = 0
            truncated = False
            for und in universe:
                if spec.expiry_rule == "nearest_listed_on_or_after_event":
                    try:
                        exp = cli.nearest_listed_expiry(und, day)
                    except (FeedError, RuntimeError, HttpError, StaleCacheError):
                        exp = None
                    if exp is None:
                        notes.append(f"{und}: no listed expiry on/after {day.isoformat()}")
                        continue
                else:
                    exp = friday
                dte = max(1, (exp - day).days)
                try:
                    vol = cli.realized_vol(und, lookback=lookback_for_dte(dte))
                except (FeedError, RuntimeError, HttpError, StaleCacheError):
                    vol = None
                if vol is not None:
                    n_vol += 1
                try:
                    spot = cli.stock_spot(und)
                except (FeedError, RuntimeError, HttpError, StaleCacheError):
                    spot = None
                if spot is not None:
                    n_spot += 1
                try:
                    payload = cli.snapshot(und, expiry=exp.isoformat())
                except StaleCacheError as exc:
                    notes.append(f"{und}: quotes stale >15min ({exc})")
                    continue
                except (FeedError, RuntimeError, HttpError) as exc:
                    notes.append(f"{und}: snapshot fail {exc}")
                    continue
                if payload.get("_truncated"):
                    truncated = True
                    notes.append(f"{und}: chain truncated")
                chunk = contracts_from_snapshot(
                    payload,
                    underlying=und,
                    expiry=exp,
                    spot=spot,
                    realized_vol=vol,
                    years_to_expiry=years_to_expiry(exp, day),
                    venue=QuoteVenue.POLYGON,
                )
                n_ok += 1
                contracts.extend(chunk)
            notes.extend(cli.last_notes)
            n_lq = sum(1 for c in contracts if c.quote.has_real_ask)
            if n_ok == 0 and any("403" in n for n in notes):
                quote_notes = (
                    "Massive option chain snapshot 403: Options Starter+ "
                    "(not Options Basic / stocks-only). last_quote only if the plan "
                    "includes quotes. No invented mid."
                )
            elif n_ok > 0 and n_lq == 0:
                quote_notes = (
                    "chain/specs/OI used; last_quote omitted (quotes not on this "
                    "Massive plan; /v3/quotes 403). No invented mid from day.close."
                )
            else:
                quote_notes = (
                    "snapshot bid/ask/OI/volume; last_quote is Massive, never relabeled IBKR"
                )
            inventory.append(
                inventory_item(
                    "polygon_quotes",
                    used=n_ok > 0,
                    missing=n_ok == 0,
                    source="polygon",
                    notes=quote_notes,
                    kind=SourceKind.REAL_LIVE if n_ok else SourceKind.UNAVAILABLE,
                    n=len(contracts),
                )
            )
            if n_ok > 0 and n_lq == 0:
                inventory.append(
                    inventory_item(
                        "massive_last_quote",
                        used=False,
                        missing=True,
                        source="polygon",
                        notes=(
                            "last_quote not on chain/contract snapshot; /v3/quotes 403. "
                            "Stocks snapshot/last trade 403. No invented mid."
                        ),
                        kind=SourceKind.UNAVAILABLE,
                    )
                )
            inventory.append(
                inventory_item(
                    "realized_vol",
                    used=n_vol > 0,
                    missing=n_vol == 0,
                    source="polygon_aggs",
                    notes="DTE-matched lookback from predeclared dailies; honest path leaves missing unconstrained",
                    kind=SourceKind.REAL_HISTORICAL if n_vol else SourceKind.UNAVAILABLE,
                    n=n_vol,
                )
            )
            inventory.append(
                inventory_item(
                    "spot",
                    used=n_spot > 0,
                    missing=n_spot == 0,
                    source="polygon_aggs_prev",
                    notes=(
                        "prev daily close from aggs (not NBBO). Stocks snapshot 403. "
                        "Session leftover."
                    ),
                    kind=SourceKind.REAL_HISTORICAL if n_spot else SourceKind.UNAVAILABLE,
                    n=n_spot,
                )
            )
            if truncated:
                inventory.append(
                    inventory_item(
                        "chain_truncated",
                        used=True,
                        missing=True,
                        source="polygon",
                        notes="chain truncated; leftover, not a complete expiry chain",
                        kind=SourceKind.UNAVAILABLE,
                    )
                )
            if n_ok < fetched_plan:
                inventory.append(
                    inventory_item(
                        "field_incomplete",
                        used=True,
                        missing=True,
                        source="polygon",
                        notes=f"field incomplete this run ({n_ok} of {universe_n} freeze; planned {fetched_plan})",
                        kind=SourceKind.UNAVAILABLE,
                        n=n_ok,
                    )
                )

        n_lq_now = sum(1 for c in contracts if c.quote.has_real_ask)
        want_ibkr = venue_name == "ibkr" or (
            (not demo) and operating and bool(contracts) and n_lq_now == 0
        )
        if want_ibkr and contracts:
            fallback = venue_name != "ibkr"
            contracts, ib_notes = overlay_ibkr(
                contracts, quotes=ibkr_quotes, live_fetch=ibkr_quotes is None
            )
            notes.extend(ib_notes)
            n_ib = sum(1 for c in contracts if c.quote_venue == QuoteVenue.IBKR)
            prefix = (
                "Massive last_quote omitted; IBKR overlay attempted. "
                "Not relabeled as Massive last_quote. "
                if fallback
                else "venue ask overlay; market data only, never placeOrder. "
            )
            inventory.append(
                inventory_item(
                    "ibkr_venue_ask",
                    used=n_ib > 0,
                    missing=n_ib == 0,
                    source="ibkr",
                    notes=prefix + ("; ".join(ib_notes) if ib_notes else "IBKR bid/ask used"),
                    kind=SourceKind.REAL_LIVE if n_ib else SourceKind.UNAVAILABLE,
                    n=n_ib,
                )
            )
            venue_used = QuoteVenue.IBKR if n_ib else venue_used
        elif venue_name == "ibkr":
            inventory.append(
                inventory_item(
                    "ibkr_venue_ask",
                    used=False,
                    missing=True,
                    source="ibkr",
                    notes="venue ask requested; no contracts to overlay",
                    kind=SourceKind.UNAVAILABLE,
                )
            )
        else:
            inventory.append(
                inventory_item(
                    "ibkr_venue_ask",
                    used=False,
                    missing=True,
                    source="ibkr",
                    notes="venue ask not requested (--quotes polygon). Massive last_quote is not IBKR.",
                    kind=SourceKind.UNAVAILABLE,
                )
            )

    apply_opening(spec.field_id, contracts)

    n_default_mult = sum(1 for c in contracts if c.multiplier_defaulted)
    if n_default_mult:
        inventory.append(
            inventory_item(
                "multiplier_default_100",
                used=True,
                missing=True,
                source="specs",
                notes=f"{n_default_mult} contracts missing shares_per_contract; used 100 and leftover says so",
                kind=SourceKind.UNAVAILABLE,
                n=n_default_mult,
            )
        )
    n_nonstd = sum(1 for c in contracts if c.nonstandard_deliverable)
    if n_nonstd:
        inventory.append(
            inventory_item(
                "nonstandard_deliverable",
                used=True,
                missing=True,
                source="specs",
                notes=f"{n_nonstd} contracts with multiplier != 100; leftover if deliverable is not 100 shares",
                kind=SourceKind.UNAVAILABLE,
                n=n_nonstd,
            )
        )

    _honesty_inventory(inventory)

    rows = [rank_contract(c, honest=honest, today=day) for c in contracts]
    rows = sort_rows(rows)
    extra = {
        "law_hash": law_hash(),
        "expiry": friday.isoformat(),
        "universe_n": universe_n,
        "fetched_n": len({c.underlying for c in contracts}),
        "quote_venue": venue_used.value,
        "incomplete": any(i.name == "field_incomplete" for i in inventory),
        "quotes_mode": venue_name,
    }
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
        extra=extra,
    )
    if demo:
        run.operating = False
    assert_no_mocks(run.inventory, operating=run.operating)
    save_last_run(run)
    return run


def _honesty_inventory(inventory: list) -> None:
    for name, notes in (
        ("earnings_narrative", "forbidden in theta"),
        ("iv_from_blogs", "forbidden in theta"),
        ("interest_rate_r0", "MC uses r=0; leftover, not a rates feed"),
        ("dividend_yield", "no dividend yield in MC; leftover, not stuffed"),
        ("calendar_dte", "calendar DTE, not remaining session hours"),
        ("earnings_jump", "earnings jump not in sigma"),
        ("american_early_exercise", "American early exercise unconstrained; not in MC"),
        ("corporate_actions", "splits/special div mid-DTE leftover; do not invent adjusted strikes"),
        ("session_rth", "RTH vs extended unconstrained if that was not the pin"),
        ("listed_iv_display_only", "listed IV is inventory/display only, never honest theta"),
    ):
        inventory.append(
            inventory_item(
                name,
                used=False,
                missing=True,
                notes=notes,
            )
        )
