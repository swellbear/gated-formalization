#!/usr/bin/env python3
"""Named finite discovery/confirm EIA spot 21-day trend hunt (Track B).

Protocol frozen in Lock_Hunt_Spot_Trend.md *before* last-500 confirm scores.

Two horses: H-SPOT-FLIP-HOLD (call sign as of t-1) and H-SPOT-REV (opposite of t).
Baseline continuation is not a horse. Pick one per scoreboard only if it
strictly beats continuation on discovery.

Three arms: train = N/A for these rules; select = discovery; confirm never trains.
Queued classes in data/spot_trend_queue.json are refused this pulse.

Does not download. Does not treat spots as CL/ICE futures. Not a trade.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

DISCOVERY_CUTOFF = "2023-08-21"
HORIZON = 21
MIN_DISCOVERY_ELIGIBLE = 250
HORSES = ["H-SPOT-FLIP-HOLD", "H-SPOT-REV"]
ACTIVE_PULSE = "L-HUNT-SPOT-TREND"
BOARDS = ("WTI", "Brent")


def sign_of(x: float) -> str:
    if x > 0:
        return "Up"
    if x < 0:
        return "Down"
    return "Flat"


def opposite(label: str) -> str:
    if label == "Up":
        return "Down"
    if label == "Down":
        return "Up"
    return "Flat"


def load_spot(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            d = rec["date"].strip()
            p = float(rec["price"])
            if p <= 0:
                continue
            rows.append({"date": d, "price": p})
    rows.sort(key=lambda r: r["date"])
    return rows


def annotate(rows: list[dict]) -> list[dict]:
    n = len(rows)
    out = []
    for i, rec in enumerate(rows):
        item = {
            "i": i,
            "date": rec["date"],
            "price": rec["price"],
            "r21": None,
            "sign": None,
            "sign_lag": None,
            "flip": False,
            "r21_fwd": None,
            "truth": None,
        }
        if i >= HORIZON and rec["price"] > 0 and rows[i - HORIZON]["price"] > 0:
            item["r21"] = math.log(rec["price"] / rows[i - HORIZON]["price"])
            item["sign"] = sign_of(item["r21"])
        if i - 1 >= HORIZON and rows[i - 1]["price"] > 0 and rows[i - 1 - HORIZON]["price"] > 0:
            r_lag = math.log(rows[i - 1]["price"] / rows[i - 1 - HORIZON]["price"])
            item["sign_lag"] = sign_of(r_lag)
        if item["sign"] in {"Up", "Down"} and item["sign_lag"] in {"Up", "Down"}:
            item["flip"] = item["sign"] != item["sign_lag"]
        if i + HORIZON < n and rec["price"] > 0 and rows[i + HORIZON]["price"] > 0:
            item["r21_fwd"] = math.log(rows[i + HORIZON]["price"] / rec["price"])
            item["truth"] = sign_of(item["r21_fwd"])
        out.append(item)
    return out


def eligible(rows: list[dict]) -> list[dict]:
    """Unified skip mask from the lock: history, realized next-21, no Flats."""
    return [
        r
        for r in rows
        if r["i"] >= HORIZON + 1
        and r["sign"] in {"Up", "Down"}
        and r["sign_lag"] in {"Up", "Down"}
        and r["truth"] in {"Up", "Down"}
    ]


def call_for(horse: str, rec: dict) -> str:
    if horse == "H-SPOT-FLIP-HOLD":
        return rec["sign_lag"]
    if horse == "H-SPOT-REV":
        return opposite(rec["sign"])
    if horse == "continuation":
        return rec["sign"]
    raise KeyError(horse)


def hit_rate(rows: list[dict], horse: str) -> dict:
    if not rows:
        return {"n": 0, "hits": 0, "hit_rate": None, "first": None, "last": None}
    hits = 0
    for rec in rows:
        if call_for(horse, rec) == rec["truth"]:
            hits += 1
    n = len(rows)
    return {
        "n": n,
        "hits": hits,
        "hit_rate": hits / n,
        "first": rows[0]["date"],
        "last": rows[-1]["date"],
    }


def last_n(rows: list[dict], n: int) -> list[dict]:
    if n <= 0:
        return []
    return rows[-n:] if len(rows) >= n else list(rows)


def prefix_cutoff(rows: list[dict], cutoff: str) -> list[dict]:
    return [r for r in rows if r["date"] <= cutoff]


def score_board(rows: list[dict], holdouts: list[int]) -> dict:
    elig = eligible(rows)
    disc_pool = prefix_cutoff(elig, DISCOVERY_CUTOFF)
    disc_board = last_n(disc_pool, 500)
    continuation = hit_rate(disc_board, "continuation")
    horses = {}
    for hid in HORSES:
        h = hit_rate(disc_board, hid)
        h["beats_continuation"] = (
            h["hit_rate"] is not None
            and continuation["hit_rate"] is not None
            and h["hit_rate"] > continuation["hit_rate"]
        )
        horses[hid] = h
    survivor = pick_survivor(horses)
    confirm = None
    if survivor["id"] is not None and holdouts:
        confirm = {}
        for n in holdouts:
            window = last_n(elig, n)
            confirm[str(n)] = {
                "horse": hit_rate(window, survivor["id"]),
                "continuation": hit_rate(window, "continuation"),
            }
            hr = confirm[str(n)]["horse"]["hit_rate"]
            cr = confirm[str(n)]["continuation"]["hit_rate"]
            confirm[str(n)]["beats_continuation"] = (
                hr is not None and cr is not None and hr > cr
            )
    return {
        "n_prints": len(rows),
        "n_eligible": len(elig),
        "n_discovery_pool": len(disc_pool),
        "vehicle_fail": len(disc_pool) < MIN_DISCOVERY_ELIGIBLE,
        "span_first": rows[0]["date"] if rows else None,
        "span_last": rows[-1]["date"] if rows else None,
        "discovery": {
            "cutoff": DISCOVERY_CUTOFF,
            "n_pool": len(disc_pool),
            "n_scoreboard": len(disc_board),
            "first": disc_board[0]["date"] if disc_board else None,
            "last": disc_board[-1]["date"] if disc_board else None,
            "continuation": continuation,
            "horses": horses,
            "survivor": survivor,
        },
        "confirm": confirm,
        "dashboard": dashboard,
    }


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
        elif hr == best_hr:
            # tie: keep earlier lock order (FLIP-HOLD is first)
            pass
    return {"id": best, "reason": "strictly beat continuation; ties keep H-SPOT-FLIP-HOLD"}


def refuse_queued(queue: dict) -> None:
    active = set(queue.get("active_horses") or [])
    if active and set(HORSES) != active:
        raise SystemExit(f"queue active_horses {sorted(active)} != pulse {HORSES}")
    burned = queue.get("burned") or []
    for row in burned:
        hid = (row or {}).get("horse")
        if hid in HORSES and (row or {}).get("status") == "do_not_score":
            raise SystemExit(f"refusing burned horse {hid}")
    for row in queue.get("next") or []:
        if (row or {}).get("id") in HORSES:
            raise SystemExit("queued next class collided with active pulse ids")


def update_queue_after_discovery(queue: dict, boards: dict) -> dict:
    burned = list(queue.get("burned") or [])
    existing = {(b.get("horse"), b.get("scoreboard")) for b in burned}
    for board, payload in boards.items():
        if payload.get("vehicle_fail"):
            continue
        surv = payload["discovery"]["survivor"]["id"]
        for hid in HORSES:
            if surv == hid:
                continue
            key = (hid, board)
            if key in existing:
                continue
            if not payload["discovery"]["horses"][hid]["beats_continuation"]:
                burned.append(
                    {
                        "horse": hid,
                        "scoreboard": board,
                        "status": "burned_discovery_loss",
                        "note": "Failed to strictly beat continuation on discovery. Do not retune.",
                    }
                )
                existing.add(key)
        if surv is None:
            # both already appended as losses
            pass
    out = dict(queue)
    out["burned"] = burned
    out["last_discovery"] = {
        board: payload["discovery"]["survivor"] for board, payload in boards.items()
    }
    return out


def latest_dashboard(rows: list[dict]) -> dict | None:
    for rec in reversed(rows):
        if rec["sign"] in {"Up", "Down"} and rec["sign_lag"] in {"Up", "Down"}:
            return {
                "as_of": rec["date"],
                "sign": rec["sign"],
                "flip": rec["flip"],
                "continuation_call": rec["sign"],
                "H-SPOT-FLIP-HOLD": rec["sign_lag"],
                "H-SPOT-REV": opposite(rec["sign"]),
                "next_21_realized": rec["truth"],
            }
    return None


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(here / "data"))
    ap.add_argument("--stage", choices=("discovery", "confirm", "all"), default="all")
    ap.add_argument("--queue", default=str(here / "data" / "spot_trend_queue.json"))
    args = ap.parse_args()
    data = Path(args.data_dir)
    queue_path = Path(args.queue)
    queue = json.loads(queue_path.read_text()) if queue_path.exists() else {
        "pulse": ACTIVE_PULSE,
        "active_horses": HORSES,
        "burned": [],
        "next": [],
    }
    refuse_queued(queue)

    paths = {
        "WTI": data / "eia_spot_wti.csv",
        "Brent": data / "eia_spot_brent.csv",
    }
    boards = {}
    vehicle_fail = False
    for name, path in paths.items():
        if not path.exists():
            raise SystemExit(f"missing {path}; run fetch_eia_spot.py first")
        rows = annotate(load_spot(path))
        scored = score_board(rows, [500, 250, 750] if args.stage in {"confirm", "all"} else [])
        if args.stage == "discovery":
            scored["confirm"] = None
            scored["confirm_deferred"] = True
        boards[name] = scored
        if scored["vehicle_fail"]:
            vehicle_fail = True
        boards[name]["dashboard"] = latest_dashboard(rows)

    if args.stage in {"discovery", "all"} and not vehicle_fail:
        queue = update_queue_after_discovery(queue, boards)

    any_survivor = any(
        (boards[b]["discovery"]["survivor"]["id"] is not None) for b in BOARDS
    )
    if args.stage == "discovery" or (args.stage == "all" and not any_survivor):
        for b in BOARDS:
            boards[b]["confirm"] = None

    out = {
        "lock": ACTIVE_PULSE,
        "stage": args.stage,
        "discovery_cutoff": DISCOVERY_CUTOFF,
        "horizon_price_steps": HORIZON,
        "train_arm": "N/A for these two rule horses (no fitted coefficients)",
        "select_arm": "discovery last 500 of prefix <= 2023-08-21",
        "confirm_arm": "last 500/250/750; never train; skipped if no survivor",
        "vehicle_fail": vehicle_fail,
        "boards": boards,
        "queue_refused_this_pulse": [row.get("id") for row in (queue.get("next") or [])],
    }
    (data / "spot_trend_hunt_scores.json").write_text(json.dumps(out, indent=2) + "\n")
    queue_path.write_text(json.dumps(queue, indent=2) + "\n")

    summary = {
        "vehicle_fail": vehicle_fail,
        "stage": args.stage,
        "boards": {
            b: {
                "n_eligible": boards[b]["n_eligible"],
                "discovery_n": boards[b]["discovery"]["n_scoreboard"],
                "continuation": boards[b]["discovery"]["continuation"]["hit_rate"],
                "horses": {
                    hid: boards[b]["discovery"]["horses"][hid]["hit_rate"] for hid in HORSES
                },
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
