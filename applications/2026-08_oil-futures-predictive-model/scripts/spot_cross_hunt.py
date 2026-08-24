#!/usr/bin/env python3
"""Named finite discovery/confirm EIA spot WTI↔Brent cross-bench overlay.

Protocol frozen in Lock_Hunt_Spot_Cross.md *before* last-500 confirm scores.

Two board-specific horses:
  H-SPOT-CROSS-B2W — Brent 21-day sign as the call on the WTI board
  H-SPOT-CROSS-W2B — WTI 21-day sign as the call on the Brent board

Scoring a board's own sign as its call is continuation (OUT as a horse).
Baseline continuation is not a horse. Pick the board's horse only if it
strictly beats continuation on discovery.

Does not unburn FLIP-HOLD / REV / INV. Does not change 21.
Does not download. Not a trade. Not a dollar-spread horse.
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
MIN_PEER_ON_DISCOVERY_500 = 250
HORSES_BY_BOARD = {
    "WTI": ["H-SPOT-CROSS-B2W"],
    "Brent": ["H-SPOT-CROSS-W2B"],
}
ALL_HORSES = ["H-SPOT-CROSS-B2W", "H-SPOT-CROSS-W2B"]
BURNED = {
    "H-SPOT-FLIP-HOLD",
    "H-SPOT-REV",
    "H-SPOT-INV-CONT",
    "H-SPOT-INV-FADE",
}
ACTIVE_PULSE = "L-HUNT-SPOT-CROSS"
BOARDS = ("WTI", "Brent")


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
            "peer_sign": None,
            "peer_date": None,
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


def attach_peer(home: list[dict], peer: list[dict]) -> dict:
    """Carry the latest peer print with date <= home date (same-day allowed)."""
    j = -1
    n = len(peer)
    n_updown = 0
    for rec in home:
        while j + 1 < n and peer[j + 1]["date"] <= rec["date"]:
            j += 1
        if j < 0:
            rec["peer_sign"] = None
            rec["peer_date"] = None
        else:
            rec["peer_sign"] = peer[j]["sign"]
            rec["peer_date"] = peer[j]["date"]
            if rec["peer_sign"] in {"Up", "Down"}:
                n_updown += 1
    return {
        "n_peer_prints": len(peer),
        "n_home_with_peer_updown": n_updown,
        "peer_first": peer[0]["date"] if peer else None,
        "peer_last": peer[-1]["date"] if peer else None,
        "clock": "latest peer print with date <= t; carry forward; Flat/missing → continuation",
    }


def call_for(horse: str, rec: dict) -> str:
    if horse == "continuation":
        return rec["sign"]
    if horse in ALL_HORSES:
        peer = rec.get("peer_sign")
        if peer in {"Up", "Down"}:
            return peer
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


def pick_survivor(horses: dict, horse_ids: list[str]) -> dict:
    beat = [hid for hid in horse_ids if horses[hid].get("beats_continuation")]
    if not beat:
        return {"id": None, "reason": "no horse strictly beat continuation on discovery"}
    best = beat[0]
    best_hr = horses[best]["hit_rate"]
    for hid in beat[1:]:
        hr = horses[hid]["hit_rate"]
        if hr > best_hr:
            best, best_hr = hid, hr
    return {"id": best, "reason": "strictly beat continuation; one horse per board so ties N/A"}


def score_board(rows: list[dict], board: str, holdouts: list[int], peer_meta: dict) -> dict:
    horse_ids = HORSES_BY_BOARD[board]
    elig = eligible(rows)
    disc_pool = prefix_cutoff(elig, DISCOVERY_CUTOFF)
    disc_board = last_n(disc_pool, 500)
    n_peer_on_disc = sum(1 for r in disc_board if r.get("peer_sign") in {"Up", "Down"})
    continuation = hit_rate(disc_board, "continuation")
    horses = {}
    for hid in horse_ids:
        h = hit_rate(disc_board, hid)
        h["beats_continuation"] = (
            h["hit_rate"] is not None
            and continuation["hit_rate"] is not None
            and h["hit_rate"] > continuation["hit_rate"]
        )
        horses[hid] = h
    survivor = pick_survivor(horses, horse_ids)
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
    peer_meta = dict(peer_meta)
    peer_meta["n_discovery_500_with_peer_updown"] = n_peer_on_disc
    return {
        "n_prints": len(rows),
        "n_eligible": len(elig),
        "n_discovery_pool": len(disc_pool),
        "vehicle_fail": len(disc_pool) < MIN_DISCOVERY_ELIGIBLE
        or n_peer_on_disc < MIN_PEER_ON_DISCOVERY_500,
        "span_first": rows[0]["date"] if rows else None,
        "span_last": rows[-1]["date"] if rows else None,
        "peer": peer_meta,
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


def refuse_queue(_queue: dict) -> None:
    """Refuse unburning prior-pulse horses as this pulse's active set.

    A discovery loss on one CROSS board must not block confirm of the
    other board's survivor in this same pulse.
    """
    for hid in ALL_HORSES:
        if hid in BURNED:
            raise SystemExit(f"active horse {hid} is on the burned list")


def update_queue_after_discovery(queue: dict, boards: dict) -> dict:
    burned = list(queue.get("burned") or [])
    existing = {(b.get("horse"), b.get("scoreboard")) for b in burned}
    for board, payload in boards.items():
        if payload.get("vehicle_fail"):
            continue
        for hid in HORSES_BY_BOARD[board]:
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
        if row.get("id") == "C-SPOT-CROSS":
            continue
        nxt.append(row)
    out = dict(queue)
    out["pulse"] = ACTIVE_PULSE
    out["lock"] = "Lock_Hunt_Spot_Cross.md"
    out["active_horses"] = ALL_HORSES
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

    paths = {
        "WTI": data / "eia_spot_wti.csv",
        "Brent": data / "eia_spot_brent.csv",
    }
    annotated = {}
    for name, path in paths.items():
        if not path.exists():
            raise SystemExit(f"missing {path}; run fetch_eia_spot.py first")
        annotated[name] = annotate_spot(load_spot(path))

    holdouts = [500, 250, 750] if args.stage in {"confirm", "all"} else []
    boards = {}
    vehicle_fail = False
    peer_of = {"WTI": "Brent", "Brent": "WTI"}
    for name in BOARDS:
        peer_name = peer_of[name]
        peer_meta = attach_peer(annotated[name], annotated[peer_name])
        peer_meta["peer_board"] = peer_name
        scored = score_board(annotated[name], name, holdouts, peer_meta)
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
        "overlay": "peer 21-day sign as of latest peer print date <= t; Flat/missing → continuation",
        "train_arm": "N/A for these two rule horses",
        "select_arm": "discovery last 500 of prefix <= 2023-08-21",
        "confirm_arm": "last 500/250/750; never train; skipped if no survivor",
        "refused_burned": sorted(BURNED),
        "horses_by_board": HORSES_BY_BOARD,
        "vehicle_fail": vehicle_fail,
        "boards": boards,
        "queue_still_queued": [row.get("id") for row in (queue.get("next") or [])],
    }
    (data / "spot_cross_hunt_scores.json").write_text(json.dumps(out, indent=2) + "\n")
    queue_path.write_text(json.dumps(queue, indent=2) + "\n")
    summary = {
        "vehicle_fail": vehicle_fail,
        "stage": args.stage,
        "boards": {
            b: {
                "n_eligible": boards[b]["n_eligible"],
                "discovery_n": boards[b]["discovery"]["n_scoreboard"],
                "peer_updown_on_discovery_500": boards[b]["peer"]["n_discovery_500_with_peer_updown"],
                "continuation": boards[b]["discovery"]["continuation"]["hit_rate"],
                "horses": {
                    hid: boards[b]["discovery"]["horses"][hid]["hit_rate"]
                    for hid in HORSES_BY_BOARD[b]
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
