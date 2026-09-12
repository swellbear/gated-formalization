"""HONER-FAMILY-AMEND doorbell from files. Not exam pnl."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.catalog import third_family_dated
from golf_offshoot.honer_15m.library import load_library, search_is_parked
from golf_offshoot.honer_15m.paths import assert_honer_path, exam_score_path, family_amend_path
from golf_offshoot.localtime import now

KIND = "HONER-FAMILY-AMEND"
REASON_EXHAUSTED = "catalog_exhausted"
REASON_DEAD = "completed_dead"
MONEY_KEYS = frozenset({"pnl", "d", "bankroll", "winner", "mean_d", "exam_pnl", "betting_pnl"})


def exam_completed_dead_from_files() -> bool:
    """True when library rows or exam_score.outcome say completed_dead. Ignores pnl."""
    payload = load_library()
    for row in payload.get("rows") or []:
        if isinstance(row, dict) and str(row.get("outcome") or "") == REASON_DEAD:
            return True
    path = exam_score_path()
    if not path.is_file():
        return False
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(card, dict):
        return False
    return str(card.get("outcome") or "") == REASON_DEAD


def family_amend_reasons_from_files() -> list[str]:
    """Why the kind is owed. File labels only. Does not read ledgers or exam d."""
    reasons: list[str] = []
    if search_is_parked():
        reasons.append(REASON_EXHAUSTED)
    if exam_completed_dead_from_files():
        reasons.append(REASON_DEAD)
    return reasons


def family_amend_owed_from_files() -> bool:
    return bool(family_amend_reasons_from_files())


def stamp_family_amend() -> dict[str, Any]:
    """Write latest/family_amend.json. No money keys. third_family from catalog files."""
    reasons = family_amend_reasons_from_files()
    exhausted = search_is_parked()
    dead = exam_completed_dead_from_files()
    dated = third_family_dated()
    payload = {
        "schema": 1,
        "lane": "honer_15m",
        "kind": KIND,
        "owed": bool(reasons) and not dated,
        "reasons": reasons,
        "catalog_exhausted": exhausted,
        "exam_completed_dead": dead,
        "third_family": dated,
        "framing": (
            "Doorbell from files (library catalog_exhausted or exam completed_dead). "
            "Not exam pnl. Third family is dated from Honer files when the catalog "
            "has a third item; this sidecar does not ping Lab."
            if dated
            else (
                "Doorbell from files (library catalog_exhausted or exam completed_dead). "
                "Not exam pnl. Third family is legal from those files and is dated "
                "from the catalog, not by pinging Lab."
            )
        ),
        "updated_at": now().isoformat(),
    }
    for key in MONEY_KEYS:
        payload.pop(key, None)
    path = family_amend_path()
    assert_honer_path(path)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
