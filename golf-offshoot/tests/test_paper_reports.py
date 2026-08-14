"""Full reports for players currently in the paper book."""

import json
from pathlib import Path

from golf_offshoot.__main__ import main
from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.demo import demo_field, demo_odds, demo_open_book, demo_tournament
from golf_offshoot.models.enums import RiskPreference, RunMode, StrategyMode
from golf_offshoot.models.strategy import PortfolioState, StrategyConfig
from golf_offshoot.pipeline import GolfOffshootPipeline
from golf_offshoot.ranking.report import format_player_report
from golf_offshoot.strategy.engine import run_strategy
from golf_offshoot.strategy.paper_reports import (
    format_paper_reports,
    load_portfolio_json,
    paper_reports_payload,
    paper_rows,
    recorded_positions,
    save_portfolio_json,
)


def _pipe(**kw):
    engine = BayesianEngine(sim=SimConfig(n_sims=400, seed=21))
    return GolfOffshootPipeline(engine=engine, snapshot_dir=None, **kw)


def test_full_report_covers_horizons_reliability_and_explain():
    pipe = _pipe()
    f = demo_field()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    row = result.ranked[0]
    inputs = next(p for p in f.players if p.player.player_id == row.player_id)
    text = format_player_report(row, inputs=inputs)
    assert row.name in text
    assert "Probabilities" in text
    assert "win" in text
    assert "make_cut" in text
    assert "Reliability:" in text
    assert "Explain:" in text
    assert "SG" in text
    assert row.explain.narrative.split(":")[0] in text or row.name in text


def test_paper_reports_only_include_book_players():
    cfg = StrategyConfig(
        enabled=True, mode=StrategyMode.STAY_SELECTIVE, risk=RiskPreference.NORMAL, bankroll=2000
    )
    pipe = _pipe(strategy_config=cfg)
    f = demo_field()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    book = demo_open_book(result, bankroll=2000, n=2)
    result.strategy = run_strategy(
        result.ranked, cfg, run_mode=RunMode.PRE_TOURNAMENT, field=f, book=book
    )
    text = format_paper_reports(result, book, field=f)
    ids = {p.player_id for p in book.positions}
    names = {r.name for r in result.ranked if r.player_id in ids}
    for name in names:
        assert name in text
    assert text.count("=== ") == len(ids)
    payload = paper_reports_payload(result, book, field=f)
    assert {p["player"]["player_id"] for p in payload["players"]} == ids
    assert payload["never_auto_bet"] is True


def test_empty_paper_explains_how_to_load():
    pipe = _pipe()
    f = demo_field()
    result = pipe.run(demo_tournament(), f, persist=False)
    empty = PortfolioState(bankroll=2000, session_label="empty")
    text = format_paper_reports(result, empty, field=f)
    assert "No players in the current paper" in text
    assert "--paper-file" in text or "--lock-paper" in text or "--demo-paper" in text


def test_roundtrip_paper_file(tmp_path: Path):
    pipe = _pipe()
    f = demo_field()
    result = pipe.run(demo_tournament(), f, market_quotes=demo_odds(f), persist=False)
    book = demo_open_book(result, bankroll=1500, n=1)
    path = tmp_path / "book.json"
    save_portfolio_json(book, path)
    loaded = load_portfolio_json(path)
    assert loaded.bankroll == 1500
    assert len(recorded_positions(loaded)) == 1
    assert loaded.positions[0].player_id == book.positions[0].player_id
    assert paper_rows(result.ranked, loaded.positions)[0].player_id == loaded.positions[0].player_id


def test_cli_paper_prints_recorded_players(capsys, tmp_path: Path):
    rc = main(["paper", "--demo-paper", "--sims", "400", "--write-paper", str(tmp_path / "demo.json")])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Paper reports" in out
    assert "never_auto_bet=True" in out
    assert "=== " in out
    assert "Probabilities" in out
    saved = json.loads((tmp_path / "demo.json").read_text())
    assert saved["positions"]
    rc = main(["paper", "--demo-paper", "--sims", "400", "--paper-file", str(tmp_path / "demo.json"), "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["players"]
    assert payload["players"][0]["player"]["explain"]
    assert payload["never_auto_bet"] is True


def test_cli_paper_missing_file_exits_2(capsys):
    rc = main(["paper", "--sims", "200", "--paper-file", "/no/such/paper.json"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not found" in err


def test_explain_uses_full_report(capsys):
    rc = main(["explain", "--player", "p01", "--sims", "400"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "--- full report ---" in out
    assert "Probabilities" in out
    assert "Reliability:" in out
