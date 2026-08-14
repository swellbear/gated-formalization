"""User-typed cash-out vs remaining winner EV. Never auto-bets."""

from golf_offshoot.models.enums import (
    BetType,
    Horizon,
    RiskPreference,
    StrategyActionKind,
    StrategyMode,
)
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.models.strategy import StrategyConfig, StrategyPosition, new_id
from golf_offshoot.strategy.cashout import (
    bind_cashout_quotes,
    compare_cashout,
    estimated_cashout_offer,
    parse_cashout_cli,
)
from golf_offshoot.strategy.live import _action_for_open
from golf_offshoot.strategy.paper_book import (
    PaperMovement,
    apply_advice,
    backfill_estimated_cashouts,
    lock_paper_positions,
)
from golf_offshoot.strategy.paper_ledger import load_ledger
from golf_offshoot.strategy.path import mark_position


def _hp(horizon: Horizon, central: float, *, low: float | None = None, high: float | None = None) -> HorizonProbability:
    lo = central if low is None else low
    hi = central if high is None else high
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(pid: str, name: str, win: float, *, posted: float, edge: float, low: float | None = None, high: float | None = None) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win, low=low, high=high),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.0, theta_sd=1.0),
        reliability=ReliabilityScore(
            player_id=pid, score=0.74, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        edge_by_bet={"win": edge},
        market_implied_by_bet={"win": 1.0 / posted},
        posted_odds_by_bet={"win": posted},
    )


def _pos(**kw) -> StrategyPosition:
    return StrategyPosition(
        position_id=new_id("pos"),
        player_id=kw.get("player_id", "10364"),
        player_name=kw.get("player_name", "Kurt Kitayama"),
        bet_type=BetType.WIN,
        stake=kw.get("stake", 8.75),
        decimal_odds=kw.get("decimal_odds", 19.0),
        entry_edge=0.049,
        entry_model_p=0.089,
        user_recorded=True,
    )


def test_parse_cashout_cli_pairs_and_junk():
    pairs, warn = parse_cashout_cli(
        ['Kurt Kitayama=12.40,Tommy Fleetwood=7.10', 'bad', 'Fleetwood:8']
    )
    by = {n: a for n, a in pairs}
    assert by["Kurt Kitayama"] == 12.40
    assert by["Tommy Fleetwood"] == 7.10
    assert by["Fleetwood"] == 8.0
    assert any("ignored cash-out fragment" in w for w in warn)


def test_bind_last_name_and_unmatched():
    positions = [
        _pos(player_id="10364", player_name="Kurt Kitayama"),
        _pos(player_id="5539", player_name="Tommy Fleetwood", stake=8.75, decimal_odds=9.5),
    ]
    pairs, _ = parse_cashout_cli("Kitayama=12.40,Fleetwood=7.10,Nobody=3")
    bound, warn = bind_cashout_quotes(pairs, positions)
    assert bound["10364"] == 12.40
    assert bound["5539"] == 7.10
    assert any("Nobody" in w for w in warn)


def test_bind_player_id():
    positions = [_pos(player_id="10364", player_name="Kurt Kitayama")]
    bound, warn = bind_cashout_quotes([("10364", 11.0)], positions)
    assert bound == {"10364": 11.0}
    assert not warn


def test_compare_point_mass_selective_needs_buffer():
    # 8.75 * 19 * 0.089 = 14.79875; 10% bar = 16.2786
    low = compare_cashout(
        stake=8.75,
        decimal_odds=19.0,
        live_model_p=0.089,
        live_model_low=0.089,
        live_model_high=0.089,
        quote=16.00,
        mode=StrategyMode.STAY_SELECTIVE,
    )
    high = compare_cashout(
        stake=8.75,
        decimal_odds=19.0,
        live_model_p=0.089,
        live_model_low=0.089,
        live_model_high=0.089,
        quote=16.28,
        mode=StrategyMode.STAY_SELECTIVE,
    )
    assert low.beats_hold is False
    assert high.beats_hold is True
    assert abs(low.hold_central - (8.75 * 19.0 * 0.089)) < 1e-9


def test_compare_wide_interval_uses_high_end():
    # high 0.18 -> hold high = 8.75*19*0.18 = 29.925; that becomes the sell bar
    cmp = compare_cashout(
        stake=8.75,
        decimal_odds=19.0,
        live_model_p=0.089,
        live_model_low=0.04,
        live_model_high=0.18,
        quote=20.00,
        mode=StrategyMode.STAY_SELECTIVE,
    )
    assert cmp.beats_hold is False
    fat = compare_cashout(
        stake=8.75,
        decimal_odds=19.0,
        live_model_p=0.089,
        live_model_low=0.04,
        live_model_high=0.18,
        quote=29.93,
        mode=StrategyMode.STAY_SELECTIVE,
    )
    assert fat.beats_hold is True


def test_protect_sells_at_central_ev():
    cmp = compare_cashout(
        stake=8.75,
        decimal_odds=19.0,
        live_model_p=0.089,
        live_model_low=0.089,
        live_model_high=0.089,
        quote=14.80,
        mode=StrategyMode.PROTECT_PROFITS,
    )
    assert cmp.beats_hold is True


def test_action_exits_when_quote_beats_hold():
    row = _row("10364", "Kurt Kitayama", 0.089, posted=19.0, edge=0.04, low=0.089, high=0.089)
    pos = _pos()
    mark = mark_position(pos, row, cashout_quote=20.0, mode=StrategyMode.STAY_SELECTIVE)
    assert mark.mtm_is_cashout is True
    assert mark.mtm_value == 20.0
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    act = _action_for_open(mark, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.EXIT
    assert "cash-out" in act.reason.lower()
    assert act.cashout_quote == 20.0


def test_action_holds_when_quote_loses_even_if_edge_collapsed():
    row = _row("10364", "Kurt Kitayama", 0.089, posted=19.0, edge=-0.02, low=0.089, high=0.089)
    pos = _pos()
    mark = mark_position(pos, row, cashout_quote=5.0, mode=StrategyMode.STAY_SELECTIVE)
    mark = mark.model_copy(update={"original_edge_collapsed": True, "live_edge": -0.02})
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    act = _action_for_open(mark, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.HOLD
    assert "below remaining winner" in act.reason.lower()


def test_without_quote_collapsed_still_exits():
    row = _row("10364", "Kurt Kitayama", 0.02, posted=19.0, edge=-0.05)
    pos = _pos()
    mark = mark_position(pos, row)
    mark = mark.model_copy(update={"original_edge_collapsed": True, "live_edge": -0.05, "is_runner": False})
    cfg = StrategyConfig(enabled=True, mode=StrategyMode.STAY_SELECTIVE, bankroll=250)
    act = _action_for_open(mark, pos, cfg, cooling=False)
    assert act.kind == StrategyActionKind.EXIT
    assert "collapsed" in act.reason.lower()


def test_paper_apply_cashout_posts_pnl(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, posted=19.0, edge=0.044)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    pos = rec.book.positions[0]
    before_ledger = load_ledger()
    quote = round(pos.stake + 3.65, 2)
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-exit-1",
                kind="exit",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-pos.stake,
                cashout_quote=quote,
                hold_expected_payout=14.80,
                reason_plain="Take the quote.",
                amount_plain="cash-out",
            )
        ],
    )
    assert rec.book.positions == []
    led = load_ledger()
    assert led.betting_pnl == round(quote - pos.stake, 2)
    assert led.bankroll == round(before_ledger.bankroll + (quote - pos.stake), 2)
    assert any(e.kind == "cashout" for e in led.entries)
    assert rec.bankroll == led.bankroll


def test_paper_apply_exit_without_quote_returns_stake(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, posted=19.0, edge=0.044)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    pos = rec.book.positions[0]
    before = load_ledger()
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-exit-2",
                kind="exit",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-pos.stake,
                reason_plain="Collapsed.",
                amount_plain="return stake",
            )
        ],
    )
    assert rec.book.positions == []
    led = load_ledger()
    assert led.betting_pnl == before.betting_pnl
    assert led.bankroll == before.bankroll


def test_estimated_cashout_offer_haircut_and_missing_live():
    assert estimated_cashout_offer(3.06, 19.0, 15.0) == 3.71
    assert estimated_cashout_offer(2.00, 19.0, 25.0) == 1.62
    assert estimated_cashout_offer(3.06, 19.0, None) is None
    assert estimated_cashout_offer(3.06, 19.0, 1.0) is None
    assert estimated_cashout_offer(0.0, 19.0, 15.0) is None


def _lock_kita(event_id="401811962"):
    rows = [_row("kita", "Kurt Kitayama", 0.089, posted=19.0, edge=0.044)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    return lock_paper_positions(rows, cfg, event_id=event_id, run_id="run-a", odds_book="bovada")


def test_paper_reduce_live_shorten_books_estimated_benefit(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = _lock_kita()
    pos = rec.book.positions[0]
    before_ledger = load_ledger()
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-reduce-short",
                kind="reduce",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-3.06,
                decimal_odds=15.0,
                reason_plain="Sell part of this paper ticket.",
                amount_plain="Sell $3.06 of the ticket.",
            )
        ],
    )
    remaining = rec.book.positions[0]
    sold = round(pos.stake - remaining.stake, 2)
    assert remaining.decimal_odds == pos.decimal_odds
    offered = estimated_cashout_offer(sold, pos.decimal_odds, 15.0)
    assert offered is not None
    led = load_ledger()
    assert led.betting_pnl == round(before_ledger.betting_pnl + (offered - sold), 2)
    assert rec.bankroll == led.bankroll
    mv = rec.movements[-1]
    assert mv.cashout_estimated is True
    assert mv.cashout_quote == offered
    assert "estimated-cashout:move-reduce-short" in (led.entries[-1].note or "")


def test_paper_reduce_live_lengthen_books_estimated_penalty(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = _lock_kita()
    pos = rec.book.positions[0]
    before_ledger = load_ledger()
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-reduce-long",
                kind="reduce",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-2.0,
                decimal_odds=25.0,
                reason_plain="Sell part of this paper ticket.",
                amount_plain="Sell $2.00 of the ticket.",
            )
        ],
    )
    remaining = rec.book.positions[0]
    sold = round(pos.stake - remaining.stake, 2)
    offered = estimated_cashout_offer(sold, pos.decimal_odds, 25.0)
    assert offered is not None
    assert offered < sold
    led = load_ledger()
    assert led.betting_pnl == round(before_ledger.betting_pnl + (offered - sold), 2)
    assert rec.bankroll == led.bankroll


def test_paper_reduce_without_live_posted_stays_at_cost(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = _lock_kita()
    pos = rec.book.positions[0]
    before = load_ledger()
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-reduce-nocoupon",
                kind="reduce",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-2.0,
                reason_plain="Sell part of this paper ticket.",
                amount_plain="Sell $2.00 of the ticket.",
            )
        ],
    )
    led = load_ledger()
    assert led.betting_pnl == before.betting_pnl
    assert led.bankroll == before.bankroll
    assert rec.movements[-1].cashout_quote is None
    assert rec.book.positions[0].stake == round(pos.stake - 2.0, 2)


def test_typed_cashout_overrides_estimate_on_exit(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = _lock_kita()
    pos = rec.book.positions[0]
    before = load_ledger()
    quote = round(pos.stake + 5.00, 2)
    estimated = estimated_cashout_offer(pos.stake, pos.decimal_odds, 15.0)
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-exit-typed",
                kind="exit",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-pos.stake,
                decimal_odds=15.0,
                cashout_quote=quote,
                reason_plain="Take the quote.",
                amount_plain="cash-out",
            )
        ],
    )
    led = load_ledger()
    assert estimated is not None
    assert led.betting_pnl == round(before.betting_pnl + (quote - pos.stake), 2)
    assert led.betting_pnl != round(before.betting_pnl + (estimated - pos.stake), 2)
    assert rec.movements[-1].cashout_estimated is False
    assert rec.movements[-1].cashout_quote == quote
    assert "movement:move-exit-typed" in (led.entries[-1].note or "")


def test_backfill_estimated_cashout_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = _lock_kita()
    pos = rec.book.positions[0]
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="act-a93819fd26",
                kind="reduce",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-3.06,
                reason_plain="Sell part of this paper ticket.",
                amount_plain="Sell $3.06 of the ticket.",
            )
        ],
    )
    assert load_ledger().betting_pnl == 0
    remaining = rec.book.positions[0]
    sold = round(pos.stake - remaining.stake, 2)
    rec.movements[-1] = rec.movements[-1].model_copy(update={"decimal_odds": 15.0})
    rec = backfill_estimated_cashouts(rec)
    offered = estimated_cashout_offer(sold, pos.decimal_odds, 15.0)
    assert offered is not None
    led = load_ledger()
    assert led.betting_pnl == round(offered - sold, 2)
    assert remaining.stake == rec.book.positions[0].stake
    assert rec.book.positions[0].decimal_odds == pos.decimal_odds
    rec = backfill_estimated_cashouts(rec)
    led2 = load_ledger()
    assert led2.betting_pnl == led.betting_pnl
    assert sum(1 for e in led2.entries if e.kind == "cashout") == 1
    assert rec.bankroll == led2.bankroll

