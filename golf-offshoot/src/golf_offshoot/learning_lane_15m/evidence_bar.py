"""Load the 15m evidence bar and burned-class registry, and adjust for the fee.

Does not score a rule. Does not read window outcomes.

The fee adjustment lives here because the bar says it must: "A binding numeric
floor may not depend on a step with no code, no artifact and no check." Hand
arithmetic in a note is not the adjustment. :func:`fee_adjust` is the function
a score note has to cite, and ``critic.py`` fails
``fee_adjusted_book_is_binding`` unless it exists and reproduces the RUN-ONLY
note's raw-fee column.
"""

from __future__ import annotations

import hashlib
import json
import math
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from golf_offshoot.localtime import isoformat_now

BAR_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
BURNED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_BURNED_CLASSES.json"

#: The public schedule ``k`` is cited from. A later schedule naming a different
#: k, or a KXBTC15M override, makes the RUN-ONLY note stale.
FEE_SCHEDULE_URL = "https://kalshi.com/docs/kalshi-fee-schedule.pdf"

#: Dotted path the score note must cite, and the path ``critic.py`` imports.
FEE_ADJUST_PATH = "golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def bar_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else _repo_root()) / BAR_REL


def burned_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else _repo_root()) / BURNED_REL


def load_evidence_bar(*, root: Path | None = None) -> dict[str, Any]:
    payload = json.loads(bar_path(root=root).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("evidence bar must be an object")
    return payload


def load_burned_classes(*, root: Path | None = None) -> dict[str, Any]:
    payload = json.loads(burned_path(root=root).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("burned-class registry must be an object")
    return payload


def bar_is_binding(*, root: Path | None = None) -> bool:
    return bool(load_evidence_bar(root=root).get("binding"))


def class_is_burned(name: str, *, root: Path | None = None) -> bool:
    """True if name matches a burned id or alias. FRAGILE-not-null is not burned."""
    needle = str(name or "").strip()
    if not needle:
        return False
    payload = load_burned_classes(root=root)
    upper = needle.upper()
    for row in payload.get("classes") or []:
        if not row.get("burned"):
            continue
        cid = str(row.get("id") or "")
        aliases = [str(a) for a in (row.get("aliases") or [])]
        names = [cid, *aliases]
        if any(upper == n.upper() or upper.replace("_", "-") == n.upper().replace("_", "-") for n in names):
            return True
    return False


def fragile_not_null(name: str, *, root: Path | None = None) -> bool:
    needle = str(name or "").strip().upper()
    payload = load_burned_classes(root=root)
    for row in payload.get("fragile_not_null") or []:
        if str(row.get("id") or "").upper() == needle:
            return True
    return False


# ------------------------------------------------------------- fee adjustment


def fee_k(*, root: Path | None = None) -> float:
    """``k`` as the bar records it. Never a literal typed at a call site."""
    fee = load_evidence_bar(root=root).get("fee_hurdle") or {}
    value = fee.get("k")
    if value is None:
        raise ValueError("the evidence bar records no fee_hurdle.k")
    return float(value)


def ceil_cent(amount: float) -> float:
    """Round up to the cent, the rounding the RUN-ONLY note actually used.

    The PDF's centicent rule is noted there and deliberately not used, so the
    hurdle this prints is slightly worse than a finer rounding would give.
    """
    # round() first so 0.02065 * 100 does not arrive as 2.0649999999999995.
    return math.ceil(round(float(amount) * 100.0, 9)) / 100.0


def fee_raw(posted_yes: float, stake: float, *, k: float | None = None,
            root: Path | None = None) -> float:
    """``k * stake * (1 - posted_yes)`` — the un-rounded entry-side taker fee.

    Kalshi's ``k * C * P * (1 - P)`` with ``C = stake / P`` reduces exactly to
    this, which is why the fee is strictly decreasing in the mark.
    """
    rate = fee_k(root=root) if k is None else float(k)
    return rate * float(stake) * (1.0 - float(posted_yes))


def fee_for_fill(posted_yes: float, stake: float, *, k: float | None = None,
                 root: Path | None = None) -> float:
    """The charged fee: raw, then ceil to the cent. Entry side only."""
    return ceil_cent(fee_raw(posted_yes, stake, k=k, root=root))


def fee_adjust(
    recorded_pnl: float | None,
    posted_yes: float | None,
    stake: float | None,
    *,
    filled: bool = True,
    k: float | None = None,
    root: Path | None = None,
) -> float:
    """Recorded pnl minus the entry fee that book never charged.

    ``settle.py`` pays ``stake * decimal_odds`` with no fee term, so every
    ``settlement_pnl`` on this tree is optimistic by exactly this amount. A
    skip books no pnl and pays no fee, so it contributes 0 on both sides.

    This is the only adjustment the score note may cite. It is *not* a full
    cost accounting: the bid/ask spread is still omitted and unmeasured.
    """
    if not filled:
        return 0.0
    if recorded_pnl is None or posted_yes is None or stake is None:
        raise ValueError("fee_adjust needs recorded_pnl, posted_yes and stake on a fill")
    return round(float(recorded_pnl) - fee_for_fill(posted_yes, stake, k=k, root=root), 4)


# --------------------------------------------------------- fee schedule pin


def probe_fee_schedule(
    url: str = FEE_SCHEDULE_URL,
    *,
    timeout_s: float = 30.0,
    opener: Any = None,
) -> dict[str, Any]:
    """Fetch the public schedule and report what came back. Never invents a hash.

    A non-200, a transport error or an empty body leaves ``sha256`` empty. The
    status and the time are recorded either way, so the machine record can tell
    *never attempted* from *attempted and externally blocked* — which is the
    distinction that decides whether Operator is silent or stonewalled.
    """
    out: dict[str, Any] = {
        "url": url,
        "checked_at": isoformat_now(),
        "status": None,
        "sha256": "",
        "bytes": 0,
        "error": "",
    }
    fetch = opener or _urlopen
    try:
        status, body = fetch(url, timeout_s)
    except urllib.error.HTTPError as exc:
        out["status"] = int(exc.code)
        out["error"] = f"HTTP {exc.code} {exc.reason}"
        return out
    except Exception as exc:  # noqa: BLE001 — a failed probe is a recorded fact
        out["error"] = f"{type(exc).__name__}: {exc}"
        return out
    out["status"] = int(status)
    out["bytes"] = len(body or b"")
    if status == 200 and body:
        out["sha256"] = hashlib.sha256(body).hexdigest()
    elif not body:
        out["error"] = f"HTTP {status} with an empty body"
    return out


def _urlopen(url: str, timeout_s: float) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "gated-formalization/1.0 (public read-only)"}
    )
    with urllib.request.urlopen(request, timeout=timeout_s) as response:  # noqa: S310
        return int(response.status), response.read()


def record_fee_schedule_probe(
    probe: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
    opener: Any = None,
) -> dict[str, Any]:
    """Write the probe result onto the bar. A placeholder hash is not writable.

    ``schedule_sha256`` is set only from a real 200 body. On any other outcome
    it is left exactly as it was and the status is recorded beside it, which
    keeps ``fee_schedule_hash_recorded`` failing — correctly.
    """
    result = probe if probe is not None else probe_fee_schedule(opener=opener)
    path = bar_path(root=root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    fee = payload.setdefault("fee_hurdle", {})
    fee["schedule_checked_at"] = result.get("checked_at") or ""
    fee["schedule_fetch_status"] = result.get("status")
    fee["schedule_fetch_note"] = result.get("error") or (
        f"HTTP {result.get('status')}, {result.get('bytes')} bytes"
    )
    fee["schedule_fetch_is_external"] = not bool(result.get("sha256"))
    digest = str(result.get("sha256") or "")
    if digest:
        fee["schedule_sha256"] = digest
        fee["schedule_digest_kind"] = (
            "sha256 of the fetched bytes; the schedule is a PDF, so there is no "
            "newline normalisation on it — unlike the text artifacts critic.py hashes"
        )
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return result
