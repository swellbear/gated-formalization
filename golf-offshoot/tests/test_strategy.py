"""Decision Layer + Dynamic Strategy System — tests. Never auto-bets."""

from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.demo import demo_field, demo_odds, demo_open_book, demo_tournament
from golf_offshoot.models.enums import (
    BetType,
    RunMode,
    RiskPreference,
    StrategyActionKind,
    StrategyMode,
)
from golf_offshoot.models.strategy import (
    StrategyConfig,
    StrategyPosition,
    new_id,
)
from golf_offshoot.pipeline import GolfOffshootPipeline
from golf_offshoot.strategy.engine import record_user_decision, run_strategy
from golf_offshoot.strategy.live import _action_for_open, golf_has_started
from golf_offshoot.strategy.path import mark_position
from golf_offshoot.strategy.sizing import suggested_stake, uncertainty_blocks_action


def _pipe(**kw):
    engine = BayesianEngine(sim=SimConfig(n_sims=400, seed=21))
    return GolfOffshootPipeline(engine=engine, snapshot_dir=None, **kw)


def test_strategy_off_is_pure_analysis():
    pipe = _pipe()
    result = pipe.run(demo_tournament(), demo_field(), market_quotes=demo_odds(demo_field()), persist=False)
    assert result.strategy is not None
    assert result.strategy.enabled is False
    assert result.strategy.never_auto_bet is True
    assert result.never_auto_bet is True
    assert result.audit.strategy is not None
    assert result.audit.strategy.enabled is False


def test_pre_tournament_builder_suggests_and_never_executes():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, risk=RiskPreference.NORMAL, bankroll=2000)
    pipe = _pipe(strategy_config=cfg)
    f = demo_field()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    rec = result.strategy
    assert rec.enabled is True
    assert rec.never_auto_bet is True
    assert rec.run_mode == RunMode.PRE_TOURNAMENT
    for a in rec.actions:
        assert a.never_auto_bet is True
        assert a.requires_user_confirmation is True
        assert a.reason
    exposure = sum(p.stake for p in rec.proposed_new_positions)
    assert exposure <= cfg.bankroll * 0.35 + 1e-6


def test_wide_range_and_low_reliability_block_add():
    assert uncertainty_blocks_action(0.25, 0.80) is not None
    assert uncertainty_blocks_action(0.05, 0.20) is not None
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, risk=RiskPreference.CONSERVATIVE, bankroll=1000)
    stake, warn = suggested_stake(
        bankroll=1000,
        model_p=0.12,
        low_p=0.02,
        decimal_odds=9.0,
        range_width=0.25,
        reliability=0.80,
        config=cfg,
        remaining_capacity=200,
    )
    assert stake == 0.0
    assert warn


def test_conservative_sizes_smaller_than_aggressive():
    args = dict(
        bankroll=5000,
        model_p=0.22,
        low_p=0.18,
        decimal_odds=8.0,
        range_width=0.06,
        reliability=0.75,
        remaining_capacity=2000,
    )
    cons, _ = suggested_stake(
        config=StrategyConfig(enabled=True, risk=RiskPreference.CONSERVATIVE, mode=StrategyMode.STAY_SELECTIVE),
        **args,
    )
    agg, _ = suggested_stake(
        config=StrategyConfig(enabled=True, risk=RiskPreference.AGGRESSIVE, mode=StrategyMode.PRESS_EDGES),
        **args,
    )
    assert agg > cons > 0


def test_tiny_kelly_still_emits_minimum_advisory_unit():
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=2000,
    )
    stake, warn = suggested_stake(
        bankroll=2000,
        model_p=0.0975,
        low_p=0.070,
        decimal_odds=17.0,
        range_width=0.054,
        reliability=0.81,
        config=cfg,
        remaining_capacity=400,
    )
    assert stake == 4.0
    assert warn and "minimum advisory" in warn.lower()


def test_protect_vs_press_on_runner():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[0]
    # fabricate a runner: long entry odds, much shorter live odds
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.WIN,
        stake=50.0,
        decimal_odds=25.0,
        entry_edge=0.04,
        entry_model_p=0.06,
        entry_market_p=0.04,
        round_entered=0,
        user_recorded=True,
    )
    mark = mark_position(pos, row)
    assert mark.is_runner
    protect = StrategyConfig(enabled=True, mode=StrategyMode.PROTECT_PROFITS, bankroll=2000)
    press = StrategyConfig(enabled=True, mode=StrategyMode.PRESS_EDGES, bankroll=2000)
    a_prot = _action_for_open(mark, pos, protect, cooling=False)
    a_press = _action_for_open(mark, pos, press, cooling=False)
    assert a_prot.kind == StrategyActionKind.REDUCE
    assert "run strongly" in a_prot.reason.lower() or "lock" in a_prot.reason.lower()
    assert a_press.kind in (StrategyActionKind.HOLD, StrategyActionKind.ADD)
    assert a_prot.kind != a_press.kind or a_prot.suggested_stake_delta != a_press.suggested_stake_delta


def test_mark_position_prefers_posted_decimal():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[0]
    row = row.model_copy(
        update={
            "posted_odds_by_bet": {**dict(row.posted_odds_by_bet), "win": 8.0},
            "market_implied_by_bet": {**dict(row.market_implied_by_bet), "win": 0.20},
        }
    )
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.WIN,
        stake=8.0,
        decimal_odds=16.0,
        entry_edge=0.04,
        entry_model_p=0.08,
        user_recorded=True,
    )
    mark = mark_position(pos, row)
    assert mark.live_decimal_odds == 8.0
    assert abs(mark.mtm_value - 16.0) < 1e-9
    assert mark.live_posted_edge is not None
    assert abs(mark.live_posted_edge - (mark.live_model_p - 0.125)) < 1e-9


def test_collapsed_edge_exits():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[-1]
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.WIN,
        stake=40.0,
        decimal_odds=8.0,
        entry_edge=0.10,
        entry_model_p=0.20,
        entry_market_p=0.10,
        user_recorded=True,
    )
    mark = mark_position(pos, row)
    # force collapse flags if live edge still high
    mark = mark.model_copy(update={"original_edge_collapsed": True, "live_edge": -0.02, "is_runner": False})
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=2000)
    act = _action_for_open(mark, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.EXIT
    assert "collapsed" in act.reason.lower()


def test_pre_tee_collapsed_holds():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    assert golf_has_started(result.ranked) is False
    row = result.ranked[-1]
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.WIN,
        stake=2.19,
        decimal_odds=29.41,
        entry_edge=0.023,
        entry_model_p=0.036,
        user_recorded=True,
    )
    mark = mark_position(pos, row)
    mark = mark.model_copy(update={"original_edge_collapsed": True, "live_edge": 0.001, "is_runner": False})
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    act = _action_for_open(mark, pos, cfg, cooling=False, golf_started=False)
    assert act.kind == StrategyActionKind.HOLD
    assert "has not started" in act.reason.lower()
    row = row.model_copy(update={"live_holes_completed": 9, "live_score_to_par": -2, "live_place": 4})
    assert golf_has_started([row]) is True
    started = _action_for_open(mark, pos, cfg, cooling=False, golf_started=True)
    assert started.kind == StrategyActionKind.EXIT


def test_cooling_off_blocks_new_risk():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.PRESS_EDGES, bankroll=1000)
    f = demo_field()
    pipe = _pipe(strategy_config=cfg)
    pre = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    book = demo_open_book(pre, bankroll=1000, n=1)
    book.realized_pnl_today = -80  # 8% > 5% daily cap
    live_field = demo_field()
    for i, p in enumerate(live_field.players):
        p.live_score_to_par = i * 0.2
        p.live_holes_completed = 9
    live = pipe.rerun_live(
        demo_tournament(),
        live_field,
        previous=pre.audit,
        market_quotes=demo_odds(live_field),
        open_book=book,
        strategy_config=cfg,
    )
    assert live.strategy.cooling_off is True
    kinds = {a.kind for a in live.strategy.actions}
    assert StrategyActionKind.NEW_BET not in kinds
    assert StrategyActionKind.ADD not in kinds


def test_live_marks_show_entry_vs_live_edge():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=2000)
    pipe = _pipe()
    f = demo_field()
    pre = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    book = demo_open_book(pre, bankroll=2000, n=2)
    live_field = demo_field()
    for i, p in enumerate(live_field.players):
        p.live_score_to_par = -4 + i * 0.5
        p.live_holes_completed = 18
    live = pipe.rerun_live(
        demo_tournament(),
        live_field,
        previous=pre.audit,
        market_quotes=demo_odds(live_field),
        open_book=book,
        strategy_config=cfg,
    )
    assert live.strategy.marks
    m = live.strategy.marks[0]
    assert m.entry_edge == book.positions[0].entry_edge
    assert m.live_model_p is not None
    assert live.strategy.status.biggest_concentration
    assert live.strategy.status.posture == StrategyMode.STAY_SELECTIVE


def test_user_decision_is_journal_only():
    cfg = StrategyConfig(enabled=True, bankroll=1000)
    pipe = _pipe(strategy_config=cfg)
    f = demo_field()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    rec = result.strategy
    aid = rec.actions[0].action_id if rec.actions else None
    d = record_user_decision(rec, aid, accepted=False, note="skip", operator="test")
    assert d.placed_by_user is True
    assert d.accepted is False
    result.audit.user_strategy_decisions.append(d)
    assert result.audit.user_strategy_decisions[0].note == "skip"


def test_every_live_action_has_plain_reason():
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.PROTECT_PROFITS, bankroll=2000)
    pipe = _pipe()
    f = demo_field()
    pre = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    book = demo_open_book(pre, bankroll=2000)
    rec = run_strategy(pre.ranked, cfg, run_mode=RunMode.LIVE, field=f, book=book)
    for a in rec.actions:
        assert a.reason
        assert a.never_auto_bet


def test_unmarked_place_ticket_holds_ride_to_settle_not_intact():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[0]
    row = row.model_copy(
        update={
            "edge_by_bet": {k: v for k, v in row.edge_by_bet.items() if k == "win"},
            "market_implied_by_bet": {k: v for k, v in row.market_implied_by_bet.items() if k == "win"},
            "posted_odds_by_bet": {k: v for k, v in row.posted_odds_by_bet.items() if k == "win"},
        }
    )
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.TOP_20,
        stake=1.61,
        decimal_odds=6.0,
        entry_edge=0.357,
        entry_model_p=0.363,
        user_recorded=True,
    )
    mark = mark_position(pos, row, ticket_screen="both")
    assert mark.live_edge_unmarked is True
    assert mark.original_edge_collapsed is False
    cfg = StrategyConfig(
        enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=270, ticket_screen="both"
    )
    act = _action_for_open(mark, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.HOLD
    assert "settle" in act.reason.lower()
    assert "coupon" in act.reason.lower()
    assert "intact" not in act.reason.lower()


def test_posted_screen_unmarked_when_place_coupon_missing():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[0]
    row = row.model_copy(
        update={
            "edge_by_bet": {**row.edge_by_bet, "top_20": 0.20},
            "posted_odds_by_bet": {k: v for k, v in row.posted_odds_by_bet.items() if k == "win"},
            "market_implied_by_bet": {k: v for k, v in row.market_implied_by_bet.items() if k == "win"},
        }
    )
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.TOP_20,
        stake=1.61,
        decimal_odds=6.0,
        entry_edge=0.357,
        entry_model_p=0.363,
        user_recorded=True,
    )
    both = mark_position(pos, row, ticket_screen="both")
    assert both.live_edge_unmarked is False
    posted = mark_position(pos, row, ticket_screen="posted")
    assert posted.live_edge_unmarked is True
    assert posted.original_edge_collapsed is False
    cfg = StrategyConfig(
        enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=270, ticket_screen="posted"
    )
    act = _action_for_open(posted, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.HOLD
    assert "intact" not in act.reason.lower()


def test_marked_win_hold_still_says_intact_when_edge_lives():
    f = demo_field()
    pipe = _pipe()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[0]
    row = row.model_copy(
        update={
            "edge_by_bet": {**row.edge_by_bet, "win": 0.07},
            "posted_odds_by_bet": {**row.posted_odds_by_bet, "win": 19.0},
            "market_implied_by_bet": {**row.market_implied_by_bet, "win": 1.0 / 19.0},
        }
    )
    pos = StrategyPosition(
        position_id=new_id("pos"),
        player_id=row.player_id,
        player_name=row.name,
        bet_type=BetType.WIN,
        stake=0.54,
        decimal_odds=19.0,
        entry_edge=0.07,
        entry_model_p=0.07 + 1.0 / 19.0,
        user_recorded=True,
    )
    mark = mark_position(pos, row, ticket_screen="both")
    assert mark.live_edge_unmarked is False
    assert mark.original_edge_collapsed is False
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=270)
    act = _action_for_open(mark, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.HOLD
    assert "intact" in act.reason.lower()
    assert "settle" not in act.reason.lower()
