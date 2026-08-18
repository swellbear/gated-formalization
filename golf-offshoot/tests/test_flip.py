from golf_offshoot.audit.journal import build_audit
from golf_offshoot.config import FLIP_HURDLE, FLIP_NEW_MIN_P
from golf_offshoot.demo import demo_tournament
from golf_offshoot.models.enums import BetType, Horizon, RunMode, StrategyActionKind, StrategyMode
from golf_offshoot.models.schemas import (
    HorizonProbability,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
    TournamentRunResult,
)
from golf_offshoot.models.strategy import (
    PortfolioState,
    PositionMark,
    StrategyConfig,
    StrategyPosition,
    new_id,
)
from golf_offshoot.ranking.leftover import format_leftover_callout
from golf_offshoot.strategy.correlation import would_stack_flip, would_stack_win_proxy
from golf_offshoot.strategy.flip import (
    build_flip_new,
    flip_entry_bar,
    flip_heat_from_theta,
    leftover_flip_heat_lines,
)
from golf_offshoot.strategy.live import _action_for_open, live_manage
from golf_offshoot.strategy.paper_book import PaperMovement
from golf_offshoot.strategy.paper_trigger import group_trigger_actions

import numpy as np


def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    lo = max(0.0, central - 0.01)
    hi = min(1.0, central + 0.01)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(
    pid: str,
    name: str,
    win: float,
    *,
    ask_dec: float | None = None,
    bid: float | None = None,
    theta: float = 0.0,
    heat_p: float | None = None,
    heat_bar: float | None = None,
    heat_by_bet: dict[str, float] | None = None,
    bar_by_bet: dict[str, float] | None = None,
    holes: int = 0,
    withdrawn: bool = False,
    extra_posted: dict[str, float] | None = None,
    extra_bids: dict[str, float] | None = None,
) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
        Horizon.WIN_AFTER_R1: _hp(Horizon.WIN_AFTER_R1, min(1.0, win * 2)),
        Horizon.WIN_AFTER_R2: _hp(Horizon.WIN_AFTER_R2, min(1.0, win * 2)),
        Horizon.WIN_AFTER_R3: _hp(Horizon.WIN_AFTER_R3, min(1.0, win * 2)),
    }
    bundle = ProbabilityBundle(
        player_id=pid, horizons=horizons, theta_mean=theta, theta_sd=0.4
    )
    rel = ReliabilityScore(
        player_id=pid, score=0.7, data_density=0.5, data_quality=0.5, input_stability=0.5
    )
    posted = {"win": ask_dec} if ask_dec is not None else {}
    if extra_posted:
        posted.update(extra_posted)
    bids = {"win": bid} if bid is not None else {}
    if extra_bids:
        bids.update(extra_bids)
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=bundle,
        reliability=rel,
        posted_odds_by_bet=posted,
        bid_by_bet=bids,
        flip_heat_p=heat_p,
        flip_heat_bar=heat_bar,
        flip_heat_p_by_bet=dict(heat_by_bet or {}),
        flip_heat_bar_by_bet=dict(bar_by_bet or {}),
        live_holes_completed=holes,
        withdrawn=withdrawn,
    )


def _flip_pos(**kwargs) -> StrategyPosition:
    base = dict(
        position_id=new_id("pos"),
        player_id="p1",
        player_name="Flip Name",
        bet_type=BetType.WIN,
        stake=2.19,
        decimal_odds=28.64,
        entry_edge=0.01,
        entry_model_p=0.04,
        shares=62.72,
        fill_price=0.0349,
        cost_usd=2.19,
        intent="flip",
        flip_hurdle_hits=0,
        user_recorded=True,
    )
    base.update(kwargs)
    return StrategyPosition(**base)


def _mark(*, offer: float | None, model_p: float = 0.04) -> PositionMark:
    return PositionMark(
        position_id="pos-1",
        player_id="p1",
        bet_type=BetType.WIN,
        entry_edge=0.01,
        live_edge=0.01,
        entry_model_p=0.04,
        live_model_p=model_p,
        entry_market_p=0.035,
        live_market_p=0.033,
        live_decimal_odds=30.0,
        stake=2.19,
        mtm_value=offer if offer is not None else 2.19,
        unrealized_pnl=0.0,
        original_edge_collapsed=False,
        live_edge_improved=False,
        is_runner=False,
        range_width=0.04,
        reliability=0.7,
        cashout_quote=offer,
        hold_expected_payout=2.50,
        mtm_is_bid=True,
        live_bid=0.033,
        shares=62.72,
    )


def test_flip_bar_is_ask_plus_spread():
    assert abs(flip_entry_bar(0.05, 0.04) - 0.06) < 1e-9
    assert abs(flip_entry_bar(0.05, None) - 0.05) < 1e-9
    assert flip_entry_bar(None, 0.04) is None


def test_heat_favorite_beats_longshot_at_same_bar():
    means = np.array([2.5, 0.0])
    sds = np.array([0.2, 0.2])
    bars = np.array([0.35, 0.35])
    p = flip_heat_from_theta(means, sds, bars, n_sims=800, seed=7)
    assert 0.0 <= p[0] <= 1.0
    assert 0.0 <= p[1] <= 1.0
    assert p[0] > p[1]


def test_leftover_prints_flip_heat_not_as_ticket():
    row = _row(
        "p1",
        "Heat Name",
        0.04,
        ask_dec=28.57,
        bid=0.033,
        heat_p=0.12,
        heat_bar=0.042,
    )
    t = demo_tournament()
    audit = build_audit(t.tournament_id, RunMode.PRE_TOURNAMENT, [row], "flip-left")
    result = TournamentRunResult(
        run_id=audit.run_id,
        tournament=t,
        mode=RunMode.PRE_TOURNAMENT,
        ranked=[row],
        audit=audit,
    )
    text = format_leftover_callout(result)
    assert "== flip heat (display; NEW if P>=0.20) ==" in text
    blob = "\n".join(leftover_flip_heat_lines([row]))
    assert "Heat Name" in blob
    assert "P=0.12" in blob
    assert "below NEW floor" in blob


def test_flip_new_skips_low_p_and_r1_stack():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    low = _row("p1", "Low Heat", 0.03, ask_dec=40.0, bid=0.02, heat_p=0.10, heat_bar=0.045)
    high = _row("p2", "High Heat", 0.03, ask_dec=50.0, bid=0.018, heat_p=0.40, heat_bar=0.038)
    _acts, pos = build_flip_new([low, high], cfg, [])
    assert all(p.intent == "flip" for p in pos)
    assert all(p.player_id == "p2" for p in pos)
    assert high.flip_heat_p >= FLIP_NEW_MIN_P
    r1 = StrategyPosition(
        position_id="r1",
        player_id="p2",
        player_name="High Heat",
        bet_type=BetType.WIN_AFTER_R1,
        stake=1.0,
        decimal_odds=12.0,
        entry_edge=0.02,
        entry_model_p=0.10,
    )
    _acts2, pos2 = build_flip_new([high], cfg, [r1])
    assert pos2 == []
    assert would_stack_win_proxy([r1], "p2", BetType.WIN, intent="flip") is True


def test_r1_still_sits_beside_hold_win():
    held = [
        StrategyPosition(
            position_id="w",
            player_id="p1",
            bet_type=BetType.WIN,
            stake=2.0,
            decimal_odds=20.0,
            entry_edge=0.03,
            entry_model_p=0.08,
            intent="hold",
        )
    ]
    assert would_stack_win_proxy(held, "p1", BetType.WIN_AFTER_R1) is False
    flip = held[0].model_copy(update={"intent": "flip"})
    assert would_stack_win_proxy([flip], "p1", BetType.WIN_AFTER_R1) is True


def test_flip_take_pop_needs_second_green_live():
    cfg = StrategyConfig(enabled=True, bankroll=250)
    pos = _flip_pos()
    hurdle = 2.19 * FLIP_HURDLE
    row = _row("p1", "Flip Name", 0.04, holes=9)
    first = _action_for_open(
        _mark(offer=hurdle + 0.01),
        pos,
        cfg,
        cooling=False,
        golf_started=True,
        row=row,
        progress_holes=9,
    )
    assert first.kind == StrategyActionKind.HOLD
    assert "green" in first.reason.lower()
    assert pos.flip_hurdle_hits == 1
    second = _action_for_open(
        _mark(offer=hurdle + 0.01),
        pos,
        cfg,
        cooling=False,
        golf_started=True,
        row=row,
        progress_holes=9,
    )
    assert second.kind == StrategyActionKind.EXIT
    assert "take the pop" in second.reason.lower()


def test_flip_does_not_use_keep_to_win():
    cfg = StrategyConfig(enabled=True, bankroll=250)
    pos = _flip_pos(flip_hurdle_hits=1)
    offer = 2.19 * FLIP_HURDLE + 0.01
    act = _action_for_open(
        _mark(offer=offer),
        pos,
        cfg,
        cooling=False,
        golf_started=True,
        row=_row("p1", "Flip Name", 0.04, holes=9),
        progress_holes=9,
    )
    assert act.kind == StrategyActionKind.EXIT
    assert "take the pop" in act.reason.lower()
    assert "winner ev" not in act.reason.lower()


def test_hold_intent_unaffected_by_flip_hurdle():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    pos = _flip_pos(intent="hold", flip_hurdle_hits=1)
    mark = _mark(offer=2.63)
    mark = mark.model_copy(
        update={
            "cashout_beats_hold": False,
            "hold_expected_payout": 10.0,
            "cashout_threshold": 11.0,
        }
    )
    act = _action_for_open(mark, pos, cfg, cooling=False, golf_started=True)
    assert "take the pop" not in act.reason.lower()


def test_pre_tee_flip_holds_even_if_green():
    cfg = StrategyConfig(enabled=True, bankroll=250)
    pos = _flip_pos(flip_hurdle_hits=1)
    act = _action_for_open(
        _mark(offer=5.00),
        pos,
        cfg,
        cooling=False,
        golf_started=False,
        row=_row("p1", "Flip Name", 0.04, holes=0),
        progress_holes=0,
    )
    assert act.kind == StrategyActionKind.HOLD
    assert pos.flip_hurdle_hits == 0


def test_flip_failed_after_36_exits_at_bid():
    cfg = StrategyConfig(enabled=True, bankroll=250)
    pos = _flip_pos()
    act = _action_for_open(
        _mark(offer=2.00),
        pos,
        cfg,
        cooling=False,
        golf_started=True,
        row=_row("p1", "Flip Name", 0.01, holes=36),
        progress_holes=36,
    )
    assert act.kind == StrategyActionKind.EXIT
    assert "flip failed" in act.reason.lower()


def test_trigger_labels_take_the_pop():
    mv = PaperMovement(
        movement_id="m1",
        kind="exit",
        player_name="Flip Name",
        bet_type="win",
        stake_delta=-2.19,
        reason_plain="Take the pop: offer still clears fill plus 20%.",
        reason_technical="kind=exit reason=Take the pop",
        intent="flip",
    )
    sell = group_trigger_actions([mv])[0]
    assert sell.label == "SELL"
    assert "TAKE THE POP" in sell.rows[0].extra


def test_live_flip_new_keeps_sleeve_size_not_kelly_min():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    row = _row(
        "p2",
        "High Heat",
        0.003,
        ask_dec=400.0,
        bid=0.002,
        heat_p=0.80,
        heat_bar=0.004,
    )
    actions, proposed, _marks = live_manage(
        [row],
        PortfolioState(bankroll=250.0),
        cfg,
        None,
        cooling=False,
    )
    flips = [p for p in proposed if p.intent == "flip"]
    assert flips
    assert all(p.stake > 1.0 for p in flips)
    assert all("flip sleeve" in (p.notes or "") for p in flips)
    assert any(a.kind == StrategyActionKind.NEW_BET and "Flip heat" in a.reason for a in actions)


def test_leftover_prints_r1_when_quoted():
    row = _row(
        "p1",
        "R1 Heat",
        0.04,
        extra_posted={"win_after_r1": 20.0},
        extra_bids={"win_after_r1": 0.04},
        heat_by_bet={"win_after_r1": 0.33},
        bar_by_bet={"win_after_r1": 0.06},
    )
    blob = "\n".join(leftover_flip_heat_lines([row]))
    assert "R1 leader" in blob
    assert "R1 Heat" in blob
    assert "P=0.33" in blob
    assert "fail clock 18 holes" in blob


def test_flip_new_can_emit_r1_and_skips_unlisted_top10():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    row = _row(
        "p3",
        "Lead Pop",
        0.04,
        extra_posted={"win_after_r1": 16.0},
        extra_bids={"win_after_r1": 0.05},
        heat_by_bet={"win_after_r1": 0.55, "top_10": 0.90},
        bar_by_bet={"win_after_r1": 0.07, "top_10": 0.12},
    )
    _acts, pos = build_flip_new([row], cfg, [])
    assert len(pos) == 1
    assert pos[0].bet_type == BetType.WIN_AFTER_R1
    assert pos[0].intent == "flip"


def test_one_flip_per_player_even_if_two_cards_clear():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    row = _row(
        "p4",
        "Both Cards",
        0.04,
        ask_dec=40.0,
        bid=0.02,
        extra_posted={"win_after_r1": 18.0},
        extra_bids={"win_after_r1": 0.05},
        heat_p=0.50,
        heat_bar=0.04,
        heat_by_bet={"win": 0.50, "win_after_r1": 0.80},
        bar_by_bet={"win": 0.04, "win_after_r1": 0.06},
    )
    _acts, pos = build_flip_new([row], cfg, [])
    assert len(pos) == 1
    assert pos[0].bet_type == BetType.WIN_AFTER_R1


def test_hold_win_blocks_r1_flip():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    row = _row(
        "p1",
        "Held Win",
        0.04,
        extra_posted={"win_after_r1": 16.0},
        heat_by_bet={"win_after_r1": 0.70},
        bar_by_bet={"win_after_r1": 0.07},
    )
    held = [
        StrategyPosition(
            position_id="w",
            player_id="p1",
            player_name="Held Win",
            bet_type=BetType.WIN,
            stake=2.19,
            decimal_odds=28.0,
            entry_edge=0.02,
            entry_model_p=0.04,
            intent="hold",
        )
    ]
    assert would_stack_flip(held, "p1", BetType.WIN_AFTER_R1) is True
    _acts, pos = build_flip_new([row], cfg, held)
    assert pos == []


def test_flip_new_does_not_refill_when_open_flips_at_cap():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    held = [
        _flip_pos(player_id=f"h{i}", player_name=f"Held {i}")
        for i in range(6)
    ]
    hot = _row(
        "hot",
        "Next Best",
        0.03,
        ask_dec=50.0,
        bid=0.018,
        heat_p=0.90,
        heat_bar=0.038,
    )
    _acts, pos = build_flip_new([hot], cfg, held)
    assert pos == []


def test_flip_new_fills_only_free_slots_after_sell():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    held = [
        _flip_pos(player_id=f"w{i}", player_name=f"Win {i}")
        for i in range(2)
    ] + [
        _flip_pos(
            player_id=f"r{i}",
            player_name=f"R2 {i}",
            bet_type=BetType.WIN_AFTER_R2,
        )
        for i in range(3)
    ]
    hotter = _row(
        "a",
        "Hotter",
        0.03,
        ask_dec=50.0,
        bid=0.018,
        heat_p=0.90,
        heat_bar=0.038,
    )
    hot = _row(
        "b",
        "Hot",
        0.03,
        ask_dec=40.0,
        bid=0.02,
        heat_p=0.80,
        heat_bar=0.040,
    )
    _acts, pos = build_flip_new([hotter, hot], cfg, held)
    assert len(pos) == 1
    assert pos[0].player_id == "a"


def test_hold_tickets_do_not_eat_flip_slots():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    holds = [
        _flip_pos(player_id=f"h{i}", player_name=f"Hold {i}", intent="hold")
        for i in range(6)
    ]
    hot = _row(
        "hot",
        "Flip Name",
        0.03,
        ask_dec=50.0,
        bid=0.018,
        heat_p=0.90,
        heat_bar=0.038,
    )
    _acts, pos = build_flip_new([hot], cfg, holds)
    assert len(pos) == 1
    assert pos[0].player_id == "hot"
    assert pos[0].intent == "flip"


def test_open_flips_count_toward_per_market_cap():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    held = [
        _flip_pos(player_id=f"w{i}", player_name=f"Win {i}", bet_type=BetType.WIN)
        for i in range(3)
    ]
    win_only = _row(
        "next-win",
        "Next Win",
        0.03,
        ask_dec=50.0,
        bid=0.018,
        heat_p=0.90,
        heat_bar=0.038,
    )
    _acts, pos = build_flip_new([win_only], cfg, held)
    assert pos == []
    r1 = _row(
        "next-r1",
        "Next R1",
        0.03,
        extra_posted={"win_after_r1": 16.0},
        extra_bids={"win_after_r1": 0.05},
        heat_by_bet={"win_after_r1": 0.55},
        bar_by_bet={"win_after_r1": 0.07},
    )
    _acts2, pos2 = build_flip_new([r1], cfg, held)
    assert len(pos2) == 1
    assert pos2[0].bet_type == BetType.WIN_AFTER_R1


def test_r1_flip_fails_at_18_not_36():
    cfg = StrategyConfig(enabled=True, bankroll=250)
    pos = _flip_pos(bet_type=BetType.WIN_AFTER_R1)
    act = _action_for_open(
        _mark(offer=2.00),
        pos,
        cfg,
        cooling=False,
        golf_started=True,
        row=_row("p1", "Flip Name", 0.04, holes=18),
        progress_holes=18,
    )
    assert act.kind == StrategyActionKind.EXIT
    assert "flip failed" in act.reason.lower()
    still_open = _action_for_open(
        _mark(offer=2.00),
        _flip_pos(bet_type=BetType.WIN_AFTER_R1),
        cfg,
        cooling=False,
        golf_started=True,
        row=_row("p1", "Flip Name", 0.04, holes=9),
        progress_holes=9,
    )
    assert still_open.kind == StrategyActionKind.HOLD
