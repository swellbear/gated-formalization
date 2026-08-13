from golf_offshoot.decision.layer import advise_bet
from golf_offshoot.demo import demo_field, demo_odds, demo_tournament
from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.models.enums import BetType, DecisionAction, Horizon
from golf_offshoot.pipeline import GolfOffshootPipeline


def test_pipeline_never_auto_bets_and_ranks():
    engine = BayesianEngine(sim=SimConfig(n_sims=500, seed=7))
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=None)
    t = demo_tournament()
    f = demo_field()
    result = pipe.run(t, f, market_quotes=demo_odds(f), persist=False)
    assert result.never_auto_bet is True
    assert len(result.ranked) == 20
    assert result.ranked[0].rank == 1
    assert result.ranked[0].probabilities.p(Horizon.WIN).central >= result.ranked[-1].probabilities.p(Horizon.WIN).central
    for row in result.ranked:
        assert row.reliability is not None
        assert row.explain is not None
        assert 0 <= row.reliability.score <= 1
        if row.decision:
            assert row.decision.never_auto_bet is True
            assert row.decision.requires_user_confirmation is True
            assert row.decision.action != "execute"


def test_advise_defaults_to_pass_without_edge():
    engine = BayesianEngine(sim=SimConfig(n_sims=400, seed=3))
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=None)
    result = pipe.run(demo_tournament(), demo_field(), persist=False)
    row = result.ranked[0]
    advice = advise_bet(row, BetType.WIN)
    assert advice.never_auto_bet
    assert advice.action in (DecisionAction.PASS, DecisionAction.CONSIDER, DecisionAction.STRONG_CONSIDER)
