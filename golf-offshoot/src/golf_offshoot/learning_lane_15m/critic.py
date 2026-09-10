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
import importlib
import inspect
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from statistics import NormalDist
from typing import Any, Callable, NamedTuple

from golf_offshoot.localtime import isoformat_now, now
from golf_offshoot.operator_surface.observability import repo_root

FINDINGS_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_CRITIC_FINDINGS.json"
BAR_MD_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.md"
BAR_JSON_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
PROPOSED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md"
PROPOSED_02_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md"
LAB_PROPOSED_02_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_LAB_PROPOSED_02.md"
DESK_REL = Path("docs") / "agents" / "DESK.md"
HUB_TASK_NAME = "GatedFormalization-15mLearningHub"

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
    Watched("lab_proposed_02", PROPOSED_02_REL, also_owes=("operator",)),
    Watched("lab_lab_proposed_02", LAB_PROPOSED_02_REL, also_owes=("operator",)),
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


def _as_dict(value: Any) -> dict[str, Any]:
    """A doctored bar can put a string where an object belongs. That is not a control."""
    return value if isinstance(value, dict) else {}


def _import_dotted(path: str) -> tuple[Callable[..., Any] | None, str]:
    """Resolve ``module.attr``. A name that does not import is not code."""
    text = str(path or "").strip()
    if "." not in text:
        return None, f"{text!r} is not a dotted path to a function"
    module_name, _, attr = text.rpartition(".")
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001 — an unimportable name is a failure
        return None, f"{module_name} does not import ({type(exc).__name__}: {exc})"
    fn = getattr(module, attr, None)
    if not callable(fn):
        return None, f"{text} is not callable"
    return fn, ""


def _source_calls(fn: Callable[..., Any] | None, needle: str) -> bool:
    """Does this function's own source reference that name?

    Static, on purpose. A control the score path *can* call is not the same as
    one it *must*; reading the scorer's source is how the difference is checked
    without executing a score.
    """
    if fn is None:
        return False
    try:
        return needle in inspect.getsource(fn)
    except (OSError, TypeError):
        return False


def _close(left: Any, right: Any, tol: float = 1e-3) -> bool:
    try:
        return abs(float(left) - float(right)) <= tol
    except (TypeError, ValueError):
        return False


def _null_bound(h0: str, delta: float) -> tuple[float, str]:
    """Which null the bar actually declares, and what it puts the bound at."""
    text = re.sub(r"\s+", "", str(h0 or "")).lower().replace("δ", "delta")
    if not text:
        return 0.0, "undeclared"
    if re.search(r"<=?0(\.0*)?$", text):
        return 0.0, "zero"
    if "delta" in text:
        return float(delta), "floor"
    return 0.0, "unrecognised"


def check_delta_above_detection_floor(*, root: Path | None = None) -> dict[str, Any]:
    """Recompute the design the bar actually specifies, under the null it declares.

    The drafted form measured δ against ``z * SE`` — the rejection threshold of a
    test against a *zero* null — and reported "delta is more than 10% above the
    floor" on a design whose null is ``mean(d) <= δ``, where power at δ is α by
    construction. That ratio can stay green at any n, forever, because both it
    and the scraped denominator move with the design while the null sits on top
    of δ.

    So: read ``distinguishable.h0``, say which null is being evaluated, and
    report the effects reached at 50% and 80% power from the same n, sd and
    α_k the test actually uses. The structured fields are read and must agree
    with the prose rationale — a bar that declares one sd in a sentence and
    another in a field can no longer be checked against whichever is flattering.
    """
    check_id = "delta_above_detection_floor"
    title = "the effect floor is checked against the null the bar declares"
    base = root or repo_root()
    bar = _load_json(base / BAR_JSON_REL)
    dist = _as_dict(bar.get("distinguishable"))
    looks = _as_dict(bar.get("looks"))
    power = _as_dict(dist.get("power"))
    delta = dist.get("effect_floor_usd_per_window")
    n = looks.get("first_look_n")
    h0 = str(dist.get("h0") or "")
    sd_declared = dist.get("sd_used")
    rationale = str(dist.get("effect_floor_rationale") or "")
    sd_match = re.search(r"sd\s*~?\s*([\d.]+)", rationale)
    if delta is None or not n or sd_declared is None:
        return _check(
            check_id, title, False,
            "cannot recompute the design: effect_floor_usd_per_window, "
            "looks.first_look_n or distinguishable.sd_used is missing",
            {"delta": delta, "n": n, "sd_used": sd_declared},
        )
    if not h0:
        return _check(
            check_id, title, False,
            "the bar declares no distinguishable.h0, so no check can know which "
            "null it is evaluating",
            {"delta": delta, "n": n},
        )
    bound, null_kind = _null_bound(h0, float(delta))
    if null_kind in {"undeclared", "unrecognised"}:
        return _check(
            check_id, title, False,
            f"h0 {h0!r} is not a form this check recognises; it will not guess a null",
            {"h0": h0},
        )

    registry = _load_json(base / REGISTRY_REL)
    trials = int(registry.get("trials_to_date") or 0)
    k = trials + 1
    alpha = 0.05 / (k * (k + 1))
    alpha_first_term = 0.05 / (1 * 2)
    normal = NormalDist()
    z_alpha = normal.inv_cdf(1.0 - alpha)
    sd = float(sd_declared)
    se = sd / (float(n) ** 0.5)
    mde = z_alpha * se
    threshold = bound + mde
    effect_50 = threshold
    effect_80 = threshold + normal.inv_cdf(0.80) * se
    ratio_zero_null = float(delta) / mde if mde else 0.0
    delta_over_threshold = float(delta) / threshold if threshold else 0.0

    disagreements: list[str] = []
    if sd_match and not _close(sd_match.group(1), sd, 1e-6):
        disagreements.append(
            f"prose rationale says sd {sd_match.group(1)} but sd_used is {sd}"
        )
    if not sd_match:
        disagreements.append("the prose rationale states no sd to cross-check sd_used against")
    for key, computed, declared in (
        ("se_at_n", se, dist.get("se_at_n")),
        ("mde", mde, dist.get("mde")),
        ("reject_if_mean_d_exceeds", threshold, dist.get("reject_if_mean_d_exceeds")),
        ("alpha_first_look", alpha_first_term, dist.get("alpha_first_look")),
        ("next_look_alpha", alpha, dist.get("next_look_alpha")),
        ("power.effect_at_50pct_power", effect_50, power.get("effect_at_50pct_power")),
        ("power.effect_at_80pct_power", effect_80, power.get("effect_at_80pct_power")),
    ):
        if declared is None:
            disagreements.append(f"the bar declares no {key}")
        elif not _close(declared, computed):
            disagreements.append(f"{key} says {declared}, recomputes to {computed:.4f}")
    if not power.get("disclosed_on_face"):
        disagreements.append("power is not disclosed on the bar's face")
    if ratio_zero_null <= 1.10:
        disagreements.append(
            f"delta {delta} is within 10% of the zero-null detection floor {mde:.4f}"
        )

    ok = not disagreements
    reading = (
        f"null is {null_kind} (h0 {h0!r}); at n={n}, sd={sd}, alpha_k={alpha:g} "
        f"(k={k}) the test rejects above {threshold:.4f}. delta {delta} is "
        f"{delta_over_threshold:.3f} of that threshold, so power at delta is alpha "
        f"by construction. 50% power at {effect_50:.4f}/window, 80% at "
        f"{effect_80:.4f}. Against a zero null the MDE would be {mde:.4f} "
        f"(ratio {ratio_zero_null:.3f}), which is not the null in force."
    )
    return _check(
        check_id, title, ok,
        reading if ok else reading + "  DISAGREEMENTS: " + "; ".join(disagreements),
        {
            "h0": h0,
            "null_kind": null_kind,
            "delta": delta,
            "n": n,
            "sd_used": sd,
            "alpha_k": alpha,
            "alpha_first_term": alpha_first_term,
            "trials_to_date": trials,
            "se": round(se, 6),
            "mde_zero_null": round(mde, 6),
            "reject_above": round(threshold, 6),
            "delta_over_reject_threshold": round(delta_over_threshold, 6),
            "delta_over_zero_null_mde": round(ratio_zero_null, 6),
            "effect_at_50pct_power": round(effect_50, 6),
            "effect_at_80pct_power": round(effect_80, 6),
            "disagreements": disagreements,
        },
    )


def check_matched_exposure(*, root: Path | None = None) -> dict[str, Any]:
    """Clause (5) has to be a function the score path calls, not a JSON object.

    If skipping contributes zero while the baseline fills, the contrast measures
    volume, not selection: when fill-all has negative EV, betting less wins
    automatically. A ``matched_exposure`` key describing a permutation is not
    that control — a dict admitting no control exists is truthy too.
    """
    check_id = "matched_exposure_control"
    title = "the matched-exposure control is code the scorer must call"
    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    dist = _as_dict(bar.get("distinguishable"))
    control = _as_dict(dist.get("matched_exposure"))
    declared_fn = str(control.get("control_function") or "")
    fn, why = _import_dotted(declared_fn)
    scorer, scorer_why = _import_dotted(
        "golf_offshoot.learning_lane_15m.rules.score_rule"
    )
    called = _source_calls(scorer, declared_fn.rpartition(".")[2]) if fn else False

    problems: list[str] = []
    if not declared_fn:
        problems.append(
            "distinguishable.matched_exposure names no control_function; a described "
            "permutation is not a permutation"
        )
    elif fn is None:
        problems.append(why)
    if scorer is None:
        problems.append(f"no score path to bind the control to: {scorer_why}")
    elif fn is not None and not called:
        problems.append(
            f"{declared_fn} exists but score_rule does not call it, so a scorecard "
            "could be produced without the control ever running"
        )
    seed, draws = control.get("seed"), control.get("draws")
    if fn is not None:
        from golf_offshoot.learning_lane_15m.rules import (
            MATCHED_EXPOSURE_DRAWS,
            MATCHED_EXPOSURE_SEED,
        )

        if seed != MATCHED_EXPOSURE_SEED:
            problems.append(f"bar pre-registers seed {seed}, code runs {MATCHED_EXPOSURE_SEED}")
        if draws is None or int(draws) < MATCHED_EXPOSURE_DRAWS:
            problems.append(
                f"bar declares {draws} draws, below the {MATCHED_EXPOSURE_DRAWS} the code requires"
            )
    ok = not problems
    return _check(
        check_id, title, ok,
        (
            f"{declared_fn} imports, holds the skip count fixed at seed {seed} over "
            f"{draws} draws, and score_rule calls it"
            if ok
            else "; ".join(problems)
        ),
        {
            "control_function": declared_fn,
            "function_exists": fn is not None,
            "score_path_calls_it": called,
            "seed": seed,
            "draws": draws,
            "contrast": str(dist.get("contrast") or ""),
            "skip_contributes": dist.get("skip_contributes"),
        },
    )


_FEE_ROW = re.compile(
    r"^\|\s*`?(\d{6})`?\s*\|\s*([\d.]+)\s*\|\s*([+\u2212-]?[\d.]+)\s*\|"
    r"\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([+\u2212-]?[\d.]+)\s*\|"
)


def run_only_fee_rows(*, root: Path | None = None) -> list[dict[str, float]]:
    """The RUN-ONLY note's own arithmetic table: mark, pnl, raw fee, ceil fee, adjusted."""
    path = (root or repo_root()) / PROPOSED_REL
    if not path.is_file():
        return []
    rows: list[dict[str, float]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = _FEE_ROW.match(line.strip())
        if not match:
            continue
        window, mark, pnl, raw, ceil_fee, adjusted = match.groups()
        rows.append(
            {
                "window": window,
                "mark": float(mark),
                "recorded_pnl": float(pnl.replace("\u2212", "-")),
                "raw_fee": float(raw),
                "fee": float(ceil_fee),
                "fee_adjusted_pnl": float(adjusted.replace("\u2212", "-")),
            }
        )
    return rows


def check_fee_adjusted_book(*, root: Path | None = None) -> dict[str, Any]:
    """``fee_adjust()`` must exist, reproduce the RUN-ONLY note, and be cited.

    The recorded book has no fee term: ``settle.py`` pays
    ``stake * decimal_odds``. The drafted check read ``"fee" in settle.py``,
    which is true only because ``data_feeds`` contains the letters — so the
    evidence block asserted a fee term the payout expression does not have. The
    fee term is now read off the payout expression itself, and the check passes
    on a tested function rather than on the substring ``fee_adj`` appearing in
    a free-text contrast.
    """
    check_id = "fee_adjusted_book_is_binding"
    title = "scoring runs on a fee-adjusted book, through committed code"
    base = root or repo_root()
    bar = _load_json(base / BAR_JSON_REL)
    fee = _as_dict(bar.get("fee_hurdle"))
    dist = _as_dict(bar.get("distinguishable"))
    contrast = str(dist.get("contrast") or "")
    declared_fn = str(fee.get("adjustment_function") or "")
    fn, why = _import_dotted(declared_fn)

    problems: list[str] = []
    if not declared_fn:
        problems.append("fee_hurdle.adjustment_function names no function")
    elif fn is None:
        problems.append(why)
    if not fee.get("score_note_must_cite_adjustment_function"):
        problems.append("the bar does not require the score note to cite that function")
    scorer, _ = _import_dotted("golf_offshoot.learning_lane_15m.rules.score_rule")
    if fn is not None and not _source_calls(scorer, declared_fn.rpartition(".")[2]):
        problems.append("score_rule does not call the declared adjustment function")

    rows = run_only_fee_rows(root=base)
    reproduced = 0
    if fn is None:
        problems.append("no adjustment function to check the RUN-ONLY table against")
    elif not rows:
        problems.append(
            f"could not read the fee table out of {PROPOSED_REL.as_posix()}; a check "
            "that cannot read its evidence is not a pass"
        )
    else:
        k = fee.get("k")
        for row in rows:
            try:
                got = fn(row["recorded_pnl"], row["mark"], 1.0, k=k)
            except Exception as exc:  # noqa: BLE001 — a raising adjustment is a failure
                problems.append(f"{declared_fn} raised on {row['window']}: {exc}")
                break
            if not _close(got, row["fee_adjusted_pnl"], 5e-3):
                problems.append(
                    f"{declared_fn} gives {got} on window {row['window']}, the "
                    f"RUN-ONLY note recorded {row['fee_adjusted_pnl']}"
                )
                break
            reproduced += 1

    settle = base / "golf-offshoot" / "src" / "golf_offshoot" / "learning_lane_15m" / "settle.py"
    body = settle.read_text(encoding="utf-8", errors="replace") if settle.is_file() else ""
    payout_lines = [
        line for line in body.splitlines()
        if re.search(r"^\s*(payout|pnl)\s*=", line)
    ]
    book_has_fee = any("fee" in line.lower() for line in payout_lines)

    ok = not problems
    return _check(
        check_id, title, ok,
        (
            f"{declared_fn} reproduces all {reproduced} rows of the RUN-ONLY fee "
            "table and score_rule calls it"
            if ok
            else "; ".join(problems)
        ),
        {
            "adjustment_function": declared_fn,
            "run_only_rows_reproduced": reproduced,
            "recorded_book_has_fee_term": book_has_fee,
            "payout_expressions": [line.strip() for line in payout_lines],
            "contrast": contrast,
            "measured_mean_per_fill_usd": fee.get("measured_mean_per_fill_usd"),
            "k": fee.get("k"),
        },
    )


def check_holdout_is_forward_only(*, root: Path | None = None) -> dict[str, Any]:
    """The holdout passes on an enforceable commit order, never on an adjective.

    ``forward_only: true`` was clearance on its own, so the substantive control
    could be deleted and the keyword kept. The control the bar actually
    specifies is commit order: the L1 score note is committed before the 71st
    eligible window closes, recording that SHA and timestamp. That is checkable,
    and this check requires the invariant that checks it to exist.
    """
    check_id = "holdout_is_forward_only"
    title = "the holdout is enforced by commit order, not by an adjective"
    base = root or repo_root()
    bar = _load_json(base / BAR_JSON_REL)
    looks = _as_dict(bar.get("looks"))
    held = str(looks.get("held_out_windows") or "")
    control = _as_dict(looks.get("commit_order_control"))
    invariant_id = str(control.get("invariant") or "")

    problems: list[str] = []
    if not invariant_id:
        problems.append(
            "looks.commit_order_control names no invariant; forward_only is an "
            "adjective and cannot be the control"
        )
    else:
        try:
            from golf_offshoot.learning_lane_15m.invariants import invariant_ids

            live = invariant_ids()
        except Exception as exc:  # noqa: BLE001 — a suite that cannot run is a failure
            live = []
            problems.append(f"cannot read the invariant suite ({type(exc).__name__}: {exc})")
        if live and invariant_id not in live:
            problems.append(
                f"{invariant_id} is named by the bar and is not in the invariant "
                f"suite ({', '.join(live)})"
            )
    if not control.get("requires_commit_sha") or not control.get("requires_committed_at"):
        problems.append(
            "the commit-order control does not require both a commit SHA and its "
            "timestamp on the score note"
        )
    by_index = bool(re.search(r"\b\d+\s*(through|to|-)\s*\d+\b", held))
    if by_index and not invariant_id:
        problems.append(
            f"held-out set is an index slice ({held!r}) with nothing enforcing that "
            "L1 was scored before the first L2 window closed"
        )
    ok = not problems
    return _check(
        check_id, title, ok,
        (
            f"held-out set {held!r} is enforced by invariant {invariant_id}, which "
            "requires the L1 score note's commit SHA and timestamp"
            if ok
            else "; ".join(problems)
        ),
        {
            "held_out_windows": held,
            "forward_only_keyword": looks.get("forward_only"),
            "keyword_is_not_clearance": True,
            "commit_order_invariant": invariant_id,
        },
    )


def _scorecards(*, root: Path | None = None) -> list[dict[str, Any]]:
    docs = (root or repo_root()) / "golf-offshoot" / "docs"
    if not docs.is_dir():
        return []
    return [
        _load_json(path) for path in sorted(docs.glob("LEARNING_LANE_15M_SCORECARD_*.json"))
    ]


def check_declared_at_precedes_scored_windows(*, root: Path | None = None) -> dict[str, Any]:
    """A rule may not be scored on a window that closed before it existed.

    Reads the scorecards as well as the registry. Keying only on a
    ``scored_windows`` field no writer exists for made this a green light with
    a docstring: the failure condition needed data nothing produced.
    """
    base = root or repo_root()
    registry = _load_json(base / REGISTRY_REL)
    declared_by_rule = {
        str(r.get("id") or ""): str(r.get("declared_at") or "")
        for r in registry.get("rules") or []
    }
    bad = []
    for rule in registry.get("rules") or []:
        declared = str(rule.get("declared_at") or "")
        for row in rule.get("scored_windows") or []:
            close = str((row or {}).get("close_at") or "")
            if declared and close and close <= declared:
                bad.append({"rule": rule.get("id"), "declared_at": declared, "close_at": close})
    cards = _scorecards(root=base)
    for card in cards:
        rule_id = str(card.get("rule_id") or "")
        declared = declared_by_rule.get(rule_id, "")
        for row in card.get("windows") or []:
            close = str((row or {}).get("close_at") or "")
            if declared and close and close <= declared:
                bad.append(
                    {"rule": rule_id, "declared_at": declared, "close_at": close,
                     "source": "scorecard"}
                )
    return _check(
        "declared_at_precedes_scored_windows",
        "no rule is scored on a window that predates its declaration",
        not bad,
        (
            f"no scored window in {len(cards)} scorecard(s) or the registry closes at "
            "or before its rule's declared_at"
            if not bad
            else f"{len(bad)} scored window(s) close at or before the rule's declared_at"
        ),
        {"violations": bad, "scorecards": len(cards)},
    )


def check_trials_counter_is_consistent(*, root: Path | None = None) -> dict[str, Any]:
    """``trials_to_date`` drives alpha, so it fails closed while nothing writes it.

    The drafted form passed on ``0 >= 0`` and printed its own vacuity. Its
    failure condition required a field the bar itself said no writer existed
    for, and its failure text quoted an alpha schedule the bar had retired. Both
    are fixed: a mechanical writer must exist, the counter must equal what the
    log accounts for, and every score note must have a matching increment.
    """
    check_id = "trials_counter_is_consistent"
    title = "trials_to_date is mechanical and accounts for every look"
    base = root or repo_root()
    registry = _load_json(base / REGISTRY_REL)
    trials = registry.get("trials_to_date")
    log = registry.get("trials_log")
    before = registry.get("trials_before_mechanism")
    writer, why = _import_dotted("golf_offshoot.learning_lane_15m.rules.record_trial")

    problems: list[str] = []
    if writer is None:
        problems.append(f"no mechanical increment exists: {why}")
    if not isinstance(log, list):
        problems.append(
            "the registry carries no trials_log, so the counter is prose and alpha "
            "cannot be audited"
        )
    if trials is None:
        problems.append("the registry records no trials_to_date")
    if isinstance(log, list) and trials is not None:
        accounted = int(before or 0) + len(log)
        if int(trials) != accounted:
            problems.append(
                f"trials_to_date={trials} but {accounted} are accounted for "
                f"({before or 0} before the mechanism + {len(log)} logged); "
                "alpha_k = 0.05/(k(k+1)) would be computed off the wrong k"
            )
    logged = [row for row in (log or []) if isinstance(row, dict)]
    l2_logged = sum(1 for row in logged if row.get("kind") == "l2_look")
    cards = _scorecards(root=base)
    l2_cards = [c for c in cards if str(c.get("look") or "").upper() == "L2"]
    if len(l2_cards) > l2_logged:
        problems.append(
            f"{len(l2_cards)} L2 score note(s) exist against {l2_logged} logged L2 "
            "look(s); a confirmation look that does not increment is a free look"
        )
    ok = not problems
    return _check(
        check_id, title, ok,
        (
            f"trials_to_date={trials} equals {int(before or 0)} pre-mechanism + "
            f"{len(logged)} logged increment(s); {len(cards)} score note(s) all match"
            if ok
            else "; ".join(problems)
        ),
        {
            "trials_to_date": trials,
            "trials_before_mechanism": before,
            "logged": len(logged),
            "l2_logged": l2_logged,
            "score_notes": len(cards),
            "writer": "golf_offshoot.learning_lane_15m.rules.record_trial",
        },
    )


_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def check_fee_schedule_hash_recorded(*, root: Path | None = None) -> dict[str, Any]:
    """The public fee schedule must be pinned by a real digest, not by non-emptiness.

    ``bool(recorded)`` made the standing blocker on binding one keystroke from
    green: ``"not-a-hash"`` passed. Restraint held it, and restraint is not a
    mechanism. A 64-hex digest and a recorded check time are.
    """
    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    fee = _as_dict(bar.get("fee_hurdle"))
    recorded = str(fee.get("schedule_sha256") or "").strip().lower()
    checked_at = str(fee.get("schedule_checked_at") or "")
    status = fee.get("schedule_fetch_status")
    note = str(fee.get("schedule_fetch_note") or "")
    problems: list[str] = []
    if not recorded:
        problems.append(
            f"no sha256 recorded for {FEE_SCHEDULE_URL}; k={fee.get('k')} is being "
            "used on habit and a schedule change would be invisible"
        )
    elif not _HEX64.match(recorded):
        problems.append(f"schedule_sha256 {recorded!r} is not a 64-hex digest")
    if not checked_at:
        problems.append(
            "schedule_checked_at is empty, so the record cannot tell never-attempted "
            "from attempted-and-externally-blocked"
        )
    if problems and checked_at:
        problems.append(f"last fetch: HTTP {status} at {checked_at} ({note})")
    ok = not problems
    return _check(
        "fee_schedule_hash_recorded",
        "the public fee schedule is pinned by a real digest",
        ok,
        (
            f"schedule sha256 {recorded[:12]}… recorded, last checked {checked_at}"
            if ok
            else "; ".join(problems)
        ),
        {
            "url": FEE_SCHEDULE_URL,
            "sha256": recorded,
            "checked_at": checked_at,
            "fetch_status": status,
            "fetch_note": note,
            "blocker_is_external": bool(checked_at and not recorded),
            "k": fee.get("k"),
        },
    )


def check_series_fee_regime_matches(*, root: Path | None = None) -> dict[str, Any]:
    """Live KXBTC15M fee_type / M must match the bar. Does not pin k.

    ``fee_adjust`` still reads ``fee_hurdle.k``. A live multiplier other than
    the declared 1 fails this check; it does not retune k in the dark. No
    snapshot yet is a named silent half-pass so CI without a gym latest/ does
    not fail the suite.
    """
    from golf_offshoot.learning_lane_15m.evidence_bar import load_series_fee_snapshot

    bar = _load_json((root or repo_root()) / BAR_JSON_REL)
    fee = _as_dict(bar.get("fee_hurdle"))
    expected_type = str(fee.get("expected_fee_type") or "quadratic").strip()
    expected_m = fee.get("expected_fee_multiplier")
    try:
        expected_m_f = float(1 if expected_m is None else expected_m)
    except (TypeError, ValueError):
        expected_m_f = 1.0
    snap = load_series_fee_snapshot(root=root)
    if not snap:
        return _check(
            "series_fee_regime_matches",
            "ingested KXBTC15M fee_type and fee_multiplier match the bar",
            True,
            "snapshot_absent — PaperWatch has not written latest/series_fee.json; "
            "this half-pass is named on the bar and is not a pin of k=0.07",
            {
                "snapshot_absent": True,
                "expected_fee_type": expected_type,
                "expected_fee_multiplier": expected_m_f,
            },
        )
    problems: list[str] = []
    if not snap.get("fee_type_present"):
        problems.append("ingested series omitted fee_type")
    if not snap.get("fee_multiplier_present"):
        problems.append("ingested series omitted fee_multiplier")
    got_type = str(snap.get("fee_type") or "").strip()
    if snap.get("fee_type_present") and got_type != expected_type:
        problems.append(f"fee_type {got_type!r} != expected {expected_type!r}")
    got_m = snap.get("fee_multiplier")
    if snap.get("fee_multiplier_present"):
        try:
            got_m_f = float(got_m)
        except (TypeError, ValueError):
            problems.append(f"fee_multiplier {got_m!r} is not a number")
            got_m_f = None
        else:
            if abs(got_m_f - expected_m_f) > 1e-9:
                problems.append(
                    f"fee_multiplier {got_m_f} != expected {expected_m_f}; "
                    "fee_adjust still reads fee_hurdle.k and was not retuned"
                )
    ok = not problems
    return _check(
        "series_fee_regime_matches",
        "ingested KXBTC15M fee_type and fee_multiplier match the bar",
        ok,
        (
            f"ingested {got_type} x {got_m} matches expected {expected_type} x {expected_m_f}"
            if ok
            else "; ".join(problems)
        ),
        {
            "snapshot_absent": False,
            "expected_fee_type": expected_type,
            "expected_fee_multiplier": expected_m_f,
            "fee_type": snap.get("fee_type"),
            "fee_multiplier": snap.get("fee_multiplier"),
            "fee_type_present": snap.get("fee_type_present"),
            "fee_multiplier_present": snap.get("fee_multiplier_present"),
        },
    )


_FOUNDER_READ_ONCE_GATE = re.compile(r"\(3\)\s*Founder read-once")
_FOUNDER_READS_IT_ONCE = "Founder reads it once"


def check_bind_has_no_founder_read_once(*, root: Path | None = None) -> dict[str, Any]:
    """Bind is crew+machine. Founder acknowledgement is not a third condition.

    Founder 2026-09-09 dropped it: the crew wrote it into the 08:30 draft; it
    was not a Founder GO. Putting the id or the numbered gate back is a Hard
    NO. Arm and HOLD lift stay Founder. A sentence that says the stamp is
    dropped does not fail this check.
    """
    base = root or repo_root()
    bar = _load_json(base / BAR_JSON_REL)
    md_path = base / BAR_MD_REL
    try:
        md = md_path.read_text(encoding="utf-8")
    except OSError:
        md = ""
    problems: list[str] = []
    conditions = bar.get("binding_conditions")
    if isinstance(conditions, list):
        for row in conditions:
            if isinstance(row, dict) and row.get("id") == "founder_read_once":
                problems.append(
                    "binding_conditions includes id founder_read_once; "
                    "Founder 2026-09-09 dropped it as a bind condition"
                )
                break
    rule = str(bar.get("binding_rule") or "")
    if _FOUNDER_READ_ONCE_GATE.search(rule):
        problems.append(
            "binding_rule still requires a numbered Founder-acknowledgement "
            "gate; bind is (1) Critic+Operator and (2) critic-invariants only"
        )
    if _FOUNDER_READS_IT_ONCE in md:
        problems.append(
            "evidence bar markdown still names the dropped Founder-acknowledgement "
            "sentence as a bind gate"
        )
    ok = not problems
    return _check(
        "bind_has_no_founder_read_once",
        "the 15m bar does not make Founder acknowledgement a bind condition",
        ok,
        (
            "no founder_read_once bind condition; bind is Critic+Operator and critic-invariants"
            if ok
            else "; ".join(problems)
        ),
        {
            "forbidden_id": "founder_read_once",
        },
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


def check_half_spread_profile(*, root: Path | None = None) -> dict[str, Any]:
    """Unmeasured spread cannot silently return. The named artifact must exist."""
    from golf_offshoot.learning_lane_15m.spread_profile import PROFILE_REL, profile_path

    check_id = "half_spread_profile_recorded"
    title = "the empirical half-spread profile is measured and named"
    base = root or repo_root()
    path = profile_path(root=root)
    payload = _load_json(path)
    n = int(payload.get("n") or 0)
    buckets = payload.get("buckets") if isinstance(payload.get("buckets"), list) else []
    bar = _load_json(base / BAR_JSON_REL)
    md_path = base / BAR_MD_REL
    try:
        md = md_path.read_text(encoding="utf-8")
    except OSError:
        md = ""
    named = (
        PROFILE_REL.name in json.dumps(bar)
        or PROFILE_REL.name in md
        or "half_spread_profile" in json.dumps(bar)
    )
    problems: list[str] = []
    if n < 1:
        problems.append(
            "half-spread profile is missing or n=0; unmeasured spread cannot bind"
        )
    if not buckets and n >= 1:
        problems.append("profile has samples but no mark buckets")
    if not named:
        problems.append("the bar face does not name LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json")
    ok = not problems
    return _check(
        check_id,
        title,
        ok,
        (
            f"profile n={n}, {len(buckets)} buckets, named on the bar"
            if ok
            else "; ".join(problems)
        ),
        {
            "n": n,
            "buckets": len(buckets),
            "named_on_bar": named,
            "path": str(PROFILE_REL).replace("\\", "/"),
        },
    )


def query_hub_autostart_task() -> dict[str, Any]:
    """Does the Windows logon task exist? Non-Windows is not this gym."""
    if os.name != "nt":
        return {"platform": os.name, "present": None, "skipped": True, "name": HUB_TASK_NAME}
    try:
        proc = subprocess.run(
            ["schtasks", "/Query", "/TN", HUB_TASK_NAME],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "platform": os.name,
            "present": False,
            "skipped": False,
            "name": HUB_TASK_NAME,
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        "platform": os.name,
        "present": proc.returncode == 0,
        "skipped": False,
        "name": HUB_TASK_NAME,
        "returncode": proc.returncode,
    }


def check_hub_autostart_registered(*, root: Path | None = None) -> dict[str, Any]:
    """The gym hub must have a logon task. Scratch-tree critic runs skip schtasks."""
    check_id = "hub_autostart_registered"
    title = "the 15m hub logon task exists"
    if root is not None:
        return _check(
            check_id,
            title,
            True,
            "scratch-tree critic run; live Windows gym queries schtasks",
            {"skipped": True, "name": HUB_TASK_NAME},
        )
    probed = query_hub_autostart_task()
    if probed.get("skipped"):
        return _check(
            check_id,
            title,
            True,
            "not Windows; hub autostart is a Windows Scheduled Task",
            probed,
        )
    ok = bool(probed.get("present"))
    return _check(
        check_id,
        title,
        ok,
        (
            f"schtasks {HUB_TASK_NAME} is registered"
            if ok
            else f"schtasks {HUB_TASK_NAME} is not registered; overnight holes follow"
        ),
        probed,
    )


#: The method suite. Every member is a property of the bar, the registry or the
#: code they name. Nothing here reads a clock.
CHECKS = (
    check_matched_exposure,
    check_delta_above_detection_floor,
    check_holdout_is_forward_only,
    check_fee_adjusted_book,
    check_declared_at_precedes_scored_windows,
    check_trials_counter_is_consistent,
    check_fee_schedule_hash_recorded,
    check_series_fee_regime_matches,
    check_bind_has_no_founder_read_once,
    check_half_spread_profile,
    check_hub_autostart_registered,
)

#: Reported beside the method suite and deliberately outside it.
#: ``honesty_stamp_is_fresh`` is a property of ``DESK.md``, owned by CoS, and a
#: fifteen-minute desk timer is not a bar defect. Inside ``CHECKS`` it set
#: ``passed``, so it paged Operator about the bar every time CoS went quiet —
#: and its detail carried ``{int(age)}s old``, which moved the Critic's proof
#: token on every pass and let the role clear itself on a heartbeat.
DESK_CHECKS = (check_honesty_stamp_is_fresh,)


def bar_names_failing_check(check_id: str, *, root: Path | None = None) -> bool:
    """Does the bar's own face name this failing check, with a reason?

    Binding condition 2 has an "or" branch — *every failing check named on this
    bar's face with Operator's reason for binding anyway* — and it was exercised
    for ``fee_schedule_hash_recorded``. The machine could not see that, so it
    kept paging Operator about a failure Operator had already disclosed.
    """
    base = root or repo_root()
    needle = str(check_id or "").strip()
    if not needle:
        return False
    for rel in (BAR_MD_REL, BAR_JSON_REL):
        path = base / rel
        if not path.is_file():
            continue
        if needle in path.read_text(encoding="utf-8", errors="replace"):
            return True
    return False


def run_critic_invariants(*, root: Path | None = None) -> dict[str, Any]:
    """Mechanical half only. Objects to nothing; it reports what a file says."""
    checks = [fn(root=root) for fn in CHECKS]
    desk = [fn(root=root) for fn in DESK_CHECKS]
    digests = watched_digests(root=root)
    failing = [c["id"] for c in checks if c["state"] != PASS]
    named = [c for c in failing if bar_names_failing_check(c, root=root)]
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
        "failing_named_on_bar": named,
        "failing_not_named_on_bar": [c for c in failing if c not in named],
        "checks": checks,
        "desk_checks": desk,
        "desk_checks_are_outside_the_method_suite": (
            "These do not set passed and never owe Operator about the bar. A desk "
            "freshness timer is CoS's obligation, not a property of the bar."
        ),
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
    named = set(payload.get("failing_named_on_bar") or [])
    for check in checks:
        mark = "PASS" if check.get("state") == PASS else "FAIL"
        suffix = "  (named on the bar's face)" if check.get("id") in named else ""
        lines.append(f"  [{mark}] {check.get('id')}{suffix}")
        if check.get("state") != PASS:
            lines.append(f"         {check.get('detail')}")
    for check in payload.get("desk_checks") or []:
        mark = "PASS" if check.get("state") == PASS else "FAIL"
        lines.append(f"  [{mark}] {check.get('id')}  (desk, not the method suite)")
    return lines
