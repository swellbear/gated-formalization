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
from golf_offshoot.learning_lane_15m.settle import (
    SETTLE_PENDING,
    SETTLE_SETTLED,
    event_ticker_from_book_id,
)
from golf_offshoot.localtime import isoformat_now
from golf_offshoot.repo_paths import repo_root

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

# Rows recomputed from disk every tick, so a published copy of one of these labels
# is stale by construction and the rebuilt value wins. Every other label keeps the
# normal merge, which is what protects the published paper_win.
LINEAGE_A_LEDGER_ROWS = (
    ("Lineage A · open paper books on this tree", "open_books"),
    ("Lineage A · settled paper books on this tree", "settled_books"),
    ("Lineage A · ledger entries on this tree", "ledger_entries"),
)
LIVE_WAKE_LABELS = frozenset(
    {
        "Learning wake",
        "Crew roles owed",
        "Wake checked",
        "Official result, paper book not on this tree",
        "Published paper history kept",
        *(label for label, _ in LINEAGE_A_LEDGER_ROWS),
    }
)

WAKE_JOIN_NOTE = (
    "A window can carry an official Kalshi result while its paper book is not on "
    "this tree. That window is reported as a missing paper join carrying no paper "
    "pnl — never as a paper win, a paper loss, or a pending window."
)

# Lineage B publishes its live fill as this label pair. Read so a fill the published
# lineage names can be checked against the books that actually exist on this tree.
LIVE_FILL_LABEL = "Live paper fill"
LIVE_FILL_STATUS_LABEL = "Live paper fill status"

LINEAGE_B_LEDGER_HEADLINE = (
    "Lineage B — published Pages export. Paper ticket counts and labeled paper "
    "settle_win strings, from the tree that wrote them. Rows labelled 'Lineage A' "
    "are this tree's own paper book, counted separately."
)
NEVER_SUMMED_NOTE = (
    "Lineage A and lineage B are two separate paper books over the same series. "
    "Their counts and pnl figures are never added together."
)

# settle.counts mixes this tree's official settle files with lineage B's published
# paper figures. Prefixed so nobody reads one row as a numerator over the other.
LINEAGE_B_PREFIX = "Lineage B · "
LINEAGE_B_COUNT_LABELS = (
    "paper_win",
    "paper settle_win pnl",
    "paper observation after settle",
)
SETTLED_WINDOWS_NOTE = (
    "Official Kalshi settle files on this tree. Not lineage B's book, and not a "
    "denominator for the lineage B paper_win below it."
)


def _base_label(label: str) -> str:
    """A count label with its lineage prefix stripped, for matching across exports."""
    return label[len(LINEAGE_B_PREFIX) :] if label.startswith(LINEAGE_B_PREFIX) else label


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


def _settle_count_value(lane: dict[str, Any] | None, label: str) -> int:
    if not lane:
        return 0
    for row in ((lane.get("settle") or {}).get("counts") or []):
        if isinstance(row, dict) and _base_label(_as_str(row.get("label"))) == label:
            try:
                return int(str(row.get("value") or "0"))
            except ValueError:
                return 0
    return 0


def _keep_published_15m(
    published: dict[str, Any] | None,
    rebuilt: dict[str, Any],
) -> bool:
    """Keep Pages history when a local journal would drop published paper settles."""
    if not published or published.get("lane_id") != LANE_15M:
        return False
    if _settle_count_value(rebuilt, "Settled windows") < _settle_count_value(
        published, "Settled windows"
    ):
        return True
    if _settle_count_value(rebuilt, "paper_win") < _settle_count_value(published, "paper_win"):
        return True
    return False


def _residual_is_pending(row: dict[str, Any]) -> bool:
    value = _as_str(row.get("value")).upper()
    return "PENDING" in value or value in {"", SETTLE_PENDING.upper()}


def _merge_residuals(
    published: list[Any] | None,
    rebuilt: list[Any] | None,
) -> list[dict[str, Any]]:
    by_label: dict[str, dict[str, Any]] = {}
    for row in list(published or []) + list(rebuilt or []):
        if not isinstance(row, dict):
            continue
        key = _as_str(row.get("label"))
        if not key:
            continue
        prev = by_label.get(key)
        if prev is None or (_residual_is_pending(prev) and not _residual_is_pending(row)):
            by_label[key] = {
                "label": key,
                "value": _as_str(row.get("value")),
                **({"note": _as_str(row.get("note"))} if row.get("note") else {}),
            }
    return list(by_label.values())


def _refresh_live_rows(rows: list[Any] | None, rebuilt_rows: list[Any] | None) -> list[Any]:
    """Swap a stale published wake row for the one this run just read off disk."""
    fresh = {
        _as_str(row.get("label")): row
        for row in rebuilt_rows or []
        if isinstance(row, dict) and _as_str(row.get("label")) in LIVE_WAKE_LABELS
    }
    out: list[Any] = []
    for row in rows or []:
        label = _as_str(row.get("label")) if isinstance(row, dict) else ""
        out.append(fresh.get(label, row))
    return out


def _merge_count_rows(published: dict[str, Any], rebuilt: dict[str, Any]) -> list[dict[str, str]]:
    """Keep published paper_win strings; raise settled/pending when local adds official rows."""
    labels: list[str] = []
    by_label: dict[str, dict[str, str]] = {}
    for row in ((published.get("settle") or {}).get("counts") or []) + (
        (rebuilt.get("settle") or {}).get("counts") or []
    ):
        if not isinstance(row, dict) or not row.get("label"):
            continue
        # Keyed on the base label so a published row that already carries its lineage
        # prefix still matches the unprefixed rebuilt row rather than duplicating it.
        label = _base_label(_as_str(row.get("label")))
        if label not in by_label:
            labels.append(label)
            by_label[label] = {
                "label": _as_str(row.get("label")),
                "value": _as_str(row.get("value")),
            }
            if row.get("note"):
                by_label[label]["note"] = _as_str(row.get("note"))
            continue
        if label in {"Pending windows", "Settled windows", "paper_win"}:
            try:
                by_label[label]["value"] = _as_str(
                    max(int(by_label[label]["value"] or "0"), int(str(row.get("value") or "0")))
                )
            except ValueError:
                pass
    pub_residuals = (published.get("settle") or {}).get("residual") or []
    residuals = _merge_residuals(pub_residuals, (rebuilt.get("settle") or {}).get("residual"))
    pending = sum(1 for row in residuals if _residual_is_pending(row))
    pub_labels = {
        _as_str(row.get("label"))
        for row in pub_residuals
        if isinstance(row, dict) and row.get("label")
    }
    extra_settled = [
        row
        for row in residuals
        if not _residual_is_pending(row) and row.get("label") not in pub_labels
    ]
    extra_wins = sum(
        1
        for row in extra_settled
        if "result=yes" in f"{row.get('value')} {row.get('note')}".lower()
        or _as_str(row.get("value")).lower() == "paper_win"
    )
    if "Pending windows" in by_label:
        by_label["Pending windows"]["value"] = _as_str(pending)
    if extra_settled and "Settled windows" in by_label:
        try:
            by_label["Settled windows"]["value"] = _as_str(
                int(by_label["Settled windows"]["value"] or "0") + len(extra_settled)
            )
        except ValueError:
            pass
    if extra_wins and "paper_win" in by_label:
        try:
            by_label["paper_win"]["value"] = _as_str(
                int(by_label["paper_win"]["value"] or "0") + extra_wins
            )
        except ValueError:
            pass
    return [by_label[label] for label in labels]


def _merge_15m_lanes(published: dict[str, Any], rebuilt: dict[str, Any]) -> dict[str, Any]:
    """Published paper history plus new local official rows. Do not invent win/lose."""
    out = dict(rebuilt)
    pub_settle = published.get("settle") or {}
    new_settle = dict(rebuilt.get("settle") or {})
    residuals = _merge_residuals(pub_settle.get("residual"), new_settle.get("residual"))
    pending = any(_residual_is_pending(row) for row in residuals)
    sources = []
    seen_src: set[tuple[str, str]] = set()
    for row in list(pub_settle.get("sources") or []) + list(new_settle.get("sources") or []):
        if not isinstance(row, dict):
            continue
        key = (_as_str(row.get("label")), _as_str(row.get("value")))
        if key in seen_src or not key[0]:
            continue
        seen_src.add(key)
        sources.append({"label": key[0], "value": key[1]})
    notes = []
    for note in list(pub_settle.get("notes") or []) + list(new_settle.get("notes") or []):
        text = _as_str(note)
        if text and text not in notes:
            notes.append(text)
    headline = _as_str(pub_settle.get("headline") or new_settle.get("headline"))
    extra_pending = [row["label"] for row in residuals if _residual_is_pending(row)]
    if extra_pending and extra_pending[0] not in headline:
        headline = (
            f"{headline} Local journal also pending {', '.join(extra_pending)}."
            if headline
            else new_settle.get("headline")
        )
    new_settle["residual"] = residuals
    new_settle["counts"] = _refresh_live_rows(
        _merge_count_rows(published, rebuilt),
        (rebuilt.get("settle") or {}).get("counts"),
    )
    new_settle["sources"] = sources or new_settle.get("sources") or []
    new_settle["notes"] = notes or new_settle.get("notes") or []
    new_settle["headline"] = headline
    new_settle["banner"] = SETTLE_PENDING if pending else new_settle.get("banner")
    new_settle["banner_state"] = "pending" if pending else new_settle.get("banner_state")
    out["settle"] = new_settle
    pub_run = published.get("last_run") or {}
    new_run = dict(rebuilt.get("last_run") or {})
    if pub_run.get("status") == "published export":
        new_run["status"] = "published export"
        if pub_run.get("headline"):
            new_run["headline"] = _as_str(pub_run.get("headline"))
        fields = list(pub_run.get("fields") or [])
        seen_labels = {_as_str(row.get("label")) for row in fields if isinstance(row, dict)}
        for row in new_run.get("fields") or []:
            if isinstance(row, dict) and _as_str(row.get("label")) not in seen_labels:
                fields.append(row)
        new_run["fields"] = _refresh_live_rows(fields, new_run.get("fields"))
        run_notes = []
        for note in list(pub_run.get("notes") or []) + list(new_run.get("notes") or []):
            text = _as_str(note)
            if text and text not in run_notes:
                run_notes.append(text)
        new_run["notes"] = run_notes
    out["last_run"] = new_run
    pub_ledger = published.get("paper_ledger") or {}
    new_ledger = dict(rebuilt.get("paper_ledger") or {})
    if pub_ledger.get("rows"):
        rows = list(pub_ledger.get("rows") or [])
        seen = {_as_str(row.get("label")) for row in rows if isinstance(row, dict)}
        for row in new_ledger.get("rows") or []:
            if isinstance(row, dict) and _as_str(row.get("label")) not in seen:
                rows.append(row)
        new_ledger["rows"] = _refresh_live_rows(rows, new_ledger.get("rows"))
        if pub_ledger.get("headline"):
            new_ledger["headline"] = _as_str(pub_ledger.get("headline"))
        ledger_notes = []
        for note in list(pub_ledger.get("notes") or []) + list(new_ledger.get("notes") or []):
            text = _as_str(note)
            if text and text not in ledger_notes:
                ledger_notes.append(text)
        new_ledger["notes"] = ledger_notes
    out["paper_ledger"] = new_ledger
    return out


def _wake_rows_by_label(wake: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    return {
        _as_str(row.get("label")): row
        for row in wake.get(key) or []
        if isinstance(row, dict) and row.get("label")
    }


def _restate_stale_pending(notes: list[Any] | None, missing: dict[str, dict[str, Any]]) -> list[str]:
    """Swap a note that calls a missing-join window pending for the honest sentence."""
    # A note already restated on an earlier export no longer names its ticker, so
    # match the restated sentence as well and put the window back in front of it.
    restated = {_as_str(row.get("note")): ticker for ticker, row in missing.items()}
    out: list[str] = []
    for note in notes or []:
        text = _as_str(note)
        ticker = restated.get(text, "")
        if not ticker:
            hit = next((t for t in missing if t and t in text), "")
            ticker = hit if hit and "pending" in text.lower() else ""
        if ticker:
            text = f"{ticker} — {_as_str(missing[ticker].get('note'))}"
        if text and text not in out:
            out.append(text)
    return out


def _restate_residual(row: Any, missing: dict[str, dict[str, Any]]) -> Any:
    if not isinstance(row, dict):
        return row
    hit = missing.get(_as_str(row.get("label")))
    if not hit:
        return row
    return {
        "label": _as_str(row.get("label")),
        "value": _as_str(hit.get("value")),
        "note": _as_str(hit.get("note")),
    }


def _live_settle_status() -> dict[str, str]:
    """`settle_status` per ticker, re-read off the settle files at export time.

    `learning_wake.json` is written on the watch cycle, so a window that gained its
    official Kalshi result between that cycle and this export is still cached there
    as pending. Pending is decided here instead, against the files as they are now.
    """
    out: dict[str, str] = {}
    for row in _settle_rows():
        ticker = _as_str(row.get("ticker"))
        if ticker:
            out[ticker] = _as_str(row.get("settle_status") or SETTLE_PENDING)
    return out


def _reconcile_pending(
    residual: list[Any],
    wake_pending: dict[str, dict[str, Any]],
    live: dict[str, str],
) -> list[dict[str, str]]:
    """The one pending list this export publishes — count, ticker and block alike.

    A window is pending only while the live settle files show no official Kalshi
    result for it. A live `settled` status vetoes a cached wake entry; it is never
    read the other way round, and a vetoed window gains no pnl by leaving the list.
    """
    rows: dict[str, dict[str, str]] = {}
    for row in residual:
        if not isinstance(row, dict):
            continue
        label = _as_str(row.get("label"))
        if not label or not _residual_is_pending(row):
            continue
        if live.get(label) == SETTLE_SETTLED:
            continue
        cached = wake_pending.get(label) or {}
        rows[label] = {
            "label": label,
            "value": SETTLE_PENDING,
            "note": _as_str(cached.get("note")) or _as_str(row.get("note")) or SETTLE_PENDING,
            "kind": _as_str(cached.get("kind")) or "awaiting_kalshi_result",
        }
    # A book can be open before its join file is written, so the wake may name a
    # window the settle files do not carry yet. Kept only while nothing contradicts it.
    settled_here = {
        _as_str(row.get("label"))
        for row in residual
        if isinstance(row, dict) and not _residual_is_pending(row)
    }
    for label, cached in wake_pending.items():
        if label in rows or label in settled_here or live.get(label) == SETTLE_SETTLED:
            continue
        rows[label] = {
            "label": label,
            "value": SETTLE_PENDING,
            "note": _as_str(cached.get("note")) or SETTLE_PENDING,
            "kind": _as_str(cached.get("kind")) or "book_open_no_join",
        }
    return list(rows.values())


def _assert_pending_is_not_settled(lane: dict[str, Any]) -> None:
    """Refuse to publish a window as pending that the same file records as settled."""
    settled = {
        _as_str(row.get("label"))
        for row in ((lane.get("settle") or {}).get("residual") or [])
        if isinstance(row, dict) and not _residual_is_pending(row)
    }
    pending = [
        _as_str(row.get("label"))
        for row in ((lane.get("learning_status") or {}).get("pending_windows") or [])
        if isinstance(row, dict)
    ]
    clash = sorted(set(pending) & settled)
    if clash:
        raise RuntimeError(
            "refused to publish a settled window as pending: "
            f"{', '.join(clash)} is both pending and settled in this manifest"
        )
    counted = _settle_count_value(lane, "Pending windows")
    if counted != len(pending):
        raise RuntimeError(
            f"pending count {counted} disagrees with pending windows {pending}"
        )


def _label_lineage_b_counts(counts: list[Any] | None, pending_n: int) -> list[Any]:
    """Name the book each settle count belongs to, and post the reconciled pending."""
    out: list[Any] = []
    for row in counts or []:
        if not isinstance(row, dict):
            out.append(row)
            continue
        base = _base_label(_as_str(row.get("label")))
        row = dict(row)
        if base == "Pending windows":
            row["value"] = _as_str(pending_n)
        elif base == "Settled windows":
            row["note"] = SETTLED_WINDOWS_NOTE
        elif base in LINEAGE_B_COUNT_LABELS:
            row["label"] = LINEAGE_B_PREFIX + base
        out.append(row)
    return out


def _wake_block_for_export(
    wake: dict[str, Any],
    pending_rows: list[dict[str, str]],
) -> dict[str, Any]:
    """The wake block as published: pending re-derived, the rest as the scan read it."""
    if not wake:
        return wake
    out = dict(wake)
    out["pending_windows"] = pending_rows
    out["rows"] = [
        {**row, "value": _as_str(len(pending_rows))}
        if isinstance(row, dict)
        and _as_str(row.get("label")) == "Pending windows on this tree"
        else row
        for row in out.get("rows") or []
    ]
    out["pending_source"] = (
        "live settlements/*.json re-read at export time, not the cached wake file"
    )
    return out


def _settle_headline_from_wake(
    missing: dict[str, dict[str, Any]],
    pending: dict[str, dict[str, Any]],
    kept: dict[str, dict[str, Any]],
) -> str:
    parts: list[str] = []
    for ticker, row in missing.items():
        result = _as_str(row.get("official_result"))
        parts.append(
            f"{ticker} is a missing paper join, not a pending window: Kalshi settled it "
            f"{result or 'and the result is on the tape'}, the paper book the published "
            "lineage names is not on this tree, so there is no paper pnl here and none "
            "is invented."
        )
    if pending:
        parts.append(
            f"{', '.join(pending)} is {SETTLE_PENDING} for want of a Kalshi result. "
            "can_close_early: wait; if close_time moves the window re-keys."
        )
    for ticker, row in kept.items():
        pnl = _as_str(row.get("published_paper_pnl"))
        outcome = _as_str(row.get("value")) or "published paper history"
        parts.append(
            f"Lineage B still publishes {ticker} {outcome} {pnl}".rstrip()
            + f". {NEVER_SUMMED_NOTE}"
        )
    return " ".join(parts)


def _last_run_headline_from_wake(
    missing: dict[str, dict[str, Any]],
    kept: dict[str, dict[str, Any]],
    books_on_tree: str,
) -> str:
    parts: list[str] = []
    for ticker, row in kept.items():
        pnl = _as_str(row.get("published_paper_pnl"))
        outcome = _as_str(row.get("value")) or "published paper history"
        parts.append(f"Lineage B published {ticker} {outcome} {pnl}".rstrip() + ".")
    for ticker, row in missing.items():
        parts.append(f"{ticker}: {_as_str(row.get('note'))}")
    if books_on_tree:
        parts.append(
            f"Lineage A holds {books_on_tree} paper books on this tree, counted apart "
            "from lineage B and never added to it."
        )
    parts.append("Observation only.")
    return " ".join(parts)


def _apply_wake_wording(lane: dict[str, Any], wake: dict[str, Any]) -> dict[str, Any]:
    """Restate the published pending wording for windows Kalshi has already settled.

    A window with an official result and no paper book here is a missing paper join,
    not a pending window (LEARNING_LANE_15M_SOURCE_DIGEST.md §4a). The published
    manifest is read back as ``existing`` on every export, so a hand edit would be
    overwritten on the next cycle; this restates it from the wake scan every time.
    """
    missing = _wake_rows_by_label(wake, "missing_paper_joins")
    kept = _wake_rows_by_label(wake, "published_history")

    out = dict(lane)
    settle = dict(out.get("settle") or {})
    settle["residual"] = [_restate_residual(row, missing) for row in settle.get("residual") or []]
    # One pending list, re-derived from the live settle files, feeding the count, the
    # headline ticker and the learning_status block alike. Ticker and count cannot
    # disagree because neither is read off the cached wake file any more.
    still_pending = _reconcile_pending(
        settle["residual"],
        _wake_rows_by_label(wake, "pending_windows"),
        _live_settle_status(),
    )
    pending = {row["label"]: row for row in still_pending}
    settle["counts"] = _label_lineage_b_counts(settle.get("counts"), len(still_pending))
    # Nothing settled yet is not the same as settled, so the banner stays pending
    # until at least one window on this tree carries an official result.
    unsettled = bool(still_pending) or not any(
        isinstance(row, dict) and not _residual_is_pending(row)
        for row in settle["residual"]
    )
    settle["banner"] = SETTLE_PENDING if unsettled else "settled"
    settle["banner_state"] = "pending" if unsettled else "off"
    settle["notes"] = _restate_stale_pending(settle.get("notes"), missing)
    headline = _settle_headline_from_wake(missing, pending, kept)
    if headline:
        settle["headline"] = headline
    out["settle"] = settle
    out["learning_status"] = _wake_block_for_export(wake, still_pending)

    last_run = dict(out.get("last_run") or {})
    fields = list(last_run.get("fields") or [])
    by_label = {_as_str(r.get("label")): r for r in fields if isinstance(r, dict)}
    live_ticker = _as_str((by_label.get(LIVE_FILL_LABEL) or {}).get("value"))
    if live_ticker in missing and LIVE_FILL_STATUS_LABEL in by_label:
        fields = [
            (
                {
                    "label": LIVE_FILL_STATUS_LABEL,
                    "value": _as_str(missing[live_ticker].get("value")),
                    "note": _as_str(missing[live_ticker].get("note")),
                }
                if isinstance(row, dict)
                and _as_str(row.get("label")) == LIVE_FILL_STATUS_LABEL
                else row
            )
            for row in fields
        ]
        last_run["fields"] = fields
    last_run["notes"] = _restate_stale_pending(last_run.get("notes"), missing)
    books_on_tree = _as_str((_wake_row(wake, "Paper books on this tree") or {}).get("value"))
    if missing or kept:
        last_run["headline"] = _last_run_headline_from_wake(missing, kept, books_on_tree)
    out["last_run"] = last_run

    if kept:
        ledger = dict(out.get("paper_ledger") or {})
        ledger["headline"] = LINEAGE_B_LEDGER_HEADLINE
        notes = [_as_str(n) for n in ledger.get("notes") or [] if _as_str(n)]
        if NEVER_SUMMED_NOTE not in notes:
            notes.append(NEVER_SUMMED_NOTE)
        ledger["notes"] = notes
        out["paper_ledger"] = ledger
    return out


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


def _wake_block() -> dict[str, Any]:
    """Learning-wake status as the wake module recorded it. Read only, never a tick."""
    from golf_offshoot.learning_lane_15m.learn import learning_status_block

    return learning_status_block()


def _wake_row(wake: dict[str, Any], label: str) -> dict[str, str]:
    for row in wake.get("rows") or []:
        if isinstance(row, dict) and row.get("label") == label:
            return row
    return {}


def _wake_display_rows(wake: dict[str, Any]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """(last_run fields, settle counts) so honesty status is drawn, not just filed."""
    if wake.get("status") == "not yet available":
        return [], []
    owed = wake.get("roles_owed") or []
    fields = [
        {
            "label": "Learning wake",
            "value": _as_str(wake.get("status")),
            "note": _as_str(wake.get("headline")),
        },
        {
            "label": "Crew roles owed",
            "value": ", ".join(_as_str(row.get("label")) for row in owed) or "none",
            "note": "; ".join(
                f"{_as_str(row.get('label'))} {_as_str(row.get('value'))}" for row in owed
            )
            or "roles_owed is a request for a turn, never a record that a role ran",
        },
        {"label": "Wake checked", "value": _as_str(wake.get("updated_text"))},
    ]
    counts = [
        row
        for row in (
            _wake_row(wake, "Official result, paper book not on this tree"),
            _wake_row(wake, "Published paper history kept"),
        )
        if row
    ]
    return fields, counts


def _15m_chart_slots() -> tuple[list[dict[str, Any]], str]:
    """Illustrator PNG only if the file exists. Never invent a chart."""
    rel = "data/charts/learning_lane_15m/paper_window_strip.png"
    path = repo_root() / "docs" / "observability-hub" / rel
    if not path.is_file():
        return [], "15m viz wall is not yet available. Charts are not invented."
    return (
        [
            {
                "slot_id": "paper_window_strip",
                "title": "15m paper window strip",
                "subline": "Bars from settlement join files — not invented · not a golf WC1 chart",
                "badges": ["LEARNING LANE", "PAPER OBSERVATION ONLY", "AI: NO CASH IN/OUT"],
                "status": "available",
                "path": rel,
                "note": "read-only PNG from official join files",
            }
        ],
        "15m strip is a settlement-file render only. Not edge. Golf Ill / WC1 do not transfer.",
    )


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
    wake = _wake_block()
    wake_fields, wake_counts = _wake_display_rows(wake)
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
                *wake_fields,
            ],
            "notes": [
                "Official settle is Kalshi result matched to documented CF Benchmarks SOURCE.",
                "A CFB websocket / DIY 60s average is observe-only.",
                "Roles owed is a request for a turn. It is never a record that a role ran.",
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
                *wake_counts,
            ],
            "sources": [
                {"label": "official_settle", "value": "Kalshi result matched to CF Benchmarks SOURCE"},
            ],
            "residual": banners,
            "observation": None,
            "notes": [
                "Do not invent win/lose. Display prices are not settle evidence.",
                WAKE_JOIN_NOTE,
            ],
        },
        "paper_ledger": {
            "status": "counts only — no cash figures published",
            "headline": "Paper ticket counts. No cash figure is published on this page.",
            "rows": [
                # Labelled by lineage so a published row and a local row that mean
                # different books can never shadow or be reconciled against each other.
                {
                    "label": LINEAGE_A_LEDGER_ROWS[0][0],
                    "value": _as_str(open_books),
                },
                {
                    "label": LINEAGE_A_LEDGER_ROWS[1][0],
                    "value": _as_str(settled_books),
                },
                {
                    "label": LINEAGE_A_LEDGER_ROWS[2][0],
                    "value": _as_str(len(ledger.entries)),
                },
                {"label": "Series", "value": PRIMARY_SERIES},
            ],
            "absent_fields": ["payout", "realized_pnl", "roi"],
            "notes": [
                "Counts only. Cash-shaped columns are absent, not derived.",
                "Leftovers stay documented PROPOSED (not Softened).",
                NEVER_SUMMED_NOTE,
            ],
        },
        "records": [],
        "records_note": (
            "No weekly operating record exists for this lane. "
            "Do not read the golf WC1 FAIL as this lane's result."
        ),
        "learning_status": wake,
        "charts": _15m_chart_slots()[0],
        "charts_note": _15m_chart_slots()[1],
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
                "learning_lane_15m paper journal is published in this Pages manifest. "
                "This file is a snapshot of a live 15-minute loop; generated_at is when "
                "it was written. A KXBTC15M window rotates about every 15 minutes, so a "
                "pending ticker here is what was true at generated_at, not necessarily now."
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
    published15 = _lane_by_id(existing, LANE_15M)
    if published15 and published15.get("lane_id") == LANE_15M:
        lane15 = _merge_15m_lanes(published15, lane15)
    lane15 = _apply_wake_wording(lane15, lane15.get("learning_status") or {})
    _assert_pending_is_not_settled(lane15)
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


def _lane_publish_fingerprint(lane: dict[str, Any] | None) -> dict[str, Any]:
    """The fields a reader can mistake for live truth. Not heartbeat / age / generated_at."""
    lane = lane or {}
    settle = lane.get("settle") or {}
    last = lane.get("last_run") or {}
    learn = lane.get("learning_status") or {}
    charts = lane.get("charts") or []
    return {
        "headline": str(settle.get("headline") or ""),
        "last_headline": str(last.get("headline") or ""),
        "residual": tuple(
            (str(row.get("label") or ""), str(row.get("value") or ""), str(row.get("note") or ""))
            for row in (settle.get("residual") or [])
            if isinstance(row, dict)
        ),
        "counts": tuple(
            (str(row.get("label") or ""), str(row.get("value") or ""))
            for row in (settle.get("counts") or [])
            if isinstance(row, dict)
        ),
        "missing_joins": tuple(
            (str(row.get("label") or ""), str(row.get("value") or ""))
            for row in (learn.get("missing_paper_joins") or [])
            if isinstance(row, dict)
        ),
        "pending": tuple(
            str(row.get("label") or row.get("ticker") or "")
            for row in (learn.get("pending_windows") or [])
            if isinstance(row, dict)
        ),
        "published": tuple(
            (
                str(row.get("label") or ""),
                str(row.get("value") or ""),
                str(row.get("published_paper_pnl") or ""),
            )
            for row in (learn.get("published_history") or [])
            if isinstance(row, dict)
        ),
        "charts": tuple(
            (str(slot.get("slot_id") or ""), str(slot.get("status") or ""), str(slot.get("path") or ""))
            for slot in charts
            if isinstance(slot, dict)
        ),
    }


def material_publish_reasons(
    published: dict[str, Any] | None,
    candidate: dict[str, Any],
) -> list[str]:
    """Why this export should ship to Pages. Empty means heartbeat — do not publish."""
    if not published:
        return ["no published manifest to compare"]
    old = _lane_publish_fingerprint(_lane_by_id(published, LANE_15M))
    new = _lane_publish_fingerprint(_lane_by_id(candidate, LANE_15M))
    reasons: list[str] = []
    if old["headline"] != new["headline"] or old["last_headline"] != new["last_headline"]:
        reasons.append("settle-status wording changed")
    if old["residual"] != new["residual"]:
        reasons.append("settle residual changed")
    if old["counts"] != new["counts"]:
        reasons.append("lineage or settle counts changed")
    if old["missing_joins"] != new["missing_joins"]:
        reasons.append("missing-paper-join residual changed")
    if old["pending"] != new["pending"]:
        reasons.append("pending window identity changed")
    if old["published"] != new["published"]:
        reasons.append("published paper history changed")
    if old["charts"] != new["charts"]:
        reasons.append("chart slot changed")
    return reasons


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
