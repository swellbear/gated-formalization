"""The invariant ratchet: each check here is a flaw that already happened once."""

from __future__ import annotations

import json

from golf_offshoot.learning_lane_15m import digest as digest_mod
from golf_offshoot.learning_lane_15m import invariants as inv
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override


def _watch(**over):
    payload = {
        "running": True,
        "cycles": 12,
        "interval_s": 90.0,
        "last_at": inv.isoformat_now(),
        "runtime": inv.runtime_stamp(),
    }
    payload.update(over)
    return payload


# ----------------------------------------------------------------- 1. digest


def _seed_digest(tmp_path, text: str):
    path = digest_mod.digest_path(root=tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_digest_that_matches_the_ledger_passes(tmp_path, monkeypatch):
    _seed_digest(tmp_path, "- `starting_bankroll` 100.0 -> `bankroll` 90.36 - `betting_pnl` -9.64\n")
    monkeypatch.setattr(
        digest_mod,
        "collect_figures",
        lambda **_: {"bankroll": 90.36, "betting_pnl": -9.64, "journal_generated_at": "x"},
    )

    check = inv.check_digest_matches_ledger(root=tmp_path)

    assert check["state"] == inv.PASS


def test_a_digest_behind_the_ledger_fails_and_names_the_drift(tmp_path, monkeypatch):
    # The live defect: figures as-of 08:51 while the book had moved $1.24.
    _seed_digest(tmp_path, "- `starting_bankroll` 100.0 -> `bankroll` 89.12 - `betting_pnl` -10.88\n")
    monkeypatch.setattr(
        digest_mod,
        "collect_figures",
        lambda **_: {"bankroll": 90.36, "betting_pnl": -9.64, "journal_generated_at": "x"},
    )

    check = inv.check_digest_matches_ledger(root=tmp_path)

    assert check["state"] == inv.FAIL
    assert check["evidence"]["bankroll_drift"] == 1.24
    assert "89.12" in check["detail"] and "90.36" in check["detail"]


def test_a_missing_digest_is_a_failure_not_a_pass(tmp_path):
    assert inv.check_digest_matches_ledger(root=tmp_path)["state"] == inv.FAIL


# ---------------------------------------------------------------- 2. process


def test_a_loop_running_the_code_on_disk_passes():
    assert inv.check_process_matches_disk(_watch())["state"] == inv.PASS


def test_a_loop_on_a_stale_role_order_fails():
    # Exactly the #176 case: the hub kept the pre-merge ROLE_ORDER and
    # whitelist, so digest-figures was never named and validator never served.
    stale = inv.runtime_stamp()
    stale["role_order"] = ["digestor", "operator", "systems", "validator"]
    stale["clerical_whitelist"] = ["illustrator", "systems", "digestor"]

    check = inv.check_process_matches_disk(_watch(runtime=stale))

    assert check["state"] == inv.FAIL
    assert set(check["evidence"]["divergent"]) == {"role_order", "clerical_whitelist"}
    assert "stale code" in check["detail"]


def test_no_runtime_stamp_cannot_prove_a_fresh_process():
    check = inv.check_process_matches_disk({"running": True, "cycles": 3})

    assert check["state"] == inv.FAIL
    assert "no runtime config" in check["detail"]


# --------------------------------------------------------------- 3. liveness


def test_a_watch_writing_cycles_passes():
    assert inv.check_watch_is_collecting(_watch())["state"] == inv.PASS


def test_a_frozen_clock_fails_even_though_the_file_looks_healthy():
    # A re-exec that never comes back leaves running=true and a stale last_at.
    frozen = _watch(last_at="2026-09-08T09:00:00-04:00", cycles=999)

    check = inv.check_watch_is_collecting(frozen)

    assert check["state"] == inv.FAIL
    assert "not collecting" in check["detail"]


def test_a_stopped_watch_fails():
    assert inv.check_watch_is_collecting(_watch(running=False))["state"] == inv.FAIL


def test_a_counter_reset_after_a_reexec_is_noted_not_failed():
    previous = {"checks": [{"id": "watch_is_collecting", "evidence": {"cycles": 53}}]}

    check = inv.check_watch_is_collecting(_watch(cycles=2), previous=previous)

    assert check["state"] == inv.PASS
    assert "counter reset" in check["detail"]


# ---------------------------------------------------------------- 4. arrears


def test_a_clerical_role_owed_past_two_ticks_is_a_defect():
    state = {"roles_owed": [{"role": "validator", "age_s": 5400, "age_text": "1h 30m"}]}

    check = inv.check_clerical_roles_clear(state, watch_status=_watch())

    assert check["state"] == inv.FAIL
    assert check["evidence"]["arrears"][0]["role"] == "validator"


def test_a_judicial_role_owed_for_hours_is_not_arrears():
    # Operator is meant to sit owed until a human rules. That is not a defect.
    state = {"roles_owed": [{"role": "operator", "age_s": 9000, "age_text": "2h 30m"}]}

    assert inv.check_clerical_roles_clear(state, watch_status=_watch())["state"] == inv.PASS


def test_a_fresh_clerical_owed_line_is_not_arrears():
    state = {"roles_owed": [{"role": "digest-figures", "age_s": 30, "age_text": "30s"}]}

    assert inv.check_clerical_roles_clear(state, watch_status=_watch())["state"] == inv.PASS


# ------------------------------------------------------------------- report


def test_the_suite_writes_a_machine_readable_report(tmp_path, monkeypatch):
    set_15m_root_override(tmp_path)
    try:
        monkeypatch.setattr(
            digest_mod,
            "collect_figures",
            lambda **_: {"bankroll": 1.0, "betting_pnl": 0.0, "journal_generated_at": "x"},
        )
        report = inv.run_invariants(
            root=tmp_path,
            state={"roles_owed": []},
            watch_status=_watch(),
        )
        path = inv.write_invariants(report)

        on_disk = json.loads(path.read_text(encoding="utf-8"))
        assert [c["id"] for c in on_disk["checks"]] == [
            "digest_matches_ledger",
            "process_matches_disk",
            "watch_is_collecting",
            "clerical_roles_clear",
        ]
        # No digest on a scratch tree, so the suite must not report all-clear.
        assert on_disk["passed"] is False
        assert on_disk["failing"] == ["digest_matches_ledger"]
    finally:
        set_15m_root_override(None)


def test_a_failing_check_names_itself_on_the_tick():
    report = {
        "ran_at": "2026-09-08T10:37:33-04:00",
        "checks": [
            {"id": "digest_matches_ledger", "title": "t", "state": "FAIL", "detail": "drift 1.24"},
            {"id": "watch_is_collecting", "title": "t2", "state": "PASS", "detail": "ok"},
        ],
    }

    lines = inv.format_invariants(report)

    assert "1 FAILING" in lines[0]
    assert any("drift 1.24" in line for line in lines)
    assert not any("ok" in line for line in lines[1:])
