#!/usr/bin/env python3
"""Named finite discovery/confirm DJT Truth Social oil-sentiment hunt.

Protocol frozen in Lock_Hunt_DJT.md *before* last-500 confirm scores.

Two horses: H-DJT-WEEK (5-session mean) and H-DJT-MONTH (21-session mean)
of daily P/N/F scores. Pick one on discovery F-CC only if it strictly beats 0.

Tell lag: F-ON/F-CC use sentiment ending on CL date t-2; F-DAY uses t-1.
Silent days score 0. Lexicon is frozen; do not retune after RMSE.

Does not download. Does not treat Yahoo as CME. Not a trade.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path

import numpy as np

DISCOVERY_CUTOFF = "2023-08-21"
HORSES = [
    {"id": "H-DJT-WEEK", "window": 5},
    {"id": "H-DJT-MONTH", "window": 21},
]


def rmse(xs: list[float]) -> float | None:
    if not xs:
        return None
    return math.sqrt(sum(x * x for x in xs) / len(xs))


def load_clf(path: str) -> list[dict]:
    rows = []
    with open(path, newline="") as f:
        for rec in csv.DictReader(f):
            rows.append(
                {
                    "date": rec["date"].strip(),
                    "open": float(rec["open"]),
                    "settle": float(rec["settle"]),
                    "front_id": rec["front_id"].strip(),
                }
            )
    rows.sort(key=lambda r: r["date"])
    return rows


def session_returns(rows: list[dict]) -> list[dict]:
    out = []
    for i in range(1, len(rows)):
        prev, cur = rows[i - 1], rows[i]
        rolled = cur["front_id"] != prev["front_id"]
        rec = {"date": cur["date"], "rolled": rolled, "r_on": None, "r_day": None, "r_cc": None}
        if cur["open"] > 0 and cur["settle"] > 0:
            rec["r_day"] = math.log(cur["settle"] / cur["open"])
        if not rolled and prev["settle"] > 0 and cur["open"] > 0:
            rec["r_on"] = math.log(cur["open"] / prev["settle"])
        if not rolled and prev["settle"] > 0 and cur["settle"] > 0:
            rec["r_cc"] = math.log(cur["settle"] / prev["settle"])
        out.append(rec)
    return out


def ols_forecast(y: np.ndarray, X: np.ndarray, x_new: np.ndarray) -> float:
    if y.size < 250 or X.shape[0] != y.size or np.linalg.matrix_rank(X) < X.shape[1]:
        return 0.0
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(x_new @ beta)


def load_lexicon(path: Path) -> dict:
    return json.loads(path.read_text())


def token_hit(text_l: str, token: str) -> bool:
    t = token.lower().strip()
    if not t:
        return False
    if " " in t:
        return t in text_l
    return re.search(r"\b" + re.escape(t) + r"\b", text_l) is not None


def any_hit(text_l: str, tokens: list[str]) -> bool:
    return any(token_hit(text_l, t) for t in tokens)


def score_post(text: str, lex: dict) -> int | None:
    text_l = text.lower()
    if not any_hit(text_l, lex["oil_adjacent"]):
        return None
    bull = any_hit(text_l, lex["bullish_price"])
    bear = any_hit(text_l, lex["bearish_price"])
    if bull and not bear:
        return 1
    if bear and not bull:
        return -1
    return 0


def load_posts(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            rows.append(
                {
                    "date_utc": rec["date_utc"].strip(),
                    "text": rec.get("text") or "",
                }
            )
    return rows


def daily_scores(posts: list[dict], lex: dict) -> dict[str, float]:
    buckets: dict[str, list[int]] = {}
    n_adj = 0
    for rec in posts:
        s = score_post(rec["text"], lex)
        if s is None:
            continue
        n_adj += 1
        buckets.setdefault(rec["date_utc"], []).append(s)
    out = {d: sum(vs) / len(vs) for d, vs in buckets.items()}
    out["_n_oil_adjacent"] = float(n_adj)  # type: ignore[assignment]
    return out


def attach_sentiment(rets: list[dict], daily: dict[str, float], windows: dict[str, int]) -> dict:
    n_adj = int(daily.pop("_n_oil_adjacent", 0))
    dates = [r["date"] for r in rets]
    series = [float(daily.get(d, 0.0)) for d in dates]
    for rec, val in zip(rets, series):
        rec["s_daily"] = val
        rec["sent"] = {}
    for name, w in windows.items():
        for t, rec in enumerate(rets):
            if t + 1 < w:
                rec["sent"][name] = 0.0
            else:
                rec["sent"][name] = float(sum(series[t - w + 1 : t + 1]) / w)
    n_nonzero_days = sum(1 for v in series if v != 0.0)
    return {
        "n_oil_adjacent_posts": n_adj,
        "n_days_with_signal": n_nonzero_days,
        "n_sessions": len(rets),
    }


def _cl_xy(kind: str, cur: dict, lag: dict) -> tuple[float | None, list[float] | None]:
    if kind == "on":
        y = cur["r_on"]
        x = [1.0, lag["r_on"], lag["r_day"]]
    elif kind == "day":
        y = cur["r_day"]
        x = [1.0, cur["r_on"], lag["r_day"]]
    else:
        y = cur["r_cc"]
        x = [1.0, lag["r_on"], lag["r_day"]]
    if y is None or any(v is None for v in x):
        return None, None
    return y, x


def _sent_lag_index(kind: str, t: int) -> int | None:
    if kind in ("on", "cc"):
        idx = t - 2
    else:
        idx = t - 1
    if idx < 0:
        return None
    return idx


def walk_forward_horse(rets: list[dict], holdout: int, min_train: int, spec: dict) -> dict:
    n = len(rets)
    oos_start = max(min_train, n - holdout)
    key = spec["id"]
    out: dict = {}
    for kind, label in [("on", "F-ON"), ("day", "F-DAY"), ("cc", "F-CC")]:
        actuals: list[float] = []
        preds: list[float] = []
        dates: list[str] = []
        y_hist: list[float] = []
        X_hist: list[list[float]] = []
        for t in range(1, n):
            cur, lag = rets[t], rets[t - 1]
            y, x_cl = _cl_xy(kind, cur, lag)
            if y is None or x_cl is None:
                continue
            s_idx = _sent_lag_index(kind, t)
            s = 0.0 if s_idx is None else float(rets[s_idx]["sent"].get(key, 0.0))
            x_full = x_cl + [s]
            if t >= oos_start:
                pred = ols_forecast(np.array(y_hist, float), np.array(X_hist, float), np.array(x_full, float))
                actuals.append(y)
                preds.append(pred)
                dates.append(cur["date"])
            y_hist.append(y)
            X_hist.append(x_full)
        err = [a - p for a, p in zip(actuals, preds)]
        out[label] = {
            "n": len(actuals),
            "first": dates[0] if dates else None,
            "last": dates[-1] if dates else None,
            "rmse_horse": rmse(err),
            "rmse_0": rmse(actuals),
            "beats_0": (
                rmse(err) is not None
                and rmse(actuals) is not None
                and rmse(err) < rmse(actuals)
            ),
        }
    return out


def pick_survivor(discovery: dict) -> dict:
    order = [h["id"] for h in HORSES]
    beat = []
    for hid in order:
        fcc = discovery[hid]["F-CC"]
        if fcc["beats_0"]:
            beat.append((hid, fcc["rmse_horse"]))
    if not beat:
        return {"id": None, "reason": "no horse strictly beat 0 on discovery F-CC last 500"}
    best = min(r for _, r in beat)
    for hid, r in beat:
        if r == best:
            return {
                "id": hid,
                "discovery_fcc_rmse_horse": r,
                "discovery_fcc_rmse_0": discovery[hid]["F-CC"]["rmse_0"],
                "reason": "lowest discovery F-CC RMSE among horses that strictly beat 0",
            }
    return {"id": None, "reason": "unreachable"}


def promote_gate(score: dict) -> dict:
    s500 = score["500"]["F-CC"]
    s250 = score["250"]["F-CC"]
    s750 = score["750"]["F-CC"]
    beat_500 = s500["rmse_horse"] < s500["rmse_0"]
    hold_250 = s250["rmse_horse"] <= s250["rmse_0"]
    hold_750 = s750["rmse_horse"] <= s750["rmse_0"]
    return {
        "fires": beat_500 and hold_250 and hold_750,
        "beat_500": beat_500,
        "hold_250": hold_250,
        "hold_750": hold_750,
    }


def build_rets(clf_path: str, cutoff: str | None, posts: list[dict], lex: dict) -> tuple[list[dict], dict]:
    rows = load_clf(clf_path)
    if cutoff is not None:
        rows = [r for r in rows if r["date"] <= cutoff]
    rets = session_returns(rows)
    daily = daily_scores(posts, lex)
    coverage = attach_sentiment(rets, daily, {h["id"]: h["window"] for h in HORSES})
    return rets, coverage


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default="data/clf_yahoo_standin.csv")
    p.add_argument("--posts", default="data/djt_truth_posts.csv")
    p.add_argument("--lexicon", default="data/djt_oil_lexicon.json")
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--discovery-cutoff", default=DISCOVERY_CUTOFF)
    p.add_argument("--discovery-holdout", type=int, default=500)
    p.add_argument("--min-adjacent", type=int, default=30)
    p.add_argument("--phase", choices=["discovery", "confirm", "all"], default="all")
    p.add_argument("--out", default="data/djt_hunt_scores.json")
    args = p.parse_args()

    lex = load_lexicon(Path(args.lexicon))
    posts = load_posts(Path(args.posts))
    payload: dict = {
        "badge": "stand-in",
        "lock": "L-HUNT-DJT",
        "tells": "L-STANDIN-DJT-TRUTH",
        "discovery_cutoff": args.discovery_cutoff,
        "discovery_holdout": args.discovery_holdout,
        "min_train": args.min_train,
        "horse_order": [h["id"] for h in HORSES],
        "n_posts": len(posts),
    }

    if args.phase in ("discovery", "all"):
        disc_rets, cov = build_rets(args.clf, args.discovery_cutoff, posts, lex)
        payload["discovery_coverage"] = cov
        if cov["n_oil_adjacent_posts"] < args.min_adjacent:
            payload["survivor"] = {
                "id": None,
                "reason": (
                    f"vehicle too thin: {cov['n_oil_adjacent_posts']} oil-adjacent posts "
                    f"in discovery prefix (need {args.min_adjacent})"
                ),
            }
            payload["discovery"] = None
            payload["vehicle_fail"] = True
        else:
            discovery = {
                spec["id"]: walk_forward_horse(disc_rets, args.discovery_holdout, args.min_train, spec)
                for spec in HORSES
            }
            payload["discovery_n_sessions"] = len(disc_rets)
            payload["discovery"] = discovery
            payload["survivor"] = pick_survivor(discovery)
            payload["vehicle_fail"] = False
    else:
        prior = json.loads(Path(args.out).read_text()) if Path(args.out).exists() else {}
        payload["discovery"] = prior.get("discovery")
        payload["survivor"] = prior.get("survivor")
        payload["discovery_n_sessions"] = prior.get("discovery_n_sessions")
        payload["discovery_coverage"] = prior.get("discovery_coverage")
        payload["vehicle_fail"] = prior.get("vehicle_fail")

    if args.phase in ("confirm", "all"):
        survivor = payload.get("survivor") or {}
        hid = survivor.get("id")
        if hid is None:
            payload["confirm"] = None
            payload["promote"] = {
                "fires": False,
                "reason": survivor.get("reason") or "no discovery survivor",
            }
        else:
            spec = next(h for h in HORSES if h["id"] == hid)
            full_rets, cov = build_rets(args.clf, None, posts, lex)
            payload["confirm_coverage"] = cov
            confirm = {}
            for h in (500, 250, 750):
                confirm[str(h)] = walk_forward_horse(full_rets, h, args.min_train, spec)
            payload["confirm_horse"] = hid
            payload["confirm"] = confirm
            payload["promote"] = promote_gate(confirm)

    Path(args.out).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
