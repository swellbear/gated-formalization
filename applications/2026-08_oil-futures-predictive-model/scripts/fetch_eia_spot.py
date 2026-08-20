#!/usr/bin/env python3
"""Fetch daily EIA Cushing WTI and Europe Brent spot prints.

Stand-in cash tape for L-STANDIN-EIA-SPOT. Does not score trend skill.
Does not treat this as NYMEX CL or ICE Brent futures.

Primary: EIA Open Data v2 if EIA_API_KEY is set, else EIA hist_xls URLs
decoded as CSV/HTML when possible.
Named fallback: FRED DCOILWTICO / DCOILBRENTEU (EIA-sourced reprints).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (compatible; gated-formalization-standin/1.0)"}

SERIES = {
    "WTI": {
        "eia_id": "PET.RWTC.D",
        "eia_facet": "RWTC",
        "fred_id": "DCOILWTICO",
        "eia_xls": "https://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls",
        "eia_leaf": "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RWTC&f=D",
    },
    "Brent": {
        "eia_id": "PET.RBRTE.D",
        "eia_facet": "RBRTE",
        "fred_id": "DCOILBRENTEU",
        "eia_xls": "https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls",
        "eia_leaf": "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D",
    },
}

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
EIA_V2 = (
    "https://api.eia.gov/v2/petroleum/pri/spt/data/"
    "?frequency=daily&data[0]=value&facets[duoarea][]={area}"
    "&facets[product][]=EPC0"
    "&sort[0][column]=period&sort[0][direction]=asc&offset={offset}&length=5000"
    "&api_key={key}"
)
# duoarea: RCLC1 = Cushing OK; RBRTE = Europe Brent in pri/spt
EIA_V2_AREA = {"WTI": "RCLC1", "Brent": "RBRTE"}


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


def _parse_date(raw: str) -> str | None:
    s = (raw or "").strip().strip('"')
    if not s or s.upper() in {"DATE", "PERIOD", "NA", "N/A", "."}:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m", "%m/%d/%Y", "%Y%m%d"):
        try:
            return dt.datetime.strptime(s[:10] if fmt != "%Y%m%d" else s[:8], fmt).date().isoformat()
        except ValueError:
            continue
    m = re.match(r"(\d{4})[./-](\d{1,2})[./-](\d{1,2})", s)
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except ValueError:
            return None
    return None


def _parse_price(raw: str) -> float | None:
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
        if not parts:
            continue
        if header:
            header = False
            continue
        if len(parts) < 2:
            continue
        d = _parse_date(parts[0])
        p = _parse_price(parts[1])
        if d and p is not None:
            rows.append({"date": d, "price": p})
    rows.sort(key=lambda r: r["date"])
    return rows


def parse_eia_v2(payload: dict) -> list[dict]:
    data = (payload.get("response") or {}).get("data") or []
    rows = []
    for rec in data:
        d = _parse_date(str(rec.get("period") or ""))
        p = _parse_price(str(rec.get("value") or ""))
        if d and p is not None:
            rows.append({"date": d, "price": p})
    rows.sort(key=lambda r: r["date"])
    return rows


def parse_html_or_csv_table(text: str) -> list[dict]:
    """Best-effort: FRED-like CSV, or HTML table cells with a date + number."""
    if "," in text.split("\n", 1)[0] and "DATE" in text[:80].upper():
        return parse_fred_csv(text)
    rows = []
    # EIA leaf pages sometimes embed "YYYY-MM-DD,price" or table rows.
    for m in re.finditer(
        r"(20\d{2}-\d{2}-\d{2}|19\d{2}-\d{2}-\d{2})[,\s</>]+([0-9]+(?:\.[0-9]+)?)",
        text,
    ):
        d = m.group(1)
        p = _parse_price(m.group(2))
        if p is not None:
            rows.append({"date": d, "price": p})
    if len(rows) < 50:
        return []
    # de-dupe last price per date
    by = {}
    for rec in rows:
        by[rec["date"]] = rec
    out = list(by.values())
    out.sort(key=lambda r: r["date"])
    return out


def fetch_eia_v2(name: str, key: str) -> tuple[list[dict], list[dict]]:
    area = EIA_V2_AREA[name]
    all_rows: list[dict] = []
    attempts = []
    offset = 0
    while True:
        url = EIA_V2.format(area=area, offset=offset, key=urllib.parse.quote(key))
        body, meta = fetch_bytes(url)
        attempts.append(meta)
        if not body:
            break
        try:
            payload = json.loads(body.decode("utf-8", "replace"))
        except json.JSONDecodeError:
            meta = dict(meta)
            meta["error"] = "json decode"
            break
        chunk = parse_eia_v2(payload)
        if not chunk:
            break
        all_rows.extend(chunk)
        if len(chunk) < 5000:
            break
        offset += 5000
        if offset > 100000:
            break
    by = {r["date"]: r for r in all_rows}
    out = sorted(by.values(), key=lambda r: r["date"])
    return out, attempts


def fetch_series(name: str, spec: dict, eia_key: str | None) -> tuple[list[dict], dict]:
    trail = []
    if eia_key:
        rows, attempts = fetch_eia_v2(name, eia_key)
        trail.extend(attempts)
        if len(rows) >= 250:
            return rows, {"vehicle": "eia_v2", "eia_id": spec["eia_id"], "attempts": trail}
    for label, url in (("eia_leaf", spec["eia_leaf"]), ("eia_xls", spec["eia_xls"])):
        body, meta = fetch_bytes(url)
        trail.append(meta)
        if not body:
            continue
        text = body.decode("utf-8", "replace")
        if "\x00" in text[:200] or text.startswith("\xd0\xcf"):
            trail[-1] = dict(meta, skipped="binary_xls_no_xlrd")
            continue
        rows = parse_html_or_csv_table(text)
        if len(rows) >= 250:
            return rows, {"vehicle": label, "eia_id": spec["eia_id"], "attempts": trail}
    fred_url = FRED_CSV.format(sid=spec["fred_id"])
    body, meta = fetch_bytes(fred_url)
    trail.append(meta)
    if body:
        rows = parse_fred_csv(body.decode("utf-8", "replace"))
        if len(rows) >= 250:
            return rows, {
                "vehicle": "fred_eia_reprint",
                "fred_id": spec["fred_id"],
                "eia_id": spec["eia_id"],
                "attempts": trail,
            }
    return [], {"vehicle": None, "attempts": trail}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "price"])
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(here / "data"))
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    eia_key = os.environ.get("EIA_API_KEY") or os.environ.get("EIA_KEY")
    report: dict = {
        "fetched_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lock": "L-STANDIN-EIA-SPOT",
        "eia_key_present": bool(eia_key),
        "series": {},
    }
    ok = True
    for name, spec in SERIES.items():
        rows, meta = fetch_series(name, spec, eia_key)
        slug = "wti" if name == "WTI" else "brent"
        csv_path = out_dir / f"eia_spot_{slug}.csv"
        if rows:
            write_csv(csv_path, rows)
        else:
            ok = False
        report["series"][name] = {
            **meta,
            "n": len(rows),
            "first": rows[0]["date"] if rows else None,
            "last": rows[-1]["date"] if rows else None,
            "csv": str(csv_path.name) if rows else None,
            "vehicle_fail": len(rows) < 250,
        }
    (out_dir / "eia_spot_fetch.json").write_text(json.dumps(report, indent=2) + "\n")
    wti_n = report["series"]["WTI"]["n"]
    brent_n = report["series"]["Brent"]["n"]
    print(json.dumps({"ok": ok, "wti_n": wti_n, "brent_n": brent_n, "vehicles": {
        "WTI": report["series"]["WTI"].get("vehicle"),
        "Brent": report["series"]["Brent"].get("vehicle"),
    }}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
