#!/usr/bin/env python3
"""Named finite discovery/confirm pre-tell hunt on Yahoo stand-in tells.

Protocol frozen in Lock_Hunt_Pretell.md *before* last-500 confirm scores.

Discovery: CL dates <= 2023-08-21; pick the single F-CC winner among eight
named horses only if it strictly beats 0 on the last 500 of that prefix.
Confirm: that one horse only, last 500/250/750 vs 0. No runner-up on confirm.

Tell lag (mandatory): F-ON/F-CC use r_tell ending on CL date t-2;
F-DAY uses r_tell ending on CL date t-1.

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

TELL_FILES = {
    "DXY": "tell_dxy.csv",
    "RBOB": "tell_rbob.csv",
    "HO": "tell_ho.csv",
    "SPX": "tell_spx.csv",
    "HG": "tell_hg.csv",
    "TNX": "tell_tnx.csv",
}

# Locked drawer order (tie-break = earlier row).
HORSES = [
    {"id": "H-TELL-DXY", "tells": ["DXY"], "sparse": False},
    {"id": "H-TELL-RBOB", "tells": ["RBOB"], "sparse": False},
    {"id": "H-TELL-HO", "tells": ["HO"], "sparse": False},
    {"id": "H-TELL-SPX", "tells": ["SPX"], "sparse": False},
    {"id": "H-TELL-HG", "tells": ["HG"], "sparse": False},
    {"id": "H-TELL-TNX", "tells": ["TNX"], "sparse": False},
    {"id": "H-TELL-AND-DXY-RBOB", "tells": ["DXY", "RBOB"], "sparse": True},
    {"id": "H-TELL-AND-RBOB-HO", "tells": ["RBOB", "HO"], "sparse": True},
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


def load_tell_closes(path: Path) -> list[tuple[str, float]]:
    bars = []
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            c = float(rec["close"])
            if c <= 0:
                continue
            bars.append((rec["date"].strip(), c))
    bars.sort(key=lambda x: x[0])
    return bars


def asof_closes(cl_dates: list[str], bars: list[tuple[str, float]]) -> dict[str, float | None]:
    j = 0
    last: float | None = None
    out: dict[str, float | None] = {}
    for d in cl_dates:
        while j < len(bars) and bars[j][0] <= d:
            last = bars[j][1]
            j += 1
        out[d] = last
    return out


def attach_tell_returns(
    rets: list[dict],
    clf_dates: list[str],
    tell_map: dict[str, dict[str, float | None]],
) -> None:
    """Attach r_<id> on each session = log(asof[d] / asof[prev_clf_date])."""
    date_to_prev: dict[str, str | None] = {}
    prev = None
    for d in clf_dates:
        date_to_prev[d] = prev
        prev = d
    for rec in rets:
        d = rec["date"]
        rec["tells"] = {}
        p = date_to_prev.get(d)
        for tid, asof in tell_map.items():
            cur_c = asof.get(d)
            prev_c = asof.get(p) if p is not None else None
            if cur_c is None or prev_c is None or cur_c <= 0 or prev_c <= 0:
                rec["tells"][tid] = None
            else:
                rec["tells"][tid] = math.log(cur_c / prev_c)


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


def _tell_lag_index(kind: str, t: int) -> int | None:
    # F-ON/F-CC: r_tell ending on t-2; F-DAY: ending on t-1.
    if kind in ("on", "cc"):
        idx = t - 2
    else:
        idx = t - 1
    if idx < 0:
        return None
    return idx


def walk_forward_horse(
    rets: list[dict],
    holdout: int,
    min_train: int,
    spec: dict,
) -> dict:
    n = len(rets)
    oos_start = max(min_train, n - holdout)
    tell_ids: list[str] = spec["tells"]
    sparse = spec["sparse"]
    out: dict = {}
    for kind, label in [("on", "F-ON"), ("day", "F-DAY"), ("cc", "F-CC")]:
        actuals: list[float] = []
        preds: list[float] = []
        dates: list[str] = []
        n_trig = 0
        n_missing_tell = 0
        y_hist: list[float] = []
        X_hist: list[list[float]] = []
        for t in range(1, n):
            cur, lag = rets[t], rets[t - 1]
            y, x_cl = _cl_xy(kind, cur, lag)
            if y is None or x_cl is None:
                continue
            t_idx = _tell_lag_index(kind, t)
            tell_vals: list[float | None] = []
            if t_idx is None:
                tell_vals = [None] * len(tell_ids)
            else:
                src = rets[t_idx]
                tell_vals = [src.get("tells", {}).get(tid) for tid in tell_ids]
            complete = all(v is not None for v in tell_vals)
            if sparse:
                if complete and all(v != 0.0 for v in tell_vals):
                    signs = [math.copysign(1.0, v) for v in tell_vals]  # type: ignore[arg-type]
                    trig = all(s == signs[0] for s in signs)
                else:
                    trig = False
            else:
                trig = complete
            x_full = None
            if complete:
                x_full = x_cl + [float(v) for v in tell_vals]  # type: ignore[arg-type]
            if t >= oos_start:
                if (not sparse and complete) or (sparse and trig and complete):
                    pred = ols_forecast(
                        np.array(y_hist, float),
                        np.array(X_hist, float),
                        np.array(x_full, float),
                    )
                    if sparse:
                        n_trig += 1
                else:
                    pred = 0.0
                    if not complete:
                        n_missing_tell += 1
                actuals.append(y)
                preds.append(pred)
                dates.append(cur["date"])
            if x_full is not None:
                y_hist.append(y)
                X_hist.append(x_full)
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
            "n_missing_tell_oos": n_missing_tell,
        }
        if sparse:
            row["n_triggered"] = n_trig
        out[label] = row
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
    best_rmse = min(r for _, r in beat)
    # Tie-break: earliest in locked table among those with best_rmse.
    for hid, r in beat:
        if r == best_rmse:
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


def build_rets(clf_path: str, data_dir: Path, cutoff: str | None) -> list[dict]:
    rows = load_clf(clf_path)
    if cutoff is not None:
        rows = [r for r in rows if r["date"] <= cutoff]
    clf_dates = [r["date"] for r in rows]
    rets = session_returns(rows)
    tell_map = {}
    for tid, fname in TELL_FILES.items():
        bars = load_tell_closes(data_dir / fname)
        tell_map[tid] = asof_closes(clf_dates, bars)
    attach_tell_returns(rets, clf_dates, tell_map)
    return rets


def score_drawer(rets: list[dict], holdout: int, min_train: int) -> dict:
    out = {}
    for spec in HORSES:
        out[spec["id"]] = walk_forward_horse(rets, holdout, min_train, spec)
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--clf", default="data/clf_yahoo_standin.csv")
    p.add_argument("--data-dir", default="data")
    p.add_argument("--min-train", type=int, default=250)
    p.add_argument("--discovery-cutoff", default=DISCOVERY_CUTOFF)
    p.add_argument("--discovery-holdout", type=int, default=500)
    p.add_argument("--phase", choices=["discovery", "confirm", "all"], default="all")
    p.add_argument("--out", default="data/pretell_hunt_scores.json")
    args = p.parse_args()

    data_dir = Path(args.data_dir)
    payload: dict = {
        "badge": "stand-in",
        "lock": "L-HUNT-PRETELL",
        "tells": "L-STANDIN-Y-TELLS",
        "discovery_cutoff": args.discovery_cutoff,
        "discovery_holdout": args.discovery_holdout,
        "min_train": args.min_train,
        "horse_order": [h["id"] for h in HORSES],
    }

    if args.phase in ("discovery", "all"):
        disc_rets = build_rets(args.clf, data_dir, args.discovery_cutoff)
        discovery = score_drawer(disc_rets, args.discovery_holdout, args.min_train)
        survivor = pick_survivor(discovery)
        payload["discovery_n_sessions"] = len(disc_rets)
        payload["discovery"] = discovery
        payload["survivor"] = survivor
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
            spec = next(h for h in HORSES if h["id"] == hid)
            full_rets = build_rets(args.clf, data_dir, cutoff=None)
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
