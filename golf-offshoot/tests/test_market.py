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
    assert abs(sum(q.implied_fair or 0 for q in fair) - 1.0) < 1e-9
