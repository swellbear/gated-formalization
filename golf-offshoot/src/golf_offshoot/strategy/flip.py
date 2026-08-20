"""Flip sleeve on listed Yes cards: leftover heat P(), small NEW, sell at fill+20%.

Winner, R1/R2/R3, and any other mapped Polymarket Yes that actually quotes.
Not hold-to-settle. Not keep-to-win. Never a CLOB order. Never invents a card.
"""

from __future__ import annotations

from collections import Counter

import numpy as np

from golf_offshoot.config import (
    DEFAULT_CUT_PLACE,
    DEFAULT_ROUND_SIGMA,
    DEFAULT_ROUNDS,
    FLIP_HEAT_N_SIMS,
    FLIP_HURDLE,
    FLIP_MAX_STAKE_FRAC,
    FLIP_NEW_MAX,
    FLIP_NEW_MAX_TOTAL,
    FLIP_NEW_MIN_P,
    FLIP_SIZE_FRAC,
)
from golf_offshoot.models.enums import BetType, Horizon, StrategyActionKind, horizon_for
from golf_offshoot.models.schemas import FieldSnapshot, PlayerOutput
from golf_offshoot.models.strategy import (
    StrategyAction,
    StrategyConfig,
    StrategyPosition,
    new_id,
)
from golf_offshoot.strategy import explanations as X
from golf_offshoot.strategy.correlation import would_stack_flip
from golf_offshoot.strategy.sizing import remaining_exposure_capacity, scaled_single_cap


FLIP_FAIL_HOLES = {
    BetType.WIN: 36,
    BetType.WIN_AFTER_R1: 18,
    BetType.WIN_AFTER_R2: 36,
    BetType.WIN_AFTER_R3: 54,
    BetType.TOP_5: 36,
    BetType.TOP_10: 36,
    BetType.TOP_20: 36,
    BetType.MAKE_CUT: 36,
}

FLIP_MARKET_LABEL = {
    BetType.WIN: "Win",
    BetType.WIN_AFTER_R1: "R1 leader",
    BetType.WIN_AFTER_R2: "R2 leader",
    BetType.WIN_AFTER_R3: "R3 leader",
    BetType.TOP_5: "Top 5",
    BetType.TOP_10: "Top 10",
    BetType.TOP_20: "Top 20",
    BetType.MAKE_CUT: "Make cut",
}

_PLACE_K = {
    BetType.TOP_5: 5,
    BetType.TOP_10: 10,
    BetType.TOP_20: 20,
}


def flip_fail_holes(bet: BetType | str) -> int:
    key = bet if isinstance(bet, BetType) else BetType(str(bet))
    return int(FLIP_FAIL_HOLES.get(key, 36))


def flip_entry_bar(ask: float | None, bid: float | None) -> float | None:
    """P() bar: conditional contract % >= ask + spread. Spread = ask - bid when both exist."""
    if ask is None or ask <= 0.0 or ask >= 1.0:
        return None
    spread = 0.0
    if bid is not None and 0.0 < bid < 1.0:
        spread = max(0.0, float(ask) - float(bid))
    return float(min(0.99, ask + spread))


def card_ask(row: PlayerOutput, bet: BetType) -> float | None:
    posted = row.posted_odds_by_bet.get(bet.value)
    try:
        dec = float(posted) if posted is not None else None
    except (TypeError, ValueError):
        return None
    if dec is None or dec <= 1.0:
        return None
    ask = 1.0 / dec
    if ask <= 0.0 or ask >= 1.0:
        return None
    return float(ask)


def card_bid(row: PlayerOutput, bet: BetType) -> float | None:
    raw = row.bid_by_bet.get(bet.value)
    try:
        bid = float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None
    if bid is None or bid <= 0.0 or bid >= 1.0:
        return None
    return float(bid)


def winner_ask(row: PlayerOutput) -> float | None:
    return card_ask(row, BetType.WIN)


def winner_bid(row: PlayerOutput) -> float | None:
    return card_bid(row, BetType.WIN)


def listed_flip_bets(
    row: PlayerOutput,
    *,
    allowed: list[BetType] | None = None,
    has_cut: bool = True,
) -> list[BetType]:
    allow = set(allowed) if allowed is not None else set(BetType)
    out: list[BetType] = []
    for bet in BetType:
        if bet not in allow:
            continue
        if bet not in FLIP_FAIL_HOLES:
            continue
        if bet == BetType.MAKE_CUT and not has_cut:
            continue
        if card_ask(row, bet) is None:
            continue
        out.append(bet)
    return out


def is_flip(pos: StrategyPosition) -> bool:
    return (getattr(pos, "intent", "hold") or "hold").lower() == "flip"


def open_flip_positions(positions: list[StrategyPosition]) -> list[StrategyPosition]:
    """Filled or proposed flip tickets that still have stake. Hold-to-Sunday does not count."""
    return [p for p in positions if is_flip(p) and float(p.stake or 0.0) > 0.0]


def flip_cost(pos: StrategyPosition) -> float:
    raw = getattr(pos, "cost_usd", None)
    if raw is not None and float(raw) > 0:
        return float(raw)
    shares = getattr(pos, "shares", None)
    fill = getattr(pos, "fill_price", None)
    if shares is not None and fill is not None and float(shares) > 0 and float(fill) > 0:
        return float(shares) * float(fill)
    return float(pos.stake or 0.0)


def flip_hurdle_dollars(pos: StrategyPosition) -> float:
    return flip_cost(pos) * FLIP_HURDLE


def position_is_fill(pos: StrategyPosition) -> bool:
    shares = getattr(pos, "shares", None)
    fill = getattr(pos, "fill_price", None)
    try:
        return shares is not None and float(shares) > 0 and fill is not None and float(fill) > 0
    except (TypeError, ValueError):
        return False


def board_progress_holes(rows: list[PlayerOutput]) -> int:
    return max((int(r.live_holes_completed or 0) for r in rows), default=0)


def flip_dead(row: PlayerOutput | None) -> bool:
    if row is None:
        return False
    if row.withdrawn:
        return True
    status = (row.live_status_name or "").lower()
    if "wd" in status or "withdraw" in status:
        return True
    if row.live_made_cut is False:
        return True
    return False


def _softmax_win(expected_final: np.ndarray, scale: float, wd: np.ndarray) -> np.ndarray:
    """Softmax over -expected_final / scale. Lower score wins. WD share is 0."""
    scale = max(float(scale), 1e-6)
    logits = -expected_final / scale
    logits = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(np.clip(logits, -40.0, 40.0))
    exp[:, wd] = 0.0
    denom = exp.sum(axis=1, keepdims=True)
    denom = np.maximum(denom, 1e-12)
    return exp / denom


def _soft_place(expected_final: np.ndarray, scale: float, k: int, wd: np.ndarray) -> np.ndarray:
    """P(finish top k) from expected totals vs the kth cutoff, with remaining noise."""
    n = expected_final.shape[1]
    kk = max(1, min(int(k), n))
    kth = np.partition(expected_final, kk - 1, axis=1)[:, kk - 1]
    z = (expected_final - kth[:, None]) / (max(float(scale), 1e-6) * np.sqrt(2.0))
    p = 1.0 / (1.0 + np.exp(np.clip(z * 1.702, -40.0, 40.0)))
    p[:, wd] = 0.0
    return p


def flip_heat_from_theta(
    theta_mean: np.ndarray,
    theta_sd: np.ndarray,
    bars: np.ndarray,
    withdrawn: np.ndarray | None = None,
    *,
    n_rounds: int = DEFAULT_ROUNDS,
    n_sims: int = FLIP_HEAT_N_SIMS,
    round_sigma: float = DEFAULT_ROUND_SIGMA,
    seed: int | None = 20260818,
) -> np.ndarray:
    """P(max(Win% after 18, Win% after 36) >= bar_i). Vector of length n."""
    table = _heat_table(
        theta_mean,
        theta_sd,
        {BetType.WIN: bars},
        withdrawn,
        n_rounds=n_rounds,
        n_sims=n_sims,
        round_sigma=round_sigma,
        seed=seed,
    )
    return table.get(BetType.WIN, np.full(int(theta_mean.shape[0]), np.nan))


def _heat_table(
    theta_mean: np.ndarray,
    theta_sd: np.ndarray,
    bars_by_bet: dict[BetType, np.ndarray],
    withdrawn: np.ndarray | None = None,
    *,
    n_rounds: int = DEFAULT_ROUNDS,
    n_sims: int = FLIP_HEAT_N_SIMS,
    round_sigma: float = DEFAULT_ROUND_SIGMA,
    seed: int | None = 20260818,
    cut_place: int = DEFAULT_CUT_PLACE,
    has_cut: bool = True,
) -> dict[BetType, np.ndarray]:
    n = int(theta_mean.shape[0])
    empty = {bet: np.full(n, np.nan, dtype=float) for bet in bars_by_bet}
    if n == 0 or not bars_by_bet:
        return empty
    wd = withdrawn if withdrawn is not None else np.zeros(n, dtype=bool)
    any_valid = False
    for bars in bars_by_bet.values():
        if np.any(np.isfinite(bars) & (bars > 0.0) & (bars < 1.0) & (~wd)):
            any_valid = True
            break
    if not any_valid:
        out = empty
        for bet in out:
            out[bet] = out[bet].copy()
            out[bet][wd] = 0.0
        return out

    rng = np.random.default_rng(seed)
    n_rounds = max(2, int(n_rounds))
    theta = rng.normal(theta_mean, np.maximum(theta_sd, 1e-4), size=(n_sims, n))
    theta[:, wd] = -1e9
    half_sig = round_sigma * np.sqrt(0.5)
    r1_front = -theta * 0.5 + rng.normal(0.0, half_sig, size=(n_sims, n))
    r1 = -theta + rng.normal(0.0, round_sigma, size=(n_sims, n))
    r2 = -theta + rng.normal(0.0, round_sigma, size=(n_sims, n))
    rem1 = max(n_rounds - 1, 1)
    rem2 = max(n_rounds - 2, 1)
    p_win_r1 = _softmax_win(r1 - theta * rem1, round_sigma * np.sqrt(rem1), wd)
    p_win_r2 = _softmax_win(r1 + r2 - theta * rem2, round_sigma * np.sqrt(rem2), wd)
    p_lead18 = _softmax_win(r1_front - theta * 0.5, half_sig, wd)
    p_lead36 = _softmax_win(r1 - theta * 1.0, round_sigma, wd)
    p_lead54 = _softmax_win(r1 + r2 - theta * 1.0, round_sigma, wd)
    p_place_r1 = {
        bet: _soft_place(r1 - theta * rem1, round_sigma * np.sqrt(rem1), k, wd)
        for bet, k in _PLACE_K.items()
        if bet in bars_by_bet
    }
    p_place_r2 = {
        bet: _soft_place(r1 + r2 - theta * rem2, round_sigma * np.sqrt(rem2), k, wd)
        for bet, k in _PLACE_K.items()
        if bet in bars_by_bet
    }
    p_cut = None
    if has_cut and BetType.MAKE_CUT in bars_by_bet:
        p_cut = _soft_place(r1 - theta * 1.0, round_sigma, max(1, int(cut_place)), wd)

    out: dict[BetType, np.ndarray] = {}
    for bet, bars in bars_by_bet.items():
        valid = np.isfinite(bars) & (bars > 0.0) & (bars < 1.0) & (~wd)
        hit = np.zeros((n_sims, n), dtype=bool)
        if bet == BetType.WIN:
            cond = (p_win_r1 >= bars) | (p_win_r2 >= bars)
        elif bet == BetType.WIN_AFTER_R1:
            cond = p_lead18 >= bars
        elif bet == BetType.WIN_AFTER_R2:
            cond = p_lead36 >= bars
        elif bet == BetType.WIN_AFTER_R3:
            cond = p_lead54 >= bars
        elif bet in _PLACE_K:
            cond = (p_place_r1[bet] >= bars) | (p_place_r2[bet] >= bars)
        elif bet == BetType.MAKE_CUT and p_cut is not None:
            cond = p_cut >= bars
        else:
            out[bet] = np.full(n, np.nan)
            out[bet][wd] = 0.0
            continue
        hit[:, valid] = cond[:, valid]
        heat = hit.mean(axis=0)
        heat[~valid] = np.nan
        heat[wd] = 0.0
        out[bet] = heat
    return out


def _heat_get(row: PlayerOutput, bet: BetType) -> tuple[float | None, float | None]:
    by_p = getattr(row, "flip_heat_p_by_bet", None) or {}
    by_b = getattr(row, "flip_heat_bar_by_bet", None) or {}
    p = by_p.get(bet.value)
    bar = by_b.get(bet.value)
    if p is None and bet == BetType.WIN:
        p = row.flip_heat_p
    if bar is None and bet == BetType.WIN:
        bar = row.flip_heat_bar
    return p, bar


def attach_flip_heat(
    rows: list[PlayerOutput],
    *,
    n_rounds: int = DEFAULT_ROUNDS,
    n_sims: int = FLIP_HEAT_N_SIMS,
    seed: int | None = 20260818,
    cut_place: int = DEFAULT_CUT_PLACE,
    has_cut: bool = True,
) -> None:
    """Fill per-card flip_heat_p_by_bet on ranked rows. Mutates in place."""
    if not rows:
        return
    n = len(rows)
    means = np.array([r.probabilities.theta_mean for r in rows], dtype=float)
    sds = np.array([r.probabilities.theta_sd for r in rows], dtype=float)
    wd = np.array([bool(r.withdrawn) for r in rows], dtype=bool)
    needed: set[BetType] = set()
    bars_by_bet: dict[BetType, np.ndarray] = {}
    for row in rows:
        row.flip_heat_p_by_bet = {}
        row.flip_heat_bar_by_bet = {}
        for bet in listed_flip_bets(row, has_cut=has_cut):
            needed.add(bet)
    if not needed:
        for row in rows:
            row.flip_heat_p = None
            row.flip_heat_bar = None
        return
    for bet in needed:
        bars = np.full(n, np.nan, dtype=float)
        for i, row in enumerate(rows):
            bar = flip_entry_bar(card_ask(row, bet), card_bid(row, bet))
            if bar is not None:
                row.flip_heat_bar_by_bet[bet.value] = bar
                bars[i] = bar
        bars_by_bet[bet] = bars
    table = _heat_table(
        means,
        sds,
        bars_by_bet,
        wd,
        n_rounds=n_rounds,
        n_sims=n_sims,
        seed=seed,
        cut_place=cut_place,
        has_cut=has_cut,
    )
    for bet, heat in table.items():
        for i, row in enumerate(rows):
            val = float(heat[i])
            if not np.isfinite(val):
                continue
            row.flip_heat_p_by_bet[bet.value] = val
    for row in rows:
        row.flip_heat_p = row.flip_heat_p_by_bet.get(BetType.WIN.value)
        row.flip_heat_bar = row.flip_heat_bar_by_bet.get(BetType.WIN.value)


def leftover_flip_heat_lines(rows: list[PlayerOutput]) -> list[str]:
    """Display P(early contract % >= ask+spread) per listed card. Not a ticket unless NEW fires."""
    lines = [
        "  P(this card's model % at an early mark >= ask + spread). Bid tracking that % is an assumption.",
        "  Display listed Yes only. NEW if P >= 0.20. One flip per player. Cap is 6 open flips (no refill). Flip sells at fill+20%, not keep-to-win.",
    ]
    any_card = False
    for bet in (
        BetType.WIN,
        BetType.WIN_AFTER_R1,
        BetType.WIN_AFTER_R2,
        BetType.WIN_AFTER_R3,
        BetType.TOP_5,
        BetType.TOP_10,
        BetType.TOP_20,
        BetType.MAKE_CUT,
    ):
        ranked: list[tuple[float, str, float, float, float | None]] = []
        for row in rows:
            ask = card_ask(row, bet)
            if ask is None:
                continue
            p, bar = _heat_get(row, bet)
            if p is None or bar is None:
                continue
            ranked.append((float(p), row.name, float(bar), ask, card_bid(row, bet)))
        if not ranked:
            continue
        any_card = True
        ranked.sort(key=lambda t: t[0], reverse=True)
        label = FLIP_MARKET_LABEL.get(bet, bet.value)
        fail = flip_fail_holes(bet)
        lines.append(f"  {label} — fail clock {fail} holes; not hold-to-settle")
        for p, name, bar, ask, bid in ranked[:8]:
            tag = "NEW if applied" if p >= FLIP_NEW_MIN_P else "below NEW floor"
            bid_s = f"{bid:.3f}" if bid is not None else "n/a"
            lines.append(
                f"    {name}  P={p:.2f}  bar={bar:.3f}  ask={ask:.3f}  bid={bid_s}  {tag}"
            )
    if not any_card:
        return [
            "  No listed Yes ask on this snapshot, or heat not attached. Display leftover, not a ticket.",
            "  NEW only if P >= 0.20. Flip sells at fill+20%, not keep-to-win. One flip per player.",
        ]
    lines.append(
        "  Display leftover. Do not stack two flips on the same name. Unlisted cards are not invented."
    )
    return lines


def flip_stake(config: StrategyConfig, remaining_capacity: float) -> float:
    unit = config.bankroll * scaled_single_cap(config)
    want = min(unit * FLIP_SIZE_FRAC, config.bankroll * FLIP_MAX_STAKE_FRAC)
    stake = min(want, max(0.0, remaining_capacity))
    min_unit = 0.002 * config.bankroll * FLIP_SIZE_FRAC
    if stake < min_unit:
        return 0.0
    return float(stake)


def build_flip_new(
    rows: list[PlayerOutput],
    config: StrategyConfig,
    open_positions: list[StrategyPosition],
    field: FieldSnapshot | None = None,
) -> tuple[list[StrategyAction], list[StrategyPosition]]:
    """Flip NEW on listed Yes. Skips hold-to-settle screens. Tiny vs bankroll. One per player.

    Caps are against open flip fills plus this snapshot's NEW. A live after you already
    booked six does not top up with the next-best names. A fail/sell that frees a slot
    can still print whoever is hottest then. Hold-to-Sunday tickets do not eat the cap.
    """
    _ = field
    actions: list[StrategyAction] = []
    proposed: list[StrategyPosition] = []
    allowed = list(config.allowed_bet_types or list(BetType))
    held_flips = open_flip_positions(open_positions)
    if len(held_flips) >= FLIP_NEW_MAX_TOTAL:
        return actions, proposed
    open_exp = sum(float(p.stake or 0.0) for p in open_positions)
    cands: list[tuple[float, PlayerOutput, BetType]] = []
    for row in rows:
        for bet in listed_flip_bets(row, allowed=allowed):
            if int(row.live_holes_completed or 0) >= flip_fail_holes(bet):
                continue
            p, bar = _heat_get(row, bet)
            if p is None or bar is None or p < FLIP_NEW_MIN_P:
                continue
            if would_stack_flip(open_positions + proposed, row.player_id, bet):
                continue
            cands.append((float(p), row, bet))
    cands.sort(key=lambda t: t[0], reverse=True)
    per_market: Counter[BetType] = Counter(p.bet_type for p in held_flips)
    seen_players: set[str] = set()
    for _, row, bet in cands:
        if row.player_id in seen_players:
            continue
        if per_market[bet] >= FLIP_NEW_MAX:
            continue
        if len(held_flips) + len(proposed) >= FLIP_NEW_MAX_TOTAL:
            break
        cap = remaining_exposure_capacity(open_exp, config.bankroll, config)
        stake = flip_stake(config, cap)
        if stake <= 0:
            break
        ask = card_ask(row, bet)
        if ask is None:
            continue
        h = horizon_for(bet)
        hp = row.probabilities.horizons.get(h) if h is not None else None
        if hp is None:
            continue
        odds = 1.0 / ask
        pid = new_id("pos")
        p, bar = _heat_get(row, bet)
        label = FLIP_MARKET_LABEL.get(bet, bet.value)
        pos = StrategyPosition(
            position_id=pid,
            player_id=row.player_id,
            player_name=row.name,
            bet_type=bet,
            stake=stake,
            decimal_odds=odds,
            entry_edge=row.edge_by_bet.get(bet.value) or 0.0,
            entry_model_p=hp.central,
            entry_market_p=row.market_implied_by_bet.get(bet.value),
            round_entered=0,
            notes=f"flip sleeve {label}; sell at fill+20% if still green next live",
            proposed=True,
            user_recorded=False,
            intent="flip",
        )
        proposed.append(pos)
        open_exp += stake
        seen_players.add(row.player_id)
        per_market[bet] += 1
        actions.append(
            StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.NEW_BET,
                player_id=row.player_id,
                player_name=row.name,
                bet_type=bet,
                position_id=pid,
                suggested_stake_delta=stake,
                suggested_unit=stake,
                reason=X.flip_heat_new(),
                reasons_detail=[
                    f"{label} flip heat P={p:.2f}" if p is not None else "flip heat",
                    f"bar={bar:.3f}" if bar is not None else "bar n/a",
                    f"hurdle fill x {FLIP_HURDLE:.0%}",
                    f"fail clock {flip_fail_holes(bet)} holes",
                    "not keep-to-win",
                    "one flip per player",
                ],
            )
        )
    return actions, proposed
