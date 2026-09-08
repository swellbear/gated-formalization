"""Learning wake for lane 15m. Evidence in, owed roles out.

PaperWatch fetches KXBTC15M, paper-fills at the posted mark, joins the official
Kalshi result and exports, every ~90 seconds. That half of the cadence runs with
nobody reading it. This module is the other half's doorbell: it reads the files
the loop already wrote and works out whether a window gained an official result,
whether a new paper book appeared, or whether something that was pending has
cleared -- and records which roles are *owed* a turn.

Owed is a request. It is never a completion. Nothing here writes a desk thread
line, Softens, ADMITs, or invents a win, a loss or a pnl; every figure printed is
copied out of a file that already had it. A role leaves ``roles_owed`` only when
an agent that really ran calls :func:`mark_roles_served`. The watch loop never
calls it, so an unserved wake keeps ageing and stays visible instead of being
quietly forgotten.

Reads: ``settlements/*.json``, ``paper/*.json`` + ``paper/ledger.json``,
``latest/journal.json``, ``docs/observability-hub/data/manifest.json``, and the
Chief of Staff honesty stamp on ``docs/agents/DESK.md``.
Writes: ``latest/learning_wake.json`` only, which is gitignored.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    PRIMARY_SERIES,
    assert_not_golf_path,
    latest_dir_15m,
    settlements_dir_15m,
)
from golf_offshoot.learning_lane_15m.settle import SETTLE_PENDING, SETTLE_SETTLED
from golf_offshoot.localtime import format_eastern, isoformat_now, now
from golf_offshoot.operator_surface.observability import repo_root

SCHEMA = 1
WAKE_FILE = "learning_wake.json"

REL_MANIFEST = Path("docs") / "observability-hub" / "data" / "manifest.json"
REL_DESK = Path("docs") / "agents" / "DESK.md"

#: Protocol order for the learning tick. Lab is not in it by default.
ROLE_ORDER = ("digestor", "operator", "systems", "validator")
LAB_ROLE = "lab"

EVENT_NEW_SETTLE = "new_settle"
EVENT_NEW_FILL = "new_fill"
EVENT_PENDING_CLEARED = "pending_cleared"

HEARTBEAT_NOTE = "no new settle; watch still running"

#: An owed role older than one 15-minute window has been sitting through a whole
#: lane cycle without anyone answering it. Age is shown either way; this only
#: decides when the tick says so out loud.
STALE_AFTER_S = 900.0

MAX_EVENTS = 24
MAX_SERVED = 24
MAX_REASONS = 8

NO_PAPER_PNL = "no paper pnl on this tree; none is invented"

STATE_OFFICIAL_NO_BOOK = "official result present; paper book not on this tree"
STATE_NO_BOOK_NO_RESULT = "no paper book on this tree; no official result on this tree either"

# Digestor's committed wording for a window Kalshi has already settled that has no
# paper book here (LEARNING_LANE_15M_SOURCE_DIGEST.md §4a). Kept in one place so the
# wake tick and the published manifest cannot drift apart on it.
MISSING_JOIN_BANNER = "missing paper join — official result present"
MISSING_JOIN_REASON = (
    "Kalshi settled this window {result}. The paper book the published lineage names "
    "is not on this tree, so there is no paper pnl here and none is invented. That is "
    "a missing paper join, not a pending window."
)

LINEAGE_A = "lineage A — local paper book on this tree"
LINEAGE_B = "lineage B — published Pages export"
NEVER_SUMMED = (
    "Lineage A and lineage B are two separate paper books over the same series. "
    "Their counts and pnl figures are never added together."
)

CONTRACT = (
    "roles_owed is a request for a turn. It is never a record that a role ran.",
    "This module writes no desk thread line, Softens nothing, and ADMITs nothing.",
    "No win, lose or pnl is invented here. Every figure is copied from a file.",
    "A role leaves roles_owed only when an agent that really ran calls mark_roles_served().",
    "The watch loop never marks a role served.",
)


# --------------------------------------------------------------------------- io


def wake_state_path() -> Path:
    path = latest_dir_15m() / WAKE_FILE
    assert_not_golf_path(path)
    return path


def hub_manifest_path() -> Path:
    return repo_root() / REL_MANIFEST


def desk_path() -> Path:
    return repo_root() / REL_DESK


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_wake_state() -> dict[str, Any] | None:
    payload = _read_json(wake_state_path())
    return payload if isinstance(payload, dict) else None


def save_wake_state(state: dict[str, Any]) -> Path:
    dest = wake_state_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    assert_not_golf_path(dest)
    dest.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return dest


# ----------------------------------------------------------------------- format


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _pnl_text(value: Any) -> str | None:
    """A paper pnl already recorded on a file. Never derived, never defaulted to 0."""
    if value is None:
        return None
    try:
        return f"{float(value):+.2f}"
    except (TypeError, ValueError):
        return None


def _parse_iso(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _age_s(since: str, at: datetime) -> float:
    started = _parse_iso(since)
    if started is None:
        return 0.0
    if started.tzinfo is None:
        started = started.replace(tzinfo=at.tzinfo)
    return max(0.0, (at - started).total_seconds())


def _age_text(seconds: float) -> str:
    total = int(seconds)
    if total < 60:
        return f"{total}s"
    if total < 3600:
        return f"{total // 60}m {total % 60:02d}s"
    return f"{total // 3600}h {(total % 3600) // 60:02d}m"


# ------------------------------------------------------------------------ files


def _settlement_rows() -> list[dict[str, Any]]:
    """Every join row written by settle.py, newest file last."""
    root = settlements_dir_15m()
    out: list[dict[str, Any]] = []
    if not root.is_dir():
        return out
    for path in sorted(root.glob("*.json")):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            continue
        for row in payload.get("rows") or []:
            if isinstance(row, dict):
                out.append(row)
    return out


def _journal_rows() -> list[dict[str, Any]]:
    payload = _read_json(latest_dir_15m() / "journal.json")
    if not isinstance(payload, dict):
        return []
    return [w for w in payload.get("windows") or [] if isinstance(w, dict)]


def _paper_books() -> dict[str, dict[str, Any]]:
    """One entry per window book on this tree, keyed by window_id."""
    from golf_offshoot.learning_lane_15m.paper import iter_books

    out: dict[str, dict[str, Any]] = {}
    for rec in iter_books():
        window_id = str(rec.tournament_id or "")
        if not window_id:
            continue
        tickers: list[str] = []
        for mv in rec.movements:
            if mv.player_id and mv.player_id not in tickers:
                tickers.append(str(mv.player_id))
        for pos in rec.book.positions:
            if pos.player_id and pos.player_id not in tickers:
                tickers.append(str(pos.player_id))
        out[window_id] = {
            "window_id": window_id,
            "tickers": tickers,
            "opened_at": _as_str(rec.locked_at),
            "settled_at": _as_str(rec.settled_at),
            "open_positions": len(rec.book.positions),
            "paper_pnl": _pnl_text(rec.settlement_pnl) if rec.settled_at is not None else None,
        }
    return out


def _ledger_summary() -> dict[str, str]:
    from golf_offshoot.learning_lane_15m.paper import load_ledger

    led = load_ledger()
    kinds: dict[str, int] = {}
    for entry in led.entries:
        kind = str(entry.kind or "")
        kinds[kind] = kinds.get(kind, 0) + 1
    return {
        "entries": _as_str(len(led.entries)),
        "paper_fill_entries": _as_str(kinds.get("paper_fill", 0)),
        "settle_entries": _as_str(kinds.get("settle_win", 0) + kinds.get("settle_loss", 0)),
    }


def _published_paper_windows(path: Path | None = None) -> dict[str, dict[str, str]]:
    """Windows the published Pages manifest already names as paper fills.

    Read so a published paper outcome is never dropped, and so a window the
    published lineage claims a book for can be checked against this tree.
    """
    payload = _read_json(path or hub_manifest_path())
    if not isinstance(payload, dict):
        return {}
    lane = next(
        (
            candidate
            for candidate in payload.get("lanes") or []
            if isinstance(candidate, dict) and candidate.get("lane_id") == LANE_15M
        ),
        None,
    )
    if lane is None:
        return {}
    last_run = lane.get("last_run") if isinstance(lane.get("last_run"), dict) else {}
    fields: dict[str, str] = {}
    for entry in (last_run or {}).get("fields") or []:
        if isinstance(entry, dict) and entry.get("label"):
            fields[str(entry["label"])] = _as_str(entry.get("value")).strip()

    out: dict[str, dict[str, str]] = {}
    settled_ticker = fields.get("Settled paper fill", "")
    if settled_ticker:
        out[settled_ticker] = {
            "ticker": settled_ticker,
            "paper_outcome": fields.get("Paper outcome", ""),
            "published_paper_pnl": fields.get("paper settle_win pnl", ""),
            "published_value": fields.get("Paper outcome", ""),
            "published_note": "published last_run field 'Settled paper fill'",
        }
    live_ticker = fields.get("Live paper fill", "")
    if live_ticker and live_ticker not in out:
        out[live_ticker] = {
            "ticker": live_ticker,
            "paper_outcome": "",
            "published_paper_pnl": "",
            "published_value": fields.get("Live paper fill status", ""),
            "published_note": "published last_run field 'Live paper fill'",
        }
    for row in ((lane.get("settle") or {}).get("residual") or []):
        if not isinstance(row, dict):
            continue
        label = _as_str(row.get("label")).strip()
        if not label.startswith(PRIMARY_SERIES) or label in out:
            continue
        out[label] = {
            "ticker": label,
            "paper_outcome": "",
            "published_paper_pnl": "",
            "published_value": _as_str(row.get("value")),
            "published_note": "published settle residual row",
        }
    return out


# ------------------------------------------------------------------------- scan


def _pending_kind(note: str, settle_status: str) -> str:
    text = (note or "").lower()
    if "no kalshi market payload" in text:
        return "no_market_payload"
    if "disputed" in text or "under review" in text:
        return "disputed"
    if settle_status and settle_status != SETTLE_SETTLED and "can_close_early" in text:
        return "awaiting_kalshi_result"
    if settle_status == "never_settled":
        return "never_settled"
    return "awaiting_kalshi_result"


def scan_learning_evidence(*, manifest_path: Path | None = None) -> dict[str, Any]:
    """Fingerprint the lane from disk. Pure read -- no book, ledger or desk is touched."""
    settled: dict[str, dict[str, str]] = {}

    for window in _journal_rows():
        ticker = _as_str(window.get("ticker")).strip()
        result = _as_str(window.get("result")).strip().lower()
        if not ticker or result not in {"yes", "no"}:
            continue
        settled[ticker] = {
            "ticker": ticker,
            "window_id": _as_str(window.get("window_id")),
            "result": result,
            "kalshi_status": _as_str(window.get("status")),
            "source": "latest/journal.json",
            "settlement_ts": "",
            "source_matched": "",
        }

    join_rows = _settlement_rows()
    for row in join_rows:
        ticker = _as_str(row.get("ticker")).strip()
        result = _as_str(row.get("kalshi_result")).strip().lower()
        if not ticker or result not in {"yes", "no"}:
            continue
        if _as_str(row.get("settle_status")) != SETTLE_SETTLED:
            continue
        settled[ticker] = {
            "ticker": ticker,
            "window_id": _as_str(row.get("window_id")),
            "result": result,
            "kalshi_status": _as_str(row.get("status")),
            "source": "settlements/*.json",
            "settlement_ts": _as_str(row.get("settlement_ts")),
            "source_matched": _as_str(row.get("source_matched")),
        }

    books = _paper_books()

    pending: list[dict[str, str]] = []
    seen_pending: set[str] = set()
    for row in join_rows:
        status = _as_str(row.get("settle_status"))
        if status == SETTLE_SETTLED:
            continue
        ticker = _as_str(row.get("ticker")).strip()
        window_id = _as_str(row.get("window_id"))
        key = ticker or window_id
        # A window that already carries an official result is not pending. The
        # join simply has not been applied on this tree yet, and the next diff
        # reports that as pending_cleared rather than holding a false pending.
        if not key or key in seen_pending or ticker in settled:
            continue
        seen_pending.add(key)
        note = _as_str(row.get("note")) or _as_str(row.get("banner"))
        pending.append(
            {
                "ticker": ticker,
                "window_id": window_id,
                "settle_status": status,
                "kind": _pending_kind(note, status),
                "reason": note,
                "source": "settlements/*.json",
            }
        )
    for window_id, book in books.items():
        if book["settled_at"] or not book["open_positions"]:
            continue
        keys = {t for t in book["tickers"]} | {window_id}
        if keys & seen_pending or any(t in settled for t in book["tickers"]):
            continue
        seen_pending.add(window_id)
        pending.append(
            {
                "ticker": book["tickers"][0] if book["tickers"] else "",
                "window_id": window_id,
                "settle_status": "",
                "kind": "book_open_no_join",
                "reason": (
                    "Paper book is open on this window and no settle join file has "
                    "been written for it yet. Wait for the Kalshi result."
                ),
                "source": "paper/*.json",
            }
        )

    local_tickers = {t for book in books.values() for t in book["tickers"]}
    published = _published_paper_windows(manifest_path)
    paper_join_missing: list[dict[str, Any]] = []
    published_only: list[dict[str, Any]] = []
    for ticker, pub in published.items():
        if ticker in local_tickers:
            continue
        official = settled.get(ticker)
        pnl = pub.get("published_paper_pnl", "")
        outcome = pub.get("paper_outcome", "")
        if pnl or outcome.startswith("paper_"):
            # Lineage B. The join is published, just not on this tree. Kept whole.
            published_only.append(
                {
                    "ticker": ticker,
                    "paper_outcome": outcome,
                    "published_paper_pnl": pnl,
                    "official_result": (official or {}).get("result", ""),
                    "paper_book_on_tree": False,
                    "source": REL_MANIFEST.as_posix(),
                    "note": (
                        "Published Pages lineage. Kept as published history, not "
                        "re-derived here and never added to the local paper book."
                    ),
                }
            )
            continue
        result = (official or {}).get("result", "")
        paper_join_missing.append(
            {
                "ticker": ticker,
                "window_id": (official or {}).get("window_id", ""),
                "official_result": result,
                "official_source": (official or {}).get("source", ""),
                "published_value": pub.get("published_value", ""),
                "paper_book_on_tree": False,
                "paper_pnl": None,
                "state": STATE_OFFICIAL_NO_BOOK if result else STATE_NO_BOOK_NO_RESULT,
                "reason": (
                    MISSING_JOIN_REASON.format(result=result)
                    if result
                    else (
                        "The published lineage names a paper book for this window and "
                        "the book is not on this tree. No official result for it is on "
                        "this tree either. Nothing is inferred in either direction."
                    )
                ),
            }
        )

    return {
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "scanned_at": isoformat_now(),
        "settled": settled,
        "fills": books,
        "pending": pending,
        "paper_join_missing": paper_join_missing,
        "published_only": published_only,
        "ledger": _ledger_summary(),
        "read_only": True,
        "sources": [
            "settlements/*.json",
            "paper/*.json",
            "paper/ledger.json",
            "latest/journal.json",
            REL_MANIFEST.as_posix(),
        ],
    }


# ----------------------------------------------------------------------- events


def roles_owed_for(
    kind: str,
    *,
    honesty_gate_passed: bool = False,
    operator_residual_posted: bool = False,
) -> list[str]:
    """Protocol order. Lab is added only when both gates are explicitly true."""
    roles = list(ROLE_ORDER)
    if honesty_gate_passed and operator_residual_posted:
        roles.append(LAB_ROLE)
    return roles


def diff_scans(previous: dict[str, Any] | None, current: dict[str, Any]) -> list[dict[str, Any]]:
    """Events between two scans. A first scan has no previous, so it raises none."""
    if not previous:
        return []
    events: list[dict[str, Any]] = []

    prev_settled = previous.get("settled") or {}
    for ticker, row in (current.get("settled") or {}).items():
        before = prev_settled.get(ticker) or {}
        if before.get("result") == row.get("result"):
            continue
        events.append(
            {
                "kind": EVENT_NEW_SETTLE,
                "ticker": ticker,
                "window_id": row.get("window_id", ""),
                "detail": f"official Kalshi result={row.get('result')} via {row.get('source')}",
            }
        )

    prev_fills = previous.get("fills") or {}
    for window_id, book in (current.get("fills") or {}).items():
        if window_id in prev_fills:
            continue
        tickers = ", ".join(book.get("tickers") or []) or window_id
        events.append(
            {
                "kind": EVENT_NEW_FILL,
                "ticker": (book.get("tickers") or [""])[0],
                "window_id": window_id,
                "detail": f"new paper book on this tree for {tickers}",
            }
        )

    now_pending = {
        _as_str(row.get("ticker")) or _as_str(row.get("window_id"))
        for row in current.get("pending") or []
    }
    for row in previous.get("pending") or []:
        key = _as_str(row.get("ticker")) or _as_str(row.get("window_id"))
        if not key or key in now_pending:
            continue
        settled_now = (current.get("settled") or {}).get(_as_str(row.get("ticker"))) or {}
        detail = "no longer pending on this tree"
        if settled_now.get("result"):
            detail = f"pending cleared by official Kalshi result={settled_now['result']}"
        events.append(
            {
                "kind": EVENT_PENDING_CLEARED,
                "ticker": _as_str(row.get("ticker")),
                "window_id": _as_str(row.get("window_id")),
                "detail": detail,
            }
        )
    return events


def _event_label(event: dict[str, Any]) -> str:
    who = _as_str(event.get("ticker")) or _as_str(event.get("window_id")) or "window"
    return f"{event.get('kind')} {who}"


def _merge_roles_owed(
    existing: Iterable[dict[str, Any]],
    events: Sequence[dict[str, Any]],
    *,
    at: str,
    at_dt: datetime,
) -> list[dict[str, Any]]:
    """Add roles the new events request. Never drop or clear an existing one."""
    by_role: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for entry in existing:
        role = _as_str(entry.get("role"))
        if not role or role in by_role:
            continue
        by_role[role] = dict(entry)
        order.append(role)

    for event in events:
        for role in event.get("roles_owed") or []:
            entry = by_role.get(role)
            if entry is None:
                entry = {
                    "role": role,
                    "owed_since": at,
                    "reasons": [],
                    "requested_by": "learning_wake evidence scan",
                }
                by_role[role] = entry
                order.append(role)
            reason = _event_label(event)
            reasons = [r for r in entry.get("reasons") or [] if r != reason]
            reasons.append(reason)
            entry["reasons"] = reasons[-MAX_REASONS:]

    out: list[dict[str, Any]] = []
    for role in sorted(order, key=lambda r: (ROLE_ORDER + (LAB_ROLE,)).index(r) if r in ROLE_ORDER + (LAB_ROLE,) else 99):
        entry = by_role[role]
        age = _age_s(_as_str(entry.get("owed_since")) or at, at_dt)
        entry["age_s"] = int(age)
        entry["age_text"] = _age_text(age)
        entry["stale"] = age >= STALE_AFTER_S
        entry["served_at"] = None
        out.append(entry)
    return out


# ------------------------------------------------------------------- lab gate


def honesty_gate_from_desk(path: Path | None = None) -> dict[str, Any]:
    """Read the Chief of Staff honesty stamp. Never write it, never infer a PASS.

    No stamp on the desk is not a pass. Anything short of an all-PASS table
    leaves the gate shut, which is the only direction this read can move it.
    """
    dest = path or desk_path()
    try:
        text = dest.read_text(encoding="utf-8")
    except OSError:
        return {
            "stamp_found": False,
            "passed": False,
            "boxes": [],
            "note": "no desk file to read the Chief of Staff honesty stamp from",
        }
    boxes: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("## honesty checklist"):
            in_table = True
            continue
        if in_table and stripped.startswith("## "):
            break
        if not in_table or not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in {"box", ""} or set(cells[0]) <= set("- :"):
            continue
        state = "FAIL" if "**FAIL**" in cells[1] else ("PASS" if "**PASS**" in cells[1] else "")
        boxes.append({"box": cells[0], "state": state or "unstamped"})
    failing = [b["box"] for b in boxes if b["state"] != "PASS"]
    return {
        "stamp_found": bool(boxes),
        "passed": bool(boxes) and not failing,
        "boxes": boxes,
        "note": (
            "all boxes stamped PASS"
            if boxes and not failing
            else (
                f"not passed: {'; '.join(failing)}"
                if boxes
                else "no honesty checklist stamped on the desk"
            )
        ),
    }


def _lab_gate_block(gate: dict[str, Any], *, operator_residual_posted: bool) -> dict[str, Any]:
    owed = bool(gate.get("passed")) and operator_residual_posted
    if owed:
        why = "honesty checklist stamped PASS and an Operator residual was passed in"
    elif not gate.get("passed"):
        why = f"honesty gate has not passed -- {gate.get('note')}"
    else:
        why = "no Operator residual was passed in; Lab never starts from a scan alone"
    return {
        "lab_owed": owed,
        "honesty_gate_passed": bool(gate.get("passed")),
        "operator_residual_posted": bool(operator_residual_posted),
        "why": why,
        "boxes": gate.get("boxes") or [],
        "note": (
            "Lab is off by default. This scan can only report the stamp CoS wrote; "
            "it never stamps one and never self-admits."
        ),
    }


# -------------------------------------------------------------------------- tick


def record_learning_tick(
    *,
    watch_status: dict[str, Any] | None = None,
    manifest_path: Path | None = None,
    desk: Path | None = None,
    honesty_gate_passed: bool | None = None,
    operator_residual_posted: bool = False,
) -> dict[str, Any]:
    """One wake tick: scan, diff against stored state, persist. Never marks served."""
    at_dt = now()
    at = isoformat_now(at_dt)
    scan = scan_learning_evidence(manifest_path=manifest_path)
    state = load_wake_state()
    previous = (state or {}).get("scan")

    gate = honesty_gate_from_desk(desk)
    passed = gate["passed"] if honesty_gate_passed is None else bool(honesty_gate_passed)

    events = diff_scans(previous, scan)
    for event in events:
        event["at"] = at
        event["lane"] = LANE_15M
        event["series"] = PRIMARY_SERIES
        event["roles_owed"] = roles_owed_for(
            str(event.get("kind") or ""),
            honesty_gate_passed=passed,
            operator_residual_posted=operator_residual_posted,
        )
        event["roles_owed_is_a_request"] = True

    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()

    owed = _merge_roles_owed(
        (state or {}).get("roles_owed") or [],
        events,
        at=at,
        at_dt=at_dt,
    )

    heartbeat = None
    if not events:
        heartbeat = {
            "at": at,
            "watch_cycles": _as_str(watch_status.get("cycles")),
            "watch_running": bool(watch_status.get("running")),
            "pending": len(scan["pending"]),
            "note": HEARTBEAT_NOTE,
        }

    history = list(events) + list((state or {}).get("events") or [])
    new_state = {
        "schema": SCHEMA,
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "trading_armed": False,
        "updated_at": at,
        "seeded_at": (state or {}).get("seeded_at") or at,
        "seeded_this_tick": state is None,
        "contract": list(CONTRACT),
        "watch": {
            "running": bool(watch_status.get("running")),
            "cycles": _as_str(watch_status.get("cycles")),
            "interval_s": _as_str(watch_status.get("interval_s")),
            "last_at": _as_str(watch_status.get("last_at")),
            "last_summary": _as_str(watch_status.get("last_summary")),
        },
        "scan": scan,
        "new_events": events,
        "events": history[:MAX_EVENTS],
        "roles_owed": owed,
        "served": list((state or {}).get("served") or [])[:MAX_SERVED],
        "heartbeat": heartbeat,
        "lab_gate": _lab_gate_block(gate, operator_residual_posted=operator_residual_posted),
    }
    save_wake_state(new_state)
    return new_state


def mark_roles_served(
    roles: Sequence[str],
    *,
    by: str = "",
    note: str = "",
) -> dict[str, Any] | None:
    """Clear owed roles. Only a role that really ran calls this; the loop never does."""
    state = load_wake_state()
    if state is None:
        return None
    wanted = {str(role).strip().lower() for role in roles if str(role).strip()}
    if not wanted:
        return state
    at = isoformat_now()
    keep: list[dict[str, Any]] = []
    served = list(state.get("served") or [])
    for entry in state.get("roles_owed") or []:
        if _as_str(entry.get("role")).lower() in wanted:
            served.insert(
                0,
                {
                    **entry,
                    "served_at": at,
                    "served_by": by or _as_str(entry.get("role")),
                    "served_note": note,
                },
            )
        else:
            keep.append(entry)
    state["roles_owed"] = keep
    state["served"] = served[:MAX_SERVED]
    state["updated_at"] = at
    save_wake_state(state)
    return state


# ------------------------------------------------------------------------ print


def _owed_summary(state: dict[str, Any]) -> str:
    owed = state.get("roles_owed") or []
    if not owed:
        return "none"
    oldest = max((int(e.get("age_s") or 0) for e in owed), default=0)
    names = ", ".join(_as_str(e.get("role")) for e in owed)
    return f"{names} (oldest {_age_text(oldest)})"


def format_wake_line(state: dict[str, Any] | None) -> str:
    """Short block for the desktop 15m journal. Text only -- the hub owns its chrome."""
    if not state:
        return (
            "learning wake  not recorded yet on this tree — "
            "no roles are owed and none are claimed"
        )
    scan = state.get("scan") or {}
    new_events = state.get("new_events") or []
    lines = [
        "learning wake  owed={owed}  new={new}  pending={pending}  "
        "paper-join-missing={missing}  checked={at}".format(
            owed=_owed_summary(state),
            new=len(new_events),
            pending=len(scan.get("pending") or []),
            missing=len(scan.get("paper_join_missing") or []),
            at=format_eastern(state.get("updated_at")),
        )
    ]
    for event in new_events[:4]:
        lines.append(f"  {_event_label(event)} — {event.get('detail')}")
    heartbeat = state.get("heartbeat")
    if heartbeat and not new_events:
        lines.append(
            f"  heartbeat: {heartbeat.get('note')} "
            f"(watch cycles {heartbeat.get('watch_cycles')})"
        )
    for row in (scan.get("paper_join_missing") or [])[:3]:
        lines.append(
            f"  {row.get('ticker')} — {row.get('state')}; {NO_PAPER_PNL}"
        )
    if state.get("roles_owed"):
        lines.append(
            "  roles_owed is a request for a turn. The loop never marks a role served."
        )
    return "\n".join(lines)


def format_wake_tick(state: dict[str, Any] | None) -> str:
    """The tick CoS reads. Everything on it came off a file."""
    if not state:
        return (
            "LEARNING WAKE  no state on this tree yet.\n"
            "Run the 15m watch, or `python -m golf_offshoot learn-15m`, to seed it.\n"
            "No roles are owed, and none are claimed."
        )
    scan = state.get("scan") or {}
    watch = state.get("watch") or {}
    new_events = state.get("new_events") or []
    lines = [
        f"LEARNING WAKE  lane={state.get('lane')} series={state.get('series')} "
        f"trading_armed=false",
        f"updated {format_eastern(state.get('updated_at'), with_seconds=True)}  "
        f"watch running={_as_str(watch.get('running'))} cycles={watch.get('cycles')}  "
        f"settled={len(scan.get('settled') or {})} fills={len(scan.get('fills') or {})} "
        f"pending={len(scan.get('pending') or [])}",
    ]
    if state.get("seeded_this_tick"):
        lines.append("first scan on this tree — state seeded, no events raised from it")

    lines.append("")
    if new_events:
        lines.append(f"new events ({len(new_events)})")
        for event in new_events:
            lines.append(f"  {_event_label(event)} — {event.get('detail')}")
            lines.append(f"    roles owed: {', '.join(event.get('roles_owed') or [])}")
    else:
        heartbeat = state.get("heartbeat") or {}
        lines.append(
            f"heartbeat  {heartbeat.get('note') or HEARTBEAT_NOTE}  "
            f"(watch cycles {heartbeat.get('watch_cycles') or watch.get('cycles')}, "
            f"pending {heartbeat.get('pending', len(scan.get('pending') or []))})"
        )
        recent = state.get("events") or []
        if recent:
            lines.append(
                f"last event  {_event_label(recent[0])} — {recent[0].get('detail')} "
                f"at {format_eastern(recent[0].get('at'), with_seconds=True)}"
            )

    lines.append("")
    owed = state.get("roles_owed") or []
    if owed:
        lines.append(f"roles owed ({len(owed)}) — a request for a turn, not a completion")
        for entry in owed:
            flag = "  STALE" if entry.get("stale") else ""
            lines.append(
                f"  {_as_str(entry.get('role')):<10} owed {entry.get('age_text')}{flag}"
            )
            for reason in entry.get("reasons") or []:
                lines.append(f"    for: {reason}")
    else:
        lines.append("roles owed: none")
    gate = state.get("lab_gate") or {}
    lines.append(
        f"  {LAB_ROLE:<10} {'owed' if gate.get('lab_owed') else 'NOT owed'} — {gate.get('why')}"
    )

    pending = scan.get("pending") or []
    lines.append("")
    lines.append(f"pending windows ({len(pending)})")
    for row in pending:
        lines.append(
            f"  {row.get('ticker') or row.get('window_id')}  {row.get('kind')}  "
            f"[{row.get('source')}]"
        )
        lines.append(f"    {row.get('reason')}")
    if not pending:
        lines.append("  none on file")

    missing = scan.get("paper_join_missing") or []
    if missing:
        lines.append("")
        lines.append(f"official result, paper book not on this tree ({len(missing)})")
        for row in missing:
            lines.append(
                f"  {row.get('ticker')}  kalshi result="
                f"{row.get('official_result') or 'none on this tree'}  "
                f"paper pnl: {NO_PAPER_PNL}"
            )
            lines.append(f"    {row.get('reason')}")

    kept = scan.get("published_only") or []
    if kept:
        lines.append("")
        lines.append(f"published paper history kept ({len(kept)})")
        for row in kept:
            bits = [row.get("paper_outcome") or "published", row.get("published_paper_pnl") or ""]
            lines.append(
                f"  {row.get('ticker')}  {' '.join(b for b in bits if b)}  "
                f"[{row.get('source')}]"
            )

    lines.extend(
        [
            "",
            "Python names owed roles. It never marks one served, never writes a desk",
            "thread line, and never invents a win, a lose or a pnl.",
            "A role clears its own line only after it really ran:",
            '  python -c "from golf_offshoot.learning_lane_15m.learn import '
            "mark_roles_served; mark_roles_served(['digestor'], by='digestor', "
            "note='posted the SOURCE honesty digest')\"",
        ]
    )
    return "\n".join(lines)


# --------------------------------------------------------------- manifest block


def learning_status_block(state: dict[str, Any] | None = None) -> dict[str, Any]:
    """Wake status for the published manifest. Strings only, no cash-shaped fields."""
    payload = state if state is not None else load_wake_state()
    if not payload:
        return {
            "status": "not yet available",
            "headline": (
                "The learning wake has not been recorded on this tree yet. "
                "No crew work is claimed either way."
            ),
            "updated_at": "",
            "updated_text": "",
            "rows": [],
            "roles_owed": [],
            "lineage": LINEAGE_A,
            "missing_paper_joins": [],
            "pending_windows": [],
            "published_history": [],
            "notes": list(CONTRACT),
        }
    scan = payload.get("scan") or {}
    owed = payload.get("roles_owed") or []
    missing = scan.get("paper_join_missing") or []
    kept = scan.get("published_only") or []
    heartbeat = payload.get("heartbeat") or {}
    rows = [
        {"label": "Roles owed", "value": _as_str(len(owed))},
        {"label": "Settled windows seen on this tree", "value": _as_str(len(scan.get("settled") or {}))},
        {"label": "Paper books on this tree", "value": _as_str(len(scan.get("fills") or {}))},
        {"label": "Pending windows on this tree", "value": _as_str(len(scan.get("pending") or []))},
        {
            "label": "Official result, paper book not on this tree",
            "value": _as_str(len(missing)),
            "note": "; ".join(
                f"{row.get('ticker')} — {row.get('state')}, {NO_PAPER_PNL}" for row in missing
            )
            or "none",
        },
        {
            "label": "Published paper history kept",
            "value": _as_str(len(kept)),
            "note": "; ".join(
                f"{row.get('ticker')} {row.get('paper_outcome')} "
                f"{row.get('published_paper_pnl')}".strip()
                for row in kept
            )
            or "none",
        },
    ]
    headline = (
        f"Crew work is owed: {', '.join(_as_str(e.get('role')) for e in owed)}."
        if owed
        else (heartbeat.get("note") or HEARTBEAT_NOTE)
    )
    return {
        "status": "crew work owed" if owed else "no crew work owed",
        "headline": headline,
        "updated_at": _as_str(payload.get("updated_at")),
        "updated_text": format_eastern(payload.get("updated_at"), with_seconds=True),
        "rows": rows,
        "roles_owed": [
            {
                "label": _as_str(entry.get("role")),
                "value": f"owed {entry.get('age_text')}",
                "note": "; ".join(entry.get("reasons") or []),
            }
            for entry in owed
        ],
        "lab": (payload.get("lab_gate") or {}).get("why", ""),
        # Which paper book this block counts. The published manifest carries lineage B
        # figures elsewhere; a later reader must not reconcile one against the other.
        "lineage": LINEAGE_A,
        "missing_paper_joins": [
            {
                "label": _as_str(row.get("ticker")),
                "value": MISSING_JOIN_BANNER,
                "note": _as_str(row.get("reason")),
                "state": _as_str(row.get("state")),
                "official_result": _as_str(row.get("official_result")),
                "paper_pnl": NO_PAPER_PNL,
            }
            for row in missing
        ],
        "pending_windows": [
            {
                "label": _as_str(row.get("ticker")),
                "value": SETTLE_PENDING,
                "note": _as_str(row.get("reason")),
                "kind": _as_str(row.get("kind")),
            }
            for row in (scan.get("pending") or [])
        ],
        "published_history": [
            {
                "label": _as_str(row.get("ticker")),
                "value": _as_str(row.get("paper_outcome")),
                "note": _as_str(row.get("note")),
                "published_paper_pnl": _as_str(row.get("published_paper_pnl")),
                "lineage": LINEAGE_B,
            }
            for row in kept
        ],
        "notes": [*CONTRACT, NEVER_SUMMED],
    }
