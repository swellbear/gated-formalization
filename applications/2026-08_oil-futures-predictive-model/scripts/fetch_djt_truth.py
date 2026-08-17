#!/usr/bin/env python3
"""Fetch Trump Truth Social archive (CNN dump; stiles fallback).

Stand-in statement tape for L-STANDIN-DJT-TRUTH. Does not score oil.
Does not treat this as an official White House archive.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (compatible; gated-formalization-standin/1.0)"}
PRIMARY = "https://ix.cnn.io/data/truth-social/truth_archive.json"
FALLBACK = "https://stilesdata.com/trump-truth-social-archive/truth_archive.json"
TAG = re.compile(r"<[^>]+>")
SPACE = re.compile(r"\s+")


def strip_html(raw: str) -> str:
    text = TAG.sub(" ", raw or "")
    text = html.unescape(text)
    return SPACE.sub(" ", text).strip()


def fetch_json(url: str) -> tuple[object | None, dict]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
            status = r.status
    except urllib.error.HTTPError as e:
        return None, {"url": url, "ok": False, "http_status": e.code, "error": str(e)}
    except Exception as e:
        return None, {"url": url, "ok": False, "http_status": None, "error": str(e)}
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception as e:
        return None, {"url": url, "ok": False, "http_status": status, "error": f"json: {e}"}
    return payload, {"url": url, "ok": True, "http_status": status, "n_bytes": len(body)}


def posts_from_payload(payload: object) -> list[dict]:
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        for key in ("posts", "data", "items", "archive"):
            if isinstance(payload.get(key), list):
                items = payload[key]
                break
        else:
            items = []
    else:
        items = []
    out = []
    seen = set()
    for rec in items:
        if not isinstance(rec, dict):
            continue
        pid = str(rec.get("id") or rec.get("uri") or rec.get("url") or "")
        created = rec.get("created_at") or rec.get("createdAt") or rec.get("date") or ""
        text = strip_html(str(rec.get("content") or rec.get("text") or rec.get("body") or ""))
        url = str(rec.get("url") or rec.get("uri") or "")
        if not created:
            continue
        try:
            if created.endswith("Z"):
                ts = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
            else:
                ts = dt.datetime.fromisoformat(created)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=dt.timezone.utc)
            day = ts.astimezone(dt.timezone.utc).date().isoformat()
        except Exception:
            continue
        if not text:
            continue
        key = pid or f"{day}|{text[:80]}"
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "id": pid,
                "created_at": created,
                "date_utc": day,
                "url": url,
                "text": text,
            }
        )
    out.sort(key=lambda r: (r["date_utc"], r["created_at"], r["id"]))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="data")
    args = p.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    used = PRIMARY
    payload, meta = fetch_json(PRIMARY)
    if payload is None:
        used = FALLBACK
        payload, meta = fetch_json(FALLBACK)
    if payload is None:
        (out_dir / "djt_truth_fetch.json").write_text(json.dumps({"ok": False, "attempts": [meta]}, indent=2) + "\n")
        print(json.dumps({"ok": False, "error": "fetch failed", "meta": meta}, indent=2))
        return 1

    posts = posts_from_payload(payload)
    csv_path = out_dir / "djt_truth_posts.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "created_at", "date_utc", "url", "text"])
        w.writeheader()
        w.writerows(posts)

    info = {
        "badge": "stand-in",
        "lock": "L-STANDIN-DJT-TRUTH",
        "ok": True,
        "source_used": used,
        "fetch": meta,
        "fetched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "n_posts": len(posts),
        "first": posts[0]["date_utc"] if posts else None,
        "last": posts[-1]["date_utc"] if posts else None,
        "note": "Truth Social only. Not White House remarks. UTC calendar date of created_at.",
    }
    (out_dir / "djt_truth_fetch.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps({k: info[k] for k in info if k != "fetch"}, indent=2))
    print(f"wrote {csv_path} rows={len(posts)}")
    return 0 if posts else 1


if __name__ == "__main__":
    raise SystemExit(main())
