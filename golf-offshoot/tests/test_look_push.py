"""Gym L1 look-push: sibling worktree, L1 JSON only, ride RUNNER_ARMED."""

import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.look_push import (
    PUSH_REF,
    copy_allowlisted_l1,
    evaluate_look_push_gates,
    is_l1_allowlist_rel,
    maybe_push_look,
    sibling_l1_stamp_blocks_overwrite,
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


def _l1_rel(rule_id: str = "R-SKIP-HOUR-CLOSE") -> Path:
    return Path(f"golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_{rule_id}_L1.json")


def _write_card(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_sibling_continue_and_park_stamps_block_overwrite(tmp_path):
    dest = tmp_path / _l1_rel()
    _write_card(dest, {"n": 70, "passes_every_binding_clause": True, "operator_look": "CONTINUE"})
    assert sibling_l1_stamp_blocks_overwrite(dest) is True
    _write_card(dest, {"n": 70, "passes_every_binding_clause": False, "operator_look": "PARK"})
    assert sibling_l1_stamp_blocks_overwrite(dest) is True
    _write_card(dest, {"n": 70, "passes_every_binding_clause": True})
    assert sibling_l1_stamp_blocks_overwrite(dest) is False
    assert sibling_l1_stamp_blocks_overwrite(tmp_path / "missing.json") is False


def test_look_push_copy_does_not_clobber_continue_or_park(tmp_path):
    """Bytes-differ is not enough: a sibling CONTINUE/PARK stamp must survive copy2."""
    rel = _l1_rel()
    gym = tmp_path / "gym"
    sibling = tmp_path / "sibling"
    gym_card = {"n": 70, "passes_every_binding_clause": True, "windows": [{"window_id": "gym"}]}
    _write_card(gym / rel, gym_card)
    _write_card(
        sibling / rel,
        {
            "n": 70,
            "passes_every_binding_clause": True,
            "operator_look": "CONTINUE",
            "operator_look_at": "2026-09-12T00:00:00-04:00",
        },
    )
    out = copy_allowlisted_l1(src_root=gym, dest_root=sibling, rels=[rel])
    assert out["copied"] == []
    assert out["preserved"] == [rel.as_posix()]
    kept = json.loads((sibling / rel).read_text(encoding="utf-8"))
    assert kept["operator_look"] == "CONTINUE"
    assert kept.get("windows") is None

    _write_card(
        sibling / rel,
        {"n": 70, "passes_every_binding_clause": False, "operator_look": "PARK"},
    )
    park = copy_allowlisted_l1(src_root=gym, dest_root=sibling, rels=[rel])
    assert park["copied"] == []
    assert park["preserved"] == [rel.as_posix()]
    kept_park = json.loads((sibling / rel).read_text(encoding="utf-8"))
    assert kept_park["operator_look"] == "PARK"
    assert kept_park.get("windows") is None


def test_look_push_copy_writes_unstamped_sibling_l1(tmp_path):
    rel = _l1_rel()
    gym = tmp_path / "gym"
    sibling = tmp_path / "sibling"
    _write_card(gym / rel, {"n": 70, "passes_every_binding_clause": True, "windows": [{"window_id": "gym"}]})
    out = copy_allowlisted_l1(src_root=gym, dest_root=sibling, rels=[rel])
    assert out["copied"] == [rel.as_posix()]
    assert out["preserved"] == []
    dest = json.loads((sibling / rel).read_text(encoding="utf-8"))
    assert dest["windows"] == [{"window_id": "gym"}]
    assert "operator_look" not in dest
