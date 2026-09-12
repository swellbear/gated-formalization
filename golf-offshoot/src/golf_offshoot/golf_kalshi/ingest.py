"""One-shot Kalshi golf ingest. Catalog + unmatched quarantine. No paper fills."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.golf_kalshi.adapter import (
    GolfKalshiFeed,
    TRADING_ARMED,
    load_last_good_catalog,
    save_catalog,
)
from golf_offshoot.golf_kalshi.matcher import extract_player_name, match_market_player, quarantine_row
from golf_offshoot.golf_kalshi.paths import (
    LANE,
    assert_golf_kalshi_path,
    catalog_path,
    golf_kalshi_root,
    unmatched_path,
)
from golf_offshoot.localtime import isoformat_now


def _write_json(path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def quarantine_unmatched(
    markets: list[dict[str, Any]],
    candidates: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    """Every ticker without a real name match stays unmatched. Never invent a player_id."""
    field = candidates or {}
    rows: list[dict[str, str]] = []
    for market in markets:
        if not isinstance(market, dict):
            continue
        ticker = str(market.get("ticker") or "")
        if not ticker:
            continue
        name = extract_player_name(market)
        if not name:
            rows.append(quarantine_row(market, reason="no_name"))
            continue
        hit = match_market_player(market, field)
        if hit is None:
            rows.append(quarantine_row(market, reason="unmatched"))
    return rows


def run_ingest(
    *,
    feed: GolfKalshiFeed | None = None,
    candidates: dict[str, str] | None = None,
    catalog: dict[str, Any] | None = None,
    refresh: bool = False,
) -> dict[str, Any]:
    """Public golf catalog into ``data/golf_kalshi/``. No 15m or Phase 1 writes."""
    feed = feed or GolfKalshiFeed()
    if catalog is None:
        try:
            catalog = feed.fetch_catalog(refresh=refresh)
        except Exception:
            catalog = load_last_good_catalog()
    save_catalog(catalog)
    markets = list(catalog.get("markets") or [])
    unmatched = quarantine_unmatched(markets, candidates)
    _write_json(
        unmatched_path(),
        {"lane": LANE, "rows": unmatched, "at": isoformat_now()},
    )
    root = golf_kalshi_root()
    return {
        "lane": LANE,
        "at": isoformat_now(),
        "trading_armed": TRADING_ARMED,
        "root": str(root),
        "catalog_path": str(catalog_path()),
        "unmatched_path": str(unmatched_path()),
        "series": len(catalog.get("series") or []),
        "markets": len(markets),
        "unmatched": len(unmatched),
        "fail_open": bool(catalog.get("fail_open")),
        "summary": (
            f"golf-kalshi ingest series={len(catalog.get('series') or [])} "
            f"markets={len(markets)} unmatched={len(unmatched)} "
            f"TRADING_ARMED={TRADING_ARMED}"
        ),
    }


def format_ingest(result: dict[str, Any]) -> str:
    return (
        f"{result.get('summary') or 'golf-kalshi ingest'}\n"
        f"  root={result.get('root')}\n"
        f"  catalog={result.get('catalog_path')}\n"
        f"  unmatched={result.get('unmatched_path')}\n"
    )
