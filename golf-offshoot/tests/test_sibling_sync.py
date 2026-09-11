"""Gym hub origin-farm observe: fetch only, no Founder pull, no master/push/reset."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from golf_offshoot.learning_lane_15m.clerical_score import maybe_score_farm
from golf_offshoot.learning_lane_15m.farm_hub import farm_panel_html
from golf_offshoot.learning_lane_15m.sibling_sync import (
    ORIGIN_SIBLING,
    fetch_argv,
    maybe_fetch_origin_farm,
    origin_farm_cache_path,
    origin_farm_meta_path,
    refuse_git_argv,
    rev_parse_argv,
    show_exhausted_argv,
    show_farm_argv,
)

SIBLING_SYNC_PY = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "golf_offshoot"
    / "learning_lane_15m"
    / "sibling_sync.py"
)

THREE_NOTEBOOKS = [
    {
        "id": "F-CLOCK-CLOSE-MINUTE-15",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 15},
        "declared_at": "2026-09-10T18:45:00-04:00",
        "execution": False,
        "selects": True,
    },
    {
        "id": "F-CLOCK-CLOSE-MINUTE-30",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 30},
        "declared_at": "2026-09-10T18:45:00-04:00",
        "execution": False,
        "selects": True,
    },
    {
        "id": "F-CLOCK-CLOSE-MINUTE-45",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 45},
        "declared_at": "2026-09-10T18:45:00-04:00",
        "execution": False,
        "selects": True,
    },
]

ORIGIN_FARM = {
    "schema": 1,
    "lane": "learning_lane_15m",
    "notebooks": THREE_NOTEBOOKS,
}


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _empty_local_farm(root: Path) -> None:
    dest = root / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_FARM.json"
    _write(
        dest,
        {"schema": 1, "lane": "learning_lane_15m", "notebooks": []},
    )


def _origin_cache(root: Path, *, sha: str = "abcdef1234567890") -> None:
    _write(origin_farm_cache_path(root=root), ORIGIN_FARM)
    _write(
        origin_farm_meta_path(root=root),
        {"source": "origin", "ref": ORIGIN_SIBLING, "sha": sha, "fetched_at_unix": 1.0},
    )


def test_observe_argv_never_push_reset_master():
    for argv in (fetch_argv(), show_farm_argv(), show_exhausted_argv(), rev_parse_argv()):
        joined = " ".join(argv).lower()
        assert "push" not in argv
        assert "reset" not in argv
        assert "merge" not in argv
        assert "checkout" not in argv
        assert "master" not in joined.split()
        assert refuse_git_argv(argv) is None
    src = SIBLING_SYNC_PY.read_text(encoding="utf-8")
    assert "founder_has_armed" not in src
    assert "publish_arm_path" not in src
    assert "git reset" not in src
    assert "HEAD:master" not in src


def test_refuse_git_argv_blocks_push_reset_master():
    assert refuse_git_argv(["push", "origin", "HEAD:master"]) == "forbidden_git_verb"
    assert refuse_git_argv(["reset", "--hard", ORIGIN_SIBLING]) == "forbidden_git_verb"
    assert refuse_git_argv(["merge", "--ff-only", ORIGIN_SIBLING]) == "forbidden_git_verb"
    assert refuse_git_argv(["fetch", "origin", "master"]) == "master_ref"
    assert refuse_git_argv(["show", "origin/master:golf-offshoot/docs/LEARNING_LANE_15M_FARM.json"]) == (
        "master_ref"
    )


def test_empty_local_farm_shows_origin_notebooks(tmp_path):
    _empty_local_farm(tmp_path)
    _origin_cache(tmp_path, sha="cb2b002deadbeef")
    html = farm_panel_html(root=tmp_path)
    assert "F-CLOCK-CLOSE-MINUTE-15" in html
    assert "F-CLOCK-CLOSE-MINUTE-30" in html
    assert "F-CLOCK-CLOSE-MINUTE-45" in html
    assert "Not live" in html
    assert "origin/cursor/honer-15m-sibling @ cb2b002" in html
    assert "<th>PnL</th>" not in html
    local = json.loads(
        (tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_FARM.json").read_text(
            encoding="utf-8"
        )
    )
    assert local["notebooks"] == []


def test_failed_fetch_keeps_last_cache(tmp_path):
    _origin_cache(tmp_path, sha="oldsha000")
    (tmp_path / ".git").mkdir()

    def git_run(argv, cwd=None):
        del cwd
        return subprocess.CompletedProcess(["git", *argv], 1, "", "network")

    out = maybe_fetch_origin_farm(
        root=tmp_path,
        now=10_000.0,
        git_run=git_run,
        force=True,
    )
    assert out["ok"] is False
    assert out["reason"] == "fetch_failed"
    assert out["updated"] is False
    cached = json.loads(origin_farm_cache_path(root=tmp_path).read_text(encoding="utf-8"))
    assert [row["id"] for row in cached["notebooks"]] == [
        "F-CLOCK-CLOSE-MINUTE-15",
        "F-CLOCK-CLOSE-MINUTE-30",
        "F-CLOCK-CLOSE-MINUTE-45",
    ]
    html = farm_panel_html(root=tmp_path)
    assert "F-CLOCK-CLOSE-MINUTE-15" in html


def test_fetch_updates_cache_without_runner_arm(tmp_path):
    _empty_local_farm(tmp_path)
    (tmp_path / ".git").mkdir()
    arm = tmp_path / "data" / "learning_lane_15m" / "latest" / "RUNNER_ARMED"
    assert not arm.is_file()
    calls: list[list[str]] = []

    def git_run(argv, cwd=None):
        del cwd
        calls.append(list(argv))
        if argv[:1] == ["fetch"]:
            return subprocess.CompletedProcess(["git", *argv], 0, "", "")
        if argv == show_farm_argv():
            return subprocess.CompletedProcess(["git", *argv], 0, json.dumps(ORIGIN_FARM), "")
        if argv == rev_parse_argv():
            return subprocess.CompletedProcess(["git", *argv], 0, "6b17dae111111\n", "")
        return subprocess.CompletedProcess(["git", *argv], 1, "", "missing")

    out = maybe_fetch_origin_farm(
        root=tmp_path,
        now=10_000.0,
        git_run=git_run,
        force=True,
    )
    assert out["ok"] is True
    assert out["updated"] is True
    assert out["sha"] == "6b17dae111111"
    assert not arm.is_file()
    for argv in calls:
        assert refuse_git_argv(argv) is None
        assert "push" not in argv
        assert "reset" not in argv
        assert "master" not in " ".join(argv).split()
    html = farm_panel_html(root=tmp_path)
    assert "F-CLOCK-CLOSE-MINUTE-45" in html
    assert "6b17dae" in html


def test_maybe_score_farm_uses_origin_cache_does_not_write_local_farm(tmp_path, monkeypatch):
    docs = tmp_path / "golf-offshoot" / "docs"
    _empty_local_farm(tmp_path)
    _write(
        docs / "LEARNING_LANE_15M_RULES.json",
        {
            "schema": 1,
            "trials_to_date": 2,
            "rules": [
                {
                    "id": "R-LIVE-CLOCK",
                    "kind": "selection",
                    "selects": True,
                    "execution": True,
                    "declared_at": "2026-09-01T00:00:00-04:00",
                    "params": {"skip_close_minute": 0},
                }
            ],
        },
    )
    _write(
        docs / "LEARNING_LANE_15M_EVIDENCE_BAR.json",
        {
            "looks": {"first_look_n": 70},
            "distinguishable": {
                "effect_floor_usd_per_window": 0.01,
                "matched_exposure": {"draws": 8, "seed": 1},
            },
        },
    )
    _origin_cache(tmp_path)
    windows = [
        {
            "window_id": f"w{i}",
            "close_at": "2026-09-10T13:00:00-04:00",
            "posted_yes": 0.4,
            "recorded_pnl": 1.5,
            "stake": 1.0,
        }
        for i in range(70)
    ]
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.gather_tape_windows",
        lambda rule: windows,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.score_rule",
        lambda *args, **kwargs: {
            "n": 70,
            "look": "L1",
            "passes_every_binding_clause": False,
            "windows": [],
        },
    )
    out = maybe_score_farm(root=tmp_path)
    assert out["wrote"] is True
    ids = {row["id"] for row in out["cards"] if row.get("wrote")}
    assert "F-CLOCK-CLOSE-MINUTE-15" in ids
    local = json.loads(
        (tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_FARM.json").read_text(
            encoding="utf-8"
        )
    )
    assert local["notebooks"] == []


def _git_run_origin(sha: str = "6b17dae111111"):
    def git_run(argv, cwd=None):
        del cwd
        if argv[:1] == ["fetch"]:
            return subprocess.CompletedProcess(["git", *argv], 0, "", "")
        if argv == show_farm_argv():
            return subprocess.CompletedProcess(["git", *argv], 0, json.dumps(ORIGIN_FARM), "")
        if argv == rev_parse_argv():
            return subprocess.CompletedProcess(["git", *argv], 0, sha + "\n", "")
        return subprocess.CompletedProcess(["git", *argv], 1, "", "missing")

    return git_run


def test_same_sha_fetch_does_not_rewrite_cache(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.learning_lane_15m.sibling_sync._last_attempt_unix", None)
    _empty_local_farm(tmp_path)
    (tmp_path / ".git").mkdir()
    first = maybe_fetch_origin_farm(
        root=tmp_path,
        now=10_000.0,
        git_run=_git_run_origin("6b17dae111111"),
        force=True,
    )
    assert first["updated"] is True
    farm_path = origin_farm_cache_path(root=tmp_path)
    meta_path = origin_farm_meta_path(root=tmp_path)
    farm_mtime = farm_path.stat().st_mtime_ns
    meta_mtime = meta_path.stat().st_mtime_ns
    farm_bytes = farm_path.read_bytes()
    meta_bytes = meta_path.read_bytes()
    second = maybe_fetch_origin_farm(
        root=tmp_path,
        now=10_060.0,
        git_run=_git_run_origin("6b17dae111111"),
        force=True,
    )
    assert second["ok"] is True
    assert second["updated"] is False
    assert second["reason"] == "unchanged"
    assert farm_path.stat().st_mtime_ns == farm_mtime
    assert meta_path.stat().st_mtime_ns == meta_mtime
    assert farm_path.read_bytes() == farm_bytes
    assert meta_path.read_bytes() == meta_bytes


def test_kick_origin_farm_fetch_is_noop_under_pytest():
    from golf_offshoot.learning_lane_15m.sibling_sync import kick_origin_farm_fetch

    kick_origin_farm_fetch()


def test_hub_poll_kicks_origin_farm_without_inline_fetch(monkeypatch):
    kicks: list[int] = []
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.sibling_sync.kick_origin_farm_fetch",
        lambda **kwargs: kicks.append(1),
    )
    from golf_offshoot.operator_surface.reload import HubWatcher, WatchSnapshot

    snap = WatchSnapshot(git_tip="refs/heads/x@1", code=(("a.py", 1),), artifacts=(("s", 1),))
    watcher = HubWatcher(snapshot_fn=lambda: snap)
    watcher.seed(snap)
    decision = watcher.poll()
    assert kicks == [1]
    assert decision.kind == "none"
