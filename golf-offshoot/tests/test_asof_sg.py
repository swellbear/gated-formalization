from datetime import datetime, timezone
from types import SimpleNamespace

from golf_offshoot.config import RECENT_SG_EVENTS
from golf_offshoot.data_feeds.asof_sg import (
    AsOfSgIndex,
    SgPill,
    average_event_tables,
    scale_recent_sg_quality,
    _percentile,
)
from golf_offshoot.data_feeds.names import normalize_name
from golf_offshoot.data_feeds.pga_sg import SgRow, SgTable
from golf_offshoot.free_parameters.board import build_player_board
from golf_offshoot.models.enums import CourseType, FactorStatus, RunMode, SourceKind
from golf_offshoot.models.schemas import DataQuality, Player, PlayerInputs, StrokesGainedProfile


def _table(year: int, name: str, total: float, *, query: str = "EVENT_ONLY") -> SgTable:
    table = SgTable(year=year, query_type=query, last_processed=query)
    row = SgRow(pga_id="1", name=name, ott=0.2, app=0.4, arg=0.1, putt=0.05, total=total, n_events=1)
    table.by_name[normalize_name(name)] = row
    table.rows = [row]
    return table


def test_event_only_mean_skips_missing_weeks_not_zero_fill():
    a = _table(2026, "Scottie Scheffler", 2.0)
    b = _table(2026, "Someone Else", 1.0)
    c = _table(2026, "Scottie Scheffler", 4.0)
    averaged = average_event_tables([a, b, c])
    scottie = averaged.by_name[normalize_name("Scottie Scheffler")]
    assert abs(scottie.total - 3.0) < 1e-9
    assert scottie.n_events == 2
    other = averaged.by_name[normalize_name("Someone Else")]
    assert abs(other.total - 1.0) < 1e-9
    assert other.n_events == 1


def test_recent_window_request_is_sixteen_not_fabricated():
    assert RECENT_SG_EVENTS == 16


def test_load_pills_includes_three_seasons():
    class Feed:
        def quality_or_missing(self, **kwargs):
            y = int(kwargs.get("year") or 2026)
            table = SgTable(year=y, query_type="SEASON")
            table.pills = [{"tournamentId": f"R{y}013", "displayName": "Wyndham Championship"}]
            q = DataQuality(
                score=0.8,
                source_name="pga_tour_sg",
                as_of=datetime.now(timezone.utc),
                source_kind=SourceKind.REAL_HISTORICAL,
            )
            return table, q

    idx = AsOfSgIndex(Feed(), year=2026)  # type: ignore[arg-type]
    pills = idx.load_pills()
    assert {p.tournament_id for p in pills} == {"R2026013", "R2025013", "R2024013"}


def test_scale_recent_quality_tracks_measured_weeks_not_window_length():
    q = DataQuality(
        score=0.82,
        source_name="pga_tour_sg_event_only",
        as_of=datetime.now(timezone.utc),
        n_observations=3,
        source_kind=SourceKind.DERIVED_FROM_REAL,
        notes="mean of 16 tables",
    )
    thin = scale_recent_sg_quality(StrokesGainedProfile(total=1.2, quality=q))
    assert thin is not None and thin.quality is not None
    assert thin.quality.n_observations == 3
    assert thin.quality.score < 0.55
    deep_q = q.model_copy(update={"n_observations": 12})
    deep = scale_recent_sg_quality(StrokesGainedProfile(total=1.2, quality=deep_q))
    assert deep is not None and deep.quality is not None
    assert deep.quality.score > thin.quality.score
    assert deep.quality.score >= 0.70


def test_percentile_depth_is_honest():
    vals = [1, 2, 3, 8, 9]
    assert _percentile(vals, 50) == 3
    assert _percentile([], 50) == 0.0


def test_panel_strength_gate_requires_material_depth():
    from golf_offshoot.calibration.dataset import panel_is_materially_stronger

    weak, why = panel_is_materially_stronger({"median_events": 3.0, "recent_coverage": 0.74})
    assert weak is False
    assert "not a materially stronger" in why
    strong, _ = panel_is_materially_stronger({"median_events": 6.0, "recent_coverage": 0.74})
    assert strong is True


def test_pills_before_excludes_current_and_undated():
    idx = AsOfSgIndex(feed=None, year=2026)  # type: ignore[arg-type]
    idx.pills = [
        SgPill("R2026013", "Wyndham Championship", start_date="2026-07-31", espn_event_id="wynd"),
        SgPill("R2026014", "FedEx St. Jude Championship", start_date="2026-08-13", espn_event_id="stj"),
        SgPill("R2026999", "Unbound Current Week"),
    ]
    prior = idx.pills_before(
        "2026-08-13",
        exclude_event_id="stj",
        exclude_name="FedEx St. Jude Championship",
    )
    assert [p.tournament_id for p in prior] == ["R2026013"]


def test_pills_before_can_supply_sixteen_dated_events():
    idx = AsOfSgIndex(feed=None, year=2026)  # type: ignore[arg-type]
    idx.pills = [
        SgPill(
            f"R2026{i:03d}",
            f"Event Number {i}",
            start_date=f"2026-04-{(i % 28) + 1:02d}",
            espn_event_id=f"e{i}",
        )
        for i in range(1, 18)
    ]
    prior = idx.pills_before("2026-08-13")
    assert len(prior) >= 16
    assert RECENT_SG_EVENTS == 16
    assert len(prior[:RECENT_SG_EVENTS]) == 16


def test_bind_history_requires_two_token_overlap():
    idx = AsOfSgIndex(feed=None, year=2026)  # type: ignore[arg-type]
    idx.pills = [SgPill("R2026013", "Wyndham Championship")]
    n = idx.bind_history(
        [
            SimpleNamespace(name="3M Open", start_date="2026-07-24", event_id="3m"),
            SimpleNamespace(name="Wyndham Championship", start_date="2026-07-31", event_id="wynd"),
        ]
    )
    assert n == 1
    assert idx.pills[0].espn_event_id == "wynd"
    assert idx.pills[0].start_date == "2026-07-31"


def test_bind_history_is_one_to_one_across_years():
    idx = AsOfSgIndex(feed=None, year=2026)  # type: ignore[arg-type]
    idx.pills = [
        SgPill("R2025013", "Wyndham Championship"),
        SgPill("R2026013", "Wyndham Championship"),
        SgPill("R2026524", "Rocket Classic"),
    ]
    n = idx.bind_history(
        [
            SimpleNamespace(name="Wyndham Championship", start_date="2025-07-31", event_id="w25"),
            SimpleNamespace(name="Wyndham Championship", start_date="2026-07-31", event_id="w26"),
            SimpleNamespace(name="Rocket Classic", start_date="2026-06-26", event_id="rk"),
        ]
    )
    assert n == 3
    by_id = {p.tournament_id: p for p in idx.pills}
    assert by_id["R2025013"].espn_event_id == "w25"
    assert by_id["R2025013"].start_date == "2025-07-31"
    assert by_id["R2026013"].espn_event_id == "w26"
    assert by_id["R2026013"].start_date == "2026-07-31"
    prior = idx.pills_before("2026-08-13")
    eids = [p.espn_event_id for p in prior]
    assert len(eids) == len(set(eids))
    assert eids[0] == "w26"


def test_bind_history_does_not_double_book_one_espn_event():
    idx = AsOfSgIndex(feed=None, year=2026)  # type: ignore[arg-type]
    idx.pills = [
        SgPill("R2025013", "Wyndham Championship"),
        SgPill("R2026013", "Wyndham Championship"),
    ]
    idx.bind_history(
        [SimpleNamespace(name="Wyndham Championship", start_date="2026-07-31", event_id="w26")]
    )
    dated = [p for p in idx.pills if p.espn_event_id]
    assert len(dated) == 1
    assert dated[0].tournament_id == "R2026013"




def test_board_consumes_recent_sg_not_finish_residual():
    q = DataQuality(
        score=0.80,
        source_name="pga_tour_sg_event_only",
        as_of=datetime.now(timezone.utc),
        n_observations=6,
        source_kind=SourceKind.DERIVED_FROM_REAL,
        notes="mean of 6 EVENT_ONLY tables",
    )
    p = PlayerInputs(
        player=Player(player_id="ss", name="Scottie Scheffler"),
        recent_form_sg=0.11,
        recent_sg=StrokesGainedProfile(total=1.75, app=0.9, quality=q),
    )
    board = build_player_board(p, CourseType.PARKLAND, RunMode.PRE_TOURNAMENT)
    st = board["recent_form"]
    assert abs(st.standardized_evidence - 1.75) < 1e-9
    assert st.quality is not None
    assert st.quality.source_name == "pga_tour_sg_event_only"
    assert st.status in (FactorStatus.CONSTRAINED, FactorStatus.PARTIALLY_CONSTRAINED)


def test_engine_consumes_recent_sg_in_delta_theta():
    from golf_offshoot.bayesian_engine.engine import BayesianEngine
    from golf_offshoot.bayesian_engine.simulate import SimConfig
    from golf_offshoot.demo import demo_tournament
    from golf_offshoot.models.schemas import FieldSnapshot
    from golf_offshoot.pipeline import GolfOffshootPipeline

    q = DataQuality(
        score=0.80,
        source_name="pga_tour_sg_event_only",
        as_of=datetime.now(timezone.utc),
        n_observations=6,
        source_kind=SourceKind.DERIVED_FROM_REAL,
        notes="unit test EVENT_ONLY mean",
    )
    hot = PlayerInputs(
        player=Player(player_id="hot", name="Hot Form"),
        talent_prior=0.0,
        recent_sg=StrokesGainedProfile(total=2.4, quality=q),
    )
    cold = PlayerInputs(
        player=Player(player_id="cold", name="No Window"),
        talent_prior=0.0,
    )
    t = demo_tournament()
    field = FieldSnapshot(tournament_id=t.tournament_id, players=[hot, cold], operating=False)
    pipe = GolfOffshootPipeline(
        engine=BayesianEngine(sim=SimConfig(n_sims=500, seed=3)),
        snapshot_dir=None,
        apply_decisions=False,
    )
    result = pipe.run(t, field, persist=False)
    row = next(r for r in result.ranked if r.player_id == "hot")
    rec = next(c for c in row.explain.contributions if c.factor_id == "recent_form")
    assert abs(rec.delta_theta) > 0.05
    assert rec.quality >= 0.7
    cold_row = next(r for r in result.ranked if r.player_id == "cold")
    cold_rec = next(
        (c for c in cold_row.explain.contributions if c.factor_id == "recent_form"),
        None,
    )
    assert cold_rec is None or abs(cold_rec.delta_theta) < 1e-9


def test_board_keeps_finish_residual_when_recent_sg_missing():
    p = PlayerInputs(
        player=Player(player_id="ss", name="Scottie Scheffler"),
        recent_form_sg=0.42,
    )
    board = build_player_board(p, CourseType.PARKLAND, RunMode.PRE_TOURNAMENT)
    assert abs(board["recent_form"].standardized_evidence - 0.42) < 1e-9
    assert board["recent_form"].quality is not None
    assert "event_only" not in board["recent_form"].quality.source_name
