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
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from golf_offshoot.localtime import isoformat_now, now as eastern_now

BAR_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
BURNED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_BURNED_CLASSES.json"

#: The public schedule ``k`` is cited from. A later schedule naming a different
#: k, or a KXBTC15M override, makes the RUN-ONLY note stale.
FEE_SCHEDULE_URL = "https://kalshi.com/docs/kalshi-fee-schedule.pdf"

#: Dotted path the score note must cite, and the path ``critic.py`` imports.
FEE_ADJUST_PATH = "golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust"

#: Gym PDF probe cooldown. Not every 90s tick. Not a Cursor/cloud retry.
FEE_PROBE_COOLDOWN_S = 12 * 3600
FEE_PROBE_UA = "gated-formalization/1.0 (public read-only)"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
FEE_PROBE_NAME = "fee_schedule_probe.json"
SERIES_FEE_NAME = "series_fee.json"


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


def fee_probe_path(*, latest_dir: Path | None = None) -> Path:
    from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

    dest = (latest_dir if latest_dir is not None else latest_dir_15m()) / FEE_PROBE_NAME
    from golf_offshoot.learning_lane_15m.paths import assert_not_golf_path

    assert_not_golf_path(dest)
    return dest


def series_fee_snapshot_path(*, root: Path | None = None, latest_dir: Path | None = None) -> Path:
    """Live gym snapshot. Tests may pass ``root`` or ``latest_dir``."""
    if latest_dir is not None:
        dest = latest_dir / SERIES_FEE_NAME
    elif root is not None:
        dest = (
            Path(root)
            / "golf-offshoot"
            / "data"
            / "learning_lane_15m"
            / "latest"
            / SERIES_FEE_NAME
        )
    else:
        from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

        dest = latest_dir_15m() / SERIES_FEE_NAME
    from golf_offshoot.learning_lane_15m.paths import assert_not_golf_path

    assert_not_golf_path(dest)
    return dest


def _parse_probe_time(text: str) -> datetime | None:
    raw = str(text or "").strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        when = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return when


def load_fee_schedule_probe(*, latest_dir: Path | None = None) -> dict[str, Any]:
    path = fee_probe_path(latest_dir=latest_dir)
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def fee_probe_due(
    *,
    latest_dir: Path | None = None,
    cooldown_s: float = FEE_PROBE_COOLDOWN_S,
    now: datetime | None = None,
) -> bool:
    """True when the gym should fetch the PDF. Missing probe file is due."""
    probe = load_fee_schedule_probe(latest_dir=latest_dir)
    checked = _parse_probe_time(str(probe.get("checked_at") or ""))
    if checked is None:
        return True
    clock = now if now is not None else eastern_now()
    age = (clock - checked).total_seconds()
    return age >= float(cooldown_s)


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
    request = urllib.request.Request(url, headers={"User-Agent": FEE_PROBE_UA})
    with urllib.request.urlopen(request, timeout=timeout_s) as response:  # noqa: S310
        return int(response.status), response.read()


def write_fee_schedule_probe(
    result: dict[str, Any],
    *,
    latest_dir: Path | None = None,
) -> Path:
    """Always write the attempt. A 429 does not amend the evidence bar."""
    dest = fee_probe_path(latest_dir=latest_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return dest


def pin_digest_from_probe(result: dict[str, Any]) -> str:
    """64-hex of a real 200 body, else empty. Never a placeholder."""
    if int(result.get("status") or 0) != 200:
        return ""
    digest = str(result.get("sha256") or "").strip().lower()
    if not _HEX64.match(digest):
        return ""
    return digest


def apply_fee_schedule_pin(
    result: dict[str, Any],
    *,
    root: Path | None = None,
) -> bool:
    """Write ``schedule_sha256`` onto the bar only when the digest is new.

    A 429, an empty body, or a non-hex digest leaves the bar bytes alone. A later
    429 does not clear a good hash. Returns True only when the bar file changed.
    """
    digest = pin_digest_from_probe(result)
    if not digest:
        return False
    path = bar_path(root=root)
    if not path.is_file():
        return False
    payload = json.loads(path.read_text(encoding="utf-8"))
    fee = payload.setdefault("fee_hurdle", {})
    current = str(fee.get("schedule_sha256") or "").strip().lower()
    if current == digest:
        return False
    if str(fee.get("schedule_pin_source") or "") == "founder_browser_bytes":
        # Gym 200 is drift detection. It does not replace Founder bytes.
        return False
    fee["schedule_sha256"] = digest
    fee["schedule_checked_at"] = result.get("checked_at") or isoformat_now()
    fee["schedule_fetch_status"] = 200
    fee["schedule_fetch_note"] = (
        result.get("error") or f"HTTP 200, {result.get('bytes')} bytes; gym PaperWatch pin"
    )
    fee["schedule_fetch_is_external"] = False
    fee["schedule_digest_kind"] = (
        "sha256 of the fetched bytes; the schedule is a PDF, so there is no "
        "newline normalisation on it — unlike the text artifacts critic.py hashes"
    )
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return True


FOUNDER_FEE_PDF_REL = Path("golf-offshoot") / "docs" / "kalshi-fee-schedule.pdf"
FOUNDER_FEE_PIN_SOURCE = "founder_browser_bytes"


def apply_founder_fee_pin(
    pdf_path: Path,
    *,
    root: Path | None = None,
    dest_rel: Path | None = None,
) -> dict[str, Any]:
    """Hash Founder-downloaded PDF bytes onto the bar. Not an HTTP 200 gym GET.

    A later gym 429 does not clear this digest. Gym probing stays on the 12h
    cooldown for drift detection only; it is not the pin clock.
    """
    src = Path(pdf_path)
    data = src.read_bytes()
    if not data.startswith(b"%PDF"):
        raise ValueError("founder fee pin is not a PDF")
    digest = hashlib.sha256(data).hexdigest()
    dest = (Path(root) if root is not None else _repo_root()) / (dest_rel or FOUNDER_FEE_PDF_REL)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    path = bar_path(root=root)
    if not path.is_file():
        raise FileNotFoundError(f"evidence bar missing at {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    fee = payload.setdefault("fee_hurdle", {})
    gym_status = fee.get("schedule_fetch_status")
    gym_checked = fee.get("schedule_checked_at")
    fee["schedule_sha256"] = digest
    fee["schedule_checked_at"] = isoformat_now()
    fee["schedule_pin_source"] = FOUNDER_FEE_PIN_SOURCE
    fee["schedule_bytes"] = len(data)
    fee["schedule_fetch_is_external"] = False
    fee["schedule_gym_last_status"] = gym_status
    fee["schedule_gym_last_checked_at"] = gym_checked
    fee["schedule_fetch_note"] = (
        f"Founder browser bytes, {len(data)} bytes, SHA-256 {digest}. "
        "Not an HTTP 200 gym GET. Gym 12h 429 is drift detection only, not the pin clock."
    )
    fee["schedule_hash_owed"] = (
        f"pinned from founder_browser_bytes SHA-256 {digest}. "
        "Gym 12h 429 is not the pin clock."
    )
    fee["schedule_digest_kind"] = (
        "sha256 of the Founder-downloaded PDF bytes; no newline normalisation"
    )
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return {
        "sha256": digest,
        "bytes": len(data),
        "dest": str(dest).replace("\\", "/"),
        "source": FOUNDER_FEE_PIN_SOURCE,
        "pinned": True,
    }


def record_fee_schedule_probe(
    probe: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
    latest_dir: Path | None = None,
    opener: Any = None,
) -> dict[str, Any]:
    """Write the probe file. Pin the bar only on a new 200 digest.

    A 429 is recorded on the probe file and does not amend the bar. That is
    the bite this split exists to stop: Cursor retries must not mint new bar
    hashes. ``schedule_sha256`` is set only from a real 200 body.
    """
    result = probe if probe is not None else probe_fee_schedule(opener=opener)
    write_fee_schedule_probe(result, latest_dir=latest_dir)
    pinned = apply_fee_schedule_pin(result, root=root)
    out = dict(result)
    out["pinned"] = pinned
    return out


def write_series_fee_snapshot(
    observed: dict[str, Any],
    *,
    latest_dir: Path | None = None,
    root: Path | None = None,
) -> Path:
    dest = series_fee_snapshot_path(root=root, latest_dir=latest_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "series": str(observed.get("series") or "KXBTC15M"),
        "fee_type": observed.get("fee_type"),
        "fee_multiplier": observed.get("fee_multiplier"),
        "fee_type_present": bool(observed.get("fee_type_present")),
        "fee_multiplier_present": bool(observed.get("fee_multiplier_present")),
        "written_at": isoformat_now(),
        "note": (
            "Ingested KXBTC15M series fee fields without defaulting a missing "
            "multiplier to 1. Not a pin of k=0.07. Not a dated fee-apply."
        ),
    }
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest


def load_series_fee_snapshot(*, root: Path | None = None, latest_dir: Path | None = None) -> dict[str, Any]:
    path = series_fee_snapshot_path(root=root, latest_dir=latest_dir)
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def gym_fee_tick(
    ingest: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
    latest_dir: Path | None = None,
    opener: Any = None,
    now: datetime | None = None,
    cooldown_s: float = FEE_PROBE_COOLDOWN_S,
    probe: bool = True,
) -> dict[str, Any]:
    """PaperWatch fee half: snapshot series M every cycle; PDF probe on cooldown.

    Does not fetch the PDF unless ``probe`` is true and the cooldown has
    elapsed. Does not invent a hash. Does not amend the bar on 429.
    """
    observed = (ingest or {}).get("series_fee") or {}
    snapshot_path = ""
    if observed:
        snapshot_path = str(
            write_series_fee_snapshot(observed, latest_dir=latest_dir, root=root)
        )
    out: dict[str, Any] = {
        "series_fee_snapshot": snapshot_path,
        "probed": False,
        "skipped_cooldown": False,
        "pinned": False,
        "status": None,
        "sha256": "",
        "error": "",
        "checked_at": "",
    }
    if not probe:
        return out
    if not fee_probe_due(latest_dir=latest_dir, cooldown_s=cooldown_s, now=now):
        out["skipped_cooldown"] = True
        last = load_fee_schedule_probe(latest_dir=latest_dir)
        out["status"] = last.get("status")
        out["sha256"] = last.get("sha256") or ""
        out["checked_at"] = last.get("checked_at") or ""
        out["error"] = last.get("error") or ""
        return out
    result = record_fee_schedule_probe(
        opener=opener, root=root, latest_dir=latest_dir
    )
    out["probed"] = True
    out["pinned"] = bool(result.get("pinned"))
    out["status"] = result.get("status")
    out["sha256"] = result.get("sha256") or ""
    out["checked_at"] = result.get("checked_at") or ""
    out["error"] = result.get("error") or ""
    return out
