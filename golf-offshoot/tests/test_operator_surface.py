import os
from pathlib import Path

from golf_offshoot.audit.journal import build_audit
from golf_offshoot.demo import demo_tournament
from golf_offshoot.models.enums import Horizon, RunMode, SourceKind
from golf_offshoot.models.schemas import (
    HorizonProbability,
    PlayerOutput,
    ProbabilityBundle,
    ReliabilityScore,
    SourceInventoryItem,
    TournamentRunResult,
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
from golf_offshoot.operator_surface.modes import CASH_BADGE, MODE_MOCK, MODE_OPERATING, build_mode_walls
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
    assert CASH_BADGE in ops.badges
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
    monkeypatch.setattr("golf_offshoot.operator_surface.runner.load_paper_book", lambda *_a, **_k: None)
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
    assert 'value="deposit"' not in page
    assert 'value="paper-deposit"' not in page
    assert "Kalshi" in page


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
