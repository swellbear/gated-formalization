from golf_offshoot.audit.journal import build_audit
from golf_offshoot.demo import demo_tournament
from golf_offshoot.models.enums import BetType, Horizon, RunMode, SourceKind
from golf_offshoot.models.schemas import (
    HorizonProbability,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
    SourceInventoryItem,
    TournamentRunResult,
)
from golf_offshoot.models.strategy import PortfolioState, StrategyPosition
from golf_offshoot.ranking.leftover import format_leftover_callout


def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    lo = max(0.0, central - 0.01)
    hi = min(1.0, central + 0.01)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(pid: str, name: str, win: float, *, score: float | None = None, holes: int = 0, place: int | None = None) -> PlayerOutput:
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
    )


def _item(
    field_name: str,
    *,
    kind: SourceKind,
    source: str = "",
    coverage: str = "",
    notes: str = "",
    impact: str = "",
) -> SourceInventoryItem:
    return SourceInventoryItem(
        field_name=field_name,
        source_kind=kind,
        source_name=source,
        coverage=coverage,
        notes=notes,
        impact_if_missing=impact,
    )


def _fixture_inventory() -> list[SourceInventoryItem]:
    return [
        _item(
            "player_identification_field",
            kind=SourceKind.REAL_LIVE,
            source="espn_field",
            coverage="70/70",
            notes="ESPN leaderboard competitors",
        ),
        _item(
            "strokes_gained_categories",
            kind=SourceKind.REAL_LIVE,
            source="pga_tour_sg",
            coverage="68/70",
            notes="THROUGH_EVENT attached 68/70; unmatched: Demo Ghost, Demo Ghost 2",
            impact="SG unconstrained for unmatched players",
        ),
        _item(
            "strokes_gained_recent_window",
            kind=SourceKind.DERIVED_FROM_REAL,
            source="pga_tour_sg_event_only",
            coverage="65/70",
            notes="EVENT_ONLY last-16",
        ),
        _item(
            "market_odds",
            kind=SourceKind.REAL_LIVE,
            source="bovada",
            coverage="40/70",
            notes="Winner quotes",
        ),
        _item(
            "course_setup_agronomy",
            kind=SourceKind.UNAVAILABLE,
            source="course_setup_agronomy",
            coverage="0",
            notes="firmness/rough/green speed not published on ESPN; left unconstrained",
            impact="tightness/rough/stimp not evidence",
        ),
        _item(
            "health_injury",
            kind=SourceKind.UNAVAILABLE,
            source="injury_wire",
            coverage="WD only",
            notes="no injury wire; WD status only",
            impact="injury rumours cannot move theta",
        ),
    ]


def _result(mode: RunMode, rows: list[PlayerOutput]) -> TournamentRunResult:
    t = demo_tournament()
    audit = build_audit(t.tournament_id, mode, rows, "leftover-test")
    audit.extra["source_inventory"] = [i.model_dump(mode="json") for i in _fixture_inventory()]
    return TournamentRunResult(
        run_id=audit.run_id,
        tournament=t,
        mode=mode,
        ranked=rows,
        audit=audit,
    )


def _section(text: str, header: str) -> str:
    marker = f"== {header} =="
    start = text.index(marker)
    rest = text[start + len(marker) :]
    nxt = rest.find("\n== ")
    return rest if nxt < 0 else rest[:nxt]


def _pos(pid: str, name: str) -> StrategyPosition:
    return StrategyPosition(
        position_id=f"pos-{pid}",
        player_id=pid,
        player_name=name,
        bet_type=BetType.WIN,
        stake=4.00,
        decimal_odds=12.0,
        entry_edge=0.04,
        entry_model_p=0.10,
        user_recorded=True,
    )


def test_leftover_has_four_sections():
    result = _result(RunMode.PRE_TOURNAMENT, [_row("p1", "Demo One", 0.12)])
    text = format_leftover_callout(result)
    assert "== already used ==" in text
    assert "== still unconstrained ==" in text
    assert "== on held tickets ==" in text
    assert "== do not stuff into theta ==" in text
    assert "GPF" in text
    assert "HumanOverride" in text
    assert "\u03b8" not in text
    assert "none held" in text


def test_ingest_prints_none_held():
    result = _result(RunMode.PRE_TOURNAMENT, [_row("p1", "Demo One", 0.12)])
    book = PortfolioState(bankroll=250.0, positions=[_pos("p1", "Demo One")])
    text = format_leftover_callout(result, book)
    held = _section(text, "on held tickets")
    assert "none held" in held
    assert "Demo One" not in held


def test_live_prints_two_open_names():
    rows = [
        _row("p1", "Held Alpha", 0.18, score=-6, holes=54, place=2),
        _row("p2", "Held Beta", 0.07, score=-3, holes=52, place=8),
        _row("p3", "Not Held", 0.04, score=1, holes=54, place=20),
    ]
    result = _result(RunMode.LIVE, rows)
    book = PortfolioState(
        bankroll=250.0,
        positions=[_pos("p1", "Held Alpha"), _pos("p2", "Held Beta")],
    )
    text = format_leftover_callout(result, book)
    held = _section(text, "on held tickets")
    assert "Held Alpha" in held
    assert "Held Beta" in held
    assert "Not Held" not in held
    assert "none held" not in held
    assert "Win% is banked to-par" in held
    assert "not extra theta" in held
    used = _section(text, "already used")
    assert "ESPN live board" in used
    assert "place / to-par / holes completed" in used


def test_wording_does_not_claim_agronomy_or_narrative_used():
    result = _result(RunMode.LIVE, [_row("p1", "Demo One", 0.12, score=-2, holes=18, place=4)])
    text = format_leftover_callout(result)
    used = _section(text, "already used").lower()
    unconstrained = _section(text, "still unconstrained").lower()
    assert "agronomy" not in used
    assert "narrative" not in used
    assert "agronomy" in unconstrained
    assert "narrative" in unconstrained
    assert "forced to 0" in unconstrained
    assert "unmatched" in unconstrained
    assert "demo ghost" in unconstrained
    assert "as-of SG" in _section(text, "already used")
    assert "posted odds" in _section(text, "already used")
    assert "bovada" in _section(text, "already used").lower()
