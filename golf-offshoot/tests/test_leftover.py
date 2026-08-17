from golf_offshoot.audit.journal import build_audit
from golf_offshoot.demo import demo_tournament
from golf_offshoot.leftover import format_leftover_callout
from golf_offshoot.models.enums import BetType, Horizon, RunMode, SourceKind
from golf_offshoot.models.schemas import (
    HorizonProbability,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
    SourceInventoryItem,
    TournamentRunResult,
)
from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id


def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    lo = max(0.0, central - 0.01)
    hi = min(1.0, central + 0.01)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(pid: str, name: str, win: float, *, score: float | None = None, holes: int = 0) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.2, theta_sd=0.8),
        reliability=ReliabilityScore(
            player_id=pid, score=0.7, data_density=0.5, data_quality=0.5, input_stability=0.5
        ),
        live_score_to_par=score,
        live_holes_completed=holes,
    )


def _item(name: str, *, kind: SourceKind, coverage: str, notes: str = "", impact: str = "") -> SourceInventoryItem:
    return SourceInventoryItem(
        field_name=name,
        source_kind=kind,
        source_name="espn_field" if "player" in name else "test",
        coverage=coverage,
        notes=notes,
        impact_if_missing=impact,
    )


def _fixture_inventory() -> list[SourceInventoryItem]:
    return [
        _item("player_identification_field", kind=SourceKind.REAL_LIVE, coverage="2/2"),
        _item(
            "strokes_gained_recent_window",
            kind=SourceKind.REAL_HISTORICAL,
            coverage="2/2",
            notes="EVENT_ONLY last-16",
        ),
        _item(
            "strokes_gained_categories",
            kind=SourceKind.REAL_HISTORICAL,
            coverage="1/2 (missing 1)",
            notes="THROUGH_EVENT; unmatched: Demo Golfer",
            impact="SG unconstrained for unmatched players",
        ),
        _item(
            "course_setup_agronomy",
            kind=SourceKind.UNAVAILABLE,
            coverage="0",
            notes="firmness/rough/green speed not published",
        ),
        _item(
            "health_injury",
            kind=SourceKind.UNAVAILABLE,
            coverage="WD only",
            notes="no injury wire; WD status only",
        ),
        _item("market_odds", kind=SourceKind.REAL_LIVE, coverage="2/2"),
    ]


def _result(mode: RunMode, rows: list[PlayerOutput]) -> TournamentRunResult:
    t = demo_tournament()
    audit = build_audit(t.tournament_id, mode, rows, "h")
    audit.extra["source_inventory"] = [i.model_dump(mode="json") for i in _fixture_inventory()]
    audit.extra["odds_book"] = "bovada"
    audit.extra["odds_quotes"] = 2
    return TournamentRunResult(
        run_id=audit.run_id,
        tournament=t,
        mode=mode,
        ranked=rows,
        audit=audit,
    )


def _used_block(text: str) -> str:
    start = text.index("== already used ==")
    end = text.index("== still unconstrained ==")
    return text[start:end]


def test_ingest_omits_held_tickets_or_prints_none():
    rows = [_row("a", "Alpha", 0.10)]
    text = format_leftover_callout(_result(RunMode.PRE_TOURNAMENT, rows))
    assert "== already used ==" in text
    assert "== still unconstrained ==" in text
    assert "== on held tickets ==" in text
    assert "== do not stuff into theta ==" in text
    assert "none held" in text
    assert "Alpha" not in text.split("== on held tickets ==")[1]


def test_live_with_two_open_names_prints_those_two():
    rows = [
        _row("kita", "Kurt Kitayama", 0.089, score=-6, holes=54),
        _row("fleet", "Tommy Fleetwood", 0.121, score=-3, holes=50),
    ]
    book = PortfolioState(
        bankroll=250,
        positions=[
            StrategyPosition(
                position_id=new_id("p"),
                player_id="kita",
                player_name="Kurt Kitayama",
                bet_type=BetType.WIN,
                stake=12.5,
                decimal_odds=17.0,
                entry_edge=0.04,
                entry_model_p=0.089,
            ),
            StrategyPosition(
                position_id=new_id("p"),
                player_id="fleet",
                player_name="Tommy Fleetwood",
                bet_type=BetType.WIN,
                stake=12.5,
                decimal_odds=9.0,
                entry_edge=0.03,
                entry_model_p=0.121,
            ),
        ],
    )
    text = format_leftover_callout(_result(RunMode.LIVE, rows), book)
    held = text.split("== on held tickets ==")[1]
    assert "Kurt Kitayama" in held
    assert "Tommy Fleetwood" in held
    assert "banked to-par" in held
    assert "not extra theta" in held
    assert "ESPN to-par / holes completed" in text


def test_wording_does_not_claim_agronomy_or_narrative_were_used():
    rows = [_row("a", "Alpha", 0.10)]
    text = format_leftover_callout(_result(RunMode.LIVE, rows))
    used = _used_block(text).lower()
    assert "agronomy" not in used
    assert "narrative" not in used
    unconstrained = text.split("== still unconstrained ==")[1].split("== on held tickets ==")[0].lower()
    assert "agronomy" in unconstrained
    assert "narrative" in unconstrained
    assert "tee/wave" in unconstrained
