from golf_offshoot.decision.layer import advise_bet, min_edge_for_bet, size_frac_for_bet
from golf_offshoot.models.enums import BetType, DecisionAction, Horizon, RiskPreference, StrategyMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.models.strategy import StrategyConfig, StrategyPosition
from golf_offshoot.strategy.correlation import would_stack_win_proxy
from golf_offshoot.strategy.paper_book import lock_paper_positions, paper_candidate_slots
from golf_offshoot.strategy.sizing import suggested_stake


def _hp(horizon: Horizon, central: float, width: float = 0.04) -> HorizonProbability:
    lo = max(0.0, central - width / 2)
    hi = min(1.0, central + width / 2)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(
    *,
    pid: str = "p1",
    name: str = "Keith Mitchell",
    win: float = 0.10,
    r1: float = 0.10,
    win_posted: float = 12.5,
    r1_posted: float = 12.5,
    win_edge: float = 0.02,
    r1_edge: float = 0.02,
) -> PlayerOutput:
    bundle = ProbabilityBundle(
        player_id=pid,
        horizons={
            Horizon.WIN: _hp(Horizon.WIN, win),
            Horizon.WIN_AFTER_R1: _hp(Horizon.WIN_AFTER_R1, r1),
            Horizon.WIN_AFTER_R2: _hp(Horizon.WIN_AFTER_R2, r1),
            Horizon.WIN_AFTER_R3: _hp(Horizon.WIN_AFTER_R3, r1),
            Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
        },
        theta_mean=0.0,
        theta_sd=1.0,
    )
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=bundle,
        reliability=ReliabilityScore(
            player_id=pid, score=0.74, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        edge_by_bet={
            "win": win_edge,
            "win_after_r1": r1_edge,
            "win_after_r2": r1_edge,
            "win_after_r3": r1_edge,
        },
        market_implied_by_bet={
            "win": 1.0 / win_posted,
            "win_after_r1": 1.0 / r1_posted,
            "win_after_r2": 1.0 / r1_posted,
            "win_after_r3": 1.0 / r1_posted,
        },
        posted_odds_by_bet={
            "win": win_posted,
            "win_after_r1": r1_posted,
            "win_after_r2": r1_posted,
            "win_after_r3": r1_posted,
        },
    )


def _pos(pid: str, bet: BetType) -> StrategyPosition:
    return StrategyPosition(
        position_id=f"pos-{pid}-{bet.value}",
        player_id=pid,
        player_name="Keith Mitchell",
        bet_type=bet,
        stake=2.19,
        decimal_odds=12.5,
        entry_edge=0.04,
        entry_model_p=0.10,
        user_recorded=True,
    )


def test_winner_bar_stays_three_pp():
    assert min_edge_for_bet(BetType.WIN, 0.08) == 0.03
    assert min_edge_for_bet(BetType.WIN, 0.40) == 0.03
    assert size_frac_for_bet(BetType.WIN) == 1.0


def test_r1_eight_cent_bar_is_two_pp():
    bar = min_edge_for_bet(BetType.WIN_AFTER_R1, 0.08)
    assert abs(bar - 0.02) < 1e-12
    assert size_frac_for_bet(BetType.WIN_AFTER_R1) == 0.35


def test_r1_two_pp_can_clear_frl_and_fail_winner():
    row = _row()
    r1 = advise_bet(row, BetType.WIN_AFTER_R1, 12.5)
    win = advise_bet(row, BetType.WIN, 12.5)
    assert r1.action == DecisionAction.CONSIDER
    assert win.action == DecisionAction.PASS


def test_paper_slots_r1_two_pp_clears():
    cfg = StrategyConfig(
        enabled=True,
        allowed_bet_types=[BetType.WIN_AFTER_R1],
        ticket_screen="both",
    )
    slots = paper_candidate_slots([_row()], cfg)
    assert len(slots) == 1
    row, bet, odds, edge, posted_edge, cleared = slots[0]
    assert bet == BetType.WIN_AFTER_R1
    assert abs(odds - 12.5) < 1e-9
    assert abs(posted_edge - 0.02) < 1e-9
    assert cleared is True
    assert row.name == "Keith Mitchell"


def test_lock_r1_is_fraction_of_winner_unit(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
        allowed_bet_types=[BetType.WIN_AFTER_R1],
    )
    rec = lock_paper_positions(
        [_row()],
        cfg,
        event_id="401811963",
        run_id="run-frl",
        odds_book="polymarket",
        write_exports=False,
        independent_bankroll=True,
        path_id="polymarket",
    )
    assert len(rec.book.positions) == 1
    assert rec.book.positions[0].bet_type == BetType.WIN_AFTER_R1
    assert abs(rec.book.positions[0].stake - 3.06) < 0.02


def test_win_plus_r3_stack_skipped_r1_allowed():
    held = [_pos("p1", BetType.WIN)]
    assert would_stack_win_proxy(held, "p1", BetType.WIN_AFTER_R3) is True
    assert would_stack_win_proxy(held, "p1", BetType.WIN_AFTER_R2) is True
    assert would_stack_win_proxy(held, "p1", BetType.WIN) is True
    assert would_stack_win_proxy(held, "p1", BetType.WIN_AFTER_R1) is False
    assert would_stack_win_proxy([], "p1", BetType.WIN_AFTER_R3) is False


def test_r1_size_frac_caps_below_winner_unit():
    from golf_offshoot.strategy.sizing import scaled_single_cap

    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.PRESS_EDGES,
        risk=RiskPreference.AGGRESSIVE,
        bankroll=250,
    )
    args = dict(
        bankroll=250,
        model_p=0.20,
        low_p=0.16,
        decimal_odds=6.0,
        range_width=0.06,
        reliability=0.80,
        remaining_capacity=50,
        config=cfg,
    )
    win, _ = suggested_stake(bet_type=BetType.WIN, **args)
    r1, _ = suggested_stake(bet_type=BetType.WIN_AFTER_R1, **args)
    win_cap = 250 * scaled_single_cap(cfg)
    assert win > 0
    assert r1 > 0
    assert r1 < win
    assert r1 <= win_cap * 0.35 + 1e-9
