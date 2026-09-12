"""Short state-machine picker. No pnl inputs. No ranking from tape."""

from __future__ import annotations

from typing import Any

from golf_offshoot.honer_15m.catalog import next_family
from golf_offshoot.honer_15m.library import (
    append_exam_row,
    append_search_untestable,
    load_library,
)
from golf_offshoot.honer_15m.policy import (
    FAMILY_RICH,
    FAMILY_SPREAD,
    load_policy,
    starvation_untestable,
)
from golf_offshoot.honer_15m.theta import _reset_freeze_clocks, current_vector, load_theta, save_theta


def on_exam_close(*, outcome: str, family: str, knobs: dict[str, Any], k: int) -> dict[str, Any]:
    """Record a closed exam. `outcome` is a label. Do not pass pnl or d."""
    return append_exam_row(k=k, family=family, knobs=knobs, outcome=outcome)


def iter_exam_queue() -> list[str]:
    """File-order brain ids. Catalog family then clip. Not pnl."""
    from golf_offshoot.honer_15m.brains import iter_brain_ids

    return list(iter_brain_ids())


def next_freeze_brain() -> str | None:
    """First freeze-ready hunt in file order. One exam chair. No pnl."""
    from golf_offshoot.honer_15m.brains import brain_scope
    from golf_offshoot.honer_15m.freeze import exam_is_open, freeze_ready

    if exam_is_open():
        return None
    for brain_id in iter_exam_queue():
        with brain_scope(brain_id):
            if freeze_ready(load_theta()):
                return brain_id
    return None


def queue_status() -> dict[str, Any]:
    """File-order exam-queue clocks. No pnl. Not a ranking by closeness."""
    from golf_offshoot.honer_15m.brains import brain_scope, iter_brain_ids
    from golf_offshoot.honer_15m.freeze import exam_is_open, freeze_ready, load_exam_state
    from golf_offshoot.honer_15m.paths import canonical_brain_id

    exam = load_exam_state()
    ids = list(iter_brain_ids())
    ready: list[str] = []
    head_id: str | None = None
    head_state: dict[str, Any] = {}
    for brain_id in ids:
        with brain_scope(brain_id):
            st = dict(load_theta())
            if head_id is None:
                head_id = brain_id
                head_state = st
            if freeze_ready(st):
                ready.append(brain_id)
    return {
        "n_hunts": len(ids),
        "ready_ids": ready,
        "n_ready": len(ready),
        "next_ready": ready[0] if ready else None,
        "exam_open": exam_is_open(),
        "exam_brain_id": str(exam.get("brain_id") or "") if exam_is_open() else "",
        "head_id": head_id or canonical_brain_id(),
        "head_state": head_state,
    }


def maybe_advance() -> dict[str, Any] | None:
    """Families hunt in parallel. Sequential family-2 start is retired.

    Clip/starvation does not switch a family-1 hunt onto family 2.
    A third family is still not this build. Does not read ledgers or exam d.
    """
    lib = load_library()
    if lib.get("catalog_exhausted"):
        return None
    nxt = next_family(FAMILY_SPREAD)
    if nxt is None:
        return {
            "advanced": False,
            "parallel_families": True,
            "catalog_exhausted": False,
            "third_family": False,
        }
    return {"advanced": False, "parallel_families": True, "catalog_exhausted": False}


def apply_search_starvation() -> dict[str, Any] | None:
    """Honer search-reachability look. Not an exam. Does not increment k. No pnl.

    Does not start family 2 (already hunting in parallel).
    """
    from golf_offshoot.honer_15m.freeze import exam_is_open, load_trials

    pol = load_policy()
    st = load_theta()
    lib = load_library()
    if lib.get("catalog_exhausted"):
        return None
    pending = bool(st.get("starvation_pending"))
    n = int(st.get("search_settled_since_freeze") or 0)
    in_band = int(st.get("in_band_settled") or 0)
    if not pending and not starvation_untestable(n=n, in_band=in_band, policy=pol):
        return None
    if exam_is_open():
        st["starvation_pending"] = True
        save_theta(st)
        return {"deferred": True, "reason": "exam_open"}
    need_clip = int(pol["clip_exhaust_windows"])
    if int(st.get("clip_streak") or 0) >= need_clip:
        st["starvation_pending"] = False
        save_theta(st)
        return {"skipped": True, "reason": "clip_wins"}
    family = str(st.get("active_family") or FAMILY_RICH)
    append_search_untestable(family=family, knobs=current_vector(st))
    counts = dict(st.get("family_starvations") or {})
    counts[family] = int(counts.get(family) or 0) + 1
    st["family_starvations"] = counts
    st["starvation_pending"] = False
    k_before = int(load_trials().get("trials_to_date") or 0)
    start_theta = float(st.get("start_theta") or pol["start_theta"])
    start_delta = float(st.get("start_delta") or pol["start_delta"])
    if family == FAMILY_SPREAD:
        st["delta"] = start_delta
        st["last_declared_delta"] = start_delta
    else:
        st["theta"] = start_theta
        st["last_declared_theta"] = start_theta
    _reset_freeze_clocks(st)
    st["advance_owed"] = ""
    save_theta(st)
    k_after = int(load_trials().get("trials_to_date") or 0)
    return {
        "starved": True,
        "reset": True,
        "advanced": False,
        "parallel_families": True,
        "family": family,
        "starvations": counts[family],
        "trials_to_date": k_after,
        "trials_unchanged": k_after == k_before,
    }
