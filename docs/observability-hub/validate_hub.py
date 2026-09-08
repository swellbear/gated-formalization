#!/usr/bin/env python3
"""Validate the read-only observability hub before publishing.

Systems runs this after dropping a new export and before committing:

    python3 docs/observability-hub/validate_hub.py

It mirrors, server-side, the checks the browser makes in assets/hub.js, and adds
the ones a browser cannot make -- that a chart declared ``available`` is really
in the published tree, and that no chart path escapes it. Exit status is 0 when
the manifest is publishable and 1 when it is not.

Standard library only. No build step, no dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HUB_DIR = Path(__file__).resolve().parent
PUBLISH_ROOT = HUB_DIR.parent  # docs/ -- what GitHub Pages serves
DEFAULT_MANIFEST = HUB_DIR / "data" / "manifest.json"
INDEX_HTML = HUB_DIR / "index.html"

SCHEMA_VERSION = 1
NOT_YET = "not yet available"
CANONICAL_LANES = ("golf", "learning_lane_15m")
LANE_BADGE = {"golf": "PHASE 1 OBSERVATION", "learning_lane_15m": "LEARNING LANE"}

# The standing posture. Hard-coded in index.html's quiet Hard-NO strip so no export
# can suppress it; the manifest must agree with it rather than replace it.
REQUIRED_GLOBAL_BADGES = (
    "READ ONLY",
    "TRADING NOT ARMED",
    "PAPER OBSERVATION ONLY",
    "AI: NO CASH IN/OUT",
)

# Strings index.html must keep carrying, whatever the data feed says. Presence is what
# is enforced, not loudness: one quiet strip satisfies this, a badge wall is not needed.
REQUIRED_STATIC_STRINGS = (
    "READ ONLY",
    "TRADING NOT ARMED",
    "PAPER OBSERVATION ONLY",
    "AI: NO CASH IN/OUT",
    "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH",
    "127.0.0.1:8765",
)

# Markup that would make the page a control surface. Checked against the whole
# static site, not just the manifest.
BANNED_MARKUP = (
    ("<form", "a form is a control surface"),
    ("<input", "an input invites operating a system this page only views"),
    ("<textarea", "an input invites operating a system this page only views"),
    ("<select", "an input invites operating a system this page only views"),
    ('method="post"', "no write path may exist on this page"),
)

FORBIDDEN_KEYS = {
    "control": {
        "action", "actions", "control", "controls", "button", "buttons",
        "form", "forms", "submit", "endpoint", "endpoints", "api", "api_base",
        "api_url", "api_endpoint", "post", "post_url", "run_url", "ingest",
        "live_run", "shadow_run", "loop", "refresh", "reload", "poll",
        "poll_url", "ws", "ws_url", "websocket", "stream_url", "arm", "arming",
        "armed", "trade", "trades", "trade_url", "order", "orders", "place",
        "place_bet", "cancel", "bet", "bets", "one_tap", "onetap", "autobet",
        "auto_bet",
    },
    "cash": {
        "deposit", "withdraw", "withdrawal", "transfer", "cash", "cash_in",
        "cash_out", "cashout", "cashin", "bankroll", "balance", "funds",
        "wallet", "stake_now", "money", "payout_url",
    },
    "secret": {
        "secret", "secrets", "api_key", "apikey", "api_secret", "token",
        "access_token", "refresh_token", "bearer", "password", "passwd",
        "credential", "credentials", "private_key", "privatekey", "key",
        "keys", "env", "dotenv", "ssh_key", "session", "cookie", "auth",
        "authorization", "kalshi_key", "kalshi_api_key",
    },
}

SECRET_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bAKIA[0-9A-Z]{12,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\."),
    re.compile(
        r"(api[_-]?key|api[_-]?secret|access[_-]?token|client[_-]?secret"
        r"|password|passwd|bearer)\s*[:=]\s*\S{8,}",
        re.IGNORECASE,
    ),
)

DOC_LINK_PREFIX = "https://github.com/swellbear/gated-formalization/"

# Edge language that may never be asserted, in any lane, in any field.
BANNED_CLAIMS = (
    "edge established",
    "edge is established",
    "banked edge",
    "edge validated",
    "validated edge",
    "proven edge",
    "guaranteed",
)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def walk_forbidden(node: object, path: str, report: Report) -> None:
    """Refuse forbidden keys at any depth, and credential-shaped values."""
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            lowered = str(key).lower()
            for kind, names in FORBIDDEN_KEYS.items():
                if lowered in names:
                    report.error(child, f"forbidden {kind}-shaped key {key!r}")
            walk_forbidden(value, child, report)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            walk_forbidden(item, f"{path}[{index}]", report)
    elif isinstance(node, str):
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(node):
                report.error(path, "value looks like a credential; remove it and rotate")
                break


def walk_claims(node: object, path: str, report: Report) -> None:
    """Flag edge claims, except where the text is explicitly denying one."""
    if isinstance(node, dict):
        for key, value in node.items():
            walk_claims(value, f"{path}.{key}" if path else str(key), report)
        return
    if isinstance(node, list):
        for index, item in enumerate(node):
            walk_claims(item, f"{path}[{index}]", report)
        return
    if not isinstance(node, str):
        return
    lowered = node.lower()
    for claim in BANNED_CLAIMS:
        if claim not in lowered:
            continue
        # "NOT EDGE ESTABLISHED" / "never claim edge established" are the
        # required denials, not violations of them.
        window_start = max(0, lowered.index(claim) - 40)
        window = lowered[window_start:lowered.index(claim)]
        if any(word in window for word in ("not ", "never ", "no ", "without ")):
            continue
        report.error(path, f"asserts {claim!r}; edge is never claimed on this page")


def check_chart(chart: dict, lane_id: str, index: int, report: Report) -> None:
    where = f"lanes[{lane_id}].charts[{index}]"
    status = chart.get("status")
    if status not in ("available", NOT_YET):
        report.error(where, f"status must be 'available' or {NOT_YET!r}, got {status!r}")
    for field in ("slot_id", "title"):
        if not chart.get(field):
            report.error(where, f"missing {field}")

    if status != "available":
        if chart.get("path"):
            report.error(where, "unavailable slot must not carry a path")
        if not chart.get("note"):
            report.warn(where, "unavailable slot should say why in 'note'")
        return

    path = chart.get("path")
    if not isinstance(path, str) or not path:
        report.error(where, "status is 'available' but no path is given")
        return
    if re.match(r"^[a-z][a-z0-9+.-]*:", path, re.IGNORECASE) or path.startswith("//"):
        report.error(where, f"path must be relative, got {path!r}")
        return
    if path.startswith("/"):
        report.error(where, f"path must be relative, got {path!r}")
        return
    if not path.lower().endswith(".png"):
        report.error(where, f"charts are PNG only, got {path!r}")
        return

    resolved = (HUB_DIR / path).resolve()
    try:
        resolved.relative_to(PUBLISH_ROOT.resolve())
    except ValueError:
        report.error(
            where,
            f"path escapes the published tree ({PUBLISH_ROOT.name}/): {path!r}",
        )
        return
    if not resolved.is_file():
        report.error(
            where,
            f"declared available but the file is not in the tree: {path!r}. "
            f"Set status to {NOT_YET!r} instead of pointing at a missing file.",
        )
        return
    with resolved.open("rb") as handle:
        if handle.read(8) != b"\x89PNG\r\n\x1a\n":
            report.error(where, f"{path!r} is not a PNG")


def check_links(links: object, where: str, report: Report) -> None:
    if not isinstance(links, list):
        return
    for index, link in enumerate(links):
        spot = f"{where}[{index}]"
        if not isinstance(link, dict):
            report.error(spot, "link must be an object")
            continue
        href = link.get("href", "")
        if not isinstance(href, str) or not href:
            report.error(spot, "link has no href")
            continue
        if href.startswith(DOC_LINK_PREFIX):
            continue
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.IGNORECASE):
            report.error(
                spot,
                f"off-repo link dropped by the viewer: {href!r}. "
                f"Use {DOC_LINK_PREFIX}… or a relative path.",
            )
            continue
        if not (HUB_DIR / href.split("#", 1)[0]).exists():
            report.warn(spot, f"relative link target not found: {href!r}")


def displayed_data_strings(lane: dict) -> list[tuple[str, str]]:
    """The lane's figure-bearing labels and values.

    Deliberately excludes prose -- notes, scope notes, headlines, summaries.
    Prose is exactly where a lane *should* name the other lane in order to
    disclaim it; a figure labelled with the other lane's identity is the actual
    blur.
    """
    found: list[tuple[str, str]] = []

    def collect(rows: object, where: str) -> None:
        if not isinstance(rows, list):
            return
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            for field in ("label", "value"):
                text = row.get(field)
                if isinstance(text, str):
                    found.append((f"{where}[{index}].{field}", text))

    settle = lane.get("settle") or {}
    ledger = lane.get("paper_ledger") or {}
    last_run = lane.get("last_run") or {}
    collect(last_run.get("fields"), "last_run.fields")
    collect(settle.get("counts"), "settle.counts")
    collect(settle.get("sources"), "settle.sources")
    collect(settle.get("residual"), "settle.residual")
    collect(ledger.get("rows"), "paper_ledger.rows")

    observation = settle.get("observation")
    if isinstance(observation, dict):
        for field in ("label", "value"):
            text = observation.get(field)
            if isinstance(text, str):
                found.append((f"settle.observation.{field}", text))

    for index, record in enumerate(lane.get("records") or []):
        if isinstance(record, dict):
            for field in ("record_id", "title", "verdict", "lean"):
                text = record.get(field)
                if isinstance(text, str):
                    found.append((f"records[{index}].{field}", text))
            collect(record.get("rows"), f"records[{index}].rows")

    for index, chart in enumerate(lane.get("charts") or []):
        if isinstance(chart, dict):
            for field in ("slot_id", "title", "path"):
                text = chart.get(field)
                if isinstance(text, str):
                    found.append((f"charts[{index}].{field}", text))

    return found


# Golf's frozen Phase 1 figures. These are golf-lane facts. If any of them turns
# up in another lane's data, the lanes have been blurred -- which is the single
# failure this hub exists to prevent.
GOLF_ONLY_MARKERS = (
    "0.279",
    "34/122",
    "wc1",
    "mitchell",
    "keep_expert",
    "phase 1 observation",
    "espn",
    "401811",
)


def check_anti_blur(lane: dict, where: str, report: Report) -> None:
    lane_id = str(lane.get("lane_id"))
    fields = displayed_data_strings(lane)

    for other in CANONICAL_LANES:
        if other == lane_id:
            continue
        for spot, text in fields:
            if other in text:
                report.error(
                    f"{where}.{spot}",
                    f"a displayed figure is labelled with the other lane id {other!r}; "
                    "lanes must not be blurred",
                )

    if lane_id == "golf":
        return
    for spot, text in fields:
        lowered = text.lower()
        for marker in GOLF_ONLY_MARKERS:
            if marker in lowered:
                report.error(
                    f"{where}.{spot}",
                    f"carries the golf-lane marker {marker!r}. Golf Phase 1 figures "
                    f"are never shown as {lane_id} figures.",
                )


def check_lane(lane: dict, report: Report) -> None:
    lane_id = lane.get("lane_id")
    where = f"lanes[{lane_id}]"
    if lane_id not in CANONICAL_LANES:
        report.error(
            where,
            f"lane_id must be one of {list(CANONICAL_LANES)}, got {lane_id!r}",
        )
        return

    for field in (
        "label", "tab_label", "lane_badge", "badges", "summary_line",
        "source_kind", "lane_scope_note", "last_run", "settle",
        "paper_ledger", "records", "charts",
    ):
        if field not in lane:
            report.error(where, f"missing required field {field!r}")

    if lane.get("lane_badge") != LANE_BADGE[lane_id]:
        report.error(
            where,
            f"lane_badge for {lane_id} must be {LANE_BADGE[lane_id]!r}, "
            f"got {lane.get('lane_badge')!r}",
        )
    if lane.get("lane_badge") not in (lane.get("badges") or []):
        report.error(where, "lane_badge must also appear in badges")

    for required in ("NOT ARMED", "PAPER OBSERVATION ONLY", "AI: NO CASH IN/OUT"):
        if required not in (lane.get("badges") or []):
            report.error(where, f"badges must include {required!r}")

    check_anti_blur(lane, where, report)

    settle = lane.get("settle") or {}
    state = settle.get("banner_state")
    if state not in ("pending", "off", "not_available"):
        report.error(f"{where}.settle", f"banner_state {state!r} is not recognised")
    if state == "pending" and not settle.get("banner"):
        report.error(f"{where}.settle", "banner_state 'pending' needs a banner string")
    if state == "not_available" and settle.get("counts"):
        report.error(
            f"{where}.settle",
            "banner_state 'not_available' must not carry counts",
        )
    observation = settle.get("observation")
    if isinstance(observation, dict) and not observation.get("chips"):
        report.error(
            f"{where}.settle.observation",
            "a hit-rate figure must carry its qualifier chips",
        )

    last_run = lane.get("last_run") or {}
    if last_run.get("status") == NOT_YET and last_run.get("fields"):
        report.error(
            f"{where}.last_run",
            f"status is {NOT_YET!r} but fields are populated",
        )

    ledger = lane.get("paper_ledger") or {}
    if ledger.get("status") == NOT_YET and ledger.get("rows"):
        report.error(
            f"{where}.paper_ledger",
            f"status is {NOT_YET!r} but rows are populated",
        )

    records = lane.get("records")
    if not isinstance(records, list):
        report.error(f"{where}.records", "records must be a list")
    elif not records and not lane.get("records_note"):
        report.error(
            f"{where}.records",
            "an empty records list needs records_note saying why",
        )
    else:
        for index, record in enumerate(records):
            spot = f"{where}.records[{index}]"
            if not isinstance(record, dict):
                report.error(spot, "record must be an object")
                continue
            for field in ("record_id", "title", "verdict", "lane_scope_note"):
                if not record.get(field):
                    report.error(spot, f"missing {field!r}")
            check_links(record.get("links"), f"{spot}.links", report)

    charts = lane.get("charts")
    if not isinstance(charts, list):
        report.error(f"{where}.charts", "charts must be a list")
    elif not charts and not lane.get("charts_note"):
        report.error(
            f"{where}.charts",
            "an empty charts list needs charts_note saying why",
        )
    else:
        seen: set[str] = set()
        for index, chart in enumerate(charts):
            if not isinstance(chart, dict):
                report.error(f"{where}.charts[{index}]", "chart must be an object")
                continue
            slot = str(chart.get("slot_id"))
            if slot in seen:
                report.error(f"{where}.charts[{index}]", f"duplicate slot_id {slot!r}")
            seen.add(slot)
            check_chart(chart, str(lane_id), index, report)

    check_links(lane.get("docs"), f"{where}.docs", report)


def check_static_site(report: Report) -> None:
    if not INDEX_HTML.is_file():
        report.error("index.html", "missing")
        return
    html = INDEX_HTML.read_text(encoding="utf-8")
    lowered = html.lower()
    for needle, why in BANNED_MARKUP:
        if needle in lowered:
            report.error("index.html", f"contains {needle!r} -- {why}")
    for needle in REQUIRED_STATIC_STRINGS:
        if needle not in html:
            report.error(
                "index.html",
                f"the static Hard-NO strip must keep carrying {needle!r}",
            )

    for asset in sorted((HUB_DIR / "assets").glob("*")):
        text = asset.read_text(encoding="utf-8", errors="replace")
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(text):
                report.error(
                    f"assets/{asset.name}",
                    "contains something credential-shaped; committed client code "
                    "must carry no keys or secrets",
                )
                break

    hub_js = HUB_DIR / "assets" / "hub.js"
    if hub_js.is_file():
        js = hub_js.read_text(encoding="utf-8")
        if re.search(r"""method\s*:\s*['"](POST|PUT|PATCH|DELETE)""", js, re.IGNORECASE):
            report.error("assets/hub.js", "issues a write request; this page is read-only")
        if "innerHTML" in js:
            report.error(
                "assets/hub.js",
                "uses innerHTML; manifest values must reach the DOM via textContent only",
            )
        # The enlarge overlay must only ever be reachable from a loaded chart.
        if "lightbox.open" in js and "addEventListener(\"load\"" not in js:
            report.error(
                "assets/hub.js",
                "the enlarge overlay must only be wired from a chart that loaded",
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        default=str(DEFAULT_MANIFEST),
        help="path to manifest.json (default: data/manifest.json beside this script)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures",
    )
    parser.add_argument(
        "--write-report",
        default="",
        help="write a JSON report with exit code, findings, and the SHA-256 of the exact bytes validated",
    )
    args = parser.parse_args()

    report = Report()
    manifest_path = Path(args.manifest)

    if not manifest_path.is_file():
        print(f"FAIL  manifest not found: {manifest_path}")
        return 1
    raw = manifest_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL  manifest is not valid JSON: {exc}")
        return 1
    if not isinstance(manifest, dict):
        print("FAIL  manifest must be a JSON object")
        return 1

    if manifest.get("schema_version") != SCHEMA_VERSION:
        report.error(
            "schema_version",
            f"expected {SCHEMA_VERSION}, got {manifest.get('schema_version')!r}",
        )

    hub = manifest.get("hub")
    if not isinstance(hub, dict):
        report.error("hub", "missing or not an object")
    else:
        for field in ("title", "generated_at", "source_kind", "source_note"):
            if not hub.get(field):
                report.error("hub", f"missing {field!r}")
        if hub.get("source_kind") not in ("fixture", "export"):
            report.error(
                "hub.source_kind",
                f"must be 'fixture' or 'export', got {hub.get('source_kind')!r}",
            )

    global_block = manifest.get("global")
    if not isinstance(global_block, dict):
        report.error("global", "missing or not an object")
    else:
        badges = global_block.get("badges") or []
        if list(badges) != list(REQUIRED_GLOBAL_BADGES):
            report.error(
                "global.badges",
                "must match the static wall in index.html exactly: "
                f"{list(REQUIRED_GLOBAL_BADGES)}",
            )
        if not global_block.get("hard_nos"):
            report.error("global.hard_nos", "the Hard NO list must be present")

    lanes = manifest.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        report.error("lanes", "must be a non-empty list")
    else:
        seen_ids = [lane.get("lane_id") for lane in lanes if isinstance(lane, dict)]
        for lane_id in CANONICAL_LANES:
            if lane_id not in seen_ids:
                report.warn("lanes", f"canonical lane {lane_id!r} is not published")
        if len(seen_ids) != len(set(seen_ids)):
            report.error("lanes", "duplicate lane_id")
        for lane in lanes:
            if isinstance(lane, dict):
                check_lane(lane, report)
            else:
                report.error("lanes", "lane must be an object")

    walk_forbidden(manifest, "", report)
    walk_claims(manifest, "", report)
    check_static_site(report)

    for warning in report.warnings:
        print(f"WARN  {warning}")
    for error in report.errors:
        print(f"ERROR {error}")

    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    exit_code = 1 if failed else 0
    if args.write_report:
        payload = {
            "schema": 1,
            "role": "validator",
            "validated_at": datetime.now(timezone.utc).astimezone().isoformat(),
            "manifest_path": str(manifest_path.resolve()),
            "byte_len": len(raw),
            "sha256": digest,
            "strict": bool(args.strict),
            "exit_code": exit_code,
            "errors": list(report.errors),
            "warnings": list(report.warnings),
        }
        out = Path(args.write_report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"REPORT {out} sha256={digest} exit_code={exit_code}")
    if failed:
        print(
            f"\nFAIL  {len(report.errors)} error(s), {len(report.warnings)} warning(s). "
            "Do not publish."
        )
        return 1
    print(
        f"\nOK    hub is publishable. {len(report.warnings)} warning(s). "
        "Read-only, no controls, no cash, no secrets, no invented charts."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
