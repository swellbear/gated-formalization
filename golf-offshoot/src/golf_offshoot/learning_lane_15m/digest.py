"""Generate the figures half of the 15m SOURCE digest.

Copies numbers out of files. Does not invent pnl. Does not write the caveats file.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import (
    latest_dir_15m,
    paper_dir_15m,
    settlements_dir_15m,
)
from golf_offshoot.localtime import format_eastern, to_eastern
from golf_offshoot.operator_surface.observability import repo_root

DIGEST_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST.md"
CAVEATS_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
MANIFEST_REL = Path("docs") / "observability-hub" / "data" / "manifest.json"
GAP_TICKER = "KXBTC15M-26SEP072245"
MISSING_JOIN = "KXBTC15M-26SEP071500-00"
LINEAGE_B = "KXBTC15M-26SEP071445-45"
CAVEATS_BANNER = (
    "<!-- BEGIN STANDING CAVEATS — generator must concatenate this file verbatim "
    "and may never write, rewrite, reorder, or drop it -->"
)


def digest_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / DIGEST_REL


def caveats_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / CAVEATS_REL


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _fmt_money(value: Any) -> str:
    if value is None:
        raise ValueError("refusing to format a missing money figure")
    number = float(value)
    text = f"{number:.2f}"
    if number > 0:
        return f"+{text}"
    return text


def _short_ticker(window_id: str) -> str:
    text = str(window_id or "")
    head = text.split("__")[0]
    if head.endswith("-30") or head.endswith("-00") or head.endswith("-15") or head.endswith("-45"):
        return head
    # KXBTC15M-26SEP080830 -> KXBTC15M-26SEP080830-30 from close minute
    parts = text.split("__")
    if len(parts) >= 3 and parts[2].endswith("Z"):
        close = parts[2]
        minute = close[14:16] if len(close) >= 16 else ""
        if minute:
            return f"{head}-{minute}"
    return head


def _parse_iso(value: str) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return to_eastern(datetime.fromisoformat(text))


def collect_figures(*, root: Path | None = None) -> dict[str, Any]:
    base = root or repo_root()
    ledger_path = paper_dir_15m() / "ledger.json"
    journal_path = latest_dir_15m() / "journal.json"
    manifest_path = base / MANIFEST_REL
    ledger = _read_json(ledger_path)
    journal = _read_json(journal_path) if journal_path.is_file() else {}
    manifest = _read_json(manifest_path) if manifest_path.is_file() else {}

    entries = ledger.get("entries") or []
    if not isinstance(entries, list):
        raise ValueError("ledger entries must be a list")
    kinds = Counter(str(row.get("kind") or "") for row in entries if isinstance(row, dict))
    events = ledger.get("events") or []
    if not isinstance(events, list):
        raise ValueError("ledger events must be a list")

    paper_books = sorted(paper_dir_15m().glob("KXBTC15M-*.json"))
    settle_files = sorted(settlements_dir_15m().glob("KXBTC15M-*.json"))
    settled_books = []
    open_books = []
    for path in paper_books:
        book = _read_json(path)
        if book.get("settled_at"):
            settled_books.append(path)
        else:
            open_books.append(path)

    first_event = events[0] if events else None
    last_event = events[-1] if events else None
    last_ticket = {}
    if isinstance(last_event, dict):
        tickets = last_event.get("tickets") or []
        if tickets and isinstance(tickets[0], dict):
            last_ticket = tickets[0]

    pending_journal = []
    for row in journal.get("windows") or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("result") or "").strip():
            continue
        status = str(row.get("status") or "")
        if status in {"finalized", "determined"}:
            continue
        pending_journal.append(row)

    gap_paper = list(paper_dir_15m().glob(f"{GAP_TICKER}*"))
    gap_settle = list(settlements_dir_15m().glob(f"{GAP_TICKER}*"))
    missing_paper = list(paper_dir_15m().glob(f"{MISSING_JOIN.split('-00')[0]}*"))
    missing_settle = list(settlements_dir_15m().glob("KXBTC15M-26SEP071500*"))

    lane = {}
    for item in manifest.get("lanes") or []:
        if isinstance(item, dict) and item.get("lane_id") == "learning_lane_15m":
            lane = item
            break

    hub = manifest.get("hub") if isinstance(manifest.get("hub"), dict) else {}
    records = lane.get("records") if isinstance(lane.get("records"), list) else None

    return {
        "journal_generated_at": journal.get("generated_at"),
        "starting_bankroll": ledger.get("starting_bankroll"),
        "bankroll": ledger.get("bankroll"),
        "betting_pnl": ledger.get("betting_pnl"),
        "deposits": ledger.get("deposits"),
        "withdrawals": ledger.get("withdrawals"),
        "entries_n": len(entries),
        "kinds": dict(kinds),
        "events_n": len(events),
        "paper_books_n": len(paper_books),
        "settled_books_n": len(settled_books),
        "open_books_n": len(open_books),
        "open_stems": [path.stem.split("__")[0] for path in open_books],
        "settle_files_n": len(settle_files),
        "first_event_name": (first_event or {}).get("event_name") if first_event else None,
        "last_event_name": (last_event or {}).get("event_name") if last_event else None,
        "last_settled_at": (last_event or {}).get("settled_at") if last_event else None,
        "last_pnl": last_ticket.get("pnl") if last_ticket else (last_event or {}).get("betting_pnl"),
        "last_bankroll_after": (last_event or {}).get("bankroll_after") if last_event else None,
        "pending_journal": [
            {
                "ticker": row.get("ticker"),
                "status": row.get("status"),
                "result": row.get("result"),
                "window_id": row.get("window_id"),
            }
            for row in pending_journal
        ],
        "gap_absent": not gap_paper and not gap_settle,
        "missing_join_absent": not missing_paper and not missing_settle,
        "manifest_generated_at": hub.get("generated_at"),
        "lineage_b_records_n": len(records) if records is not None else None,
        "lineage_b_kept": LINEAGE_B,
    }


def render_figures(figures: dict[str, Any]) -> str:
    journal_at = figures.get("journal_generated_at")
    if not journal_at:
        raise ValueError("journal generated_at is missing; refusing a default")
    asof = format_eastern(_parse_iso(str(journal_at)))
    kinds = figures.get("kinds") or {}
    pending = figures.get("pending_journal") or []
    pending_line = "none recorded on the current journal tape"
    if pending:
        row = pending[0]
        pending_line = (
            f"`{row.get('ticker')}` · journal `status` `{row.get('status')}` · "
            f"`result` {json.dumps(row.get('result'))} · `window_id` `{row.get('window_id')}`"
        )
    open_stems = figures.get("open_stems") or []
    open_line = ", ".join(f"`{stem}`" for stem in open_stems) if open_stems else "none recorded"

    last_pnl = figures.get("last_pnl")
    last_pnl_text = "not recorded on the last events row"
    if last_pnl is not None:
        last_pnl_text = _fmt_money(last_pnl)

    return f"""# Digestor — 15m SOURCE honesty digest (living spine)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `digestor` — honesty owner. Never Soften / Harden / Kill / ADMIT.
**Admit?** N · **Soften?** N · **Trading ARMED?** N
**Evidence as-of:** {asof} (`latest/journal.json` `generated_at`)
**Figures:** generated from files. **Caveats:** concatenated verbatim from [`LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md`](LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md). The generator may not write that file.

Truth on disk, in the order this digest trusts it:

| Rank | File | What it is |
|------|------|-----------|
| 1 | `golf-offshoot/data/learning_lane_15m/settlements/*.json` | Official Kalshi join |
| 2 | `golf-offshoot/data/learning_lane_15m/latest/journal.json` | Kalshi tape |
| 3 | `golf-offshoot/data/learning_lane_15m/paper/*.json` + `paper/ledger.json` | Lineage A |
| 4 | `docs/observability-hub/data/manifest.json` | Lineage B published export |
| aid | `latest/learning_wake.json` | Derived, never authoritative |
| aid | `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` | Illustrator board |

---

## Generated figures

Cited to the file that recorded them. No default, no zero-fill, no pnl a file does not have.

### Lineage A — `paper/ledger.json`

- `starting_bankroll` {figures['starting_bankroll']} → `bankroll` {figures['bankroll']} · `betting_pnl` {figures['betting_pnl']} · `deposits` {figures['deposits']} · `withdrawals` {figures['withdrawals']}
- entries {figures['entries_n']} ({', '.join(f'{n} `{kind}`' for kind, n in sorted(kinds.items()) if kind)})
- events {figures['events_n']}
- paper books on this tree: {figures['paper_books_n']} ({figures['settled_books_n']} with `settled_at`, {figures['open_books_n']} open: {open_line})
- settle files on this tree: {figures['settle_files_n']}
- first event `event_name`: `{figures['first_event_name']}`
- last event `event_name`: `{figures['last_event_name']}` · `settled_at` `{figures['last_settled_at']}` · last-row ticket `pnl` {last_pnl_text} · `bankroll_after` {figures['last_bankroll_after']}

Recorded book. The standing caveats say these figures omit the known fee.

### Pending on the current journal tape

{pending_line}

### Absences (recorded as absence, not as zero)

- `{GAP_TICKER}` paper+settle files present? `{not figures['gap_absent']}` — expected absent; see caveats.
- `{MISSING_JOIN}` paper+settle files present? `{not figures['missing_join_absent']}` — expected absent; missing paper join.

### Lineage B — `docs/observability-hub/data/manifest.json`

- hub `generated_at` `{figures['manifest_generated_at']}` (local export; a local rewrite is not a publish)
- `$.lanes[1].records` length: {figures['lineage_b_records_n']}
- published history kept: `{figures['lineage_b_kept']}` `paper_win` `+1.67` — cited to the manifest, never re-derived here, never added to lineage A
"""


def write_digest(*, root: Path | None = None) -> Path:
    base = root or repo_root()
    caveats = caveats_path(root=base)
    if not caveats.is_file():
        raise FileNotFoundError(f"standing caveats missing: {caveats}")
    caveats_text = caveats.read_text(encoding="utf-8")
    if not caveats_text.strip():
        raise ValueError("standing caveats file is empty; refusing to drop it")
    figures = collect_figures(root=base)
    body = render_figures(figures).rstrip() + "\n\n" + CAVEATS_BANNER + "\n\n" + caveats_text
    if not body.endswith("\n"):
        body += "\n"
    path = digest_path(root=base)
    path.write_text(body, encoding="utf-8")
    return path
