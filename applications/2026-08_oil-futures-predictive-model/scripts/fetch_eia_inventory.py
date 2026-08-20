#!/usr/bin/env python3
"""Fetch EIA weekly US crude stocks excluding SPR (WCESTUS1).

Stand-in inventory tape for L-STANDIN-EIA-INV. Does not score trend skill.
Naive surprise is computed in the hunt script, not here.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (compatible; gated-formalization-standin/1.0)"}
FRED_ID = "WCESTUS1"
EIA_ID = "PET.WCESTUS1.W"
FRED_CSV = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={FRED_ID}"
EIA_LEAF = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCESTUS1&f=W"


def fetch_bytes(url: str, timeout: int = 120) -> tuple[bytes | None, dict]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return body, {
                "url": url,
                "ok": True,
                "http_status": r.status,
                "n_bytes": len(body),
                "content_type": r.headers.get("Content-Type"),
            }
    except urllib.error.HTTPError as e:
        return None, {"url": url, "ok": False, "http_status": e.code, "error": str(e)}
    except Exception as e:
        return None, {"url": url, "ok": False, "http_status": None, "error": str(e)}


def parse_date(raw: str) -> str | None:
    s = (raw or "").strip().strip('"')
    if not s or s.upper() in {"DATE", "PERIOD", "NA", "N/A", "."}:
        return None
    for fmt, n in (("%Y-%m-%d", 10), ("%Y-%m-%d", 10), ("%m/%d/%Y", 10)):
        try:
            return dt.datetime.strptime(s[:n], fmt).date().isoformat()
        except ValueError:
            continue
    return None


def parse_level(raw: str) -> float | None:
    s = (raw or "").strip().strip('"').replace(",", "")
    if not s or s in {".", "NA", "N/A", ""}:
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    if v <= 0:
        return None
    return v


def parse_fred_csv(text: str) -> list[dict]:
    rows = []
    reader = csv.reader(io.StringIO(text.lstrip("\ufeff")))
    header = True
    for parts in reader:
        if not parts or len(parts) < 2:
            continue
        if header:
            header = False
            continue
        d = parse_date(parts[0])
        v = parse_level(parts[1])
        if d and v is not None:
            rows.append({"week_ending": d, "stocks": v})
    rows.sort(key=lambda r: r["week_ending"])
    return rows


def eia_release_date(week_ending: str) -> str:
    """Wednesday after the Friday week-ending (typical WPSR)."""
    d = dt.date.fromisoformat(week_ending)
    # Move back to Friday if the file uses Saturday/Sunday.
    while d.weekday() > 4:  # Sat=5 Sun=6
        d -= dt.timedelta(days=1)
    if d.weekday() != 4:
        # Not Friday: next Friday, then +5 — or if already Mon-Thu, previous Friday.
        d = d - dt.timedelta(days=(d.weekday() - 4) % 7)
    return (d + dt.timedelta(days=5)).isoformat()


def attach_release(rows: list[dict]) -> list[dict]:
    out = []
    for rec in rows:
        item = dict(rec)
        item["release_date"] = eia_release_date(rec["week_ending"])
        out.append(item)
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["week_ending", "release_date", "stocks"])
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(here / "data"))
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    trail = []
    rows: list[dict] = []
    vehicle = None
    # EIA leaf is usually HTML; try then FRED.
    body, meta = fetch_bytes(EIA_LEAF)
    trail.append(meta)
    if body:
        text = body.decode("utf-8", "replace")
        if "DATE" in text[:80].upper() and "," in text.split("\n", 1)[0]:
            rows = parse_fred_csv(text)
            if len(rows) >= 30:
                vehicle = "eia_leaf_csv"
    if len(rows) < 30:
        body, meta = fetch_bytes(FRED_CSV)
        trail.append(meta)
        if body:
            rows = parse_fred_csv(body.decode("utf-8", "replace"))
            if len(rows) >= 30:
                vehicle = "fred_eia_reprint"
    rows = attach_release(rows)
    ok = len(rows) >= 30
    csv_path = out_dir / "eia_weekly_crude_exspr.csv"
    if rows:
        write_csv(csv_path, rows)
    report = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lock": "L-STANDIN-EIA-INV",
        "eia_id": EIA_ID,
        "fred_id": FRED_ID,
        "eia_key_present": bool(os.environ.get("EIA_API_KEY") or os.environ.get("EIA_KEY")),
        "vehicle": vehicle,
        "n": len(rows),
        "first_week": rows[0]["week_ending"] if rows else None,
        "last_week": rows[-1]["week_ending"] if rows else None,
        "first_release": rows[0]["release_date"] if rows else None,
        "last_release": rows[-1]["release_date"] if rows else None,
        "vehicle_fail": not ok,
        "attempts": trail,
        "csv": csv_path.name if rows else None,
        "note": "Naive surprise is hunt-side (WoW minus prior-4-week mean WoW). Not Bloomberg consensus.",
    }
    (out_dir / "eia_inv_fetch.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"ok": ok, "n": len(rows), "vehicle": vehicle,
                      "first": report["first_week"], "last": report["last_week"]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
