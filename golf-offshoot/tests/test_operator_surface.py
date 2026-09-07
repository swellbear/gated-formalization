import os
from pathlib import Path

from golf_offshoot.audit.journal import build_audit
from golf_offshoot.demo import demo_tournament
from golf_offshoot.models.enums import BetType, Horizon, RunMode, SourceKind, StrategyActionKind, StrategyMode
from golf_offshoot.models.schemas import (
    HorizonProbability,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
    SourceInventoryItem,
    TournamentRunResult,
)
from golf_offshoot.models.strategy import (
    StrategyAction,
    StrategyRecommendation,
    StrategyStatusSummary,
    new_id,
)
from golf_offshoot.operator_surface.app import build_surface, render_html, render_text
from golf_offshoot.operator_surface.artifacts import (
    CALIB_MISSING,
    LIVE_TABLE_MISSING,
    SETTLE_PENDING,
    SHADOW_EMPTY,
    SHADOW_MISSING,
    load_honesty,
)
from golf_offshoot.operator_surface.modes import (
    CASH_BADGE,
    MODE_MOCK,
    MODE_OPERATING,
    PAPER_ONLY,
    build_mode_walls,
)
from golf_offshoot.operator_surface.paper import (
    PAPER_ADVICE_EMPTY,
    PAPER_APPLIED,
    PAPER_BARRED_MOCK,
    PAPER_EMPTY_FIELD,
    PAPER_LOCKED,
    apply_observation_paper,
)
from golf_offshoot.operator_surface.notify import notify_run_complete
from golf_offshoot.operator_surface.paths import PathUnsafeError, resolve_roots, safe_under
from golf_offshoot.operator_surface.runner import (
    OperatorSafetyError,
    refuse_forbidden,
    run_ingest,
    run_live,
    run_loop,
)
from golf_offshoot.operator_surface.viz import NOT_YET_AVAILABLE, load_viz_wall
from golf_offshoot.ranking.leftover import leftover_from_audit

import pytest


def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    return HorizonProbability(horizon=horizon, central=central, low=max(0.0, central - 0.01), high=min(1.0, central + 0.01))


def _row(pid: str, name: str, win: float) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=1,
        probabilities=ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.0, theta_sd=1.0),
        reliability=ReliabilityScore(player_id=pid, score=0.7, data_density=0.5, data_quality=0.5, input_stability=0.5),
    )


def _shadow_row(**overrides) -> dict:
    row = {
        "timestamp": "2026-09-07T12:00:00+00:00",
        "tournament": "BMW Championship",
        "tournament_id": "401811963",
        "player": "Scottie Scheffler",
        "player_id": "scheffler",
        "market": "win",
        "model_probability": 0.12,
        "model_p_low": 0.08,
        "model_p_high": 0.18,
        "posted_decimal": 9.5,
        "odds_as_of": "2026-09-07T12:00:00+00:00",
        "run_mode": "live",
        "mode": "stay_selective",
        "action_kind": "new_bet",
        "suggested_stake": 4.0,
        "never_auto_bet": True,
        "paper_observation_only": True,
        "run_id": "run-1",
        "recommendation_id": "rec-1",
    }
    row.update(overrides)
    return row


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(__import__("json").dumps(r) + "\n" for r in rows), encoding="utf-8")


def test_mode_walls_operating_vs_mock():
    ops = build_mode_walls(live_data=True)
    assert ops.mode == MODE_OPERATING
    assert ops.trading_armed is False
    assert "PHASE 1 OBSERVATION" in ops.badges
    assert "NOT ARMED" in ops.badges
    assert PAPER_ONLY in ops.badges
    assert CASH_BADGE in ops.badges
    assert "not trading armed" in ops.render_text().lower()
    assert "LIVE DATA" in ops.render_text()
    mock = build_mode_walls(mock=True)
    assert mock.mode == MODE_MOCK
    assert mock.is_mock is True
    assert "OFFLINE DEMO" in mock.render_text()
    assert "NOT OPERATING EVIDENCE" in mock.render_text()


def test_missing_shadow_is_not_zero_edge(tmp_path):
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.shadow.status == SHADOW_MISSING
    assert "zero-edge" in honesty.shadow.text
    assert honesty.calibration.status == CALIB_MISSING
    assert honesty.ranked.status == LIVE_TABLE_MISSING
    assert "demo field" in honesty.ranked.text


def test_empty_shadow_journal(tmp_path):
    path = tmp_path / "shadow" / "advises.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("", encoding="utf-8")
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.shadow.status == SHADOW_EMPTY
    assert honesty.shadow.status != SHADOW_MISSING


def test_shadow_settle_pending_and_required_fields(tmp_path):
    path = tmp_path / "shadow" / "advises.jsonl"
    _write_jsonl(path, [_shadow_row()])
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.shadow.status == "SHADOW_OK"
    assert honesty.shadow.settle_banner == SETTLE_PENDING
    assert SETTLE_PENDING in honesty.shadow.text
    for key in (
        "timestamp",
        "tournament",
        "tournament_id",
        "player",
        "player_id",
        "market",
        "model_probability",
        "never_auto_bet",
        "paper_observation_only",
        "run_id",
        "recommendation_id",
    ):
        assert key in honesty.shadow.text or honesty.shadow.rows[0][key] is not None


def test_empty_git_shadow_does_not_hide_external_sot(tmp_path):
    repo = tmp_path / "repo_data"
    external = tmp_path / "external"
    (repo / "shadow").mkdir(parents=True)
    _write_jsonl(external / "shadow" / "advises.jsonl", [_shadow_row(player="Matt Fitzpatrick")])
    env = {"GOLF_OFFSHOOT_ARTIFACT_ROOT": str(external)}
    honesty = load_honesty(environ=env, viz_root=tmp_path / "viz")
    assert honesty.shadow.status == "SHADOW_OK"
    assert honesty.shadow.rows[0]["player"] == "Matt Fitzpatrick"
    empty = load_honesty(artifact_root=repo, viz_root=tmp_path / "viz")
    assert empty.shadow.status == SHADOW_MISSING


def test_mock_shadow_barred_from_honesty(tmp_path):
    path = tmp_path / "shadow" / "advises.jsonl"
    _write_jsonl(path, [_shadow_row(reason="OFFLINE DEMO — MOCK DATA")])
    # marker in the file body
    path.write_text("OFFLINE DEMO — MOCK DATA\n", encoding="utf-8")
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.shadow.barred_mock is True
    assert "barred" in honesty.shadow.text


def test_calibration_latest_keep_expert(tmp_path):
    calib = tmp_path / "calibration"
    calib.mkdir()
    (calib / "weights_calib-v1.json").write_text(
        '{"version_id":"golf-offshoot-0.3.0-calib-v1","created_at":"2026-08-01T00:00:00+00:00","recommendation":"keep_expert"}',
        encoding="utf-8",
    )
    (calib / "weights_calib-v3.json").write_text(
        '{"version_id":"golf-offshoot-0.7.0-calib-v3","created_at":"2026-08-13T20:00:00+00:00","recommendation":"keep_expert","no_future_leakage":true,"weight_hash_expert":"abc","weight_hash_calibrated":"def","metrics":{"holdout_expert":{"brier":0.1}}}',
        encoding="utf-8",
    )
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.calibration.status == "CALIB_OK"
    assert honesty.calibration.recommendation == "keep_expert"
    assert honesty.calibration.no_future_leakage is True
    assert "calib-v3" in (honesty.calibration.version_id or "")
    assert "abc" in honesty.calibration.text


def test_live_table_and_leftover_from_latest(tmp_path):
    latest = tmp_path / "latest"
    latest.mkdir()
    (latest / "401811963_live_run1.txt").write_text(
        "BMW Championship  (live)\nobservation only  never auto-bet\n1 Scottie Scheffler 0.120\n",
        encoding="utf-8",
    )
    (latest / "401811963_live_run1.html").write_text("<html>Scottie Scheffler</html>", encoding="utf-8")
    (latest / "leftover.txt").write_text(
        "LEFTOVER CALLOUT\n== still unconstrained ==\n  agronomy\n== on held tickets ==\n  none held\n== do not stuff into theta ==\n  no\n",
        encoding="utf-8",
    )
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.ranked.status == "LIVE_TABLE_OK"
    assert "Scottie Scheffler" in honesty.ranked.text
    assert honesty.ranked.html_path is not None
    assert "PHASE 1 OBSERVATION" in honesty.ranked.banner
    assert honesty.leftover.status == "LEFTOVER_OK"
    assert "agronomy" in honesty.leftover.unconstrained
    assert "none held" in honesty.leftover.held_tickets
    assert "no" in honesty.leftover.do_not_stuff_theta


def test_demo_ranked_file_is_barred(tmp_path):
    latest = tmp_path / "latest"
    latest.mkdir()
    (latest / "demo_live_toy.txt").write_text("OFFLINE DEMO — MOCK DATA\n1 Demo Golfer 0.50\n", encoding="utf-8")
    honesty = load_honesty(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    assert honesty.ranked.barred_mock is True
    assert "Demo Golfer" not in honesty.ranked.text or honesty.ranked.status != "LIVE_TABLE_OK"
    assert honesty.ranked.status == "LIVE_TABLE_BARRED_MOCK"


def test_leftover_from_audit_is_display_only():
    t = demo_tournament()
    rows = [_row("p1", "Held One", 0.2)]
    audit = build_audit(t.tournament_id, RunMode.LIVE, rows, "shell-leftover")
    audit.extra["source_inventory"] = [
        SourceInventoryItem(
            field_name="health_injury",
            source_kind=SourceKind.UNAVAILABLE,
            source_name="injury_wire",
            coverage="WD only",
            impact_if_missing="injury rumours cannot move theta",
        ).model_dump(mode="json")
    ]
    text = leftover_from_audit(audit, t.name)
    assert "do not stuff into theta" in text
    assert "still unconstrained" in text


def test_viz_missing_is_not_invented(tmp_path):
    roots = resolve_roots(artifact_root=tmp_path, viz_root=tmp_path / "viz")
    wall = load_viz_wall(roots)
    assert wall.slot("shadow_honesty_strip").status == NOT_YET_AVAILABLE
    assert wall.slot("calibration_weather").status == NOT_YET_AVAILABLE
    assert "not invented" in wall.slot("shadow_honesty_strip").note or "not yet available" in wall.slot("shadow_honesty_strip").note
    assert wall.slot("shadow_honesty_strip").title == "Shadow honesty strip"
    assert wall.slot("calibration_weather").title == "Calibration weather"
    assert "not settled PnL" in wall.slot("shadow_honesty_strip").subline
    assert "keep_expert" in wall.slot("calibration_weather").subline


def test_viz_renders_existing_png_and_mtime(tmp_path):
    viz = tmp_path / "viz"
    viz.mkdir()
    png = viz / "shadow_honesty_strip.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")
    (viz / "calibration_weather.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    roots = resolve_roots(artifact_root=tmp_path, viz_root=viz)
    wall = load_viz_wall(roots)
    assert wall.slot("shadow_honesty_strip").status == "available"
    assert wall.slot("shadow_honesty_strip").mtime == png.stat().st_mtime
    png.write_bytes(b"\x89PNG\r\n\x1a\nmore")
    os.utime(png, (png.stat().st_atime, png.stat().st_mtime + 5))
    wall2 = load_viz_wall(roots)
    assert wall2.slot("shadow_honesty_strip").mtime != wall.slot("shadow_honesty_strip").mtime


def test_viz_manifest_rejects_traversal(tmp_path):
    viz = tmp_path / "viz"
    viz.mkdir()
    (viz / "viz_wall_manifest.json").write_text(
        '{"slots":{"shadow_honesty_strip":{"path":"../secret.png"}}}',
        encoding="utf-8",
    )
    roots = resolve_roots(artifact_root=tmp_path, viz_root=viz)
    wall = load_viz_wall(roots)
    assert wall.manifest_error
    assert wall.slot("shadow_honesty_strip").status == NOT_YET_AVAILABLE
    with pytest.raises(PathUnsafeError):
        safe_under(Path("../secret.png"), viz)


def test_notify_off_when_topic_absent(monkeypatch):
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    notice = notify_run_complete(command="ingest", ok=True)
    assert notice.sent is False
    assert "absent" in notice.reason


def test_notify_one_completion_not_progress(monkeypatch):
    monkeypatch.setenv("NTFY_TOPIC", "golf-bmw-test")
    calls = []

    def _fake(body, **kwargs):
        calls.append(body)
        return "https://ntfy.sh/golf-bmw-test"

    monkeypatch.setattr("golf_offshoot.operator_surface.notify.publish_ntfy", _fake)
    first = notify_run_complete(command="live", ok=True, event_id="401811963", detail="done")
    assert first.sent is True
    assert len(calls) == 1
    assert "NOT ARMED" in calls[0]
    assert CASH_BADGE in calls[0]


def test_forbidden_cash_and_trade_actions():
    for action in ("deposit", "withdraw", "lock-paper", "apply-paper", "cash-out", "arm", "kalshi-auth"):
        with pytest.raises(OperatorSafetyError):
            refuse_forbidden(action)


def test_shell_flow_ingest_live_shadow(monkeypatch, tmp_path):
    t = demo_tournament()
    t.espn_event_id = "401811963"
    rows = [_row("p1", "Scottie Scheffler", 0.11)]
    audit = build_audit(t.tournament_id, RunMode.PRE_TOURNAMENT, rows, "shell-flow")
    audit.extra["source_inventory"] = [
        SourceInventoryItem(
            field_name="player_identification_field",
            source_kind=SourceKind.REAL_LIVE,
            source_name="espn_field",
            coverage="50/50",
        ).model_dump(mode="json")
    ]
    audit.extra["export_txt"] = str(tmp_path / "401811963_live_run.txt")
    result = TournamentRunResult(
        run_id=audit.run_id,
        tournament=t,
        mode=RunMode.PRE_TOURNAMENT,
        ranked=rows,
        audit=audit,
        never_auto_bet=True,
    )

    def _fake_operating(**kwargs):
        result.mode = kwargs["mode"]
        result.audit.extra["export_txt"] = str(tmp_path / f"401811963_{kwargs['mode'].value}_run.txt")
        return result

    monkeypatch.setattr("golf_offshoot.operator_surface.runner.run_operating", _fake_operating)
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    ingest = run_ingest(event_id="401811963", notify=True)
    assert ingest.ok
    assert ingest.event_id == "401811963"
    assert ingest.notice is not None
    assert ingest.notice.sent is False
    assert "Scottie Scheffler" in ingest.table
    assert ingest.inventory
    live = run_live(event_id="401811963", notify=False)
    assert live.ok
    assert live.leftover
    assert "do not stuff into theta" in live.leftover
    loop = run_loop(event_id="401811963", notify=False)
    assert loop.ok
    assert loop.command == "loop"
    assert loop.notice is None


def test_shell_text_and_html_include_walls(tmp_path):
    (tmp_path / "latest").mkdir()
    (tmp_path / "latest" / "401811963_live_x.txt").write_text("real live table\nnever auto-bet\n", encoding="utf-8")
    surface = build_surface(event_id="401811963", artifact_root=tmp_path, viz_root=tmp_path / "viz")
    text = render_text(surface)
    page = render_html(surface)
    assert "PHASE 1 OBSERVATION" in text
    assert CASH_BADGE in text
    assert "NOT ARMED" in text
    assert "Shadow honesty strip" in text
    assert "Calibration weather" in page
    assert "NEVER DEPOSITS" in page
    assert "PAPER OBSERVATION ONLY" in page
    assert "not trading armed" in page
    assert 'value="deposit"' not in page
    assert 'value="paper-deposit"' not in page
    assert 'value="paper-withdraw"' not in page
    assert 'value="cash-out"' not in page
    assert "Kalshi" in page
    assert "not yet available" in page
    assert "notify-first" in page
    assert "<img " not in page


def test_cli_shell_print(tmp_path):
    from golf_offshoot.__main__ import main

    (tmp_path / "latest").mkdir()
    (tmp_path / "latest" / "401811963_live_x.txt").write_text(
        "BMW live ranked\nnever auto-bet\n",
        encoding="utf-8",
    )
    code = main(
        [
            "shell",
            "--print",
            "--event",
            "401811963",
            "--artifact-root",
            str(tmp_path),
            "--viz-root",
            str(tmp_path / "viz"),
        ]
    )
    assert code == 0


def _posted_row(pid: str, name: str, win: float, *, edge: float, posted: float) -> PlayerOutput:
    row = _row(pid, name, win)
    row.edge_by_bet = {"win": edge}
    row.posted_odds_by_bet = {"win": posted}
    row.market_implied_by_bet = {"win": 1.0 / posted}
    return row


def _strategy_status() -> StrategyStatusSummary:
    return StrategyStatusSummary(
        open_exposure=0.0,
        exposure_frac=0.0,
        unrealized_pnl=0.0,
        unrealized_edge_weighted=0.0,
        biggest_concentration="",
        biggest_concentration_frac=0.0,
        posture=StrategyMode.STAY_SELECTIVE,
        cooling_off=False,
        n_positions=0,
        n_suggested_actions=1,
    )


def _live_result(rows, *, operating: bool = True, strategy=None, event_id="401811963"):
    t = demo_tournament()
    t.espn_event_id = event_id
    t.name = "BMW Championship"
    audit = build_audit(event_id, RunMode.LIVE, rows, "shell-paper")
    audit.extra["operating"] = operating
    audit.extra["bankroll"] = 250.0
    audit.extra["odds_book"] = "bovada"
    return TournamentRunResult(
        run_id=audit.run_id,
        tournament=t,
        mode=RunMode.LIVE,
        ranked=rows,
        audit=audit,
        never_auto_bet=True,
        strategy=strategy,
    )


def test_observation_paper_empty_field_is_loud(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    result = _live_result([])
    note = apply_observation_paper(result)
    assert note.status == PAPER_EMPTY_FIELD
    assert note.record is None
    assert not list((tmp_path / "paper").glob("401811963.json")) if (tmp_path / "paper").exists() else True
    assert "not a demo book" in note.text
    assert "NOT ARMED" in note.text


def test_observation_paper_no_posted_odds_is_not_silent_demo(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_row("p1", "Scottie Scheffler", 0.11)]
    note = apply_observation_paper(_live_result(rows, strategy=None))
    assert note.status == PAPER_EMPTY_FIELD
    assert note.record is None
    assert not (tmp_path / "paper" / "401811963.json").exists()
    assert "silent demo fill" in note.text
    assert "NOT ARMED" in note.text


def test_observation_paper_empty_advice_locks_honestly(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_posted_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    result = _live_result(rows, strategy=None)
    note = apply_observation_paper(result)
    assert note.status == PAPER_LOCKED
    assert note.locked is True
    assert note.applied is False
    assert note.record is not None
    assert "PAPER OBSERVATION ONLY" in note.text
    assert "NOT ARMED" in note.text
    assert any("shell auto-lock" in n for n in note.record.notes)


def test_observation_paper_barred_demo_does_not_write(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_posted_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    result = _live_result(rows, operating=False)
    note = apply_observation_paper(result)
    assert note.status == PAPER_BARRED_MOCK
    assert note.record is None
    assert not (tmp_path / "paper" / "401811963.json").exists()


def test_shell_live_auto_applies_paper_advises(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_posted_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    first = apply_observation_paper(_live_result(rows, strategy=None))
    assert first.status == PAPER_LOCKED
    pos = first.record.book.positions[0]
    before = pos.stake
    strategy = StrategyRecommendation(
        recommendation_id=new_id("sr"),
        mode=StrategyMode.STAY_SELECTIVE,
        run_mode=RunMode.LIVE,
        actions=[
            StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.REDUCE,
                player_id=pos.player_id,
                player_name=pos.player_name,
                bet_type=BetType.WIN,
                position_id=pos.position_id,
                suggested_stake_delta=-1.25,
                reason="paper observation reduce",
            )
        ],
        status=_strategy_status(),
    )
    second = apply_observation_paper(_live_result(rows, strategy=strategy))
    assert second.status == PAPER_APPLIED
    assert second.applied is True
    assert second.record.book.positions[0].stake < before
    assert "NOT ARMED" in second.text
    assert "PAPER OBSERVATION ONLY" in second.text
    assert CASH_BADGE in second.text


def test_shell_live_wires_paper_apply(monkeypatch, tmp_path):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rows = [_posted_row("kita", "Kurt Kitayama", 0.089, edge=0.044, posted=17.0)]
    result = _live_result(rows, strategy=None)

    def _fake_operating(**kwargs):
        return result

    monkeypatch.setattr("golf_offshoot.operator_surface.runner.run_operating", _fake_operating)
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    live = run_live(event_id="401811963", notify=False)
    assert live.ok
    assert live.extras.get("paper_status") in {PAPER_LOCKED, PAPER_ADVICE_EMPTY, PAPER_APPLIED}
    assert live.paper
    assert "NOT ARMED" in live.paper
    assert "deposit" not in live.extras
    ingest = run_ingest(event_id="401811963", notify=False)
    assert ingest.ok
    assert ingest.paper == ""
    assert "paper_status" not in ingest.extras
    loop = run_loop(event_id="401811963", notify=False)
    assert loop.ok
    assert loop.command == "loop"
    assert loop.extras.get("paper_status") in {PAPER_LOCKED, PAPER_ADVICE_EMPTY, PAPER_APPLIED}
    assert loop.paper
    page = render_html(
        build_surface(
            event_id="401811963",
            artifact_root=tmp_path,
            viz_root=tmp_path / "viz",
            last_run=live,
        )
    )
    assert "Paper observation (not trading)" in page
    assert PAPER_ONLY in page
    assert 'value="paper-deposit"' not in page
    assert 'value="paper-withdraw"' not in page
    assert 'value="cash-out"' not in page


def test_cash_controls_still_blocked_after_paper_apply():
    for action in ("paper-deposit", "paper-withdraw", "deposit", "withdraw", "cash-out", "transfer"):
        with pytest.raises(OperatorSafetyError) as exc:
            refuse_forbidden(action)
        assert "NOT ARMED" in str(exc.value)
        assert "NEVER DEPOSITS" in str(exc.value)


def test_windows_hub_launcher_files_are_observation_only():
    from golf_offshoot.operator_surface.app import DEFAULT_HOST
    from golf_offshoot.operator_surface.desktop import launcher_paths

    assert DEFAULT_HOST == "127.0.0.1"
    paths = launcher_paths()
    for key in ("open_hub_bat", "install_ps1", "install_bat", "open_hub_sh"):
        assert paths[key].is_file(), key
    bat = paths["open_hub_bat"].read_text(encoding="utf-8")
    assert "python -m golf_offshoot shell" in bat
    assert "127.0.0.1" in bat
    assert "NOT ARMED" in bat
    assert "PAPER OBSERVATION ONLY" in bat
    assert "NEVER DEPOSITS" in bat
    assert "paper-deposit" not in bat.lower()
    assert "kalshi" not in bat.lower()
    ps1 = paths["install_ps1"].read_text(encoding="utf-8")
    assert "Golf Offshoot Phase 1 Hub.lnk" in ps1
    assert "Open-Phase1-Hub.bat" in ps1
    assert "WScript.Shell" in ps1
    assert "NOT ARMED" in ps1


def test_write_desktop_launcher(tmp_path):
    from golf_offshoot.operator_surface.desktop import SHORTCUT_STEM, write_desktop_launcher

    dest = write_desktop_launcher(desktop=tmp_path / "Desktop")
    assert dest.name == f"{SHORTCUT_STEM}.bat"
    text = dest.read_text(encoding="utf-8")
    assert "Open-Phase1-Hub.bat" in text
    assert "NOT ARMED" in text
    assert (tmp_path / "Desktop" / f"{SHORTCUT_STEM}.command").is_file()


def test_cli_install_desktop_shortcut(tmp_path, monkeypatch):
    from golf_offshoot.__main__ import main
    from golf_offshoot.operator_surface.desktop import SHORTCUT_STEM

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    assert main(["shell", "--install-desktop-shortcut"]) == 0
    assert (tmp_path / "Desktop" / f"{SHORTCUT_STEM}.bat").is_file()


def test_hub_html_renders_viz_pngs_when_present(tmp_path):
    viz = tmp_path / "viz"
    viz.mkdir()
    (viz / "shadow_honesty_strip.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (viz / "calibration_weather.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=viz))
    assert page.count("<img ") == 2
    assert "/viz/shadow_honesty_strip.png" in page
    assert "/viz/calibration_weather.png" in page
    assert 'class="missing"' not in page
    assert "Shadow honesty strip" in page
    assert "Calibration weather" in page


def test_hub_puts_viz_wall_above_dense_blocks(tmp_path):
    viz = tmp_path / "viz"
    viz.mkdir()
    (viz / "shadow_honesty_strip.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (viz / "calibration_weather.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (tmp_path / "latest").mkdir()
    (tmp_path / "latest" / "401811963_live_x.txt").write_text("real live table\nnever auto-bet\n", encoding="utf-8")
    page = render_html(build_surface(event_id="401811963", artifact_root=tmp_path, viz_root=viz))
    wall = page.index('class="viz-wall"')
    assert wall < page.index("What you can do here")
    assert wall < page.index("Ranked table")
    assert wall < page.index("Paper journal (shadow log)")
    assert page.index("PHASE 1 OBSERVATION") < wall
    assert page.index(CASH_BADGE) < wall


def test_hub_action_labels_are_plain_and_post_values_unchanged(tmp_path):
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz"))
    for value in ("ingest", "live", "shadow", "loop", "refresh"):
        assert f'value="{value}"' in page
    for label in ("Pull latest data", "Update live ranks", "Check paper journal", "Do all three", "Reload files"):
        assert label in page
    assert ">ingest<" not in page
    assert ">shadow<" not in page
    assert "reload artifacts" not in page


def test_hub_settle_banner_is_loud(tmp_path):
    missing = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz"))
    assert 'class="settle"' in missing
    assert SHADOW_MISSING in missing
    assert "not zero edge" in missing
    _write_jsonl(tmp_path / "shadow" / "advises.jsonl", [_shadow_row()])
    pending = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz"))
    assert 'class="settle"' in pending
    assert SETTLE_PENDING in pending
    assert "not settled cash" in pending
    assert "paper wins 0" in pending


def test_hub_http_serves_viz_pngs(tmp_path):
    from http.client import HTTPConnection
    from http.server import ThreadingHTTPServer
    from threading import Thread

    from golf_offshoot.operator_surface.app import OperatorHandler

    viz = tmp_path / "viz"
    viz.mkdir()
    payload = b"\x89PNG\r\n\x1a\nHUB"
    (viz / "shadow_honesty_strip.png").write_bytes(payload)
    (viz / "calibration_weather.png").write_bytes(payload)
    state = {
        "event_id": "",
        "artifact_root": tmp_path,
        "viz_root": viz,
        "odds_book": "auto",
        "surface": build_surface(artifact_root=tmp_path, viz_root=viz),
    }
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), OperatorHandler)
    httpd.surface_state = state  # type: ignore[attr-defined]
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = httpd.server_address[:2]
        conn = HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/viz/shadow_honesty_strip.png")
        resp = conn.getresponse()
        body = resp.read()
        assert resp.status == 200
        assert body == payload
        conn.request("GET", "/")
        page = conn.getresponse().read().decode("utf-8")
        assert "<img " in page
        assert "/viz/shadow_honesty_strip.png" in page
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_viz_root_prefers_repo_root_pngs_over_empty_shared(tmp_path, monkeypatch):
    from golf_offshoot.operator_surface import paths as pathmod

    empty_ops = tmp_path / "illustrator_ops" / "golf_offshoot"
    empty_ops.mkdir(parents=True)
    offshoot = tmp_path / "offshoot"
    offshoot_docs = offshoot / "docs" / "viz" / "golf_offshoot_dryrun_2026-09-07"
    offshoot_docs.mkdir(parents=True)
    (offshoot_docs / "README.md").write_text("no pngs yet\n", encoding="utf-8")
    repo = tmp_path / "repo"
    root_docs = repo / "docs" / "viz" / "golf_offshoot_dryrun_2026-09-07"
    root_docs.mkdir(parents=True)
    (root_docs / "shadow_honesty_strip.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (root_docs / "calibration_weather.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    monkeypatch.setattr(pathmod, "DEFAULT_EXTERNAL_VIZ_ROOT", empty_ops)
    monkeypatch.setattr(pathmod, "package_root", lambda: offshoot)
    monkeypatch.setattr(pathmod, "git_repo_root", lambda start=None: repo)
    root, src = pathmod.resolve_viz_root(environ={})
    assert root == root_docs.resolve()
    assert src == "repo_root_docs_viz"


def test_viz_root_prefers_live_illustrator_ops_over_repo_fallbacks(tmp_path, monkeypatch):
    from golf_offshoot.operator_surface import paths as pathmod

    ops = tmp_path / "illustrator_ops" / "golf_offshoot"
    ops.mkdir(parents=True)
    (ops / "shadow_honesty_strip.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (ops / "calibration_weather.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (ops / "viz_wall_manifest.json").write_text(
        '{"slots":{"shadow_honesty_strip":{"path":"shadow_honesty_strip.png"},'
        '"calibration_weather":{"path":"calibration_weather.png"}}}',
        encoding="utf-8",
    )
    offshoot = tmp_path / "offshoot"
    offshoot_docs = offshoot / "docs" / "viz" / "golf_offshoot_dryrun_2026-09-07"
    offshoot_docs.mkdir(parents=True)
    (offshoot_docs / "shadow_honesty_strip.png").write_bytes(b"\x89PNG\r\n\x1a\nOLD")
    repo = tmp_path / "repo"
    root_docs = repo / "docs" / "viz" / "golf_offshoot_dryrun_2026-09-07"
    root_docs.mkdir(parents=True)
    (root_docs / "shadow_honesty_strip.png").write_bytes(b"\x89PNG\r\n\x1a\nROOT")
    (root_docs / "calibration_weather.png").write_bytes(b"\x89PNG\r\n\x1a\nROOT")
    monkeypatch.setattr(pathmod, "DEFAULT_EXTERNAL_VIZ_ROOT", ops)
    monkeypatch.setattr(pathmod, "package_root", lambda: offshoot)
    monkeypatch.setattr(pathmod, "git_repo_root", lambda start=None: repo)
    root, src = pathmod.resolve_viz_root(environ={})
    assert root == ops.resolve()
    assert src == "illustrator_ops"


def test_repo_viz_candidates_include_offshoot_and_pr140_root():
    from golf_offshoot.operator_surface.paths import REPO_VIZ_FALLBACK, _repo_viz_candidates, git_repo_root, package_root

    labels = {label: path for path, label in _repo_viz_candidates()}
    assert "repo_docs_viz" in labels
    assert labels["repo_docs_viz"] == (package_root() / REPO_VIZ_FALLBACK).resolve()
    repo = git_repo_root()
    if repo is not None:
        assert "repo_root_docs_viz" in labels
        assert labels["repo_root_docs_viz"] == (repo / REPO_VIZ_FALLBACK).resolve()
        assert labels["repo_root_docs_viz"] != labels["repo_docs_viz"]
