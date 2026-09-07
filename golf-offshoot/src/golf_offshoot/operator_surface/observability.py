"""Hub-UI shareable export. Binds to docs/observability-hub SCHEMA (PR #151).

Viewer reads only docs/observability-hub/data/manifest.json.
Lanes are an array. Numbers are strings. Forbidden keys are refused, not sanitised.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paper import iter_books, load_ledger
from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    LANE_GOLF,
    PRIMARY_SERIES,
    assert_not_golf_path,
    latest_dir_15m,
    settlements_dir_15m,
)
from golf_offshoot.learning_lane_15m.settle import SETTLE_PENDING, event_ticker_from_book_id
from golf_offshoot.localtime import isoformat_now

SCHEMA_VERSION = 1
SCHEMA_SOT = "docs/observability-hub/data/SCHEMA.md"
HUB_MANIFEST_REL = Path("docs") / "observability-hub" / "data" / "manifest.json"

REQUIRED_GLOBAL_BADGES = (
    "READ ONLY",
    "TRADING NOT ARMED",
    "PAPER OBSERVATION ONLY",
    "AI: NO CASH IN/OUT",
)

HARD_NOS = (
    "No ingest / live / shadow / loop / refresh controls",
    "No paper deposit / withdraw / transfer",
    "No trade arming, one-tap bet, or Kalshi trade keys",
    "No cash movement UI",
    "No API keys, secrets, or .env values on the page or in the committed client JS",
    "Missing charts stay \"not yet available\" — never invented",
    "Never claim edge / banked edge / \"edge established\"",
    "Never blur the golf WC1 FAIL into the 15-minute learning lane",
)

# Exact key names from Hub SCHEMA / validate_hub.py. Prose may use these words.
FORBIDDEN_KEYS = frozenset(
    {
        "action", "actions", "control", "controls", "button", "buttons",
        "form", "forms", "submit", "endpoint", "endpoints", "api", "api_base",
        "api_url", "api_endpoint", "post", "post_url", "run_url", "ingest",
        "live_run", "shadow_run", "loop", "refresh", "reload", "poll",
        "poll_url", "ws", "ws_url", "websocket", "stream_url", "arm", "arming",
        "armed", "trade", "trades", "trade_url", "order", "orders", "place",
        "place_bet", "cancel", "bet", "bets", "one_tap", "onetap", "autobet",
        "auto_bet",
        "deposit", "withdraw", "withdrawal", "transfer", "cash", "cash_in",
        "cash_out", "cashout", "cashin", "bankroll", "balance", "funds",
        "wallet", "stake_now", "money", "payout_url",
        "secret", "secrets", "api_key", "apikey", "api_secret", "token",
        "access_token", "refresh_token", "bearer", "password", "passwd",
        "credential", "credentials", "private_key", "privatekey", "key",
        "keys", "env", "dotenv", "ssh_key", "session", "cookie", "auth",
        "authorization", "kalshi_key", "kalshi_api_key",
    }
)

# Golf Phase 1 WC1 stays on golf only. Copied from PR #151 fixture when no hub file.
WC1_STATUS = "FAIL / park unproven · NOT edge"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def hub_manifest_path() -> Path:
    return repo_root() / HUB_MANIFEST_REL


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _walk_forbidden(node: Any, path: str = "") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            if str(key).lower() in FORBIDDEN_KEYS:
                raise RuntimeError(f"hub manifest refused forbidden key {key!r} at {child}")
            _walk_forbidden(value, child)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _walk_forbidden(item, f"{path}[{index}]")


def _load_existing_manifest(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _lane_by_id(manifest: dict[str, Any] | None, lane_id: str) -> dict[str, Any] | None:
    if not manifest:
        return None
    lanes = manifest.get("lanes")
    if not isinstance(lanes, list):
        return None
    for lane in lanes:
        if isinstance(lane, dict) and lane.get("lane_id") == lane_id:
            return lane
    return None


def _golf_lane_fallback() -> dict[str, Any]:
    """Minimal SCHEMA-valid golf lane used only when #151 manifest is absent."""
    return {
        "lane_id": LANE_GOLF,
        "label": "Golf — Phase 1 observation",
        "tab_label": "Golf · Phase 1",
        "lane_badge": "PHASE 1 OBSERVATION",
        "badges": [
            "PHASE 1 OBSERVATION",
            "NOT ARMED",
            "PAPER OBSERVATION ONLY",
            "AI: NO CASH IN/OUT",
            "NOT EDGE ESTABLISHED",
            "NOT BANKED MONEY",
        ],
        "summary_line": (
            "Golf-offshoot Phase 1. Paper observation only. Edge is not established."
        ),
        "source_kind": "real operating exports (not demo, not mock, not a Kalshi sandbox)",
        "lane_scope_note": (
            "Everything in this tab is the golf lane. The WC1 dated FAIL belongs "
            "to this lane only and does not transfer."
        ),
        "last_run": {
            "status": "not yet available",
            "headline": "Golf last-run honesty is published on the Hub UI fixture from PR #151.",
            "fields": [],
            "notes": ["This fallback does not invent golf figures."],
        },
        "settle": {
            "banner": None,
            "banner_state": "not_available",
            "headline": "Golf settle summary lives on the Hub UI fixture from PR #151.",
            "counts": [],
            "sources": [],
            "residual": [],
            "observation": None,
            "notes": ["Do not invent golf settle counts here."],
        },
        "paper_ledger": {
            "status": "not yet available",
            "headline": "Golf paper counts are published on the Hub UI fixture from PR #151.",
            "rows": [],
            "absent_fields": [],
            "notes": ["Operator golf ledger is gitignored and is not published here."],
        },
        "records": [
            {
                "record_id": "WC1",
                "title": "WC1 weekly operating claim — FAIL / park unproven · NOT edge",
                "verdict": "FAIL",
                "lean": "park unproven",
                "lane_scope_note": (
                    "This is a golf-lane record. It says nothing about learning_lane_15m."
                ),
                "rows": [
                    {"label": "Exit", "value": "FAIL"},
                    {"label": "Lean", "value": "park unproven"},
                ],
                "hard_nos": ["Never claim edge / banked edge / \"edge established\""],
                "links": [],
            }
        ],
        "charts": [],
        "charts_note": "Golf boards are published by the Hub UI tree. This fallback invents none.",
        "docs": [],
    }


def _settle_payloads() -> list[dict[str, Any]]:
    root = settlements_dir_15m()
    out: list[dict[str, Any]] = []
    if not root.is_dir():
        return out
    for path in sorted(root.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(payload, dict):
            out.append(payload)
    return out


def _settle_rows() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for payload in _settle_payloads():
        for row in payload.get("rows") or []:
            if isinstance(row, dict):
                out.append(row)
    return out


def collect_journal_windows(
    markets: list[dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """Windows for latest/journal.json: live snapshot plus paper/settlement books.

    Live markets alone can be empty (initialized-only feed). Paper books and
    settlement joins still name the observed windows.
    """
    by_key: dict[str, dict[str, str]] = {}

    def _put(row: dict[str, Any]) -> None:
        ticker = _as_str(row.get("ticker"))
        event_ticker = _as_str(row.get("event_ticker"))
        window = _as_str(row.get("window_id"))
        if not event_ticker and window:
            event_ticker = event_ticker_from_book_id(window)
        if not event_ticker and ticker:
            event_ticker = event_ticker_from_book_id(ticker)
        key = window or ticker or event_ticker
        if not key:
            return
        prev = by_key.get(key, {})
        by_key[key] = {
            "ticker": ticker or prev.get("ticker") or "",
            "event_ticker": event_ticker or prev.get("event_ticker") or "",
            "window_id": window or prev.get("window_id") or "",
            "status": _as_str(row.get("status") or prev.get("status") or ""),
            "result": _as_str(row.get("result") or row.get("kalshi_result") or prev.get("result") or ""),
        }

    for market in markets or []:
        if isinstance(market, dict):
            _put(market)

    for rec in iter_books():
        window = str(rec.tournament_id or "")
        event_ticker = event_ticker_from_book_id(window)
        status = "settled" if rec.settled_at is not None else "open"
        positions = list(rec.book.positions)
        if positions:
            for pos in positions:
                _put(
                    {
                        "ticker": pos.player_id,
                        "event_ticker": event_ticker,
                        "window_id": window,
                        "status": status,
                        "result": "",
                    }
                )
        else:
            _put(
                {
                    "ticker": "",
                    "event_ticker": event_ticker,
                    "window_id": window,
                    "status": status,
                    "result": "",
                }
            )

    for payload in _settle_payloads():
        top_event = _as_str(payload.get("event_ticker"))
        top_window = _as_str(payload.get("window_id"))
        rows = payload.get("rows") or []
        if not rows:
            _put(
                {
                    "ticker": "",
                    "event_ticker": top_event,
                    "window_id": top_window,
                    "status": "",
                    "result": "",
                }
            )
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            _put(
                {
                    "ticker": row.get("ticker"),
                    "event_ticker": row.get("event_ticker") or top_event,
                    "window_id": row.get("window_id") or top_window,
                    "status": row.get("status") or row.get("settle_status"),
                    "result": row.get("kalshi_result") or row.get("result") or "",
                }
            )
    return list(by_key.values())


def _build_15m_lane(
    *,
    markets: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    books = iter_books()
    ledger = load_ledger()
    settles = _settle_rows()
    pending = sum(1 for r in settles if str(r.get("settle_status") or "") != "settled")
    settled = sum(1 for r in settles if str(r.get("settle_status") or "") == "settled")
    open_books = sum(1 for b in books if b.settled_at is None)
    settled_books = sum(1 for b in books if b.settled_at is not None)
    has_journal = bool(books or ledger.entries or settles or markets)

    badges = [
        "LEARNING LANE",
        "NOT ARMED",
        "PAPER OBSERVATION ONLY",
        "AI: NO CASH IN/OUT",
        "NOT EDGE ESTABLISHED",
    ]
    docs = [
        {
            "label": "15-min Kalshi learning lane (paper observation)",
            "href": (
                "https://github.com/swellbear/gated-formalization/blob/master/"
                "golf-offshoot/docs/LEARNING_LANE_15M.md"
            ),
        }
    ]
    if not has_journal:
        badges.append("NO EXPORTS PUBLISHED YET")
        return {
            "lane_id": LANE_15M,
            "label": "15-minute Kalshi — learning lane",
            "tab_label": "15-min Kalshi · Learning",
            "lane_badge": "LEARNING LANE",
            "badges": badges,
            "summary_line": (
                "KXBTC15M learning lane. CF index BRTI. Official settle is Kalshi "
                "result matched to CF Benchmarks SOURCE. No journal has been "
                "published into this tree yet."
            ),
            "source_kind": "not yet available — no export published",
            "lane_scope_note": (
                "This lane has no weekly operating record of its own. The golf WC1 "
                "dated FAIL is a golf-lane record and does not apply here, in either direction."
            ),
            "last_run": {
                "status": "not yet available",
                "headline": "No run has been published for this lane.",
                "fields": [],
                "notes": [
                    "Series is KXBTC15M only. CF index id is pinned BRTI. "
                    "A CFB websocket average is observe-only and is never official settle.",
                    "Paper journals live under /workspace/kalshi_15m_exports/ and are not this file.",
                ],
            },
            "settle": {
                "banner": None,
                "banner_state": "not_available",
                "headline": "No settle summary published for this lane.",
                "counts": [],
                "sources": [],
                "residual": [],
                "observation": None,
                "notes": [
                    "Stay SETTLE_PENDING until Kalshi result. Do not invent win/lose.",
                    "Golf settle figures are golf figures and are not shown on this tab.",
                ],
            },
            "paper_ledger": {
                "status": "not yet available",
                "headline": "No paper ledger summary published for this lane.",
                "rows": [],
                "absent_fields": [],
                "notes": [
                    "When counts arrive they are counts. No cash figure is published here.",
                    "Leftovers stay documented PROPOSED (not Softened).",
                ],
            },
            "records": [],
            "records_note": (
                "No weekly operating record exists for this lane. "
                "Do not read the golf WC1 FAIL as this lane's result."
            ),
            "charts": [],
            "charts_note": (
                "No chart slots have been declared for this lane yet. "
                "Missing charts stay not yet available — never invented."
            ),
            "docs": docs,
        }

    banners = []
    for row in settles:
        status = _as_str(row.get("settle_status") or SETTLE_PENDING)
        banners.append(
            {
                "label": _as_str(row.get("ticker")),
                "value": status,
                "note": _as_str(row.get("banner") or row.get("note") or ""),
            }
        )
    banner_state = "pending" if pending or not settled else "off"
    banner = SETTLE_PENDING if banner_state == "pending" else "settled"
    journal_windows = collect_journal_windows(markets)
    window_rows = []
    for mkt in journal_windows:
        window_rows.append(
            {
                "label": _as_str(mkt.get("ticker") or mkt.get("window_id") or mkt.get("event_ticker")),
                "value": _as_str(mkt.get("status") or ""),
                "note": _as_str(mkt.get("window_id") or mkt.get("event_ticker") or ""),
            }
        )
    return {
        "lane_id": LANE_15M,
        "label": "15-minute Kalshi — learning lane",
        "tab_label": "15-min Kalshi · Learning",
        "lane_badge": "LEARNING LANE",
        "badges": badges,
        "summary_line": (
            "KXBTC15M learning lane. Paper observation only. Not live trading "
            "and not a golf WC1 edge."
        ),
        "source_kind": "paper observation journal (not a Kalshi cash account)",
        "lane_scope_note": (
            "Everything in this tab is learning_lane_15m. Golf WC1 / Ill do not transfer."
        ),
        "last_run": {
            "status": "published export",
            "headline": "15-min paper loop snapshot. Observation only.",
            "fields": [
                {"label": "Series", "value": PRIMARY_SERIES},
                {"label": "CF index", "value": "BRTI"},
                {"label": "CFB websocket average", "value": "observe only"},
                {"label": "never_auto_bet", "value": "true"},
                {"label": "paper_observation_only", "value": "true"},
                {"label": "Windows in this snapshot", "value": _as_str(len(journal_windows))},
            ],
            "notes": [
                "Official settle is Kalshi result matched to documented CF Benchmarks SOURCE.",
                "A CFB websocket / DIY 60s average is observe-only.",
            ],
        },
        "settle": {
            "banner": banner,
            "banner_state": banner_state,
            "headline": (
                "SETTLE_PENDING until Kalshi result. can_close_early: wait; "
                "if close_time moves the window re-keys."
            ),
            "counts": [
                {"label": "Pending windows", "value": _as_str(pending)},
                {"label": "Settled windows", "value": _as_str(settled)},
            ],
            "sources": [
                {"label": "official_settle", "value": "Kalshi result matched to CF Benchmarks SOURCE"},
            ],
            "residual": banners,
            "observation": None,
            "notes": [
                "Do not invent win/lose. Display prices are not settle evidence.",
            ],
        },
        "paper_ledger": {
            "status": "counts only — no cash figures published",
            "headline": "Paper ticket counts. No cash figure is published on this page.",
            "rows": [
                {"label": "Open books", "value": _as_str(open_books)},
                {"label": "Settled books", "value": _as_str(settled_books)},
                {"label": "Ledger entries", "value": _as_str(len(ledger.entries))},
                {"label": "Series", "value": PRIMARY_SERIES},
            ],
            "absent_fields": ["payout", "realized_pnl", "roi"],
            "notes": [
                "Counts only. Cash-shaped columns are absent, not derived.",
                "Leftovers stay documented PROPOSED (not Softened).",
            ],
        },
        "records": [],
        "records_note": (
            "No weekly operating record exists for this lane. "
            "Do not read the golf WC1 FAIL as this lane's result."
        ),
        "charts": [],
        "charts_note": "15m viz wall is not yet available. Charts are not invented.",
        "docs": docs,
    }


def _hub_block(*, source_kind: str, generated_at: str) -> dict[str, Any]:
    return {
        "title": "gated-formalization — observability hub",
        "subtitle": "Read-only mirror of published artifacts. No controls, no cash, no keys.",
        "generated_at": generated_at,
        "source_kind": source_kind,
        "source_note": (
            "Systems export bound to docs/observability-hub/data/SCHEMA.md (PR #151). "
            "Golf figures stay the published Hub fixture unless already on disk. "
            + (
                "learning_lane_15m paper journal is published in this Pages manifest."
                if source_kind == "export"
                else "15m journals stay under /workspace/kalshi_15m_exports/ until published here."
            )
        ),
        "control_surface_note": (
            "The control surface is the local operator shell at 127.0.0.1:8765 "
            "on the operator's own machine. It is deliberately not reachable from "
            "this page and is not linked from it."
        ),
    }


def _global_block() -> dict[str, Any]:
    return {
        "badges": list(REQUIRED_GLOBAL_BADGES),
        "wall_lines": [
            "This page is a viewer. It has no ingest, live, shadow, loop, or refresh control.",
            "No paper deposit, withdraw, or transfer. No cash movement of any kind.",
            "No trade arming, no one-tap bet, no Kalshi account, key, or wallet scope.",
            "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH.",
        ],
        "hard_nos": list(HARD_NOS),
    }


def build_hub_manifest(
    *,
    markets: list[dict[str, Any]] | None = None,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Hub-UI manifest. lanes is an array. Numbers are strings."""
    golf = _lane_by_id(existing, LANE_GOLF) or _golf_lane_fallback()
    if golf.get("lane_id") != LANE_GOLF:
        raise RuntimeError("golf lane_id must be exact 'golf'")
    lane15 = _build_15m_lane(markets=markets)
    if "wc1" in lane15 or any(
        str(rec.get("record_id") or "").lower() == "wc1" for rec in (lane15.get("records") or [])
    ):
        raise RuntimeError("never put golf WC1 under learning_lane_15m")
    has_15m_journal = lane15["last_run"].get("status") != "not yet available"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "hub": _hub_block(
            source_kind="export" if has_15m_journal else "fixture",
            generated_at=isoformat_now(),
        ),
        "global": _global_block(),
        "lanes": [golf, lane15],
    }
    ids = [lane.get("lane_id") for lane in payload["lanes"]]
    if ids != [LANE_GOLF, LANE_15M]:
        raise RuntimeError(f"canonical lane ids must be golf then learning_lane_15m, got {ids}")
    _walk_forbidden(payload)
    return payload


def build_observability_payload(
    *,
    markets: list[dict[str, Any]] | None = None,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Alias for callers that still use the old name. Hub SCHEMA only."""
    return build_hub_manifest(markets=markets, existing=existing)


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def write_observability_exports(
    *,
    markets: list[dict[str, Any]] | None = None,
    hub_dir: Path | None = None,
) -> dict[str, str]:
    """Publish Hub-UI manifest + a separate 15m live journal. No control surface."""
    dest = (hub_dir / "manifest.json") if hub_dir is not None else hub_manifest_path()
    existing = _load_existing_manifest(dest)
    payload = build_hub_manifest(markets=markets, existing=existing)
    hub_path = _write_json(dest, payload)

    journal = {
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "cf_index_id": "BRTI",
        "cfb_ws_average_role": "observe_only",
        "generated_at": payload["hub"]["generated_at"],
        "note": "Live 15m journal. Not the Hub UI contract. Hub reads only manifest.json.",
        "windows": collect_journal_windows(markets),
    }
    _walk_forbidden(journal)
    latest = latest_dir_15m() / "journal.json"
    assert_not_golf_path(latest)
    live_path = _write_json(latest, journal)
    return {
        "hub_manifest": str(hub_path),
        "learning_lane_15m_journal": str(live_path),
    }
