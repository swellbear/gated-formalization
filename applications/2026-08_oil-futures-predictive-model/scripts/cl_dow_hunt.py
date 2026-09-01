#!/usr/bin/env python3
"""Named finite discovery/confirm weekday overlay on Yahoo CL.

Protocol frozen in Lock_Hunt_CL_Dow.md *before* last-500 confirm scores.

Two horses: H-CL-DOW-WD (lags + Tue-Fri dummies, Monday baseline) and
H-CL-DOW-FRI (lags + Friday dummy).
Pick one on discovery F-CC only if it strictly beats 0.

Does not download. Does not treat Yahoo as CME. Not a trade.
Not a retune of L-HUNT-CL-SEAS. Not H-SPARSE-CAL event-day sparse.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import date
from pathlib import Path

import numpy as np

DISCOVERY_CUTOFF = "2023-08-21"
HORSES = [
    {"id": "H-CL-DOW-WD", "kind": "weekdays"},
    {"id": "H-CL-DOW-FRI", "kind": "friday"},
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
        wd = date.fromisoformat(cur["date"]).weekday()
        rec["weekday"] = wd
        rec["wd_dummies"] = [1.0 if wd == d else 0.0 for d in (1, 2, 3, 4)]
        rec["friday"] = 1.0 if wd == 4 else 0.0
        out.append(rec)
    return out


def ols_forecast(y: np.ndarray, X: np.ndarray, x_new: np.ndarray) -> float:
    if y.size < 250 or X.shape[0] != y.size or np.linalg.matrix_rank(X) < X.shape[1]:
        return 0.0
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(x_new @ beta)


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


def extra_features(spec: dict, rec: dict) -> list[float]:
    if spec["kind"] == "weekdays":
        return [float(v) for v in rec["wd_dummies"]]
    return [float(rec["friday"])]


def walk_forward_horse(rets: list[dict], holdout: int, min_train: int, spec: dict) -> dict:
    n = len(rets)
    oos_start = max(min_train, n - holdout)
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
            x_full = x_cl + extra_features(spec, cur)
            if t >= oos_start:
                pred = ols_forecast(
                    np.array(y_hist, float), np.array(X_hist, float), np.array(x_full, float)
                )
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
                "reason": "lowest discovery F-CC RMSE among horses that strictly beat 0; ties keep H-CL-DOW-WD",
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


def build_rets(clf_path: str, cutoff: str | None) -> list[dict]:
    rows = load_clf(clf_path)
    if cutoff is not None:
        rows = [r for r in rows if r["date"] <= cutoff]
    return session_returns(rows)


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default=str(here / "data" / "clf_yahoo_standin.csv"))
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--discovery-cutoff", default=DISCOVERY_CUTOFF)
    p.add_argument("--discovery-holdout", type=int, default=500)
    p.add_argument("--phase", choices=["discovery", "confirm", "all"], default="all")
    p.add_argument("--out", default=str(here / "data" / "cl_dow_hunt_scores.json"))
    args = p.parse_args()

    payload: dict = {
        "badge": "stand-in",
        "lock": "L-HUNT-CL-DOW",
        "discovery_cutoff": args.discovery_cutoff,
        "discovery_holdout": args.discovery_holdout,
        "min_train": args.min_train,
        "horse_order": [h["id"] for h in HORSES],
        "refused_prior": [
            "H-LAG-WF",
            "H-SPARSE-CAL",
            "H-SPARSE-VOL",
            "H-GAP-FADE",
            "H-GAP-CONT",
            "L-HUNT-PRETELL",
            "L-HUNT-DJT",
            "L-HUNT-COT",
            "H-CL-INV-SURP",
            "H-CL-INV-WOW",
            "H-CL-SEAS-ANN",
            "H-CL-SEAS-MON",
        ],
    }

    if args.phase in ("discovery", "all"):
        disc_rets = build_rets(args.clf, args.discovery_cutoff)
        payload["discovery_n_sessions"] = len(disc_rets)
        payload["discovery_span"] = {
            "first": disc_rets[0]["date"] if disc_rets else None,
            "last": disc_rets[-1]["date"] if disc_rets else None,
        }
        if len(disc_rets) < args.discovery_holdout + args.min_train:
            payload["survivor"] = {
                "id": None,
                "reason": (
                    f"vehicle too thin: {len(disc_rets)} discovery sessions "
                    f"(need {args.discovery_holdout + args.min_train})"
                ),
            }
            payload["discovery"] = None
            payload["vehicle_fail"] = True
        else:
            discovery = {
                spec["id"]: walk_forward_horse(
                    disc_rets, args.discovery_holdout, args.min_train, spec
                )
                for spec in HORSES
            }
            payload["discovery"] = discovery
            payload["survivor"] = pick_survivor(discovery)
            payload["vehicle_fail"] = False
    else:
        prior = json.loads(Path(args.out).read_text()) if Path(args.out).exists() else {}
        payload["discovery"] = prior.get("discovery")
        payload["survivor"] = prior.get("survivor")
        payload["discovery_n_sessions"] = prior.get("discovery_n_sessions")
        payload["discovery_span"] = prior.get("discovery_span")
        payload["vehicle_fail"] = prior.get("vehicle_fail")

    if args.phase in ("confirm", "all"):
        survivor = payload.get("survivor") or {}
        hid = survivor.get("id")
        if hid is None or payload.get("vehicle_fail"):
            payload["confirm"] = None
            payload["promote"] = {
                "fires": False,
                "reason": survivor.get("reason") or "no discovery survivor",
            }
        else:
            spec = next(h for h in HORSES if h["id"] == hid)
            full_rets = build_rets(args.clf, None)
            confirm = {}
            for h in (500, 250, 750):
                confirm[str(h)] = walk_forward_horse(full_rets, h, args.min_train, spec)
            payload["confirm_horse"] = hid
            payload["confirm"] = confirm
            payload["promote"] = promote_gate(confirm)

    if args.phase == "discovery":
        payload["confirm"] = None
        payload["confirm_deferred"] = True
        if payload.get("promote") is None:
            payload["promote"] = {"fires": False, "reason": "confirm deferred"}

    Path(args.out).write_text(json.dumps(payload, indent=2) + "\n")
    summary = {
        "vehicle_fail": payload.get("vehicle_fail"),
        "phase": args.phase,
        "survivor": (payload.get("survivor") or {}).get("id"),
        "discovery_fcc": {
            hid: {
                "rmse_horse": payload["discovery"][hid]["F-CC"]["rmse_horse"],
                "rmse_0": payload["discovery"][hid]["F-CC"]["rmse_0"],
                "beats_0": payload["discovery"][hid]["F-CC"]["beats_0"],
            }
            for hid in [h["id"] for h in HORSES]
            if payload.get("discovery")
        },
        "promote_fires": (payload.get("promote") or {}).get("fires"),
        "confirm_ran": payload.get("confirm") is not None,
    }
    print(json.dumps(summary, indent=2))
    return 1 if payload.get("vehicle_fail") else 0


if __name__ == "__main__":
    raise SystemExit(main())
