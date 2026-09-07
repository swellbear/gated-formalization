"""Hub change detection + reload trigger. No live browser."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace

from golf_offshoot.operator_surface.app import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    build_surface,
    hub_url,
    maybe_open_hub_browser,
    open_hub_browser,
    rebuild_surface,
    render_html,
)
from golf_offshoot.operator_surface.app import main as shell_main
from golf_offshoot.operator_surface.paths import resolve_roots
from golf_offshoot.operator_surface.reload import (
    REEXEC_CODE,
    HubWatcher,
    WatchSnapshot,
    artifact_watch_files,
    classify_change,
    collect_snapshot,
    hub_child_command,
    hub_code_files,
    is_hub_child,
    is_noise_name,
    read_git_tip,
    supervise_hub_child,
)


def _git_repo(root: Path, *, ref: str = "refs/heads/master", sha: str = "aaa111") -> Path:
    git = root / ".git"
    git.mkdir(parents=True)
    (git / "HEAD").write_text(f"ref: {ref}\n", encoding="utf-8")
    ref_path = git / ref
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    ref_path.write_text(sha + "\n", encoding="utf-8")
    return root


def _pkg_with_hub(root: Path) -> Path:
    pkg = root / "golf_offshoot"
    surface = pkg / "operator_surface"
    surface.mkdir(parents=True)
    (surface / "app.py").write_text("# hub\n", encoding="utf-8")
    (surface / "reload.py").write_text("# reload\n", encoding="utf-8")
    (pkg / "__main__.py").write_text("# cli\n", encoding="utf-8")
    audit = pkg / "audit"
    audit.mkdir()
    (audit / "shadow_settle.py").write_text("# settle join\n", encoding="utf-8")
    return pkg


def _empty_snap() -> WatchSnapshot:
    return WatchSnapshot(git_tip="refs/heads/master@aaa", code=(("app.py", 1),), artifacts=(("shadow", 1),))


def test_read_git_tip_ref_and_sha(tmp_path):
    repo = _git_repo(tmp_path, sha="abc123")
    assert read_git_tip(repo) == "refs/heads/master@abc123"
    (repo / ".git" / "refs" / "heads" / "master").write_text("def456\n", encoding="utf-8")
    assert read_git_tip(repo) == "refs/heads/master@def456"


def test_read_git_tip_packed_refs_and_worktree(tmp_path):
    repo = tmp_path / "repo"
    real = tmp_path / "real.git"
    real.mkdir()
    (real / "HEAD").write_text("ref: refs/heads/master\n", encoding="utf-8")
    (real / "packed-refs").write_text("# pack\n999fff refs/heads/master\n", encoding="utf-8")
    repo.mkdir()
    (repo / ".git").write_text(f"gitdir: {real}\n", encoding="utf-8")
    assert read_git_tip(repo) == "refs/heads/master@999fff"


def test_noise_names_skip_editor_temps():
    assert is_noise_name("app.py.tmp")
    assert is_noise_name("app.py.swp")
    assert is_noise_name("app.py~")
    assert is_noise_name("__pycache__")
    assert is_noise_name(".#app.py")
    assert not is_noise_name("app.py")
    assert not is_noise_name("advises.jsonl")
    assert not is_noise_name("weights_calib-v3.json")


def test_git_tip_change_is_code_reload():
    prev = _empty_snap()
    curr = WatchSnapshot(git_tip="refs/heads/master@bbb", code=prev.code, artifacts=prev.artifacts)
    decision = classify_change(prev, curr)
    assert decision.kind == "code"
    assert decision.should_reexec
    assert "git_tip" in decision.reasons


def test_hub_mtime_change_is_code_reload():
    prev = _empty_snap()
    curr = WatchSnapshot(git_tip=prev.git_tip, code=(("app.py", 99),), artifacts=prev.artifacts)
    decision = classify_change(prev, curr)
    assert decision.kind == "code"
    assert "hub_mtime" in decision.reasons


def test_artifact_mtime_change_is_soft_reload():
    prev = _empty_snap()
    curr = WatchSnapshot(git_tip=prev.git_tip, code=prev.code, artifacts=(("shadow", 99),))
    decision = classify_change(prev, curr)
    assert decision.kind == "artifacts"
    assert decision.should_soft_reload
    assert not decision.should_reexec


def test_git_and_artifacts_together_reexec():
    prev = _empty_snap()
    curr = WatchSnapshot(git_tip="refs/heads/master@ccc", code=prev.code, artifacts=(("shadow", 99),))
    decision = classify_change(prev, curr)
    assert decision.kind == "code"


def test_debounce_ignores_transient_then_fires(tmp_path):
    clock = {"t": 0.0}

    def now() -> float:
        return clock["t"]

    watcher = HubWatcher(debounce_s=1.5, clock=now)
    base = _empty_snap()
    watcher.seed(base)
    changed = WatchSnapshot(git_tip=base.git_tip, code=base.code, artifacts=(("shadow", 2),))
    assert watcher.observe(changed, now=0.0).kind == "none"
    clock["t"] = 0.4
    thrash = WatchSnapshot(git_tip=base.git_tip, code=base.code, artifacts=(("shadow", 3),))
    assert watcher.observe(thrash, now=0.4).kind == "none"
    clock["t"] = 1.0
    assert watcher.observe(thrash, now=1.0).kind == "none"
    clock["t"] = 2.0
    decision = watcher.observe(thrash, now=2.0)
    assert decision.kind == "artifacts"
    assert watcher.observe(thrash, now=3.0).kind == "none"


def test_collect_snapshot_sees_hub_and_artifact_mtimes(tmp_path):
    repo = _git_repo(tmp_path / "repo")
    pkg = _pkg_with_hub(tmp_path / "src")
    art = tmp_path / "art"
    viz = tmp_path / "viz"
    (art / "shadow").mkdir(parents=True)
    (art / "latest").mkdir()
    (art / "calibration").mkdir()
    viz.mkdir()
    shadow = art / "shadow" / "advises.jsonl"
    shadow.write_text("{}\n", encoding="utf-8")
    live = art / "latest" / "401811963_live_x.txt"
    live.write_text("live\n", encoding="utf-8")
    (art / "calibration" / "weights_calib-v3.json").write_text("{}", encoding="utf-8")
    (viz / "shadow_honesty_strip.png").write_bytes(b"\x89PNG")
    roots = resolve_roots(artifact_root=art, viz_root=viz, environ={})
    snap = collect_snapshot(repo=repo, code_files=hub_code_files(pkg), roots=roots)
    assert snap.git_tip.endswith("@aaa111")
    code_names = {Path(name).name for name, _mtime in snap.code}
    assert "app.py" in code_names
    assert "shadow_settle.py" in code_names
    assert "reload.py" in code_names
    watched = {Path(name.rstrip("/")).name for name, _mtime in snap.artifacts}
    assert "advises.jsonl" in watched
    assert "401811963_live_x.txt" in watched
    assert "weights_calib-v3.json" in watched
    assert "shadow_honesty_strip.png" in watched
    assert not any(is_noise_name(Path(name.rstrip("/")).name) and not name.endswith("/") for name, _ in snap.artifacts)

    live.write_text("live2\n", encoding="utf-8")
    os.utime(live, ns=(live.stat().st_mtime_ns + 2_000_000, live.stat().st_mtime_ns + 2_000_000))
    later = collect_snapshot(repo=repo, code_files=hub_code_files(pkg), roots=roots)
    assert classify_change(snap, later).kind == "artifacts"

    app_py = pkg / "operator_surface" / "app.py"
    app_py.write_text("# hub v2\n", encoding="utf-8")
    os.utime(app_py, ns=(app_py.stat().st_mtime_ns + 2_000_000, app_py.stat().st_mtime_ns + 2_000_000))
    code_later = collect_snapshot(repo=repo, code_files=hub_code_files(pkg), roots=roots)
    assert classify_change(later, code_later).kind == "code"


def test_artifact_watch_skips_tmp(tmp_path):
    art = tmp_path / "art"
    (art / "latest").mkdir(parents=True)
    (art / "latest" / "401811963_live_x.txt").write_text("ok\n", encoding="utf-8")
    (art / "latest" / "401811963_live_x.txt.tmp").write_text("tmp\n", encoding="utf-8")
    roots = resolve_roots(artifact_root=art, viz_root=tmp_path / "viz", environ={})
    names = {p.name for p in artifact_watch_files(roots)}
    assert "401811963_live_x.txt" in names
    assert "401811963_live_x.txt.tmp" not in names


def test_rebuild_surface_bumps_generation_trigger(tmp_path):
    (tmp_path / "latest").mkdir()
    live = tmp_path / "latest" / "401811963_live_x.txt"
    live.write_text("first live table\nnever auto-bet\n", encoding="utf-8")
    state = {
        "event_id": "401811963",
        "artifact_root": tmp_path,
        "viz_root": tmp_path / "viz",
        "generation": 0,
        "reload_kind": "ok",
        "surface": build_surface(event_id="401811963", artifact_root=tmp_path, viz_root=tmp_path / "viz"),
    }
    assert "first live table" in state["surface"]["honesty"].ranked.text
    live.write_text("second live table after pull\nnever auto-bet\n", encoding="utf-8")
    rebuild_surface(state)
    state["generation"] = int(state["generation"]) + 1
    state["reload_kind"] = "artifacts"
    assert "second live table after pull" in state["surface"]["honesty"].ranked.text
    assert state["generation"] == 1


def test_hub_child_command_windows_module_form():
    cmd = hub_child_command(host="127.0.0.1", port=8765, open_browser=True)
    assert cmd[1:4] == ["-m", "golf_offshoot", "shell"]
    assert "--host" in cmd and "127.0.0.1" in cmd
    assert "--port" in cmd and "8765" in cmd
    assert "--no-browser" not in cmd
    skipped = hub_child_command(host="127.0.0.1", port=9000, open_browser=False)
    assert "--no-browser" in skipped
    assert "--lane" not in cmd
    with_lane = hub_child_command(host="127.0.0.1", port=8765, lane="learning_lane_15m")
    assert with_lane[with_lane.index("--lane") + 1] == "learning_lane_15m"


def test_supervise_restarts_only_on_reexec_code():
    calls = []

    def runner(cmd, env=None):
        calls.append((list(cmd), dict(env or {})))
        if len(calls) == 1:
            return SimpleNamespace(returncode=REEXEC_CODE)
        return SimpleNamespace(returncode=0)

    code = supervise_hub_child(["python", "-m", "golf_offshoot", "shell"], runner=runner)
    assert code == 0
    assert len(calls) == 2
    assert calls[0][1]["GOLF_OFFSHOOT_HUB_CHILD"] == "1"


def test_is_hub_child_env():
    assert is_hub_child({"GOLF_OFFSHOOT_HUB_CHILD": "1"})
    assert not is_hub_child({})


def test_html_includes_watch_poll_and_no_cash_controls(tmp_path):
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz"))
    assert "/api/watch" in page
    assert "location.reload" in page
    assert 'value="paper-deposit"' not in page
    assert 'value="cash-out"' not in page


def test_shell_main_opens_browser_unless_no_browser(monkeypatch):
    seen: list[dict] = []

    def fake_serve(**kwargs):
        seen.append(kwargs)
        return 0

    monkeypatch.setattr("golf_offshoot.operator_surface.app.serve", fake_serve)
    assert shell_main([]) == 0
    assert seen[0]["open_browser"] is True
    assert seen[0]["host"] == DEFAULT_HOST
    assert seen[0]["port"] == DEFAULT_PORT
    assert shell_main(["--no-browser", "--port", "9001"]) == 0
    assert seen[1]["open_browser"] is False
    assert seen[1]["port"] == 9001


def test_cli_shell_forwards_no_browser(monkeypatch):
    from golf_offshoot.__main__ import main

    seen: list[dict] = []

    def fake_serve(**kwargs):
        seen.append(kwargs)
        return 0

    monkeypatch.setattr("golf_offshoot.operator_surface.app.serve", fake_serve)
    assert main(["shell"]) == 0
    assert seen[0]["open_browser"] is True
    assert main(["shell", "--no-browser"]) == 0
    assert seen[1]["open_browser"] is False


def test_open_hub_browser_windows_startfile(monkeypatch):
    opened: list[str] = []
    monkeypatch.setattr("golf_offshoot.operator_surface.app.sys.platform", "win32")
    monkeypatch.setattr("golf_offshoot.operator_surface.app.os.startfile", lambda url: opened.append(url), raising=False)
    assert open_hub_browser("http://127.0.0.1:8765/") is True
    assert opened == ["http://127.0.0.1:8765/"]


def test_maybe_open_hub_browser_respects_opt_out(monkeypatch):
    opened: list[str] = []
    monkeypatch.setattr("golf_offshoot.operator_surface.app.open_hub_browser", lambda url: opened.append(url) or True)
    assert maybe_open_hub_browser("http://127.0.0.1:8765/", enabled=False) is False
    assert opened == []
    assert maybe_open_hub_browser("http://127.0.0.1:8765/", enabled=True) is True
    assert opened == ["http://127.0.0.1:8765/"]


def test_hub_url_uses_configured_host_port():
    assert hub_url("127.0.0.1", 8765) == "http://127.0.0.1:8765/"
    assert hub_url("127.0.0.1", 9001) == "http://127.0.0.1:9001/"


def test_api_watch_generation_and_soft_reload(tmp_path):
    from http.client import HTTPConnection
    from threading import Thread

    from golf_offshoot.operator_surface.app import OperatorHandler, _HubServer

    (tmp_path / "latest").mkdir()
    (tmp_path / "latest" / "401811963_live_x.txt").write_text("v1\nnever auto-bet\n", encoding="utf-8")
    state = {
        "event_id": "401811963",
        "artifact_root": tmp_path,
        "viz_root": tmp_path / "viz",
        "odds_book": "auto",
        "generation": 0,
        "reload_kind": "ok",
        "surface": build_surface(event_id="401811963", artifact_root=tmp_path, viz_root=tmp_path / "viz"),
    }
    httpd = _HubServer(("127.0.0.1", 0), OperatorHandler)
    httpd.surface_state = state
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = httpd.server_address[:2]
        conn = HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/api/watch")
        payload = conn.getresponse().read().decode("utf-8")
        assert '"generation": 0' in payload
        (tmp_path / "latest" / "401811963_live_x.txt").write_text("v2 after pull\nnever auto-bet\n", encoding="utf-8")
        rebuild_surface(state)
        state["generation"] = 1
        state["reload_kind"] = "artifacts"
        conn.request("GET", "/api/watch")
        later = conn.getresponse().read().decode("utf-8")
        assert '"generation": 1' in later
        assert "artifacts" in later
        conn.request("GET", "/text")
        body = conn.getresponse().read().decode("utf-8")
        assert "v2 after pull" in body
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
