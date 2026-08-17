"""Typed bid vs hold-to-expiry value. Never invents a sell. Never auto-trades."""

from __future__ import annotations

import re
from dataclasses import dataclass

from options_offshoot.compare.law import METHOD_LAW_V1
from options_offshoot.config import PRESS_CASHOUT_BUFFER
from options_offshoot.models.enums import StrategyMode
from options_offshoot.models.schemas import PaperPosition, RankedContract

_PAIR = re.compile(
    r"^\s*(.+?)\s*[=:]\s*\$?\s*([0-9]+(?:\.[0-9]+)?)\s*$",
    re.IGNORECASE,
)


def parse_cashout_cli(raw: list[str] | str | None) -> dict[str, float]:
    """Map contract_id or underlying -> per-share bid."""
    if raw is None:
        return {}
    chunks = raw if isinstance(raw, list) else [raw]
    out: dict[str, float] = {}
    for chunk in chunks:
        for part in str(chunk).split(","):
            part = part.strip()
            if not part:
                continue
            m = _PAIR.match(part)
            if not m:
                continue
            key = m.group(1).strip()
            out[key] = float(m.group(2))
    return out


def typed_bid(cashouts: dict[str, float], pos: PaperPosition) -> float | None:
    if pos.contract_id in cashouts:
        return cashouts[pos.contract_id]
    if pos.underlying in cashouts:
        return cashouts[pos.underlying]
    return None


@dataclass(frozen=True)
class CashoutCompare:
    quote_per_share: float
    proceeds: float
    hold_value: float
    threshold: float
    beats_hold: bool


def hold_to_expiry_value(pos: PaperPosition, row: RankedContract | None) -> float | None:
    if row is None or row.model.fair is None:
        return None
    n = int(pos.n_contracts or 0)
    if n <= 0:
        return None
    return float(row.model.fair) * int(pos.multiplier) * n


def exit_proceeds(per_share: float, pos: PaperPosition) -> float:
    n = max(int(pos.n_contracts or 0), 0)
    return float(per_share) * int(pos.multiplier) * n


def buffer_for(mode: StrategyMode) -> float:
    if mode == StrategyMode.PROTECT_PROFITS:
        return 0.0
    if mode == StrategyMode.PRESS_EDGES:
        return float(PRESS_CASHOUT_BUFFER)
    return float(METHOD_LAW_V1["stay_selective_cashout_buffer"])


def compare_bid(
    pos: PaperPosition,
    row: RankedContract | None,
    per_share: float,
    *,
    mode: StrategyMode,
) -> CashoutCompare | None:
    hold = hold_to_expiry_value(pos, row)
    if hold is None:
        return None
    proceeds = exit_proceeds(per_share, pos)
    buf = buffer_for(mode)
    threshold = hold * (1.0 + buf)
    return CashoutCompare(
        quote_per_share=per_share,
        proceeds=proceeds,
        hold_value=hold,
        threshold=threshold,
        beats_hold=proceeds + 1e-9 >= threshold,
    )
