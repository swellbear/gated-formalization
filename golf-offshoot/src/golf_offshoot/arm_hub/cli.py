"""CLI for the ARM hub. Own flags. Never binds port 8765."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from golf_offshoot.arm_hub.arm import resolve_mode
from golf_offshoot.arm_hub.bankroll import load_ledger
from golf_offshoot.arm_hub.executor import load_state
from golf_offshoot.arm_hub.loop import run_once, run_replay
from golf_offshoot.arm_hub.paths import arm_hub_root, set_arm_hub_root_override
from golf_offshoot.arm_hub.strategy_loader import load_or_build_policy, pin_from_operator_dir
from golf_offshoot.arm_hub.watch import run_watch, write_kill

FORBIDDEN_PORT = 8765


def _banner(runtime_mode: str, armed: bool) -> str:
    if armed:
        return "*** ARMED (live venue) ***"
    return "*** NOT ARMED — PAPER ***"


def print_status(root: Path | None = None) -> None:
    runtime = resolve_mode(root)
    ledger = load_ledger(root)
    state = load_state(root)
    print("=== ARM HUB (paper-live sim) ===")
    print(_banner(runtime.mode, runtime.trading_armed))
    print(f"mode={runtime.mode}  ladder={runtime.ladder_rung}")
    print(f"reason={runtime.reason}")
    print(
        f"paper bankroll: {ledger.starting_bankroll:.2f} open → "
        f"{ledger.bankroll:.2f} now  (accumulate; no daily reset)"
    )
    print(f"betting_pnl={ledger.betting_pnl:.2f}  fees_paid={ledger.fees_paid:.2f}")
    print(f"policy={state.get('policy_version') or '(none yet)'}")
    opens = state.get("open_positions") or []
    print(f"open positions: {len(opens)}")
    for pos in opens:
        print(f"  - {pos.get('ticker')} {pos.get('side')} @{pos.get('yes_price')} rule={pos.get('rule_id')}")
    print("loop: unattended deterministic Python — no bot in the hot path")
    print("host swap when live:", runtime.host)
    print("sacred learning_lane_15m: untouched")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="golf_offshoot arm-hub",
        description=(
            "Separate Kalshi ARM-candidate hub. Paper $500 by default. "
            "Trading NOT ARMED. No bot in the runtime loop. Never port 8765."
        ),
    )
    p.add_argument(
        "--watch",
        action="store_true",
        help="always-on own PID; loop until latest/KILL",
    )
    p.add_argument(
        "--kill",
        action="store_true",
        help="write data/arm_hub/latest/KILL (does not touch learning_lane)",
    )
    p.add_argument(
        "--status",
        action="store_true",
        help="print paper bankroll / policy / NOT ARMED banner and exit",
    )
    p.add_argument(
        "--replay",
        action="store_true",
        help="play the fixture tape end-to-end (CI / paper exam)",
    )
    p.add_argument(
        "--pin-from",
        default="",
        help="offline: copy shortlist_v1 + SHORTLIST_SHELF from this dir into strategies/",
    )
    p.add_argument(
        "--rebuild-policy",
        action="store_true",
        help="offline: rebuild POLICY.json from pinned keepers (never used by --watch)",
    )
    p.add_argument("--root", default="", help="override data/arm_hub root (tests)")
    p.add_argument(
        "--interval",
        type=float,
        default=None,
        help="--watch sleep seconds (default from config.yaml)",
    )
    p.add_argument(
        "--quotes",
        default="",
        choices=["", "replay", "public"],
        help="quote source override (default config.yaml; replay for CI)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="print the tick result as JSON",
    )
    p.add_argument(
        "--port",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.port == FORBIDDEN_PORT:
        print("ARM hub must not bind port 8765 (learning-lane hub).", file=sys.stderr)
        return 2
    root = Path(args.root).resolve() if args.root else None
    if root is not None:
        set_arm_hub_root_override(root)
    try:
        if args.kill:
            path = write_kill(root or arm_hub_root())
            print(f"wrote {path} (ARM hub only; learning_lane untouched)")
            return 0
        if args.pin_from:
            copied = pin_from_operator_dir(Path(args.pin_from), root=root)
            load_or_build_policy(root, rebuild=True)
            print("pinned:", ", ".join(str(p) for p in copied.values()))
            return 0
        if args.status:
            print_status(root)
            return 0
        if args.watch:
            return run_watch(
                root,
                interval_s=args.interval,
                quotes_source=args.quotes or None,
            )
        if args.replay:
            results = run_replay(root)
            if args.as_json:
                print(
                    json.dumps(
                        [
                            {
                                "action": r.action,
                                "reason": r.reason,
                                "bankroll": r.bankroll,
                                "mode": r.mode,
                                "armed": r.trading_armed,
                            }
                            for r in results
                        ],
                        indent=2,
                    )
                )
            else:
                print_status(root)
                print(f"replay ticks: {len(results)}")
            return 0
        tick = run_once(
            root,
            quotes_source=args.quotes or None,
            rebuild_policy=bool(args.rebuild_policy),
        )
        if args.as_json:
            print(
                json.dumps(
                    {
                        "action": tick.action,
                        "reason": tick.reason,
                        "bankroll": tick.bankroll,
                        "mode": tick.mode,
                        "armed": tick.trading_armed,
                        "banner": tick.banner,
                        "policy_version": tick.policy_version,
                    },
                    indent=2,
                )
            )
        else:
            print_status(root)
            print(f"tick: {tick.action} — {tick.reason}")
        return 0
    finally:
        if root is not None:
            set_arm_hub_root_override(None)
