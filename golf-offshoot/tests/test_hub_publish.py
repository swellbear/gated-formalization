"""Gym hub publish: refuse unarmed / heartbeat / missing ledger; never sibling HEAD."""

from golf_offshoot.learning_lane_15m.hub_publish import (
    evaluate_publish_gates,
    master_push_argv,
    maybe_publish_hub,
    watch_collecting_passed,
)


def test_unarmed_refuses():
    gates = evaluate_publish_gates(
        armed=False,
        ledger_present=True,
        watch_ok=True,
        material_reasons=["settle-status wording changed"],
    )
    assert gates["publish"] is False
    assert gates["reason"] == "unarmed"


def test_heartbeat_refuses():
    gates = evaluate_publish_gates(
        armed=True,
        ledger_present=True,
        watch_ok=True,
        material_reasons=[],
    )
    assert gates["publish"] is False
    assert gates["reason"] == "heartbeat"


def test_ledger_missing_refuses():
    gates = evaluate_publish_gates(
        armed=True,
        ledger_present=False,
        watch_ok=True,
        material_reasons=["settle-status wording changed"],
    )
    assert gates["publish"] is False
    assert gates["reason"] == "lineage_a_ledger_missing"


def test_watch_not_collecting_refuses():
    assert watch_collecting_passed({"checks": [{"id": "watch_is_collecting", "passed": False}]}) is False
    gates = evaluate_publish_gates(
        armed=True,
        ledger_present=True,
        watch_ok=False,
        material_reasons=["settle-status wording changed"],
    )
    assert gates["reason"] == "watch_not_collecting"


def test_push_is_worktree_head_to_master_not_sibling():
    argv = master_push_argv()
    assert argv == ["push", "origin", "HEAD:master"]
    joined = " ".join(argv)
    assert "--force" not in argv
    assert "honer-15m-sibling" not in joined
    assert "HEAD:cursor/honer-15m-sibling" not in joined


def test_scratch_override_does_not_push(tmp_path):
    from golf_offshoot.learning_lane_15m.paths import set_15m_root_override

    def fake_git(argv, *, cwd):
        raise AssertionError("git must not run under a 15m root override")

    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        result = maybe_publish_hub(root=tmp_path, git_run=fake_git)
        assert result["published"] is False
        assert result["reason"] == "scratch_override"
    finally:
        set_15m_root_override(None)


def test_maybe_publish_hub_unarmed_does_not_push(monkeypatch, tmp_path):
    calls: list[tuple] = []

    def fake_git(argv, *, cwd):
        calls.append((tuple(argv), str(cwd)))
        raise AssertionError("git must not run while unarmed")

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.hub_publish.founder_has_armed_publish",
        lambda: False,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.hub_publish.lineage_a_ledger_present",
        lambda root=None: True,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.hub_publish.load_invariants_payload",
        lambda: {"checks": [{"id": "watch_is_collecting", "passed": True}]},
    )
    result = maybe_publish_hub(root=tmp_path, git_run=fake_git)
    assert result["published"] is False
    assert result["pushed"] is False
    assert result["reason"] == "unarmed"
    assert result["push_argv"] == ["push", "origin", "HEAD:master"]
    assert calls == []
    assert "honer-15m-sibling" not in str(result)
