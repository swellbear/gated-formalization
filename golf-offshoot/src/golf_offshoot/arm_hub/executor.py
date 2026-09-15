"""One deterministic executor. Mode swaps host + credentials + balance source.

No AI. No bot. POLICY.json + quotes in; fill/settle out. Same functions for
paper and live. Live submit is refused unless ARM.flag and secrets resolve.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from golf_offshoot.arm_hub.arm import (
    NotArmedError,
    RuntimeMode,
    assert_live_allowed,
    refuse_live_order,
)
from golf_offshoot.arm_hub.bankroll import (
    PaperLedger,
    apply_fill,
    apply_settle,
    ceil_cent,
    daily_pnl,
    drawdown_pct,
    fee_usd,
    load_ledger,
    save_ledger,
)
from golf_offshoot.arm_hub.paths import (
    HUB_ID,
    SERIES_DEFAULT,
    assert_not_learning_lane_path,
    audit_dir,
    fills_dir,
    settlements_dir,
    state_path,
)
from golf_offshoot.arm_hub.poller import Quote
from golf_offshoot.arm_hub.strategy_loader import (
    InventPackRefused,
    assert_not_invent_for_live,
    live_allowlist,
)
from golf_offshoot.localtime import now

Venue = Literal["paper", "live"]


@dataclass
class Guardrails:
    max_step_pct_bankroll: float = 0.10
    max_step_abs_usd: float = 50.0
    peak_dd_brake_pct: float = 0.20
    daily_kill_usd: float = 75.0
    promote_bar_only_when_live: bool = True


@dataclass
class OrderIntent:
    ticker: str
    event_ticker: str
    side: str
    yes_price: float
    stake: float
    fee: float
    rule_id: str
    claim: str
    dsl: str
    reason: str


@dataclass
class Fill:
    fill_id: str
    ticker: str
    event_ticker: str
    side: str
    yes_price: float
    stake: float
    fee: float
    rule_id: str
    venue: Venue
    at: str
    note: str = ""


@dataclass
class Position:
    ticker: str
    event_ticker: str
    side: str
    yes_price: float
    stake: float
    fee: float
    rule_id: str
    fill_id: str


@dataclass
class TickResult:
    mode: str
    trading_armed: bool
    action: str
    reason: str
    bankroll: float
    policy_version: str
    fill: Fill | None = None
    settlement: dict[str, Any] | None = None
    banner: str = "NOT ARMED"


def load_state(root: Path | None = None) -> dict[str, Any]:
    path = state_path(root)
    assert_not_learning_lane_path(path)
    if not path.is_file():
        return {
            "hub_id": HUB_ID,
            "trading_armed": False,
            "mode": "paper",
            "paper_bankroll_open": 500.0,
            "paper_bankroll_now": 500.0,
            "open_positions": [],
            "policy_version": "",
            "hub_untouched_note": (
                "Separate from learning_lane_15m. Do not share paper paths "
                "or grow-freeze watcher membership."
            ),
            "unattended": True,
        }
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("state.json must be an object")
    return raw


def save_state(state: dict[str, Any], root: Path | None = None) -> Path:
    path = state_path(root)
    assert_not_learning_lane_path(path)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return path


def _day_key(ts: datetime | None = None) -> str:
    return (ts or now()).date().isoformat()


def _size_stake(ledger: PaperLedger, pct: float, guard: Guardrails) -> float:
    raw = float(ledger.bankroll) * float(pct)
    cap = min(float(guard.max_step_abs_usd), float(ledger.bankroll) * float(guard.max_step_pct_bankroll))
    return ceil_cent(max(0.0, min(raw, cap)))


def _brake_reason(ledger: PaperLedger, guard: Guardrails) -> str | None:
    if drawdown_pct(ledger) >= float(guard.peak_dd_brake_pct):
        return f"peak DD brake ({guard.peak_dd_brake_pct:.0%})"
    if daily_pnl(ledger, _day_key()) <= -abs(float(guard.daily_kill_usd)):
        return f"daily kill ({guard.daily_kill_usd:.2f})"
    return None


def context_matches(rule: dict[str, Any], quote: Quote) -> bool:
    """Contextual — not 'always fire this id'."""
    when = rule.get("when") if isinstance(rule.get("when"), dict) else {}
    lo_s = when.get("secs_to_expiry_min")
    hi_s = when.get("secs_to_expiry_max")
    if quote.secs_to_expiry is not None:
        if lo_s is not None and quote.secs_to_expiry < int(lo_s):
            return False
        if hi_s is not None and quote.secs_to_expiry > int(hi_s):
            return False
    elif lo_s is not None or hi_s is not None:
        return False
    p = quote.yes_price
    lo_p = float(when.get("yes_price_min", 0.0))
    hi_p = float(when.get("yes_price_max", 1.0))
    if not (lo_p <= p <= hi_p):
        return False
    return bool(rule.get("enabled", True))


def select_rule(
    policy: dict[str, Any],
    quote: Quote,
    runtime: RuntimeMode,
    guard: Guardrails,
) -> tuple[dict[str, Any] | None, str]:
    rules = list(policy.get("rules") or [])
    if runtime.is_live and guard.promote_bar_only_when_live:
        allowed_ids = {r["id"] for r in live_allowlist(policy)}
        rules = [r for r in rules if isinstance(r, dict) and r.get("id") in allowed_ids]
    matched: list[dict[str, Any]] = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if not context_matches(rule, quote):
            continue
        if runtime.is_live:
            try:
                assert_not_invent_for_live(rule)
            except InventPackRefused:
                continue
        matched.append(rule)
    if not matched:
        return None, "no contextual keeper matched"
    matched.sort(key=lambda r: (-float(r.get("weight") or 0.0), int(r.get("path_rank") or 99)))
    return matched[0], "contextual match"


def intent_from_rule(
    rule: dict[str, Any],
    quote: Quote,
    ledger: PaperLedger,
    guard: Guardrails,
) -> OrderIntent | None:
    stake = _size_stake(ledger, float(rule.get("size_pct_bankroll") or 0.02), guard)
    if stake <= 0:
        return None
    fee = fee_usd(stake=stake, yes_price=quote.yes_price)
    return OrderIntent(
        ticker=quote.ticker,
        event_ticker=quote.event_ticker,
        side=str(rule.get("side") or "yes"),
        yes_price=quote.yes_price,
        stake=stake,
        fee=fee,
        rule_id=str(rule.get("id") or ""),
        claim=str(rule.get("claim") or ""),
        dsl=str(rule.get("dsl") or ""),
        reason="contextual keeper",
    )


def submit_order(
    intent: OrderIntent,
    runtime: RuntimeMode,
    ledger: PaperLedger,
    *,
    root: Path | None = None,
) -> Fill:
    """Same function for paper and live. Venue is the only swap."""
    if runtime.is_live:
        assert_live_allowed(runtime)
        refuse_live_order(runtime, intent_note=intent.ticker)
    apply_fill(
        ledger,
        stake=intent.stake,
        fee=intent.fee,
        ticker=intent.ticker,
        rule_id=intent.rule_id,
        note=f"paper {intent.side} @{intent.yes_price:.4f}",
    )
    fill = Fill(
        fill_id=f"fill-{intent.ticker}",
        ticker=intent.ticker,
        event_ticker=intent.event_ticker,
        side=intent.side,
        yes_price=intent.yes_price,
        stake=intent.stake,
        fee=intent.fee,
        rule_id=intent.rule_id,
        venue="paper",
        at=now().isoformat(),
        note=intent.reason,
    )
    dest = fills_dir(root) / f"{_safe(intent.ticker)}.json"
    assert_not_learning_lane_path(dest)
    dest.write_text(json.dumps(asdict(fill), indent=2) + "\n", encoding="utf-8")
    return fill


def settle_position(
    pos: Position,
    result: str,
    ledger: PaperLedger,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    result = str(result or "").strip().lower()
    if result not in {"yes", "no"}:
        raise ValueError("settle requires official yes/no; do not invent")
    won = (pos.side == "yes" and result == "yes") or (pos.side == "no" and result == "no")
    contracts = pos.stake / pos.yes_price if pos.yes_price else 0.0
    payout = ceil_cent(contracts * 1.0) if won else 0.0
    apply_settle(
        ledger,
        payout=payout,
        stake=pos.stake,
        fee=pos.fee,
        ticker=pos.ticker,
        rule_id=pos.rule_id,
        won=won,
        day_key=_day_key(),
    )
    row = {
        "ticker": pos.ticker,
        "result": result,
        "won": won,
        "payout": payout,
        "stake": pos.stake,
        "fee": pos.fee,
        "pnl": ceil_cent(payout - pos.stake - pos.fee),
        "rule_id": pos.rule_id,
        "at": now().isoformat(),
    }
    dest = settlements_dir(root) / f"{_safe(pos.ticker)}.json"
    assert_not_learning_lane_path(dest)
    dest.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
    return row


def _safe(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in name).strip("-") or "row"


def _audit(root: Path | None, payload: dict[str, Any]) -> None:
    dest = audit_dir(root) / "ticks.jsonl"
    assert_not_learning_lane_path(dest)
    with dest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, default=str) + "\n")


def run_tick(
    *,
    quotes: list[Quote],
    policy: dict[str, Any],
    runtime: RuntimeMode,
    root: Path | None = None,
    guard: Guardrails | None = None,
    max_fills: int = 1,
) -> TickResult:
    """Deterministic tick. Reads already-loaded POLICY + quotes. No bots."""
    guard = guard or Guardrails()
    ledger = load_ledger(root)
    state = load_state(root)
    open_raw = list(state.get("open_positions") or [])
    positions = [Position(**{k: p[k] for k in Position.__dataclass_fields__ if k in p}) for p in open_raw if isinstance(p, dict)]

    settlement = None
    # Settle first when an official result is on the quote for an open ticket.
    still_open: list[Position] = []
    for pos in positions:
        match = next((q for q in quotes if q.ticker == pos.ticker and q.result in {"yes", "no"}), None)
        if match is None:
            still_open.append(pos)
            continue
        settlement = settle_position(pos, match.result, ledger, root=root)
    positions = still_open

    action = "idle"
    reason = "no quote"
    fill = None
    if quotes and not positions:
        brake = _brake_reason(ledger, guard)
        if brake:
            action, reason = "brake", brake
        else:
            # One fill per tick / window. First quote that matches context.
            filled = 0
            for quote in quotes:
                if filled >= max_fills:
                    break
                if quote.status in {"settled", "finalized", "determined"} and quote.result:
                    continue
                rule, why = select_rule(policy, quote, runtime, guard)
                if rule is None:
                    action, reason = "skip", why
                    continue
                intent = intent_from_rule(rule, quote, ledger, guard)
                if intent is None:
                    action, reason = "skip", "stake capped to 0"
                    continue
                try:
                    fill = submit_order(intent, runtime, ledger, root=root)
                except NotArmedError:
                    raise
                positions.append(
                    Position(
                        ticker=fill.ticker,
                        event_ticker=fill.event_ticker,
                        side=fill.side,
                        yes_price=fill.yes_price,
                        stake=fill.stake,
                        fee=fill.fee,
                        rule_id=fill.rule_id,
                        fill_id=fill.fill_id,
                    )
                )
                action, reason = "fill", f"{rule['id']} {why}"
                filled += 1
    elif positions:
        action, reason = "hold", "open position; one ticket at a time"

    save_ledger(ledger, root)
    state.update(
        {
            "hub_id": HUB_ID,
            "trading_armed": runtime.trading_armed,
            "mode": runtime.mode,
            "paper_bankroll_open": ledger.starting_bankroll,
            "paper_bankroll_now": ledger.bankroll,
            "open_positions": [asdict(p) for p in positions],
            "policy_version": str(policy.get("policy_version") or ""),
            "last_action": action,
            "last_reason": reason,
            "runtime_reason": runtime.reason,
            "series": SERIES_DEFAULT,
            "updated_at": now().isoformat(),
            "unattended": True,
        }
    )
    save_state(state, root)
    _audit(
        root,
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "reason": reason,
            "mode": runtime.mode,
            "armed": runtime.trading_armed,
            "bankroll": ledger.bankroll,
        },
    )
    banner = "NOT ARMED" if not runtime.trading_armed else "ARMED (live venue)"
    return TickResult(
        mode=runtime.mode,
        trading_armed=runtime.trading_armed,
        action=action,
        reason=reason,
        bankroll=ledger.bankroll,
        policy_version=str(policy.get("policy_version") or ""),
        fill=fill,
        settlement=settlement,
        banner=banner,
    )
