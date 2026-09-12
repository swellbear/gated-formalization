"""Load the frozen P-* library. File order is the picker. Pnl does not rank."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.evidence_bar import class_is_burned
from golf_offshoot.repo_paths import repo_root

LIBRARY_REL = Path("golf-offshoot") / "docs" / "POLICY_FAMILY.json"
LESSONS_REL = Path("golf-offshoot") / "docs" / "P_FAMILY_LESSONS.json"
SCORE_REL = (
    Path("golf-offshoot") / "data" / "learning_lane_15m" / "latest" / "policy_family_score.json"
)
ALLOWED_SERIES = "KXBTC15M"
CATALOG_KIND = "P-FAMILY-SEARCH"
COMPARISON_ID = "P-FILL-ALL-YES"
REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
PICKER_REL = (
    Path("golf-offshoot") / "data" / "learning_lane_15m" / "latest" / "policy_family_picker.json"
)
FROZEN_IDS = (
    "P-FILL-ALL-YES",
    "P-SKIP-COINFLIP",
    "P-SKIP-RICH-075",
    "P-SKIP-WIDE-0400",
    "P-SKIP-LAST-SECONDS-60",
    "P-SKIP-INELIGIBLE-CLOSED",
)
#: Honer burned ids, copied so this package never imports honer_15m.
BURNED_HONER_IDS = frozenset(
    {
        "FLIP",
        "PERSIST",
        "SEAS-DIR",
        "SHRINK",
        "LOGIT",
        "RETUNE-COINFLIP-BAND",
        "FEE-AS-SIGNAL",
        "SUM-LINEAGES",
        "BACKFILL-GAP",
        "BASELINE-AS-EDGE",
    }
)


class PolicyFamilyError(ValueError):
    """Library is malformed, burned, or not the six frozen names."""


def library_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else repo_root()) / LIBRARY_REL


def lessons_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else repo_root()) / LESSONS_REL


def score_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else repo_root()) / SCORE_REL


def picker_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else repo_root()) / PICKER_REL


def registry_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else repo_root()) / REGISTRY_REL


def _as_upper(value: Any) -> str:
    return str(value or "").strip().upper()


def _is_burned(ident: str, *, root: Path | None = None) -> bool:
    token = str(ident or "").strip()
    if not token:
        return False
    if token in BURNED_HONER_IDS or token.upper() in BURNED_HONER_IDS:
        return True
    return class_is_burned(token, root=root)


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
    if "fill-no" in joined or "buy no" in joined or "buy-no" in joined:
        return True
    return False


def _validate_row(row: dict[str, Any], *, index: int, root: Path | None = None) -> None:
    if not isinstance(row, dict):
        raise PolicyFamilyError(f"policy {index} must be an object")
    ident = str(row.get("id") or "").strip()
    if not ident:
        raise PolicyFamilyError(f"policy {index} missing id")
    if _is_burned(ident, root=root):
        raise PolicyFamilyError(f"burned catalog id refused: {ident}")
    if _looks_like_fill_no(row):
        raise PolicyFamilyError(f"{ident} is fill-NO; zero fill-NO rows")
    params = row.get("params") or {}
    if not isinstance(params, dict):
        raise PolicyFamilyError(f"{ident} params must be an object")
    if "gamma" in params or params.get("gamma") is not None:
        raise PolicyFamilyError(f"{ident} names gamma; that is #200, not P-*")
    if params.get("missing_quotes") not in (None, "fill"):
        raise PolicyFamilyError(f"{ident} must fill missing quotes, not skip them")
    if ident == "P-SKIP-WIDE-0400" and str(params.get("missing_quotes") or "fill") != "fill":
        raise PolicyFamilyError("P-SKIP-WIDE-0400 missing bid/ask must fill YES")


def load_library(*, root: Path | None = None) -> dict[str, Any]:
    path = library_path(root=root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise PolicyFamilyError("POLICY_FAMILY.json must be an object")
    if payload.get("trading_armed") is True:
        raise PolicyFamilyError("policy family trading_armed must stay false")
    if payload.get("lab_admits") is True:
        raise PolicyFamilyError("policy family lab_admits must stay false")
    series = str(payload.get("series") or "")
    if series and series != ALLOWED_SERIES:
        raise PolicyFamilyError(f"v1 is {ALLOWED_SERIES} lineage A only; do not widen")
    rows = list(payload.get("policies") or [])
    if not rows:
        raise PolicyFamilyError("POLICY_FAMILY.json has no policies")
    for index, row in enumerate(rows):
        _validate_row(row, index=index, root=root)
    ids = tuple(str(row.get("id") or "") for row in rows)
    if ids != FROZEN_IDS:
        raise PolicyFamilyError(
            f"file order must be {list(FROZEN_IDS)}; got {list(ids)}"
        )
    return payload


def policy_ids(*, root: Path | None = None) -> tuple[str, ...]:
    payload = load_library(root=root)
    return tuple(str(row["id"]) for row in payload["policies"])


def policy_by_id(policy_id: str, *, root: Path | None = None) -> dict[str, Any]:
    payload = load_library(root=root)
    for row in payload["policies"]:
        if str(row.get("id") or "") == policy_id:
            return row
    raise PolicyFamilyError(f"{policy_id} is not in POLICY_FAMILY.json")
