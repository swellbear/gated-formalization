"""Short state-machine picker. No pnl inputs. No ranking from tape."""

from __future__ import annotations

from typing import Any

from golf_offshoot.honer_15m.catalog import next_family
from golf_offshoot.honer_15m.library import (
    append_exam_row,
    append_search_untestable,
    last_unscored_seed_theta,
    load_library,
    save_library,
)
from golf_offshoot.honer_15m.policy import (
    ADVANCE_OWED_STARVATION,
    FAMILY_RICH,
    FAMILY_SPREAD,
    load_policy,
    starvation_untestable,
)
from golf_offshoot.honer_15m.quality import quote_quality_ok
from golf_offshoot.honer_15m.theta import _reset_freeze_clocks, current_vector, load_theta, save_theta


def on_exam_close(*, outcome: str, family: str, knobs: dict[str, Any], k: int) -> dict[str, Any]:
    """Record a closed exam. `outcome` is a label. Do not pass pnl or d."""
    return append_exam_row(k=k, family=family, knobs=knobs, outcome=outcome)


def maybe_advance() -> dict[str, Any] | None:
    """Advance on clip exhaustion or an owed search-starvation gate. Does not read ledgers or exam d."""
    pol = load_policy()
    need = int(pol["clip_exhaust_windows"])
    st = load_theta()
    lib = load_library()
    if lib.get("catalog_exhausted"):
        return None
    clip_ready = int(st.get("clip_streak") or 0) >= need
    owed = str(st.get("advance_owed") or "") == ADVANCE_OWED_STARVATION
    if not clip_ready and not owed:
        return None
    active = str(st.get("active_family") or lib.get("active_family") or FAMILY_RICH)
    nxt = next_family(active)
    if nxt is None:
        lib["catalog_exhausted"] = True
        lib["active_family"] = active
        save_library(lib)
        st["advance_owed"] = ""
        st["starvation_pending"] = False
        save_theta(st)
        return {"advanced": False, "catalog_exhausted": True, "active_family": active}
    if nxt == FAMILY_SPREAD and not quote_quality_ok():
        if owed:
            st["advance_owed"] = ADVANCE_OWED_STARVATION
            save_theta(st)
        return {
            "advanced": False,
            "waiting_on_quotes": True,
            "catalog_exhausted": False,
            "active_family": active,
        }
    seed = last_unscored_seed_theta(lib)
    if seed is None:
        seed = float(st.get("theta") or pol["start_theta"])
    st["theta"] = float(seed)
    st["active_family"] = nxt
    _reset_freeze_clocks(st)
    st["advance_owed"] = ""
    st["starvation_pending"] = False
    if nxt == FAMILY_SPREAD:
        start_delta = float(pol["start_delta"])
        st["delta"] = start_delta
        st["last_declared_delta"] = start_delta
    lib["active_family"] = nxt
    lib["seed_theta"] = float(seed)
    save_theta(st)
    save_library(lib)
    return {"advanced": True, "catalog_exhausted": False, "active_family": nxt, "seed_theta": float(seed)}


def apply_search_starvation() -> dict[str, Any] | None:
    """Honer search-reachability look. Not an exam. Does not increment k. No pnl."""
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
    if counts[family] == 1:
        if family == FAMILY_SPREAD:
            start = float(pol["start_delta"])
            st["delta"] = start
            st["last_declared_delta"] = start
        else:
            start = float(pol["start_theta"])
            st["theta"] = start
            st["last_declared_theta"] = start
        _reset_freeze_clocks(st)
        save_theta(st)
        k_after = int(load_trials().get("trials_to_date") or 0)
        return {
            "starved": True,
            "reset": True,
            "advanced": False,
            "family": family,
            "starvations": counts[family],
            "trials_to_date": k_after,
            "trials_unchanged": k_after == k_before,
        }
    st["advance_owed"] = ADVANCE_OWED_STARVATION
    save_theta(st)
    out = maybe_advance() or {}
    k_after = int(load_trials().get("trials_to_date") or 0)
    return {
        "starved": True,
        "reset": False,
        "family": family,
        "starvations": counts[family],
        "trials_to_date": k_after,
        "trials_unchanged": k_after == k_before,
        **out,
    }
