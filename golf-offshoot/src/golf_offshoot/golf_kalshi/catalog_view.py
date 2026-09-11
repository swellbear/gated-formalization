"""Catalog observation tree. Tour family → series → open/settled markets. No invented tours."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from golf_offshoot.golf_kalshi.sleeves import classify_sleeve

FAMILY_ORDER = (
    "PGA Tour",
    "LIV",
    "LPGA",
    "DP World",
    "Champions",
    "Masters",
    "US Open",
    "The Open",
    "Majors",
    "Ryder Cup",
    "Solheim Cup",
    "Presidents Cup",
    "TGL",
    "Other golf",
)


def catalog_family(series_ticker: str) -> str:
    """Tour bucket from Kalshi series ticker stems already on this gym. Not a ranking."""
    token = str(series_ticker or "").strip().upper()
    if token.startswith("KXLIV"):
        return "LIV"
    if token.startswith("KXLPGA"):
        return "LPGA"
    if token.startswith("KXCHAMPTOUR"):
        return "Champions"
    if token.startswith("KXDPWORLD") or token.startswith("KXDPWT"):
        return "DP World"
    if token.startswith("KXTGL"):
        return "TGL"
    if "RYDER" in token:
        return "Ryder Cup"
    if "SOLHEIM" in token:
        return "Solheim Cup"
    if token.startswith("KXPRESCUP"):
        return "Presidents Cup"
    if "MASTERS" in token:
        return "Masters"
    if token.startswith("KXTHEOPEN"):
        return "The Open"
    if token.startswith("KXUSOPEN") or token.startswith("KXPGAUSO"):
        return "US Open"
    if "MAJOR" in token:
        return "Majors"
    if token.startswith("KXPGA"):
        return "PGA Tour"
    return "Other golf"


def market_bucket(market: dict[str, Any]) -> str:
    status = str(market.get("status") or "").strip().lower()
    if status in {"settled", "finalized"}:
        return "settled"
    if str(market.get("result") or "").strip():
        return "settled"
    return "open"


def _sleeve_mix(markets: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for market in markets:
        sleeve = classify_sleeve(market)
        counts[sleeve] = counts.get(sleeve, 0) + 1
    parts = [f"{name} {counts[name]}" for name in ("fast", "week", "slow") if counts.get(name)]
    return " · ".join(parts)


def _sort_markets(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda m: (
            0 if m.get("in_play") else 1,
            str(m.get("yes_sub_title") or m.get("title") or ""),
            str(m.get("ticker") or ""),
        ),
    )


def group_catalog(
    series: list[dict[str, Any]],
    markets: list[dict[str, Any]],
    booked: set[str] | None = None,
    *,
    include_markets: bool = True,
) -> dict[str, Any]:
    """Every series kept. First paint is family/series summaries unless include_markets."""
    booked = booked or set()
    buckets: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: {"open": [], "settled": []})
    for market in markets:
        st = str(market.get("series_ticker") or "").strip()
        if not st:
            continue
        buckets[st][market_bucket(market)].append(market)
    by_ticker = {
        str(row.get("series_ticker") or "").strip(): row
        for row in series
        if str(row.get("series_ticker") or "").strip()
    }
    for st in buckets:
        if st not in by_ticker:
            by_ticker[st] = {"series_ticker": st, "title": st, "tags": ["Golf"]}
    families: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for st, row in by_ticker.items():
        open_m = _sort_markets(buckets[st]["open"])
        settled_m = _sort_markets(buckets[st]["settled"])
        tickers = {str(m.get("ticker") or "") for m in open_m + settled_m}
        in_book = bool(tickers & booked)
        in_play = any(m.get("in_play") for m in open_m)
        preview = []
        if in_play or in_book:
            for market in open_m:
                name = str(market.get("yes_sub_title") or "").strip()
                if name and name not in preview:
                    preview.append(name)
                if len(preview) >= 8:
                    break
        families[catalog_family(st)].append(
            {
                "series_ticker": st,
                "title": str(row.get("title") or st),
                "fee_multiplier": row.get("fee_multiplier"),
                "open": open_m if include_markets else [],
                "settled": settled_m if include_markets else [],
                "open_n": len(open_m),
                "settled_n": len(settled_m),
                "in_play": in_play,
                "in_book": in_book,
                "sleeves": _sleeve_mix(open_m) or _sleeve_mix(settled_m),
                "names_preview": preview,
            }
        )
    tree = []
    for name, rows in families.items():
        rows = sorted(
            rows,
            key=lambda s: (
                0 if s["in_play"] or s["in_book"] else 1,
                -int(s["open_n"]),
                str(s["title"]),
            ),
        )
        tree.append(
            {
                "name": name,
                "series": rows,
                "series_n": len(rows),
                "open_n": sum(int(s["open_n"]) for s in rows),
                "settled_n": sum(int(s["settled_n"]) for s in rows),
                "in_play": any(s["in_play"] for s in rows),
                "in_book": any(s["in_book"] for s in rows),
            }
        )
    order = {name: i for i, name in enumerate(FAMILY_ORDER)}
    tree.sort(
        key=lambda fam: (
            0 if fam["in_play"] or fam["in_book"] else 1,
            order.get(str(fam["name"]), 99),
            str(fam["name"]),
        )
    )
    return {
        "families": tree,
        "series_n": len(by_ticker),
        "open_n": sum(int(f["open_n"]) for f in tree),
        "settled_n": sum(int(f["settled_n"]) for f in tree),
        "in_play": sum(1 for f in tree if f["in_play"]),
        "in_book": sum(1 for f in tree if f["in_book"]),
    }
