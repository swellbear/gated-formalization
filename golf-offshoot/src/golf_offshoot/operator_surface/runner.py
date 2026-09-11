"""Thin wrappers around existing ingest / live / shadow. Observation only."""

from __future__ import annotations

from dataclasses import dataclass, field
from io import StringIO
from typing import Any

from golf_offshoot.models.enums import RunMode
from golf_offshoot.operating import format_inventory, run_operating
from golf_offshoot.operator_surface.notify import CompletionNotice, notify_run_complete
from golf_offshoot.operator_surface.paper import PaperApplyResult, apply_observation_paper
from golf_offshoot.ranking.display import format_table
from golf_offshoot.ranking.leftover import format_leftover_callout

FORBIDDEN_ACTIONS = frozenset(
    {
        "deposit",
        "withdraw",
        "transfer",
        "lock-paper",
        "apply-paper",
        "cash-out",
        "paper-deposit",
        "paper-withdraw",
        "arm",
        "place",
        "cancel",
        "auto-bet",
        "kalshi-auth",
    }
)
ALLOWED_ACTIONS = frozenset({"ingest", "live", "shadow", "loop"})


class OperatorSafetyError(ValueError):
    """Phase 1 shell refused a cash/trade/arm action."""


@dataclass
class RunRecord:
    command: str
    ok: bool
    event_id: str = ""
    run_id: str = ""
    summary: str = ""
    leftover: str = ""
    inventory: str = ""
    paper: str = ""
    table: str = ""
    export_html: str = ""
    export_txt: str = ""
    export_pdf: str = ""
    notice: CompletionNotice | None = None
    error: str = ""
    extras: dict[str, Any] = field(default_factory=dict)


def refuse_forbidden(action: str) -> None:
    key = (action or "").strip().lower()
    if key in FORBIDDEN_ACTIONS:
        raise OperatorSafetyError(
            f"refused {key}: Phase 1 observation only. Trading NOT ARMED. "
            "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH."
        )
    if key not in ALLOWED_ACTIONS:
        raise OperatorSafetyError(f"unknown operator action {action!r}")


def run_ingest(
    *,
    event_id: str | None = None,
    sims: int = 1500,
    refresh: bool = False,
    odds_book: str = "auto",
    notify: bool = True,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
) -> RunRecord:
    refuse_forbidden("ingest")
    try:
        result = run_operating(
            event_id=event_id or None,
            mode=RunMode.PRE_TOURNAMENT,
            sims=sims,
            enable_strategy=False,
            persist=True,
            refresh=refresh,
            odds_book=odds_book,
        )
    except Exception as exc:
        rec = RunRecord(command="ingest", ok=False, event_id=event_id or "", error=str(exc))
        rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return rec
    return _from_result(
        "ingest",
        result,
        notify=notify,
        topic=notify_topic,
        dry_run=dry_run_notify,
        event_hint=event_id,
    )


def run_live(
    *,
    event_id: str | None = None,
    sims: int = 1500,
    refresh: bool = False,
    odds_book: str = "auto",
    notify: bool = True,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
) -> RunRecord:
    """Operating live. Auto-applies paper-observation advises. Trading stays NOT ARMED."""
    refuse_forbidden("live")
    try:
        result = run_operating(
            event_id=event_id or None,
            mode=RunMode.LIVE,
            sims=sims,
            enable_strategy=True,
            persist=True,
            refresh=refresh,
            odds_book=odds_book,
        )
    except Exception as exc:
        rec = RunRecord(command="live", ok=False, event_id=event_id or "", error=str(exc))
        rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return rec
    return _from_result(
        "live",
        result,
        notify=notify,
        topic=notify_topic,
        dry_run=dry_run_notify,
        event_hint=event_id,
    )


def run_shadow(*, notify: bool = False, notify_topic: str | None = None, dry_run_notify: bool = False) -> RunRecord:
    refuse_forbidden("shadow")
    from golf_offshoot.operator_surface.artifacts import load_honesty

    honesty = load_honesty()
    rec = RunRecord(
        command="shadow",
        ok=honesty.shadow.status != "SHADOW_BARRED_MOCK",
        summary=f"shadow {honesty.shadow.status} source={honesty.shadow.source}",
        table=honesty.shadow.text,
    )
    if notify:
        rec.notice = _maybe_notify(rec, notify=True, topic=notify_topic, dry_run=dry_run_notify)
    return rec


def run_loop(
    *,
    event_id: str | None = None,
    sims: int = 1500,
    refresh: bool = False,
    odds_book: str = "auto",
    notify: bool = True,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
) -> RunRecord:
    """ingest → live → shadow. Live auto-applies paper observation. One completion notify."""
    refuse_forbidden("loop")
    parts: list[str] = []
    ingest = run_ingest(
        event_id=event_id,
        sims=sims,
        refresh=refresh,
        odds_book=odds_book,
        notify=False,
    )
    parts.append(f"ingest={'ok' if ingest.ok else 'failed'}")
    if not ingest.ok:
        ingest.command = "loop"
        ingest.summary = " ".join(parts)
        ingest.notice = _maybe_notify(ingest, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return ingest
    live = run_live(
        event_id=ingest.event_id or event_id,
        sims=sims,
        refresh=refresh,
        odds_book=odds_book,
        notify=False,
    )
    parts.append(f"live={'ok' if live.ok else 'failed'}")
    shadow = run_shadow(notify=False)
    parts.append("shadow=viewed")
    live.command = "loop"
    live.summary = " ".join(parts)
    live.table = "\n\n".join(x for x in (ingest.table, live.table, shadow.table) if x)
    live.notice = _maybe_notify(live, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
    return live


def _from_result(
    command: str,
    result,
    *,
    notify: bool,
    topic: str | None,
    dry_run: bool,
    event_hint: str | None,
) -> RunRecord:
    tid = result.tournament.espn_event_id or result.tournament.tournament_id or event_hint or ""
    inv_raw = result.audit.extra.get("source_inventory") or []
    inventory = ""
    if inv_raw:
        from golf_offshoot.models.schemas import SourceInventoryItem

        items = [SourceInventoryItem.model_validate(x) for x in inv_raw]
        inventory = format_inventory(items)
    paper_note: PaperApplyResult | None = None
    open_book = None
    if command in {"live", "loop"}:
        paper_note = apply_observation_paper(result, event_hint=tid)
        if paper_note.record is not None:
            open_book = paper_note.record.book
    leftover = format_leftover_callout(result, open_book)
    table = format_table(result.ranked, n=len(result.ranked))
    extras = {"never_auto_bet": result.never_auto_bet, "mode": result.mode.value}
    if paper_note is not None:
        extras["paper_status"] = paper_note.status
        extras["paper_applied"] = paper_note.applied
        extras["paper_locked"] = paper_note.locked
    rec = RunRecord(
        command=command,
        ok=True,
        event_id=str(tid),
        run_id=result.run_id,
        summary=(
            f"{command} {result.tournament.name} id={tid} n={len(result.ranked)} "
            f"run={result.run_id} mode={result.mode.value}"
            + (f" paper={paper_note.status}" if paper_note else "")
        ),
        leftover=leftover,
        inventory=inventory,
        paper=paper_note.text if paper_note else "",
        table=table,
        export_html=str(result.audit.extra.get("export_html") or ""),
        export_txt=str(result.audit.extra.get("export_txt") or ""),
        export_pdf=str(result.audit.extra.get("export_pdf") or ""),
        extras=extras,
    )
    rec.notice = _maybe_notify(rec, notify=notify, topic=topic, dry_run=dry_run)
    return rec


def _maybe_notify(
    rec: RunRecord,
    *,
    notify: bool,
    topic: str | None,
    dry_run: bool,
) -> CompletionNotice | None:
    if not notify:
        return None
    return notify_run_complete(
        command=rec.command,
        ok=rec.ok,
        event_id=rec.event_id,
        detail=rec.error or rec.summary,
        topic=topic,
        dry_run=dry_run,
        lane=str((rec.extras or {}).get("lane") or ""),
    )


def run_15m_ingest(
    *,
    refresh: bool = True,
    notify: bool = True,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
    feed=None,
) -> RunRecord:
    """Public KXBTC15M fetch. Observation only. One completion notify."""
    refuse_forbidden("ingest")
    from golf_offshoot.learning_lane_15m.loop import ingest
    from golf_offshoot.learning_lane_15m.paths import LANE_15M, PRIMARY_SERIES

    try:
        payload = ingest(refresh=refresh, feed=feed)
    except Exception as exc:
        rec = RunRecord(
            command="ingest",
            ok=False,
            event_id=PRIMARY_SERIES,
            error=str(exc),
            extras={"lane": LANE_15M},
        )
        rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return rec
    rec = RunRecord(
        command="ingest",
        ok=True,
        event_id=PRIMARY_SERIES,
        summary=(
            f"learning_lane_15m ingest series={PRIMARY_SERIES} "
            f"markets={len(payload.get('markets') or [])} "
            f"events={len(payload.get('events') or [])}"
        ),
        table=payload.get("banner") or "",
        extras={"lane": LANE_15M, "markets": len(payload.get("markets") or [])},
    )
    rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
    return rec


def run_15m_live(
    *,
    refresh: bool = True,
    notify: bool = True,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
    feed=None,
) -> RunRecord:
    """15m live refresh + paper autobet + settle join. One completion notify."""
    refuse_forbidden("live")
    from golf_offshoot.learning_lane_15m.loop import live, paper_autobet, settle_join
    from golf_offshoot.learning_lane_15m.paths import LANE_15M, PRIMARY_SERIES

    try:
        live_state = live(refresh=refresh, feed=feed)
        markets = live_state.get("markets") or []
        events = live_state.get("events") or []
        paper = paper_autobet(markets)
        joined = settle_join(markets, events)
    except Exception as exc:
        rec = RunRecord(
            command="live",
            ok=False,
            event_id=PRIMARY_SERIES,
            error=str(exc),
            extras={"lane": LANE_15M},
        )
        rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return rec
    rec = RunRecord(
        command="live",
        ok=True,
        event_id=PRIMARY_SERIES,
        summary=(
            f"learning_lane_15m live series={PRIMARY_SERIES} "
            f"fills={paper.get('fills', 0)} settled={joined.get('settled', 0)} "
            f"pending={joined.get('pending', 0)}"
        ),
        paper=paper.get("ledger") or joined.get("ledger") or "",
        table=(
            f"paper autobet fills={paper.get('fills', 0)}\n"
            f"settle settled={joined.get('settled', 0)} pending={joined.get('pending', 0)}"
        ),
        extras={
            "lane": LANE_15M,
            "paper_fills": paper.get("fills", 0),
            "settled": joined.get("settled", 0),
            "pending": joined.get("pending", 0),
        },
    )
    rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
    return rec


def run_15m_shadow(*, notify: bool = False, notify_topic: str | None = None, dry_run_notify: bool = False) -> RunRecord:
    refuse_forbidden("shadow")
    from golf_offshoot.learning_lane_15m.paper import format_15m_ledger, latest_shadow_lines
    from golf_offshoot.learning_lane_15m.paths import LANE_15M, PRIMARY_SERIES

    rec = RunRecord(
        command="shadow",
        ok=True,
        event_id=PRIMARY_SERIES,
        summary="learning_lane_15m shadow viewed",
        table="\n".join([format_15m_ledger(), *latest_shadow_lines(12)]),
        extras={"lane": LANE_15M},
    )
    if notify:
        rec.notice = _maybe_notify(rec, notify=True, topic=notify_topic, dry_run=dry_run_notify)
    return rec


def run_15m_loop(
    *,
    refresh: bool = True,
    notify: bool = True,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
    feed=None,
) -> RunRecord:
    """ingest → live → paper autobet → settle join. One completion notify."""
    refuse_forbidden("loop")
    from golf_offshoot.learning_lane_15m.loop import format_loop_report, run_loop as lane_loop
    from golf_offshoot.learning_lane_15m.paths import LANE_15M, PRIMARY_SERIES

    try:
        payload = lane_loop(refresh=refresh, feed=feed)
    except Exception as exc:
        rec = RunRecord(
            command="loop",
            ok=False,
            event_id=PRIMARY_SERIES,
            error=str(exc),
            extras={"lane": LANE_15M},
        )
        rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return rec
    paper = payload.get("paper_autobet") or {}
    joined = payload.get("settle_join") or {}
    rec = RunRecord(
        command="loop",
        ok=True,
        event_id=PRIMARY_SERIES,
        summary=(
            f"learning_lane_15m loop series={PRIMARY_SERIES} "
            f"fills={paper.get('fills', 0)} settled={joined.get('settled', 0)} "
            f"pending={joined.get('pending', 0)}"
        ),
        paper=paper.get("ledger") or joined.get("ledger") or "",
        table=format_loop_report(payload),
        extras={
            "lane": LANE_15M,
            "paper_fills": paper.get("fills", 0),
            "settled": joined.get("settled", 0),
            "pending": joined.get("pending", 0),
        },
    )
    rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
    return rec


def run_golf_kalshi_tick(
    *,
    command: str = "loop",
    notify: bool = False,
    notify_topic: str | None = None,
    dry_run_notify: bool = False,
    feed=None,
    brain=None,
    executor=None,
) -> RunRecord:
    """One Kalshi golf tick. Does not write Phase 1 or Polymarket ledgers."""
    refuse_forbidden(command if command in ALLOWED_ACTIONS else "loop")
    from golf_offshoot.golf_kalshi.loop import run_tick
    from golf_offshoot.golf_kalshi.paper import ledger_path, load_ledger

    try:
        payload = run_tick(feed=feed, brain=brain, executor=executor)
    except Exception as exc:
        rec = RunRecord(
            command=command,
            ok=False,
            error=str(exc),
            extras={"lane": "golf_kalshi"},
        )
        rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
        return rec
    led = load_ledger()
    rec = RunRecord(
        command=command,
        ok=True,
        summary=str(payload.get("summary") or "golf kalshi tick"),
        table=json_summary(payload),
        extras={
            "lane": "golf_kalshi",
            "fills": payload.get("fills"),
            "skips": payload.get("skips"),
            "consulted_decide": payload.get("consulted_decide"),
            "ledger": str(ledger_path()),
            "bankroll": led.get("bankroll"),
        },
    )
    rec.notice = _maybe_notify(rec, notify=notify, topic=notify_topic, dry_run=dry_run_notify)
    return rec


def json_summary(payload: dict) -> str:
    fills = payload.get("fills")
    skips = payload.get("skips")
    return f"golf kalshi fills={fills} skips={skips} decide=yes"


def format_run_record(rec: RunRecord) -> str:
    buf = StringIO()
    buf.write(f"status={'ok' if rec.ok else 'failed'} command={rec.command}\n")
    if rec.summary:
        buf.write(rec.summary + "\n")
    if rec.error:
        buf.write(f"ERROR {rec.error}\n")
    if rec.inventory:
        buf.write("\n" + rec.inventory + "\n")
    if rec.table:
        buf.write("\n" + rec.table + "\n")
    if rec.leftover:
        buf.write("\n" + rec.leftover + "\n")
    if rec.paper:
        buf.write("\n" + rec.paper + "\n")
    for label, path in (
        ("HTML", rec.export_html),
        ("txt", rec.export_txt),
        ("PDF", rec.export_pdf),
    ):
        if path:
            buf.write(f"export {label}: {path}\n")
    if rec.notice:
        buf.write(f"notify {rec.notice.reason}\n")
    return buf.getvalue()
