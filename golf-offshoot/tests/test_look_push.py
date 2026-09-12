"""Gym L1 look-push: sibling worktree, L1 JSON only, ride RUNNER_ARMED."""

from pathlib import Path

from golf_offshoot.learning_lane_15m.look_push import (
    PUSH_REF,
    evaluate_look_push_gates,
    is_l1_allowlist_rel,
    maybe_push_look,
    sibling_push_argv,
)


def test_look_push_argv_is_sibling_not_master():
    argv = sibling_push_argv()
    assert argv == ["push", "origin", "HEAD:cursor/honer-15m-sibling"]
    assert argv == ["push", "origin", PUSH_REF]
    joined = " ".join(argv)
    assert "HEAD:master" not in joined
    assert "--force" not in argv


def test_allowlist_is_l1_json_only():
    assert is_l1_allowlist_rel(Path("golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json"))
    assert not is_l1_allowlist_rel(Path("golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_F-CLOCK_FARM.json"))
    assert not is_l1_allowlist_rel(Path("golf-offshoot/data/learning_lane_15m/paper/ledger.json"))
    gates = evaluate_look_push_gates(
        armed=True,
        rels=[Path("golf-offshoot/data/learning_lane_15m/paper/ledger.json")],
    )
    assert gates["push"] is False
    assert gates["reason"] == "allowlist_refused"
    fee = evaluate_look_push_gates(
        armed=True,
        rels=[Path("golf-offshoot/docs/fee_total.json")],
    )
    assert fee["push"] is False
    ok = evaluate_look_push_gates(
        armed=True,
        rels=[Path("golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json")],
    )
    assert ok["push"] is True


def test_unarmed_does_not_push(monkeypatch, tmp_path):
    calls: list[tuple] = []

    def fake_git(argv, *, cwd):
        calls.append((tuple(argv), str(cwd)))
        raise AssertionError("git must not run while unarmed")

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.look_push._runner_armed",
        lambda: False,
    )
    result = maybe_push_look(root=tmp_path, git_run=fake_git)
    assert result["pushed"] is False
    assert result["reason"] == "unarmed"
    assert calls == []
    assert result["push_argv"] == ["push", "origin", "HEAD:cursor/honer-15m-sibling"]


def test_scratch_override_does_not_push(tmp_path):
    from golf_offshoot.learning_lane_15m.paths import set_15m_root_override

    def fake_git(argv, *, cwd):
        raise AssertionError("git must not run under a 15m root override")

    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        result = maybe_push_look(root=tmp_path, git_run=fake_git)
        assert result["pushed"] is False
        assert result["reason"] == "scratch_override"
    finally:
        set_15m_root_override(None)
