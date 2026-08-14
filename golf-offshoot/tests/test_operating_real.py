from datetime import date

from golf_offshoot.data_feeds.history import (
    FinishRow,
    HistoricalEvent,
    HistoryIndex,
    finish_skill,
)
from golf_offshoot.models.enums import SourceKind
from golf_offshoot.pipeline import GolfOffshootPipeline, MockOnOperatingPathError
from golf_offshoot.demo import demo_field, demo_tournament
from golf_offshoot.models.enums import DataRole
from golf_offshoot.models.schemas import DataQuality
from datetime import datetime, timezone


def _ev(eid: str, start: str, rows: list[FinishRow], course: str = "c1") -> HistoricalEvent:
    return HistoricalEvent(
        event_id=eid,
        name=eid,
        start_date=start,
        course_id=course,
        course_name="Test",
        city="Memphis",
        state="TN",
        yardage=7200,
        par=70,
        has_cut=True,
        cut_place=10,
        field_size=max(len(rows), 2),
        is_major=False,
        status_state="post",
        finishes=rows,
    )


def _row(pid: str, finish: int, field_n: int = 20, made: bool = True) -> FinishRow:
    sk = finish_skill(finish, field_n, made)
    return FinishRow(
        player_id=pid,
        name=pid,
        finish=finish,
        made_cut=made,
        withdrawn=False,
        won=finish == 1 and made,
        top_5=finish <= 5 and made,
        top_10=finish <= 10 and made,
        top_20=finish <= 20 and made,
        score_to_par=float(finish - 10),
        skill=sk,
    )


def test_finish_skill_ranks_winner_above_missed_cut():
    assert finish_skill(1, 40, True) > finish_skill(35, 40, False)


def test_features_do_not_use_future_events():
    a = _ev("e1", "2026-01-10", [_row("pA", 1), _row("pB", 20)])
    b = _ev("e2", "2026-02-10", [_row("pA", 15), _row("pB", 1)])
    idx = HistoryIndex(events=[a, b]).sorted()
    feat_before_b = idx.features_for("pA", before="2026-02-10", course_id="c1", event_wind_kph=None)
    # pA won e1, so talent should be positive from e1 only
    assert feat_before_b.n_starts == 1
    assert feat_before_b.talent_prior > 0
    feat_after = idx.features_for("pA", before="2026-03-10", course_id="c1", event_wind_kph=None)
    assert feat_after.n_starts == 2
    # later poor finish should pull talent down vs pre-e2
    assert feat_after.talent_prior < feat_before_b.talent_prior


def test_operating_path_rejects_mock_quality():
    t = demo_tournament()
    field = demo_field()
    field.operating = True
    field.players[0].source_qualities["recent_form"] = DataQuality(
        score=0.9,
        role=DataRole.MOCK,
        source_name="sneaky_mock",
        as_of=datetime.now(timezone.utc),
        source_kind=SourceKind.MOCK,
        n_observations=3,
    )
    pipe = GolfOffshootPipeline(snapshot_dir=None)
    try:
        pipe.prepare_field(t, field)
        raised = False
    except MockOnOperatingPathError:
        raised = True
    assert raised


def test_split_and_dataset_exclude_future():
    from datetime import timedelta
    from golf_offshoot.calibration.dataset import build_event_dataset, split_events
    from golf_offshoot.models.schemas import Course, Tournament
    from golf_offshoot.models.enums import CourseType

    events = []
    start0 = date(2026, 1, 8)
    for i in range(12):
        rows = [_row(f"p{j}", (j + i) % 20 + 1) for j in range(20)]
        ev = _ev(f"e{i:02d}", (start0 + timedelta(days=7 * i)).isoformat(), rows)
        ev.tournament = Tournament(
            tournament_id=ev.event_id,
            name=ev.name,
            course=Course(course_id="c1", name="T", course_type=CourseType.PARKLAND),
            start_date=ev.start_date,
            has_cut=True,
            cut_place=10,
        )
        events.append(ev)
    idx = HistoryIndex(events=events).sorted()
    train, hold = split_events(idx, burn_in=2, holdout_n=2)
    assert hold[-1].start > train[-1].start
    ds = build_event_dataset(idx, hold[0])
    assert ds is not None
    # features for holdout event must not include that event's own results
    p0 = ds.field.players[0].player.player_id
    feat = idx.features_for(p0, before=hold[0].start_date, course_id="c1", event_wind_kph=None, exclude_event_id=hold[0].event_id)
    assert feat.n_starts == sum(
        1
        for e in events
        if e.start < hold[0].start and any(r.player_id == p0 for r in e.finishes)
    )
