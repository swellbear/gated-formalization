"""Derive the honesty gate from files instead of trusting typed prose.

The gate used to be four asterisks and a word, typed by hand on the desk and
verified against nothing. The demonstrated capability was "reword the desk
until Lab is unblocked."

Three of the four boxes are derivable from evidence the wake already reads, so
they are derived here and the **derived verdict wins**. Desk prose can shut a
derived box; it can never open one. The fourth genuinely needs judgment, so it
must carry evidence — PIDs, file hashes, timestamps — and a stamp with no
evidence attached does not open the gate.

The parser is deliberately **not** widened to accept more phrasings. It is
narrowed: a judgment box now needs `**PASS**` *and* evidence.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

#: Keyword that identifies a desk row, so a reworded box still maps to its
#: derivation instead of quietly becoming a free-text judgment row.
BOX_LINEAGE = "lineage"
BOX_MISSING_JOIN = "missing_join"
BOX_HUB_TREE = "hub_tree"
BOX_NO_INVENT = "no_invented"

DERIVED_BOXES = (BOX_LINEAGE, BOX_MISSING_JOIN, BOX_HUB_TREE)

#: The window the missing-join box is about.
MISSING_JOIN_TICKER = "KXBTC15M-26SEP071500-00"

HUB_PORT = 8765

#: Evidence a judgment box must carry. An adjective is not evidence.
_EVIDENCE_PATTERNS = (
    re.compile(r"\bPID\s*\d+", re.IGNORECASE),
    re.compile(r"\b[0-9a-f]{16,64}\b"),
    re.compile(r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}"),
    re.compile(r"\b\d{2}:\d{2}(:\d{2})?\b"),
)


def classify_box(title: str) -> str:
    """Map a desk row title onto its derivation, by keyword not by exact text."""
    low = title.lower()
    if "071500-00" in low or "missing join" in low:
        return BOX_MISSING_JOIN
    if BOX_LINEAGE in low:
        return BOX_LINEAGE
    if "hub process" in low or "hub tree" in low:
        return BOX_HUB_TREE
    if "invented" in low:
        return BOX_NO_INVENT
    return ""


def has_evidence(cell: str) -> bool:
    return any(pattern.search(cell) for pattern in _EVIDENCE_PATTERNS)


# ------------------------------------------------------------------ hub tree


def hub_trees() -> dict[str, Any]:
    """Count hub **trees**, not OS processes.

    The criterion is preserved exactly as written: a supervisor plus its child
    is one hub. Two independent supervisors are two hubs.
    """
    try:
        import psutil
    except Exception as exc:  # noqa: BLE001 — no psutil is not a pass
        return {"ok": False, "trees": None, "note": f"cannot read the process table: {exc}"}

    hubs: dict[int, dict[str, Any]] = {}
    for proc in psutil.process_iter(["pid", "ppid", "cmdline"]):
        try:
            argv = proc.info.get("cmdline") or []
        except Exception:  # noqa: BLE001
            continue
        line = " ".join(str(a) for a in argv)
        if "golf_offshoot" in line and " shell" in f" {line}":
            hubs[int(proc.info["pid"])] = {
                "pid": int(proc.info["pid"]),
                "ppid": int(proc.info.get("ppid") or 0),
            }
    roots = [row for row in hubs.values() if row["ppid"] not in hubs]
    listener = None
    try:
        for conn in psutil.net_connections(kind="tcp"):
            if conn.laddr and conn.laddr.port == HUB_PORT and conn.status == psutil.CONN_LISTEN:
                listener = conn.pid
                break
    except Exception:  # noqa: BLE001 — needs privileges on some systems
        listener = None
    return {
        "ok": len(roots) == 1,
        "trees": len(roots),
        "roots": [row["pid"] for row in roots],
        "pids": sorted(hubs),
        "listener_pid": listener,
        "port": HUB_PORT,
        "note": (
            f"one hub tree: supervisor {roots[0]['pid']} over {sorted(hubs)}, "
            f"listener {listener} on {HUB_PORT}"
            if len(roots) == 1
            else f"{len(roots)} independent hub trees: {[r['pid'] for r in roots]}"
        ),
    }


# ------------------------------------------------------------- derived boxes


def derive_boxes(
    scan: dict[str, Any] | None,
    *,
    invariants: dict[str, Any] | None = None,
    hub: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    """Machine verdicts for the boxes that do not need a human."""
    scan = scan or {}
    out: dict[str, dict[str, Any]] = {}

    # Lineage: A is the local ledger, B is the kept published history. The box
    # is about them staying apart, so the derivation is that B survives as its
    # own rows and nothing reports a combined figure.
    published_only = scan.get("published_only") or []
    ledger = scan.get("ledger") or {}
    summed = any(
        str(key).lower() in {"combined_bankroll", "total_bankroll", "all_lineages"}
        for key in ledger
    )
    out[BOX_LINEAGE] = {
        "ok": (not summed) and isinstance(ledger, dict) and bool(ledger),
        "note": (
            f"lineage A ledger present; lineage B kept as {len(published_only)} "
            "published row(s); no combined figure on the scan"
            if not summed
            else "a combined bankroll figure appeared on the scan"
        ),
        "evidence": {
            "published_only": [row.get("ticker") for row in published_only],
            "ledger_bankroll": ledger.get("bankroll"),
            "combined_field_present": summed,
        },
    }

    # Missing join: the window must be reported as a missing paper join with an
    # official result and no invented pnl — never as SETTLE_PENDING.
    missing = scan.get("paper_join_missing") or []
    row = next((r for r in missing if MISSING_JOIN_TICKER in str(r.get("ticker") or "")), None)
    pending_tickers = {
        str(r.get("ticker") or "") for r in scan.get("pending") or []
    }
    invented = [r for r in missing if r.get("paper_pnl") not in (None, "", "none")]
    ok = MISSING_JOIN_TICKER not in pending_tickers and not invented
    out[BOX_MISSING_JOIN] = {
        "ok": ok,
        "note": (
            f"{MISSING_JOIN_TICKER} is not on the pending list and no "
            f"missing-join row carries a pnl ({len(missing)} row(s) scanned)"
            if ok
            else f"{MISSING_JOIN_TICKER} is being reported pending, or a missing join carries a pnl"
        ),
        "evidence": {
            "row_present": bool(row),
            "on_pending_list": MISSING_JOIN_TICKER in pending_tickers,
            "rows_with_pnl": [r.get("ticker") for r in invented],
        },
    }

    hub_state = hub if hub is not None else hub_trees()
    out[BOX_HUB_TREE] = {
        "ok": bool(hub_state.get("ok")),
        "note": hub_state.get("note"),
        "evidence": hub_state,
    }
    return out
