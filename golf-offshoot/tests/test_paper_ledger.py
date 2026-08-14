from golf_offshoot.models.enums import Horizon, RiskPreference, StrategyMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.strategy.paper_book import lock_paper_positions
from golf_offshoot.strategy.paper_ledger import (
    EventInspect,
    SettleError,
    load_ledger,
    record_deposit,
    record_withdrawal,
    settle_finished_open_books,
    settle_paper_event,
    working_bankroll,
)


def _hp(horizon: Horizon, central: float, width: float = 0.04) -> HorizonProbability:
    lo = max(0.0, central - width / 2)
    hi = min(1.0, central + width / 2)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(pid: str, name: str, win: float, *, edge: float, posted: float) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    bundle = ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.0, theta_sd=1.0)
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=bundle,
        reliability=ReliabilityScore(
            player_id=pid, score=0.74, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        edge_by_bet={"win": edge},
        market_implied_by_bet={"win": 1.0 / posted},
        posted_odds_by_bet={"win": posted},
    )


def test_deposit_and_withdraw_roll_bankroll(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    led = record_deposit(250, note="open")
    assert led.bankroll == 250
    assert led.deposits == 250
    assert led.never_auto_bet is True
    led = record_deposit(50, note="add")
    assert led.bankroll == 300
    led = record_withdrawal(20, note="take out")
    assert led.bankroll == 280
    assert led.withdrawals == 20
    loaded = load_ledger()
    assert loaded.bankroll == 280
    assert len(loaded.entries) == 3


def test_settle_win_and_loss_updates_lifetime(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [
        _row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=19.0),
        _row("fleet", "Tommy Fleetwood", 0.121, edge=0.041, posted=9.5),
    ]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", event_name="St Jude", run_id="run-a")
    assert rec.book.open_exposure == 17.50
    ledger = load_ledger()
    assert ledger.bankroll == 250
    finishes = {
        "kita": (1, "Kurt Kitayama"),
        "fleet": (12, "Tommy Fleetwood"),
    }
    ledger, rec, week = settle_paper_event(
        "401811962",
        finishes=finishes,
        completed=True,
        winner_ids=["kita"],
        event_name="St Jude",
    )
    # Kitayama 8.75 * 18 profit = 157.50; Fleetwood -8.75; net +148.75
    assert week.betting_pnl == 148.75
    assert ledger.bankroll == 398.75
    assert rec.settled_at is not None
    assert rec.book.positions == []
    assert any(t.won and t.player_name == "Kurt Kitayama" for t in week.tickets)
    assert any((not t.won) and t.player_name == "Tommy Fleetwood" for t in week.tickets)
    try:
        settle_paper_event(
            "401811962",
            finishes=finishes,
            completed=True,
            winner_ids=["kita"],
            event_name="St Jude",
        )
        raise AssertionError("second settle should fail")
    except SettleError:
        pass


def test_settle_refuses_unofficial_field(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=19.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a")
    try:
        settle_paper_event(
            "401811962",
            finishes={"kita": (1, "Kurt Kitayama")},
            completed=False,
            winner_ids=["kita"],
        )
        raise AssertionError("should refuse")
    except SettleError as exc:
        assert "not final" in str(exc)


def test_pack_includes_bankroll_page(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=19.0)]
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=250,
    )
    rec = lock_paper_positions(rows, cfg, event_id="401811962", run_id="run-a")
    pack = __import__("pathlib").Path(rec.latest_pack)
    from pypdf import PdfReader

    html = (pack / "05_bankroll.html").read_text(encoding="utf-8")
    assert "rolls from week to week" in html or "rolls week to week" in html
    assert "$250.00" in html or "$250" in html
    assert "Open tickets $8.75" in html
    assert "Cash at cost $241.25" in html
    pdf_text = " ".join(
        (PdfReader(str(pack / "05_bankroll.pdf")).pages[0].extract_text() or "").split()
    )
    assert "Open tickets $8.75" in pdf_text
    assert "cash at cost $241.25" in pdf_text.lower() or "Cash at cost $241.25" in pdf_text
    assert (pack / "05_bankroll.pdf").read_bytes().startswith(b"%PDF")
    assert "05_bankroll.pdf" in (pack / "00_README.txt").read_text(encoding="utf-8")
    combo = pack / "00_full_readout.pdf"
    assert combo.is_file()
    assert combo.read_bytes().startswith(b"%PDF")
    assert "00_full_readout.pdf" in (pack / "00_README.txt").read_text(encoding="utf-8")

    combo_pages = len(PdfReader(str(combo)).pages)
    part_pages = 0
    for name in ("01_paper_tickets.pdf", "02_bets_explained.pdf", "03_field_live.pdf", "05_bankroll.pdf"):
        part = pack / name
        if part.is_file():
            part_pages += len(PdfReader(str(part)).pages)
    assert combo_pages == part_pages
    assert combo_pages >= 3


def _cfg(bankroll: float = 250) -> StrategyConfig:
    return StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=bankroll,
    )


def _st_jude_lock(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [
        _row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=19.0),
        _row("fleet", "Tommy Fleetwood", 0.121, edge=0.041, posted=9.5),
    ]
    return lock_paper_positions(rows, _cfg(), event_id="401811962", event_name="St Jude", run_id="run-a")


def test_auto_settle_finished_then_next_lock_uses_rolled_caps(tmp_path, monkeypatch):
    rec = _st_jude_lock(tmp_path, monkeypatch)
    assert rec.book.open_exposure == 17.50
    finished = EventInspect(
        completed=True,
        finishes={"kita": (1, "Kurt Kitayama"), "fleet": (12, "Tommy Fleetwood")},
        winner_ids=["kita"],
        event_name="St Jude",
        status_note="state=post",
    )
    settled, skipped = settle_finished_open_books(
        inspect_event=lambda _eid, refresh=False: finished
    )
    assert skipped == []
    assert len(settled) == 1
    assert settled[0][0].bankroll == 398.75
    assert working_bankroll(except_event_id="next-event") == 398.75
    nxt = lock_paper_positions(
        [_row("p2", "Next Name", 0.15, edge=0.05, posted=10.0)],
        _cfg(250),
        event_id="next-event",
        event_name="Next Week",
        run_id="run-b",
    )
    assert nxt.bankroll == 398.75
    assert nxt.book.positions[0].stake == 13.96  # 3.5% of 398.75


def test_unfinished_open_book_reserves_cash_from_next_lock(tmp_path, monkeypatch):
    _st_jude_lock(tmp_path, monkeypatch)
    still_live = EventInspect(
        completed=False,
        finishes={},
        winner_ids=[],
        event_name="St Jude",
        status_note="state=in",
    )
    settled, skipped = settle_finished_open_books(
        inspect_event=lambda _eid, refresh=False: still_live
    )
    assert settled == []
    assert skipped
    assert working_bankroll(except_event_id="next-event") == 232.50
    nxt = lock_paper_positions(
        [_row("p2", "Next Name", 0.15, edge=0.05, posted=10.0)],
        _cfg(250),
        event_id="next-event",
        event_name="Next Week",
        run_id="run-b",
    )
    assert nxt.bankroll == 232.50
    assert nxt.book.positions[0].stake == 8.14  # 3.5% of 232.50


def test_playoff_does_not_auto_settle(tmp_path, monkeypatch):
    _st_jude_lock(tmp_path, monkeypatch)
    playoff = EventInspect(
        completed=True,
        finishes={"kita": (1, "Kurt Kitayama"), "fleet": (1, "Tommy Fleetwood")},
        winner_ids=["kita", "fleet"],
        event_name="St Jude",
        status_note="state=post",
    )
    settled, skipped = settle_finished_open_books(
        inspect_event=lambda _eid, refresh=False: playoff
    )
    assert settled == []
    assert any("exactly one official winner" in why for _rec, why in skipped)
    assert load_ledger().bankroll == 250
    assert working_bankroll(except_event_id="next-event") == 232.50
