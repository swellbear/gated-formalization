"""Hub change detection + reload trigger. No live browser."""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace

from golf_offshoot.operator_surface.app import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    _window_summary_15m,
    apply_request_lane,
    build_surface,
    hub_url,
    maybe_open_hub_browser,
    open_hub_browser,
    rebuild_surface,
    render_html,
)
from golf_offshoot.operator_surface.app import main as shell_main
from golf_offshoot.operator_surface.hub_browser import (
    choose_hub_window,
    hub_window_hints,
    refresh_existing_hub_window,
)
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


def _linked_worktree(tmp_path: Path, *, sha: str, branch: str = "refs/heads/feature") -> Path:
    """The layout git actually writes for `git worktree add`.

    Branch refs live in the common dir. The worktree git dir holds only HEAD
    and a `commondir` pointer.
    """
    common = tmp_path / "main" / ".git"
    (common / branch).parent.mkdir(parents=True, exist_ok=True)
    (common / branch).write_text(sha + "\n", encoding="utf-8")
    wt_git = common / "worktrees" / "side"
    wt_git.mkdir(parents=True, exist_ok=True)
    (wt_git / "HEAD").write_text(f"ref: {branch}\n", encoding="utf-8")
    (wt_git / "commondir").write_text("../..\n", encoding="utf-8")
    repo = tmp_path / "side"
    repo.mkdir(exist_ok=True)
    (repo / ".git").write_text(f"gitdir: {wt_git}\n", encoding="utf-8")
    return repo


def test_read_git_tip_resolves_a_branch_sha_inside_a_linked_worktree(tmp_path):
    # Reading only the worktree git dir leaves the sha empty, so every commit
    # on the current branch looks like no change and the hub never re-execs.
    repo = _linked_worktree(tmp_path, sha="1111aaa")
    assert read_git_tip(repo) == "refs/heads/feature@1111aaa"


def test_a_commit_on_the_same_branch_is_a_code_reload_in_a_worktree(tmp_path):
    repo = _linked_worktree(tmp_path, sha="1111aaa")
    before = WatchSnapshot(git_tip=read_git_tip(repo), code=(), artifacts=())
    (tmp_path / "main" / ".git" / "refs" / "heads" / "feature").write_text(
        "2222bbb\n", encoding="utf-8"
    )
    after = WatchSnapshot(git_tip=read_git_tip(repo), code=(), artifacts=())

    assert before.git_tip != after.git_tip
    assert classify_change(before, after).should_reexec is True


def test_hub_code_files_watch_the_lane_package(tmp_path):
    # PaperWatch and the clerical runner execute in the hub process. A merge
    # that only touches the lane must still re-exec.
    pkg = _pkg_with_hub(tmp_path)
    lane = pkg / "learning_lane_15m"
    lane.mkdir()
    (lane / "runner.py").write_text("# clerical runner\n", encoding="utf-8")
    (lane / "learn.py").write_text("# wake\n", encoding="utf-8")
    golf = pkg / "golf_kalshi"
    golf.mkdir()
    (golf / "loop.py").write_text("# golf kalshi\n", encoding="utf-8")

    names = {path.name for path in hub_code_files(pkg)}

    assert {"runner.py", "learn.py", "loop.py", "app.py", "__main__.py"} <= names


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


def test_same_lane_query_does_not_rebuild_surface(monkeypatch):
    rebuilt: list[int] = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app.rebuild_surface",
        lambda state, **kwargs: rebuilt.append(1),
    )
    monkeypatch.setattr("golf_offshoot.operator_surface.app._sync_paper_watch", lambda state: None)
    state = {"lane": "learning_lane_15m", "surface": {}}
    assert apply_request_lane(state, "learning_lane_15m") is False
    assert rebuilt == []
    assert apply_request_lane(state, "golf") is True
    assert rebuilt == [1]
    assert state["lane"] == "golf"


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


def test_open_hub_browser_reuses_window(monkeypatch):
    opened: list[tuple[str, int]] = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app.webbrowser.open",
        lambda url, new=0, autoraise=True: opened.append((url, new)) or True,
    )
    # No hub window on screen, so this falls through to the browser.
    monkeypatch.setattr("golf_offshoot.operator_surface.app.refresh_existing_hub_window", lambda url: False)
    assert open_hub_browser("http://127.0.0.1:8765/") is True
    assert opened == [("http://127.0.0.1:8765/", 0)]


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


# --- hub restarts without the founder clicking anything -----------------------


def test_hub_child_never_opens_browser_even_when_argv_omitted_no_browser(monkeypatch, capsys):
    """The reported bug: a re-exec child stacked a Chrome tab on every restart.

    A parent started before ``--no-browser`` existed hands ``open_browser=True``
    down forever, so the opt-out cannot live in argv alone. Being a child is the
    thing that bars the browser.
    """
    opened: list[str] = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app.open_hub_browser",
        lambda url: opened.append(url) or True,
    )
    monkeypatch.setenv("GOLF_OFFSHOOT_HUB_CHILD", "1")
    assert maybe_open_hub_browser("http://127.0.0.1:8765/", enabled=True) is False
    assert opened == []
    assert "Opening hub in your default browser" not in capsys.readouterr().out

    # The parent, which the founder actually started, still gets its one window.
    monkeypatch.delenv("GOLF_OFFSHOOT_HUB_CHILD")
    assert maybe_open_hub_browser("http://127.0.0.1:8765/", enabled=True) is True
    assert opened == ["http://127.0.0.1:8765/"]


def test_open_hub_browser_prefers_refreshing_existing_window(monkeypatch):
    """Refresh the tab that is open. Only open a new one when there is none."""
    opened: list[str] = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app.webbrowser.open",
        lambda url, new=0, autoraise=True: opened.append(url) or True,
    )
    monkeypatch.setattr("golf_offshoot.operator_surface.app.refresh_existing_hub_window", lambda url: True)
    assert open_hub_browser("http://127.0.0.1:8765/") is True
    assert opened == []

    monkeypatch.setattr("golf_offshoot.operator_surface.app.refresh_existing_hub_window", lambda url: False)
    assert open_hub_browser("http://127.0.0.1:8765/") is True
    assert opened == ["http://127.0.0.1:8765/"]


def test_choose_hub_window_matches_browser_and_skips_console():
    hints = hub_window_hints("http://127.0.0.1:8765/")
    assert "golf-offshoot operator shell" in hints
    assert "127.0.0.1:8765" in hints

    # The console running the hub carries the same words in its title bar. Sending
    # it F5 would type into a terminal, so class has to agree with title.
    console = (11, "golf-offshoot operator shell - powershell", "ConsoleWindowClass")
    terminal = (12, "python -m golf_offshoot shell --port 8765", "CASCADIA_HOSTING_WINDOW_CLASS")
    chrome = (13, "golf-offshoot operator shell - Google Chrome", "Chrome_WidgetWin_1")
    assert choose_hub_window([console, terminal, chrome], hints) == 13
    assert choose_hub_window([console, terminal], hints) is None

    # A browser showing something else is not the hub.
    other = (14, "Inbox - Gmail - Google Chrome", "Chrome_WidgetWin_1")
    assert choose_hub_window([other], hints) is None
    # Falling back to the bare address still finds the tab when the title is absent.
    bare = (15, "127.0.0.1:8765/?lane=learning_lane_15m", "MozillaWindowClass")
    assert choose_hub_window([other, bare], hints) == 15


def test_refresh_existing_hub_window_uses_found_window():
    seen: list[int] = []

    def lister():
        return [(21, "golf-offshoot operator shell - Google Chrome", "Chrome_WidgetWin_1")]

    def refresher(hwnd):
        seen.append(hwnd)
        return True

    assert refresh_existing_hub_window("http://127.0.0.1:8765/", lister=lister, refresher=refresher) is True
    assert seen == [21]

    # No hub window on screen: report nothing to reuse instead of poking a window.
    assert refresh_existing_hub_window("http://127.0.0.1:8765/", lister=list, refresher=refresher) is False
    assert seen == [21]

    # Opt-out never touches the desktop at all.
    assert (
        refresh_existing_hub_window(
            "http://127.0.0.1:8765/",
            lister=lister,
            refresher=refresher,
            environ={"GOLF_OFFSHOOT_HUB_NO_FOCUS": "1"},
        )
        is False
    )
    assert seen == [21]


def test_html_watch_script_reloads_same_tab_on_generation(tmp_path):
    """Generation bump reloads this tab. A single /api/watch miss must not."""
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz"))
    assert "/api/watch" in page
    assert "if (reloading) return;" in page
    assert "lost = true" not in page
    assert "if (lost) { location.reload(); return; }" not in page
    assert "if (s.generation === gen) return;" in page
    assert "reloading = true;" in page
    assert "location.reload();" in page
    assert "if (!r.ok) throw new Error" in page


# --- 15m board chrome ---------------------------------------------------------


def test_15m_lane_shows_labelled_window_board(monkeypatch, tmp_path):
    png = tmp_path / "paper_window_strip.png"
    png.write_bytes(b"\x89PNG\r\n")
    monkeypatch.setattr("golf_offshoot.operator_surface.app._chart_15m_path", lambda: png)
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app._window_rows_15m",
        lambda: [
            SimpleNamespace(
                ticker="KXBTC15M-26SEP071445-45",
                settle_status="settled",
                kalshi_result="yes",
                paper_join=True,
            ),
            SimpleNamespace(
                ticker="KXBTC15M-26SEP071500-00",
                settle_status="SETTLE_PENDING",
                kalshi_result="",
                paper_join=True,
            ),
        ],
    )
    page = render_html(build_surface(lane="learning_lane_15m", artifact_root=tmp_path, viz_root=tmp_path / "viz"))

    # A titled figure, not an unlabelled colour block.
    assert "<figure>" in page and "<figcaption>" in page
    assert "KXBTC15M paper windows" in page
    # The caption names the windows: ticker, status, result.
    assert "KXBTC15M-26SEP071445-45 · settled · result=yes" in page
    assert "KXBTC15M-26SEP071500-00 · SETTLE_PENDING" in page
    assert "settled result=yes 1 · settled result=no 0 · SETTLE_PENDING 1" in page
    # Enlarge still works on this lane even though golf has no chart on disk.
    assert 'id="viz-lightbox"' in page
    assert 'data-viz-zoom="1"' in page
    # No golf boards leak onto the learning lane.
    for slot in ("shadow_honesty_strip", "calibration_weather", "wc1_dated_record"):
        assert f"viz-slot-{slot}" not in page


def test_15m_missing_png_stays_not_yet_available(monkeypatch, tmp_path):
    monkeypatch.setattr("golf_offshoot.operator_surface.app._chart_15m_path", lambda: None)
    page = render_html(build_surface(lane="learning_lane_15m", artifact_root=tmp_path, viz_root=tmp_path / "viz"))
    assert "not yet available" in page
    # Factory strip stays missing. Honer may still open a lightbox for its own PNG.
    assert "/viz15/paper_window_strip.png" not in page


def test_15m_window_summary_never_invents_a_result():
    """A window with no result on disk is pending. It is never scored win or lose."""
    rows = [
        SimpleNamespace(ticker="A-1", settle_status="settled", kalshi_result="no", paper_join=True),
        SimpleNamespace(ticker="A-2", settle_status="active", kalshi_result="", paper_join=False),
        SimpleNamespace(ticker="A-3", settle_status="", kalshi_result=None, paper_join=False),
    ]
    counts, windows = _window_summary_15m(rows)
    assert "settled result=yes 0 · settled result=no 1 · SETTLE_PENDING 2" in counts
    assert "1 paper-book join(s), 2 Kalshi-only journal row(s)" in counts
    assert "A-1 · settled · result=no" in windows
    assert "A-2 · active · SETTLE_PENDING" in windows
    # A row with no result on disk carries no verdict of any kind.
    assert "A-2 · active · result=" not in windows
    assert "A-3 · unknown · SETTLE_PENDING" in windows
    for verdict in ("paper_win", "paper_lose", "settle_win", "won", "lost"):
        assert verdict not in windows.lower()
    assert _window_summary_15m([]) == ("", "")


def test_15m_caption_caps_named_windows():
    rows = [
        SimpleNamespace(ticker=f"KXBTC15M-{i}", settle_status="settled", kalshi_result="yes", paper_join=False)
        for i in range(9)
    ]
    counts, windows = _window_summary_15m(rows, limit=4)
    assert counts.startswith("9 KXBTC15M window(s)")
    assert windows.count(";") == 3
    assert "+5 more on the board" in windows


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
