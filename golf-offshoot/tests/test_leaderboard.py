from pathlib import Path

from golf_offshoot.audit.journal import build_audit
from golf_offshoot.demo import demo_tournament
from golf_offshoot.models.enums import Horizon, RiskPreference, RunMode, StrategyMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore, TournamentRunResult
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.ranking.export_leaderboard import export_live_leaderboard
from golf_offshoot.ranking.leaderboard import (
    format_leaderboard,
    format_thru,
    format_to_par,
    leaderboard_view,
)
from golf_offshoot.strategy.paper_book import lock_paper_positions
from golf_offshoot.strategy.paper_pack import _field_pack_name, _pack_pdf_sources


def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    lo = max(0.0, central - 0.01)
    hi = min(1.0, central + 0.01)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(
    pid: str,
    name: str,
    win: float,
    *,
    place: int | None = None,
    place_disp: str = "",
    score: float | None = None,
    holes: int = 0,
    withdrawn: bool = False,
    cut: bool | None = None,
    status: str = "",
) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    bundle = ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.0, theta_sd=1.0)
    rel = ReliabilityScore(
        player_id=pid, score=0.7, data_density=0.5, data_quality=0.5, input_stability=0.5
    )
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=bundle,
        reliability=rel,
        live_score_to_par=score,
        live_holes_completed=holes,
        live_place=place,
        live_place_display=place_disp,
        live_status_name=status,
        live_made_cut=cut,
        withdrawn=withdrawn,
    )


def test_thru_and_score_display():
    assert format_to_par(-8) == "-8"
    assert format_to_par(0) == "E"
    assert format_to_par(2) == "+2"
    assert format_to_par(None) == "-"
    assert format_thru(6, 4) == "6"
    assert format_thru(18, 4) == "F"
    assert format_thru(24, 4) == "6"
    assert format_thru(72, 4) == "F"
    assert format_thru(12, 4, withdrawn=True) == "-"
    assert format_thru(36, 4, missed_cut=True) == "-"


def test_leaderboard_sorts_by_place_not_win():
    rows = [
        _row("a", "High Win", 0.20, place=12, place_disp="12", score=1, holes=18),
        _row("b", "Leader", 0.05, place=1, place_disp="1", score=-8, holes=18),
        _row("c", "Tied", 0.08, place=3, place_disp="T3", score=-4, holes=14),
        _row("d", "Withdrawn", 0.01, place=None, score=None, holes=5, withdrawn=True, status="STATUS_WITHDRAW"),
        _row("e", "Missed", 0.02, place=60, place_disp="CUT", score=4, holes=36, cut=False, status="STATUS_CUT"),
    ]
    view = leaderboard_view(rows, n_rounds=4, held_ids={"b"})
    names = [r[1] for r in view.rows]
    assert names[:3] == ["Leader", "Tied", "High Win"]
    assert names[-2:] == ["Missed", "Withdrawn"]
    leader = view.rows[0]
    assert leader[0] == "1"
    assert leader[2] == "-8"
    assert leader[3] == "F"
    assert leader[6] == "paper"
    tied = view.rows[1]
    assert tied[0] == "T3"
    assert tied[3] == "14"
    text = format_leaderboard(rows, held_ids={"b"})
    assert "Leader" in text
    assert "paper" in text


def test_export_leaderboard_live_only(tmp_path):
    rows = [_row("b", "Leader", 0.05, place=1, place_disp="1", score=-8, holes=18)]
    t = demo_tournament()
    live_audit = build_audit(t.tournament_id, RunMode.LIVE, rows, "h")
    live = TournamentRunResult(
        run_id=live_audit.run_id,
        tournament=t,
        mode=RunMode.LIVE,
        ranked=rows,
        audit=live_audit,
    )
    paths = export_live_leaderboard(live, held_ids={"b"}, directory=tmp_path)
    assert paths is not None
    assert paths.pdf.is_file()
    assert paths.pdf.read_bytes().startswith(b"%PDF")
    assert "leaderboard" in paths.pdf.name
    html = paths.html.read_text(encoding="utf-8")
    assert "Leader" in html
    assert "printed" in html
    txt = paths.txt.read_text(encoding="utf-8")
    assert "-8" in txt
    assert "printed" in txt
    assert "not the model ranking" in html.lower() or "Not model Win%" in html
    txt = paths.txt.read_text(encoding="utf-8")
    assert "-8" in txt
    pre_audit = build_audit(t.tournament_id, RunMode.PRE_TOURNAMENT, rows, "h")
    pre = TournamentRunResult(
        run_id=pre_audit.run_id,
        tournament=t,
        mode=RunMode.PRE_TOURNAMENT,
        ranked=rows,
        audit=pre_audit,
    )
    assert export_live_leaderboard(pre, directory=tmp_path) is None


def test_field_pack_name_does_not_clobber_leaderboard():
    live = Path("401811962_live_run-a.pdf")
    board = Path("401811962_live_run-a_leaderboard.pdf")
    assert _field_pack_name(live) == "03_field_live.pdf"
    assert _field_pack_name(board) == "03_leaderboard.pdf"


def test_paper_pack_puts_leaderboard_before_model_table(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [
        _row("kita", "Kurt Kitayama", 0.089, place=4, place_disp="T4", score=-6, holes=18),
        _row("fleet", "Tommy Fleetwood", 0.121, place=8, place_disp="T8", score=-3, holes=14),
    ]
    t = demo_tournament()
    audit = build_audit(t.tournament_id, RunMode.LIVE, rows, "h")
    result = TournamentRunResult(
        run_id="run-a",
        tournament=t,
        mode=RunMode.LIVE,
        ranked=rows,
        audit=audit,
    )
    export_dir = tmp_path / "exports"
    lb = export_live_leaderboard(result, held_ids={"kita"}, directory=export_dir)
    field_pdf = export_dir / "401811962_live_run-a.pdf"
    field_pdf.write_bytes(lb.pdf.read_bytes())
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(
        [
            PlayerOutput(
                player_id="kita",
                name="Kurt Kitayama",
                rank=1,
                probabilities=rows[0].probabilities,
                reliability=rows[0].reliability,
                edge_by_bet={"win": 0.044},
                market_implied_by_bet={"win": 1 / 17.0},
                posted_odds_by_bet={"win": 17.0},
            )
        ],
        cfg,
        event_id="401811962",
        run_id="run-a",
        odds_book="bovada",
        extra_export_files=[lb.pdf, field_pdf],
    )
    pack = Path(rec.latest_pack)
    assert (pack / "03_leaderboard.pdf").is_file()
    assert (pack / "03_field_live.pdf").is_file()
    names = [p.name for p, _ in _pack_pdf_sources(pack)]
    assert names.index("03_leaderboard.pdf") < names.index("03_field_live.pdf")
    if "05_bankroll.pdf" in names:
        assert names[-1] == "05_bankroll.pdf"
    readme = (pack / "00_README.txt").read_text(encoding="utf-8")
    assert "03_leaderboard.pdf" in readme
    combo = pack / "00_full_readout.pdf"
    assert combo.is_file()
    from pypdf import PdfReader

    text = "\n".join((page.extract_text() or "") for page in PdfReader(str(combo)).pages)
    assert "leaderboard" in text.lower() or "ToPar" in text or "Kurt Kitayama" in text


def test_pack_sources_bankroll_is_last(tmp_path):
    for name in (
        "00_trigger.pdf",
        "01_paper_tickets.pdf",
        "03_field_live.pdf",
        "03_zzz_extra.pdf",
        "05_bankroll.pdf",
    ):
        (tmp_path / name).write_bytes(b"%PDF-1.4\n")
    names = [p.name for p, _ in _pack_pdf_sources(tmp_path)]
    assert names[-1] == "05_bankroll.pdf"
    assert names.index("03_zzz_extra.pdf") < names.index("05_bankroll.pdf")
