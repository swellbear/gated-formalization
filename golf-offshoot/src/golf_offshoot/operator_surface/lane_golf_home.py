"""Golf (Kalshi) operator-shell chrome. Display copy only.

Upgrades the live Golf (Kalshi) gym to the locked hub-intent glance /
cockpit language. Does not invent pnl, mix 15m lineage A, retune golf θ,
restyle WC1 / Ill, or arm trading. Optional-imports live golf-kalshi modules
when they exist on the tree; otherwise the page stays honest and idle.
"""

from __future__ import annotations

import html
import importlib
import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF, golf_data_root
from golf_offshoot.operator_surface.lanes import SELECTOR_FIELD
from golf_offshoot.operator_surface.runner import RunRecord, format_run_record

HEADER_TITLE = "Golf (Kalshi) paper watch"
HEADER_KICKER = "Golf Kalshi paper gym"
TRUST_LINE = "Paper · not armed"
GYM_LOCK_NOTE = "gym lock"
GYM_LOCK = "Golf (Kalshi)"
DATA_MARKET = "golf-kalshi"

FARM_HELP = (
    "Discovery notebooks for this gym later (sleeve mix, tour haircut, unmatched rate). "
    "Not live. Not hour-close. Not 2-to-1. Not coinflip. Lab chair for 15m farm stays on 15m."
)
HONER_HELP = (
    "Own sandbox. Does not consult 15m decide(). No combined bankroll. No Lineage A."
)
FARM_IDLE = "Idle. no golf tape yet — wait for paper settles"
HONER_IDLE = "Idle. no golf tape yet — wait for paper settles"
MUSEUM_HELP = "WC1 fail / not proven. Not this gym. Charts are the previous claim — not restyled."
CATALOG_MISSING = (
    "Golf catalog module is not on this checkout. The live Windows tree loads the series "
    "book here. Counts are not invented."
)
BOOK_MISSING = "Golf (Kalshi) book not on this checkout — none invented"

TABS = (
    ("home", "Home"),
    ("scoreboard", "Scoreboard"),
    ("lab", "Lab"),
    ("ops", "Ops"),
    ("farm", "Farm"),
    ("honer", "Honer"),
    ("museum", "Museum"),
)

ACTION_BUTTONS_GOLF = (
    (
        "ingest",
        "Golf Kalshi tick",
        "One golf Kalshi tick on the live gym. Does not write Polymarket ledgers. "
        "Does not stop the 15m PaperWatch.",
    ),
    (
        "live",
        "Paper fill if brain can see",
        "One golf Kalshi tick. Paper fill if the brain can see. Observation only.",
    ),
    (
        "shadow",
        "Re-read golf ledger",
        "Re-read the golf Kalshi ledger. Nothing is placed.",
    ),
    (
        "loop",
        "Extra golf tick",
        "One golf Kalshi tick.",
    ),
    (
        "refresh",
        "Reload files",
        "Re-read saved files from disk. No run is started.",
    ),
)

_HOOK_MODULES = (
    "golf_offshoot.golf_kalshi.hub",
    "golf_offshoot.golf_kalshi.board",
    "golf_offshoot.golf_kalshi.watch",
    "golf_offshoot.golf_kalshi.catalog",
    "golf_offshoot.golf_kalshi",
    "golf_offshoot.kalshi_golf.hub",
    "golf_offshoot.kalshi_golf",
)

_ROOT_OVERRIDE: Path | None = None


def set_golf_kalshi_root_override(path: Path | None) -> None:
    """Test hook. None restores default resolution."""
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def golf_kalshi_root() -> Path:
    if _ROOT_OVERRIDE is not None:
        return _ROOT_OVERRIDE
    root = golf_data_root()
    for candidate in (
        root / "golf_kalshi",
        root / "golf-kalshi",
        root.parent / "golf_kalshi",
        Path(__file__).resolve().parents[3] / "data" / "golf_kalshi",
    ):
        if candidate.is_dir():
            return candidate
    return root / "golf_kalshi"


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError):
        return None
    return data if isinstance(data, dict) else None


def _fmt_money(value: object) -> str:
    if value is None or value == "":
        return ""
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        text = str(value).strip()
        return text


def _call(mod: Any, name: str, *args: Any) -> Any:
    fn = getattr(mod, name, None)
    if not callable(fn):
        return None
    try:
        return fn(*args)
    except Exception:
        return None


def golf_kalshi_module() -> Any | None:
    for name in _HOOK_MODULES:
        try:
            return importlib.import_module(name)
        except Exception:
            continue
    return None


def golf_kalshi_present() -> bool:
    snap = golf_kalshi_snapshot()
    return bool(snap.get("present"))


def golf_kalshi_snapshot() -> dict[str, Any]:
    """Copy golf Kalshi figures from a live module or files. Never invent."""
    snap: dict[str, Any] = {
        "present": False,
        "source": "missing",
        "watch_kind": "off",
        "watch_label": "Watch off",
        "watch_at": "",
        "tickets_n": None,
        "pnl": "",
        "bankroll": "",
        "fees": "",
        "halt": None,
        "field_hunt": "",
        "sleeves": [],
        "tickets": [],
        "catalog_counts": {},
        "catalog_html": "",
        "recipe": "",
        "farm_status": FARM_IDLE,
        "honer_status": HONER_IDLE,
        "module": False,
    }
    mod = golf_kalshi_module()
    if mod is not None:
        payload = _call(mod, "operator_snapshot") or _call(mod, "hub_snapshot") or _call(mod, "snapshot")
        if isinstance(payload, dict) and payload:
            return _normalize_snapshot(payload, source="module", module=True)
        watch = _call(mod, "watch_status")
        if isinstance(watch, dict):
            snap.update(watch)
            snap["present"] = True
            snap["source"] = "module"
            snap["module"] = True
            html_board = _call(mod, "catalog_html") or _call(mod, "catalog_overview_html")
            if isinstance(html_board, str) and html_board.strip():
                snap["catalog_html"] = html_board
            return _normalize_snapshot(snap, source="module", module=True)

    root = golf_kalshi_root()
    file_payload = None
    for rel in (
        Path("latest") / "snapshot.json",
        Path("latest") / "watch.json",
        Path("snapshot.json"),
    ):
        file_payload = _read_json(root / rel)
        if file_payload:
            break
    tickets_payload = _read_json(root / "latest" / "tickets.json") or _read_json(root / "tickets.json")
    ledger = _read_json(root / "paper" / "ledger.json") or _read_json(root / "ledger.json")
    recipe = _read_json(root / "latest" / "recipe.json") or _read_json(root / "recipe.json")
    farm = _read_json(root / "farm" / "status.json")
    honer = _read_json(root / "honer" / "status.json")
    merged: dict[str, Any] = {}
    if file_payload:
        merged.update(file_payload)
    if tickets_payload:
        if isinstance(tickets_payload.get("tickets"), list):
            merged["tickets"] = tickets_payload["tickets"]
        elif isinstance(tickets_payload.get("open_tickets"), list):
            merged["tickets"] = tickets_payload["open_tickets"]
        merged.setdefault("tickets_n", tickets_payload.get("count") or tickets_payload.get("tickets_n"))
    if ledger:
        merged.setdefault("bankroll", ledger.get("bankroll"))
        merged.setdefault("pnl", ledger.get("betting_pnl") if "betting_pnl" in ledger else ledger.get("pnl"))
        merged.setdefault("fees", ledger.get("fees"))
    if recipe:
        merged.setdefault("recipe", recipe.get("recipe") or recipe.get("name"))
        if recipe.get("brain"):
            merged["recipe"] = (
                f"{merged.get('recipe') or 'golf-kalshi-recipe'} · {recipe.get('brain')}"
            ).strip(" ·")
    if farm and farm.get("status"):
        merged["farm_status"] = farm.get("status")
    if honer and honer.get("status"):
        merged["honer_status"] = honer.get("status")
    if merged:
        return _normalize_snapshot(merged, source="files", module=False)
    return snap


def _normalize_snapshot(raw: dict[str, Any], *, source: str, module: bool) -> dict[str, Any]:
    watch = raw.get("watch") if isinstance(raw.get("watch"), dict) else raw
    running = watch.get("running")
    if running is None:
        label = str(watch.get("watch") or watch.get("watch_label") or "").strip().lower()
        if label.startswith("on") or label == "watch on":
            running = True
        elif label.startswith("off"):
            running = False
    last_ok = watch.get("last_ok", True)
    if running and last_ok is False:
        watch_kind = "fail"
        watch_label = "Watch on — last cycle failed"
    elif running:
        watch_kind = "on"
        watch_label = "Watch on"
    else:
        watch_kind = "off"
        watch_label = "Watch off"
    tickets = raw.get("tickets") or raw.get("open_tickets") or []
    if not isinstance(tickets, list):
        tickets = []
    tickets_n = raw.get("tickets_n")
    if tickets_n is None:
        tickets_n = raw.get("paper_tickets")
    if tickets_n is None and tickets:
        tickets_n = len(tickets)
    halt = raw.get("halt")
    if isinstance(halt, str):
        halt_l = halt.strip().lower()
        if halt_l in {"no", "false", "0"}:
            halt = False
        elif halt_l in {"yes", "true", "1"}:
            halt = True
    catalog = raw.get("catalog_counts") if isinstance(raw.get("catalog_counts"), dict) else {}
    if not catalog and any(k in raw for k in ("series", "open_markets", "settled")):
        catalog = {
            "series": raw.get("series"),
            "open_markets": raw.get("open_markets"),
            "settled": raw.get("settled"),
            "in_play_families": raw.get("in_play_families"),
            "booked_series": raw.get("booked_series"),
        }
    sleeves = raw.get("sleeves") if isinstance(raw.get("sleeves"), list) else []
    present = bool(
        module
        or tickets
        or tickets_n is not None
        or raw.get("bankroll") not in (None, "")
        or raw.get("pnl") not in (None, "")
        or catalog
        or raw.get("recipe")
        or running
    )
    return {
        "present": present,
        "source": source,
        "module": module,
        "watch_kind": watch_kind,
        "watch_label": watch_label,
        "watch_at": str(watch.get("watch_at") or watch.get("last_at") or raw.get("watch_at") or ""),
        "watch_summary": str(watch.get("last_summary") or raw.get("last_summary") or ""),
        "tickets_n": tickets_n,
        "pnl": _fmt_money(raw.get("pnl") if "pnl" in raw else raw.get("betting_pnl")),
        "bankroll": _fmt_money(raw.get("bankroll")),
        "fees": _fmt_money(raw.get("fees")),
        "halt": halt,
        "field_hunt": str(raw.get("field_hunt") or "").strip(),
        "sleeves": sleeves,
        "tickets": tickets,
        "catalog_counts": catalog,
        "catalog_html": str(raw.get("catalog_html") or ""),
        "recipe": str(raw.get("recipe") or "").strip(),
        "farm_status": str(raw.get("farm_status") or FARM_IDLE),
        "honer_status": str(raw.get("honer_status") or HONER_IDLE),
    }


def golf_catalog_series_html(ticker: str) -> tuple[str, int]:
    mod = golf_kalshi_module()
    if mod is None:
        return (f"<p class='help'>{_esc(CATALOG_MISSING)}</p>", 503)
    body = _call(mod, "series_html", ticker) or _call(mod, "catalog_series_html", ticker)
    if not isinstance(body, str) or not body.strip():
        return ("<p class='help'>Markets not available.</p>", 404)
    return (body, 200)


def golf_catalog_unmatched_html() -> tuple[str, int]:
    mod = golf_kalshi_module()
    if mod is None:
        return (f"<p class='help'>{_esc(CATALOG_MISSING)}</p>", 503)
    body = _call(mod, "unmatched_html") or _call(mod, "catalog_unmatched_html")
    if not isinstance(body, str) or not body.strip():
        return ("<p class='help'>Unmatched not available.</p>", 404)
    return (body, 200)


def _halt_label(halt: object) -> str:
    if halt is True:
        return "Halt yes"
    if halt is False:
        return "Halt no"
    return "Halt not on file"


def glance_chips_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    watch_kind = data["watch_kind"]
    chips = [
        f'<span class="chip watch-{_esc(watch_kind)}" data-watch="{_esc(watch_kind)}">'
        f"{_esc(data['watch_label'])}</span>",
        f'<span class="chip market" data-kind="gym">{_esc(GYM_LOCK)}</span>',
    ]
    when = data.get("watch_at") or ""
    if when:
        chips.append(f'<span class="chip quiet" data-kind="watch-at">{_esc(when)}</span>')
    n = data.get("tickets_n")
    if n is None:
        chips.append('<span class="chip quiet" data-kind="tickets">paper tickets not on file</span>')
    else:
        chips.append(
            f'<span class="chip" data-kind="tickets">paper tickets {_esc(n)}</span>'
        )
    if data.get("pnl"):
        bank = f" · bankroll ${_esc(data['bankroll'])}" if data.get("bankroll") else ""
        chips.append(
            f'<span class="chip pnl" data-kind="golf-pnl">P/L ${_esc(data["pnl"])}{bank}</span>'
        )
    else:
        chips.append(
            '<span class="chip pnl" data-kind="golf-pnl">P/L not on file — none invented</span>'
        )
    if data.get("fees"):
        chips.append(f'<span class="chip quiet" data-kind="fees">fees {_esc(data["fees"])}</span>')
    chips.append(
        f'<span class="chip" data-kind="halt">{_esc(_halt_label(data.get("halt")))}</span>'
    )
    return "".join(chips)


def glance_strip_html() -> str:
    return f'<div class="glance" id="glance-strip">{glance_chips_html()}</div>'


def session_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    n = data.get("tickets_n")
    if n is None:
        pos = '<span class="sess-pos">open tickets not on this checkout</span>'
        note = f'<span class="sess-note">{_esc(BOOK_MISSING)}</span>'
    elif int(n) == 0:
        pos = '<span class="sess-pos">no open paper tickets</span>'
        note = '<span class="sess-note">copied from the golf Kalshi book · not 15m lineage A</span>'
    else:
        pos = f'<span class="sess-pos">{_esc(n)} open paper tickets · SETTLE_PENDING</span>'
        note = '<span class="sess-note">copied from the golf Kalshi book · not 15m lineage A</span>'
    halt = _halt_label(data.get("halt"))
    return (
        '<span class="sess-k">Gym</span>'
        f'<span class="sess-ticker">{_esc(GYM_LOCK)}</span>'
        f'<span class="sess-clock">{_esc(halt)}</span>'
        f"{pos}{note}"
    )


def session_strip_html() -> str:
    return f'<div class="session" id="session-strip">{session_inner_html()}</div>'


def _now_block(
    label: str,
    primary: str,
    *,
    glance_sub: str = "",
    extra: list[str] | None = None,
) -> str:
    bits = [
        '<div class="now-row"><span class="now-k">' + _esc(label) + "</span> "
        f'<span class="now-v">{_esc(primary)}</span></div>'
    ]
    if glance_sub:
        bits.append(f'<div class="now-sub">{_esc(glance_sub)}</div>')
    if extra:
        bits.append('<div class="now-more cockpit-only">')
        bits.extend(f'<div class="now-sub">{_esc(line)}</div>' for line in extra if line)
        bits.append("</div>")
    return "".join(bits)


def this_lane_now_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    n = data.get("tickets_n")
    if data["watch_kind"] == "fail":
        doing = "Watch on — last cycle failed"
    elif data["present"]:
        ticket_bit = f"{n} paper tickets" if n is not None else "tickets not on file"
        doing = f"Watch {data['watch_kind']} · {ticket_bit}"
    else:
        doing = "Golf (Kalshi) watch not on this checkout"
    doing_extra = []
    if data.get("watch_summary"):
        doing_extra.append(str(data["watch_summary"]))
    if data.get("watch_at"):
        doing_extra.append(f"last stamp {data['watch_at']}")
    if data.get("field_hunt"):
        doing_extra.append(data["field_hunt"])
    if data.get("halt") is True:
        thinking = "Halt is on — no new paper fill"
        thinking_glance = "halted"
    elif n:
        thinking = f"{n} open tickets waiting on golf settles"
        thinking_glance = "SETTLE_PENDING · not 15m"
    elif data["present"]:
        thinking = "no open golf tickets on file"
        thinking_glance = ""
    else:
        thinking = "no golf Kalshi book to think over on this checkout"
        thinking_glance = BOOK_MISSING
    thinking_extra = []
    if data.get("recipe"):
        thinking_extra.append(f"recipe {data['recipe']}")
    thinking_extra.append("brain does not consult 15m decide()")
    thinking_extra.append("golf Kalshi P/L is not lineage A")
    learning = data.get("farm_status") or FARM_IDLE
    learning_glance = "Honer idle · Farm idle"
    learning_extra = [
        data.get("honer_status") or HONER_IDLE,
        "Honer does not consult 15m decide(). No combined bankroll.",
    ]
    jump = (
        '<p class="now-jump">open tickets → '
        '<a href="#scoreboard" data-tab="scoreboard">Scoreboard</a>'
        " · recipe → "
        '<a href="#lab" data-tab="lab">Lab</a>'
        " · organs → "
        '<a href="#farm" data-tab="farm">Farm</a>'
        " / "
        '<a href="#honer" data-tab="honer">Honer</a></p>'
    )
    return (
        _now_block("Doing", doing, glance_sub=data.get("field_hunt") or "", extra=doing_extra)
        + _now_block("Thinking", thinking, glance_sub=thinking_glance, extra=thinking_extra)
        + _now_block("Learning", learning, glance_sub=learning_glance, extra=learning_extra)
        + jump
    )


def this_lane_now_html() -> str:
    return (
        '<div class="lane-now home-only" id="lane-now">'
        f"{this_lane_now_inner_html()}"
        "</div>"
    )


def _tile(name: str, status: str, note: str, *, lane: str) -> str:
    return (
        f'<article class="lane-tile" data-lane="{_esc(lane)}">'
        f'<span class="tile-name">{_esc(name)}</span>'
        f'<span class="tile-status">{_esc(status)}</span>'
        f'<span class="tile-note">{_esc(note)}</span>'
        "</article>"
    )


def golf_organ_tiles_inner_html() -> str:
    """Compact Golf (Kalshi) / Farm / Honer tiles for the 15m glance. Not a cockpit."""
    data = golf_kalshi_snapshot()
    if data["present"]:
        n = data.get("tickets_n")
        tickets = f"{n} paper tickets" if n is not None else "tickets not on file"
        pnl = f"P/L ${data['pnl']}" if data.get("pnl") else "P/L not on file"
        golf_status = f"{data['watch_label']} · {tickets}"
        golf_note = f"{pnl} · {_halt_label(data.get('halt'))} · not lineage A"
    else:
        golf_status = "book not on this checkout"
        golf_note = "live gym is Golf (Kalshi) · previous Phase 1 claim stays in Museum"
    farm_status = "idle"
    farm_note = data.get("farm_status") or FARM_IDLE
    honer_status = "idle"
    honer_note = data.get("honer_status") or HONER_IDLE
    return (
        _tile("Golf (Kalshi)", golf_status, golf_note, lane="golf")
        + _tile("Golf Farm", farm_status, farm_note, lane="golf-farm")
        + _tile("Golf Honer", honer_status, honer_note, lane="golf-honer")
    )


def fifteen_m_tile_inner_html() -> str:
    """One compact 15m tile on the golf home. Not a second 15m cockpit."""
    try:
        from golf_offshoot.operator_surface.lane_15m_home import glance_model

        model = glance_model()
    except Exception:
        return _tile(
            "15-min Kalshi",
            "not on this tree",
            "KXBTC15M · no invented pnl",
            lane=LANE_15M,
        )
    watch = str(model.get("watch_label") or "Watch off")
    ticker = str(model.get("ticker") or "KXBTC15M")
    pnl = model.get("lineage_a_pnl")
    if pnl:
        note = f"{ticker} · lineage A P/L ${pnl} · never summed into golf"
    else:
        note = f"{ticker} · lineage A P/L not on file — none invented"
    return _tile("15-min Kalshi", watch, note, lane=LANE_15M)


def other_lane_tiles_html() -> str:
    inner = fifteen_m_tile_inner_html()
    return f'<div class="lane-tiles home-only" id="lane-tiles">{inner}</div>'


def role_strip_html() -> str:
    from golf_offshoot.operator_surface.lane_15m_home import role_strip_inner_html

    return f'<div class="role-strip home-only" id="role-strip">{role_strip_inner_html()}</div>'


def tabs_nav_html() -> str:
    bits = []
    for tab_id, label in TABS:
        css = ' class="active"' if tab_id == "home" else ""
        bits.append(
            f'<a href="#{_esc(tab_id)}" data-tab="{_esc(tab_id)}"{css}>{_esc(label)}</a>'
        )
    bits.append(
        '<span class="density-toggle home-only" aria-label="density">'
        '<a href="#glance" data-density="glance" class="active">Glance</a>'
        '<a href="#cockpit" data-density="cockpit">Cockpit</a>'
        "</span>"
    )
    return f'<nav class="thin-tabs" aria-label="Golf Kalshi views">{"".join(bits)}</nav>'


def header_golf_html(*, lane_line: str, wall_lines: str, wall_class: str = "ops") -> str:
    css = wall_class if wall_class in {"ops", "mock"} else "ops"
    return (
        f'<header class="{_esc(css)}">'
        f'<p class="kicker">{_esc(HEADER_KICKER)}</p>'
        f"<h1>{_esc(HEADER_TITLE)}</h1>"
        '<div class="market-lock">'
        f'<span class="lock-ticker">{_esc(GYM_LOCK)}</span>'
        f'<span class="lock-note">{_esc(GYM_LOCK_NOTE)}</span>'
        "</div>"
        f'<div class="trust">{_esc(TRUST_LINE)}</div>'
        f'<div class="lane-line">{_esc(lane_line)}</div>'
        f"{wall_lines}"
        "</header>"
    )


def tickets_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    rows = data.get("tickets") or []
    if not rows:
        if data["present"]:
            return "<p class='help'>No open golf Kalshi tickets on file.</p>"
        return f"<p class='help'>{_esc(BOOK_MISSING)}</p>"
    body = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        player = row.get("player") or row.get("name") or ""
        market = row.get("market") or row.get("title") or ""
        sleeve = row.get("sleeve") or ""
        stake = _fmt_money(row.get("stake"))
        quote = row.get("quote")
        quote_txt = _fmt_money(quote) if quote not in (None, "") else ""
        status = row.get("status") or "SETTLE_PENDING"
        body.append(
            "<tr>"
            f"<td>{_esc(player)}</td>"
            f"<td>{_esc(market)}</td>"
            f"<td>{_esc(sleeve)}</td>"
            f"<td>{_esc(stake)}</td>"
            f"<td>{_esc(quote_txt)}</td>"
            f"<td>{_esc(status)}</td>"
            "</tr>"
        )
    if not body:
        return f"<p class='help'>{_esc(BOOK_MISSING)}</p>"
    return (
        '<p class="help">Paper fills from decide_golf. Catalog open markets are Kalshi '
        "contracts, not this table. Not 15m lineage A.</p>"
        '<div class="gk-table-wrap" id="gk-tickets">'
        '<table class="board-table gk-board">'
        "<thead><tr><th>Player</th><th>Market</th><th>Sleeve</th>"
        "<th>Stake</th><th>Quote</th><th>Status</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def sleeves_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    sleeves = data.get("sleeves") or []
    if not sleeves:
        return "<p class='help'>Sleeves not on this checkout.</p>"
    bits = []
    for row in sleeves:
        if not isinstance(row, dict):
            continue
        name = row.get("name") or row.get("sleeve") or ""
        used = row.get("used")
        cap = row.get("cap")
        used_f = None
        cap_f = None
        try:
            used_f = float(used)
            cap_f = float(cap)
        except (TypeError, ValueError):
            used_f = None
        pct = 0
        if used_f is not None and cap_f:
            pct = max(0, min(100, int(round(100 * used_f / cap_f))))
        title = ""
        if used_f is not None and cap_f is not None:
            title = f"{used_f:.2f} / {cap_f:.2f}"
        bits.append(
            f"<div><span>{_esc(name)}</span>"
            f'<div class="gk-bar" title="{_esc(title)}"><span style="width:{pct}%"></span></div>'
            "</div>"
        )
    if not bits:
        return "<p class='help'>Sleeves not on this checkout.</p>"
    return f'<div class="gk-sleeves" id="gk-sleeves">{"".join(bits)}</div>'


def catalog_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    html_board = str(data.get("catalog_html") or "").strip()
    counts = data.get("catalog_counts") or {}
    chips = []
    labels = (
        ("series", "Series"),
        ("open_markets", "Open markets"),
        ("settled", "Settled"),
        ("in_play_families", "In-play families"),
        ("booked_series", "Booked series"),
    )
    for key, label in labels:
        val = counts.get(key)
        if val in (None, ""):
            continue
        chips.append(f'<span class="chip"><b>{_esc(label)}</b> {_esc(val)}</span>')
    chip_row = f'<div class="gk-chips">{"".join(chips)}</div>' if chips else ""
    if html_board:
        return (
            f"{chip_row}"
            '<p class="help">Tour family → series counts. Market rows load when you open a '
            "series. Open markets are the catalog, not paper tickets.</p>"
            f'<div class="gk-catalog" id="gk-catalog">{html_board}</div>'
        )
    return (
        f"{chip_row}"
        f"<p class='help'>{_esc(CATALOG_MISSING)}</p>"
        '<details class="gk-unmatched" data-loaded="0">'
        "<summary>Unmatched · load when the module is present</summary>"
        '<div class="gk-unmatched-body"></div></details>'
    )


def farm_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    return (
        f'<p class="help">{_esc(FARM_HELP)}</p>'
        f'<p class="loud" id="golf-farm-status">{_esc(data.get("farm_status") or FARM_IDLE)}</p>'
    )


def honer_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    return (
        f'<p class="help">{_esc(HONER_HELP)}</p>'
        f'<p class="loud" id="golf-honer-status">{_esc(data.get("honer_status") or HONER_IDLE)}</p>'
    )


def lab_inner_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    recipe = data.get("recipe") or "recipe stamp not on this checkout"
    return (
        '<p class="view-lead">Lab for this gym is the golf Kalshi recipe. '
        "Not the 15m PROPOSED. Not an ADMIT.</p>"
        f'<p class="gk-nums">{_esc(recipe)}</p>'
        "<p class='help'>brain keep_expert stays keep_expert until a new dated claim. "
        "Nothing here retunes Phase 1 θ.</p>"
    )


def _is_15m_run(rec: RunRecord | None) -> bool:
    if rec is None:
        return False
    extras = rec.extras if isinstance(rec.extras, dict) else {}
    if extras.get("lane") == LANE_15M:
        return True
    if rec.command == "watch":
        return True
    blob = " ".join(
        str(bit)
        for bit in (rec.paper, rec.table, rec.summary, rec.event_id, rec.error)
        if bit
    )
    return "KXBTC15M" in blob or "learning_lane_15m" in blob or "journal=15m" in blob


def ops_watch_inner_html(*, last_run: RunRecord | None = None) -> str:
    data = golf_kalshi_snapshot()
    rows = [
        ("Watch", data["watch_label"]),
        ("Tickets", "not on file" if data.get("tickets_n") is None else str(data["tickets_n"])),
        ("Halt", _halt_label(data.get("halt"))),
        ("Book", "on this tree" if data["present"] else "not on this checkout"),
    ]
    dl = "".join(f"<div><dt>{_esc(k)}</dt><dd>{_esc(v)}</dd></div>" for k, v in rows)
    return f"<dl class='ops-grid'>{dl}</dl>"


def ops_html(*, last_run: RunRecord | None = None, checkout_is_phase1: bool = True) -> str:
    buttons = []
    help_rows = []
    for value, label, blurb in ACTION_BUTTONS_GOLF:
        css = ' class="soft"' if value == "refresh" else ""
        buttons.append(f'<button{css} name="action" value="{value}">{_esc(label)}</button>')
        help_rows.append(f"<li><b>{_esc(label)}</b> — {_esc(blurb)}</li>")
    if _is_15m_run(last_run):
        last_html = (
            "<p class='help'>Last shell cycle was the 15m PaperWatch. "
            "It is not shown here — golf extras never dump the 15m ledger.</p>"
        )
    elif last_run is not None:
        paper = last_run.paper or ""
        if "KXBTC15M" in paper or "journal=15m" in paper:
            paper = ""
        rec_html = _esc(format_run_record(last_run))
        last_html = f"<pre>{rec_html}</pre>"
        if paper:
            last_html += f"<pre>{_esc(paper)}</pre>"
    else:
        last_html = (
            "<p class='help'>No golf Kalshi extra cycle in this shell session. "
            "Buttons below are extras, not the loop.</p>"
        )
    honesty = ""
    if checkout_is_phase1 and not golf_kalshi_snapshot().get("module"):
        honesty = (
            "<p class='help'>This checkout's POST still runs the Phase 1 observation pipeline "
            "until the Golf (Kalshi) runner is on the tree. The live Windows gym maps these "
            "buttons to golf Kalshi ticks. Museum holds the previous Phase 1 claim.</p>"
        )
    return (
        f'<div id="tab-ops-watch">{ops_watch_inner_html(last_run=last_run)}</div>'
        "<p class='view-lead'>This view is Ops. Trading is not armed. No ESPN pin. "
        "These buttons are extras. PaperWatch on 15m keeps running. "
        "Paper bankroll auto-apply is paper observation only — it is not trading armed.</p>"
        f"{honesty}"
        '<form class="row" method="post" action="/run">'
        f'<input type="hidden" name="{SELECTOR_FIELD}" value="{LANE_GOLF}"/>'
        f"{''.join(buttons)}"
        "</form>"
        f'<ul class="help">{"".join(help_rows)}</ul>'
        "<h3>Last extra cycle</h3>"
        f"{last_html}"
        '<form class="row lane-form" method="get" action="/">'
        "<fieldset><legend>Other chrome</legend>"
        "<p class='help'>Opening 15-min Kalshi does <strong>not</strong> stop this gym's "
        "files, and does not stop PaperWatch.</p>"
        f'<button type="submit" name="{SELECTOR_FIELD}" value="{LANE_GOLF}" class="active">'
        "Stay on Golf (Kalshi)</button>"
        f'<button type="submit" name="{SELECTOR_FIELD}" value="{LANE_15M}">'
        "15-min Kalshi (learning)</button>"
        "</fieldset></form>"
    )


def cockpit_rail_html(snap: dict[str, Any] | None = None) -> str:
    data = snap if snap is not None else golf_kalshi_snapshot()
    think = "<p>no golf Kalshi book on this checkout</p>"
    if data["present"]:
        n = data.get("tickets_n")
        think = (
            f"<p>{_esc(n) if n is not None else 'tickets not on file'} open · "
            f"{_esc(_halt_label(data.get('halt')))}</p>"
        )
        if data.get("recipe"):
            think += f"<p class='help'>{_esc(data['recipe'])}</p>"
    learn = f"<p>{_esc(data.get('farm_status') or FARM_IDLE)}</p>"
    learn += f"<p class='help'>{_esc(data.get('honer_status') or HONER_IDLE)}</p>"
    tape = tickets_inner_html(data) if data.get("tickets") else "<p>Open tickets live on Scoreboard.</p>"
    return (
        '<div class="cockpit-rail cockpit-only" id="cockpit-rail">'
        "<article>"
        '<h3><a href="#lab" data-tab="lab">How it\'s thinking</a></h3>'
        f"{think}"
        "</article>"
        "<article>"
        '<h3><a href="#farm" data-tab="farm">How it\'s learning</a></h3>'
        f"{learn}"
        "</article>"
        '<article class="tape-card">'
        '<h3><a href="#scoreboard" data-tab="scoreboard">Open tickets</a></h3>'
        f"{tape}"
        "</article>"
        "</div>"
    )


def museum_html(*, viz_wall: str, honesty_blocks: str, settle_banner: str) -> str:
    return (
        '<div id="tab-museum" class="tab-panel" data-tab-panel="museum">'
        '<section class="panel" id="museum">'
        "<h2>Previous golf claim</h2>"
        f'<p class="help">{_esc(MUSEUM_HELP)}</p>'
        f"{settle_banner}"
        f"{viz_wall}"
        f'<div id="museum-ranked">{honesty_blocks}</div>'
        "</section></div>"
    )


def main_golf_html(
    *,
    last_run: RunRecord | None = None,
    viz_wall: str = "",
    honesty_blocks: str = "",
    settle_banner: str = "",
) -> str:
    snap = golf_kalshi_snapshot()
    field = ""
    hunt = data_field_hunt(snap)
    if hunt:
        field = f'<p class="gk-nums" id="gk-field-hunt">{_esc(hunt)}</p>'
    return (
        '<div id="tab-home" class="tab-panel active" data-tab-panel="home">'
        f"{cockpit_rail_html(snap)}"
        '<section class="panel" id="golf-kalshi">'
        "<h2>Golf (Kalshi)</h2>"
        f"{field}"
        '<div class="cockpit-only">'
        "<h3>Sleeves</h3>"
        f'<div id="gk-sleeves-slot">{sleeves_inner_html(snap)}</div>'
        "</div>"
        '<div class="cockpit-only">'
        "<h3>Open tickets</h3>"
        f'<div id="gk-tickets-home">{tickets_inner_html(snap)}</div>'
        "</div>"
        "</section>"
        "</div>"
        '<div id="tab-scoreboard" class="tab-panel" data-tab-panel="scoreboard">'
        '<section class="panel"><h2>Scoreboard</h2>'
        '<p class="view-lead">Open golf Kalshi tickets and the catalog. '
        "Catalog is not the glance. Not 15m lineage A.</p>"
        f'<div id="tab-scoreboard-body">{tickets_inner_html(snap)}{sleeves_inner_html(snap)}</div>'
        "<h3>Catalog</h3>"
        f"{catalog_inner_html(snap)}"
        "</section></div>"
        '<div id="tab-lab" class="tab-panel" data-tab-panel="lab">'
        '<section class="panel"><h2>Lab</h2>'
        f'<div id="tab-lab-body">{lab_inner_html(snap)}</div>'
        "</section></div>"
        '<div id="tab-ops" class="tab-panel" data-tab-panel="ops">'
        '<section class="panel"><h2>Ops</h2>'
        f"{ops_html(last_run=last_run)}"
        "</section></div>"
        '<div id="tab-farm" class="tab-panel" data-tab-panel="farm">'
        '<section class="panel gk-organ" id="golf-farm"><h2>Golf Farm</h2>'
        f'<div id="golf-farm-body">{farm_inner_html(snap)}</div>'
        "</section></div>"
        '<div id="tab-honer" class="tab-panel" data-tab-panel="honer">'
        '<section class="panel gk-organ" id="golf-honer"><h2>Golf Honer</h2>'
        f'<div id="golf-honer-body">{honer_inner_html(snap)}</div>'
        "</section></div>"
        f"{museum_html(viz_wall=viz_wall, honesty_blocks=honesty_blocks, settle_banner=settle_banner)}"
    )


def data_field_hunt(snap: dict[str, Any]) -> str:
    return str(snap.get("field_hunt") or "")


def live_payload(state: dict | None = None, *, last_run: RunRecord | None = None) -> dict[str, Any]:
    rec = last_run
    if rec is None and state and isinstance(state.get("surface"), dict):
        rec = state["surface"].get("last_run")
    snap = golf_kalshi_snapshot()
    from golf_offshoot.operator_surface.lane_15m_home import role_strip_inner_html

    return {
        "glance_html": glance_chips_html(snap),
        "session_html": session_inner_html(snap),
        "now_html": this_lane_now_inner_html(snap),
        "tiles_html": fifteen_m_tile_inner_html(),
        "roles_html": role_strip_inner_html(state),
        "tickets_html": tickets_inner_html(snap),
        "sleeves_html": sleeves_inner_html(snap),
        "farm_html": farm_inner_html(snap),
        "honer_html": honer_inner_html(snap),
        "lab_html": lab_inner_html(snap),
        "ops_watch_html": ops_watch_inner_html(last_run=rec),
        "scoreboard_html": tickets_inner_html(snap) + sleeves_inner_html(snap),
        "cockpit_html": cockpit_rail_html(snap),
        "watch_kind": snap["watch_kind"],
        "trading_armed": False,
        "lane": LANE_GOLF,
        "series": DATA_MARKET,
        "market": DATA_MARKET,
    }


LANE_GOLF_CSS = """
 body.lane-golf main { max-width: 1400px; }
 body.lane-golf header.ops .kicker { margin: 0; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.8; }
 body.lane-golf header.ops .market-lock { margin-top: 8px; }
 body.lane-golf header.ops .lock-ticker { font-size: 20px; font-weight: 700; letter-spacing: 1px; }
 body.lane-golf header.ops .lock-note { margin-left: 8px; font-size: 12px; opacity: 0.85; }
 body.lane-golf header.ops .trust { margin-top: 6px; font-size: 12px; font-weight: 400; opacity: 0.75; }
 body.lane-golf:not([data-view="home"]) .home-only { display: none; }
 .lane-switch { background: #f4f1ea; padding: 8px 20px 4px; border-bottom: 1px solid #c9c2b2; }
 .lane-switch form.lane-form { margin: 0; }
 .gk-nums { font-size: 13px; color: #4a4a4a; }
 .gk-sleeves { display: grid; gap: 8px; margin: 8px 0 16px; }
 .gk-sleeves span { display: inline-block; width: 90px; }
 .gk-bar { display: inline-block; width: 180px; height: 8px; background: #e6e0d4; vertical-align: middle; }
 .gk-bar span { display: block; height: 100%; background: #1f3b4d; }
 .gk-table-wrap { overflow-x: auto; }
 table.gk-board { border-collapse: collapse; width: 100%; font-size: 13px; }
 table.gk-board th { text-align: left; background: #1f3b4d; color: #fff; padding: 6px 8px; }
 table.gk-board td { border-bottom: 1px solid #c9c2b2; padding: 6px 8px; }
 .gk-catalog { display: grid; gap: 8px; margin: 8px 0 16px; }
 details.gk-family, details.gk-series, details.gk-settled, details.gk-unmatched { border: 1px solid #c9c2b2; padding: 8px 10px; background: #fff; }
 details.gk-series, details.gk-settled { margin: 8px 0 0; }
 details.gk-unmatched { margin: 8px 0 16px; }
 details.gk-family > summary, details.gk-series > summary, details.gk-unmatched > summary { cursor: pointer; font-weight: 700; color: #1f3b4d; }
 .gk-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 14px; }
 .gk-chips .chip, .gk-chip { display: inline-block; background: #fff; border: 1px solid #c9c2b2; padding: 6px 10px; font-size: 13px; }
 body.density-cockpit .gk-sleeves, body.density-cockpit #gk-tickets-home { display: block; }
"""


LANE_GOLF_JS = """
(function(){
  var nav = document.querySelector('.thin-tabs');
  if (!nav) return;
  var allowed = {home:1, scoreboard:1, lab:1, ops:1, farm:1, honer:1, museum:1};
  function foldExceptions(open){
    var fold = document.getElementById('exceptions-fold');
    if (fold) fold.open = !!open;
  }
  function show(id){
    if (!allowed[id]) id = 'home';
    document.querySelectorAll('.tab-panel').forEach(function(p){
      p.classList.toggle('active', p.getAttribute('data-tab-panel') === id);
    });
    nav.querySelectorAll('[data-tab]').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('data-tab') === id);
    });
    try { localStorage.setItem('gpf-golf-tab', id); } catch (e) {}
    document.body.setAttribute('data-view', id);
  }
  function setDensity(mode){
    var cockpit = mode === 'cockpit';
    document.body.classList.toggle('density-cockpit', cockpit);
    document.body.classList.toggle('density-glance', !cockpit);
    try { localStorage.setItem('gpf-golf-density', cockpit ? 'cockpit' : 'glance'); } catch (e) {}
    document.querySelectorAll('[data-density]').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('data-density') === (cockpit ? 'cockpit' : 'glance'));
    });
    foldExceptions(cockpit);
  }
  document.addEventListener('click', function(ev){
    var dens = ev.target.closest ? ev.target.closest('[data-density]') : null;
    if (dens) {
      ev.preventDefault();
      setDensity(dens.getAttribute('data-density') || 'glance');
      return;
    }
    var a = ev.target.closest ? ev.target.closest('[data-tab]') : null;
    if (!a) return;
    ev.preventDefault();
    var id = a.getAttribute('data-tab') || 'home';
    show(id);
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  });
  document.addEventListener('keydown', function(ev){
    if (ev.altKey || ev.metaKey || ev.ctrlKey) return;
    var t = ev.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    var keys = {'1':'home','2':'scoreboard','3':'lab','4':'ops','5':'farm','6':'honer','7':'museum'};
    if (!keys[ev.key]) return;
    ev.preventDefault();
    show(keys[ev.key]);
    if (history.replaceState) history.replaceState(null, '', '#' + keys[ev.key]);
  });
  var hash = (location.hash || '').replace('#','');
  if (hash === 'golf-kalshi') hash = 'home';
  if (hash === 'golf-farm') hash = 'farm';
  if (hash === 'golf-honer') hash = 'honer';
  if (hash === 'cockpit') { setDensity('cockpit'); show('home'); }
  else if (hash === 'glance') { setDensity('glance'); show('home'); }
  else if (allowed[hash]) { show(hash); }
  else {
    var savedTab = '';
    try { savedTab = localStorage.getItem('gpf-golf-tab') || ''; } catch (e) {}
    show(allowed[savedTab] ? savedTab : 'home');
  }
  try {
    var saved = localStorage.getItem('gpf-golf-density');
    if (hash !== 'cockpit' && hash !== 'glance' && saved) setDensity(saved);
    else if (hash !== 'cockpit' && hash !== 'glance') setDensity('glance');
  } catch (e) {}
})();
(function(){
  document.addEventListener('toggle', function(ev){
    var el = ev.target;
    if (!el || !el.classList || !el.open) return;
    if (el.getAttribute('data-loaded') === '1') return;
    if (el.classList.contains('gk-series')) {
      var st = el.getAttribute('data-series');
      var slot = el.querySelector('.gk-series-body');
      if (!st || !slot) return;
      slot.textContent = 'Loading markets…';
      fetch('/golf-catalog/series?ticker=' + encodeURIComponent(st), {cache:'no-store'}).then(function(r){
        if (!r.ok) throw new Error('series');
        return r.text();
      }).then(function(html){
        slot.innerHTML = html;
        el.setAttribute('data-loaded', '1');
      }).catch(function(){
        slot.textContent = 'Markets not available.';
      });
      return;
    }
    if (el.classList.contains('gk-unmatched')) {
      var body = el.querySelector('.gk-unmatched-body');
      if (!body) return;
      body.textContent = 'Loading unmatched…';
      fetch('/golf-catalog/unmatched', {cache:'no-store'}).then(function(r){
        if (!r.ok) throw new Error('unmatched');
        return r.text();
      }).then(function(html){
        body.innerHTML = html;
        el.setAttribute('data-loaded', '1');
      }).catch(function(){
        body.textContent = 'Unmatched not available.';
      });
    }
  }, true);
})();
"""
