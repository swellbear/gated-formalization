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


def test_maybe_score_writes_first_70_even_when_clauses_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.active_execution_rule",
        lambda **k: {"id": "R-SKIP-HOUR-CLOSE", "execution": True, "selects": True},
    )
    windows = [
        {"window_id": str(i), "close_at": f"2026-09-10T{i:02d}:00:00-04:00"}
        for i in range(75)
    ]
    seen: dict = {}

    def _gather(rule):
        del rule
        return list(windows)

    def _score(rule_id, scored, **kwargs):
        seen["n"] = len(scored)
        seen["allow_nonbinding"] = kwargs.get("allow_nonbinding")
        return {
            "rule_id": rule_id,
            "n": len(scored),
            "passes_every_binding_clause": False,
            "look": "L1",
        }

    dest = tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json"
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.gather_lived_windows",
        _gather,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.score_rule",
        _score,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.scorecard_path",
        lambda *a, **k: dest,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score._head_commit_sha",
        lambda **k: "abc123deadbeef",
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.evidence_bar.load_evidence_bar",
        lambda **k: {"looks": {"first_look_n": 70}},
    )
    out = maybe_score_executing(root=tmp_path)
    assert out["wrote"] is True
    assert seen["n"] == 70
    assert seen["allow_nonbinding"] is True
    payload = dest.read_text(encoding="utf-8")
    assert "abc123deadbeef" in payload
    assert "committed_at" in payload
    assert "caveat" in payload
    assert "execution" not in payload or '"execution": false' not in payload.lower()
