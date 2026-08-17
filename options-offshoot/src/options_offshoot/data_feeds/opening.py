"""Archive first prematch ask. Never relabel live as open."""

from __future__ import annotations

import json
from pathlib import Path

from options_offshoot.config import SNAPSHOT_DIR
from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.models.schemas import Contract, FieldRun


def snapshot_dir() -> Path:
    d = package_root() / SNAPSHOT_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def opening_path(field_id: str) -> Path:
    return snapshot_dir() / f"{field_id}_opening.json"


def last_run_path(field_id: str) -> Path:
    return snapshot_dir() / f"{field_id}_last.json"


def load_opening(field_id: str) -> dict[str, float]:
    path = opening_path(field_id)
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    out: dict[str, float] = {}
    for key, val in (raw or {}).items():
        try:
            px = float(val)
        except (TypeError, ValueError):
            continue
        if px > 0:
            out[str(key)] = px
    return out


def apply_opening(field_id: str, contracts: list[Contract]) -> dict[str, float]:
    stored = load_opening(field_id)
    changed = False
    for c in contracts:
        if c.contract_id in stored:
            c.opening_ask = stored[c.contract_id]
            continue
        ask = c.quote.ask
        if ask is not None and ask > 0:
            stored[c.contract_id] = float(ask)
            c.opening_ask = float(ask)
            changed = True
        else:
            c.opening_ask = None
    if changed:
        opening_path(field_id).write_text(json.dumps(stored, indent=2), encoding="utf-8")
    return stored


def save_last_run(run: FieldRun) -> Path:
    path = last_run_path(run.field_id)
    payload = {
        "field_id": run.field_id,
        "run_id": run.run_id,
        "n": len(run.rows),
        "n_ask": sum(1 for r in run.rows if r.contract.quote.has_real_ask and r.contract.liquid),
        "n_clear_ask": sum(1 for r in run.rows if r.clears_ask),
        "map_only": bool(run.extra.get("map_only")),
        "honest": run.honest,
        "extra": {
            k: v
            for k, v in run.extra.items()
            if k in ("law_hash", "expiry", "universe_n", "fetched_n", "quote_venue", "incomplete")
        },
    }
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def load_last_stats(field_id: str) -> dict | None:
    path = last_run_path(field_id)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
