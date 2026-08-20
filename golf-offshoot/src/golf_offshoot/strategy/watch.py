"""Phone ping when the paper trigger actually changes. Never writes packs. Never auto-bets."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from golf_offshoot.compare.apply import advice_signature
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.data_feeds.names import normalize_name
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    _position_is_fill,
    advice_from_recommendation,
)
from golf_offshoot.strategy.paper_trigger import (
    group_trigger_actions,
    sanitize_pre_tee_advice,
    trigger_headline,
)

PULL_KINDS = frozenset({"exit", "reduce", "reallocate", "add", "new_bet", "lock"})
_DEFAULT_NTFY = "https://ntfy.sh"


class WatchConfigError(ValueError):
    """Bad ntfy settings. Nothing was posted."""


@dataclass(frozen=True)
class WatchDecision:
    headline: str
    body: str
    signature: str
    should_ping: bool
    kind: str
    priority: str
    pulls: tuple = ()


def ntfy_topic(raw: str | None = None) -> str:
    topic = (raw or os.environ.get("NTFY_TOPIC") or "").strip()
    if not topic:
        raise WatchConfigError(
            "ntfy topic missing. Subscribe in the ntfy app, then set NTFY_TOPIC in golf-offshoot/.env"
        )
    if any(ch for ch in topic if not (ch.isalnum() or ch in "-_")):
        raise WatchConfigError("NTFY_TOPIC may only use letters, numbers, hyphen, underscore")
    if len(topic) < 4:
        raise WatchConfigError("NTFY_TOPIC is too short")
    return topic


def ntfy_server(raw: str | None = None) -> str:
    base = (raw or os.environ.get("NTFY_URL") or _DEFAULT_NTFY).strip().rstrip("/")
    if not base.startswith("https://") and not base.startswith("http://"):
        raise WatchConfigError("NTFY_URL must be http(s)")
    return base


def watch_state_path(event_id: str, path_id: str = "polymarket") -> Path:
    safe_event = "".join(ch if ch.isalnum() else "-" for ch in str(event_id or "event"))
    safe_path = "".join(ch if ch.isalnum() else "-" for ch in str(path_id or "lived"))
    return package_data_dir() / "paper" / f"watch_{safe_event}_{safe_path}.json"


def load_watch_state(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return raw if isinstance(raw, dict) else {}


def save_watch_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(path)


def serialize_pulls(moves: list[PaperMovement]) -> list[dict]:
    out: list[dict] = []
    for mv in moves or []:
        out.append(
            {
                "kind": mv.kind,
                "player_id": mv.player_id,
                "player_name": mv.player_name,
                "bet_type": mv.bet_type,
                "intent": mv.intent or "hold",
                "model_win": mv.model_win,
                "edge_w": mv.edge_w,
                "posted_edge": mv.posted_edge,
                "decimal_odds": mv.decimal_odds,
            }
        )
    return out


def last_pulls_from_state(state: dict | None) -> list[dict]:
    raw = (state or {}).get("last_pulls")
    return list(raw) if isinstance(raw, list) else []


def _bet_key(raw) -> str:
    val = getattr(raw, "value", raw)
    return str(val or "win").replace("-", "_").lower()


def _filled_tickets(positions) -> tuple[dict, dict]:
    by_name: dict[tuple[str, str], object] = {}
    by_id: dict[tuple[str, str], object] = {}
    for pos in positions or []:
        if not _position_is_fill(pos):
            continue
        bet = _bet_key(getattr(pos, "bet_type", "win"))
        name = normalize_name(getattr(pos, "player_name", "") or "")
        pid = str(getattr(pos, "player_id", "") or "")
        if name:
            by_name[(name, bet)] = pos
        if pid:
            by_id[(pid, bet)] = pos
    return by_name, by_id


def _filled_position(mv: PaperMovement, by_name: dict, by_id: dict):
    bet = _bet_key(mv.bet_type)
    name = normalize_name(mv.player_name or "")
    if name:
        hit = by_name.get((name, bet))
        if hit is not None:
            return hit
    pid = str(mv.player_id or "")
    if pid:
        return by_id.get((pid, bet))
    return None


def _add_is_filled_ticket_reprint(mv: PaperMovement, pos) -> bool:
    """True when ADD reprints the open fill dollars, not a later 20% bump."""
    try:
        delta = abs(float(mv.stake_delta or 0.0))
    except (TypeError, ValueError):
        return False
    try:
        stake = float(getattr(pos, "stake", 0.0) or 0.0)
        cost = getattr(pos, "cost_usd", None)
        cost_f = float(cost) if cost is not None else stake
    except (TypeError, ValueError):
        return False
    open_usd = min((x for x in (stake, cost_f) if x > 0), default=0.0)
    if delta <= 0.005:
        return True
    if open_usd <= 0:
        return False
    return delta + 0.005 >= 0.9 * open_usd


def suppress_executed_pulls(moves: list[PaperMovement], positions) -> list[PaperMovement]:
    """Drop ADD/NEW already covered by a user-typed fill on that name+market.

    Watch pings the whole current pull set when any row appears. An already-filled
    R1 ADD at the original ticket dollars hitchhiking next to a later NEW is the
    old ticket, not a second buy. A live_improved bump (~20/40% of stake) still
    pings.
    """
    by_name, by_id = _filled_tickets(positions)
    if not by_name and not by_id:
        return list(moves or [])
    out: list[PaperMovement] = []
    for mv in moves or []:
        kind = (mv.kind or "").lower()
        pos = _filled_position(mv, by_name, by_id)
        if pos is None:
            out.append(mv)
            continue
        if kind in {"new_bet", "lock"}:
            continue
        if kind == "add" and _add_is_filled_ticket_reprint(mv, pos):
            continue
        out.append(mv)
    return out


def pull_moves(
    advice: list[PaperMovement],
    rows: list | None,
    positions=None,
) -> list[PaperMovement]:
    cleaned = sanitize_pre_tee_advice(list(advice or []), rows)
    pulls = [m for m in cleaned if (m.kind or "").lower() in PULL_KINDS]
    return suppress_executed_pulls(pulls, positions)


def _priority_for(moves: list[PaperMovement]) -> str:
    blob = " ".join(f"{m.kind} {m.reason_plain} {m.reason_technical}" for m in moves).lower()
    if "take the pop" in blob or "flip failed" in blob:
        return "high"
    if any((m.kind or "").lower() == "exit" for m in moves):
        return "high"
    return "default"


def format_watch_body(moves: list[PaperMovement], *, event: str, extra: str = "") -> tuple[str, str]:
    sections = group_trigger_actions(moves)
    headline = trigger_headline(sections)
    lines = [headline, event]
    if extra:
        lines.append(extra)
    for section in sections:
        if section.label == "HOLD":
            continue
        lines.append(section.label)
        for row in section.rows:
            extra_row = f"  {row.extra}" if row.extra else ""
            amt = f"  {row.amount}" if row.amount else ""
            lines.append(f"  {row.name}  {row.market}{amt}{extra_row}")
    lines.append("Mock paper. Never auto-bet. Do not apply from this ping.")
    return headline, "\n".join(lines)


def decide_watch(
    advice: list[PaperMovement],
    rows: list | None,
    *,
    event: str,
    prev_signature: str = "",
    armed: bool = False,
    arm_ping: bool = True,
    positions=None,
) -> WatchDecision:
    pulls = pull_moves(advice, rows, positions=positions)
    sig = advice_signature(pulls)
    if pulls:
        headline, body = format_watch_body(pulls, event=event)
        return WatchDecision(
            headline=headline,
            body=body,
            signature=sig,
            should_ping=sig != (prev_signature or ""),
            kind="pull",
            priority=_priority_for(pulls),
            pulls=tuple(pulls),
        )
    headline = "NOTHING TO PULL — all HOLD"
    if arm_ping and not armed:
        return WatchDecision(
            headline=headline,
            body=(
                f"{headline}\n{event}\n"
                "Watch armed. Later pings are TAKE THE POP / FLIP FAILED / SELL / NEW / REALLOCATE only.\n"
                "Mock paper. Never auto-bet."
            ),
            signature=sig,
            should_ping=True,
            kind="armed",
            priority="min",
            pulls=(),
        )
    return WatchDecision(
        headline=headline,
        body=f"{headline}\n{event}",
        signature=sig,
        should_ping=False,
        kind="hold",
        priority="min",
        pulls=(),
    )


def _header_text(raw: str) -> str:
    """HTTP headers are latin-1. Trigger copy uses an em dash."""
    return (
        (raw or "")
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .encode("ascii", "replace")
        .decode("ascii")
    )


def publish_ntfy(
    body: str,
    *,
    topic: str | None = None,
    title: str = "",
    priority: str = "default",
    dry_run: bool = False,
    timeout: float = 10.0,
) -> str:
    name = ntfy_topic(topic)
    server = ntfy_server()
    url = f"{server}/{name}"
    if dry_run:
        return url
    data = body.encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "text/plain; charset=utf-8")
    if title:
        req.add_header("Title", _header_text(title)[:120])
    req.add_header("Priority", priority)
    req.add_header("Tags", "golf,warning")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
    except urllib.error.URLError as exc:
        raise WatchConfigError(f"ntfy post failed: {exc}") from exc
    return url


def advice_for_watch(record: PaperBookFile | None, result) -> list[PaperMovement]:
    if record is None or result is None or result.strategy is None:
        return []
    return advice_from_recommendation(record, result.strategy, run_id=result.run_id or "")


def ensure_ntfy_topic_in_env() -> str:
    """Keep an existing topic. If none, write one into .env so the phone can subscribe."""
    current = (os.environ.get("NTFY_TOPIC") or "").strip()
    if current:
        return ntfy_topic(current)
    from golf_offshoot.data_feeds.local_env import local_env_path
    import secrets

    topic = "golf-bmw-" + secrets.token_hex(4)
    path = local_env_path()
    block = (
        "\n# ntfy phone alerts for `watch`. Subscribe in the ntfy app to this topic.\n"
        f"NTFY_TOPIC={topic}\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(block)
    os.environ["NTFY_TOPIC"] = topic
    return topic
