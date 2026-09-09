"""Cite the factory fee-schedule pin. A cite is not a dated fee-apply."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.localtime import now

DOCS = Path(__file__).resolve().parents[3] / "docs"
FACTORY_BAR = DOCS / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
HONER_BAR = DOCS / "HONER_15M_EVIDENCE_BAR.json"


def factory_schedule_sha256(*, bar_path: Path | None = None) -> str:
    """Read the factory pin from the bar JSON. Does not import the factory package."""
    path = bar_path if bar_path is not None else FACTORY_BAR
    if not path.is_file():
        return ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    if not isinstance(payload, dict):
        return ""
    fee = payload.get("fee_hurdle") or {}
    if not isinstance(fee, dict):
        return ""
    return str(fee.get("schedule_sha256") or "").strip().lower()


def cite_factory_pin(
    *,
    factory_bar: Path | None = None,
    honer_bar: Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    """Record the factory sha256 onto the honer bar. Does not clear ``fee_omitted``."""
    sha = factory_schedule_sha256(bar_path=factory_bar)
    cite = {
        "schedule_sha256": sha,
        "cited_at": now().isoformat(),
        "fee_omitted": True,
        "note": (
            "cite of factory schedule_sha256; not a dated honer fee-apply; "
            "keep-lock stays closed while fee_omitted"
            if sha
            else "factory pin empty; cannot apply; keep-lock stays closed"
        ),
    }
    if not write:
        return cite
    path = honer_bar if honer_bar is not None else HONER_BAR
    if not path.is_file():
        return cite
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return cite
    if not isinstance(payload, dict):
        return cite
    payload["factory_fee_cite"] = cite
    payload["fee_omitted"] = True
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return cite
