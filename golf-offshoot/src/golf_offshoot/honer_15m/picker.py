"""Short state-machine picker. No pnl inputs. No ranking from tape."""

from __future__ import annotations

from typing import Any

from golf_offshoot.honer_15m.catalog import next_family
from golf_offshoot.honer_15m.library import append_exam_row, last_unscored_seed_theta, load_library, save_library
from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD, load_policy
from golf_offshoot.honer_15m.quality import quote_quality_ok
from golf_offshoot.honer_15m.theta import load_theta, save_theta


def on_exam_close(*, outcome: str, family: str, knobs: dict[str, Any], k: int) -> dict[str, Any]:
    """Record a closed exam. `outcome` is a label. Do not pass pnl or d."""
    return append_exam_row(k=k, family=family, knobs=knobs, outcome=outcome)


def maybe_advance() -> dict[str, Any] | None:
    """Advance only on clip exhaustion. Does not read ledgers or exam d."""
    pol = load_policy()
    need = int(pol["clip_exhaust_windows"])
    st = load_theta()
    lib = load_library()
    if lib.get("catalog_exhausted"):
        return None
    if int(st.get("clip_streak") or 0) < need:
        return None
    active = str(st.get("active_family") or lib.get("active_family") or FAMILY_RICH)
    nxt = next_family(active)
    if nxt is None:
        lib["catalog_exhausted"] = True
        lib["active_family"] = active
        save_library(lib)
        return {"advanced": False, "catalog_exhausted": True, "active_family": active}
    if nxt == FAMILY_SPREAD and not quote_quality_ok():
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
    st["search_settled_since_freeze"] = 0
    st["in_band_settled"] = 0
    st["in_band_stable"] = 0
    st["far_settled_since_freeze"] = 0
    st["stable_windows"] = 0
    st["clip_streak"] = 0
    if nxt == FAMILY_SPREAD:
        start_delta = float(pol["start_delta"])
        st["delta"] = start_delta
        st["last_declared_delta"] = start_delta
    lib["active_family"] = nxt
    lib["seed_theta"] = float(seed)
    save_theta(st)
    save_library(lib)
    return {"advanced": True, "catalog_exhausted": False, "active_family": nxt, "seed_theta": float(seed)}
