from golf_offshoot.bayesian_engine.updates import ThetaState
from golf_offshoot.decision.layer import advise_bet
from golf_offshoot.flags.bias import COURSE_HISTORY_MISSING, PLAYER_HARD_PASS_FLAGS, flag_player
from golf_offshoot.models.enums import BetType, DecisionAction, Horizon
from golf_offshoot.models.schemas import (
    HorizonProbability,
    Player,
    PlayerInputs,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
)


def _theta() -> ThetaState:
    return ThetaState(mean=0.0, variance=1.0)


def _bundle(pid: str, *, central: float, width: float) -> ProbabilityBundle:
    lo = max(0.0, central - width / 2)
    hi = min(1.0, central + width / 2)
    return ProbabilityBundle(
        player_id=pid,
        horizons={
            Horizon.WIN: HorizonProbability(horizon=Horizon.WIN, central=central, low=lo, high=hi),
        },
        theta_mean=0.0,
        theta_sd=1.0,
    )


def _inputs(*, lesser: bool, course_rounds: int, name: str = "Scottie Scheffler") -> PlayerInputs:
    return PlayerInputs(
        player=Player(player_id="id-1", name=name, is_lesser_known=lesser),
        course_history_rounds=course_rounds,
    )


def _row(*, flags: list[str], win: float = 0.14, edge: float = 0.06, posted: float = 10.0) -> PlayerOutput:
    bundle = _bundle("id-1", central=win, width=0.04)
    return PlayerOutput(
        player_id="id-1",
        name="Scottie Scheffler",
        rank=1,
        probabilities=bundle,
        reliability=ReliabilityScore(
            player_id="id-1", score=0.70, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        edge_by_bet={"win": edge},
        market_implied_by_bet={"win": 1.0 / posted},
        posted_odds_by_bet={"win": posted},
        flags=list(flags),
    )


def test_known_player_missing_venue_is_not_sparse():
    flags = flag_player(
        _inputs(lesser=False, course_rounds=0),
        _theta(),
        _bundle("id-1", central=0.14, width=0.03),
    )
    assert COURSE_HISTORY_MISSING in flags
    assert "sparse_data" not in flags
    assert "thin_sample_overconfidence" not in flags
    assert not PLAYER_HARD_PASS_FLAGS.intersection(flags)


def test_lesser_known_stays_sparse_hard_pass():
    flags = flag_player(
        _inputs(lesser=True, course_rounds=0, name="Player 7"),
        _theta(),
        _bundle("name:player-7", central=0.015, width=0.02),
    )
    assert "sparse_data" in flags
    assert COURSE_HISTORY_MISSING not in flags


def test_lesser_known_tight_favorite_is_overconfident():
    flags = flag_player(
        _inputs(lesser=True, course_rounds=0, name="Player 7"),
        _theta(),
        _bundle("name:player-7", central=0.08, width=0.03),
    )
    assert "thin_sample_overconfidence" in flags
    assert "sparse_data" in flags


def test_known_player_with_course_rounds_has_no_course_flag():
    flags = flag_player(
        _inputs(lesser=False, course_rounds=8),
        _theta(),
        _bundle("id-1", central=0.14, width=0.03),
    )
    assert COURSE_HISTORY_MISSING not in flags
    assert "sparse_data" not in flags


def test_advise_does_not_veto_missing_venue_history():
    advice = advise_bet(_row(flags=[COURSE_HISTORY_MISSING]), BetType.WIN, decimal_odds=10.0)
    assert advice.action in (DecisionAction.CONSIDER, DecisionAction.STRONG_CONSIDER)
    assert any("not a ticket veto" in r for r in advice.reasons)


def test_advise_still_passes_sparse_data():
    advice = advise_bet(
        _row(flags=["sparse_data"], win=0.14, edge=0.06, posted=10.0),
        BetType.WIN,
        decimal_odds=10.0,
    )
    assert advice.action == DecisionAction.PASS
    assert any("sparse_data" in r for r in advice.reasons)
