"""Generic Honer search brains. Parallel family hunts. One exam chair.

Dating unused clip slots is the default process (farm I_farm_open analog).
The sidecar tick dates leftovers, then loops every brain. Not a Palshi button.
Dating is not a trial: factory k and Honer k stay put.
File order (catalog family, then clip) is the exam queue. No pnl.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any, Iterator

from golf_offshoot.honer_15m.paths import (
    assert_honer_path,
    brains_manifest_path,
    canonical_brain_id,
    reset_search_brain_id,
    search_brains_spec_path,
    search_book_root,
    set_search_brain_id,
)
from golf_offshoot.honer_15m.policy import (
    FAMILY_RICH,
    FAMILY_SPREAD,
    load_policy,
)
from golf_offshoot.localtime import now

CLIP_DECLARED_AT = "2026-09-12T12:00:00-04:00"
DEFER_QUOTES = "defer"


def clip_starts(*, lo: float, hi: float, step: float) -> tuple[float, ...]:
    """Inclusive clip lattice. Appends hi when it is not on the step grid. Not tape."""
    lo_i = int(round(float(lo) * 1000))
    hi_i = int(round(float(hi) * 1000))
    step_i = int(round(float(step) * 1000))
    if step_i <= 0:
        raise ValueError("clip step must be positive")
    vals = list(range(lo_i, hi_i + 1, step_i))
    if not vals or vals[-1] != hi_i:
        vals.append(hi_i)
    return tuple(v / 1000.0 for v in vals)


def brain_id_for(*, family: str, start: float, knob: str) -> str:
    cents = int(round(float(start) * 100))
    if str(family) == FAMILY_SPREAD or str(knob) == "delta":
        return f"f2-start-{cents:03d}"
    return f"f1-start-{cents:03d}"


def family1_start_thetas(policy: dict[str, Any] | None = None) -> tuple[float, ...]:
    pol = policy or load_policy()
    return clip_starts(lo=float(pol["theta_min"]), hi=float(pol["theta_max"]), step=float(pol["step"]))


def family2_start_deltas(policy: dict[str, Any] | None = None) -> tuple[float, ...]:
    pol = policy or load_policy()
    return clip_starts(
        lo=float(pol["delta_min"]),
        hi=float(pol["delta_max"]),
        step=float(pol["delta_step"]),
    )


def planned_brain_items(policy: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Catalog file order, then clip order. Predeclared. Not ranked by pnl."""
    pol = policy or load_policy()
    items: list[dict[str, Any]] = []
    for start in family1_start_thetas(pol):
        ident = brain_id_for(family=FAMILY_RICH, start=start, knob="theta")
        items.append(
            {
                "id": ident,
                "family": FAMILY_RICH,
                "knob": "theta",
                "start_theta": float(start),
                "start_delta": float(pol["start_delta"]),
                "catalog_advance": False,
                "declared_at": CLIP_DECLARED_AT,
            }
        )
    for start in family2_start_deltas(pol):
        ident = brain_id_for(family=FAMILY_SPREAD, start=start, knob="delta")
        items.append(
            {
                "id": ident,
                "family": FAMILY_SPREAD,
                "knob": "delta",
                "start_theta": float(pol["start_theta"]),
                "start_delta": float(start),
                "catalog_advance": False,
                "declared_at": CLIP_DECLARED_AT,
            }
        )
    return items


@contextmanager
def brain_scope(brain_id: str | None) -> Iterator[str | None]:
    token = set_search_brain_id(brain_id)
    try:
        yield brain_id
    finally:
        reset_search_brain_id(token)


def load_runtime_brains() -> dict[str, Any]:
    path = brains_manifest_path()
    if not path.is_file():
        return {"schema": 1, "lane": "honer_15m", "items": [], "k_unchanged": True}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"schema": 1, "lane": "honer_15m", "items": [], "k_unchanged": True}
    return payload if isinstance(payload, dict) else {"schema": 1, "items": []}


def iter_brain_ids() -> list[str]:
    """File-order exam queue. Empty runtime → canonical hunt only (undated tests)."""
    items = list(load_runtime_brains().get("items") or [])
    ids = [str(row["id"]) for row in items if isinstance(row, dict) and row.get("id")]
    if ids:
        return ids
    return [canonical_brain_id()]


def _ensure_brain_files(item: dict[str, Any]) -> None:
    from golf_offshoot.honer_15m.theta import default_state, load_theta, save_theta

    brain_id = str(item["id"])
    family = str(item.get("family") or FAMILY_RICH)
    with brain_scope(brain_id):
        root = search_book_root(brain_id)
        assert_honer_path(root)
        (root / "paper").mkdir(parents=True, exist_ok=True)
        path = None
        from golf_offshoot.honer_15m.paths import theta_path

        path = theta_path()
        if path.is_file():
            st = load_theta()
            st.setdefault("brain_id", brain_id)
            st.setdefault("start_theta", float(item.get("start_theta") or st.get("theta") or 0.75))
            st.setdefault("start_delta", float(item.get("start_delta") or st.get("delta") or 0.04))
            st.setdefault("catalog_advance", False)
            st.setdefault("active_family", family)
            save_theta(st)
            return
        state = default_state(
            start_theta=float(item["start_theta"]),
            start_delta=float(item["start_delta"]),
            active_family=family,
            brain_id=brain_id,
            catalog_advance=False,
        )
        save_theta(state)


def date_unused_clip_slots() -> dict[str, Any]:
    """Date every unused family-1 and family-2 clip slot in one fire.

    Does not increment Honer trials.json. Does not write factory RULES.json.
    Idempotent: existing clocks stay. Palshi does not have to press this.
    """
    from golf_offshoot.honer_15m.freeze import load_trials

    k_before = int(load_trials().get("trials_to_date") or 0)
    planned = planned_brain_items()
    runtime = load_runtime_brains()
    existing = {
        str(row["id"]): row
        for row in (runtime.get("items") or [])
        if isinstance(row, dict) and row.get("id")
    }
    created: list[str] = []
    ordered: list[dict[str, Any]] = []
    for item in planned:
        ident = str(item["id"])
        if ident not in existing:
            _ensure_brain_files(item)
            created.append(ident)
        else:
            _ensure_brain_files(item)
        ordered.append(item)
    payload = {
        "schema": 1,
        "lane": "honer_15m",
        "framing": (
            "Parallel family hunts. File order is the exam queue, not pnl. "
            "Dating is not a trial. One exam chair."
        ),
        "declared_at": CLIP_DECLARED_AT,
        "items": ordered,
        "created_this_fire": created,
        "k_unchanged": True,
        "updated_at": now().isoformat(),
    }
    path = brains_manifest_path()
    assert_honer_path(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    k_after = int(load_trials().get("trials_to_date") or 0)
    payload["trials_to_date"] = k_after
    payload["trials_unchanged"] = k_after == k_before
    return payload


def spec_matches_clip() -> bool:
    path = search_brains_spec_path()
    if not path.is_file():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    got = [str(row.get("id")) for row in (payload.get("items") or []) if isinstance(row, dict)]
    want = [row["id"] for row in planned_brain_items()]
    return got == want


def write_search_brains_spec() -> dict[str, Any]:
    """Photocopy of the clip menu into docs. Not tape. Not a trial."""
    items = planned_brain_items()
    payload = {
        "schema": 1,
        "lane": "honer_15m",
        "series": "KXBTC15M",
        "declared_at": CLIP_DECLARED_AT,
        "note": (
            "Dated clip menu. File order is the exam queue (family 1 then family 2, "
            "then clip). Not sorted by tape or pnl. Dating unused slots is not a trial. "
            "One exam chair. HOLD stands. Not a third family."
        ),
        "items": items,
    }
    path = search_brains_spec_path()
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def quotes_complete_for_spread(spread: float | None) -> bool:
    return spread is not None
