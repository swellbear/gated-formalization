#!/usr/bin/env python3
"""Walk-forward H-GAP-FADE / H-GAP-CONT on the Yahoo CL=F stand-in.

Protocol frozen in Lock_Horses_Gap.md *before* last-500 confirm scores.

F-DAY only uses this morning's overnight gap (known at the open).
F-ON and F-CC are locked to forecast 0 (gap not known at t-1 settle).

Trigger: |r_ON,t| >= expanding 80th percentile of |r_ON| through t-1;
require >= 250 past |r_ON|. Scale k from expanding no-intercept OLS
r_DAY = k * r_ON on past complete days (min 250).
FADE: pred = -abs(k) * r_ON; CONT: pred = +abs(k) * r_ON; else 0.

Discovery: dates <= 2023-08-21; pick the single F-DAY winner only if it
strictly beats 0 on the last 500 of that prefix. Confirm: that one horse
(or none) on last 500/250/750. A day win does not promote.

Does not download. Does not treat Yahoo as CME. Not a trade.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

DISCOVERY_CUTOFF = "2023-08-21"
HORSES = ["H-GAP-FADE", "H-GAP-CONT"]


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


def slope_no_intercept(y: list[float], x: list[float]) -> float | None:
    if len(y) < 250 or len(y) != len(x):
        return None
    xv = np.array(x, float)
    yv = np.array(y, float)
    denom = float(xv @ xv)
    if denom <= 0.0:
        return None
    return float(xv @ yv) / denom


def walk_forward_gap(
    rets: list[dict],
    holdout: int,
    min_train: int,
    horse: str,
) -> dict:
    n = len(rets)
    oos_start = max(min_train, n - holdout)
    fade = horse == "H-GAP-FADE"

    def collect(kind: str) -> dict:
        actuals: list[float] = []
        preds: list[float] = []
        dates: list[str] = []
        n_trig = 0
        on_hist: list[float] = []
        # past complete F-DAY pairs for k (through t-1): append after each t
        y_day: list[float] = []
        x_on: list[float] = []
        for t in range(0, n):
            cur = rets[t]
            if kind == "on":
                y = cur["r_on"]
                pred = 0.0
                trig = False
            elif kind == "cc":
                y = cur["r_cc"]
                pred = 0.0
                trig = False
            else:
                y = cur["r_day"]
                r_on = cur["r_on"]
                trig = False
                pred = 0.0
                if y is not None and r_on is not None:
                    trig = (
                        len(on_hist) >= min_train
                        and abs(r_on) >= float(np.percentile(on_hist, 80))
                    )
                    k = slope_no_intercept(y_day, x_on)
                    if trig and k is not None:
                        scale = abs(k)
                        pred = (-scale if fade else scale) * r_on
            # skip missing y (same as H-LAG)
            if y is None:
                if kind == "day" and cur["r_on"] is not None:
                    on_hist.append(abs(cur["r_on"]))
                continue
            if kind == "day" and cur["r_on"] is None:
                # cannot form F-DAY horse features; skip like H-LAG
                continue
            if t >= oos_start:
                if trig:
                    n_trig += 1
                actuals.append(y)
                preds.append(pred)
                dates.append(cur["date"])
            if kind == "day" and cur["r_on"] is not None:
                on_hist.append(abs(cur["r_on"]))
                if cur["r_day"] is not None:
                    y_day.append(cur["r_day"])
                    x_on.append(cur["r_on"])
        err = [a - p for a, p in zip(actuals, preds)]
        row = {
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
        if kind == "day":
            row["n_triggered"] = n_trig
        return row

    return {
        "F-ON": collect("on"),
        "F-DAY": collect("day"),
        "F-CC": collect("cc"),
    }


def pick_survivor(discovery: dict) -> dict:
    beat = []
    for hid in HORSES:
        day = discovery[hid]["F-DAY"]
        if day["beats_0"]:
            beat.append((hid, day["rmse_horse"]))
    if not beat:
        return {"id": None, "reason": "no horse strictly beat 0 on discovery F-DAY last 500"}
    best = min(r for _, r in beat)
    for hid, r in beat:
        if r == best:
            return {
                "id": hid,
                "discovery_fday_rmse_horse": r,
                "discovery_fday_rmse_0": discovery[hid]["F-DAY"]["rmse_0"],
                "reason": "lowest discovery F-DAY RMSE among horses that strictly beat 0",
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
        "note": "F-CC locked to 0 for these horses; a day win does not promote",
    }


def build_rets(clf_path: str, cutoff: str | None) -> list[dict]:
    rows = load_clf(clf_path)
    if cutoff is not None:
        rows = [r for r in rows if r["date"] <= cutoff]
    return session_returns(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default="data/clf_yahoo_standin.csv")
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--discovery-cutoff", default=DISCOVERY_CUTOFF)
    p.add_argument("--discovery-holdout", type=int, default=500)
    p.add_argument("--phase", choices=["discovery", "confirm", "all"], default="all")
    p.add_argument("--out", default="data/gap_horse_scores.json")
    args = p.parse_args()

    payload: dict = {
        "badge": "stand-in",
        "lock": "L-HUNT-GAP",
        "horses": HORSES,
        "discovery_cutoff": args.discovery_cutoff,
        "discovery_holdout": args.discovery_holdout,
        "min_train": args.min_train,
        "note": "F-ON and F-CC forecasts locked to 0. Selection is F-DAY. Day win != promote.",
    }

    if args.phase in ("discovery", "all"):
        disc_rets = build_rets(args.clf, args.discovery_cutoff)
        discovery = {
            hid: walk_forward_gap(disc_rets, args.discovery_holdout, args.min_train, hid)
            for hid in HORSES
        }
        payload["discovery_n_sessions"] = len(disc_rets)
        payload["discovery"] = discovery
        payload["survivor"] = pick_survivor(discovery)
    else:
        prior = json.loads(Path(args.out).read_text()) if Path(args.out).exists() else {}
        payload["discovery"] = prior.get("discovery")
        payload["survivor"] = prior.get("survivor")
        payload["discovery_n_sessions"] = prior.get("discovery_n_sessions")

    if args.phase in ("confirm", "all"):
        survivor = payload.get("survivor") or {}
        hid = survivor.get("id")
        if hid is None:
            payload["confirm"] = None
            payload["promote"] = {"fires": False, "reason": "no discovery survivor"}
        else:
            full_rets = build_rets(args.clf, cutoff=None)
            confirm = {}
            for h in (500, 250, 750):
                confirm[str(h)] = walk_forward_gap(full_rets, h, args.min_train, hid)
            payload["confirm_horse"] = hid
            payload["confirm"] = confirm
            payload["promote"] = promote_gate(confirm)

    Path(args.out).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
