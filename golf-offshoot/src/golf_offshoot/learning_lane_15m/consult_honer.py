"""AND-skip compositor for a dated honer consult.

Lives in the factory package. Reads ``latest/honer_consult.json`` only.
Never imports ``honer_15m``. Never reads ``honer_15m/latest/theta.json``.

Dark unless that snapshot exists and ``consult_enabled`` is exactly true.
Factory skip stays skip. Honer fill never forces a factory skip into a fill.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

SNAPSHOT_NAME = "honer_consult.json"
FAMILY_RICH = "H-SKIP-RICH-YES"
FAMILY_SPREAD = "H-SKIP-WIDE-SPREAD"


def consult_snapshot_path(*, root: Path | None = None) -> Path:
    base = Path(root) if root is not None else latest_dir_15m()
    return base / SNAPSHOT_NAME


def load_consult_snapshot(*, root: Path | None = None) -> dict[str, Any] | None:
    path = consult_snapshot_path(root=root)
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def consult_is_enabled(snapshot: dict[str, Any] | None) -> bool:
    return bool(snapshot) and snapshot.get("consult_enabled") is True


def market_spread(market: dict[str, Any] | None) -> float | None:
    if not market:
        return None
    try:
        bid = market.get("yes_bid")
        ask = market.get("yes_ask")
        if bid is None or ask is None:
            return None
        spread = float(ask) - float(bid)
    except (TypeError, ValueError):
        return None
    if spread < 0:
        return None
    return spread


def express_frozen_honer(
    snapshot: dict[str, Any],
    *,
    posted_yes: float,
    spread: float | None,
) -> tuple[str, str]:
    """Skip expression from frozen knobs. Mirrors honer families without importing them."""
    family = str(snapshot.get("family") or FAMILY_RICH)
    try:
        theta = float(snapshot.get("theta"))
    except (TypeError, ValueError) as exc:
        raise ValueError("honer consult snapshot is missing a numeric theta") from exc
    try:
        delta = float(snapshot.get("delta") or 0.0)
    except (TypeError, ValueError):
        delta = 0.0
    if family == FAMILY_SPREAD and spread is not None and float(spread) >= delta:
        return "skip", f"honer consult: spread {spread:g} >= delta {delta:g}"
    if float(posted_yes) >= theta:
        return "skip", f"honer consult: posted_yes >= theta {theta:g}"
    return "fill", f"honer consult: posted_yes below theta {theta:g}"


def compose_and_skip(
    factory_verdict: dict[str, Any],
    *,
    posted_yes: float,
    spread: float | None = None,
    root: Path | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """AND-skip. Dark path returns the factory verdict object unchanged."""
    snap = snapshot if snapshot is not None else load_consult_snapshot(root=root)
    if not consult_is_enabled(snap):
        return factory_verdict
    assert snap is not None
    action = str(factory_verdict.get("action") or "")
    if action != "fill":
        return factory_verdict
    try:
        honer_action, honer_reason = express_frozen_honer(
            snap, posted_yes=posted_yes, spread=spread
        )
    except ValueError:
        # Fail closed: an enabled snapshot without numeric theta / a usable
        # family expression must not crash paper. Flag stays off on this tree.
        return factory_verdict
    if honer_action != "skip":
        return factory_verdict
    out = dict(factory_verdict)
    out["action"] = "skip"
    out["reason"] = honer_reason
    out["consult"] = "honer_and_skip"
    return out


def _honer_latest() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "honer_15m" / "latest"


def _honer_bar_path() -> Path:
    return Path(__file__).resolve().parents[3] / "docs" / "HONER_15M_EVIDENCE_BAR.json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_honer_exam() -> dict[str, Any]:
    return _load_json(_honer_latest() / "exam.json")


def load_honer_exam_score() -> dict[str, Any]:
    return _load_json(_honer_latest() / "exam_score.json")


def freeze_hash(exam: dict[str, Any]) -> str:
    import hashlib

    blob = json.dumps(
        {
            "family": exam.get("frozen_family") or exam.get("family"),
            "theta": exam.get("frozen_theta") if exam.get("frozen_theta") is not None else exam.get("theta"),
            "delta": exam.get("frozen_delta") if exam.get("frozen_delta") is not None else exam.get("delta"),
            "declared_at": exam.get("declared_at"),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def knobs_from_exam(exam: dict[str, Any]) -> dict[str, Any]:
    family = str(exam.get("frozen_family") or exam.get("family") or FAMILY_RICH)
    try:
        theta = float(exam.get("frozen_theta") if exam.get("frozen_theta") is not None else exam.get("theta"))
    except (TypeError, ValueError):
        theta = None
    try:
        delta = float(exam.get("frozen_delta") if exam.get("frozen_delta") is not None else exam.get("delta") or 0.0)
    except (TypeError, ValueError):
        delta = 0.0
    return {
        "family": family,
        "theta": theta,
        "delta": delta,
        "declared_at": str(exam.get("declared_at") or ""),
        "freeze_hash": freeze_hash(exam),
    }


def snapshot_matches_freeze(snapshot: dict[str, Any] | None, exam: dict[str, Any]) -> bool:
    if not snapshot or not exam:
        return False
    knobs = knobs_from_exam(exam)
    if snapshot.get("family") != knobs["family"]:
        return False
    if str(snapshot.get("declared_at") or "") != knobs["declared_at"]:
        return False
    if knobs["theta"] is None:
        return False
    try:
        if abs(float(snapshot.get("theta")) - float(knobs["theta"])) > 1e-9:
            return False
    except (TypeError, ValueError):
        return False
    return str(snapshot.get("freeze_hash") or "") == knobs["freeze_hash"]


def write_consult_candidate(
    exam: dict[str, Any],
    *,
    dest: Path | None = None,
    consult_enabled: bool = False,
) -> dict[str, Any]:
    """Photocopy freeze knobs. Never copies live search theta. Flag defaults false."""
    knobs = knobs_from_exam(exam)
    if knobs["theta"] is None:
        raise ValueError("freeze exam is missing numeric theta")
    snap = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "source": "honer freeze photocopy",
        "family": knobs["family"],
        "theta": knobs["theta"],
        "delta": knobs["delta"],
        "declared_at": knobs["declared_at"],
        "freeze_hash": knobs["freeze_hash"],
        "consult_enabled": bool(consult_enabled) and consult_enabled is True,
        "live_theta_never_consults": True,
    }
    # Force exact-true only when caller passed True; never stringify.
    snap["consult_enabled"] = True if consult_enabled is True else False
    path = dest if dest is not None else consult_snapshot_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")
    return snap


def consult_enable_gates(
    *,
    exam: dict[str, Any] | None = None,
    score: dict[str, Any] | None = None,
    honer_bar: dict[str, Any] | None = None,
    snapshot: dict[str, Any] | None = None,
    invariants: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    exam = exam if exam is not None else load_honer_exam()
    score = score if score is not None else load_honer_exam_score()
    bar = honer_bar if honer_bar is not None else _load_json(_honer_bar_path())
    snap = snapshot if snapshot is not None else load_consult_snapshot()
    inv = invariants if invariants is not None else _load_json(_honer_latest() / "invariants.json")
    apply = bar.get("honer_fee_apply") if isinstance(bar.get("honer_fee_apply"), dict) else {}
    sha = str(apply.get("schedule_sha256") or "").strip().lower()
    outcome = str(score.get("outcome") or "")
    survives = score.get("survives") is True or outcome == "completed_unscored"
    gates = [
        {
            "id": "freeze_present",
            "ok": bool(exam.get("frozen_family") or exam.get("family"))
            and (exam.get("frozen_theta") is not None or exam.get("theta") is not None),
        },
        {
            "id": "fee_apply",
            "ok": bar.get("fee_omitted") is False and len(sha) == 64,
        },
        {
            "id": "exam_not_dead",
            "ok": bool(score) and survives and outcome not in {"parked", "completed_dead"},
        },
        {
            "id": "snapshot_is_freeze",
            "ok": snapshot_matches_freeze(snap, exam),
        },
        {
            "id": "honer_invariants",
            "ok": inv.get("passed") is True,
        },
        {
            "id": "not_live_theta",
            "ok": snap.get("live_theta_never_consults") is True if snap else False,
        },
    ]
    return gates


def maybe_sync_and_enable(*, dest: Path | None = None) -> dict[str, Any]:
    """Copy freeze to honer_consult.json. Enable only when every gate holds.

    Does not arm. Does not ADMIT. Does not read live theta.json.
    """
    exam = load_honer_exam()
    result: dict[str, Any] = {"wrote_candidate": False, "consult_enabled": False, "gates": []}
    if not exam:
        return result
    try:
        snap = write_consult_candidate(exam, dest=dest, consult_enabled=False)
    except ValueError:
        return result
    result["wrote_candidate"] = True
    gates = consult_enable_gates(exam=exam, snapshot=snap)
    result["gates"] = gates
    result["snapshot"] = snap
    if all(g.get("ok") for g in gates):
        snap = write_consult_candidate(exam, dest=dest, consult_enabled=True)
        result["consult_enabled"] = True
        result["snapshot"] = snap
    return result

