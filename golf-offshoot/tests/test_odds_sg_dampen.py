from datetime import datetime, timezone

import numpy as np

from golf_offshoot.bayesian_engine.live_dampen import (
    live_position_evidence,
    live_progress,
    remaining_totals,
)
from golf_offshoot.bayesian_engine.simulate import SimConfig, simulate_field
from golf_offshoot.data_feeds.bovada import BovadaOddsFeed
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.data_feeds.pga_sg import PgaTourSgFeed, SgRow, SgTable
from golf_offshoot.free_parameters.board import build_player_board
from golf_offshoot.models.enums import BetType, CourseType, FactorStatus, Horizon, RunMode, SourceKind
from golf_offshoot.models.schemas import DataQuality, Player, PlayerInputs, StrokesGainedProfile


def test_normalize_name_strips_accents_and_aliases():
    assert normalize_name("Ludvig Åberg") == "ludvig aberg"
    assert normalize_name("Siwoo Kim") == "si woo kim"
    assert normalize_name("J.J. Spaun") == "j j spaun"
    cands = {"ludvig aberg": "espn-1", "si woo kim": "espn-2"}
    assert match_name("Ludvig Aberg", cands) == "espn-1"
    assert match_name("Si Woo Kim", cands) == "espn-2"


def test_bovada_parser_matches_winner_and_skips_unmatched():
    event = {
        "description": "FedEx St. Jude Championship",
        "lastModified": 1755100000000,
        "displayGroups": [
            {
                "markets": [
                    {
                        "description": "Winner Live",
                        "outcomes": [
                            {"description": "Scottie Scheffler", "price": {"decimal": "5.50"}},
                            {"description": "Nobody In Field", "price": {"decimal": "101.00"}},
                            {"description": "Tommy Fleetwood", "price": {"decimal": "13.00"}},
                        ],
                    },
                    {
                        "description": "1st Round Leader",
                        "outcomes": [{"description": "Scottie Scheffler", "price": {"decimal": "9.00"}}],
                    },
                ]
            }
        ],
    }
    feed = BovadaOddsFeed()
    quotes, unmatched, markets = feed._quotes_from_event(
        event,
        {"scottie scheffler": "id-ss", "tommy fleetwood": "id-tf"},
    )
    assert unmatched == 1
    assert any("Winner" in m for m in markets)
    by = {q.player_id: q for q in quotes}
    assert by["id-ss"].bet_type == BetType.WIN
    assert by["id-ss"].decimal_odds == 5.5
    assert by["id-ss"].implied_raw == 1.0 / 5.5
    assert by["id-ss"].book == "bovada_live"
    assert "Nobody In Field" not in [q.player_id for q in quotes]


def test_pga_sg_name_match_fills_categories():
    table = SgTable(year=2026, last_processed="Through the Wyndham Championship, Aug 9")
    row = SgRow(
        pga_id="48081",
        name="Scottie Scheffler",
        ott=0.8,
        app=1.1,
        arg=0.2,
        putt=0.15,
        total=2.25,
        n_rounds=56,
    )
    table.by_name[normalize_name(row.name)] = row
    q = DataQuality(
        score=0.88,
        source_name="pga_tour_sg",
        as_of=datetime.now(timezone.utc),
        n_observations=164,
        source_kind=SourceKind.REAL_HISTORICAL,
        notes="test",
    )
    feed = PgaTourSgFeed()
    prof = feed.profile_for("Scottie Scheffler", table, q)
    assert prof is not None
    assert abs(prof.total - 2.25) < 1e-9
    assert prof.quality is not None
    assert not prof.quality.missing
    assert prof.quality.source_kind == SourceKind.REAL_HISTORICAL
    assert feed.profile_for("Not A Golfer", table, q) is None


def test_sg_quality_activates_board_factors():
    q = DataQuality(
        score=0.88,
        source_name="pga_tour_sg",
        as_of=datetime.now(timezone.utc),
        n_observations=40,
        missing=False,
        source_kind=SourceKind.REAL_HISTORICAL,
        notes="SG:T",
    )
    p = PlayerInputs(
        player=Player(player_id="ss", name="Scottie Scheffler"),
        sg=StrokesGainedProfile(ott=0.8, app=1.1, arg=0.2, putt=0.15, total=2.25, quality=q),
    )
    board = build_player_board(p, CourseType.PARKLAND, RunMode.PRE_TOURNAMENT)
    assert board["sg_match"].standardized_evidence == 2.25
    assert board["approach_sg"].standardized_evidence == 1.1
    assert board["putting"].standardized_evidence == 0.15
    assert board["sg_match"].quality is not None
    assert not board["sg_match"].quality.missing
    assert board["sg_match"].status in (FactorStatus.CONSTRAINED, FactorStatus.PARTIALLY_CONSTRAINED)


def test_live_progress_round1_is_much_weaker_than_late():
    early = live_progress(6)
    r1 = live_progress(18)
    late = live_progress(54)
    assert early["dampen"] < 0.04
    assert abs(r1["dampen"] - 0.25) < 1e-9
    assert abs(late["dampen"] - 0.75) < 1e-9
    ev6, _ = live_position_evidence(-6.0, 6)
    ev18, _ = live_position_evidence(-6.0, 18)
    assert abs(ev6) < 0.08
    assert abs(ev18 - 0.5) < 1e-9


def test_board_live_position_is_dampened_at_six_holes():
    p = PlayerInputs(
        player=Player(player_id="kk", name="Kurt Kitayama"),
        live_score_to_par=-6.0,
        live_holes_completed=6,
    )
    board = build_player_board(p, CourseType.PARKLAND, RunMode.LIVE)
    st = board["live_position"]
    assert abs(st.standardized_evidence) < 0.08
    assert st.quality is not None
    assert st.quality.score < 0.5


def test_remaining_totals_mean_matches_banked_plus_theta():
    theta = np.ones((8000, 1))
    current = np.array([-2.0])
    holes = np.array([18.0])
    rng = np.random.default_rng(0)
    tot = remaining_totals(theta, current, holes, 4, 2.35, rng)
    # 18 holes done → 3 remaining rounds; E = -2 + (-1)*3 = -5
    assert abs(float(tot.mean()) + 5.0) < 0.12


def test_thru_holes_round_finish_is_not_72():
    from golf_offshoot.data_feeds.espn import _thru_holes

    r1_done = {"status": {"type": {"name": "STATUS_FINISH"}, "period": 1, "thru": 18}}
    assert _thru_holes(r1_done, 4) == 18
    playing = {"status": {"type": {"name": "STATUS_IN_PROGRESS"}, "period": 1, "thru": 6}}
    assert _thru_holes(playing, 4) == 6
    r2_hole3 = {"status": {"type": {"name": "STATUS_IN_PROGRESS"}, "period": 2, "thru": 3}}
    assert _thru_holes(r2_hole3, 4) == 21
    event_over = {"status": {"type": {"name": "STATUS_FINAL"}, "period": 4, "thru": 18}}
    assert _thru_holes(event_over, 4) == 72
    finish_no_thru = {"status": {"type": {"name": "STATUS_FINISH"}, "period": 1}}
    assert _thru_holes(finish_no_thru, 4) == 18


def test_early_live_lead_does_not_dominate_equal_field():
    n = 60
    ids = [f"p{i:02d}" for i in range(n)]
    mean = np.zeros(n)
    sd = np.full(n, 0.25)
    live_score = np.zeros(n)
    live_holes = np.zeros(n)
    live_score[0] = -6.0
    live_holes[0] = 6.0
    bundles = simulate_field(
        ids,
        mean,
        sd,
        live_score=live_score,
        live_holes=live_holes,
        config=SimConfig(n_sims=2000, seed=7, cut_after=0, cut_place=n),
    )
    win0 = bundles["p00"].p(Horizon.WIN).central
    # Scorecard −6 is real, so Win rises vs 1/n (~1.7%). Equal-θ 60-man field
    # lands near 15%. The old failure mode was ~26% in a 69-man field after an
    # undampened live_position θ jump; this remaining-holes model must stay below that.
    assert win0 > 1.0 / n
    assert win0 < 0.18
