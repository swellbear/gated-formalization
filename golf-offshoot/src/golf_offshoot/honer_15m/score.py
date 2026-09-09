"""Sibling exam contrast and futility. Own seed. Do not import live rules.py."""

from __future__ import annotations

import math
import random
from typing import Any

from golf_offshoot.honer_15m.books import iter_settled
from golf_offshoot.honer_15m.policy import load_policy


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
