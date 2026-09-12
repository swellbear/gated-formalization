"""Dated paper rules. A window that closed before declaration is not OOS.

Three things live here besides :func:`decide`, all of them owed by the bar:

* :func:`matched_exposure_permutation` — clause (5). The bar declares a
  permutation null at a fixed skip count and a pre-registered seed; a JSON
  object saying so is not the control, so the control is code and
  :func:`score_rule` cannot produce a scorecard without calling it.
* :func:`record_trial` — ``trials_to_date`` drives alpha and was prose. It now
  increments on the declaration of a selection rule and on an L2 look, in code,
  with a log an invariant can match score notes against.
* :func:`score_rule` — the scorer, with the bar's guards in front of it rather
  than in a comment. It refuses a non-binding bar, a failing method suite, and
  an n below the declared first look. Lived ``skip_count`` must also clear
  the same ``10/n`` density floor as declare; a miss is undecidable, not a
  clause-1 miss versus δ.
"""

from __future__ import annotations

import json
import math
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from golf_offshoot.learning_lane_15m.evidence_bar import fee_adjust
from golf_offshoot.localtime import isoformat_now, to_eastern

REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
SCORECARD_DIR_REL = Path("golf-offshoot") / "docs"
SCORECARD_GLOB = "LEARNING_LANE_15M_SCORECARD_*.json"

#: Clause (5), pre-registered on the bar's face. Named here so the check can
#: compare the bar's declaration against the code that would actually run.
MATCHED_EXPOSURE_SEED = 20260908
MATCHED_EXPOSURE_DRAWS = 10000

#: Dotted path the bar must cite for clause (5).
PERMUTATION_PATH = (
    "golf_offshoot.learning_lane_15m.rules.matched_exposure_permutation"
)


class RuleNotScorable(RuntimeError):
    """A guard in front of the scorer fired. Not a score, and not a failure."""


class RuleAlreadyInformed(ValueError):
    """A new selecting rule cannot be declared on a tree that already has marks."""


class RuleSkipRateUnnamed(ValueError):
    """A new selecting rule must name expected_skip_rate from product structure."""


class RuleTooSparse(ValueError):
    """A new selecting rule's product-structure skip rate is below the density floor."""


class RuleFillNone(ValueError):
    """AND-skip of three or four quartet minutes is not a skip-vs-fill look."""


#: Four 15m close minutes. The density floor is 10 / first_look_n, not a tape count.
QUARTET_CLOSE_MINUTES = frozenset({0, 15, 30, 45})
QUARTET_SLOT_COUNT = 4
MIN_EXPECTED_SKIP_COUNT = 10
DEFAULT_FIRST_LOOK_N = 70
FILL_NONE_QUARTET = (
    "fill-none: AND-skip of the whole quartet leaves no filled window"
)
FILL_NONE_TRIPLE = (
    "fill-none: AND-skip of a quartet triple leaves one filled window"
)


def registry_path(*, root: Path | None = None) -> Path:
    if root is not None:
        return Path(root) / REGISTRY_REL
    return Path(__file__).resolve().parents[4] / REGISTRY_REL


def load_rules(*, root: Path | None = None) -> dict[str, Any]:
    path = registry_path(root=root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("rule registry must be an object")
    return payload


def _as_dt(value: str) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"unparseable timestamp {value!r}") from exc
    return to_eastern(parsed)


def window_is_oos(rule: dict[str, Any], *, close_at: str) -> bool:
    """True only when the window closed strictly after the rule was declared.

    OOS is the expression gate for :func:`decide`. It is not the lived/replay
    label :func:`score_rule` uses. A window can be OOS and still be replay.
    """
    declared = _as_dt(str(rule.get("declared_at") or ""))
    closed = _as_dt(close_at)
    return closed > declared


def _replay_bounds(rule: dict[str, Any]) -> tuple[datetime, datetime] | None:
    """(after, at_or_before] if this row names a replay interval, else None.

    Prefer the explicit ``replay_close_*`` pair. If only
    ``lived_paper_begins_at`` is set, the interval is (declared_at, flip].
    """
    after = str(rule.get("replay_close_after") or "").strip()
    until = str(rule.get("replay_close_at_or_before") or "").strip()
    if after and until:
        return _as_dt(after), _as_dt(until)
    begins = str(rule.get("lived_paper_begins_at") or "").strip()
    declared = str(rule.get("declared_at") or "").strip()
    if begins and declared:
        return _as_dt(declared), _as_dt(begins)
    return None


def window_is_replay(rule: dict[str, Any], *, close_at: str) -> bool:
    """True when close is in the declared replay interval (after, at_or_before]."""
    bounds = _replay_bounds(rule)
    if bounds is None:
        return False
    after, until = bounds
    closed = _as_dt(close_at)
    return after < closed <= until


def window_is_lived(rule: dict[str, Any], *, close_at: str) -> bool:
    """True when the window is OOS and not in the declared replay interval.

    Rules that name no replay interval treat every OOS close as lived-for-score
    (L1 may still be a replay *mode* via ``execution=false``; that is the L2
    execution guard, not this clock).
    """
    if not window_is_oos(rule, close_at=close_at):
        return False
    return not window_is_replay(rule, close_at=close_at)


def favorite_threshold(odds: float) -> float:
    """posted_yes cutoff for an N-to-1 favorite: p = odds / (1 + odds)."""
    if float(odds) <= 0:
        raise ValueError("favorite_odds must be positive")
    return float(odds) / (1.0 + float(odds))


def close_minute(close_at: str) -> int:
    """Clock minute of a window close. Not a posted-yes mark."""
    return _as_dt(close_at).minute


def selects_on_posted_yes_cut(rule: dict[str, Any]) -> bool:
    """True when the free parameters are posted-yes cuts (skip-band family).

    A close-minute class is a new class, not another skip-band. The informing-
    marks gate refuses only the skip-band family.
    """
    params = rule.get("params") or {}
    expr = rule.get("expression") or {}
    skip_if = str(expr.get("skip_if") or "")
    if skip_if in {"close_minute_eq", "close_minute_in"}:
        return False
    if params.get("skip_close_minutes") is not None and params.get("favorite_odds") is None:
        return False
    if params.get("skip_close_minute") is not None and params.get("favorite_odds") is None:
        return False
    return True


def clock_skip_minutes(rule: dict[str, Any]) -> list[int] | None:
    """Named 15m close minutes this rule skips, or None if it is not a clock rule.

    Product structure only. Does not read ``paper/`` pnl.
    """
    params = rule.get("params") or {}
    expr = rule.get("expression") or {}
    skip_if = str(expr.get("skip_if") or "")
    if params.get("skip_close_minutes") is not None or skip_if == "close_minute_in":
        raw = params.get("skip_close_minutes")
        if raw is None:
            raw = expr.get("minutes") or expr.get("close_minutes")
        if raw is None:
            return []
        try:
            return [int(x) for x in raw]
        except (TypeError, ValueError):
            return []
    if params.get("skip_close_minute") is not None or skip_if == "close_minute_eq":
        raw = params.get("skip_close_minute")
        if raw is None:
            raw = expr.get("minute")
        if raw is None:
            return []
        try:
            return [int(raw)]
        except (TypeError, ValueError):
            return []
    return None


def expected_skip_rate(rule: dict[str, Any]) -> float | None:
    """Skip rate from the 15m clock quartet, or None when the rule cannot name one.

    A posted-yes cut cannot name this rate without the tape. Existing registry
    rows are grandfathered: this function is for new ``declare_rule`` calls.
    """
    if not rule.get("selects"):
        return None
    minutes = clock_skip_minutes(rule)
    if minutes is None:
        return None
    if not minutes:
        return 0.0
    unique: list[int] = []
    seen: set[int] = set()
    for minute in minutes:
        if minute not in seen:
            seen.add(minute)
            unique.append(minute)
    if any(minute not in QUARTET_CLOSE_MINUTES for minute in unique):
        return 0.0
    return len(unique) / float(QUARTET_SLOT_COUNT)


def min_expected_skip_rate(*, root: Path | None = None) -> float:
    """Hard refuse: ``10 / looks.first_look_n`` (~14% at n=70). Not 20/70."""
    n = DEFAULT_FIRST_LOOK_N
    try:
        from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar

        n = int(
            (load_evidence_bar(root=root).get("looks") or {}).get("first_look_n")
            or DEFAULT_FIRST_LOOK_N
        )
    except (OSError, ValueError, TypeError, KeyError):
        n = DEFAULT_FIRST_LOOK_N
    if n <= 0:
        n = DEFAULT_FIRST_LOOK_N
    return MIN_EXPECTED_SKIP_COUNT / float(n)


def clock_fill_none_reason(rule: dict[str, Any]) -> str:
    """Product-structure fill-none. Empty if two or more quartet minutes still fill.

    Hire #2 refused the full quartet (zero fill minutes). A leftover triple
    such as INTRA-HOUR ``{15, 30, 45}`` leaves one fill minute — the farm
    card can skip every window. Density language stays off this reason.
    """
    minutes = clock_skip_minutes(rule)
    if minutes is None:
        return ""
    skipped = {int(m) for m in minutes if int(m) in QUARTET_CLOSE_MINUTES}
    if skipped >= QUARTET_CLOSE_MINUTES:
        return FILL_NONE_QUARTET
    if len(skipped) >= 3:
        return FILL_NONE_TRIPLE
    return ""


def named_expected_skip_rate(rule: dict[str, Any]) -> float | None:
    """Product-structure rate, else a stored ``expected_skip_rate`` on the row."""
    rate = expected_skip_rate(rule)
    if rate is not None:
        return float(rate)
    raw = rule.get("expected_skip_rate")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def lived_skip_density(
    skip_count: int,
    n: int,
    *,
    expected_rate: float | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """Same ``10/n`` floor as declare, applied to lived ``skip_count``.

    A look that skips fewer than 10 of n, or that fills none of the n
    windows, is undecidable. Not a t-test versus δ.
    """
    skip_n = int(skip_count)
    total = int(n)
    floor_rate = min_expected_skip_rate(root=root)
    floor_count = MIN_EXPECTED_SKIP_COUNT
    reason = ""
    if total <= 0:
        reason = "no windows"
    elif skip_n >= total:
        reason = f"skip_count {skip_n}/{total} is fill-none; not a skip-vs-fill look"
    elif skip_n < floor_count:
        named = ""
        if expected_rate is not None:
            named = f" vs expected_skip_rate {expected_rate}"
        reason = (
            f"skip_count {skip_n}/{total} below density floor "
            f"{floor_count}/{total}{named}"
        )
    return {
        "skip_count": skip_n,
        "n": total,
        "expected_skip_rate": expected_rate,
        "floor_count": floor_count,
        "floor_rate": round(floor_rate, 6),
        "passes": not reason,
        "reason": reason,
        "undecidable": bool(reason),
    }


def _express_selection(
    rule: dict[str, Any],
    posted_yes: float,
    *,
    close_at: str = "",
) -> tuple[str, str]:
    """Fill-or-skip from declared parameters. Does not read the tape."""
    params = rule.get("params") or {}
    if params.get("skip_close_minutes") is not None:
        if not str(close_at or "").strip():
            return "unknown", f"no close_at for {rule.get('id')}"
        skip_set = {int(x) for x in params["skip_close_minutes"]}
        minute = close_minute(close_at)
        if minute in skip_set:
            return "skip", f"close_minute in {sorted(skip_set)} (civil walls)"
        return "fill", f"close_minute {minute} not in {sorted(skip_set)}"
    if params.get("skip_close_minute") is not None:
        if not str(close_at or "").strip():
            return "unknown", f"no close_at for {rule.get('id')}"
        skip_m = int(params["skip_close_minute"])
        minute = close_minute(close_at)
        if minute == skip_m:
            return "skip", f"close_minute == {skip_m} (hour-ending slot)"
        return "fill", f"close_minute {minute} != {skip_m}"
    if params.get("favorite_odds") is not None:
        odds = float(params["favorite_odds"])
        threshold = favorite_threshold(odds)
        if float(posted_yes) >= threshold:
            return "skip", f"posted_yes >= {odds:g}:1 favorite threshold {threshold}"
        return "fill", f"posted_yes below {odds:g}:1 favorite threshold"
    if str(rule.get("id") or "") == "R-SKIP-COINFLIP":
        if 0.45 < float(posted_yes) < 0.55:
            return "skip", "posted_yes inside (0.45, 0.55)"
        return "fill", "posted_yes outside coinflip band"
    return "unknown", f"no expression for {rule.get('id')}"


def decide(
    rule: dict[str, Any],
    *,
    posted_yes: float,
    close_at: str,
) -> dict[str, Any]:
    """Express a fill-or-skip. Does not place anything. Does not invent pnl."""
    kind = str(rule.get("kind") or "")
    selects = bool(rule.get("selects"))
    if kind == "baseline" or not selects:
        # Baseline is "fill what the loop hands you." OOS is a selection-rule
        # scoring constraint, not a reason to stop the observation book.
        eligible = True
        action = "fill"
        reason = "baseline fill at posted mark"
    elif not str(close_at or "").strip():
        # Open candidate, no close stamp yet. score_rule still requires one.
        eligible = True
        action = "unknown"
        reason = f"no expression for {rule.get('id')}"
    else:
        eligible = window_is_oos(rule, close_at=close_at)
        action = "ineligible"
        reason = "window closed at or before declared_at; not OOS for this rule"
    if eligible and selects:
        action, reason = _express_selection(rule, posted_yes, close_at=close_at)
    return {
        "rule_id": rule.get("id"),
        "eligible": eligible,
        "action": action,
        "reason": reason,
        "execution": bool(rule.get("execution")),
    }


def rule_by_id(rule_id: str, *, root: Path | None = None,
               registry: dict[str, Any] | None = None) -> dict[str, Any] | None:
    reg = registry if registry is not None else load_rules(root=root)
    for rule in reg.get("rules") or []:
        if str(rule.get("id") or "") == str(rule_id):
            return rule
    return None


def active_execution_rule(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """The one rule the paper loop honours, or None when the registry is silent.

    A selection rule with ``execution: true`` outranks the baseline — that is
    what the execution flip means. Two of them executing at once is not a tie
    to be broken quietly: the loop would be honouring a rule nobody named, so
    it raises.
    """
    reg = registry if registry is not None else load_rules(root=root)
    live = [r for r in reg.get("rules") or [] if r.get("execution")]
    selecting = [r for r in live if r.get("selects")]
    if len(selecting) > 1:
        raise ValueError(
            "more than one selection rule has execution=true: "
            + ", ".join(str(r.get("id")) for r in selecting)
            + ". The paper loop will not pick one on its own"
        )
    if selecting:
        return selecting[0]
    return live[0] if live else None


def set_selecting_execution(
    rule_id: str,
    execution: bool,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """Flip one selecting row's execution flag. Never writes golf_kalshi.

    Cloud PARK uses this to drop the chair. Observe-park uses it so this
    PC's book stops. Does not arm. Does not invent tape.
    """
    path = registry_path(root=root)
    posix = path.as_posix().replace("\\", "/")
    if "golf_kalshi" in posix.split("/"):
        raise ValueError("refusing to write golf_kalshi from a 15m execution flip")
    reg = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(reg, dict):
        raise ValueError("rule registry must be an object")
    found = False
    for row in reg.get("rules") or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("id") or "") != str(rule_id):
            continue
        if row.get("selects") is not True:
            raise ValueError(f"{rule_id} is not a selecting rule")
        row["execution"] = bool(execution)
        found = True
        break
    if not found:
        raise ValueError(f"{rule_id} is not in the registry")
    path.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    return {"id": str(rule_id), "execution": bool(execution), "path": str(path)}


# ------------------------------------------------------- clause (2): alpha_k


def alpha_k(trials_to_date: int) -> float:
    """``0.05 / (k(k+1))`` with ``k = trials_to_date + 1``.

    The drafted ``0.05/k`` weights are the harmonic series and diverge, so they
    control nothing. This schedule sums to 0.05 over unbounded looks.
    """
    k = int(trials_to_date) + 1
    return 0.05 / (k * (k + 1))


# --------------------------------------------- clause (5): the actual control


def matched_exposure_permutation(
    baseline_pnl: Sequence[float],
    rule_fill_pnl: Sequence[float],
    skipped: Sequence[bool],
    *,
    alpha: float,
    draws: int = MATCHED_EXPOSURE_DRAWS,
    seed: int = MATCHED_EXPOSURE_SEED,
) -> dict[str, Any]:
    """Permutation null holding the skip count fixed and reassigning the skips.

    Clause (1) alone credits mechanical fee avoidance: abstaining at any rate on
    a book with a strictly positive fee raises ``mean(d)`` with no skill
    present. This null is centred on abstaining at the *observed rate* with no
    skill, so the question becomes "did this abstention rule beat abstaining at
    the same rate?" Deterministic given the seed; reads no new data.
    """
    n = len(baseline_pnl)
    if n == 0 or len(rule_fill_pnl) != n or len(skipped) != n:
        raise ValueError("baseline_pnl, rule_fill_pnl and skipped must be the same length")
    if draws < MATCHED_EXPOSURE_DRAWS:
        raise ValueError(f"the bar pre-registers at least {MATCHED_EXPOSURE_DRAWS} draws")
    skip_count = sum(1 for flag in skipped if flag)

    def _mean_d(skip_set: set[int]) -> float:
        total = 0.0
        for i in range(n):
            arm = 0.0 if i in skip_set else float(rule_fill_pnl[i])
            total += arm - float(baseline_pnl[i])
        return total / n

    observed = _mean_d({i for i, flag in enumerate(skipped) if flag})
    rng = random.Random(seed)
    indices = list(range(n))
    null: list[float] = []
    for _ in range(int(draws)):
        null.append(_mean_d(set(rng.sample(indices, skip_count))))
    null.sort()
    # >= observed, so the p-value is conservative on ties.
    at_or_above = sum(1 for value in null if value >= observed)
    position = max(0, min(len(null) - 1, math.ceil((1.0 - alpha) * len(null)) - 1))
    quantile = null[position]
    return {
        "observed_mean_d": round(observed, 6),
        "quantile": round(quantile, 6),
        "quantile_at": round(1.0 - alpha, 6),
        "p_value": round((at_or_above + 1) / (len(null) + 1), 6),
        "exceeds_quantile": observed > quantile,
        "draws": int(draws),
        "seed": int(seed),
        "skip_count": skip_count,
        "n": n,
    }


# ------------------------------------------------------ clause (1): the t-test


def _betacf(a: float, b: float, x: float) -> float:
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-16:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta ``I_x(a, b)``."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + b * math.log(1.0 - x) + a * math.log(x)
    ) * _betacf(b, a, 1.0 - x) / b


def student_t_sf(t: float, df: float) -> float:
    """P(T > t) for Student's t with ``df`` degrees of freedom."""
    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    x = df / (df + float(t) * float(t))
    tail = 0.5 * _betainc(df / 2.0, 0.5, x)
    return tail if t > 0 else 1.0 - tail


def paired_t_against_floor(d: Sequence[float], delta: float) -> dict[str, Any]:
    """One-sided paired t-test of ``H0: mean(d) <= delta``."""
    n = len(d)
    if n < 2:
        raise ValueError("a paired t-test needs at least two windows")
    mean = sum(float(v) for v in d) / n
    var = sum((float(v) - mean) ** 2 for v in d) / (n - 1)
    sd = math.sqrt(var)
    se = sd / math.sqrt(n) if sd else 0.0
    t = (mean - float(delta)) / se if se else 0.0
    return {
        "n": n,
        "mean_d": round(mean, 6),
        "sd_d": round(sd, 6),
        "se": round(se, 6),
        "delta": float(delta),
        "t": round(t, 6),
        "p_value": round(student_t_sf(t, n - 1), 8) if se else None,
    }


# --------------------------------------------------- trials_to_date, in code


TRIAL_DECLARATION = "declaration"
TRIAL_L2_LOOK = "l2_look"


def trials_to_date(*, root: Path | None = None,
                   registry: dict[str, Any] | None = None) -> int:
    reg = registry if registry is not None else load_rules(root=root)
    return int(reg.get("trials_to_date") or 0)


def record_trial(
    subject: str,
    kind: str,
    *,
    root: Path | None = None,
    note: str = "",
    now_iso: str | None = None,
) -> dict[str, Any]:
    """Increment ``trials_to_date`` and log why. Baseline naming is not a trial.

    The counter defines the multiplicity family. Incrementing it "once per
    first-look score" counts what got written up rather than what got tried,
    which is the wrong denominator and always flatters. Declaration of a
    selection rule and an L2 confirmation look are the two events that count.
    """
    if kind not in {TRIAL_DECLARATION, TRIAL_L2_LOOK}:
        raise ValueError(f"{kind!r} is not a trial kind; baseline naming is not a trial")
    path = registry_path(root=root)
    reg = json.loads(path.read_text(encoding="utf-8"))
    entry = {
        "subject": str(subject),
        "kind": kind,
        "at": now_iso or isoformat_now(),
        "note": note,
    }
    log = list(reg.get("trials_log") or [])
    log.append(entry)
    reg["trials_log"] = log
    reg["trials_to_date"] = int(reg.get("trials_to_date") or 0) + 1
    entry["trials_to_date_after"] = reg["trials_to_date"]
    path.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    return entry


def informing_marks_on_tree(*, root: Path | None = None) -> bool:
    """True when this tree already has posted-yes marks a new cut would see."""
    from golf_offshoot.learning_lane_15m.paths import has_15m_root_override, paper_dir_15m

    if has_15m_root_override():
        folder = paper_dir_15m()
    elif root is not None:
        folder = Path(root) / "golf-offshoot" / "data" / "learning_lane_15m" / "paper"
    else:
        folder = paper_dir_15m()
    if not folder.is_dir():
        return False
    return any(folder.glob("KXBTC15M-*.json"))


def declare_rule(
    rule: dict[str, Any],
    *,
    root: Path | None = None,
    now_iso: str | None = None,
) -> dict[str, Any]:
    """Append a rule to the registry, incrementing the counter when it selects.

    A new posted-yes selecting rule is refused if informing marks already
    exist on this tree. A close-minute class is not a skip-band. New
    selecting rows must name ``expected_skip_rate`` from the 15m quartet
    at or above ``10 / first_look_n``, and must not AND-skip a quartet
    triple or the whole quartet. Existing rows stay; this gate is
    pre-registration, not a rewrite. Do not read ``paper/`` pnl for the rate.
    """
    rule_id = str(rule.get("id") or "").strip()
    if not rule_id:
        raise ValueError("a rule needs an id")
    row = dict(rule)
    if (
        row.get("selects")
        and selects_on_posted_yes_cut(row)
        and informing_marks_on_tree(root=root)
    ):
        raise RuleAlreadyInformed(
            f"{rule_id} selects on posted-yes cuts and this tree already has "
            "informing KXBTC15M marks; a new Established-capable rule needs a "
            "new class or a new lane, not another skip-band here"
        )
    if row.get("selects"):
        fill_none = clock_fill_none_reason(row)
        if fill_none:
            raise RuleFillNone(f"{rule_id} {fill_none}")
        rate = expected_skip_rate(row)
        floor = min_expected_skip_rate(root=root)
        if rate is None:
            raise RuleSkipRateUnnamed(
                f"{rule_id} cannot name expected_skip_rate from product structure "
                "(a posted-yes cut is tape-informed, not a 15m clock rate); "
                "declare a CLOCK-* kind or another named quartet skip"
            )
        if rate < floor:
            raise RuleTooSparse(
                f"{rule_id} expected_skip_rate={rate} is below the density floor "
                f"{floor} (10/first_look_n); a minute not on the 15m quartet "
                f"{sorted(QUARTET_CLOSE_MINUTES)} is 0. Catalog prefers ≥ 0.25"
            )
        row["expected_skip_rate"] = round(float(rate), 6)
    path = registry_path(root=root)
    reg = json.loads(path.read_text(encoding="utf-8"))
    if any(str(r.get("id") or "") == rule_id for r in reg.get("rules") or []):
        raise ValueError(f"{rule_id} is already declared; a redeclaration is a new rule")
    row.setdefault("declared_at", now_iso or isoformat_now())
    reg.setdefault("rules", []).append(row)
    path.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    if row.get("selects"):
        record_trial(rule_id, TRIAL_DECLARATION, root=root,
                     note="selection rule declared", now_iso=now_iso)
    return row


# ---------------------------------------------------------------- the scorer


def scorecard_paths(*, root: Path | None = None) -> list[Path]:
    docs = registry_path(root=root).parent
    return sorted(docs.glob(SCORECARD_GLOB)) if docs.is_dir() else []


def _bar(root: Path | None, bar: dict[str, Any] | None) -> dict[str, Any]:
    if bar is not None:
        return bar
    from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar

    return load_evidence_bar(root=root)


def _assert_scorable(
    rule: dict[str, Any],
    bar: dict[str, Any],
    n: int,
    look: str,
    *,
    root: Path | None,
    allow_nonbinding: bool,
) -> None:
    if not rule.get("selects"):
        raise RuleNotScorable(
            f"{rule.get('id')} selects nothing; naming a baseline is not a trial and "
            "scoring one is not a result"
        )
    first_look_n = int((bar.get("looks") or {}).get("first_look_n") or 0)
    if not first_look_n:
        raise RuleNotScorable("the bar declares no first_look_n")
    if n < first_look_n:
        raise RuleNotScorable(
            f"{n} eligible windows is below the declared first look of {first_look_n}; "
            "continuous scoring against a threshold manufactures significance"
        )
    if look == "L2" and not rule.get("execution"):
        raise RuleNotScorable(
            "L2 confirmation requires lived execution; a replayed survivor is not a "
            "lived one"
        )
    if allow_nonbinding:
        return
    if not bar.get("binding"):
        raise RuleNotScorable(
            "the evidence bar is not binding, so a scorecard against it would be a "
            "number with no threshold behind it"
        )
    from golf_offshoot.learning_lane_15m.critic import load_findings

    findings = load_findings(root=root)
    if not findings:
        raise RuleNotScorable("no critic-invariants findings on this tree to score under")
    if findings.get("passed") is not True:
        raise RuleNotScorable(
            "critic-invariants reports "
            f"{', '.join(findings.get('failing') or ['failing checks'])}; the method "
            "checks must pass on the bytes proposed to bind before a rule is scored"
        )


def _assert_window_lived_or_raise(rule: dict[str, Any], *, close_at: str, look: str) -> str:
    """Label a scored window. Replay treated as lived fails as a machine."""
    close_s = str(close_at)
    if not window_is_oos(rule, close_at=close_s):
        raise RuleNotScorable(
            f"{close_s} closed at or before declared_at; it is not OOS for "
            f"{rule.get('id')}"
        )
    if window_is_replay(rule, close_at=close_s):
        bounds = _replay_bounds(rule)
        after = bounds[0].isoformat() if bounds else "?"
        until = bounds[1].isoformat() if bounds else "?"
        raise RuleNotScorable(
            f"{close_s} is in the replay interval ({after}, {until}]; a {look} "
            "score that treats it as lived fails the bar"
        )
    if not window_is_lived(rule, close_at=close_s):
        raise RuleNotScorable(
            f"{close_s} is not lived for {rule.get('id')}"
        )
    return "lived"


def score_rule(
    rule_id: str,
    windows: Sequence[dict[str, Any]],
    *,
    look: str = "L1",
    root: Path | None = None,
    bar: dict[str, Any] | None = None,
    registry: dict[str, Any] | None = None,
    allow_nonbinding: bool = False,
    now_iso: str | None = None,
) -> dict[str, Any]:
    """Apply every binding clause and return a scorecard. Never an ADMIT.

    ``windows`` carries ``close_at``, ``posted_yes``, ``recorded_pnl`` and
    ``stake`` per eligible window. Every pnl is fee-adjusted through
    :func:`fee_adjust` before it is compared — the recorded book has no fee
    term, and comparing gross numbers under a fee thesis is incoherent.

    Lived ``skip_count`` is checked against the same ``10/n`` density floor
    as declare (and against fill-none). A miss is ``undecidable`` /
    ``density_fail``: clause (1) is not scored versus δ.
    """
    look = str(look).upper()
    if look not in {"L1", "L2"}:
        raise ValueError("look must be L1 or L2")
    reg = registry if registry is not None else load_rules(root=root)
    rule = rule_by_id(rule_id, root=root, registry=reg)
    if rule is None:
        raise RuleNotScorable(f"{rule_id} is not in the registry")
    resolved = _bar(root, bar)
    _assert_scorable(rule, resolved, len(windows), look,
                     root=root, allow_nonbinding=allow_nonbinding)

    dist = resolved.get("distinguishable") or {}
    delta = float(dist.get("effect_floor_usd_per_window"))
    control = dist.get("matched_exposure") or {}
    draws = int(control.get("draws") or MATCHED_EXPOSURE_DRAWS)
    seed = int(control.get("seed") or MATCHED_EXPOSURE_SEED)
    k_before = trials_to_date(root=root, registry=reg)
    alpha = alpha_k(k_before)

    baseline_pnl: list[float] = []
    rule_fill_pnl: list[float] = []
    skipped: list[bool] = []
    rows: list[dict[str, Any]] = []
    for window in windows:
        close_at = str(window["close_at"])
        evidence = _assert_window_lived_or_raise(rule, close_at=close_at, look=look)
        posted = float(window["posted_yes"])
        stake = float(window.get("stake") or 1.0)
        recorded = float(window["recorded_pnl"])
        verdict = decide(rule, posted_yes=posted, close_at=close_at)
        skip = verdict["action"] == "skip"
        base_adj = fee_adjust(recorded, posted, stake, root=root)
        # A rule that fills the same contract as the baseline books the same
        # number. A rule that fills a different one supplies its own recorded
        # pnl and mark; nothing here re-derives a fill that was never booked.
        fill_adj = fee_adjust(
            float(window.get("rule_recorded_pnl", recorded)),
            float(window.get("rule_posted_yes", posted)),
            stake,
            root=root,
        )
        baseline_pnl.append(base_adj)
        rule_fill_pnl.append(fill_adj)
        skipped.append(skip)
        rows.append(
            {
                "window_id": window.get("window_id") or "",
                "close_at": close_at,
                "posted_yes": posted,
                "action": verdict["action"],
                "evidence": evidence,
                "pnl_baseline_fee_adj": base_adj,
                "pnl_rule_fee_adj": 0.0 if skip else fill_adj,
            }
        )

    n = len(rows)
    skip_count = sum(1 for flag in skipped if flag)
    density = lived_skip_density(
        skip_count,
        n,
        expected_rate=named_expected_skip_rate(rule),
        root=root,
    )
    card = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "framing": (
            "A scorecard is not an ADMIT, not an edge, not a track record and not a "
            "dated record. It is arithmetic under a named bar."
        ),
        "rule_id": rule_id,
        "look": look,
        "scored_at": now_iso or isoformat_now(),
        "n": n,
        "skip_count": skip_count,
        "skip_rate": round(skip_count / n, 6) if n else 0.0,
        "alpha_k": alpha,
        "trials_to_date_before": k_before,
        "delta": delta,
        "fee_adjust": "golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust",
        "permutation_control": PERMUTATION_PATH,
        "density": density,
        "density_fail": not density["passes"],
        "undecidable": bool(density["undecidable"]),
        "cost_accounting_is_incomplete": (
            "the bid/ask spread is omitted and unmeasured; no figure here is a full "
            "cost accounting"
        ),
        "windows": rows,
    }
    if not density["passes"]:
        card["clause_1_paired_t_vs_floor"] = {
            "passes": None,
            "not_scored": f"density-fail; not a t-test vs delta={delta}",
            "delta": delta,
        }
        card["clause_4_positive_side"] = {
            "passes": None,
            "not_scored": density["reason"] or "density-fail",
        }
        card["clause_5_matched_exposure"] = {
            "passes": None,
            "not_scored": "density-fail; permutation not run",
        }
        card["passes_every_binding_clause"] = False
        card["caveat"] = (
            "Undecidable / density-fail. Lived skip_count is below the "
            "10/n density floor, or the look filled none. "
            "Not a t-test vs δ. Not an ADMIT."
        )
        return card

    d = [row["pnl_rule_fee_adj"] - row["pnl_baseline_fee_adj"] for row in rows]
    rule_side = [row["pnl_rule_fee_adj"] for row in rows]
    clause_1 = paired_t_against_floor(d, delta)
    clause_1["alpha"] = alpha
    clause_1["passes"] = bool(clause_1["p_value"] is not None and clause_1["p_value"] < alpha)
    mean_rule = sum(rule_side) / n
    clause_4 = {"mean_pnl_rule_fee_adj": round(mean_rule, 6), "passes": mean_rule > 0}
    clause_5 = matched_exposure_permutation(
        baseline_pnl, rule_fill_pnl, skipped, alpha=alpha, draws=draws, seed=seed
    )
    clause_5["passes"] = bool(clause_5["exceeds_quantile"])
    passes = clause_1["passes"] and clause_4["passes"] and clause_5["passes"]
    card["clause_1_paired_t_vs_floor"] = clause_1
    card["clause_4_positive_side"] = clause_4
    card["clause_5_matched_exposure"] = clause_5
    card["passes_every_binding_clause"] = passes
    if look == "L2":
        card["trial_recorded"] = record_trial(
            rule_id, TRIAL_L2_LOOK, root=root,
            note="L2 confirmation look", now_iso=now_iso,
        )
    return card
