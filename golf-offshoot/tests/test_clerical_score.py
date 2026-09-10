"""Clerical score_rule for the executing factory selection only."""

from golf_offshoot.learning_lane_15m.clerical_score import (
    FORBIDDEN_SCORE_IDS,
    maybe_score_executing,
    scorecard_path,
)


def test_forbidden_ids_are_coinflip_and_favorite():
    assert FORBIDDEN_SCORE_IDS == {"R-SKIP-COINFLIP", "R-SKIP-2TO1-FAVORITE"}


def test_maybe_score_refuses_coinflip(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.active_execution_rule",
        lambda **k: {"id": "R-SKIP-COINFLIP", "execution": True, "selects": True},
    )
    dest = tmp_path / "LEARNING_LANE_15M_SCORECARD_R-SKIP-COINFLIP_L1.json"
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.scorecard_path",
        lambda *a, **k: dest,
    )
    out = maybe_score_executing(root=tmp_path)
    assert out["wrote"] is False
    assert "forbidden" in out["reason"]
    assert dest.is_file() is False


def test_maybe_score_refuses_parked_favorite(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.active_execution_rule",
        lambda **k: {"id": "R-SKIP-2TO1-FAVORITE", "execution": True, "selects": True},
    )
    dest = tmp_path / "LEARNING_LANE_15M_SCORECARD_R-SKIP-2TO1-FAVORITE_L1.json"
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.scorecard_path",
        lambda *a, **k: dest,
    )
    out = maybe_score_executing(root=tmp_path)
    assert out["wrote"] is False
    assert "forbidden" in out["reason"]
    assert dest.is_file() is False


def test_maybe_score_no_card_below_n(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.active_execution_rule",
        lambda **k: {"id": "R-SKIP-HOUR-CLOSE", "execution": True, "selects": True},
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.gather_lived_windows",
        lambda rule: [{"window_id": str(i)} for i in range(3)],
    )
    dest = tmp_path / "LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json"
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.scorecard_path",
        lambda *a, **k: dest,
    )

    def _bar(**kwargs):
        return {"looks": {"first_look_n": 70}}

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.evidence_bar.load_evidence_bar",
        _bar,
    )
    out = maybe_score_executing(root=tmp_path)
    assert out["wrote"] is False
    assert out["n"] == 3
    assert dest.is_file() is False
    assert not scorecard_path("R-SKIP-HOUR-CLOSE", root=tmp_path).is_file()
