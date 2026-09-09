"""Keep-lock. A green exam is not a keep while this returns a reason."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BAR_JSON = Path(__file__).resolve().parents[3] / "docs" / "HONER_15M_EVIDENCE_BAR.json"


def load_bar() -> dict[str, Any]:
    if not BAR_JSON.is_file():
        return {
            "binding": False,
            "fee_omitted": True,
            "founder_read_once": False,
            "lab_admits": False,
            "trading_armed": False,
        }
    try:
        payload = json.loads(BAR_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"binding": False, "fee_omitted": True, "founder_read_once": False}
    return payload if isinstance(payload, dict) else {}


def keep_blocked_reason(bar: dict[str, Any] | None = None) -> str | None:
    payload = bar if bar is not None else load_bar()
    if payload.get("fee_omitted", True):
        return "fee omitted"
    if payload.get("binding") is not True:
        return "bar not binding"
    if payload.get("founder_read_once") is not True:
        return "founder_read_once false"
    if payload.get("lab_admits"):
        return "lab_admits is not a keep"
    if payload.get("trading_armed"):
        return "trading NOT ARMED"
    return None


def can_keep(bar: dict[str, Any] | None = None) -> bool:
    return keep_blocked_reason(bar) is None
