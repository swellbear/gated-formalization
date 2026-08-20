from golf_offshoot.data_feeds.polymarket import quotes_from_event, yes_bid
from golf_offshoot.models.enums import BetType, Horizon, StrategyMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id
from golf_offshoot.strategy.cashout import bid_cashout_dollars, min_sell_price
from golf_offshoot.strategy.fills import FillError, parse_fill_market, record_polymarket_fill
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement, save_paper_book
from golf_offshoot.strategy.paper_trigger import group_trigger_actions, trigger_document
from golf_offshoot.strategy.path import mark_position


def _hp(win: float) -> dict:
    return {
        Horizon.WIN: HorizonProbability(horizon=Horizon.WIN, central=win, low=max(0.0, win - 0.02), high=min(1.0, win + 0.02)),
        Horizon.TOP_5: HorizonProbability(horizon=Horizon.TOP_5, central=min(1.0, win * 3), low=0.0, high=1.0),
        Horizon.TOP_10: HorizonProbability(horizon=Horizon.TOP_10, central=min(1.0, win * 5), low=0.0, high=1.0),
        Horizon.MAKE_CUT: HorizonProbability(horizon=Horizon.MAKE_CUT, central=1.0, low=1.0, high=1.0),
    }


def test_yes_bid_is_not_ask():
    assert yes_bid({"bestBid": 0.03, "bestAsk": 0.05}) == 0.03
    assert yes_bid({"bestBidQuote": {"value": "0.2220", "currency": "USD"}}) == 0.222
    assert yes_bid({"bestBid": 0.0, "bestAsk": 0.05}) is None
    assert yes_bid({"bestAsk": 0.05}) is None


def test_quotes_carry_bid_without_synthesizing():
    event = {
        "markets": [
            {
                "groupItemTitle": "Scottie Scheffler",
                "question": "Will Scottie Scheffler win the 2026 BMW Championship?",
                "sportsMarketType": "moneyline",
                "bestAsk": 0.20,
                "bestBid": 0.18,
                "closed": False,
            }
        ]
    }
    quotes, _um, _seen = quotes_from_event(event, {"Scottie Scheffler": "id-ss"})
    assert quotes[0].implied_raw == 0.20
    assert quotes[0].bid_raw == 0.18
    assert quotes[0].decimal_odds == 5.0


def test_bid_cashout_and_min_sell():
    assert bid_cashout_dollars(50, 0.041) == 2.05
    assert bid_cashout_dollars(50, None) is None
    assert min_sell_price(2.60, 50) == 0.052
    assert min_sell_price(2.60, 0) is None


def test_parse_fill_market():
    assert parse_fill_market("top 10") == BetType.TOP_10
    assert parse_fill_market("win_after_r1") == BetType.WIN_AFTER_R1
    assert parse_fill_market("after round 2") == BetType.WIN_AFTER_R2
    assert parse_fill_market("r3") == BetType.WIN_AFTER_R3
    try:
        parse_fill_market("2-ball")
    except FillError:
        return
    raise AssertionError("expected FillError")


def test_record_fill_replaces_observation_not_ledger(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    obs = StrategyPosition(
        position_id="paper-obs",
        player_id="id-mf",
        player_name="Matt Fitzpatrick",
        bet_type=BetType.WIN,
        stake=2.19,
        decimal_odds=29.41,
        entry_edge=0.023,
        entry_model_p=0.036,
        notes="paper lock [observation]",
    )
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250,
        starting_bankroll=250,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(bankroll=250, positions=[obs]),
    )
    save_paper_book(rec)
    out = record_polymarket_fill(
        event_id="401811963",
        player_name="Matt Fitzpatrick",
        shares=50,
        fill=0.034,
        cost=1.80,
    )
    assert out.path_id == "polymarket"
    assert out.independent_bankroll is True
    assert len(out.book.positions) == 1
    pos = out.book.positions[0]
    assert pos.position_id == "paper-obs"
    assert pos.shares == 50
    assert pos.stake == 1.80
    assert abs(pos.decimal_odds - (50 / 1.80)) < 1e-9
    assert abs(pos.entry_model_p - 0.036) < 1e-9
    assert abs(pos.entry_edge - 0.023) < 1e-9
    assert pos.fill_price == 0.034
    assert not (tmp_path / "paper" / "ledger.json").is_file()
    assert (tmp_path / "paper" / "401811963_polymarket.json").is_file()
    assert pos.intent == "hold"


def test_record_fill_can_add_flip_without_touching_hold(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    hold = StrategyPosition(
        position_id="paper-hold",
        player_id="id-mf",
        player_name="Matt Fitzpatrick",
        bet_type=BetType.WIN,
        stake=2.19,
        decimal_odds=28.64,
        entry_edge=0.023,
        entry_model_p=0.036,
        shares=62.72,
        fill_price=0.0349,
        cost_usd=2.19,
        intent="hold",
        user_recorded=True,
    )
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250,
        starting_bankroll=250,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(bankroll=250, positions=[hold]),
    )
    save_paper_book(rec)
    out = record_polymarket_fill(
        event_id="401811963",
        player_name="Russell Henley",
        shares=114.99,
        fill=2.19 / 114.99,
        cost=2.19,
        market="win_after_r2",
        player_id="id-rh",
        intent="flip",
    )
    names = {p.player_name: p for p in out.book.positions}
    assert names["Matt Fitzpatrick"].intent == "hold"
    assert names["Matt Fitzpatrick"].shares == 62.72
    assert names["Russell Henley"].intent == "flip"
    assert names["Russell Henley"].bet_type == BetType.WIN_AFTER_R2
    assert names["Russell Henley"].cost_usd == 2.19
    assert abs(names["Russell Henley"].shares - 114.99) < 1e-9


def test_fill_prefers_ntfy_add_over_new_and_adds_shares(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    held = StrategyPosition(
        position_id="paper-gw",
        player_id="name:gary-woodland",
        player_name="Gary Woodland",
        bet_type=BetType.WIN_AFTER_R1,
        stake=0.50,
        decimal_odds=2.5,
        entry_edge=0.15,
        entry_model_p=0.56,
        entry_market_p=0.41,
        shares=1.25,
        fill_price=0.40,
        cost_usd=0.50,
        intent="hold",
        user_recorded=True,
    )
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250,
        starting_bankroll=250,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        latest_advice=[
            PaperMovement(
                movement_id="a1",
                kind="new_bet",
                player_id="3550",
                player_name="Gary Woodland",
                bet_type="win_after_r1",
                intent="hold",
                model_win=0.56,
            ),
            PaperMovement(
                movement_id="a2",
                kind="add",
                player_id="3550",
                player_name="Gary Woodland",
                bet_type="win_after_r1",
                intent="hold",
                model_win=0.56,
                posted_edge=0.15,
            ),
        ],
        book=PortfolioState(bankroll=250, positions=[held]),
    )
    save_paper_book(rec)
    out = record_polymarket_fill(
        event_id="401811963",
        player_name="Gary Woodland",
        shares=0.27,
        fill=0.44,
        cost=0.12,
        market="win_after_r1",
        ranked_names={"Gary Woodland": "3550"},
    )
    assert len(out.book.positions) == 1
    pos = out.book.positions[0]
    assert pos.player_id == "3550"
    assert pos.intent == "hold"
    assert abs(pos.shares - 1.52) < 1e-9
    assert pos.cost_usd == 0.62
    assert pos.position_id == "paper-gw"
    assert any(m.kind == "fill_add" for m in out.movements)
    assert "last ntfy ADD" in out.notes[-1]


def test_fill_add_on_observation_replaces_stub(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    obs = StrategyPosition(
        position_id="paper-obs",
        player_id="3550",
        player_name="Gary Woodland",
        bet_type=BetType.WIN_AFTER_R1,
        stake=0.53,
        decimal_odds=2.44,
        entry_edge=0.15,
        entry_model_p=0.56,
        notes="paper lock [observation]",
        intent="hold",
    )
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250,
        starting_bankroll=250,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(bankroll=250, positions=[obs]),
    )
    save_paper_book(rec)
    out = record_polymarket_fill(
        event_id="401811963",
        player_name="Gary Woodland",
        shares=0.27,
        fill=0.44,
        cost=0.12,
        market="win_after_r1",
        pulls=[
            {
                "kind": "add",
                "player_id": "3550",
                "player_name": "Gary Woodland",
                "bet_type": "win_after_r1",
                "intent": "hold",
                "model_win": 0.56,
                "posted_edge": 0.15,
            }
        ],
    )
    pos = out.book.positions[0]
    assert pos.shares == 0.27
    assert pos.cost_usd == 0.12
    assert pos.intent == "hold"
    assert abs(pos.entry_model_p - 0.56) < 1e-9
    assert pos.position_id == "paper-obs"


def test_fill_add_uses_pull_hold_not_guessed_flip(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    obs = StrategyPosition(
        position_id="paper-obs",
        player_id="name:gary-woodland",
        player_name="Gary Woodland",
        bet_type=BetType.WIN_AFTER_R1,
        stake=0.53,
        decimal_odds=2.44,
        entry_edge=0.0,
        entry_model_p=0.44,
        notes="wrongly tagged flip",
        intent="flip",
    )
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250,
        starting_bankroll=250,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(bankroll=250, positions=[obs]),
    )
    save_paper_book(rec)
    out = record_polymarket_fill(
        event_id="401811963",
        player_name="Gary Woodland",
        shares=0.27,
        fill=0.44,
        cost=0.12,
        market="win_after_r1",
        ranked_names={"Gary Woodland": "3550"},
        pulls=[
            {
                "kind": "add",
                "player_id": "3550",
                "player_name": "Gary Woodland",
                "bet_type": "win_after_r1",
                "intent": "hold",
                "model_win": 0.56,
                "posted_edge": 0.15,
            }
        ],
    )
    pos = out.book.positions[0]
    assert pos.player_id == "3550"
    assert pos.intent == "hold"
    assert pos.shares == 0.27


def test_mark_position_uses_bid_unless_typed():
    pos = StrategyPosition(
        position_id=new_id("fill"),
        player_id="id-mf",
        player_name="Matt Fitzpatrick",
        bet_type=BetType.WIN,
        stake=1.80,
        decimal_odds=50 / 1.80,
        entry_edge=0.0,
        entry_model_p=0.034,
        shares=50,
        fill_price=0.034,
        cost_usd=1.80,
    )
    row = PlayerOutput(
        player_id="id-mf",
        name="Matt Fitzpatrick",
        rank=3,
        probabilities=ProbabilityBundle(player_id="id-mf", horizons=_hp(0.036), theta_mean=0.0, theta_sd=1.0),
        reliability=ReliabilityScore(
            player_id="id-mf", score=0.70, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        posted_odds_by_bet={"win": 29.41},
        bid_by_bet={"win": 0.041},
        edge_by_bet={"win": 0.023},
    )
    mark = mark_position(pos, row, mode=StrategyMode.STAY_SELECTIVE)
    assert mark.mtm_is_bid is True
    assert mark.cashout_quote == 2.05
    assert mark.live_bid == 0.041
    assert mark.min_sell_price is not None
    typed = mark_position(pos, row, cashout_quote=3.00, mode=StrategyMode.STAY_SELECTIVE)
    assert typed.mtm_is_bid is False
    assert typed.cashout_quote == 3.00


def test_trigger_shows_bid_and_min_sell():
    mv = PaperMovement(
        movement_id=new_id("mv"),
        kind="hold",
        status="advised",
        player_name="Matt Fitzpatrick",
        bet_type="win",
        live_bid=0.041,
        min_sell_price=0.052,
        cashout_quote=2.05,
        mtm_is_bid=True,
    )
    sections = group_trigger_actions([mv])
    extra = sections[0].rows[0].extra
    assert "bid 0.041" in extra
    assert "min-sell 0.052" in extra
    assert "offer $2.05" in extra


def test_trigger_fill_tape_is_display_not_sell():
    from golf_offshoot.models.enums import BetType
    from golf_offshoot.models.strategy import StrategyPosition

    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250,
        book=PortfolioState(
            bankroll=250,
            positions=[
                StrategyPosition(
                    position_id="fill-1",
                    player_id="id-mf",
                    player_name="Matt Fitzpatrick",
                    bet_type=BetType.WIN,
                    stake=2.19,
                    decimal_odds=28.64,
                    entry_edge=0.023,
                    entry_model_p=0.036,
                    shares=62.72,
                    fill_price=0.0349,
                    cost_usd=2.19,
                )
            ],
        ),
    )
    advice = [
        PaperMovement(
            movement_id=new_id("mv"),
            kind="hold",
            status="advised",
            player_id="id-mf",
            player_name="Matt Fitzpatrick",
            bet_type="win",
            live_bid=0.033,
            min_sell_price=0.063,
            cashout_quote=2.07,
            hold_expected_payout=2.89,
            mtm_is_bid=True,
        )
    ]
    text = trigger_document(rec, advice=advice)
    assert "FILL TAPE" in text
    assert "Matt Fitzpatrick" in text
    assert "cost $2.19" in text
    assert "offer $2.07" in text
    assert "keep-to-win $2.89" in text
    assert "no pop" in text
    assert "not a sell" in text.lower()
