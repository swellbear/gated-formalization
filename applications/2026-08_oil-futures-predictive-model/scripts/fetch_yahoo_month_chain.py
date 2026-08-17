#!/usr/bin/env python3
"""Fetch currently listed Yahoo NYMEX CL month contracts and stack a frontness panel.

Stand-in only. Expired Yahoo months typically 404, so historical CL1–CL18
generics usually cannot be built. This script records that fact.

Does not treat Yahoo as CME official. Does not apply CME roll rule R1.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

MONTHS = list("FGHJKMNQUVXZ")
MONTH_NUM = {c: i + 1 for i, c in enumerate(MONTHS)}
UA = {"User-Agent": "Mozilla/5.0 (compatible; gated-formalization-standin/1.0)"}


def chart_url(symbol: str, period1: int, period2: int) -> str:
    return (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{symbol}?interval=1d&period1={period1}&period2={period2}"
    )


def fetch_symbol(symbol: str, period1: int, period2: int) -> dict:
    req = urllib.request.Request(chart_url(symbol, period1, period2), headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = json.loads(r.read().decode())
            status = r.status
    except urllib.error.HTTPError as e:
        return {"symbol": symbol, "http_status": e.code, "ok": False, "error": str(e), "bars": []}
    except Exception as e:
        return {"symbol": symbol, "http_status": None, "ok": False, "error": str(e), "bars": []}

    result = (raw.get("chart") or {}).get("result")
    if not result:
        return {"symbol": symbol, "http_status": status, "ok": False, "error": "empty result", "bars": []}
    res = result[0]
    ts = res.get("timestamp") or []
    quote = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    opens = quote.get("open") or []
    closes = quote.get("close") or []
    bars = []
    for i, t in enumerate(ts):
        o = opens[i] if i < len(opens) else None
        c = closes[i] if i < len(closes) else None
        if o is None or c is None:
            continue
        if o <= 0 or c <= 0:
            continue
        day = dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
        bars.append({"date": day, "open": float(o), "settle": float(c)})
    meta = res.get("meta") or {}
    return {
        "symbol": symbol,
        "http_status": status,
        "ok": True,
        "shortName": meta.get("shortName"),
        "n_bars": len(bars),
        "first": bars[0]["date"] if bars else None,
        "last": bars[-1]["date"] if bars else None,
        "bars": bars,
    }


def delivery_of(symbol: str) -> tuple[int, int]:
    # CLU26.NYM -> (2026, 9)
    code = symbol.split(".")[0]  # CLU26
    letter = code[2]
    yy = int(code[3:])
    year = 2000 + yy if yy < 80 else 1900 + yy
    return year, MONTH_NUM[letter]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="data")
    p.add_argument("--start-year", type=int, default=25)
    p.add_argument("--end-year", type=int, default=29)
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    period1 = int(dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    period2 = int(dt.datetime.now(dt.timezone.utc).timestamp()) + 86400

    symbols = [f"CL{m}{yy:02d}.NYM" for yy in range(args.start_year, args.end_year + 1) for m in MONTHS]
    fetched = []
    for i, s in enumerate(symbols):
        fetched.append(fetch_symbol(s, period1, period2))
        if (i + 1) % 10 == 0:
            time.sleep(0.2)

    ok = [x for x in fetched if x["ok"] and x["bars"]]
    fail = [x for x in fetched if not x["ok"] or not x["bars"]]

    # Panel: on each date, rank live contracts by delivery.
    by_date: dict[str, list[tuple[tuple[int, int], str, dict]]] = defaultdict(list)
    for rec in ok:
        dly = delivery_of(rec["symbol"])
        for bar in rec["bars"]:
            by_date[bar["date"]].append((dly, rec["symbol"], bar))

    panel_rows = []
    tenors_needed = list(range(1, 19))
    dates_with_cl1_18 = 0
    for day in sorted(by_date):
        items = sorted(by_date[day], key=lambda x: x[0])
        for i, (dly, sym, bar) in enumerate(items, start=1):
            if i > 18:
                break
            panel_rows.append(
                {
                    "date": day,
                    "tenor": i,
                    "open": f"{bar['open']:.6f}",
                    "settle": f"{bar['settle']:.6f}",
                    "contract_id": sym,
                    "delivery": f"{dly[0]:04d}-{dly[1]:02d}",
                }
            )
        if len(items) >= 18:
            dates_with_cl1_18 += 1

    panel_path = out_dir / "clf_yahoo_month_chain.csv"
    with panel_path.open("w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["date", "tenor", "open", "settle", "contract_id", "delivery"]
        )
        w.writeheader()
        w.writerows(panel_rows)

    # How many dates have a tenor-1 row whose contract is actually the calendar front
    # vs merely the nearest *still-listed* Yahoo month (expired fronts missing).
    n_tenor = defaultdict(int)
    for row in panel_rows:
        n_tenor[int(row["tenor"])] += 1

    first_last = {}
    if panel_rows:
        first_last = {"first_date": panel_rows[0]["date"], "last_date": panel_rows[-1]["date"]}

    meta = {
        "badge": "stand-in",
        "source": "Yahoo v8 chart NYMEX CL month contracts",
        "fetched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "period1": period1,
        "period2": period2,
        "n_symbols_tried": len(symbols),
        "n_ok": len(ok),
        "n_fail": len(fail),
        "ok_symbols": [
            {"symbol": x["symbol"], "shortName": x.get("shortName"), "n_bars": x["n_bars"], "first": x["first"], "last": x["last"]}
            for x in ok
        ],
        "fail_symbols": [{"symbol": x["symbol"], "http_status": x.get("http_status"), "error": x.get("error")} for x in fail],
        "panel_rows": len(panel_rows),
        "n_dates": len(by_date),
        "dates_with_tenors_1_to_18": dates_with_cl1_18,
        "tenor_row_counts": {str(k): n_tenor[k] for k in range(1, 19)},
        **first_last,
        "historical_cl1_18_note": (
            "Yahoo 404s expired month contracts. Nearest still-listed month is not "
            "historical CL1 on dates before that contract was front. Kearney-Shang "
            "walk-forward on CL1-CL18 therefore cannot run on this panel as a freeze match."
        ),
    }
    meta_path = out_dir / "clf_yahoo_month_chain_fetch.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({k: meta[k] for k in meta if k not in {"ok_symbols", "fail_symbols"}}, indent=2))
    print(f"wrote {panel_path} rows={len(panel_rows)}")
    print(f"wrote {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
