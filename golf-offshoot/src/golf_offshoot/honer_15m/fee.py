"""Cite and apply the factory fee-schedule pin. A cite is not an apply."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from golf_offshoot.localtime import now

DOCS = Path(__file__).resolve().parents[3] / "docs"
FACTORY_BAR = DOCS / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
HONER_BAR = DOCS / "HONER_15M_EVIDENCE_BAR.json"
FEE_ADJUST_PATH = "golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust"
#: Factory ``founder_browser_bytes`` pin. A cite of a short or empty sha is not an apply.
FOUNDER_BROWSER_BYTES_PIN = (
    "c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601"
)
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def pin_is_64_hex(sha: str) -> bool:
    return bool(_SHA256_HEX.fullmatch(str(sha or "").strip().lower()))


def factory_schedule_sha256(*, bar_path: Path | None = None) -> str:
    """Read the factory pin from the bar JSON. Does not import the factory package."""
    path = bar_path if bar_path is not None else FACTORY_BAR
    if not path.is_file():
        return ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    if not isinstance(payload, dict):
        return ""
    fee = payload.get("fee_hurdle") or {}
    if not isinstance(fee, dict):
        return ""
    return str(fee.get("schedule_sha256") or "").strip().lower()


def cite_factory_pin(
    *,
    factory_bar: Path | None = None,
    honer_bar: Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    """Record the factory sha256 onto the honer bar. Does not clear ``fee_omitted``."""
    sha = factory_schedule_sha256(bar_path=factory_bar)
    cite = {
        "schedule_sha256": sha,
        "cited_at": now().isoformat(),
        "fee_omitted": True,
        "note": (
            "cite of factory schedule_sha256; not a dated honer fee-apply; "
            "keep-lock stays closed while fee_omitted"
            if sha
            else "factory pin empty; cannot apply; keep-lock stays closed"
        ),
    }
    if not write:
        return cite
    path = honer_bar if honer_bar is not None else HONER_BAR
    if not path.is_file():
        return cite
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return cite
    if not isinstance(payload, dict):
        return cite
    payload["factory_fee_cite"] = cite
    if payload.get("honer_fee_apply") is None:
        payload["fee_omitted"] = True
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return cite


def apply_factory_fee(
    *,
    factory_bar: Path | None = None,
    honer_bar: Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    """Dated honer fee-apply. Score-time ``fee_adjust``; does not rewrite ledgers.

    Clears ``fee_omitted`` only when the factory pin is a 64-hex sha. Keep-lock
    stays closed while the honer bar is unbound. This is not consult enable,
    not a keep, not an ADMIT, and not arm.
    """
    sha = factory_schedule_sha256(bar_path=factory_bar)
    usable = pin_is_64_hex(sha)
    path = honer_bar if honer_bar is not None else HONER_BAR
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            existing = {}
        if isinstance(existing, dict) and fee_is_applied(existing) and write:
            prior = existing.get("honer_fee_apply")
            if isinstance(prior, dict):
                return prior
    applied = {
        "applied_at": now().isoformat(),
        "schedule_sha256": sha,
        "fee_adjust": FEE_ADJUST_PATH,
        "applies_at": "score_time",
        "does_not_rewrite_search_ledgers": True,
        "pin_source": (
            "founder_browser_bytes" if sha == FOUNDER_BROWSER_BYTES_PIN else "factory_schedule_sha256"
        ),
        "fee_omitted": not usable,
        "note": (
            "dated honer fee-apply of factory founder_browser_bytes pin; "
            "score_time fee_adjust; search/exam ledgers stay gross"
            if usable
            else "factory pin is not a 64-hex sha; apply refused; fee_omitted stays true"
        ),
    }
    if not usable or not write:
        return applied
    cite = cite_factory_pin(factory_bar=factory_bar, honer_bar=honer_bar, write=write)
    if not path.is_file():
        return applied
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return applied
    if not isinstance(payload, dict):
        return applied
    payload["factory_fee_cite"] = dict(cite)
    payload["factory_fee_cite"]["fee_omitted"] = False
    payload["factory_fee_cite"]["note"] = "cite landed; dated honer fee-apply follows"
    payload["honer_fee_apply"] = applied
    payload["fee_omitted"] = False
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return applied


def fee_is_applied(bar: dict[str, Any] | None = None) -> bool:
    payload = bar if bar is not None else {}
    if not payload:
        from golf_offshoot.honer_15m.keep import load_bar

        payload = load_bar()
    apply = payload.get("honer_fee_apply") or {}
    if not isinstance(apply, dict):
        return False
    sha = str(apply.get("schedule_sha256") or "").strip().lower()
    return payload.get("fee_omitted") is False and pin_is_64_hex(sha)


def adjust_fill(
    recorded_pnl: float,
    posted_yes: float,
    stake: float,
    *,
    filled: bool = True,
) -> float:
    """Factory ``fee_adjust`` at score time. Lazy import keeps the wall except here."""
    from golf_offshoot.learning_lane_15m.evidence_bar import fee_adjust

    if not filled:
        return fee_adjust(recorded_pnl, posted_yes, stake, filled=False)
    return fee_adjust(recorded_pnl, posted_yes, stake, filled=True)
