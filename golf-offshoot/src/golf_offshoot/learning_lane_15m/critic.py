"""The Critic's body: a repo-side event class and a deterministic checker.

The Critic had authority and no trigger. The wake only knew four market event
kinds, so a bar landing on master raised nothing, a rule reaching its n raised
nothing, and an invariant being added raised nothing. Nothing could name it.

Split, the same way Digestor was split:

* ``critic-invariants`` — this module. A deterministic checker over the
  method artifacts, with ``LEARNING_LANE_15M_CRITIC_FINDINGS.json`` as its
  proof artifact. Clerical, on the whitelist, cleared by serve-on-proof.
* ``soften-critic`` — the adversarial analysis turn. Stays in
  ``JUDICIAL_NEVER``. A written attack is not hash-provable.

The event class is: **a watched artifact's hash changed and no Critic finding
exists for that hash.** The findings file is keyed by content hash, so editing
a bar re-owes the Critic on the new text and cannot be cleared by editing
something else.

Checks here are the ratchet (Part 6): every flaw analysis finds becomes a
permanent check so it cannot recur silently. These are *method* checks. The
lane/process checks live in ``invariants.py``.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, NamedTuple

from golf_offshoot.localtime import isoformat_now, now
from golf_offshoot.operator_surface.observability import repo_root

FINDINGS_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_CRITIC_FINDINGS.json"
BAR_MD_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.md"
BAR_JSON_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
PROPOSED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md"
DESK_REL = Path("docs") / "agents" / "DESK.md"

#: The public schedule the fee hurdle is cited from. RUN-ONLY already requires
#: that a later schedule naming a different k or a KXBTC15M override makes the
#: note stale, so 0.07 must not be used by habit.
FEE_SCHEDULE_URL = "https://kalshi.com/docs/kalshi-fee-schedule.pdf"

PASS = "PASS"
FAIL = "FAIL"


class Watched(NamedTuple):
    id: str
    rel: Path
    #: Roles this artifact also owes when its hash is new. A Lab PROPOSED
    #: arriving is an Operator trigger as well as a Critic one.
    also_owes: tuple[str, ...] = ()
    #: Hash only this section of the file, so unrelated edits do not re-owe.
    section: str = ""


WATCHED: tuple[Watched, ...] = (
    Watched("evidence_bar", BAR_MD_REL),
    Watched("evidence_bar_json", BAR_JSON_REL),
    Watched("rule_registry", REGISTRY_REL),
    Watched("lab_proposed", PROPOSED_REL, also_owes=("operator",)),
    Watched("honesty_stamp", DESK_REL, section="## Honesty checklist"),
)


def findings_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / FINDINGS_REL


def _section_text(text: str, heading: str) -> str:
    out: list[str] = []
    grabbing = False
    for line in text.splitlines():
        if line.strip().lower().startswith(heading.lower()):
            grabbing = True
            out.append(line)
            continue
        if grabbing and line.strip().startswith("## "):
            break
        if grabbing:
            out.append(line)
    return "\n".join(out)


def artifact_digest(item: Watched, *, root: Path | None = None) -> dict[str, Any]:
    path = (root or repo_root()) / item.rel
    if not path.is_file():
        return {"id": item.id, "path": str(item.rel).replace("\\", "/"), "sha256": "", "present": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    if item.section:
        text = _section_text(text, item.section)
    return {
        "id": item.id,
        "path": str(item.rel).replace("\\", "/"),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "present": True,
    }


def watched_digests(*, root: Path | None = None) -> list[dict[str, Any]]:
    return [artifact_digest(item, root=root) for item in WATCHED]


def load_findings(*, root: Path | None = None) -> dict[str, Any]:
    path = findings_path(root=root)
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def reviewed_hashes(*, root: Path | None = None) -> set[str]:
    payload = load_findings(root=root)
    out: set[str] = set()
    for row in payload.get("reviewed") or []:
        digest = str((row or {}).get("sha256") or "")
        if digest:
            out.add(digest)
    return out


def unreviewed(*, root: Path | None = None) -> list[dict[str, Any]]:
    """Watched artifacts whose current hash carries no Critic finding."""
    seen = reviewed_hashes(root=root)
    rows = []
    for item, digest in zip(WATCHED, watched_digests(root=root)):
        if not digest.get("present") or digest["sha256"] in seen:
            continue
        rows.append({**digest, "also_owes": list(item.also_owes)})
    return rows


# ------------------------------------------------------------ ratchet checks


def _check(check_id: str, title: str, ok: bool, detail: str, evidence: Any = None) -> dict[str, Any]:
    return {
        "id": check_id,
        "title": title,
        "state": PASS if ok else FAIL,
        "detail": detail,
        "evidence": evidence if evidence is not None else {},
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def check_delta_above_detection_floor(*, root: Path | None = None) -> dict[str, Any]:
    """δ must not sit at the minimum detectable effect at the declared n.

    A bar whose effect floor equals its own MDE can only ever see its own
    detection floor: any rule that clears it clears it by being exactly as big
    as the smallest thing the test could have found.
    """
    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    dist = bar.get("distinguishable") or {}
    looks = bar.get("looks") or {}
    delta = dist.get("effect_floor_usd_per_window")
    n = looks.get("first_look_n")
    rationale = str(dist.get("effect_floor_rationale") or "")
    sd_match = re.search(r"sd\s*~?\s*([\d.]+)", rationale)
    crit_match = re.search(r"([\d.]+)\s*\*\s*SE", rationale)
    if delta is None or not n or not sd_match or not crit_match:
        return _check(
            "delta_above_detection_floor",
            "effect floor is not merely the detection floor",
            False,
            "cannot recompute the MDE from the bar: effect floor, n, sd or critical value missing",
            {"delta": delta, "n": n, "rationale": rationale},
        )
    sd = float(sd_match.group(1))
    crit = float(crit_match.group(1))
    mde = crit * sd / (float(n) ** 0.5)
    ratio = float(delta) / mde if mde else 0.0
    ok = ratio > 1.10
    return _check(
        "delta_above_detection_floor",
        "effect floor is not merely the detection floor",
        ok,
        (
            f"delta {delta} vs MDE {mde:.4f} at n={n} (ratio {ratio:.3f}). "
            + (
                "delta is more than 10% above the floor"
                if ok
                else "delta is within ~10% of the minimum detectable effect, so the "
                "bar can only see its own detection floor"
            )
        ),
        {"delta": delta, "mde": round(mde, 4), "ratio": round(ratio, 3), "n": n, "sd": sd},
    )


def check_matched_exposure(*, root: Path | None = None) -> dict[str, Any]:
    """A rule and its control must be compared at matched exposure.

    If skipping contributes zero while the baseline fills, the contrast
    measures volume, not selection: when fill-all has negative EV, betting less
    wins automatically.
    """
    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    dist = bar.get("distinguishable") or {}
    contrast = str(dist.get("contrast") or "")
    skip = dist.get("skip_contributes")
    per_bet = "per_bet" in contrast or "per-bet" in contrast
    declared = dist.get("matched_exposure")
    ok = bool(declared) or per_bet
    return _check(
        "matched_exposure_control",
        "rule and control are compared at matched exposure",
        ok,
        (
            "the bar declares a matched-exposure or per-bet contrast"
            if ok
            else (
                f"contrast is {contrast!r} with skip_contributes={skip}: a skipped "
                "window scores 0 against a baseline that filled, so the comparison "
                "rewards not playing rather than selecting"
            )
        ),
        {"contrast": contrast, "skip_contributes": skip, "matched_exposure": declared},
    )


def check_fee_adjusted_book(*, root: Path | None = None) -> dict[str, Any]:
    """A rule that only wins gross of fees is not admissible.

    ``settle.py`` pays ``stake * decimal_odds`` with no fee term while the
    RUN-ONLY note measured the missing entry-side taker fee, so the recorded
    book is fee-free. Scoring a fee thesis on it is incoherent.
    """
    base = root or repo_root()
    bar = _load_json(base / BAR_JSON_REL)
    fee = bar.get("fee_hurdle") or {}
    dist = bar.get("distinguishable") or {}
    contrast = str(dist.get("contrast") or "")
    settle = base / "golf-offshoot" / "src" / "golf_offshoot" / "learning_lane_15m" / "settle.py"
    body = settle.read_text(encoding="utf-8", errors="replace") if settle.is_file() else ""
    book_has_fee = "fee" in body.lower()
    binding = bool(fee.get("binding")) or "fee_adj" in contrast
    ok = binding
    return _check(
        "fee_adjusted_book_is_binding",
        "scoring runs on a fee-adjusted book",
        ok,
        (
            "the scored contrast is fee-adjusted"
            if ok
            else "the bar names a fee hurdle but does not bind scoring to a "
            "fee-adjusted contrast; the recorded book has no fee term"
        ),
        {
            "contrast": contrast,
            "recorded_book_has_fee_term": book_has_fee,
            "measured_mean_per_fill_usd": fee.get("measured_mean_per_fill_usd"),
            "k": fee.get("k"),
        },
    )


def check_holdout_is_forward_only(*, root: Path | None = None) -> dict[str, Any]:
    """A holdout separated only by index is not out of sample.

    L2 = "windows 41 through 80" is an index split inside one period and one
    regime. OOS has to be forward-only and pre-registered to mean anything.
    """
    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    looks = bar.get("looks") or {}
    held = str(looks.get("held_out_windows") or "")
    by_index = bool(re.search(r"\b\d+\s*(through|to|-)\s*\d+\b", held))
    regime = bool(looks.get("held_out_regime") or looks.get("forward_only"))
    ok = regime or not by_index
    return _check(
        "holdout_is_forward_only",
        "holdout is forward-only, not an index slice",
        ok,
        (
            "the holdout is declared forward-only"
            if ok
            else f"held-out set is an index slice ({held!r}) inside the same period "
            "and regime, which is not out of sample in any useful sense"
        ),
        {"held_out_windows": held, "forward_only": looks.get("forward_only")},
    )


def check_declared_at_precedes_scored_windows(*, root: Path | None = None) -> dict[str, Any]:
    """A rule may not be scored on a window that closed before it existed."""
    base = root or repo_root()
    registry = _load_json(base / REGISTRY_REL)
    bad = []
    for rule in registry.get("rules") or []:
        declared = str(rule.get("declared_at") or "")
        scored = rule.get("scored_windows") or []
        for row in scored:
            close = str((row or {}).get("close_at") or "")
            if declared and close and close <= declared:
                bad.append({"rule": rule.get("id"), "declared_at": declared, "close_at": close})
    return _check(
        "declared_at_precedes_scored_windows",
        "no rule is scored on a window that predates its declaration",
        not bad,
        (
            "no rule records a scored window at or before its declared_at"
            if not bad
            else f"{len(bad)} scored window(s) close at or before the rule's declared_at"
        ),
        {"violations": bad},
    )


def check_trials_counter_is_consistent(*, root: Path | None = None) -> dict[str, Any]:
    """``trials_to_date`` drives alpha. If it lags the register, alpha is wrong."""
    base = root or repo_root()
    registry = _load_json(base / REGISTRY_REL)
    trials = registry.get("trials_to_date")
    rules = registry.get("rules") or []
    looked = [r for r in rules if r.get("scored_windows") or r.get("last_look_at")]
    ok = trials is not None and int(trials) >= len(looked)
    return _check(
        "trials_counter_is_consistent",
        "trials_to_date is consistent with the register",
        ok,
        (
            f"trials_to_date={trials} covers {len(looked)} rule(s) that have been looked at"
            if ok
            else f"trials_to_date={trials} is below the {len(looked)} rule(s) already "
            "looked at, so alpha 0.05/(trials+1) is too generous"
        ),
        {"trials_to_date": trials, "rules": len(rules), "looked_at": len(looked)},
    )


def check_fee_schedule_hash_recorded(*, root: Path | None = None) -> dict[str, Any]:
    """The public fee schedule must be pinned by hash, not by habit.

    RUN-ONLY already says a later schedule naming a different ``k`` or a
    KXBTC15M override makes the note stale. Without a recorded hash nobody can
    tell whether that has happened, so 0.07 keeps getting reused.
    """
    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    fee = bar.get("fee_hurdle") or {}
    recorded = str(fee.get("schedule_sha256") or "")
    checked_at = str(fee.get("schedule_checked_at") or "")
    ok = bool(recorded)
    return _check(
        "fee_schedule_hash_recorded",
        "the public fee schedule is pinned by hash",
        ok,
        (
            f"schedule hash {recorded[:12]}… recorded, last checked {checked_at or 'unknown'}"
            if ok
            else f"no sha256 recorded for {FEE_SCHEDULE_URL}; k={fee.get('k')} is being "
            "used on habit and a schedule change would be invisible"
        ),
        {"url": FEE_SCHEDULE_URL, "sha256": recorded, "checked_at": checked_at, "k": fee.get("k")},
    )


def check_honesty_stamp_is_fresh(
    *,
    root: Path | None = None,
    window_s: float = 900.0,
) -> dict[str, Any]:
    """An honesty box may not be reported from a stamp older than one window."""
    base = root or repo_root()
    desk = base / DESK_REL
    text = desk.read_text(encoding="utf-8", errors="replace") if desk.is_file() else ""
    match = re.search(r"##\s*Honesty checklist.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", text)
    if not match:
        return _check(
            "honesty_stamp_is_fresh",
            "the honesty stamp is inside one window",
            False,
            "no dated honesty checklist heading on the desk",
            {},
        )
    stamped = f"{match.group(1)} {match.group(2)}"
    try:
        when = datetime.strptime(stamped, "%Y-%m-%d %H:%M").replace(tzinfo=now().tzinfo)
    except ValueError:
        return _check(
            "honesty_stamp_is_fresh",
            "the honesty stamp is inside one window",
            False,
            f"unparseable honesty stamp {stamped!r}",
            {},
        )
    age = (now() - when).total_seconds()
    ok = age <= window_s
    return _check(
        "honesty_stamp_is_fresh",
        "the honesty stamp is inside one window",
        ok,
        (
            f"stamped {stamped}, {int(age)}s old, inside one {int(window_s)}s window"
            if ok
            else f"stamped {stamped}, {int(age)}s old — older than one {int(window_s)}s "
            "window, so its boxes are being reported from a stale reading"
        ),
        {"stamped": stamped, "age_s": int(age), "window_s": window_s},
    )


CHECKS = (
    check_matched_exposure,
    check_delta_above_detection_floor,
    check_holdout_is_forward_only,
    check_fee_adjusted_book,
    check_declared_at_precedes_scored_windows,
    check_trials_counter_is_consistent,
    check_fee_schedule_hash_recorded,
    check_honesty_stamp_is_fresh,
)


def run_critic_invariants(*, root: Path | None = None) -> dict[str, Any]:
    """Mechanical half only. Objects to nothing; it reports what a file says."""
    checks = [fn(root=root) for fn in CHECKS]
    digests = watched_digests(root=root)
    failing = [c["id"] for c in checks if c["state"] != PASS]
    return {
        "schema": 1,
        "lane": "learning_lane_15m",
        "role": "critic-invariants",
        "ran_at": isoformat_now(),
        "framing": (
            "Deterministic checks over method artifacts. This is the mechanical "
            "half of the Critic. It objects to nothing, scores nothing, admits "
            "nothing and parks nothing. A written attack is soften-critic's turn "
            "and is never auto-served."
        ),
        "passed": not failing,
        "failing": failing,
        "checks": checks,
        "reviewed": [
            {**row, "checked_at": isoformat_now()} for row in digests if row.get("present")
        ],
    }


def write_critic_findings(
    payload: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
) -> Path:
    """The proof artifact. Serve-on-proof clears the role only when this moves."""
    report = payload if payload is not None else run_critic_invariants(root=root)
    dest = findings_path(root=root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    return dest


def format_critic(payload: dict[str, Any] | None) -> list[str]:
    if not payload:
        return ["critic invariants: not run on this tree yet"]
    checks = payload.get("checks") or []
    failing = [c for c in checks if c.get("state") != PASS]
    lines = [
        f"critic invariants ({len(checks)})  "
        f"{'ALL PASS' if not failing else str(len(failing)) + ' FAILING'}"
    ]
    for check in checks:
        mark = "PASS" if check.get("state") == PASS else "FAIL"
        lines.append(f"  [{mark}] {check.get('id')}")
        if check.get("state") != PASS:
            lines.append(f"         {check.get('detail')}")
    return lines
