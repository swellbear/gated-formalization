"""Sibling exam contrast, futility, and machine score artifact.

Do not import live ``rules.py``. ``fee_adjust`` is a score-time lazy import
via ``honer_15m.fee``. Gross ledgers stay as booked.
"""

from __future__ import annotations

import json
import math
import random
from typing import Any

from golf_offshoot.honer_15m.books import iter_settled
from golf_offshoot.honer_15m.fee import adjust_fill, fee_is_applied
from golf_offshoot.honer_15m.keep import load_bar
from golf_offshoot.honer_15m.paths import assert_honer_path, exam_score_path
from golf_offshoot.honer_15m.policy import STAKE, load_policy
from golf_offshoot.localtime import now


def exam_sums(rows: list[dict[str, Any]] | None = None) -> dict[str, float]:
    settled = rows if rows is not None else iter_settled("exam")
    d_sum = 0.0
    pnl_sum = 0.0
    n = 0
    for row in settled:
        n += 1
        d_sum += float(row.get("d") or 0.0)
        pnl_sum += float(row.get("pnl") or 0.0)
    return {"n": float(n), "d_sum": d_sum, "exam_pnl_sum": pnl_sum}


def fee_adjusted_exam_rows(rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Score-time fee_adjust. Does not rewrite search or exam ledgers."""
    settled = rows if rows is not None else iter_settled("exam")
    out: list[dict[str, Any]] = []
    stake = float(STAKE)
    for row in settled:
        posted = float(row.get("posted_yes") or 0.0)
        fill_all = float(row.get("fill_all_pnl") or 0.0)
        filled = str(row.get("action") or "") == "fill"
        exam_pnl = float(row.get("pnl") or 0.0)
        fill_all_adj = adjust_fill(fill_all, posted, stake, filled=True)
        exam_adj = adjust_fill(exam_pnl, posted, stake, filled=True) if filled else 0.0
        item = dict(row)
        item["pnl_fee_adj"] = exam_adj
        item["fill_all_pnl_fee_adj"] = fill_all_adj
        item["d_fee_adj"] = round(exam_adj - fill_all_adj, 4)
        out.append(item)
    return out


def exam_sums_fee_adj(rows: list[dict[str, Any]] | None = None) -> dict[str, float]:
    adj = fee_adjusted_exam_rows(rows)
    d_sum = 0.0
    pnl_sum = 0.0
    for row in adj:
        d_sum += float(row.get("d_fee_adj") or 0.0)
        pnl_sum += float(row.get("pnl_fee_adj") or 0.0)
    return {"n": float(len(adj)), "d_sum": d_sum, "exam_pnl_sum": pnl_sum}


def futility_impossible(
    n: int,
    d_sum: float,
    exam_pnl_sum: float,
    *,
    exam_n: int | None = None,
) -> bool:
    """Remaining windows are all skips: d=+1 each, exam pnl +0. Simultaneous path."""
    total = int(exam_n if exam_n is not None else load_policy()["exam_n"])
    if n < 0 or n > total:
        return True
    remaining = total - n
    final_d = float(d_sum) + remaining * 1.0
    final_pnl = float(exam_pnl_sum)
    mean_d = final_d / total
    mean_pnl = final_pnl / total
    return mean_d <= 0.0 or mean_pnl <= 0.0


def should_check_futility(n: int) -> bool:
    return n in {int(x) for x in load_policy()["futility_looks"]}


def classify_completed_exam(rows: list[dict[str, Any]] | None = None) -> str:
    """End-of-70 give-up label. Not a score. Not Established. Not a keep.

    Uses fee-adjusted d/pnl when a dated honer fee-apply is on the bar.
    """
    if fee_is_applied(load_bar()):
        sums = exam_sums_fee_adj(rows)
    else:
        sums = exam_sums(rows)
    n = int(sums["n"])
    if n <= 0:
        return "completed_dead"
    mean_d = float(sums["d_sum"]) / n
    mean_pnl = float(sums["exam_pnl_sum"]) / n
    if mean_d <= 0.0 or mean_pnl <= 0.0:
        return "completed_dead"
    return "completed_unscored"


def mean_and_sd(values: list[float]) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    mu = sum(values) / len(values)
    if len(values) < 2:
        return (mu, 0.0)
    var = sum((x - mu) ** 2 for x in values) / (len(values) - 1)
    return (mu, math.sqrt(var))


def alpha_k(trials_to_date: int) -> float:
    k = int(trials_to_date) + 1
    return 0.05 / (k * (k + 1))


def permutation_mean_d(ds: list[float], *, seed: int, draws: int = 10_000) -> float:
    """Null: shuffle signs of skip-contrast; report fraction mean(d*) >= mean(d)."""
    if not ds:
        return 1.0
    obs = sum(ds) / len(ds)
    rng = random.Random(int(seed))
    hits = 0
    for _ in range(int(draws)):
        trial = [x * rng.choice((-1.0, 1.0)) for x in ds]
        if (sum(trial) / len(trial)) >= obs:
            hits += 1
    return hits / float(draws)


def write_exam_scorecard(
    exam: dict[str, Any],
    *,
    outcome: str,
) -> dict[str, Any]:
    """Machine score/park artifact. Not a keep. Does not flip consult."""
    rows = iter_settled("exam")
    adj = fee_adjusted_exam_rows(rows) if fee_is_applied(load_bar()) else []
    if adj:
        d_sum = sum(float(r.get("d_fee_adj") or 0.0) for r in adj)
        pnl_sum = sum(float(r.get("pnl_fee_adj") or 0.0) for r in adj)
        n = len(adj)
        ds = [float(r.get("d_fee_adj") or 0.0) for r in adj]
    else:
        sums = exam_sums(rows)
        n = int(sums["n"])
        d_sum = float(sums["d_sum"])
        pnl_sum = float(sums["exam_pnl_sum"])
        ds = [float(r.get("d") or 0.0) for r in rows]
    label = outcome
    if outcome not in {"parked", "completed_dead", "completed_unscored"}:
        label = classify_completed_exam(rows)
    pol = load_policy()
    seed = int(pol.get("permutation_seed") or 20260909)
    card = {
        "schema": 1,
        "lane": "honer_15m",
        "framing": (
            "Machine exam score. Not a keep, not an ADMIT, not arm, not consult enable."
        ),
        "outcome": label,
        "survives": label == "completed_unscored",
        "n": n,
        "d_sum": d_sum,
        "exam_pnl_sum": pnl_sum,
        "mean_d": (d_sum / n) if n else 0.0,
        "mean_exam_pnl": (pnl_sum / n) if n else 0.0,
        "fee_applied": fee_is_applied(load_bar()),
        "fee_adjust": "golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust",
        "permutation_p_mean_d": permutation_mean_d(ds, seed=seed) if n else 1.0,
        "frozen_family": exam.get("frozen_family"),
        "frozen_theta": exam.get("frozen_theta"),
        "frozen_delta": exam.get("frozen_delta"),
        "declared_at": exam.get("declared_at"),
        "k_after": exam.get("k_after"),
        "park_reason": exam.get("park_reason") or "",
        "consult_enabled": False,
        "scored_at": now().isoformat(),
    }
    path = exam_score_path()
    assert_honer_path(path)
    path.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    return card
