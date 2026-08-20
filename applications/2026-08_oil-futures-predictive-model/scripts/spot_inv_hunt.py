#!/usr/bin/env python3
"""Named finite discovery/confirm EIA inventory-surprise overlay (Track B queue).

Protocol frozen in Lock_Hunt_Spot_Inv.md *before* last-500 confirm scores.

Two horses: H-SPOT-INV-CONT (draw surprise → Up) and H-SPOT-INV-FADE (opposite).
Baseline continuation is not a horse. Pick one per scoreboard only if it
strictly beats continuation on discovery.

Does not unburn H-SPOT-FLIP-HOLD / H-SPOT-REV. Does not change 21.
Does not download. Not a trade. Not Bloomberg consensus surprise.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
from pathlib import Path

DISCOVERY_CUTOFF = "2023-08-21"
HORIZON = 21
MIN_DISCOVERY_ELIGIBLE = 250
MIN_INV_REPORTS = 30
HORSES = ["H-SPOT-INV-CONT", "H-SPOT-INV-FADE"]
BURNED = {"H-SPOT-FLIP-HOLD", "H-SPOT-REV"}
ACTIVE_PULSE = "L-HUNT-SPOT-INV"
BOARDS = ("WTI", "Brent")
LOOKBACK_WOW = 4


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


def annotate_spot(rows: list[dict]) -> list[dict]:
    n = len(rows)
    out = []
    for i, rec in enumerate(rows):
        item = {
            "i": i,
            "date": rec["date"],
            "price": rec["price"],
            "sign": None,
            "sign_lag": None,
            "truth": None,
            "surprise": 0.0,
            "inv_release": None,
        }
        if i >= HORIZON and rec["price"] > 0 and rows[i - HORIZON]["price"] > 0:
            item["sign"] = sign_of(math.log(rec["price"] / rows[i - HORIZON]["price"]))
        if i - 1 >= HORIZON and rows[i - 1]["price"] > 0 and rows[i - 1 - HORIZON]["price"] > 0:
            item["sign_lag"] = sign_of(
                math.log(rows[i - 1]["price"] / rows[i - 1 - HORIZON]["price"])
            )
        if i + HORIZON < n and rec["price"] > 0 and rows[i + HORIZON]["price"] > 0:
            item["truth"] = sign_of(math.log(rows[i + HORIZON]["price"] / rec["price"]))
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
    ]


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
            rec["wow"] = None
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
    return rows


def attach_inventory(spots: list[dict], inv: list[dict]) -> dict:
    releases = [r["release_date"] for r in inv]
    j = -1
    n = len(inv)
    n_nonzero = 0
    for rec in spots:
        cutoff = (dt.date.fromisoformat(rec["date"]) - dt.timedelta(days=1)).isoformat()
        while j + 1 < n and releases[j + 1] <= cutoff:
            j += 1
        if j < 0:
            rec["surprise"] = 0.0
            rec["inv_release"] = None
        else:
            rec["surprise"] = float(inv[j]["surprise"])
            rec["inv_release"] = inv[j]["release_date"]
            if rec["surprise"] != 0.0:
                n_nonzero += 1
    span_first = spots[0]["date"] if spots else ""
    span_last = spots[-1]["date"] if spots else ""
    n_in_span = sum(1 for r in inv if span_first <= r["release_date"] <= span_last) if spots else 0
    disc_end = DISCOVERY_CUTOFF
    n_in_disc = sum(1 for r in inv if span_first <= r["release_date"] <= disc_end) if spots else 0
    return {
        "n_reports": len(inv),
        "n_reports_in_session_span": n_in_span,
        "n_reports_release_le_discovery_cutoff": n_in_disc,
        "n_sessions_with_nonzero_surprise": n_nonzero,
        "first_week": inv[0]["week_ending"] if inv else None,
        "last_week": inv[-1]["week_ending"] if inv else None,
        "lookback_wow": LOOKBACK_WOW,
    }


def call_for(horse: str, rec: dict) -> str:
    s = rec["surprise"]
    if horse == "continuation":
        return rec["sign"]
    if horse == "H-SPOT-INV-CONT":
        if s < 0:
            return "Up"
        if s > 0:
            return "Down"
        return rec["sign"]
    if horse == "H-SPOT-INV-FADE":
        if s < 0:
            return "Down"
        if s > 0:
            return "Up"
        return rec["sign"]
    raise KeyError(horse)


def hit_rate(rows: list[dict], horse: str) -> dict:
    if not rows:
        return {"n": 0, "hits": 0, "hit_rate": None, "first": None, "last": None}
    hits = sum(1 for rec in rows if call_for(horse, rec) == rec["truth"])
    n = len(rows)
    return {
        "n": n,
        "hits": hits,
        "hit_rate": hits / n,
        "first": rows[0]["date"],
        "last": rows[-1]["date"],
    }


def last_n(rows: list[dict], n: int) -> list[dict]:
    return rows[-n:] if n > 0 and len(rows) >= n else list(rows)


def prefix_cutoff(rows: list[dict], cutoff: str) -> list[dict]:
    return [r for r in rows if r["date"] <= cutoff]


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
    return {"id": best, "reason": "strictly beat continuation; ties keep H-SPOT-INV-CONT"}


def score_board(rows: list[dict], holdouts: list[int], inv_meta: dict) -> dict:
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
        "vehicle_fail": len(disc_pool) < MIN_DISCOVERY_ELIGIBLE
        or inv_meta.get("n_reports_release_le_discovery_cutoff", 0) < MIN_INV_REPORTS,
        "span_first": rows[0]["date"] if rows else None,
        "span_last": rows[-1]["date"] if rows else None,
        "inventory": inv_meta,
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
    }


def refuse_queue(queue: dict) -> None:
    for row in queue.get("burned") or []:
        hid = (row or {}).get("horse")
        if hid in HORSES:
            raise SystemExit(f"refusing burned active horse {hid}")
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
        if row.get("id") == "C-SPOT-INV":
            continue
        nxt.append(row)
    out = dict(queue)
    out["pulse"] = ACTIVE_PULSE
    out["lock"] = "Lock_Hunt_Spot_Inv.md"
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

    inv_path = data / "eia_weekly_crude_exspr.csv"
    if not inv_path.exists():
        raise SystemExit(f"missing {inv_path}; run fetch_eia_inventory.py first")
    inv = load_inventory(inv_path)

    holdouts = [500, 250, 750] if args.stage in {"confirm", "all"} else []
    boards = {}
    vehicle_fail = False
    for name, fname in (("WTI", "eia_spot_wti.csv"), ("Brent", "eia_spot_brent.csv")):
        path = data / fname
        if not path.exists():
            raise SystemExit(f"missing {path}; run fetch_eia_spot.py first")
        spots = annotate_spot(load_spot(path))
        inv_meta = attach_inventory(spots, inv)
        scored = score_board(spots, holdouts, inv_meta)
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
        "surprise": "wow minus mean of prior 4 wow; not Bloomberg consensus",
        "clock": "latest WPSR with release_date <= t-1; carry forward",
        "train_arm": "N/A for these two rule horses",
        "select_arm": "discovery last 500 of prefix <= 2023-08-21",
        "confirm_arm": "last 500/250/750; never train; skipped if no survivor",
        "refused_burned": sorted(BURNED),
        "vehicle_fail": vehicle_fail,
        "boards": boards,
        "queue_still_queued": [row.get("id") for row in (queue.get("next") or [])],
    }
    (data / "spot_inv_hunt_scores.json").write_text(json.dumps(out, indent=2) + "\n")
    queue_path.write_text(json.dumps(queue, indent=2) + "\n")
    summary = {
        "vehicle_fail": vehicle_fail,
        "stage": args.stage,
        "boards": {
            b: {
                "n_eligible": boards[b]["n_eligible"],
                "discovery_n": boards[b]["discovery"]["n_scoreboard"],
                "inv_reports_le_cutoff": boards[b]["inventory"]["n_reports_release_le_discovery_cutoff"],
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
