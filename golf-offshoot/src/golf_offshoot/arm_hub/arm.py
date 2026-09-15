"""Mode gate: PAPER unless ARM.flag and production secrets are both present.

One executor codepath. This module only chooses venue + host + balance source.
It never invents keys. It never places an order.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from golf_offshoot.arm_hub.paths import arm_flag_path, assert_not_learning_lane_path

Mode = Literal["paper", "live"]

PROD_HOST = "https://external-api.kalshi.com/trade-api/v2"
DEMO_HOST = "https://demo-api.kalshi.com/trade-api/v2"
PAPER_PUBLIC_HOST = "https://api.elections.kalshi.com/trade-api/v2"

KEY_ID_ENV = "KALSHI_ARM_API_KEY_ID"
KEY_PATH_ENV = "KALSHI_ARM_PRIVATE_KEY_PATH"

LADDER = ("paper", "demo_shadow", "live")


class NotArmedError(RuntimeError):
    """Live orders / live venue are refused. Default is PAPER / NOT ARMED."""


class LiveKeysMissing(NotArmedError):
    """ARM.flag is not enough. Production keys must come from env/files."""


@dataclass(frozen=True)
class Secrets:
    key_id: str | None
    private_key_path: str | None

    @property
    def complete(self) -> bool:
        if not self.key_id or not self.private_key_path:
            return False
        return Path(self.private_key_path).is_file()


@dataclass(frozen=True)
class RuntimeMode:
    mode: Mode
    trading_armed: bool
    live_arm_flag: bool
    host: str
    secrets: Secrets
    reason: str
    ladder_rung: str

    @property
    def is_live(self) -> bool:
        return self.mode == "live" and self.trading_armed


def load_secrets_from_env(
    environ: dict[str, str] | None = None,
) -> Secrets:
    """Read key id + RSA path from env only. Empty if unset. Never invent."""
    env = environ if environ is not None else os.environ
    key_id = (env.get(KEY_ID_ENV) or "").strip() or None
    key_path = (env.get(KEY_PATH_ENV) or "").strip() or None
    if key_path:
        assert_not_learning_lane_path(key_path)
    return Secrets(key_id=key_id, private_key_path=key_path)


def arm_flag_present(root: Path | None = None) -> bool:
    return arm_flag_path(root).is_file()


def resolve_mode(
    root: Path | None = None,
    *,
    environ: dict[str, str] | None = None,
) -> RuntimeMode:
    """PAPER unless ``latest/ARM.flag`` exists AND both secrets resolve.

    Missing keys with a flag still stay PAPER. The executor does not invent
    credentials and does not silently flip live.
    """
    flag = arm_flag_present(root)
    secrets = load_secrets_from_env(environ)
    if flag and secrets.complete:
        return RuntimeMode(
            mode="live",
            trading_armed=True,
            live_arm_flag=True,
            host=PROD_HOST,
            secrets=secrets,
            reason="ARM.flag present and production secrets resolved",
            ladder_rung="live",
        )
    if flag and not secrets.complete:
        return RuntimeMode(
            mode="paper",
            trading_armed=False,
            live_arm_flag=True,
            host=PAPER_PUBLIC_HOST,
            secrets=secrets,
            reason=(
                "ARM.flag present but "
                f"{KEY_ID_ENV} / {KEY_PATH_ENV} missing or unreadable; staying PAPER"
            ),
            ladder_rung="paper",
        )
    return RuntimeMode(
        mode="paper",
        trading_armed=False,
        live_arm_flag=False,
        host=PAPER_PUBLIC_HOST,
        secrets=secrets,
        reason="ARM.flag absent; PAPER (NOT ARMED)",
        ladder_rung="paper",
    )


def assert_live_allowed(runtime: RuntimeMode) -> None:
    """Hard gate before any live order or private endpoint."""
    if not runtime.live_arm_flag:
        raise NotArmedError(
            "ARM hub is NOT ARMED (latest/ARM.flag absent); live orders refused"
        )
    if not runtime.secrets.complete:
        raise LiveKeysMissing(
            f"live orders refused: set {KEY_ID_ENV} and {KEY_PATH_ENV} "
            "(RSA .key file). Keys are never invented."
        )
    if not runtime.trading_armed or runtime.mode != "live":
        raise NotArmedError("ARM hub trading_armed is false; live orders refused")


def refuse_live_order(runtime: RuntimeMode, *, intent_note: str = "") -> None:
    """Always-on guard used by the single executor before a live submit."""
    assert_live_allowed(runtime)
    extra = f" ({intent_note})" if intent_note else ""
    raise NotArmedError(
        f"live submit reached the transport stub{extra}; "
        "this scaffold ships paper-first. Live HTTP is the same codepath "
        f"swapped to {PROD_HOST} only after ARM.flag + keys."
    )
