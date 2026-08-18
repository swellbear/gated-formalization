from golf_offshoot.market.odds import american_to_decimal, decimal_to_implied, remove_overround
from golf_offshoot.models.enums import BetType
from golf_offshoot.models.schemas import MarketQuote


def test_american_and_overround():
    assert abs(american_to_decimal(-110) - 1.909090) < 0.01
    assert abs(decimal_to_implied(2.0) - 0.5) < 1e-9
    quotes = [
        MarketQuote(player_id="a", bet_type=BetType.WIN, decimal_odds=2.0),
        MarketQuote(player_id="b", bet_type=BetType.WIN, decimal_odds=2.0),
    ]
    fair, tot = remove_overround(quotes, BetType.WIN)
    assert abs(tot - 1.0) < 1e-9
def test_opening_quotes_are_not_dejuiced_into_current_book():
    from golf_offshoot.market.odds import build_market_snapshot, edges_for_player
    from golf_offshoot.models.enums import Horizon
    from golf_offshoot.models.schemas import HorizonProbability, ProbabilityBundle

    quotes = [
        MarketQuote(
            player_id="a",
            bet_type=BetType.WIN,
            decimal_odds=5.0,
            implied_raw=0.2,
            book="bovada_live",
            line_role="current",
        ),
        MarketQuote(
            player_id="a",
            bet_type=BetType.WIN,
            decimal_odds=8.0,
            implied_raw=0.125,
            book="bovada",
            line_role="opening",
        ),
    ]
    snap = build_market_snapshot("t", quotes)
    current = [q for q in snap.quotes if q.line_role != "opening"]
    assert len(current) == 1
    assert current[0].decimal_odds == 5.0
    assert "a:win" in snap.movement_vs_open
    bundle = ProbabilityBundle(
        player_id="a",
        theta_mean=0.0,
        theta_sd=1.0,
        horizons={
            Horizon.WIN: HorizonProbability(horizon=Horizon.WIN, central=0.25, low=0.1, high=0.4),
        },
    )
    edge, implied, posted, bids = edges_for_player(bundle, snap)
    assert posted["win"] == 5.0
    assert bids == {}
    assert abs(implied["win"] - 1.0) < 1e-9  # single current quote, fair=1 after de-juice

