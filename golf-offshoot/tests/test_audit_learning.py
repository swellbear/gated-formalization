from pathlib import Path

from golf_offshoot.audit.journal import load_audit, save_audit
from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.demo import demo_field, demo_odds, demo_tournament
from golf_offshoot.learning.loop import PlayerResult, evaluate_run
from golf_offshoot.pipeline import GolfOffshootPipeline


def test_audit_roundtrip(tmp_path: Path):
    engine = BayesianEngine(sim=SimConfig(n_sims=300, seed=9))
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=tmp_path)
    result = pipe.run(demo_tournament(), demo_field(), market_quotes=demo_odds(demo_field()), persist=True)
    files = list(tmp_path.glob("*.json"))
    assert files
    loaded = load_audit(files[0])
    assert loaded.run_id == result.run_id
    assert loaded.model.version_id.startswith("golf-offshoot-")
    assert loaded.data_snapshot_hash


def test_learning_brier_defined():
    engine = BayesianEngine(sim=SimConfig(n_sims=300, seed=4))
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=None)
    result = pipe.run(demo_tournament(), demo_field(), persist=False)
    winner = result.ranked[0].player_id
    results = [
        PlayerResult(player_id=r.player_id, won=(r.player_id == winner), made_cut=True)
        for r in result.ranked
    ]
    report = evaluate_run(result.audit, results)
    assert report.n == 20
    assert 0 <= report.brier_win <= 1
