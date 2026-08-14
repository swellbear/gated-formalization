"""Deterministic mock tournament so tests and the CLI have a full field."""

from __future__ import annotations

from datetime import datetime, timezone

from golf_offshoot.models.enums import BetType, CourseType, DataRole, RunMode, SourceKind
from golf_offshoot.models.schemas import (
    Course,
    DataQuality,
    FieldSnapshot,
    MarketQuote,
    Player,
    PlayerInputs,
    StrokesGainedProfile,
    Tournament,
)

NAMES = [
    ("p01", "Rory Blake", False, 1.85),
    ("p02", "Scott Lang", False, 1.55),
    ("p03", "Jordan Hale", False, 1.40),
    ("p04", "Collin Ward", False, 1.25),
    ("p05", "Xander Cole", False, 1.15),
    ("p06", "Max Rivera", False, 1.05),
    ("p07", "Patrick Ng", False, 0.95),
    ("p08", "Hideki Mori", False, 0.88),
    ("p09", "Sam Ortiz", False, 0.70),
    ("p10", "Tony Ellis", False, 0.62),
    ("p11", "Adam Pierce", False, 0.50),
    ("p12", "Chris Young", False, 0.42),
    ("p13", "Luke Patel", False, 0.30),
    ("p14", "Ryan Cho", True, 0.05),
    ("p15", "Nate Brooks", True, -0.10),
    ("p16", "Omar Diaz", False, 0.22),
    ("p17", "Will Grant", False, 0.18),
    ("p18", "Eric Stone", False, 0.10),
    ("p19", "Ben Walsh", True, -0.25),
    ("p20", "Kai Jensen", False, 0.35),
]


def _q(score: float, n: int) -> DataQuality:
    return DataQuality(
        score=score,
        role=DataRole.MOCK,
        source_name="demo",
        as_of=datetime.now(timezone.utc),
        n_observations=n,
        source_kind=SourceKind.MOCK,
    )


def demo_tournament(course_type: CourseType = CourseType.PARKLAND) -> Tournament:
    course = Course(
        course_id="quail-hollow-demo",
        name="Quail Hollow (demo)",
        course_type=course_type,
        par=72,
        yardage=7600 if course_type != CourseType.LINKS else 7200,
        tightness=0.62,
        rough_severity=0.55,
        green_speed=0.70,
        wind_exposure=0.35 if course_type != CourseType.LINKS else 0.80,
        firmness=0.55,
        coastal=course_type == CourseType.LINKS,
    )
    return Tournament(
        tournament_id="demo-2026-wells",
        name="Demo Wells Fargo",
        course=course,
        start_date="2026-05-07",
        cut_place=10,  # scaled for 20-player demo field
        n_rounds=4,
        is_major=course_type == CourseType.MAJOR_SETUP,
    )


def demo_field(seed_form: bool = True) -> FieldSnapshot:
    players: list[PlayerInputs] = []
    for i, (pid, name, lesser, talent) in enumerate(NAMES):
        dist = 310 - i * 1.6
        acc = 58 + (i % 5) * 1.4
        sg = StrokesGainedProfile(
            ott=0.4 - i * 0.03,
            app=0.5 - i * 0.035,
            arg=0.1 - i * 0.01,
            putt=0.2 - (i % 7) * 0.04,
            total=talent * 0.45,
            driving_distance_yd=dist,
            driving_accuracy_pct=acc,
            quality=_q(0.78, 24),
        )
        hist_n = 0 if lesser else (12 - i // 3)
        players.append(
            PlayerInputs(
                player=Player(player_id=pid, name=name, owgr=i + 1, is_lesser_known=lesser),
                talent_prior=talent,
                talent_prior_sd=0.55 if lesser else 0.35,
                sg=sg,
                course_history_rounds=max(0, hist_n),
                course_history_sg=(0.2 - i * 0.02) if hist_n else None,
                recent_form_sg=(0.35 - i * 0.025) if seed_form else None,
                short_term_trend=0.15 if i in (3, 14) else (-0.1 if i == 1 else 0.02),
                weather_fit=0.1 if i % 4 == 0 else -0.05,
                health_flag=-0.8 if i == 6 else 0.0,
                narrative_momentum=0.9 if i == 3 else (0.4 if i == 0 else 0.0),
            )
        )
    return FieldSnapshot(
        tournament_id="demo-2026-wells",
        mode=RunMode.PRE_TOURNAMENT,
        players=players,
        weather_summary="moderate breeze, dry",
    )


def demo_odds(field: FieldSnapshot) -> list[MarketQuote]:
    """Softmax-ish market from talent so edges are not all zero, not all huge."""
    import math

    xs = [p.talent_prior for p in field.players]
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    quotes = []
    for p, e in zip(field.players, exps):
        fair = e / s
        # juice
        implied = fair * 1.18
        dec = 1.0 / implied
        quotes.append(
            MarketQuote(
                player_id=p.player.player_id,
                bet_type=BetType.WIN,
                decimal_odds=dec,
                implied_raw=implied,
                book="demo-book",
            )
        )
    return quotes


def demo_open_book(result, *, bankroll: float = 2000.0, n: int = 2):
    """User-recorded demo positions from a finished run. Not placed by the system."""
    from golf_offshoot.models.enums import BetType
    from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id
    from golf_offshoot.models.enums import Horizon

    positions = []
    for row in result.ranked[:n]:
        odds = None
        if result.market:
            for q in result.market.quotes:
                if q.player_id == row.player_id and q.bet_type == BetType.WIN and q.decimal_odds:
                    odds = q.decimal_odds
                    break
        if not odds:
            hp = row.probabilities.p(Horizon.WIN)
            odds = 1.0 / max(hp.central, 0.02)
        edge = row.edge_by_bet.get("win") or 0.04
        positions.append(
            StrategyPosition(
                position_id=new_id("pos"),
                player_id=row.player_id,
                player_name=row.name,
                bet_type=BetType.WIN,
                stake=round(0.02 * bankroll, 2),
                decimal_odds=odds,
                entry_edge=edge,
                entry_model_p=row.probabilities.p(Horizon.WIN).central,
                entry_market_p=row.market_implied_by_bet.get("win"),
                round_entered=0,
                notes="demo user-recorded position",
                user_recorded=True,
                proposed=False,
            )
        )
    return PortfolioState(bankroll=bankroll, positions=positions, session_label="demo")
