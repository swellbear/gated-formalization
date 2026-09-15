"""ARM hub scaffold. Separate from learning_lane_15m. Trading NOT ARMED."""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

import pytest

from golf_offshoot.arm_hub.arm import (
    KEY_ID_ENV,
    KEY_PATH_ENV,
    NotArmedError,
    refuse_live_order,
    resolve_mode,
)
from golf_offshoot.arm_hub.bankroll import load_ledger
from golf_offshoot.arm_hub.cli import main as arm_main
from golf_offshoot.arm_hub.executor import submit_order
from golf_offshoot.arm_hub.loop import run_once, run_replay
from golf_offshoot.arm_hub.paths import (
    LearningLanePathRefused,
    assert_not_learning_lane_path,
    default_data_root,
    kill_path,
    set_arm_hub_root_override,
)
from golf_offshoot.arm_hub.strategy_loader import join_shortlist_shelf, load_or_build_policy, load_pins
from golf_offshoot.arm_hub.watch import run_watch, write_kill

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "arm_hub"


def _sandbox(tmp_path: Path) -> Path:
    root = tmp_path / "arm_hub"
    shutil.copytree(SAMPLE, root, ignore=shutil.ignore_patterns("paper", "latest", "audit"))
    (root / "paper" / "fills").mkdir(parents=True)
    (root / "paper" / "settlements").mkdir(parents=True)
    (root / "latest").mkdir(parents=True)
    (root / "audit").mkdir(parents=True)
    return root


@pytest.fixture
def hub(tmp_path):
    root = _sandbox(tmp_path)
    set_arm_hub_root_override(root)
    yield root
    set_arm_hub_root_override(None)


def test_assert_refuses_learning_lane_data_tree(tmp_path):
    bad = tmp_path / "data" / "learning_lane_15m" / "paper" / "ledger.json"
    bad.parent.mkdir(parents=True)
    bad.write_text("{}", encoding="utf-8")
    with pytest.raises(LearningLanePathRefused):
        assert_not_learning_lane_path(bad)


def test_assert_refuses_kalshi_15m_exports(tmp_path):
    bad = tmp_path / "kalshi_15m_exports" / "paper"
    bad.mkdir(parents=True)
    with pytest.raises(LearningLanePathRefused):
        assert_not_learning_lane_path(bad)


def test_sources_do_not_import_learning_lane():
    pkg = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "arm_hub"
    for py in pkg.glob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "learning_lane_15m" not in alias.name
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("golf_offshoot.learning_lane_15m")
                assert "learning_lane_15m" not in node.module


def test_default_data_root_is_sibling_not_learning_lane():
    root = default_data_root()
    assert root.name == "arm_hub"
    assert "learning_lane_15m" not in root.parts


def test_paper_mode_without_arm_flag(hub):
    runtime = resolve_mode(hub, environ={})
    assert runtime.mode == "paper"
    assert runtime.trading_armed is False
    assert runtime.live_arm_flag is False
    assert (hub / "latest" / "ARM.flag").is_file() is False


def test_arm_flag_without_keys_stays_paper(hub):
    (hub / "latest" / "ARM.flag").write_text("live\n", encoding="utf-8")
    runtime = resolve_mode(hub, environ={})
    assert runtime.mode == "paper"
    assert runtime.trading_armed is False
    assert runtime.live_arm_flag is True


def test_kill_writes_arm_hub_kill_only(hub, tmp_path):
    lane_kill = tmp_path / "data" / "learning_lane_15m" / "latest" / "KILL"
    lane_kill.parent.mkdir(parents=True)
    rc = arm_main(["--kill", "--root", str(hub)])
    assert rc == 0
    assert kill_path(hub).is_file()
    assert not lane_kill.is_file()


def test_cli_kill_does_not_create_learning_lane_dirs(hub, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    arm_main(["--kill", "--root", str(hub)])
    assert not (tmp_path / "data" / "learning_lane_15m").exists()


def test_strategy_join_prefers_keep(hub):
    shortlist, shelf = load_pins(hub)
    rows = join_shortlist_shelf(shortlist, shelf, prefer_keep_only=True)
    ids = {r["id"] for r in rows}
    assert "KEEP-PATH-01" in ids
    assert "KEEP-PATH-02" in ids
    assert "DEAD-PATH-09" not in ids
    policy = load_or_build_policy(hub, rebuild=True)
    ids_policy = {r["id"] for r in policy["rules"]}
    assert "INVENT-PACK-99" not in ids_policy
    jsonl = (hub / "strategies" / "strategy_bridge_keepers.jsonl").read_text(encoding="utf-8")
    assert "KEEP-PATH-01" in jsonl
    assert "INVENT-PACK-99" not in jsonl
    assert all(r.get("lab_admits") is False for r in policy["rules"])
    assert all(r.get("trading_armed") is False for r in policy["rules"])
    assert all(r.get("hub_untouched") is True for r in policy["rules"])


def test_paper_replay_accumulates_from_500(hub):
    results = run_replay(hub)
    ledger = load_ledger(hub)
    assert ledger.starting_bankroll == 500.0
    assert ledger.never_daily_reset is True
    assert any(r.action == "fill" for r in results)
    assert any(r.settlement for r in results)
    assert ledger.bankroll != 500.0
    assert ledger.fees_paid > 0
    assert len(ledger.entries) >= 2
    # Second window is a coinflip — contextual skip, not always-fire.
    assert any(r.action == "skip" for r in results)
    assert ledger.trading_armed is False


def test_one_tick_paper_without_keys(hub):
    tick = run_once(hub, quotes_source="replay")
    assert tick.trading_armed is False
    assert tick.mode == "paper"
    assert tick.banner == "NOT ARMED"


def test_armed_false_refuses_live_orders(hub):
    runtime = resolve_mode(hub, environ={})
    with pytest.raises(NotArmedError):
        refuse_live_order(runtime, intent_note="test")


def test_submit_order_refuses_when_flag_and_keys_claim_live(hub, tmp_path):
    key = tmp_path / "arm.key"
    key.write_text("-----BEGIN RSA PRIVATE KEY-----\nnot-a-real-key\n", encoding="utf-8")
    (hub / "latest" / "ARM.flag").write_text("live\n", encoding="utf-8")
    runtime = resolve_mode(
        hub,
        environ={KEY_ID_ENV: "demo-id", KEY_PATH_ENV: str(key)},
    )
    assert runtime.mode == "live"
    from golf_offshoot.arm_hub.bankroll import empty_ledger
    from golf_offshoot.arm_hub.executor import OrderIntent

    intent = OrderIntent(
        ticker="KXBTC15M-X",
        event_ticker="KXBTC15M-X",
        side="yes",
        yes_price=0.4,
        stake=10.0,
        fee=0.42,
        rule_id="KEEP-PATH-01",
        claim="",
        dsl="",
        reason="test",
    )
    with pytest.raises(NotArmedError):
        submit_order(intent, runtime, empty_ledger(), root=hub)


def test_watch_respects_kill(hub):
    write_kill(hub)
    assert run_watch(hub, interval_s=0, max_ticks=3, sleep=False) == 0


def test_watch_two_ticks_then_kill(hub):
    rc = run_watch(hub, interval_s=0, max_ticks=2, quotes_source="replay", sleep=False)
    assert rc == 0
    assert (hub / "paper" / "ledger.json").is_file()


def test_golf_offshoot_arm_hub_cli(hub):
    from golf_offshoot.__main__ import main

    rc = main(["arm-hub", "--status", "--root", str(hub)])
    assert rc == 0


def test_cli_help_lists_arm_hub(capsys):
    from golf_offshoot.__main__ import main

    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    assert "arm-hub" in capsys.readouterr().out


def test_refuses_port_8765(hub):
    rc = arm_main(["--port", "8765", "--root", str(hub)])
    assert rc == 2
