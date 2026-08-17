#!/usr/bin/env python3
"""Fetch CFTC Disaggregated Futures-Only COT for NYMEX WTI (067651).

Stand-in positioning tape for L-STANDIN-CFTC-COT. Does not score oil.
Does not treat this as a live desk feed.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import zipfile
from pathlib import Path
import urllib.error
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (compatible; gated-formalization-standin/1.0)"}
CONTRACT = "067651"
ZIP_TMPL = "https://www.cftc.gov/files/dea/history/fut_disagg_txt_{year}.zip"
CURRENT = "https://www.cftc.gov/dea/newcot/f_disagg.txt"
FIRST_YEAR = 2006
SCALE_NOTE = "Net = MM long - MM short (contracts). Hunt script scales by 1e5."


def friday_of_report_week(report: dt.date) -> dt.date:
    # weekday(): Mon=0 … Fri=4. Friday on or after the report date.
    return report + dt.timedelta(days=(4 - report.weekday()) % 7)


def fetch_bytes(url: str, timeout: int = 120) -> tuple[bytes | None, dict]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return body, {"url": url, "ok": True, "http_status": r.status, "n_bytes": len(body)}
    except urllib.error.HTTPError as e:
        return None, {"url": url, "ok": False, "http_status": e.code, "error": str(e)}
    except Exception as e:
        return None, {"url": url, "ok": False, "http_status": None, "error": str(e)}


def _norm(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def _pick_col(fieldnames: list[str], *needles: str) -> str | None:
    norms = {_norm(f): f for f in fieldnames}
    for n in needles:
        if n in norms:
            return norms[n]
    for key, orig in norms.items():
        if all(part in key for part in needles):
            return orig
    return None


def parse_disagg_text(text: str) -> list[dict]:
    sample = text.lstrip("\ufeff")
    f = io.StringIO(sample)
    reader = csv.DictReader(f)
    if not reader.fieldnames:
        return []
    code_col = _pick_col(reader.fieldnames, "cftccontractmarketcode") or _pick_col(
        reader.fieldnames, "cftc", "contract", "market", "code"
    )
    date_col = _pick_col(reader.fieldnames, "reportdateasyyyymmdd") or _pick_col(
        reader.fieldnames, "reportdate"
    )
    long_col = _pick_col(reader.fieldnames, "mmoneypositionslongall") or _pick_col(
        reader.fieldnames, "mmoney", "long", "all"
    )
    short_col = _pick_col(reader.fieldnames, "mmoneypositionsshortall") or _pick_col(
        reader.fieldnames, "mmoney", "short", "all"
    )
    name_col = _pick_col(reader.fieldnames, "marketandexchangenames") or _pick_col(
        reader.fieldnames, "contractmarketname"
    )
    if not (code_col and date_col and long_col and short_col):
        return []
    out = []
    for rec in reader:
        code = str(rec.get(code_col) or "").strip().strip("'")
        if code != CONTRACT:
            continue
        raw_d = str(rec.get(date_col) or "").strip().strip("'")
        try:
            if "T" in raw_d:
                report = dt.date.fromisoformat(raw_d.split("T", 1)[0])
            else:
                report = dt.date.fromisoformat(raw_d[:10])
        except Exception:
            continue
        try:
            mm_long = float(str(rec.get(long_col) or "0").replace(",", ""))
            mm_short = float(str(rec.get(short_col) or "0").replace(",", ""))
        except ValueError:
            continue
        name = str(rec.get(name_col) or "").strip() if name_col else ""
        release = friday_of_report_week(report)
        out.append(
            {
                "report_date": report.isoformat(),
                "release_date": release.isoformat(),
                "contract_code": CONTRACT,
                "market": name,
                "mm_long": mm_long,
                "mm_short": mm_short,
                "mm_net": mm_long - mm_short,
            }
        )
    return out


def parse_zip(blob: bytes) -> list[dict]:
    rows = []
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.lower()
            if not (name.endswith(".txt") or name.endswith(".csv")):
                continue
            text = zf.read(info).decode("latin-1", errors="replace")
            rows.extend(parse_disagg_text(text))
    return rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="data")
    p.add_argument("--first-year", type=int, default=FIRST_YEAR)
    p.add_argument("--last-year", type=int, default=dt.date.today().year)
    args = p.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    attempts: list[dict] = []
    by_report: dict[str, dict] = {}

    for year in range(args.first_year, args.last_year + 1):
        url = ZIP_TMPL.format(year=year)
        blob, meta = fetch_bytes(url)
        attempts.append(meta)
        if blob is None:
            continue
        for rec in parse_zip(blob):
            by_report[rec["report_date"]] = rec

    blob, meta = fetch_bytes(CURRENT)
    attempts.append(meta)
    if blob is not None:
        for rec in parse_disagg_text(blob.decode("latin-1", errors="replace")):
            by_report[rec["report_date"]] = rec

    rows = sorted(by_report.values(), key=lambda r: r["report_date"])
    csv_path = out_dir / "cftc_cl_mm_net.csv"
    fields = ["report_date", "release_date", "contract_code", "market", "mm_long", "mm_short", "mm_net"]
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    info = {
        "badge": "stand-in",
        "lock": "L-STANDIN-CFTC-COT",
        "ok": bool(rows),
        "contract_code": CONTRACT,
        "report": "disaggregated_futures_only",
        "fetched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "n_reports": len(rows),
        "first": rows[0]["report_date"] if rows else None,
        "last": rows[-1]["report_date"] if rows else None,
        "first_release": rows[0]["release_date"] if rows else None,
        "last_release": rows[-1]["release_date"] if rows else None,
        "n_ok_attempts": sum(1 for a in attempts if a.get("ok")),
        "n_attempts": len(attempts),
        "note": SCALE_NOTE + " Release date = Friday of the report week.",
        "attempts": attempts,
    }
    (out_dir / "cftc_cot_fetch.json").write_text(json.dumps(info, indent=2) + "\n")
    slim = {k: info[k] for k in info if k != "attempts"}
    print(json.dumps(slim, indent=2))
    print(f"wrote {csv_path} rows={len(rows)}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
