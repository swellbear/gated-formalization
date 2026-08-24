#!/usr/bin/env python3
"""Named finite discovery/confirm EIA spot expanding-window logistic (Track B).

Protocol frozen in Lock_Hunt_Spot_Logit.md *before* last-500 confirm scores.

Two horses (train arm used):
  H-SPOT-LOGIT-FULL — intercept + sign_num + abs_r21
  H-SPOT-LOGIT-SIGN — intercept + sign_num

Past-only expanding window: train on eligible u with date(u+21) < date(t).
Min train 50; fit failure → continuation. Pick one per board only if it
strictly beats continuation on discovery.

Does not unburn prior horses. Does not retune W2B. Does not change 21.
Does not download. Not a trade.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

DISCOVERY_CUTOFF = "2023-08-21"
HORIZON = 21
MIN_DISCOVERY_ELIGIBLE = 250
MIN_TRAIN = 50
MIN_SUCCESSFUL_FITS_ON_DISC_500 = 250
HORSES = ["H-SPOT-LOGIT-FULL", "H-SPOT-LOGIT-SIGN"]
BURNED = {
    "H-SPOT-FLIP-HOLD",
    "H-SPOT-REV",
    "H-SPOT-INV-CONT",
    "H-SPOT-INV-FADE",
    "H-SPOT-CROSS-B2W",
}
ACTIVE_PULSE = "L-HUNT-SPOT-LOGIT"
BOARDS = ("WTI", "Brent")
MAX_IRLS = 25
EPS = 1e-12


def sign_of(x: float) -> str:
    if x > 0:
        return "Up"
    if x < 0:
        return "Down"
    return "Flat"


def load_spot(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            p = float(rec["price"])
            if p <= 0:
                continue
            rows.append({"date": rec["date"].strip(), "price": p})
    rows.sort(key=lambda r: r["date"])
    return rows


def annotate_spot(raw: list[dict]) -> list[dict]:
    n = len(raw)
    out = []
    for i, rec in enumerate(raw):
        item = {
            "i": i,
            "date": rec["date"],
            "price": rec["price"],
            "sign": None,
            "sign_lag": None,
            "r21": None,
            "abs_r21": None,
            "sign_num": None,
            "truth": None,
            "outcome_date": None,
        }
        if i >= HORIZON and rec["price"] > 0 and raw[i - HORIZON]["price"] > 0:
            r = math.log(rec["price"] / raw[i - HORIZON]["price"])
            item["r21"] = r
            item["abs_r21"] = abs(r)
            item["sign"] = sign_of(r)
            if item["sign"] == "Up":
                item["sign_num"] = 1.0
            elif item["sign"] == "Down":
                item["sign_num"] = -1.0
        if i - 1 >= HORIZON and raw[i - 1]["price"] > 0 and raw[i - 1 - HORIZON]["price"] > 0:
            item["sign_lag"] = sign_of(
                math.log(raw[i - 1]["price"] / raw[i - 1 - HORIZON]["price"])
            )
        if i + HORIZON < n and rec["price"] > 0 and raw[i + HORIZON]["price"] > 0:
            item["truth"] = sign_of(math.log(raw[i + HORIZON]["price"] / rec["price"]))
            item["outcome_date"] = raw[i + HORIZON]["date"]
        out.append(item)
    return out


def eligible(rows: list[dict]) -> list[dict]:
    return [
        r
        for r in rows
        if r["i"] >= HORIZON + 1
        and r["sign"] in {"Up", "Down"}
        and r["sign_lag"] in {"Up", "Down"}
        and r["truth"] in {"Up", "Down"}
        and r["sign_num"] is not None
        and r["abs_r21"] is not None
        and r["outcome_date"] is not None
    ]


def design_row(rec: dict, horse: str) -> np.ndarray:
    if horse == "H-SPOT-LOGIT-FULL":
        return np.array([1.0, rec["sign_num"], rec["abs_r21"]], dtype=float)
    if horse == "H-SPOT-LOGIT-SIGN":
        return np.array([1.0, rec["sign_num"]], dtype=float)
    raise KeyError(horse)


def fit_logit(X: np.ndarray, y: np.ndarray) -> np.ndarray | None:
    n, p = X.shape
    if n < MIN_TRAIN or p < 1:
        return None
    if np.unique(y).size < 2:
        return None
    beta = np.zeros(p, dtype=float)
    for _ in range(MAX_IRLS):
        eta = X @ beta
        eta = np.clip(eta, -30.0, 30.0)
        mu = 1.0 / (1.0 + np.exp(-eta))
        w = mu * (1.0 - mu)
        w = np.maximum(w, EPS)
        z = eta + (y - mu) / w
        WX = X * w[:, None]
        try:
            xtwx = X.T @ WX
            xtwz = X.T @ (w * z)
            # Tiny ridge for numerical invertibility only (not a free hyperparameter).
            xtwx = xtwx + (1e-8) * np.eye(p)
            beta_new = np.linalg.solve(xtwx, xtwz)
        except np.linalg.LinAlgError:
            return None
        if not np.all(np.isfinite(beta_new)):
            return None
        if np.max(np.abs(beta_new - beta)) < 1e-8:
            return beta_new
        beta = beta_new
    if not np.all(np.isfinite(beta)):
        return None
    return beta


def predict_call(beta: np.ndarray | None, x: np.ndarray, continuation: str) -> tuple[str, bool]:
    if beta is None:
        return continuation, False
    eta = float(np.dot(beta, x))
    if not math.isfinite(eta):
        return continuation, False
    eta = max(-30.0, min(30.0, eta))
    p_up = 1.0 / (1.0 + math.exp(-eta))
    if p_up >= 0.5:
        return "Up", True
    return "Down", True


def walk_forward_calls(elig: list[dict]) -> dict[str, list[dict]]:
    """Return parallel lists of call records per horse, same order as elig."""
    out = {hid: [] for hid in HORSES}
    # Eligible rows sorted by date. Train = earlier elig rows whose next-21
    # outcome print is strictly before the call date.
    matured = 0
    for j, rec in enumerate(elig):
        t_date = rec["date"]
        while matured < j and elig[matured]["outcome_date"] < t_date:
            matured += 1
        train = elig[:matured]
        for hid in HORSES:
            cont = rec["sign"]
            if len(train) < MIN_TRAIN:
                call, fitted = cont, False
            else:
                X = np.vstack([design_row(u, hid) for u in train])
                y = np.array([1.0 if u["truth"] == "Up" else 0.0 for u in train], dtype=float)
                beta = fit_logit(X, y)
                call, fitted = predict_call(beta, design_row(rec, hid), cont)
            out[hid].append(
                {
                    "date": rec["date"],
                    "truth": rec["truth"],
                    "continuation": cont,
                    "call": call,
                    "fitted": fitted,
                    "n_train": len(train),
                }
            )
    return out


def hit_rate_from_calls(calls: list[dict], use_continuation: bool = False) -> dict:
    if not calls:
        return {"n": 0, "hits": 0, "hit_rate": None, "first": None, "last": None, "n_fitted": 0}
    hits = 0
    n_fitted = 0
    for c in calls:
        pred = c["continuation"] if use_continuation else c["call"]
        if pred == c["truth"]:
            hits += 1
        if c.get("fitted"):
            n_fitted += 1
    n = len(calls)
    return {
        "n": n,
        "hits": hits,
        "hit_rate": hits / n,
        "first": calls[0]["date"],
        "last": calls[-1]["date"],
        "n_fitted": n_fitted,
    }


def last_n(rows: list, n: int):
    return rows[-n:] if n > 0 and len(rows) >= n else list(rows)


def prefix_cutoff_calls(calls: list[dict], cutoff: str) -> list[dict]:
    return [c for c in calls if c["date"] <= cutoff]


def pick_survivor(horses: dict) -> dict:
    beat = [hid for hid in HORSES if horses[hid].get("beats_continuation")]
    if not beat:
        return {"id": None, "reason": "no horse strictly beat continuation on discovery"}
    best = beat[0]
    best_hr = horses[best]["hit_rate"]
    for hid in beat[1:]:
        hr = horses[hid]["hit_rate"]
        if hr > best_hr:
            best, best_hr = hid, hr
    return {"id": best, "reason": "strictly beat continuation; ties keep H-SPOT-LOGIT-FULL"}


def score_board(elig: list[dict], calls_by_horse: dict, holdouts: list[int]) -> dict:
    # Align continuation from any horse list
    base_calls = calls_by_horse[HORSES[0]]
    disc_pool = prefix_cutoff_calls(base_calls, DISCOVERY_CUTOFF)
    disc_board = last_n(disc_pool, 500)
    disc_dates = {c["date"] for c in disc_board}

    continuation = hit_rate_from_calls(disc_board, use_continuation=True)
    horses = {}
    for hid in HORSES:
        disc_h = [c for c in calls_by_horse[hid] if c["date"] in disc_dates]
        # Preserve date order of disc_board
        by_date = {c["date"]: c for c in disc_h}
        disc_h = [by_date[c["date"]] for c in disc_board]
        h = hit_rate_from_calls(disc_h)
        h["beats_continuation"] = (
            h["hit_rate"] is not None
            and continuation["hit_rate"] is not None
            and h["hit_rate"] > continuation["hit_rate"]
        )
        horses[hid] = h
    survivor = pick_survivor(horses)
    n_fitted = horses[HORSES[0]]["n_fitted"]
    confirm = None
    if survivor["id"] is not None and holdouts:
        confirm = {}
        for n in holdouts:
            window = last_n(calls_by_horse[survivor["id"]], n)
            confirm[str(n)] = {
                "horse": hit_rate_from_calls(window),
                "continuation": hit_rate_from_calls(window, use_continuation=True),
            }
            hr = confirm[str(n)]["horse"]["hit_rate"]
            cr = confirm[str(n)]["continuation"]["hit_rate"]
            confirm[str(n)]["beats_continuation"] = (
                hr is not None and cr is not None and hr > cr
            )
    return {
        "n_prints": elig[-1]["i"] + 1 if elig else 0,
        "n_eligible": len(elig),
        "n_discovery_pool": len(disc_pool),
        "vehicle_fail": len(disc_pool) < MIN_DISCOVERY_ELIGIBLE
        or n_fitted < MIN_SUCCESSFUL_FITS_ON_DISC_500,
        "span_first": elig[0]["date"] if elig else None,
        "span_last": elig[-1]["date"] if elig else None,
        "min_train": MIN_TRAIN,
        "discovery": {
            "cutoff": DISCOVERY_CUTOFF,
            "n_pool": len(disc_pool),
            "n_scoreboard": len(disc_board),
            "first": disc_board[0]["date"] if disc_board else None,
            "last": disc_board[-1]["date"] if disc_board else None,
            "n_fitted_full_on_scoreboard": n_fitted,
            "continuation": continuation,
            "horses": horses,
            "survivor": survivor,
        },
        "confirm": confirm,
    }


def refuse_queue(_queue: dict) -> None:
    for hid in HORSES:
        if hid in BURNED:
            raise SystemExit(f"active horse {hid} is on the burned list")


def update_queue_after_discovery(queue: dict, boards: dict) -> dict:
    burned = list(queue.get("burned") or [])
    existing = {(b.get("horse"), b.get("scoreboard")) for b in burned}
    for board, payload in boards.items():
        if payload.get("vehicle_fail"):
            continue
        for hid in HORSES:
            if payload["discovery"]["horses"][hid]["beats_continuation"]:
                continue
            key = (hid, board)
            if key in existing:
                continue
            burned.append(
                {
                    "horse": hid,
                    "scoreboard": board,
                    "status": "burned_discovery_loss",
                    "note": "Failed to strictly beat continuation on discovery. Do not retune.",
                }
            )
            existing.add(key)
    nxt = []
    for row in queue.get("next") or []:
        if row.get("id") == "C-SPOT-LOGIT":
            continue
        nxt.append(row)
    out = dict(queue)
    out["pulse"] = ACTIVE_PULSE
    out["lock"] = "Lock_Hunt_Spot_Logit.md"
    out["active_horses"] = HORSES
    out["burned"] = burned
    out["next"] = nxt
    out["last_discovery"] = {
        board: payload["discovery"]["survivor"] for board, payload in boards.items()
    }
    return out


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(here / "data"))
    ap.add_argument("--stage", choices=("discovery", "confirm", "all"), default="all")
    ap.add_argument("--queue", default=str(here / "data" / "spot_trend_queue.json"))
    args = ap.parse_args()
    data = Path(args.data_dir)
    queue_path = Path(args.queue)
    queue = json.loads(queue_path.read_text()) if queue_path.exists() else {}
    refuse_queue(queue)

    holdouts = [500, 250, 750] if args.stage in {"confirm", "all"} else []
    boards = {}
    vehicle_fail = False
    for name, fname in (("WTI", "eia_spot_wti.csv"), ("Brent", "eia_spot_brent.csv")):
        path = data / fname
        if not path.exists():
            raise SystemExit(f"missing {path}; run fetch_eia_spot.py first")
        elig = eligible(annotate_spot(load_spot(path)))
        calls = walk_forward_calls(elig)
        scored = score_board(elig, calls, holdouts)
        if args.stage == "discovery":
            scored["confirm"] = None
            scored["confirm_deferred"] = True
        boards[name] = scored
        if scored["vehicle_fail"]:
            vehicle_fail = True

    if args.stage in {"discovery", "all"} and not vehicle_fail:
        queue = update_queue_after_discovery(queue, boards)

    any_survivor = any(boards[b]["discovery"]["survivor"]["id"] is not None for b in BOARDS)
    if args.stage == "discovery" or (args.stage == "all" and not any_survivor):
        for b in BOARDS:
            boards[b]["confirm"] = None

    out = {
        "lock": ACTIVE_PULSE,
        "stage": args.stage,
        "discovery_cutoff": DISCOVERY_CUTOFF,
        "horizon_price_steps": HORIZON,
        "train_arm": "expanding past-only logistic; outcome_date < t; min_train 50",
        "features": {
            "FULL": "intercept + sign_num(+1/-1) + abs_r21",
            "SIGN": "intercept + sign_num(+1/-1)",
        },
        "select_arm": "discovery last 500 of prefix <= 2023-08-21",
        "confirm_arm": "last 500/250/750; never train; skipped if no survivor",
        "refused_burned": sorted(BURNED),
        "vehicle_fail": vehicle_fail,
        "boards": boards,
        "queue_still_queued": [row.get("id") for row in (queue.get("next") or [])],
    }
    (data / "spot_logit_hunt_scores.json").write_text(json.dumps(out, indent=2) + "\n")
    queue_path.write_text(json.dumps(queue, indent=2) + "\n")
    summary = {
        "vehicle_fail": vehicle_fail,
        "stage": args.stage,
        "boards": {
            b: {
                "n_eligible": boards[b]["n_eligible"],
                "discovery_n": boards[b]["discovery"]["n_scoreboard"],
                "n_fitted_on_discovery_500": boards[b]["discovery"]["n_fitted_full_on_scoreboard"],
                "continuation": boards[b]["discovery"]["continuation"]["hit_rate"],
                "horses": {hid: boards[b]["discovery"]["horses"][hid]["hit_rate"] for hid in HORSES},
                "survivor": boards[b]["discovery"]["survivor"]["id"],
                "confirm_ran": boards[b]["confirm"] is not None,
            }
            for b in BOARDS
        },
    }
    print(json.dumps(summary, indent=2))
    return 1 if vehicle_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
