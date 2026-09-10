"""Empirical half-spread profile: mean (yes_ask − yes_bid)/2 bucketed by mark.

Named on the evidence bar. critic-invariants fails if this artifact is
missing or empty, so an unmeasured spread cannot silently return. Gym cycles
append live quotes into latest/; the committed docs file is the named snapshot.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from golf_offshoot.learning_lane_15m.paths import (
    latest_dir_15m,
    paper_dir_15m,
    snapshots_dir_15m,
)
from golf_offshoot.localtime import isoformat_now
from golf_offshoot.operator_surface.observability import repo_root

PROFILE_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json"
BUCKET_WIDTH = 0.05
QUOTES_NAME = "spread_quotes.jsonl"
LATEST_PROFILE_NAME = "half_spread_profile.json"
MAX_SNAPSHOT_FILES = 800


def profile_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / PROFILE_REL


def latest_profile_path(*, latest_dir: Path | None = None) -> Path:
    return (latest_dir or latest_dir_15m()) / LATEST_PROFILE_NAME


def quotes_log_path(*, latest_dir: Path | None = None) -> Path:
    return (latest_dir or latest_dir_15m()) / QUOTES_NAME


def half_spread(bid: Any, ask: Any) -> float | None:
    try:
        if bid is None or ask is None:
            return None
        spread = (float(ask) - float(bid)) / 2.0
    except (TypeError, ValueError):
        return None
    if spread < 0:
        return None
    return spread


def sample_from_market(market: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(market, dict):
        return None
    bid = market.get("yes_bid")
    ask = market.get("yes_ask")
    hs = half_spread(bid, ask)
    if hs is None:
        return None
    mark = market.get("paper_mark")
    if mark is None:
        try:
            mark = (float(bid) + float(ask)) / 2.0
        except (TypeError, ValueError):
            return None
    try:
        mark_f = float(mark)
    except (TypeError, ValueError):
        return None
    if mark_f <= 0.0 or mark_f >= 1.0:
        return None
    return {
        "ticker": str(market.get("ticker") or ""),
        "mark": mark_f,
        "yes_bid": float(bid),
        "yes_ask": float(ask),
        "half_spread": hs,
    }


def bucket_key(mark: float) -> str:
    lo = int(mark / BUCKET_WIDTH) * BUCKET_WIDTH
    hi = lo + BUCKET_WIDTH
    return f"{lo:.2f}-{hi:.2f}"


def samples_from_markets(markets: Iterable[Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in markets:
        sample = sample_from_market(row if isinstance(row, dict) else None)
        if sample:
            out.append(sample)
    return out


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def collect_from_quote_bus() -> list[dict[str, Any]]:
    try:
        from golf_offshoot.quote_bus.bus import load_latest
    except Exception:  # noqa: BLE001 — missing bus is an empty sample, not a crash
        return []
    snap = load_latest() or {}
    return samples_from_markets(snap.get("markets") or [])


def collect_from_snapshots(*, limit: int = MAX_SNAPSHOT_FILES) -> list[dict[str, Any]]:
    folder = snapshots_dir_15m()
    if not folder.is_dir():
        return []
    files = sorted(folder.glob("*.json"), key=lambda p: p.name, reverse=True)[: max(0, int(limit))]
    out: list[dict[str, Any]] = []
    for path in files:
        payload = _load_json(path)
        markets = payload.get("markets")
        if not isinstance(markets, list):
            ingest = payload.get("ingest") if isinstance(payload.get("ingest"), dict) else {}
            markets = ingest.get("markets") if isinstance(ingest, dict) else []
        out.extend(samples_from_markets(markets or []))
    return out


def collect_from_paper_books() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    folder = paper_dir_15m()
    if not folder.is_dir():
        return []
    for path in folder.glob("KXBTC15M-*.json"):
        book = _load_json(path)
        positions = ((book.get("book") or {}).get("positions")) or []
        for pos in positions:
            if not isinstance(pos, dict):
                continue
            sample = sample_from_market(
                {
                    "ticker": pos.get("player_id"),
                    "yes_bid": pos.get("yes_bid"),
                    "yes_ask": pos.get("yes_ask"),
                    "paper_mark": pos.get("fill_price") or pos.get("entry_market_p"),
                }
            )
            if sample:
                out.append(sample)
    return out


def append_quotes(
    markets: list[dict[str, Any]],
    *,
    latest_dir: Path | None = None,
) -> list[dict[str, Any]]:
    samples = samples_from_markets(markets)
    if not samples:
        return []
    dest = quotes_log_path(latest_dir=latest_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("a", encoding="utf-8") as handle:
        for row in samples:
            handle.write(json.dumps(row) + "\n")
    return samples


def load_quote_log(*, latest_dir: Path | None = None) -> list[dict[str, Any]]:
    path = quotes_log_path(latest_dir=latest_dir)
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict):
                rows.append(row)
    except OSError:
        return []
    return rows


def build_profile(samples: list[dict[str, Any]]) -> dict[str, Any]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for row in samples:
        hs = row.get("half_spread")
        mark = row.get("mark")
        try:
            hs_f = float(hs)
            mark_f = float(mark)
        except (TypeError, ValueError):
            continue
        buckets[bucket_key(mark_f)].append(hs_f)
    bucket_rows = []
    for key in sorted(buckets, key=lambda k: float(k.split("-")[0])):
        vals = buckets[key]
        bucket_rows.append(
            {
                "bucket": key,
                "n": len(vals),
                "mean_half_spread": round(sum(vals) / len(vals), 6),
            }
        )
    n = len(samples)
    mean_all = round(sum(float(r["half_spread"]) for r in samples) / n, 6) if n else None
    return {
        "schema": 1,
        "lane": "learning_lane_15m",
        "series": "KXBTC15M",
        "formula": "(yes_ask - yes_bid) / 2",
        "bucket_width": BUCKET_WIDTH,
        "n": n,
        "mean_half_spread": mean_all,
        "buckets": bucket_rows,
        "written_at": isoformat_now(),
        "note": (
            "Empirical half-spread from quoted bid/ask already on disk or "
            "appended by PaperWatch. Not a fee. Not a bind. Display prices "
            "are not settle evidence."
        ),
    }


def write_profile(
    payload: dict[str, Any],
    *,
    root: Path | None = None,
    latest_dir: Path | None = None,
) -> dict[str, str]:
    docs = profile_path(root=root)
    docs.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2) + "\n"
    docs.write_text(text, encoding="utf-8")
    latest = latest_profile_path(latest_dir=latest_dir)
    latest.parent.mkdir(parents=True, exist_ok=True)
    latest.write_text(text, encoding="utf-8")
    return {"docs": str(docs), "latest": str(latest)}


def rebuild_from_disk(
    *,
    root: Path | None = None,
    latest_dir: Path | None = None,
    snapshot_limit: int = MAX_SNAPSHOT_FILES,
) -> dict[str, Any]:
    samples = []
    samples.extend(collect_from_quote_bus())
    samples.extend(collect_from_snapshots(limit=snapshot_limit))
    samples.extend(collect_from_paper_books())
    samples.extend(load_quote_log(latest_dir=latest_dir))
    profile = build_profile(samples)
    profile["sources"] = {
        "quote_bus": True,
        "snapshots_limit": snapshot_limit,
        "paper_books": True,
        "quote_log": True,
    }
    write_profile(profile, root=root, latest_dir=latest_dir)
    return profile


def record_live_quotes(
    markets: list[dict[str, Any]],
    *,
    root: Path | None = None,
    latest_dir: Path | None = None,
) -> dict[str, Any]:
    """PaperWatch hook. Appends live quotes and refreshes latest/; docs only if empty."""
    append_quotes(markets, latest_dir=latest_dir)
    samples = load_quote_log(latest_dir=latest_dir)
    if not samples:
        samples = samples_from_markets(markets)
    profile = build_profile(samples)
    latest = latest_profile_path(latest_dir=latest_dir)
    latest.parent.mkdir(parents=True, exist_ok=True)
    latest.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    docs = profile_path(root=root)
    if not docs.is_file() or not _load_json(docs).get("n"):
        write_profile(profile, root=root, latest_dir=latest_dir)
    return profile
