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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

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
REL_PNG = Path("docs") / "observability-hub" / "data" / "charts" / "learning_lane_15m" / "paper_window_strip.png"

#: Protocol order for the learning tick. Market events name the figures
#: generator, not the human digestor. Human digestor is owed only when the
#: caveats file itself needs a turn. Lab is not in the default list.
ROLE_ORDER = ("digest-figures", "learning-card", "operator", "systems", "validator")
ILLUSTRATOR_ROLE = "illustrator"
DIGESTOR_ROLE = "digestor"
LAB_ROLE = "lab"
OPERATOR_ROLE = "operator"
CRITIC_INVARIANTS_ROLE = "critic-invariants"
SOFTEN_CRITIC_ROLE = "soften-critic"
LEARNING_CARD_ROLE = "learning-card"

#: Display order for the desk and the tick, protocol order first.
_ROLE_RANK = (
    "digest-figures",
    LEARNING_CARD_ROLE,
    DIGESTOR_ROLE,
    OPERATOR_ROLE,
    "systems",
    "validator",
    ILLUSTRATOR_ROLE,
    CRITIC_INVARIANTS_ROLE,
    SOFTEN_CRITIC_ROLE,
    LAB_ROLE,
)

#: What a routine market event names. All three are clerical: the runner
#: clears them on the next pass, so naming them on every settle costs nothing
#: and keeps the published surface current.
ROUTINE_ROLES = ("digest-figures", "systems", "validator")

EVENT_NEW_SETTLE = "new_settle"
EVENT_NEW_FILL = "new_fill"
EVENT_PENDING_CLEARED = "pending_cleared"
EVENT_BOARD_STALE = "board_stale"
EVENT_LEARNING_CARD_STALE = "learning_card_stale"

from golf_offshoot.learning_lane_15m.triggers import (  # noqa: E402
    EVENT_ARTIFACT_UNREVIEWED,
    EVENT_BOOK_OPEN_NO_JOIN,
    EVENT_CRITIC_FINDINGS_FAILING,
    EVENT_DETECTOR_BLIND,
    EVENT_FALSIFIER_FIRED,
    EVENT_LAB_PROPOSED,
    EVENT_PAPER_JOIN_MISSING_GREW,
    EVENT_PARK_AGED,
    EVENT_RULE_REACHED_N,
    EVENT_SETTLE_CONTRADICTS_BOOK,
    EVENT_UNRECORDED_COST,
    EVENT_WINDOW_SEQUENCE_GAP,
)
from golf_offshoot.learning_lane_15m.triggers import (  # noqa: E402
    EVENT_DIGEST_CONTRADICTS_LEDGER,
    EVENT_PUBLISHED_FALSEHOOD,
    EVENT_VALIDATOR_REPORT_FAILING,
)

#: Human digestor is owed when the generated figures **cannot express what
#: changed**. Enumerated here and in PROTOCOL.md. Not zero, not every settle —
#: the every-settle trigger is deliberately not restored.
DIGESTOR_TRIGGERS = frozenset(
    {
        EVENT_PAPER_JOIN_MISSING_GREW,
        EVENT_BOOK_OPEN_NO_JOIN,
        EVENT_WINDOW_SEQUENCE_GAP,
        EVENT_SETTLE_CONTRADICTS_BOOK,
        EVENT_UNRECORDED_COST,
        # The figure is wrong *after* the generator had its pass, so the figures
        # role cannot express what changed by running again.
        EVENT_DIGEST_CONTRADICTS_LEDGER,
    }
)

#: Operator is judicial. A normally-settled window owes it nothing. Enumerated
#: here and in PROTOCOL.md. If an exception class is unclear, it stays on this
#: list and Operator says why — it is never dropped to shorten the owed list.
OPERATOR_TRIGGERS = frozenset(
    {
        EVENT_PARK_AGED,
        EVENT_SETTLE_CONTRADICTS_BOOK,
        EVENT_PAPER_JOIN_MISSING_GREW,
        EVENT_WINDOW_SEQUENCE_GAP,
        EVENT_FALSIFIER_FIRED,
        EVENT_RULE_REACHED_N,
        EVENT_LAB_PROPOSED,
        # A failing method check may not be retired by the machine that found
        # it. The failing checks are properties of the bar, and the bar is
        # Operator's.
        EVENT_CRITIC_FINDINGS_FAILING,
        # A detector that cannot see is not a detector that saw nothing.
        EVENT_DETECTOR_BLIND,
        # A clerical artifact reporting its own subject matter as failing. Being
        # served on proof retires the run, never the finding.
        EVENT_VALIDATOR_REPORT_FAILING,
        EVENT_PUBLISHED_FALSEHOOD,
        EVENT_DIGEST_CONTRADICTS_LEDGER,
    }
)

#: Repo-side. Market data is not the only thing that changes.
CRITIC_TRIGGERS = frozenset({EVENT_ARTIFACT_UNREVIEWED})

#: Kinds that are not about the market. Naming the figures roles on these is
#: the same over-firing the severity split exists to stop: a failing method
#: check does not need the digest regenerated.
NON_MARKET_KINDS = frozenset(
    {
        EVENT_CRITIC_FINDINGS_FAILING,
        EVENT_DETECTOR_BLIND,
        EVENT_VALIDATOR_REPORT_FAILING,
        EVENT_PUBLISHED_FALSEHOOD,
        EVENT_DIGEST_CONTRADICTS_LEDGER,
        EVENT_LEARNING_CARD_STALE,
    }
)

#: Pre-split leftover reasons. A routine settle no longer names digestor or
#: operator; lines that still carry these prefixes are the board lying.
RETIRED_JUDICIAL_PREFIXES = ("new_settle ", "new_fill ", "pending_cleared ")

#: The board may trail the live journal by the current open window. Two or more
#: windows ahead of the PNG is a lag — Illustrator is owed, not optional.
BOARD_LAG_WINDOWS = 1

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
    "crew_tick is a doorbell. The runner may write it. The runner is not CoS.",
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


# ----------------------------------------------------------------- board lag


_MONTHS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def _parse_window_close_stamp(text: str) -> float | None:
    raw = str(text or "").strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H-%M-%SZ"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            continue
    parsed = _parse_iso(raw)
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _ticker_close_epoch(ticker: str) -> float | None:
    """Close clock from a KXBTC15M-YYMONDDHHMM[-MM] ticker. ET, not invented."""
    try:
        from golf_offshoot.data_feeds.kalshi_15m import parse_market_ticker

        token = parse_market_ticker(ticker)["window_token"]
    except Exception:
        return None
    if len(token) < 11:
        return None
    mon = _MONTHS.get(token[2:5])
    if mon is None:
        return None
    try:
        from zoneinfo import ZoneInfo

        close = datetime(
            2000 + int(token[:2]),
            mon,
            int(token[5:7]),
            int(token[7:9]),
            int(token[9:11]),
            tzinfo=ZoneInfo("America/New_York"),
        )
    except (ValueError, OSError):
        return None
    return close.timestamp()


def _window_close_epoch(window_id: str, ticker: str) -> float | None:
    parts = str(window_id or "").split("__")
    if len(parts) >= 3:
        stamp = _parse_window_close_stamp(parts[-1])
        if stamp is not None:
            return stamp
    return _ticker_close_epoch(ticker)


def _evidence_windows(scan: dict[str, Any]) -> list[dict[str, str]]:
    """Every journal/settlement/pending window the board should be able to name."""
    seen: dict[str, dict[str, str]] = {}
    for ticker, row in (scan.get("settled") or {}).items():
        seen[ticker] = {
            "ticker": ticker,
            "window_id": _as_str(row.get("window_id")),
            "kind": "settled",
        }
    for row in scan.get("pending") or []:
        ticker = _as_str(row.get("ticker")) or _as_str(row.get("window_id"))
        if ticker and ticker not in seen:
            seen[ticker] = {
                "ticker": ticker,
                "window_id": _as_str(row.get("window_id")),
                "kind": "pending",
            }
    for window in _journal_rows():
        ticker = _as_str(window.get("ticker")).strip()
        if not ticker or ticker in seen:
            continue
        seen[ticker] = {
            "ticker": ticker,
            "window_id": _as_str(window.get("window_id")),
            "kind": "journal",
        }
    return list(seen.values())


def board_lag(scan: dict[str, Any] | None = None) -> dict[str, Any]:
    """How many live windows closed after the PNG was written.

    One window of trail is the open window and is allowed. Two or more means
    the board has fallen behind the journal/settlements and Illustrator is owed.
    File mtimes on the JSON are ignored — PaperWatch rewrites them every cycle.
    """
    evidence = scan if scan is not None else scan_learning_evidence()
    png = repo_root() / REL_PNG
    exists = png.is_file()
    png_ts = float(png.stat().st_mtime) if exists else None
    behind: list[str] = []
    unknown = 0
    for row in _evidence_windows(evidence):
        close = _window_close_epoch(row.get("window_id", ""), row.get("ticker", ""))
        if close is None:
            unknown += 1
            continue
        if png_ts is None or close > png_ts:
            behind.append(row["ticker"])
    lag = len(behind)
    stale = lag > BOARD_LAG_WINDOWS
    if not exists:
        note = (
            f"no PNG on disk; {lag} window(s) of journal/settlement evidence"
            + ("; illustrator is owed" if stale else "")
        )
    elif stale:
        note = (
            f"PNG lags live journal/settlements by {lag} windows "
            f"(more than {BOARD_LAG_WINDOWS}); illustrator is owed"
        )
    else:
        note = f"PNG is current ({lag} window(s) ahead of the board; one is allowed)"
    return {
        "png_exists": exists,
        "png_path": REL_PNG.as_posix(),
        "lag_windows": lag,
        "lag_tickers": behind,
        "unknown_close": unknown,
        "stale": stale,
        "note": note,
    }


def _board_stale_event(lag: dict[str, Any], *, at: str) -> dict[str, Any]:
    tickers = lag.get("lag_tickers") or []
    named = ", ".join(tickers[:4])
    if len(tickers) > 4:
        named += f" (+{len(tickers) - 4} more)"
    return {
        "kind": EVENT_BOARD_STALE,
        "ticker": tickers[0] if tickers else "",
        "window_id": "",
        "at": at,
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "detail": lag.get("note") or "PNG lags the live journal/settlements",
        "lag_windows": lag.get("lag_windows"),
        "lag_tickers": tickers,
        "roles_owed": [ILLUSTRATOR_ROLE],
        "roles_owed_is_a_request": True,
    }


# ----------------------------------------------------------------------- events


def roles_owed_for(
    kind: str,
    *,
    honesty_gate_passed: bool = False,
    operator_residual_posted: bool = False,
    also_owes: Sequence[str] = (),
) -> list[str]:
    """Which roles this event kind owes a turn. Severity split, enumerated.

    A routine settle names the three clerical roles and nobody else. Judicial
    roles are named only by their enumerated exception kinds, so the owed list
    is something a human can still read after ninety-six windows in a day.

    Lab is added only when both gates are explicitly true.
    """
    kind = str(kind or "").strip()
    if kind == EVENT_BOARD_STALE:
        return [ILLUSTRATOR_ROLE]
    if kind == EVENT_LEARNING_CARD_STALE:
        return [LEARNING_CARD_ROLE]
    if kind in CRITIC_TRIGGERS:
        roles = {CRITIC_INVARIANTS_ROLE, SOFTEN_CRITIC_ROLE}
        roles.update(r for r in also_owes if r)
        return sorted(roles, key=_role_rank)
    roles: set[str] = set() if kind in NON_MARKET_KINDS else set(ROUTINE_ROLES)
    if kind in DIGESTOR_TRIGGERS:
        roles.add(DIGESTOR_ROLE)
    if kind in OPERATOR_TRIGGERS:
        roles.add(OPERATOR_ROLE)
    roles.update(r for r in also_owes if r)
    if honesty_gate_passed and operator_residual_posted:
        roles.add(LAB_ROLE)
    return sorted(roles, key=_role_rank)


def _role_rank(role: str) -> int:
    return _ROLE_RANK.index(role) if role in _ROLE_RANK else 99


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


def exception_events(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """The enumerated exceptions that owe a judicial role.

    Each detector reads files. One that cannot read what it needs raises
    nothing rather than guessing, and a detector raising nothing is not
    evidence that the condition is absent — it is evidence it was not seen.
    """
    from golf_offshoot.learning_lane_15m import triggers as T
    from golf_offshoot.learning_lane_15m.paths import has_15m_root_override

    def _as(name: str, fn: Callable[[], Any]) -> Callable[[], Any]:
        fn.__name__ = name
        return fn

    detectors: list[Any] = [
        _as("paper_join_missing_grew", lambda: T.paper_join_missing_grew(previous, current)),
        _as("new_book_open_no_join", lambda: T.new_book_open_no_join(previous, current)),
        _as("window_sequence_gaps", lambda: T.window_sequence_gaps(previous, current)),
        _as("settles_contradicting_their_book", lambda: T.settles_contradicting_their_book(previous, current)),
    ]
    # Detectors below read the *repo*, not the lane data directory. Under a
    # scratch root the repo is not the tree under test, so reading it would
    # leak live findings into a sandbox — the same leak that let a test rewrite
    # the published digest. This is a scope limit, not a blind detector.
    if not has_15m_root_override():
        detectors.extend(
            [
                T.unrecorded_cost,
                T.park_aged,
                T.falsifier_fired,
                # Negative results from the clerical whitelist. Each of these
                # roles is served on proof, so an artifact reporting its own
                # subject matter as failing would otherwise clear the role that
                # wrote it and owe nobody. ``test_serve_on_proof.py`` asserts
                # one of these exists for every whitelisted role.
                _as("critic_findings_failing", lambda: T.critic_findings_failing()),
                T.validator_report_failing,
                _as("published_falsehood", lambda: T.published_falsehood(current)),
                _as("digest_contradicts_ledger", lambda: T.digest_contradicts_ledger(previous)),
                T.board_render_refused,
                _as("rule_reached_n", lambda: T.rule_reached_n(current)),
            ]
        )

    events: list[dict[str, Any]] = []
    for detector in detectors:
        try:
            events.extend(detector() or [])
        except Exception as exc:  # noqa: BLE001 — a blind detector is not a pass
            events.append(_blind_detector_event(detector, exc))
    return events


def _blind_detector_event(detector: Any, exc: BaseException) -> dict[str, Any]:
    name = getattr(detector, "__name__", "") or "an exception detector"
    return {
        "kind": EVENT_DETECTOR_BLIND,
        "ticker": name,
        "window_id": "",
        "detail": (
            f"{name} failed to read its evidence ({type(exc).__name__}: {exc}); "
            "a detector that cannot see is not a detector that saw nothing"
        ),
    }


def _learning_card_input_events() -> list[dict[str, Any]]:
    """Owe learning-card when its inputs moved. Raises if the registry is unreadable."""
    from golf_offshoot.learning_lane_15m.learning_card import stale_events

    return stale_events()


def guarded_events(name: str, source: Callable[[], Any]) -> list[dict[str, Any]]:
    """Run an event source; a raise becomes ``detector_blind``, never silence.

    ``exception_events`` has wrapped its own detectors since #148, but
    ``diff_scans``, ``repo_events`` and ``board_lag`` were called bare. Any of
    the three raising would have propagated out of the tick — and a tick that
    does not finish writes no ``roles_owed`` at all, so every clerical role on
    the whitelist would go un-owed and nothing would say why.
    ``test_serve_on_proof.py`` asserts this over each whitelisted role's own
    named source.
    """
    try:
        return list(source() or [])
    except Exception as exc:  # noqa: BLE001 — a blind source is not a quiet one
        event = _blind_detector_event(source, exc)
        event["ticker"] = name
        event["detail"] = (
            f"{name} failed to read its evidence ({type(exc).__name__}: {exc}); "
            "a detector that cannot see is not a detector that saw nothing"
        )
        return [event]


def repo_events() -> list[dict[str, Any]]:
    """Repo-side event class: an artifact changed and no Critic finding covers it.

    Market data is not the only thing that changes. A bar being drafted, a rule
    reaching its n, an invariant being added, a park being written — the Critic
    is owed on those and no market event kind covers them.

    The import is inside the ``try`` on purpose. It used to sit outside it, so
    an ImportError propagated instead of being handled — and the bare
    ``return []`` below it meant any runtime fault reported *no events*,
    silently leaving the Critic un-owed. That is the same silent-pass the
    module exists to prevent, so a failure here raises instead.
    """
    from golf_offshoot.learning_lane_15m.paths import has_15m_root_override

    if has_15m_root_override():
        # Scratch root: the live repo is not the tree under test.
        return []
    try:
        from golf_offshoot.learning_lane_15m.critic import unreviewed

        rows = unreviewed()
    except Exception as exc:  # noqa: BLE001 — a suite that cannot run is a failure
        return [_blind_detector_event(repo_events, exc)]
    return [
        {
            "kind": EVENT_ARTIFACT_UNREVIEWED,
            "ticker": row.get("id") or "",
            "window_id": "",
            "detail": (
                f"{row.get('path')} is at sha256 {str(row.get('sha256'))[:12]}… and no "
                "Critic finding exists for that hash"
            ),
            "also_owes": tuple(row.get("also_owes") or ()),
        }
        for row in rows
    ]


def _event_label(event: dict[str, Any]) -> str:
    who = _as_str(event.get("ticker")) or _as_str(event.get("window_id")) or "window"
    return f"{event.get('kind')} {who}"


def rekey_leftover_owed(
    existing: Iterable[dict[str, Any]],
    *,
    drop_disclosed_critic_failing: bool = False,
) -> list[dict[str, Any]]:
    """Drop pre-split every-settle reasons from judicial lines.

    Human digestor is not owed for ``new_settle`` / ``new_fill`` /
    ``pending_cleared``. Operator is not owed for those either. After this
    pass those roles stay owed only on the exception lists already enumerated
    in ``triggers.py`` and PROTOCOL.md. A leftover ``critic_findings_failing``
    for a failing set the bar already names is the same class of lie: Operator
    has already written the reason, so the line is not a request for work.

    Does not restore every-settle triggers. Does not drop a live exception
    class to shorten the list.
    """
    out: list[dict[str, Any]] = []
    for entry in existing:
        role = _as_str(entry.get("role"))
        if role not in {DIGESTOR_ROLE, OPERATOR_ROLE}:
            out.append(dict(entry))
            continue
        kept: list[Any] = []
        for reason in entry.get("reasons") or []:
            text = str(reason)
            if any(text.startswith(prefix) for prefix in RETIRED_JUDICIAL_PREFIXES):
                continue
            if (
                drop_disclosed_critic_failing
                and role == OPERATOR_ROLE
                and text.startswith("critic_findings_failing")
            ):
                continue
            kept.append(reason)
        if not kept:
            continue
        row = dict(entry)
        row["reasons"] = kept
        out.append(row)
    return out


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
    for role in sorted(order, key=_role_rank):
        entry = by_role[role]
        age = _age_s(_as_str(entry.get("owed_since")) or at, at_dt)
        entry["age_s"] = int(age)
        entry["age_text"] = _age_text(age)
        entry["stale"] = age >= STALE_AFTER_S
        entry["served_at"] = None
        # Judicial silence as a number rather than a vibe: how many ticks this
        # role has been named and has not answered.
        entry["ticks_unanswered"] = int(entry.get("ticks_unanswered") or 0) + 1
        out.append(entry)
    return out


# ------------------------------------------------------------------- lab gate


def honesty_gate_from_desk(
    path: Path | None = None,
    *,
    scan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read the honesty stamp, but derive every box that can be derived.

    Never write it, never infer a PASS. No stamp on the desk is not a pass.

    Three boxes are computed from files and the **derived verdict wins** — desk
    prose can shut one, never open one. The remaining box needs judgment, so it
    must carry evidence (PIDs, hashes, timestamps); ``**PASS**`` alone no longer
    opens it. A derived box missing from the desk is still evaluated, so
    deleting a row cannot open the gate either.

    The parser was not widened to accept more phrasings. It was narrowed.
    """
    from golf_offshoot.learning_lane_15m.honesty import (
        DERIVED_BOXES,
        classify_box,
        derive_boxes,
        has_evidence,
    )

    dest = path or desk_path()
    derived = derive_boxes(scan)
    try:
        text = dest.read_text(encoding="utf-8")
    except OSError:
        return {
            "stamp_found": False,
            "passed": False,
            "boxes": [
                {
                    "box": key,
                    "state": "PASS" if derived[key]["ok"] else "FAIL",
                    "source": "derived",
                    "note": derived[key]["note"],
                }
                for key in DERIVED_BOXES
            ],
            "note": "no desk file to read the Chief of Staff honesty stamp from",
        }
    boxes: list[dict[str, Any]] = []
    seen_derived: set[str] = set()
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
        typed = "FAIL" if "**FAIL**" in cells[1] else ("PASS" if "**PASS**" in cells[1] else "")
        kind = classify_box(cells[0])
        row: dict[str, Any] = {"box": cells[0], "typed": typed or "unstamped"}
        if kind in derived:
            seen_derived.add(kind)
            machine = derived[kind]
            # Fail-closed in both directions: the file decides PASS, the desk
            # may still shut it.
            state = "PASS" if machine["ok"] and typed != "FAIL" else "FAIL"
            row.update(
                {
                    "state": state,
                    "source": "derived",
                    "note": machine["note"],
                    "evidence": machine.get("evidence"),
                }
            )
        else:
            evidenced = has_evidence(cells[1])
            row.update(
                {
                    "state": "PASS" if (typed == "PASS" and evidenced) else "FAIL",
                    "source": "judgment",
                    "has_evidence": evidenced,
                    "note": (
                        "stamped PASS with evidence attached"
                        if typed == "PASS" and evidenced
                        else (
                            "stamped PASS with no evidence — a stamp with no PIDs, "
                            "hashes or timestamps does not open the gate"
                            if typed == "PASS"
                            else f"not stamped PASS ({typed or 'unstamped'})"
                        )
                    ),
                }
            )
        boxes.append(row)

    for key in DERIVED_BOXES:
        if key in seen_derived:
            continue
        machine = derived[key]
        boxes.append(
            {
                "box": f"{key} (not on the desk)",
                "typed": "absent",
                "state": "PASS" if machine["ok"] else "FAIL",
                "source": "derived",
                "note": machine["note"],
                "evidence": machine.get("evidence"),
            }
        )

    failing = [b["box"] for b in boxes if b["state"] != "PASS"]
    stamped = any(b.get("typed") not in {None, "", "absent"} for b in boxes)
    return {
        "stamp_found": stamped,
        "passed": bool(boxes) and not failing,
        "derived_boxes": list(DERIVED_BOXES),
        "boxes": boxes,
        "note": (
            "all boxes pass; derived boxes came off files, judgment boxes carry evidence"
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
    crew_hub_ok: bool | None = None,
) -> dict[str, Any]:
    """One wake tick: scan, diff against stored state, persist. Never marks served."""
    at_dt = now()
    at = isoformat_now(at_dt)
    scan = scan_learning_evidence(manifest_path=manifest_path)
    state = load_wake_state()
    previous = (state or {}).get("scan")

    gate = honesty_gate_from_desk(desk, scan=scan)
    passed = gate["passed"] if honesty_gate_passed is None else bool(honesty_gate_passed)

    events = guarded_events("diff_scans", lambda: diff_scans(previous, scan))
    events.extend(guarded_events("exception_events", lambda: exception_events(previous, scan)))
    events.extend(guarded_events("repo_events", repo_events))
    events.extend(guarded_events("learning_card_inputs", _learning_card_input_events))
    try:
        lag = board_lag(scan)
    except Exception as exc:  # noqa: BLE001 — a blind board is not a current one
        events.append(_blind_detector_event(board_lag, exc) | {"ticker": "board_lag"})
        lag = {"stale": False, "detail": f"board_lag failed: {exc}"}
    already_owed = {
        _as_str(entry.get("role")).lower()
        for entry in ((state or {}).get("roles_owed") or [])
    }
    if lag.get("stale") and ILLUSTRATOR_ROLE not in already_owed:
        events.append(_board_stale_event(lag, at=at))
    for event in events:
        event["at"] = at
        event["lane"] = LANE_15M
        event["series"] = PRIMARY_SERIES
        event["roles_owed"] = roles_owed_for(
            str(event.get("kind") or ""),
            honesty_gate_passed=passed,
            operator_residual_posted=operator_residual_posted,
            also_owes=event.pop("also_owes", ()) or (),
        )
        event["roles_owed_is_a_request"] = True

    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()

    drop_disclosed = False
    try:
        from golf_offshoot.learning_lane_15m.critic import (
            bar_names_failing_check,
            load_findings,
        )

        findings = load_findings()
        failing = [str(f) for f in (findings or {}).get("failing") or []]
        drop_disclosed = (not failing) or all(
            bar_names_failing_check(check) for check in failing
        )
    except Exception:  # noqa: BLE001 — re-key still drops the retired market reasons
        drop_disclosed = False

    owed = _merge_roles_owed(
        rekey_leftover_owed(
            (state or {}).get("roles_owed") or [],
            drop_disclosed_critic_failing=drop_disclosed,
        ),
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
        "board": lag,
        "lab_gate": _lab_gate_block(gate, operator_residual_posted=operator_residual_posted),
    }
    new_state["invariants"] = _run_invariants_block(new_state, watch_status)
    if state and isinstance(state.get("crew_tick"), dict):
        new_state["crew_tick"] = {
            "last_cos_at": state["crew_tick"].get("last_cos_at") or "",
            "last_cos_commit": state["crew_tick"].get("last_cos_commit") or "",
            "handled_reason_ids": list(state["crew_tick"].get("handled_reason_ids") or []),
        }
    from golf_offshoot.learning_lane_15m.crew_tick import attach_crew_tick

    desk_text = None
    if desk is not None:
        try:
            desk_text = Path(desk).read_text(encoding="utf-8")
        except OSError:
            desk_text = ""
    attach_crew_tick(
        new_state,
        desk_text=desk_text,
        previous_watch=(state or {}).get("watch") if state else None,
        hub_ok=crew_hub_ok,
    )
    save_wake_state(new_state)
    return new_state


def _run_invariants_block(
    state: dict[str, Any],
    watch_status: dict[str, Any],
) -> dict[str, Any]:
    """Run the invariant suite and keep a summary on the tick.

    Full evidence goes to ``latest/invariants.json``. The wake carries the
    verdicts so a failure is on the tick even if nobody opens the report. A
    suite that cannot run is itself a failure — never a silent pass.
    """
    try:
        from golf_offshoot.learning_lane_15m.invariants import (
            run_invariants,
            write_invariants,
        )

        report = run_invariants(state=state, watch_status=watch_status)
        write_invariants(report)
    except Exception as exc:  # noqa: BLE001 — the suite failing is a finding
        return {
            "passed": False,
            "failing": ["invariant_suite"],
            "checks": [
                {
                    "id": "invariant_suite",
                    "title": "invariant suite runs",
                    "state": "FAIL",
                    "detail": f"suite raised {type(exc).__name__}: {exc}",
                }
            ],
        }
    return {
        "ran_at": report.get("ran_at"),
        "passed": report.get("passed"),
        "failing": report.get("failing"),
        "report": str(_invariants_report_path()),
        "checks": [
            {
                "id": check.get("id"),
                "title": check.get("title"),
                "state": check.get("state"),
                "detail": check.get("detail"),
            }
            for check in report.get("checks") or []
        ],
    }


def _invariants_report_path() -> Path:
    from golf_offshoot.learning_lane_15m.invariants import invariants_path

    return invariants_path()


def refresh_invariants(
    *,
    watch_status: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Re-run the suite against the state as it stands and store the verdicts.

    Called after the clerical runner has had its pass, so a digest the runner
    just regenerated is not reported stale. Names no role owed and marks none
    served — this only re-reads.
    """
    state = load_wake_state()
    if state is None:
        return None
    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()
    block = _run_invariants_block(state, watch_status)
    state["invariants"] = block
    save_wake_state(state)
    return block


def mark_roles_served(
    roles: Sequence[str],
    *,
    by: str = "",
    note: str = "",
    served_kind: str = "human",
) -> dict[str, Any] | None:
    """Clear owed roles. Only a role that really ran calls this; the loop never does.

    ``served_kind`` is permanent provenance: ``human`` or ``auto``. The runner
    may pass ``auto`` only after the artifact it was asked to produce actually
    changed on disk.
    """
    kind = str(served_kind or "human").strip().lower()
    if kind not in {"human", "auto"}:
        raise ValueError("served_kind must be 'human' or 'auto'")
    state = load_wake_state()
    if state is None:
        return None
    wanted = {str(role).strip().lower() for role in roles if str(role).strip()}
    wanted -= {"chief-of-staff", "cos"}
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
                    "served_kind": kind,
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
    from golf_offshoot.learning_lane_15m.critic import format_critic, load_findings
    from golf_offshoot.learning_lane_15m.invariants import format_invariants

    lines.extend(format_invariants(state.get("invariants")))
    lines.append("")
    from golf_offshoot.learning_lane_15m.crew_tick import format_crew_tick

    lines.extend(format_crew_tick(state.get("crew_tick")))
    lines.append("")
    lines.extend(format_critic(load_findings()))

    lines.append("")
    owed = state.get("roles_owed") or []
    if owed:
        lines.append(f"roles owed ({len(owed)}) — a request for a turn, not a completion")
        for entry in owed:
            flag = "  STALE" if entry.get("stale") else ""
            silent = int(entry.get("ticks_unanswered") or 0)
            # Judicial silence is a count, not an impression.
            quiet = f"  silent {silent} ticks" if silent > 1 else ""
            lines.append(
                f"  {_as_str(entry.get('role')):<10} owed {entry.get('age_text')}{quiet}{flag}"
            )
            for reason in entry.get("reasons") or []:
                lines.append(f"    for: {reason}")
    else:
        lines.append("roles owed: none")
    gate = state.get("lab_gate") or {}
    lines.append(
        f"  {LAB_ROLE:<10} {'owed' if gate.get('lab_owed') else 'NOT owed'} — {gate.get('why')}"
    )
    board = state.get("board") or {}
    if board:
        flag = "owed" if any(_as_str(e.get("role")) == ILLUSTRATOR_ROLE for e in owed) else (
            "owed" if board.get("stale") else "NOT owed"
        )
        lines.append(f"  {ILLUSTRATOR_ROLE:<10} {flag} — {board.get('note')}")

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
            "mark_roles_served; mark_roles_served(['digest-figures'], by='digest-figures', "
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
        {
            "label": "Board lag",
            "value": _as_str((payload.get("board") or {}).get("lag_windows") or 0),
            "note": _as_str((payload.get("board") or {}).get("note")),
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
