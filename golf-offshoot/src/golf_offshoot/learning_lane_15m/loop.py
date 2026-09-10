"""Shared ops loop for lane 15m: ingest → live → paper autobet → settle join.

Observation only. Independent of the PGA calendar. Does not retune golf θ.
"""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.data_feeds.kalshi_15m import Kalshi15mFeed
from golf_offshoot.learning_lane_15m.paper import (
    TRADING_ARMED,
    format_15m_ledger,
    load_ledger,
    paper_autobet_open_markets,
)
from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    PRIMARY_SERIES,
    assert_not_golf_path,
    snapshots_dir_15m,
)
from golf_offshoot.learning_lane_15m.notify import notify_settlements
from golf_offshoot.learning_lane_15m.settle import settle_join_books
from golf_offshoot.operator_surface.observability import write_observability_exports
from golf_offshoot.localtime import filename_stamp

OBSERVATION_BANNER = (
    "PHASE 1 OBSERVATION · Trading NOT ARMED · PAPER OBSERVATION ONLY · "
    "AI: NO CASH IN/OUT · LEARNING LANE"
)


def _write_snapshot(name: str, payload: dict[str, Any]) -> str:
    dest = snapshots_dir_15m() / f"{filename_stamp()}_{name}.json"
    assert_not_golf_path(dest)
    dest.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return str(dest)


def ingest(*, refresh: bool = False, feed: Kalshi15mFeed | None = None) -> dict[str, Any]:
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    src = feed or Kalshi15mFeed(refresh=refresh)
    payload, quality = src.fetch(refresh=refresh)
    out = {
        "step": "ingest",
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "banner": OBSERVATION_BANNER,
        "trading_armed": False,
        "events": payload.get("events") or [],
        "markets": payload.get("markets") or [],
        "quality": quality.model_dump(mode="json"),
        "series_fee": payload.get("series_fee") or {},
    }
    out["snapshot"] = _write_snapshot("ingest", out)
    return out


def live(*, refresh: bool = True, feed: Kalshi15mFeed | None = None) -> dict[str, Any]:
    """Public price refresh. Same read-only adapter as ingest."""
    out = ingest(refresh=refresh, feed=feed)
    out["step"] = "live"
    out["snapshot"] = _write_snapshot("live", out)
    return out


def paper_autobet(markets: list[dict[str, Any]]) -> dict[str, Any]:
    fills = paper_autobet_open_markets(markets)
    return {
        "step": "paper_autobet",
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "banner": OBSERVATION_BANNER,
        "trading_armed": False,
        "fills": len(fills),
        "tickers": [m.player_id for m in fills],
        "ledger": format_15m_ledger(load_ledger()),
    }


def settle_join(
    markets: list[dict[str, Any]],
    events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    rows = settle_join_books(markets, events=events)
    ping = notify_settlements(rows)
    return {
        "step": "settle_join",
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "banner": OBSERVATION_BANNER,
        "trading_armed": False,
        "rows": [r.model_dump() for r in rows],
        "pending": sum(1 for r in rows if r.settle_status != "settled"),
        "settled": sum(1 for r in rows if r.settle_status == "settled"),
        "notify": ping,
        "ledger": format_15m_ledger(load_ledger()),
    }


def run_loop(*, refresh: bool = True, feed: Kalshi15mFeed | None = None) -> dict[str, Any]:
    """End-to-end paper observation loop against public KXBTC15M windows."""
    live_state = live(refresh=refresh, feed=feed)
    from golf_offshoot.quote_bus import publish as publish_quote_bus

    bus = publish_quote_bus(live_state)
    markets = live_state.get("markets") or []
    events = live_state.get("events") or []
    paper = paper_autobet(markets)
    joined = settle_join(markets, events)
    export_paths = write_observability_exports(markets=markets)
    return {
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "banner": OBSERVATION_BANNER,
        "trading_armed": False,
        "ingest": live_state,
        "live": live_state,
        "paper_autobet": paper,
        "settle_join": joined,
        "observability_export": export_paths,
        "quote_bus": {"fetch_id": bus.get("fetch_id"), "fetched_at": bus.get("fetched_at")},
    }


def format_loop_report(result: dict[str, Any]) -> str:
    paper = result.get("paper_autobet") or {}
    joined = result.get("settle_join") or {}
    live_state = result.get("live") or {}
    lines = [
        result.get("banner") or OBSERVATION_BANNER,
        f"lane={result.get('lane')} series={result.get('series')} trading_armed=false",
        f"live markets={len(live_state.get('markets') or [])} "
        f"events={len(live_state.get('events') or [])}",
        f"paper autobet fills={paper.get('fills', 0)} tickers={paper.get('tickers') or []}",
        f"settle join settled={joined.get('settled', 0)} pending={joined.get('pending', 0)}",
        "",
        joined.get("ledger") or paper.get("ledger") or "",
    ]
    for row in joined.get("rows") or []:
        lines.append(
            f"  {row.get('ticker')} {row.get('settle_status')} "
            f"result={row.get('kalshi_result') or 'n/a'} "
            f"source_matched={row.get('source_matched')}"
        )
    lines.append("15-min Kalshi is a learning lane for the shared ops loop. Not live cash.")
    return "\n".join(lines)
