"""Load the frozen factory overlay catalog. File order is the picker. Pnl does not rank."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.repo_paths import repo_root

LIBRARY_REL = Path("golf-offshoot") / "docs" / "FACTORY_OVERLAY.json"
CATALOG_KIND = "F-SKIP-FOREIGN-HORIZON"
FOREIGN_HORIZON_ID = "F-SKIP-FOREIGN-HORIZON"
FROZEN_IDS = (FOREIGN_HORIZON_ID,)
QUEUED_NEXT = ("F-SKIP-NON-PRIMARY-CONTRACT",)


class FactoryOverlayError(ValueError):
    """Overlay catalog is malformed, mixed with P-*/Honer, or fill-NO."""


def library_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else repo_root()) / LIBRARY_REL


def _as_upper(value: Any) -> str:
    return str(value or "").strip().upper()


def _looks_like_fill_no(row: dict[str, Any]) -> bool:
    side = _as_upper(row.get("side"))
    if side in {"NO", "FILL_NO", "FILL-NO"}:
        return True
    blobs = [
        str(row.get("id") or ""),
        str(row.get("skip_when") or ""),
        str(row.get("else") or ""),
        str(row.get("kind") or ""),
        str((row.get("params") or {}).get("side") or ""),
    ]
    joined = " ".join(blobs).lower().replace("_", "-")
    return "fill-no" in joined or "buy no" in joined or "buy-no" in joined


def _validate_row(row: dict[str, Any], *, index: int) -> None:
    if not isinstance(row, dict):
        raise FactoryOverlayError(f"policy {index} must be an object")
    ident = str(row.get("id") or "").strip()
    if not ident:
        raise FactoryOverlayError(f"policy {index} missing id")
    if ident.startswith("P-"):
        raise FactoryOverlayError(f"{ident} is a P-* row; factory overlay must not mix")
    if ident.startswith("H-SKIP-"):
        raise FactoryOverlayError(f"{ident} is a Honer copy; do not copy H-SKIP-*")
    if ident.startswith("G-SKIP-"):
        raise FactoryOverlayError(f"{ident} is golf-only; factory overlay must not name G-SKIP-*")
    if _looks_like_fill_no(row):
        raise FactoryOverlayError(f"{ident} is fill-NO; zero fill-NO rows")
    if _as_upper(row.get("side")) not in {"", "YES"}:
        raise FactoryOverlayError(f"{ident} side must be yes")
    params = row.get("params") or {}
    if not isinstance(params, dict):
        raise FactoryOverlayError(f"{ident} params must be an object")
    if ident == FOREIGN_HORIZON_ID:
        if str(params.get("missing_horizon") or "fill") != "fill":
            raise FactoryOverlayError("F-SKIP-FOREIGN-HORIZON missing horizon must fill YES")
        if str(params.get("missing_series") or "fill") != "fill":
            raise FactoryOverlayError("F-SKIP-FOREIGN-HORIZON missing series must fill YES")
        if str(params.get("fifteen_m_in_play_series") or "") != "KXBTC15M":
            raise FactoryOverlayError("15m in-play series is frozen KXBTC15M")
        if str(params.get("golf_foreign_sleeve") or "") != "slow":
            raise FactoryOverlayError("golf foreign sleeve is frozen slow")
        if str(params.get("golf_foreign_horizon") or "") != "season":
            raise FactoryOverlayError("golf foreign horizon is frozen season")


def load_library(*, root: Path | None = None) -> dict[str, Any]:
    path = library_path(root=root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FactoryOverlayError("FACTORY_OVERLAY.json must be an object")
    if payload.get("trading_armed") is True:
        raise FactoryOverlayError("factory overlay trading_armed must stay false")
    if payload.get("lab_admits") is True:
        raise FactoryOverlayError("factory overlay lab_admits must stay false")
    if payload.get("execution") is True:
        raise FactoryOverlayError("factory overlay execution must stay false")
    rows = list(payload.get("policies") or [])
    if not rows:
        raise FactoryOverlayError("FACTORY_OVERLAY.json has no policies")
    for index, row in enumerate(rows):
        _validate_row(row, index=index)
    ids = tuple(str(row.get("id") or "") for row in rows)
    if ids != FROZEN_IDS:
        raise FactoryOverlayError(f"file order must be {list(FROZEN_IDS)}; got {list(ids)}")
    queued = tuple(str(item) for item in (payload.get("queued_next") or []))
    if queued != QUEUED_NEXT:
        raise FactoryOverlayError(f"queued_next must be {list(QUEUED_NEXT)}; got {list(queued)}")
    return payload


def policy_ids(*, root: Path | None = None) -> tuple[str, ...]:
    payload = load_library(root=root)
    return tuple(str(row["id"]) for row in payload["policies"])


def policy_by_id(policy_id: str, *, root: Path | None = None) -> dict[str, Any]:
    payload = load_library(root=root)
    for row in payload["policies"]:
        if str(row.get("id") or "") == policy_id:
            return row
    raise FactoryOverlayError(f"{policy_id} is not in FACTORY_OVERLAY.json")
