#!/usr/bin/env python3
"""Walk-forward horses vs no-change RMSE on the Yahoo CL=F stand-in.

H-LAG-WF (specified before looking at OOS):
  Tape: clf_yahoo_standin.csv
  OOS: last 500 sessions (same holdout as L-PULSE-STANDIN-1)
  Expanding OLS, min train 250, intercept included.
  Information sets (r_CC = r_ON + r_DAY on this continuous generic, so r_CC
  is not a third lag — including it makes OLS rank-deficient and silently
  collapses to the 0 forecast):
    F-ON:  y=r_ON,t  X=[1, r_ON,t-1, r_DAY,t-1]   issued at t-1 settle
    F-DAY: y=r_DAY,t X=[1, r_ON,t,   r_DAY,t-1]   issued at t open
    F-CC:  y=r_CC,t  X=[1, r_ON,t-1, r_DAY,t-1]   issued at t-1 settle
  Rank-deficient or n_train<250 → forecast 0 that day.

H-KS-FTS: requires a historical CL1–CL18 panel. If that panel cannot support
the same 500-session OOS on tenor 1, the horse is skipped (not a silent substitute).

H-SPARSE-CAL / H-SPARSE-VOL (specified before looking at OOS):
  Same OLS as H-LAG-WF (fit on all expanding days, min train 250).
  Emit OLS only when a trigger known at issue time is true; else forecast 0.
  CAL: session date is EIA WPSR or regularly scheduled FOMC announcement
       (data/sparse_calendar.json).
  VOL: |r_CC,t-1| >= expanding 80th percentile of |r_CC| through t-1;
       require >= 250 past |r_CC| else no trigger. Same trigger all windows.

Does not download. Does not treat Yahoo as CME. Not a trade.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import date, timedelta
from pathlib import Path

import numpy as np


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


def load_calendar(path: str, tape_dates: list[str]) -> set[str]:
    spec = json.loads(Path(path).read_text())
    tape = set(tape_dates)
    event: set[str] = set()
    for d in spec["fomc_announcement_dates"]:
        if d in tape:
            event.add(d)
    skip_wed = {row["skip_wednesday"] for row in spec["eia_holiday_overrides"]}
    alt = {row["alternate"] for row in spec["eia_holiday_overrides"]}
    if tape_dates:
        start = date.fromisoformat(tape_dates[0])
        end = date.fromisoformat(tape_dates[-1])
        wed = start
        while wed.weekday() != 2:
            wed += timedelta(days=1)
        while wed <= end:
            iso = wed.isoformat()
            if iso not in skip_wed:
                if iso in tape:
                    event.add(iso)
                else:
                    nxt = wed + timedelta(days=1)
                    last = wed + timedelta(days=6)
                    while nxt <= last:
                        cand = nxt.isoformat()
                        if cand in tape:
                            event.add(cand)
                            break
                        nxt += timedelta(days=1)
            wed += timedelta(days=7)
    for a in alt:
        if a in tape:
            event.add(a)
    return event


def walk_forward_lag(rets: list[dict], holdout: int, min_train: int) -> dict:
    n = len(rets)
    oos_start = max(min_train, n - holdout)

    def collect(kind: str) -> tuple[list[float], list[float], list[str]]:
        actuals: list[float] = []
        preds: list[float] = []
        dates: list[str] = []
        y_hist: list[float] = []
        X_hist: list[list[float]] = []
        for t in range(1, n):
            cur, lag = rets[t], rets[t - 1]
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
                continue
            if t >= oos_start:
                pred = ols_forecast(np.array(y_hist, float), np.array(X_hist, float), np.array(x, float))
                actuals.append(y)
                preds.append(pred)
                dates.append(cur["date"])
            y_hist.append(y)
            X_hist.append(x)
        return actuals, preds, dates

    out = {}
    for kind, label in [("on", "F-ON"), ("day", "F-DAY"), ("cc", "F-CC")]:
        actuals, preds, dates = collect(kind)
        err = [a - p for a, p in zip(actuals, preds)]
        out[label] = {
            "n": len(actuals),
            "first": dates[0] if dates else None,
            "last": dates[-1] if dates else None,
            "rmse_horse": rmse(err),
            "rmse_0": rmse(actuals),
            "beats_0": (rmse(err) is not None and rmse(actuals) is not None and rmse(err) < rmse(actuals)),
        }
    return out


def _window_xy(kind: str, cur: dict, lag: dict) -> tuple[float | None, list[float] | None]:
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


def walk_forward_sparse(
    rets: list[dict],
    holdout: int,
    min_train: int,
    mode: str,
    event_days: set[str],
) -> dict:
    n = len(rets)
    oos_start = max(min_train, n - holdout)
    out: dict = {}
    for kind, label in [("on", "F-ON"), ("day", "F-DAY"), ("cc", "F-CC")]:
        actuals: list[float] = []
        preds: list[float] = []
        dates: list[str] = []
        n_trig = 0
        y_hist: list[float] = []
        X_hist: list[list[float]] = []
        for t in range(1, n):
            cur, lag = rets[t], rets[t - 1]
            y, x = _window_xy(kind, cur, lag)
            if mode == "cal":
                trig = cur["date"] in event_days
            else:
                hist = [abs(rets[s]["r_cc"]) for s in range(0, t) if rets[s]["r_cc"] is not None]
                trig = (
                    lag["r_cc"] is not None
                    and len(hist) >= min_train
                    and abs(lag["r_cc"]) >= float(np.percentile(hist, 80))
                )
            if y is None or x is None:
                continue
            if t >= oos_start:
                if trig:
                    pred = ols_forecast(
                        np.array(y_hist, float),
                        np.array(X_hist, float),
                        np.array(x, float),
                    )
                    n_trig += 1
                else:
                    pred = 0.0
                actuals.append(y)
                preds.append(pred)
                dates.append(cur["date"])
            y_hist.append(y)
            X_hist.append(x)
        err = [a - p for a, p in zip(actuals, preds)]
        out[label] = {
            "n": len(actuals),
            "n_triggered": n_trig,
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


def promote_gate(score: dict) -> dict:
    """L-SCREEN-Y-PROMOTE: F-CC < 0 on 500, and F-CC <= 0 on 250 and 750."""
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


def _months_ahead(date: str, delivery: str) -> int:
    y, m, _ = (int(x) for x in date.split("-"))
    dy, dm = (int(x) for x in delivery.split("-"))
    return (dy - y) * 12 + (dm - m)


def curve_supports_ks(panel_csv: Path, holdout: int) -> dict:
    """Tenor 1 must be a near-dated front, not the nearest *still-listed* leftover."""
    if not panel_csv.exists():
        return {"ok": False, "reason": "panel csv missing"}
    by_date: dict[str, list[dict]] = {}
    with panel_csv.open(newline="") as f:
        for rec in csv.DictReader(f):
            by_date.setdefault(rec["date"], []).append(rec)
    true_front_complete = []
    labeled_18 = 0
    for day, recs in by_date.items():
        tenors = {int(r["tenor"]) for r in recs}
        if set(range(1, 19)) <= tenors:
            labeled_18 += 1
        t1 = next((r for r in recs if r["tenor"] == "1"), None)
        if t1 is None:
            continue
        if set(range(1, 19)) <= tenors and 0 <= _months_ahead(day, t1["delivery"]) <= 2:
            true_front_complete.append(day)
    true_front_complete.sort()
    return {
        "ok": len(true_front_complete) >= holdout + 250,
        "n_dates_total": len(by_date),
        "n_dates_labeled_cl1_cl18": labeled_18,
        "n_dates_true_front_cl1_cl18": len(true_front_complete),
        "first_true_front_complete": true_front_complete[0] if true_front_complete else None,
        "last_true_front_complete": true_front_complete[-1] if true_front_complete else None,
        "reason": None
        if len(true_front_complete) >= holdout + 250
        else (
            "Yahoo expired months 404; nearest still-listed contract is not historical CL1. "
            f"True-front dates with CL1–CL18: {len(true_front_complete)} (need {holdout + 250})."
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default="data/clf_yahoo_standin.csv")
    p.add_argument("--curve", default="data/clf_yahoo_month_chain.csv")
    p.add_argument("--calendar", default="data/sparse_calendar.json")
    p.add_argument("--holdout", type=int, default=500)
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--out", default="data/horse_scores.json")
    args = p.parse_args()

    rows = load_clf(args.clf)
    rets = session_returns(rows)
    tape_dates = [r["date"] for r in rows]
    events = load_calendar(args.calendar, tape_dates)
    lag = walk_forward_lag(rets, args.holdout, args.min_train)
    cal = walk_forward_sparse(rets, args.holdout, args.min_train, "cal", events)
    vol = walk_forward_sparse(rets, args.holdout, args.min_train, "vol", events)
    ks_gate = curve_supports_ks(Path(args.curve), args.holdout)
    sparse_sens = {}
    for h in (250, 750):
        sparse_sens[str(h)] = {
            "H-SPARSE-CAL": walk_forward_sparse(rets, h, args.min_train, "cal", events),
            "H-SPARSE-VOL": walk_forward_sparse(rets, h, args.min_train, "vol", events),
        }
    promote = {
        "H-SPARSE-CAL": promote_gate(
            {"500": cal, "250": sparse_sens["250"]["H-SPARSE-CAL"], "750": sparse_sens["750"]["H-SPARSE-CAL"]}
        ),
        "H-SPARSE-VOL": promote_gate(
            {"500": vol, "250": sparse_sens["250"]["H-SPARSE-VOL"], "750": sparse_sens["750"]["H-SPARSE-VOL"]}
        ),
    }
    payload = {
        "tape": args.clf,
        "badge": "stand-in",
        "holdout": args.holdout,
        "min_train": args.min_train,
        "calendar": args.calendar,
        "n_event_days_on_tape": len(events),
        "H-LAG-WF": lag,
        "H-SPARSE-CAL": cal,
        "H-SPARSE-VOL": vol,
        "H-KS-FTS": {
            "run": False,
            "gate": ks_gate,
        },
        "sparse_sensitivity": sparse_sens,
        "promote": promote,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
