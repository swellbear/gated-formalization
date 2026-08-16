from pathlib import Path

from golf_offshoot.models.enums import BetType, Horizon, RiskPreference, RunMode, StrategyActionKind, StrategyMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.models.strategy import (
    PositionMark,
    PortfolioState,
    StrategyAction,
    StrategyConfig,
    StrategyPosition,
    StrategyRecommendation,
    StrategyStatusSummary,
    new_id,
)
from golf_offshoot.strategy.explanations import unmarked_ride_to_settle
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    advice_from_recommendation,
    apply_advice,
    load_paper_book,
    lock_paper_positions,
    paper_candidates,
    ticket_rows,
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
    place: int | None = None,
    place_disp: str = "",
    score: float | None = None,
    holes: int = 0,
) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.TOP_20: _hp(Horizon.TOP_20, min(1.0, win * 8)),
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
        live_place=place,
        live_place_display=place_disp,
        live_score_to_par=score,
        live_holes_completed=holes,
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
    cleared_only = [r.name for r in paper_candidates(rows, require_cleared=True)]
    assert cleared_only == ["Kurt Kitayama"]


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
    assert "Place" in html
    assert "printed" in html
    from pypdf import PdfReader

    pdf_text = "".join((p.extract_text() or "") for p in PdfReader(pdf_path).pages)
    assert "printed" in pdf_text
    assert "EDT" in pdf_text or "EST" in pdf_text
    assert "UTC" not in pdf_text
    assert "full-field" not in rec.export_pdf
    assert rec.movements
    assert all(m.kind == "lock" and m.status == "applied" for m in rec.movements)
    assert rec.latest_pack
    pack = Path(rec.latest_pack)
    assert (pack / "00_README.txt").is_file()
    assert (pack / "00_trigger.pdf").is_file()
    assert (pack / "01_paper_tickets.pdf").is_file()
    explained = (pack / "02_bets_explained.pdf").read_bytes()
    assert explained.startswith(b"%PDF")
    html_x = (pack / "02_bets_explained.html").read_text(encoding="utf-8")
    assert "Why the amounts" in html_x
    assert "When (ET)" in html_x
    assert "Entered" in html_x
    assert "Exited" in html_x
    assert "EDT" in html_x or "EST" in html_x
    assert "UTC" not in html_x
    assert "concentration rule" in html_x
    assert "Kurt Kitayama" in html_x
    assert "never auto-bet" in html_x.lower() or "Never auto-bet" in html_x
    assert (pack / "04_movements.json").is_file()


def test_movement_clocks_pair_entry_and_exit(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.strategy.paper_book import format_paper_time, movement_clocks

    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(
        [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)],
        cfg,
        event_id="401811962",
        write_exports=False,
        run_id="clk",
    )
    lock_mv = rec.movements[0]
    _when, entered, exited = movement_clocks(rec, lock_mv)
    assert exited == "open"
    assert entered == format_paper_time(lock_mv.at)
    pos = rec.book.positions[0]
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="exit-clk",
                kind="exit",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                bet_type="win",
                stake_delta=-pos.stake,
            )
        ],
    )
    exit_mv = next(m for m in rec.movements if m.kind == "exit")
    when, entered, exited = movement_clocks(rec, exit_mv)
    assert exited == when
    assert entered == format_paper_time(lock_mv.at)
    assert exited != "open"


def test_lock_sizes_cleared_full_unit_observation_quarter(tmp_path, monkeypatch):
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
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    by = {p.player_name: p for p in rec.book.positions}
    assert abs(by["Kurt Kitayama"].stake - 8.75) < 1e-9
    assert abs(by["Tommy Fleetwood"].stake - 2.19) < 0.02
    assert "[cleared]" in by["Kurt Kitayama"].notes
    assert "[observation]" in by["Tommy Fleetwood"].notes
    kita_mv = next(m for m in rec.movements if m.player_name == "Kurt Kitayama")
    fleet_mv = next(m for m in rec.movements if m.player_name == "Tommy Fleetwood")
    assert "[cleared]" in kita_mv.reason_plain
    assert "[observation]" in fleet_mv.reason_plain
    html = Path(rec.export_html).read_text(encoding="utf-8")
    assert "[cleared] Kurt Kitayama" in html
    assert "[observation] Tommy Fleetwood" in html


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


def test_pack_tickets_refresh_after_apply(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.strategy.paper_pack import write_paper_pack

    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    pos = rec.book.positions[0]
    lock_txt = (Path(rec.latest_pack) / "01_paper_tickets.txt").read_text(encoding="utf-8")
    assert "Kurt Kitayama" in lock_txt
    assert "Sungjae Im" not in lock_txt
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-reduce-1",
                kind="reduce",
                status="advised",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_before=pos.stake,
                stake_delta=-2.0,
                reason_plain="Sell part of this paper ticket.",
                amount_plain="Sell $2.00 of the ticket.",
            ),
            PaperMovement(
                movement_id="move-new-1",
                kind="new_bet",
                status="advised",
                player_id="im",
                player_name="Sungjae Im",
                bet_type="top_20",
                stake_delta=2.47,
                decimal_odds=1.54,
                model_win=0.786,
                edge_w=0.761,
                posted_edge=0.137,
                reason_plain="New paper ticket.",
                amount_plain="New $2.47.",
            ),
        ],
    )
    pack = write_paper_pack(rec, run_id="live-b")
    txt = (pack / "01_paper_tickets.txt").read_text(encoding="utf-8")
    assert "Sungjae Im" in txt
    assert "Top 20" in txt
    assert "2.47" in txt
    html = (pack / "01_paper_tickets.html").read_text(encoding="utf-8")
    assert "Sungjae Im" in html
    assert "$2.47" in html
    assert f"${round(pos.stake - 2.0, 2):.2f}" in html
    assert Path(rec.export_txt).read_text(encoding="utf-8") == txt


def test_ticket_rows_live_mark_and_place_na_without_coupon(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-new-1",
                kind="new_bet",
                status="advised",
                player_id="im",
                player_name="Sungjae Im",
                bet_type="top_20",
                stake_delta=2.47,
                decimal_odds=1.54,
                model_win=0.786,
                edge_w=0.761,
                posted_edge=0.137,
                reason_plain="New paper ticket.",
                amount_plain="New $2.47.",
            )
        ],
    )
    live_kita = _row(
        "kita", "Kurt Kitayama", 0.070, edge=0.021, posted=15.0,
        place=5, place_disp="T5", score=-6, holes=27,
    )
    live_im = _row(
        "im", "Sungjae Im", 0.097, edge=0.070, posted=31.0,
        place=2, place_disp="T2", score=-8, holes=36,
    )
    tickets = ticket_rows(rec, [live_kita, live_im], live_run_id="live-b")
    by = {(t.player_name, t.market): t for t in tickets}
    kita = by[("Kurt Kitayama", "Win")]
    assert kita.posted == 17.0
    assert kita.live_posted == 15.0
    assert kita.live_model == 0.070
    assert abs(kita.live_edge_w - 0.021) < 1e-9
    assert kita.live_place == "T5"
    assert kita.live_to_par == "-6"
    assert kita.live_thru == "9"
    assert kita.board_now == "T5 -6 9"
    im = by[("Sungjae Im", "Top 20")]
    assert im.posted == 1.54
    assert im.live_model is not None
    assert im.live_posted is None
    assert im.live_posted_edge is None
    assert im.live_edge_w is None
    assert im.live_place == "T2"
    assert im.live_to_par == "-8"
    assert im.live_thru == "F"


def test_pack_tickets_fill_live_from_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.audit.journal import current_model_record, save_audit
    from golf_offshoot.models.schemas import AuditRecord
    from golf_offshoot.strategy.paper_pack import write_paper_pack

    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    audit = AuditRecord(
        run_id="live-b",
        tournament_id="401811962",
        mode=RunMode.LIVE,
        model=current_model_record(),
        data_snapshot_hash="test",
        outputs=[
            _row(
                "kita", "Kurt Kitayama", 0.070, edge=0.021, posted=15.0,
                place=5, place_disp="T5", score=-6, holes=27,
            )
        ],
    )
    save_audit(audit, tmp_path / "snapshots")
    pack = write_paper_pack(rec, run_id="live-b")
    txt = (pack / "01_paper_tickets.txt").read_text(encoding="utf-8")
    assert "This live" in txt or "Live post" in txt
    assert "17.00" in txt
    assert "15.00" in txt
    html = (pack / "01_paper_tickets.html").read_text(encoding="utf-8")
    assert "At entry" in html
    assert "This live" in html
    assert "Place" in html
    assert "T5" in html
    assert "-6" in html
    assert "printed" in html
    explained = (pack / "02_bets_explained.html").read_text(encoding="utf-8")
    assert "Place" in explained
    assert "T5" in explained
    assert "printed" in explained
    explained = (pack / "02_bets_explained.txt").read_text(encoding="utf-8")
    assert "live@15.00" in explained
    assert "entry@17.00" in explained


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


def test_advice_carries_live_model_and_posted_edge(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.strategy.engine import run_strategy

    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    locked = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    rec = run_strategy(rows, cfg, run_mode=RunMode.LIVE, book=locked.book)
    advice = advice_from_recommendation(locked, rec, run_id="live-a")
    assert advice
    holdish = next(a for a in advice if a.kind in {"hold", "exit", "reduce", "add"})
    assert holdish.model_win is not None
    assert holdish.edge_w is not None
    assert holdish.posted_edge is not None
    assert holdish.decimal_odds == 17.0


def test_apply_new_bet_fills_odds_from_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    scott = _row("scott", "Adam Scott", 0.059, edge=0.037, posted=26.0)
    monkeypatch.setattr(
        "golf_offshoot.strategy.paper_book.load_snapshot_outputs",
        lambda run_id, directory=None: [scott],
    )
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-scott-1",
                kind="new_bet",
                status="advised",
                player_id="scott",
                player_name="Adam Scott",
                bet_type="win",
                stake_delta=0.5,
                run_id="run-live",
                reason_plain="Open a new paper ticket.",
                amount_plain="New paper stake $0.50.",
            )
        ],
    )
    pos = next(p for p in rec.book.positions if p.player_name == "Adam Scott")
    assert pos.stake == 0.50
    assert pos.decimal_odds == 26.0
    assert pos.entry_model_p == 0.059
    assert rec.movements[-1].decimal_odds == 26.0
    assert rec.movements[-1].status == "applied"


def test_apply_new_bet_skips_without_coupon(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a", odds_book="bovada")
    n = len(rec.book.positions)
    rec = apply_advice(
        rec,
        [
            PaperMovement(
                movement_id="move-nobody",
                kind="new_bet",
                status="advised",
                player_id="nobody",
                player_name="Nobody",
                bet_type="win",
                stake_delta=0.5,
                run_id="missing",
            )
        ],
    )
    assert len(rec.book.positions) == n


def test_pressure_report_path_is_per_event():
    from golf_offshoot.operating import pressure_report_path

    path = pressure_report_path("401811962")
    assert path.name == "PRESSURE_TEST_401811962.md"
    other = pressure_report_path("401703504")
    assert other.name == "PRESSURE_TEST_401703504.md"


def test_display_lane_live_suffix():
    from golf_offshoot.strategy.paper_book import display_lane

    assert display_lane(True) == "[cleared]"
    assert display_lane(False) == "[observation]"
    assert display_lane(True, has_live=True, live_posted_edge=None) == "[cleared|n/a]"
    assert display_lane(True, has_live=True, live_posted_edge=0.002, live_edge_w=0.05) == "[cleared|miss]"
    assert display_lane(True, has_live=True, live_posted_edge=0.06, live_edge_w=0.07) == "[cleared]"


def test_ticket_lane_marks_live_na_without_coupon(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(
        [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)],
        cfg,
        event_id="401811962",
        write_exports=False,
        run_id="lane-na",
    )
    live = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=None)]
    rows = ticket_rows(rec, live)
    assert rows[0].lane == "[cleared|n/a]"
    still = ticket_rows(rec)
    assert still[0].lane == "[cleared]"


def test_ticket_txt_keeps_entered_and_market_on_one_row(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.strategy.paper_export import paper_book_document

    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(
        [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)],
        cfg,
        event_id="401811962",
        write_exports=False,
        run_id="entered-width",
        odds_book="bovada",
    )
    text = paper_book_document(rec, tickets=ticket_rows(rec), live_run_id="entered-width")
    data_line = next(ln for ln in text.splitlines() if "Kurt Kitayama" in ln and "Win" in ln)
    assert "EDT" in data_line or "EST" in data_line
    assert "Win" in data_line


def test_unmarked_hold_blotter_does_not_say_intact():
    pos_id = new_id("pos")
    pid = "yella"
    pos = StrategyPosition(
        position_id=pos_id,
        player_id=pid,
        player_name="S. Yellamaraju",
        bet_type=BetType.TOP_20,
        stake=1.61,
        decimal_odds=6.0,
        entry_edge=0.357,
        entry_model_p=0.363,
        user_recorded=True,
    )
    book = PaperBookFile(
        tournament_id="401811962",
        bankroll=270.0,
        book=PortfolioState(bankroll=270.0, positions=[pos]),
    )
    mark = PositionMark(
        position_id=pos_id,
        player_id=pid,
        bet_type=BetType.TOP_20,
        entry_edge=0.357,
        live_edge=None,
        entry_model_p=0.363,
        live_model_p=0.0,
        entry_market_p=None,
        live_market_p=None,
        live_decimal_odds=None,
        stake=1.61,
        mtm_value=1.61,
        unrealized_pnl=0.0,
        original_edge_collapsed=False,
        live_edge_improved=False,
        is_runner=False,
        range_width=0.2,
        reliability=0.5,
        live_edge_unmarked=True,
    )
    rec = StrategyRecommendation(
        recommendation_id=new_id("rec"),
        mode=StrategyMode.STAY_SELECTIVE,
        run_mode=RunMode.LIVE,
        actions=[
            StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.HOLD,
                player_id=pid,
                player_name="S. Yellamaraju",
                bet_type=BetType.TOP_20,
                position_id=pos_id,
                reason=unmarked_ride_to_settle(),
            )
        ],
        marks=[mark],
        status=StrategyStatusSummary(
            open_exposure=1.61,
            exposure_frac=0.01,
            unrealized_pnl=0.0,
            unrealized_edge_weighted=0.0,
            biggest_concentration="",
            biggest_concentration_frac=0.0,
            posture=StrategyMode.STAY_SELECTIVE,
            cooling_off=False,
            n_positions=1,
            n_suggested_actions=1,
        ),
    )
    advice = advice_from_recommendation(book, rec, run_id="live-u")
    assert advice
    blob = advice[0].reason_plain.lower()
    assert "intact" not in blob
    assert "settle" in blob
    assert "cash-out" in blob
