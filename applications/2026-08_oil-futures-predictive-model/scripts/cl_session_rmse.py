#!/usr/bin/env python3
"""RMSE of a no-change (0) forecast on F-ON / F-DAY / F-CC.

Expect a CSV with columns: date, open, settle, front_id
  date      ISO YYYY-MM-DD
  open      official printed daily open
  settle    official daily settlement
  front_id  contract code for that session's front (e.g. CLZ2026)

Roll rule R1: when front_id changes vs the previous row, drop F-ON and F-CC
for that row (roll jump). F-DAY is kept if open and settle are on the new front.

Does not download prices. Does not treat Yahoo as CME official.
"""
from __future__ import annotations

import argparse
import csv
import math


def rmse(xs: list[float]) -> float | None:
    if not xs:
        return None
    return math.sqrt(sum(x * x for x in xs) / len(xs))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("csv_path")
    p.add_argument("--holdout", type=int, default=500, help="use last N rows after filters as OOS")
    args = p.parse_args()

    rows = []
    with open(args.csv_path, newline="") as f:
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

    r_on: list[float] = []
    r_day: list[float] = []
    r_cc: list[float] = []
    for i in range(1, len(rows)):
        prev, cur = rows[i - 1], rows[i]
        rolled = cur["front_id"] != prev["front_id"]
        if cur["open"] > 0 and cur["settle"] > 0:
            r_day.append(math.log(cur["settle"] / cur["open"]))
        if not rolled and prev["settle"] > 0 and cur["open"] > 0:
            r_on.append(math.log(cur["open"] / prev["settle"]))
        if not rolled and prev["settle"] > 0 and cur["settle"] > 0:
            r_cc.append(math.log(cur["settle"] / prev["settle"]))

    def tail(xs: list[float]) -> list[float]:
        if args.holdout and len(xs) > args.holdout:
            return xs[-args.holdout :]
        return xs

    out = {
        "F-ON": (rmse(tail(r_on)), len(tail(r_on))),
        "F-DAY": (rmse(tail(r_day)), len(tail(r_day))),
        "F-CC": (rmse(tail(r_cc)), len(tail(r_cc))),
    }
    for k, (val, n) in out.items():
        print(f"{k}\tRMSE={val}\tn={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
