"""Dated wallet recipe. Live loader stays recipe_v1(). Not ranked by pnl."""

from __future__ import annotations

from dataclasses import dataclass

from golf_offshoot.config import (
    MIN_EDGE_TO_CONSIDER,
    STRATEGY_COOLING_OFF_DRAWDOWN_FRAC,
    STRATEGY_EDGE_COLLAPSE_RATIO,
    STRATEGY_EDGE_IMPROVE_ABS,
    STRATEGY_MAX_DAILY_LOSS_FRAC,
    STRATEGY_MAX_SINGLE_POSITION_FRAC,
    STRATEGY_MAX_TOTAL_EXPOSURE_FRAC,
)

RECIPE_ID = "golf-kalshi-recipe-v1.2"
PREVIOUS_RECIPE_ID = "golf-kalshi-recipe-v1"
DECLARED_AT = "2026-09-11"
PLAYER_BRAIN_VERSION = "keep_expert"
SEED_BANKROLL = 1000.0
SLOW_CAP_FRAC = 0.30
FAST_RESERVE_FRAC = 0.20
CAP_SHARE_FAST = 0.25
CAP_SHARE_WEEK = 0.50
CAP_SHARE_SLOW = 0.25
MAX_TICKETS_PER_EVENT = 3
KELLY_FRACTION = 0.25
FLIP_HURDLE = 1.20
MAX_REALLOCATES_PER_TICK = 2
MAX_ADDS_PER_TICK = 2
FAIL_HOLES = {
    "win_after_r1": 18,
    "win_after_r2": 36,
    "win_after_r3": 54,
    "win": 36,
    "top_5": 36,
    "top_10": 36,
    "top_20": 36,
    "make_cut": 36,
    "season": 0,
}
LIVE_SCALE = 0.10
LIVE_SCALE_UNTIL_N = 10
PAPER_HALT_SECONDS = 120
PAPER_RESUME_RULE = "paper_pause"
LIVE_RESUME_RULE = "next_utc_day"
RESUME_RULE = PAPER_RESUME_RULE
MIN_STAKE = 1.0
LISTED_HAIRCUT = 0.5


@dataclass(frozen=True)
class WalletRecipe:
    recipe_id: str = RECIPE_ID
    declared_at: str = DECLARED_AT
    player_brain_version: str = PLAYER_BRAIN_VERSION
    seed: float = SEED_BANKROLL
    slow_cap_frac: float = SLOW_CAP_FRAC
    fast_reserve_frac: float = FAST_RESERVE_FRAC
    cap_share_fast: float = CAP_SHARE_FAST
    cap_share_week: float = CAP_SHARE_WEEK
    cap_share_slow: float = CAP_SHARE_SLOW
    max_tickets_per_event: int = MAX_TICKETS_PER_EVENT
    kelly_fraction: float = KELLY_FRACTION
    collapse_ratio: float = STRATEGY_EDGE_COLLAPSE_RATIO
    improve_abs: float = STRATEGY_EDGE_IMPROVE_ABS
    flip_hurdle: float = FLIP_HURDLE
    max_reallocates_per_tick: int = MAX_REALLOCATES_PER_TICK
    max_adds_per_tick: int = MAX_ADDS_PER_TICK
    single_name_frac: float = STRATEGY_MAX_SINGLE_POSITION_FRAC
    total_exposure_frac: float = STRATEGY_MAX_TOTAL_EXPOSURE_FRAC
    daily_loss_frac: float = STRATEGY_MAX_DAILY_LOSS_FRAC
    drawdown_frac: float = STRATEGY_COOLING_OFF_DRAWDOWN_FRAC
    min_edge: float = MIN_EDGE_TO_CONSIDER
    live_scale: float = LIVE_SCALE
    live_scale_until_n: int = LIVE_SCALE_UNTIL_N
    paper_halt_seconds: int = PAPER_HALT_SECONDS
    paper_resume_rule: str = PAPER_RESUME_RULE
    live_resume_rule: str = LIVE_RESUME_RULE
    resume_rule: str = RESUME_RULE
    min_stake: float = MIN_STAKE
    listed_haircut: float = LISTED_HAIRCUT

    def cap_share(self, sleeve: str) -> float:
        return {
            "fast": self.cap_share_fast,
            "week": self.cap_share_week,
            "slow": self.cap_share_slow,
        }.get(str(sleeve or "week"), self.cap_share_week)

    def total_cap(self, bank: float) -> float:
        return float(self.total_exposure_frac) * float(bank)

    def sleeve_target(self, sleeve: str, bank: float) -> float:
        return self.cap_share(sleeve) * self.total_cap(bank)


def recipe_v1() -> WalletRecipe:
    """Live dated recipe. Name kept so callers do not fork."""
    return WalletRecipe()


def recipe_public() -> dict[str, object]:
    r = recipe_v1()
    cap = r.total_cap(r.seed)
    return {
        "recipe": r.recipe_id,
        "declared_at": r.declared_at,
        "player_brain": r.player_brain_version,
        "seed": r.seed,
        "slow_cap": r.slow_cap_frac,
        "fast_reserve": r.fast_reserve_frac,
        "cap_share_fast": r.cap_share_fast,
        "cap_share_week": r.cap_share_week,
        "cap_share_slow": r.cap_share_slow,
        "cap_fast": round(r.sleeve_target("fast", r.seed), 2),
        "cap_week": round(r.sleeve_target("week", r.seed), 2),
        "cap_slow": round(r.sleeve_target("slow", r.seed), 2),
        "total_cap": round(cap, 2),
        "max_tickets_per_event": r.max_tickets_per_event,
        "kelly_fraction": r.kelly_fraction,
        "single_name": r.single_name_frac,
        "total_exposure": r.total_exposure_frac,
        "daily_loss": r.daily_loss_frac,
        "drawdown": r.drawdown_frac,
        "resume": r.paper_resume_rule,
        "paper_halt_seconds": r.paper_halt_seconds,
        "live_resume": r.live_resume_rule,
    }


def fail_holes_for(horizon: str) -> int:
    return int(FAIL_HOLES.get(str(horizon or ""), 36) or 0)
