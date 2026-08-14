from pathlib import Path

from golf_offshoot.models.enums import Horizon, RiskPreference, StrategyMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.strategy.paper_book import (
    PaperMovement,
    apply_advice,
    load_paper_book,
    lock_paper_positions,
    paper_candidates,
)


def _hp(horizon: Horizon, central: float, width: float = 0.04) -> HorizonProbability:
    lo = max(0.0, central - width / 2)
    hi = min(1.0, central + width / 2)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(
    pid: str,
    name: str,
    win: float,
    *,
    edge: float | None,
    posted: float | None,
    flags: list[str] | None = None,
    rel: float = 0.74,
) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    bundle = ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.0, theta_sd=1.0)
    posted_odds = {"win": posted} if posted else {}
    implied = {"win": 1.0 / posted} if posted else {}
    edges = {"win": edge} if edge is not None else {}
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=bundle,
        reliability=ReliabilityScore(
            player_id=pid, score=rel, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        edge_by_bet=edges,
        market_implied_by_bet=implied,
        posted_odds_by_bet=posted_odds,
        flags=list(flags or []),
    )


def test_paper_candidates_skip_flags_and_negative_posted():
    rows = [
        _row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0),
        _row("fleet", "Tommy Fleetwood", 0.121, edge=0.041, posted=9.5),
        _row("scott", "Adam Scott", 0.027, edge=0.017, posted=20.0, flags=["sparse_data"]),
        _row("thor", "Michael Thorbjornsen", 0.053, edge=0.04, posted=8.0, flags=["thin_sample_overconfidence"]),
        _row("scheff", "Scottie Scheffler", 0.113, edge=0.012, posted=7.5),  # posted_edge negative-ish
    ]
    names = [r.name for r in paper_candidates(rows)]
    assert "Kurt Kitayama" in names
    assert "Tommy Fleetwood" in names
    assert "Adam Scott" not in names
    assert "Michael Thorbjornsen" not in names
    assert names[0] == "Kurt Kitayama"


def test_lock_paper_book_persists_and_never_auto_bets(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [
        _row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0),
        _row("fleet", "Tommy Fleetwood", 0.121, edge=0.041, posted=9.5),
    ]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(
        rows,
        cfg,
        event_id="401811962",
        event_name="FedEx St. Jude Championship",
        run_id="test-run",
        odds_book="bovada",
    )
    assert rec.never_auto_bet is True
    assert rec.paper_observation_only is True
    assert rec.bankroll == 250
    assert len(rec.book.positions) == 2
    assert rec.book.open_exposure <= 250 * 0.20 + 1e-6
    for p in rec.book.positions:
        assert p.user_recorded is True
        assert p.proposed is False
        assert p.stake > 0
        assert "paper lock" in p.notes
    loaded = load_paper_book("401811962")
    assert loaded is not None
    assert len(loaded.positions) == 2
    assert loaded.session_label == "paper-250"
    assert rec.export_pdf
    assert "_paper_" in rec.export_pdf
    assert rec.export_pdf.endswith(".pdf")
    pdf_path = Path(rec.export_pdf)
    assert pdf_path.is_file()
    assert pdf_path.read_bytes().startswith(b"%PDF")
    html = Path(rec.export_html).read_text(encoding="utf-8")
    assert "Observation only" in html
    assert "sportsbook takes a cut" in html
    assert "1/decimal_odds" in html
    assert "Kurt Kitayama" in html
    assert "full-field" not in rec.export_pdf
    assert rec.movements
    assert all(m.kind == "lock" and m.status == "applied" for m in rec.movements)
    assert rec.latest_pack
    pack = Path(rec.latest_pack)
    assert (pack / "00_README.txt").is_file()
    assert (pack / "01_paper_tickets.pdf").is_file()
    explained = (pack / "02_bets_explained.pdf").read_bytes()
    assert explained.startswith(b"%PDF")
    html_x = (pack / "02_bets_explained.html").read_text(encoding="utf-8")
    assert "Why the amounts" in html_x
    assert "concentration rule" in html_x
    assert "Kurt Kitayama" in html_x
    assert "never auto-bet" in html_x.lower() or "Never auto-bet" in html_x
    assert (pack / "04_movements.json").is_file()


def test_lock_paper_book_writes_new_pdf_per_lock(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    first = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    second = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-b", odds_book="bovada")
    assert first.export_pdf != second.export_pdf
    assert Path(first.export_pdf).is_file()
    assert Path(second.export_pdf).is_file()
    assert "_paper_" in Path(first.export_pdf).name
    assert "_paper_" in Path(second.export_pdf).name
    assert first.latest_pack != second.latest_pack
    assert Path(first.latest_pack).is_dir()
    assert Path(second.latest_pack).is_dir()


def test_apply_paper_reduce_keeps_mock_and_never_auto_bets(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    pos = rec.book.positions[0]
    before = pos.stake
    advice = [
        PaperMovement(
            movement_id="move-reduce-1",
            kind="reduce",
            status="advised",
            player_id=pos.player_id,
            player_name=pos.player_name,
            position_id=pos.position_id,
            stake_before=before,
            stake_delta=-2.0,
            reason_plain="Sell part of this paper ticket.",
            amount_plain="Sell $2.00 of the ticket.",
        )
    ]
    rec = apply_advice(rec, advice)
    assert rec.never_auto_bet is True
    assert rec.book.positions[0].stake == round(before - 2.0, 2)
    assert rec.movements[-1].status == "applied"
    assert rec.movements[-1].kind == "reduce"


def test_paper_pack_copies_field_table(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    field_pdf = tmp_path / "exports" / "401811962_live_run-a.pdf"
    field_pdf.parent.mkdir(parents=True, exist_ok=True)
    field_pdf.write_bytes(b"%PDF-1.4 fake field table")
    rec = lock_paper_positions(
        rows,
        cfg,
        event_id="401811962",
        run_id="run-a",
        odds_book="bovada",
        extra_export_files=[field_pdf],
    )
    pack = Path(rec.latest_pack)
    copied = pack / "03_field_live.pdf"
    assert copied.is_file()
    assert copied.read_bytes().startswith(b"%PDF")
    readme = (pack / "00_README.txt").read_text(encoding="utf-8")
    assert "03_field_live.pdf" in readme
    assert "02_bets_explained.pdf" in readme
