"""A/B method compare. Never auto-bets. Lived paper is a museum."""

from datetime import datetime, timezone

from golf_offshoot.clustering.similars import _player_vector, cosine
from golf_offshoot.compare.apply import maybe_apply_paper
from golf_offshoot.compare.fights import book_view, fights_at
from golf_offshoot.compare.law import learner_may_move_t, law_hash
from golf_offshoot.compare.paths import ComparePath, config_for, ledger_id
from golf_offshoot.decision.layer import advise_bet
from golf_offshoot.demo import demo_field, demo_odds, demo_tournament
from golf_offshoot.field_effects.interaction import field_interaction_adjustments
from golf_offshoot.models.enums import BetType, DecisionAction, Horizon, RiskPreference, RunMode, StrategyMode
from golf_offshoot.models.schemas import (
    AuditRecord,
    DataQuality,
    HorizonProbability,
    ModelVersionRecord,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
    StrokesGainedProfile,
)
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    load_paper_file,
    lock_paper_positions,
    paper_book_path,
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
    posted_by_bet: dict[str, float] | None = None,
    edge_by_bet: dict[str, float] | None = None,
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
    posted_odds = dict(posted_by_bet or {})
    if posted and "win" not in posted_odds:
        posted_odds["win"] = posted
    implied = {k: 1.0 / v for k, v in posted_odds.items() if v}
    edges = dict(edge_by_bet or {})
    if edge is not None and "win" not in edges:
        edges["win"] = edge
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


def _st_jude_rows() -> list[PlayerOutput]:
    return [
        _row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0),
        _row("fleet", "Tommy Fleetwood", 0.121, edge=0.041, posted=9.5),
        _row("scheff", "Scottie Scheffler", 0.113, edge=0.012, posted=7.5),
    ]


def test_b_never_tickets_on_edgew_alone():
    rows = _st_jude_rows()
    posted = [r.name for r in paper_candidates(rows, ticket_screen="posted")]
    edgew = [r.name for r in paper_candidates(rows, ticket_screen="edgew")]
    assert "Kurt Kitayama" in posted
    assert "Tommy Fleetwood" not in posted
    assert "Tommy Fleetwood" in edgew
    fleet = next(r for r in rows if r.name == "Tommy Fleetwood")
    assert advise_bet(fleet, BetType.WIN, 9.5, ticket_screen="posted").action == DecisionAction.PASS
    assert advise_bet(fleet, BetType.WIN, 9.5, ticket_screen="edgew").action != DecisionAction.PASS


def test_b_nerves_lock_refuses_fleetwood(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    cfg = config_for(ComparePath.B_NERVES)
    rec = lock_paper_positions(
        _st_jude_rows(),
        cfg,
        event_id="401811962",
        path_id=ledger_id(ComparePath.B_NERVES),
        independent_bankroll=True,
        write_exports=False,
        run_id="test-nerves",
    )
    names = [p.player_name for p in rec.book.positions]
    assert "Kurt Kitayama" in names
    assert "Tommy Fleetwood" not in names
    assert rec.independent_bankroll is True
    assert rec.path_id == "b_nerves"
    assert paper_book_path("401811962", "b_nerves") != paper_book_path("401811962", "lived")
    assert load_paper_file("401811962", "lived") is None
    assert load_paper_file("401811962", "b_nerves") is not None


def test_a_replay_lock_keeps_fleetwood_edgew(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    cfg = config_for(ComparePath.A_REPLAY)
    rec = lock_paper_positions(
        _st_jude_rows(),
        cfg,
        event_id="401811962",
        path_id=ledger_id(ComparePath.A_REPLAY),
        independent_bankroll=True,
        write_exports=False,
        run_id="test-a",
    )
    names = [p.player_name for p in rec.book.positions]
    assert "Kurt Kitayama" in names
    assert "Tommy Fleetwood" in names
    by = {p.player_name: p for p in rec.book.positions}
    assert abs(by["Kurt Kitayama"].stake - by["Tommy Fleetwood"].stake) < 1e-9


def test_learner_rejects_copy_a_because_a_won():
    ok, why = learner_may_move_t(n_events=20, reason="copy_a_edgew_because_a_won")
    assert ok is False
    assert "copy_a_edgew_because_a_won" in why
    ok2, why2 = learner_may_move_t(n_events=1, reason="holdout named")
    assert ok2 is False
    assert "keep_t" in why2
    assert law_hash() == law_hash()


def test_honest_missing_sg_not_treated_as_zero():
    field = demo_field().players
    missing = field[0]
    missing.sg = StrokesGainedProfile(
        ott=0.0,
        app=0.0,
        arg=0.0,
        putt=0.0,
        total=0.0,
        driving_distance_yd=None,
        driving_accuracy_pct=None,
        quality=DataQuality(
            score=0.0,
            source_name="none",
            as_of=datetime.now(timezone.utc),
            missing=True,
        ),
    )
    missing.recent_form_sg = None
    missing.recent_sg = None
    vec_lie = _player_vector(missing, honest=False)
    vec_honest = _player_vector(missing, honest=True)
    assert vec_lie[4] == 0.0
    assert vec_honest[4] != vec_honest[4]  # NaN
    other = _player_vector(field[1], honest=True)
    assert cosine(vec_honest, other) >= 0.0
    t = demo_tournament()
    lie = field_interaction_adjustments(field, t.course, honest=False)
    honest = field_interaction_adjustments(field, t.course, honest=True)
    pid = missing.player.player_id
    assert lie[pid] != 0.0 or honest[pid] == 0.0 or abs(honest[pid]) < abs(lie[pid])


def test_hysteresis_skips_hold_and_same_set(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = lock_paper_positions(
        [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)],
        StrategyConfig(
            enabled=True,
            mode=StrategyMode.STAY_SELECTIVE,
            risk=RiskPreference.CONSERVATIVE,
            bankroll=250,
        ),
        event_id="401811962",
        independent_bankroll=True,
        write_exports=False,
        run_id="hyst",
    )
    pos = rec.book.positions[0]
    holds = [
        PaperMovement(
            movement_id="h1",
            kind="hold",
            player_id=pos.player_id,
            player_name=pos.player_name,
            position_id=pos.position_id,
        )
    ]
    rec, applied = maybe_apply_paper(rec, holds)
    assert applied is False
    reduce = [
        PaperMovement(
            movement_id="r1",
            kind="reduce",
            player_id=pos.player_id,
            player_name=pos.player_name,
            position_id=pos.position_id,
            stake_delta=-1.0,
        )
    ]
    rec, applied = maybe_apply_paper(rec, reduce)
    assert applied is True
    rec, applied = maybe_apply_paper(rec, reduce)
    assert applied is False


def test_compare_book_does_not_reopen_after_settle(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.strategy.paper_ledger import settle_independent_compare_event

    rec = lock_paper_positions(
        _st_jude_rows(),
        config_for(ComparePath.A_REPLAY),
        event_id="401811962",
        path_id="a_replay",
        independent_bankroll=True,
        write_exports=False,
        run_id="hyst",
    )
    rec = settle_independent_compare_event(
        "401811962",
        "a_replay",
        finishes={"kita": (1, "Kurt Kitayama"), "fleet": (12, "Tommy Fleetwood")},
        completed=True,
        winner_ids=["kita"],
        event_name="St Jude",
    )
    bankroll = rec.bankroll
    rec, applied = maybe_apply_paper(
        rec,
        [
            PaperMovement(
                movement_id="junk",
                kind="new_bet",
                player_id="scheff",
                player_name="Scottie Scheffler",
                bet_type="win",
                stake_delta=8.75,
                decimal_odds=1.57,
            )
        ],
        force=True,
    )
    assert applied is False
    assert rec.book.positions == []
    assert rec.bankroll == bankroll


def test_fights_page_flags_fleetwood_disagreement(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    a = lock_paper_positions(
        _st_jude_rows(),
        config_for(ComparePath.A_REPLAY),
        event_id="401811962",
        path_id="a_replay",
        independent_bankroll=True,
        write_exports=False,
        run_id="a",
    )
    b = lock_paper_positions(
        _st_jude_rows(),
        config_for(ComparePath.B_NERVES),
        event_id="401811962",
        path_id="b_nerves",
        independent_bankroll=True,
        write_exports=False,
        run_id="b",
    )
    views = {"a_replay": book_view(a, "a_replay"), "b_nerves": book_view(b, "b_nerves")}
    events = fights_at(views)
    names = [e.player_name for e in events]
    assert "Tommy Fleetwood" in names
    fleet = next(e for e in events if e.player_name == "Tommy Fleetwood")
    assert "a_replay" in fleet.owned_by
    assert "b_nerves" in fleet.missing_from
    assert "EdgeW" in fleet.plain
    assert "vs-posted" in fleet.plain
    assert "ticket_screen=posted" in fleet.technical or "screen=posted" in fleet.technical
    assert "t=0.03" in fleet.technical


def test_fights_explains_place_ladder_vs_winner_only():
    from golf_offshoot.compare.fights import HeldTicket, PathBookView, fights_at

    lived = PathBookView(
        path_id="lived",
        n=1,
        names=["Sungjae Im"],
        exposure=2.47,
        bankroll=270,
        holdings=[
            HeldTicket("lived", "11382", "Sungjae Im", "top_20", 2.47, 0.08, 0.78, 1.54)
        ],
    )
    a = PathBookView(path_id="a_replay", n=0, names=[], exposure=0.0, bankroll=250)
    events = fights_at({"lived": lived, "a_replay": a}, event_id="401811962")
    assert events[0].player_name == "Sungjae Im"
    assert "Winner-only" in events[0].plain
    assert "place" in events[0].plain.lower() or "top 20" in events[0].plain.lower()
    assert "top_20" in events[0].technical
    assert "allowed_bet_types=[win]" in events[0].technical


def test_replay_walks_snapshots_into_separate_ledgers(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    monkeypatch.setattr("golf_offshoot.compare.fights.package_data_dir", lambda: tmp_path)
    from golf_offshoot.audit.journal import save_audit
    from golf_offshoot.compare.replay import replay_event

    snap = tmp_path / "snapshots"
    snap.mkdir()
    rows = _st_jude_rows()
    audit = AuditRecord(
        run_id="20260814T120000Z-deadbeef",
        tournament_id="401811962",
        mode=RunMode.LIVE,
        model=ModelVersionRecord(version_id="golf-offshoot-0.7.0", family="t", weight_hash="x", config_hash="y"),
        data_snapshot_hash="abc",
        outputs=rows,
        extra={"odds_book": "bovada"},
    )
    save_audit(audit, snap)
    payload = replay_event("401811962", write_exports=False, snapshot_dir=snap)
    assert payload["n_snapshots"] == 1
    a = load_paper_file("401811962", "a_replay")
    b = load_paper_file("401811962", "b_nerves")
    lived = load_paper_file("401811962", "lived")
    assert lived is None
    assert a is not None and "Tommy Fleetwood" in [p.player_name for p in a.book.positions]
    assert b is not None and "Tommy Fleetwood" not in [p.player_name for p in b.book.positions]
    assert a.independent_bankroll is True
    assert b.independent_bankroll is True


def test_independent_compare_book_does_not_touch_ledger(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    from golf_offshoot.strategy.paper_ledger import load_ledger, record_deposit

    record_deposit(250, note="lived opening")
    before = load_ledger()
    rec = lock_paper_positions(
        [_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)],
        config_for(ComparePath.B_NERVES),
        event_id="401811962",
        path_id="b_nerves",
        independent_bankroll=True,
        write_exports=False,
        run_id="iso",
    )
    pos = rec.book.positions[0]
    rec, applied = maybe_apply_paper(
        rec,
        [
            PaperMovement(
                movement_id="exit-1",
                kind="exit",
                player_id=pos.player_id,
                player_name=pos.player_name,
                position_id=pos.position_id,
                stake_delta=-pos.stake,
                decimal_odds=8.0,
            )
        ],
        force=True,
    )
    assert applied is True
    after = load_ledger()
    assert after.bankroll == before.bankroll
    assert len(after.entries) == len(before.entries)


def test_pipeline_persists_field_market_and_law(tmp_path):
    from golf_offshoot.bayesian_engine.engine import BayesianEngine
    from golf_offshoot.bayesian_engine.simulate import SimConfig
    from golf_offshoot.pipeline import GolfOffshootPipeline

    engine = BayesianEngine(sim=SimConfig(n_sims=200, seed=9))
    pipe = GolfOffshootPipeline(engine=engine, snapshot_dir=tmp_path)
    result = pipe.run(demo_tournament(), demo_field(), market_quotes=demo_odds(demo_field()), persist=True)
    extra = result.audit.extra
    assert extra.get("field")
    assert extra.get("market")
    assert extra.get("method_law_hash") == law_hash()
    assert extra.get("honest_theta") is False
    pipe.honest = True
    honest = pipe.run(demo_tournament(), demo_field(), market_quotes=demo_odds(demo_field()), persist=False)
    assert honest.audit.extra.get("honest_theta") is True


def test_batch_pack_writes_combo_readout(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    monkeypatch.setattr("golf_offshoot.compare.fights.package_data_dir", lambda: tmp_path)
    from golf_offshoot.compare.pack import write_batch_pack
    from pypdf import PdfReader

    rows = _st_jude_rows()
    lock_paper_positions(
        rows,
        config_for(ComparePath.A_REPLAY),
        event_id="401811962",
        event_name="FedEx St. Jude Championship",
        path_id="lived",
        write_exports=False,
        run_id="batch-test",
    )
    lock_paper_positions(
        rows,
        config_for(ComparePath.A_REPLAY),
        event_id="401811962",
        event_name="FedEx St. Jude Championship",
        path_id="a_replay",
        independent_bankroll=True,
        write_exports=False,
        run_id="batch-test",
    )
    lock_paper_positions(
        rows,
        config_for(ComparePath.B_NERVES),
        event_id="401811962",
        event_name="FedEx St. Jude Championship",
        path_id="b_nerves",
        independent_bankroll=True,
        write_exports=False,
        run_id="batch-test",
    )
    pack = write_batch_pack(
        "401811962",
        event_name="FedEx St. Jude Championship",
        run_id="batch-test",
        directory=tmp_path / "packs",
    )
    combo = pack / "00_full_readout.pdf"
    assert combo.is_file()
    assert combo.read_bytes().startswith(b"%PDF")
    assert (pack / "01_how_to_read.pdf").is_file()
    assert (pack / "02_fights.pdf").is_file()
    assert (pack / "05_lived_tickets.pdf").is_file()
    assert (pack / "06_lived_explained.pdf").is_file()
    assert (pack / "07_a_replay_tickets.pdf").is_file()
    assert (pack / "11_b_nerves_tickets.pdf").is_file()
    assert (pack / "15_bankroll.pdf").is_file()
    how = " ".join((PdfReader(str(pack / "01_how_to_read.pdf")).pages[0].extract_text() or "").split())
    assert "HOW TO READ THIS PACK" in how
    assert "A-control is not a second book" in how
    lived = " ".join((PdfReader(str(pack / "05_lived_tickets.pdf")).pages[0].extract_text() or "").split())
    assert "Lived museum tickets" in lived
    nerves = " ".join((PdfReader(str(pack / "11_b_nerves_tickets.pdf")).pages[0].extract_text() or "").split())
    assert "B-nerves tickets" in nerves
    fights = (pack / "02_fights.txt").read_text(encoding="utf-8")
    assert "== what these books are ==" in fights
    combo_text = " ".join((PdfReader(str(combo)).pages[0].extract_text() or "").split())
    assert "TRIGGER" in combo_text
    assert (pack / "00_trigger.pdf").is_file()
    trigger = (pack / "00_trigger.txt").read_text(encoding="utf-8")
    assert "TRIGGER" in trigger
    assert "00_full_readout.pdf" in (pack / "00_README.txt").read_text(encoding="utf-8")
    assert "00_trigger.pdf" in (pack / "00_README.txt").read_text(encoding="utf-8")
    combo_pages = len(PdfReader(str(combo)).pages)
    part_pages = 0
    for path in sorted(pack.glob("*.pdf")):
        if path.name == "00_full_readout.pdf":
            continue
        part_pages += len(PdfReader(str(path)).pages)
    assert combo_pages == part_pages
    assert combo_pages >= 4


def test_st_jude_compare_stays_winner_only():
    from golf_offshoot.compare.paths import allowed_compare_bets, compare_allows_place

    assert compare_allows_place("401811962") is False
    assert allowed_compare_bets("401811962") == [BetType.WIN]
    cfg = config_for(ComparePath.B_FULL, event_id="401811962")
    assert cfg.allowed_bet_types == [BetType.WIN]


def test_next_event_compare_allows_place_markets():
    from golf_offshoot.compare.paths import compare_allows_place

    assert compare_allows_place("401812000") is True
    cfg = config_for(ComparePath.A_REPLAY, event_id="401812000")
    assert BetType.WIN in cfg.allowed_bet_types
    assert BetType.TOP_5 in cfg.allowed_bet_types
    assert BetType.TOP_10 in cfg.allowed_bet_types
    assert BetType.TOP_20 in cfg.allowed_bet_types
    assert BetType.MAKE_CUT not in cfg.allowed_bet_types


def test_quoted_round_markets_join_allowed_bets():
    from golf_offshoot.compare.paths import allowed_bets_for_quotes
    from golf_offshoot.models.schemas import MarketQuote

    quote = MarketQuote(
        player_id="x",
        bet_type=BetType.WIN_AFTER_R1,
        decimal_odds=12.0,
        implied_raw=1.0 / 12.0,
        book="polymarket",
    )
    bets = allowed_bets_for_quotes("401811963", [quote])
    assert BetType.WIN in bets
    assert BetType.WIN_AFTER_R1 in bets
    assert allowed_bets_for_quotes("401811962", [quote]) == [BetType.WIN]


def test_future_lock_takes_real_place_coupon_not_invented(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    with_place = _row(
        "im",
        "Sungjae Im",
        0.08,
        edge=0.05,
        posted=12.0,
        posted_by_bet={"win": 12.0, "top_20": 1.8},
        edge_by_bet={"win": 0.05, "top_20": 0.12},
    )
    win_only = _row("fleet", "Tommy Fleetwood", 0.12, edge=0.041, posted=9.5)
    rec = lock_paper_positions(
        [with_place, win_only],
        config_for(ComparePath.B_FULL, event_id="401812000"),
        event_id="401812000",
        path_id="b_full",
        independent_bankroll=True,
        write_exports=False,
        run_id="future-place",
        require_cleared=True,
    )
    bets = {(p.player_name, p.bet_type.value) for p in rec.book.positions}
    assert ("Sungjae Im", "top_20") in bets
    assert ("Tommy Fleetwood", "top_20") not in bets


def test_st_jude_lock_ignores_place_even_if_coupon_exists(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    row = _row(
        "im",
        "Sungjae Im",
        0.08,
        edge=0.05,
        posted=12.0,
        posted_by_bet={"win": 12.0, "top_20": 1.8},
        edge_by_bet={"win": 0.05, "top_20": 0.12},
    )
    rec = lock_paper_positions(
        [row],
        config_for(ComparePath.B_FULL, event_id="401811962"),
        event_id="401811962",
        path_id="b_full",
        independent_bankroll=True,
        write_exports=False,
        run_id="stjude-place",
        require_cleared=True,
    )
    bets = {p.bet_type.value for p in rec.book.positions}
    assert "top_20" not in bets
    assert bets <= {"win"}


def test_split_pnl_keeps_winner_and_place_separate():
    from golf_offshoot.compare.scores import split_pnl
    from golf_offshoot.strategy.paper_ledger import TicketResult

    tickets = [
        TicketResult(player_name="A", bet_type="win", stake=8.75, decimal_odds=2.0, won=True, payout=17.5, pnl=8.75),
        TicketResult(player_name="B", bet_type="top_20", stake=2.0, decimal_odds=1.5, won=False, payout=0.0, pnl=-2.0),
    ]
    win, place, total = split_pnl(tickets)
    assert win == 8.75
    assert place == -2.0
    assert total == 6.75


def test_batch_pack_held_and_as_of_and_book_stamp(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    monkeypatch.setattr("golf_offshoot.compare.fights.package_data_dir", lambda: tmp_path)
    from golf_offshoot.audit.journal import save_audit
    from golf_offshoot.compare.pack import write_batch_pack
    from golf_offshoot.models.schemas import AuditRecord, ModelVersionRecord
    from golf_offshoot.strategy.paper_book import save_paper_book

    rows = [
        _row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0, place=4, place_disp="T4", score=-6, holes=18),
        _row("fleet", "Tommy Fleetwood", 0.121, edge=0.041, posted=9.5, place=8, place_disp="T8", score=-3, holes=14),
        _row("scheff", "Scottie Scheffler", 0.113, edge=0.012, posted=7.5, place=1, place_disp="1", score=-8, holes=18),
    ]
    lived = lock_paper_positions(
        rows,
        config_for(ComparePath.A_REPLAY, event_id="401811962"),
        event_id="401811962",
        event_name="FedEx St. Jude Championship",
        path_id="lived",
        write_exports=False,
        run_id="held-test",
        odds_book="bovada",
    )
    held_ids = {p.player_id for p in lived.book.positions}
    assert "kita" in held_ids
    assert "scheff" not in held_ids
    a_replay = lock_paper_positions(
        rows,
        config_for(ComparePath.A_REPLAY, event_id="401811962"),
        event_id="401811962",
        event_name="FedEx St. Jude Championship",
        path_id="a_replay",
        independent_bankroll=True,
        write_exports=False,
        run_id="held-test",
    )
    assert not a_replay.odds_book
    a_replay = a_replay.model_copy(update={"bankroll": 267.0, "book": a_replay.book.model_copy(update={"bankroll": 267.0})})
    save_paper_book(a_replay)
    audit = AuditRecord(
        run_id="held-test",
        tournament_id="401811962",
        mode=RunMode.LIVE,
        model=ModelVersionRecord(version_id="golf-offshoot-0.7.0", family="t", weight_hash="x", config_hash="y"),
        data_snapshot_hash="abc",
        outputs=rows,
        as_of=datetime(2026, 8, 15, 19, 1, 50, tzinfo=timezone.utc),
        extra={"odds_book": "bovada"},
    )
    save_audit(audit, tmp_path / "snapshots")
    pack = write_batch_pack(
        "401811962",
        event_name="FedEx St. Jude Championship",
        run_id="held-test",
        directory=tmp_path / "packs",
    )
    board = (pack / "03_leaderboard.txt").read_text(encoding="utf-8")
    kita_line = next(ln for ln in board.splitlines() if "Kurt Kitayama" in ln)
    scheff_line = next(ln for ln in board.splitlines() if "Scottie Scheffler" in ln)
    assert "paper" in kita_line
    assert "paper" not in scheff_line
    fights = (pack / "02_fights.txt").read_text(encoding="utf-8")
    assert "as_of=n/a" not in fights
    assert "Lock frozen" in fights or "live apply still mutates" in fights
    assert "started $250" in fights
    assert "now $267" in fights
    stamped = load_paper_file("401811962", path_id="a_replay")
    assert stamped is not None
    assert stamped.odds_book == "bovada"
    tickets = (pack / "07_a_replay_tickets.txt").read_text(encoding="utf-8")
    assert "book n/a" not in tickets
    assert "bovada" in tickets
    assert "started $250, now $267" in tickets


def test_fights_row_as_of_formats_when_passed():
    from golf_offshoot.compare.fights import PathBookView, fights_document

    a = PathBookView(path_id="a_replay", n=1, names=["Tommy Fleetwood"], exposure=1.0, bankroll=250)
    b = PathBookView(path_id="b_nerves", n=0, names=[], exposure=0.0, bankroll=250)
    events = fights_at(
        {"a_replay": a, "b_nerves": b},
        as_of="2026-08-15T19:01:50-04:00",
        run_id="held-test",
        event_id="401811962",
    )
    text = fights_document(
        "401811962",
        event_name="FedEx St. Jude Championship",
        views={"a_replay": a, "b_nerves": b},
        events=events,
    )
    assert "as_of=n/a" not in text
    assert "2026-08-15" in text
    assert "Tommy Fleetwood" in text
