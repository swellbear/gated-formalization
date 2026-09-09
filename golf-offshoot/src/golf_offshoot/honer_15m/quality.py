"""Search-book quote completeness. Not factory money. Not a keep."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.books import load_decisions
from golf_offshoot.honer_15m.paths import assert_honer_path, quote_quality_path
from golf_offshoot.honer_15m.policy import load_policy
from golf_offshoot.localtime import now

WINDOW = 20


def _chronological(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: str(r.get("at") or r.get("ticker") or ""))


def measure(decisions: dict[str, Any] | None = None) -> dict[str, Any]:
    pol = load_policy()
    need = int(pol["clip_exhaust_windows"] or WINDOW)
    min_frac = float(pol["spread_quote_min_frac"])
    raw = decisions if decisions is not None else load_decisions("search")
    rows = [r for r in raw.values() if isinstance(r, dict)]
    window = _chronological(rows)[-need:]
    n = len(window)
    with_spread = sum(1 for r in window if r.get("spread") is not None)
    frac = (with_spread / n) if n else 0.0
    ok = n > 0 and frac >= min_frac
    return {
        "n": n,
        "window": need,
        "with_spread": with_spread,
        "frac": frac,
        "min_frac": min_frac,
        "ok": ok,
        "updated_at": now().isoformat(),
        "lane": "honer_15m",
    }


def save_quote_quality(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload if payload is not None else measure()
    path = quote_quality_path()
    assert_honer_path(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def quote_quality_ok(decisions: dict[str, Any] | None = None) -> bool:
    return bool(measure(decisions).get("ok"))
