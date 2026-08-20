"""Model versioning, snapshots, and the decision journal.

Freeze exactly what the system believed: version, weights, data hash, outputs,
human overrides, and any bets the user recorded. No auto-bet writer exists.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from uuid import uuid4

from golf_offshoot.bayesian_engine.weights import complete_alpha, weight_hash
from golf_offshoot.localtime import filename_stamp
from golf_offshoot.config import MODEL_FAMILY, MODEL_VERSION
from golf_offshoot.models.enums import RunMode
from golf_offshoot.models.schemas import (
    AuditRecord,
    BetRecord,
    HumanOverride,
    ModelVersionRecord,
    PlayerOutput,
)


def config_hash(extra: dict | None = None) -> str:
    payload = {"version": MODEL_VERSION, "family": MODEL_FAMILY, "extra": extra or {}}
    raw = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def data_snapshot_hash(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def current_model_record(alpha: dict[str, float] | None = None) -> ModelVersionRecord:
    a = complete_alpha(alpha)
    return ModelVersionRecord(
        version_id=MODEL_VERSION,
        family=MODEL_FAMILY,
        weight_hash=weight_hash(a),
        config_hash=config_hash({"alpha": a}),
        notes="weights may be expert-initialized or a frozen calibration artifact",
    )


def new_run_id() -> str:
    return filename_stamp() + "-" + uuid4().hex[:8]


def build_audit(
    tournament_id: str,
    mode: RunMode,
    outputs: list[PlayerOutput],
    data_hash: str,
    overrides: list[HumanOverride] | None = None,
    bets: list[BetRecord] | None = None,
    previous_run_id: str | None = None,
    delta_notes: list[str] | None = None,
    alpha: dict[str, float] | None = None,
) -> AuditRecord:
    return AuditRecord(
        run_id=new_run_id(),
        tournament_id=tournament_id,
        mode=mode,
        model=current_model_record(alpha),
        data_snapshot_hash=data_hash,
        outputs=outputs,
        overrides=overrides or [],
        bets_placed=bets or [],
        previous_run_id=previous_run_id,
        delta_notes=delta_notes or [],
    )


def save_audit(record: AuditRecord, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record.run_id}.json"
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path


def load_audit(path: Path) -> AuditRecord:
    return AuditRecord.model_validate_json(path.read_text(encoding="utf-8"))


def latest_pre_audit(tournament_id: str, directory: Path | None = None) -> AuditRecord | None:
    """Most recent pre-tournament snapshot for this ESPN/event id. Not invented if missing."""
    from pydantic import ValidationError

    from golf_offshoot.data_feeds.http import package_data_dir

    d = directory or (package_data_dir() / "snapshots")
    if not d.exists():
        return None
    want = str(tournament_id or "")
    if not want:
        return None
    best: AuditRecord | None = None
    for path in d.glob("*.json"):
        try:
            rec = load_audit(path)
        except (OSError, ValueError, KeyError, TypeError, ValidationError):
            continue
        if str(rec.tournament_id) != want:
            continue
        if rec.mode != RunMode.PRE_TOURNAMENT:
            continue
        if best is None or rec.as_of > best.as_of:
            best = rec
    return best


def list_event_audits(
    tournament_id: str,
    directory: Path | None = None,
    *,
    skip_compare: bool = True,
) -> list[AuditRecord]:
    """Snapshots for one ESPN/event id, oldest first. Missing dir is empty, not invented."""
    from pydantic import ValidationError

    from golf_offshoot.data_feeds.http import package_data_dir

    d = directory or (package_data_dir() / "snapshots")
    if not d.exists():
        return []
    want = str(tournament_id or "")
    if not want:
        return []
    out: list[AuditRecord] = []
    for path in d.glob("*.json"):
        try:
            rec = load_audit(path)
        except (OSError, ValueError, KeyError, TypeError, ValidationError):
            continue
        if str(rec.tournament_id) != want:
            continue
        if skip_compare and rec.extra.get("compare_path"):
            continue
        out.append(rec)
    out.sort(key=lambda r: (r.as_of, r.run_id))
    return out


def latest_event_audit(
    tournament_id: str,
    directory: Path | None = None,
    *,
    prefer_live: bool = True,
) -> AuditRecord | None:
    """Newest snapshot for this event. Live beats a stale pre-tournament ingest."""
    audits = list_event_audits(tournament_id, directory)
    if not audits:
        return None
    if prefer_live:
        lives = [a for a in audits if a.mode == RunMode.LIVE]
        if lives:
            return lives[-1]
    return audits[-1]


def diff_runs(previous: AuditRecord, current: AuditRecord) -> list[str]:
    from golf_offshoot.models.enums import Horizon

    notes: list[str] = []

    prev_map = {o.player_id: o.probabilities.p(Horizon.WIN).central for o in previous.outputs}
    cur_map = {o.player_id: o.probabilities.p(Horizon.WIN).central for o in current.outputs}
    for pid, p_now in cur_map.items():
        p_old = prev_map.get(pid)
        if p_old is None:
            notes.append(f"{pid}: new in field")
            continue
        d = p_now - p_old
        if abs(d) >= 0.01:
            notes.append(f"{pid}: win {p_old:.3f} → {p_now:.3f} ({d:+.3f})")
    return notes
