#!/usr/bin/env python3
"""Named finite discovery/confirm CFTC managed-money WTI hunt.

Protocol frozen in Lock_Hunt_COT.md *before* last-500 confirm scores.

Two horses: H-COT-NET (carried MM net / 1e5) and H-COT-CHG (week change / 1e5).
Pick one on discovery F-CC only if it strictly beats 0.

Tell lag: F-ON/F-CC use COT known as of CL date t-2; F-DAY uses t-1.
Known as of = latest report whose Friday release_date <= lagged date.

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
SCALE = 1e5
HORSES = [
    {"id": "H-COT-NET", "field": "net_scaled"},
    {"id": "H-COT-CHG", "field": "chg_scaled"},
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


def load_cot(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            net = float(rec["mm_net"])
            rows.append(
                {
                    "report_date": rec["report_date"].strip(),
                    "release_date": rec["release_date"].strip(),
                    "mm_net": net,
                }
            )
    rows.sort(key=lambda r: r["release_date"])
    prev = None
    for rec in rows:
        rec["net_scaled"] = rec["mm_net"] / SCALE
        rec["chg_scaled"] = 0.0 if prev is None else (rec["mm_net"] - prev) / SCALE
        prev = rec["mm_net"]
    return rows


def attach_cot(rets: list[dict], cot: list[dict]) -> dict:
    releases = [c["release_date"] for c in cot]
    j = -1
    n = len(cot)
    for rec in rets:
        d = rec["date"]
        while j + 1 < n and releases[j + 1] <= d:
            j += 1
        rec["cot"] = {
            "H-COT-NET": 0.0 if j < 0 else float(cot[j]["net_scaled"]),
            "H-COT-CHG": 0.0 if j < 0 else float(cot[j]["chg_scaled"]),
        }
        rec["cot_release"] = None if j < 0 else cot[j]["release_date"]
    n_nonzero_net = sum(1 for r in rets if r["cot"]["H-COT-NET"] != 0.0)
    n_nonzero_chg = sum(1 for r in rets if r["cot"]["H-COT-CHG"] != 0.0)
    span_first = rets[0]["date"] if rets else ""
    span_last = rets[-1]["date"] if rets else ""
    n_reports_span = sum(1 for c in cot if span_first <= c["release_date"] <= span_last) if rets else 0
    return {
        "n_reports": len(cot),
        "n_reports_in_session_span": n_reports_span,
        "n_sessions": len(rets),
        "n_sessions_with_net": n_nonzero_net,
        "n_sessions_with_chg": n_nonzero_chg,
        "span_first": span_first or None,
        "span_last": span_last or None,
        "first_report": cot[0]["report_date"] if cot else None,
        "last_report": cot[-1]["report_date"] if cot else None,
        "scale": SCALE,
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


def _cot_lag_index(kind: str, t: int) -> int | None:
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
            s_idx = _cot_lag_index(kind, t)
            s = 0.0 if s_idx is None else float(rets[s_idx]["cot"].get(key, 0.0))
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


def build_rets(clf_path: str, cutoff: str | None, cot: list[dict]) -> tuple[list[dict], dict]:
    rows = load_clf(clf_path)
    if cutoff is not None:
        rows = [r for r in rows if r["date"] <= cutoff]
    rets = session_returns(rows)
    coverage = attach_cot(rets, cot)
    return rets, coverage


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default="data/clf_yahoo_standin.csv")
    p.add_argument("--cot", default="data/cftc_cl_mm_net.csv")
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--discovery-cutoff", default=DISCOVERY_CUTOFF)
    p.add_argument("--discovery-holdout", type=int, default=500)
    p.add_argument("--min-reports", type=int, default=30)
    p.add_argument("--phase", choices=["discovery", "confirm", "all"], default="all")
    p.add_argument("--out", default="data/cot_hunt_scores.json")
    args = p.parse_args()

    cot = load_cot(Path(args.cot))
    payload: dict = {
        "badge": "stand-in",
        "lock": "L-HUNT-COT",
        "tells": "L-STANDIN-CFTC-COT",
        "discovery_cutoff": args.discovery_cutoff,
        "discovery_holdout": args.discovery_holdout,
        "min_train": args.min_train,
        "scale": SCALE,
        "horse_order": [h["id"] for h in HORSES],
        "n_reports": len(cot),
    }

    if args.phase in ("discovery", "all"):
        disc_rets, cov = build_rets(args.clf, args.discovery_cutoff, cot)
        payload["discovery_coverage"] = cov
        n_rep = int(cov.get("n_reports_in_session_span") or 0)
        if n_rep < args.min_reports:
            payload["survivor"] = {
                "id": None,
                "reason": (
                    f"vehicle too thin: {n_rep} COT reports "
                    f"in discovery session span (need {args.min_reports})"
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
            full_rets, cov = build_rets(args.clf, None, cot)
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
