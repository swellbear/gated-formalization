#!/usr/bin/env python3
"""Date-gated reminder for the parked leftover callout. Fail open. Stdlib only."""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

TRIGGER = date(2026, 8, 17)
SPEC = "golf-offshoot/docs/PARKED_LEFTOVER_CALLOUT.md"
ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "golf-offshoot" / "docs" / "PARKED_LEFTOVER_CALLOUT.md"
SRC_ROOT = ROOT / "golf-offshoot" / "src"
STATE_DIR = Path(__file__).resolve().parent / ".state"
NAG_STAMP = STATE_DIR / "leftover-callout-nagged"


def _today() -> date:
    raw = os.environ.get("GOLF_LEFTOVER_ASOF", "").strip()
    if raw:
        return date.fromisoformat(raw)
    return date.today()


def _out(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=True))
    sys.stdout.write("\n")


def _is_done() -> bool:
    if SPEC_PATH.is_file():
        head = SPEC_PATH.read_text(encoding="utf-8", errors="replace")[:800]
        if re.search(r"\*\*Status:\*\*\s*DONE", head, re.I):
            return True
        if re.search(r"^Status:\s*DONE", head, re.I | re.M):
            return True
    if SRC_ROOT.is_dir():
        candidates = [
            SRC_ROOT / "golf_offshoot" / "ranking" / "leftover.py",
            SRC_ROOT / "golf_offshoot" / "operating.py",
            SRC_ROOT / "golf_offshoot" / "strategy" / "engine.py",
        ]
        for path in candidates:
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if "def format_leftover_callout" in text:
                return True
    return False


def _golfish(text: str) -> bool:
    return bool(
        re.search(
            r"golf-offshoot|leftover callout|st\.?\s*jude|401811962|"
            r"paper-(settle|lock|ledger)|format_leftover_callout",
            text,
            re.I,
        )
    )


def _maybe_nag_user() -> str | None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        today = _today().isoformat()
        if NAG_STAMP.is_file() and NAG_STAMP.read_text(encoding="utf-8").strip() == today:
            return None
        NAG_STAMP.write_text(today, encoding="utf-8")
    except OSError:
        pass
    return (
        "Golf leftover callout is due now that St. Jude week is over. "
        f"Spec: {SPEC}"
    )


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        _out({})
        return 0
    if not isinstance(payload, dict):
        _out({})
        return 0
    if _is_done():
        _out({})
        return 0

    prompt = " ".join(
        str(payload.get(k) or "")
        for k in ("prompt", "command", "user_prompt", "text")
    )
    due = _today() >= TRIGGER
    if not due:
        if _golfish(prompt) and re.search(r"leftover|callout|implement", prompt, re.I):
            _out(
                {
                    "additional_context": (
                        "Do not implement the leftover callout until after the 2026 "
                        "FedEx St. Jude Championship (ESPN 401811962) is over "
                        f"(not before {TRIGGER.isoformat()} unless settling/scoring). "
                        f"Parked spec: {SPEC}."
                    )
                }
            )
            return 0
        _out({})
        return 0

    ctx = (
        f"DUE: implement the golf-offshoot leftover callout per {SPEC} before other "
        "new golf-offshoot features (settle/scoring of 401811962 may run first if "
        "that is the user ask). Display-only. No GPF residual branches. No stuffing "
        "into theta. Mark Status: DONE on that page when shipped. Ignore this if "
        "the session is GPF/applications work."
    )
    out: dict[str, str] = {"additional_context": ctx}
    msg = _maybe_nag_user()
    if msg:
        out["user_message"] = msg
    _out(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
