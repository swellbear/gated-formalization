#!/usr/bin/env python3
"""Fetch Yahoo daily closes for the locked L-STANDIN-Y-TELLS drawer.

Stand-in only. Does not treat Yahoo as CME official. Does not score horses.
Symbols and roles are frozen in Lock_Hunt_Pretell.md — do not add tickers here
after seeing hunt scores.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (compatible; gated-formalization-standin/1.0)"}

# Locked drawer (L-STANDIN-Y-TELLS). Do not expand after scores.
TELLS = [
    {"id": "DXY", "symbol": "DX-Y.NYB", "file": "tell_dxy.csv", "role": "dollar"},
    {"id": "RBOB", "symbol": "RB=F", "file": "tell_rbob.csv", "role": "gasoline"},
    {"id": "HO", "symbol": "HO=F", "file": "tell_ho.csv", "role": "heating oil"},
    {"id": "SPX", "symbol": "^GSPC", "file": "tell_spx.csv", "role": "equities"},
    {"id": "HG", "symbol": "HG=F", "file": "tell_hg.csv", "role": "copper"},
    {"id": "TNX", "symbol": "^TNX", "file": "tell_tnx.csv", "role": "10Y yield"},
]


def chart_url(symbol: str, period1: int, period2: int) -> str:
    enc = urllib.parse.quote(symbol, safe="")
    return (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{enc}?interval=1d&period1={period1}&period2={period2}"
    )


def fetch_symbol(symbol: str, period1: int, period2: int, require_positive: bool) -> dict:
    url = chart_url(symbol, period1, period2)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = json.loads(r.read().decode())
            status = r.status
    except urllib.error.HTTPError as e:
        return {
            "symbol": symbol,
            "source_url": url,
            "http_status": e.code,
            "ok": False,
            "error": str(e),
            "bars": [],
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "source_url": url,
            "http_status": None,
            "ok": False,
            "error": str(e),
            "bars": [],
        }

    result = (raw.get("chart") or {}).get("result")
    if not result:
        return {
            "symbol": symbol,
            "source_url": url,
            "http_status": status,
            "ok": False,
            "error": "empty result",
            "bars": [],
        }
    res = result[0]
    ts = res.get("timestamp") or []
    quote = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    closes = quote.get("close") or []
    bars = []
    dropped_null = 0
    dropped_nonpos = 0
    for i, t in enumerate(ts):
        c = closes[i] if i < len(closes) else None
        if c is None:
            dropped_null += 1
            continue
        c = float(c)
        if require_positive and c <= 0:
            dropped_nonpos += 1
            continue
        day = dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()
        bars.append({"date": day, "close": c})
    meta = res.get("meta") or {}
    return {
        "symbol": symbol,
        "source_url": url,
        "http_status": status,
        "ok": True,
        "shortName": meta.get("shortName"),
        "n_bars": len(bars),
        "dropped_null": dropped_null,
        "dropped_nonpos": dropped_nonpos,
        "first": bars[0]["date"] if bars else None,
        "last": bars[-1]["date"] if bars else None,
        "bars": bars,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="data")
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    period1 = int(dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    period2 = int(dt.datetime.now(dt.timezone.utc).timestamp()) + 86400

    fetched = []
    for i, spec in enumerate(TELLS):
        rec = fetch_symbol(spec["symbol"], period1, period2, require_positive=True)
        rec["id"] = spec["id"]
        rec["role"] = spec["role"]
        rec["file"] = spec["file"]
        fetched.append(rec)
        csv_path = out_dir / spec["file"]
        if rec["ok"] and rec["bars"]:
            with csv_path.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["date", "close"])
                w.writeheader()
                for bar in rec["bars"]:
                    w.writerow({"date": bar["date"], "close": f"{bar['close']:.8f}"})
        if i + 1 < len(TELLS):
            time.sleep(0.25)

    meta = {
        "badge": "stand-in",
        "lock": "L-STANDIN-Y-TELLS",
        "source": "Yahoo v8 chart daily Close",
        "fetched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "period1": period1,
        "period2": period2,
        "n_symbols": len(TELLS),
        "series": [
            {k: x[k] for k in x if k != "bars"}
            for x in fetched
        ],
        "note": (
            "Vendor generics / cash indexes. Not CME official. Not a skill pass. "
            "Drawer frozen in Lock_Hunt_Pretell.md."
        ),
    }
    meta_path = out_dir / "tell_yahoo_fetch.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    n_ok = sum(1 for x in fetched if x.get("ok") and x.get("n_bars"))
    print(f"wrote {meta_path}; ok={n_ok}/{len(TELLS)}")
    return 0 if n_ok == len(TELLS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
