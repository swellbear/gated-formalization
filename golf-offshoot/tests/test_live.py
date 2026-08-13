from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.demo import demo_field, demo_tournament
from golf_offshoot.models.enums import RunMode
from golf_offshoot.pipeline import GolfOffshootPipeline


def test_live_rerun_changes_mode_and_can_diff():
    engine = BayesianEngine(sim=SimConfig(n_sims=350, seed=11))
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=None)
    t = demo_tournament()
    pre = pipe.run(t, demo_field(), persist=False)
    live_field = demo_field()
    for i, p in enumerate(live_field.players):
        p.live_score_to_par = -3 + i * 0.4
        p.live_holes_completed = 18
    live = pipe.rerun_live(t, live_field, previous=pre.audit, market_quotes=None)
    assert live.mode == RunMode.LIVE
    assert live.audit.previous_run_id == pre.run_id
    assert any("live_position" in p.factors for p in live_field.players)
