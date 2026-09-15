"""One-tick and replay drivers. Disk POLICY/state only. No bot calls."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from golf_offshoot.arm_hub.arm import resolve_mode
from golf_offshoot.arm_hub.bankroll import load_ledger, save_ledger
from golf_offshoot.arm_hub.executor import Guardrails, TickResult, run_tick
from golf_offshoot.arm_hub.paths import assert_not_learning_lane_path, config_path, replay_tape_path
from golf_offshoot.arm_hub.poller import (
    QuoteFetchError,
    fetch_public_open_markets,
    load_replay_tape,
    quotes_from_replay_window,
)
from golf_offshoot.arm_hub.strategy_loader import load_or_build_policy


def _parse_scalar(raw: str) -> Any:
    text = raw.strip()
    if text in {"true", "True", "yes"}:
        return True
    if text in {"false", "False", "no"}:
        return False
    if text in {"null", "None", "~"}:
        return None
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text.strip("'\"")


def load_config(root: Path | None = None) -> dict[str, Any]:
    path = config_path(root)
    defaults: dict[str, Any] = {
        "interval_s": 30,
        "quotes_source": "replay",
        "max_step_pct_bankroll": 0.10,
        "max_step_abs_usd": 50.0,
        "peak_dd_brake_pct": 0.20,
        "daily_kill_usd": 75.0,
        "promote_bar_only_when_live": True,
        "prefer_keep_only": True,
        "series": "KXBTC15M",
    }
    if not path.is_file():
        return defaults
    assert_not_learning_lane_path(path)
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if not stripped or ":" not in stripped:
            continue
        key, val = stripped.split(":", 1)
        key = key.strip()
        if key in defaults or key in {
            "hub_id",
            "paper_bankroll_open",
            "trading_armed",
            "paper_mode",
        }:
            defaults[key] = _parse_scalar(val)
    return defaults


def _guard(cfg: dict[str, Any]) -> Guardrails:
    return Guardrails(
        max_step_pct_bankroll=float(cfg.get("max_step_pct_bankroll", 0.10)),
        max_step_abs_usd=float(cfg.get("max_step_abs_usd", 50.0)),
        peak_dd_brake_pct=float(cfg.get("peak_dd_brake_pct", 0.20)),
        daily_kill_usd=float(cfg.get("daily_kill_usd", 75.0)),
        promote_bar_only_when_live=bool(cfg.get("promote_bar_only_when_live", True)),
    )


def ensure_seed(root: Path | None = None) -> None:
    """Create the $500 ledger if missing. Does not reset an existing book."""
    save_ledger(load_ledger(root), root)


def run_once(
    root: Path | None = None,
    *,
    quotes_source: str | None = None,
    rebuild_policy: bool = False,
) -> TickResult:
    """One unattended tick. Rebuild of POLICY is offline-only (default false)."""
    ensure_seed(root)
    cfg = load_config(root)
    source = (quotes_source or str(cfg.get("quotes_source") or "replay")).lower()
    runtime = resolve_mode(root)
    policy = load_or_build_policy(
        root,
        prefer_keep_only=bool(cfg.get("prefer_keep_only", True)),
        rebuild=rebuild_policy,
    )
    if source == "public":
        try:
            quotes = fetch_public_open_markets()
        except QuoteFetchError:
            quotes = []
    else:
        tape = load_replay_tape(root=root)
        quotes = []
        if tape:
            quotes = quotes_from_replay_window(tape[0])
    return run_tick(
        quotes=quotes,
        policy=policy,
        runtime=runtime,
        root=root,
        guard=_guard(cfg),
    )


def run_replay(root: Path | None = None) -> list[TickResult]:
    """Play the whole fixture tape (CI / paper exam). Same executor as live."""
    ensure_seed(root)
    cfg = load_config(root)
    runtime = resolve_mode(root)
    policy = load_or_build_policy(root, rebuild=False)
    tape = load_replay_tape(replay_tape_path(root), root=root)
    results: list[TickResult] = []
    for window in tape:
        quotes = quotes_from_replay_window(window)
        # Quote-only tick (may fill).
        results.append(
            run_tick(
                quotes=quotes,
                policy=policy,
                runtime=runtime,
                root=root,
                guard=_guard(cfg),
            )
        )
        result = str(window.get("result") or "").strip().lower()
        if result in {"yes", "no"}:
            settled_quotes = []
            for q in quotes:
                settled_quotes.append(
                    type(q)(
                        ticker=q.ticker,
                        event_ticker=q.event_ticker,
                        yes_bid=q.yes_bid,
                        yes_ask=q.yes_ask,
                        yes_price=q.yes_price,
                        secs_to_expiry=q.secs_to_expiry,
                        status="settled",
                        result=result,
                        raw=q.raw,
                    )
                )
            results.append(
                run_tick(
                    quotes=settled_quotes,
                    policy=policy,
                    runtime=runtime,
                    root=root,
                    guard=_guard(cfg),
                )
            )
    return results
