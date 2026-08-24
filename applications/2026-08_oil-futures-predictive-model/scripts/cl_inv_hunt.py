#!/usr/bin/env python3
"""Named finite discovery/confirm EIA inventory overlay on Yahoo CL.

Protocol frozen in Lock_Hunt_CL_Inv.md *before* last-500 confirm scores.

Two horses: H-CL-INV-SURP (naive surprise / 1e4) and H-CL-INV-WOW (Δ / 1e4).
Pick one on discovery F-CC only if it strictly beats 0.

Inventory lag: F-ON/F-CC use release known as of CL date t-2; F-DAY uses t-1.

Does not download. Does not treat Yahoo as CME. Not a trade.
Not a Track B spot hit-rate horse.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

DISCOVERY_CUTOFF = "2023-08-21"
SCALE = 1e4
LOOKBACK_WOW = 4
MIN_REPORTS = 30
HORSES = [
    {"id": "H-CL-INV-SURP", "field": "surprise_scaled"},
    {"id": "H-CL-INV-WOW", "field": "wow_scaled"},
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


def load_inventory(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            rows.append(
                {
                    "week_ending": rec["week_ending"].strip(),
                    "release_date": rec["release_date"].strip(),
                    "stocks": float(rec["stocks"]),
                }
            )
    rows.sort(key=lambda r: r["release_date"])
    wow: list[float | None] = []
    for i, rec in enumerate(rows):
        if i == 0:
            rec["wow"] = 0.0
            rec["surprise"] = 0.0
            wow.append(None)
            continue
        delta = rec["stocks"] - rows[i - 1]["stocks"]
        rec["wow"] = delta
        wow.append(delta)
        if i >= LOOKBACK_WOW + 1 and all(wow[j] is not None for j in range(i - LOOKBACK_WOW, i)):
            expected = sum(wow[j] for j in range(i - LOOKBACK_WOW, i)) / LOOKBACK_WOW
            rec["surprise"] = delta - expected
        else:
            rec["surprise"] = 0.0
        rec["wow_scaled"] = rec["wow"] / SCALE
        rec["surprise_scaled"] = rec["surprise"] / SCALE
    if rows:
        rows[0]["wow_scaled"] = 0.0
        rows[0]["surprise_scaled"] = 0.0
    return rows


def attach_inv(rets: list[dict], inv: list[dict]) -> dict:
    releases = [r["release_date"] for r in inv]
    j = -1
    n = len(inv)
    for rec in rets:
        d = rec["date"]
        while j + 1 < n and releases[j + 1] <= d:
            j += 1
        if j < 0:
            rec["inv"] = {"H-CL-INV-SURP": 0.0, "H-CL-INV-WOW": 0.0}
            rec["inv_release"] = None
        else:
            rec["inv"] = {
                "H-CL-INV-SURP": float(inv[j]["surprise_scaled"]),
                "H-CL-INV-WOW": float(inv[j]["wow_scaled"]),
            }
            rec["inv_release"] = inv[j]["release_date"]
    span_first = rets[0]["date"] if rets else ""
    span_last = rets[-1]["date"] if rets else ""
    n_reports_span = (
        sum(1 for r in inv if span_first <= r["release_date"] <= span_last) if rets else 0
    )
    n_nonzero = sum(1 for r in rets if r["inv"]["H-CL-INV-SURP"] != 0.0)
    return {
        "n_reports": len(inv),
        "n_reports_in_session_span": n_reports_span,
        "n_sessions": len(rets),
        "n_sessions_with_nonzero_surprise": n_nonzero,
        "span_first": span_first or None,
        "span_last": span_last or None,
        "first_week": inv[0]["week_ending"] if inv else None,
        "last_week": inv[-1]["week_ending"] if inv else None,
        "scale": SCALE,
        "lookback_wow": LOOKBACK_WOW,
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


def _inv_lag_index(kind: str, t: int) -> int | None:
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
            s_idx = _inv_lag_index(kind, t)
            s = 0.0 if s_idx is None else float(rets[s_idx]["inv"].get(key, 0.0))
            x_full = x_cl + [s]
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
                "reason": "lowest discovery F-CC RMSE among horses that strictly beat 0; ties keep H-CL-INV-SURP",
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


def build_rets(clf_path: str, cutoff: str | None, inv: list[dict]) -> tuple[list[dict], dict]:
    rows = load_clf(clf_path)
    if cutoff is not None:
        rows = [r for r in rows if r["date"] <= cutoff]
    rets = session_returns(rows)
    coverage = attach_inv(rets, inv)
    return rets, coverage


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default=str(here / "data" / "clf_yahoo_standin.csv"))
    p.add_argument("--inv", default=str(here / "data" / "eia_weekly_crude_exspr.csv"))
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--discovery-cutoff", default=DISCOVERY_CUTOFF)
    p.add_argument("--discovery-holdout", type=int, default=500)
    p.add_argument("--min-reports", type=int, default=MIN_REPORTS)
    p.add_argument("--phase", choices=["discovery", "confirm", "all"], default="all")
    p.add_argument("--out", default=str(here / "data" / "cl_inv_hunt_scores.json"))
    args = p.parse_args()

    inv_path = Path(args.inv)
    if not inv_path.exists():
        raise SystemExit(f"missing {inv_path}; run fetch_eia_inventory.py first")
    inv = load_inventory(inv_path)
    payload: dict = {
        "badge": "stand-in",
        "lock": "L-HUNT-CL-INV",
        "tells": "L-STANDIN-EIA-INV-CL",
        "discovery_cutoff": args.discovery_cutoff,
        "discovery_holdout": args.discovery_holdout,
        "min_train": args.min_train,
        "scale": SCALE,
        "surprise": "wow minus mean of prior 4 wow; not Bloomberg consensus",
        "horse_order": [h["id"] for h in HORSES],
        "n_reports": len(inv),
        "refused_prior": [
            "H-LAG-WF",
            "H-SPARSE-CAL",
            "H-SPARSE-VOL",
            "H-GAP-FADE",
            "H-GAP-CONT",
            "L-HUNT-PRETELL",
            "L-HUNT-DJT",
            "L-HUNT-COT",
        ],
    }

    if args.phase in ("discovery", "all"):
        disc_rets, cov = build_rets(args.clf, args.discovery_cutoff, inv)
        payload["discovery_coverage"] = cov
        n_rep = int(cov.get("n_reports_in_session_span") or 0)
        if n_rep < args.min_reports:
            payload["survivor"] = {
                "id": None,
                "reason": (
                    f"vehicle too thin: {n_rep} inventory reports "
                    f"in discovery session span (need {args.min_reports})"
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
        if hid is None or payload.get("vehicle_fail"):
            payload["confirm"] = None
            payload["promote"] = {
                "fires": False,
                "reason": survivor.get("reason") or "no discovery survivor",
            }
        else:
            spec = next(h for h in HORSES if h["id"] == hid)
            full_rets, cov = build_rets(args.clf, None, inv)
            payload["confirm_coverage"] = cov
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
