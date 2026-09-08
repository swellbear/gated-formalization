"""3e: every CLERICAL_WHITELIST member has the three serve-on-proof properties.

A role added to the whitelist without them is a red build. X7 recurring in
costume is the exhibit — a timestamp-only rewrite, a passed:false report, or a
silent event source each used to clear or un-owe a clerical role.
"""

from __future__ import annotations

import json

import pytest

from golf_offshoot.learning_lane_15m.learn import (
    DIGESTOR_TRIGGERS,
    OPERATOR_TRIGGERS,
    guarded_events,
    roles_owed_for,
)
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.runner import (
    CLERICAL_CONTRACTS,
    CLERICAL_WHITELIST,
    serve_role,
)
from golf_offshoot.learning_lane_15m.triggers import EVENT_DETECTOR_BLIND


@pytest.mark.parametrize("role", CLERICAL_WHITELIST)
def test_every_whitelist_role_has_a_contract(role):
    assert role in CLERICAL_CONTRACTS
    contract = CLERICAL_CONTRACTS[role]
    assert contract.token is not None
    assert contract.negative_event
    assert contract.event_source
    judicial = set(OPERATOR_TRIGGERS) | set(DIGESTOR_TRIGGERS) | {EVENT_DETECTOR_BLIND}
    assert contract.negative_event in judicial


@pytest.mark.parametrize("role", CLERICAL_WHITELIST)
def test_a_timestamp_only_rewrite_does_not_clear(role, tmp_path):
    set_15m_root_override(tmp_path)
    try:
        (tmp_path / "latest").mkdir(parents=True, exist_ok=True)
        (tmp_path / "latest" / "learning_wake.json").write_text(
            json.dumps({"roles_owed": [{"role": role}], "served": []}),
            encoding="utf-8",
        )
        path, first, second = _clock_pair(role, tmp_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(first, encoding="utf-8")

        def _restamp():
            path.write_text(second, encoding="utf-8")

        result = serve_role(role, do_work=_restamp, root=tmp_path)
        assert result["marked"] is False, result
        assert "heartbeat" in result["reason"]
    finally:
        set_15m_root_override(None)


@pytest.mark.parametrize("role", CLERICAL_WHITELIST)
def test_a_negative_result_does_not_retire_the_finding(role):
    """Serving the role on proof retires the run, never the finding."""
    kind = CLERICAL_CONTRACTS[role].negative_event
    owed = roles_owed_for(kind)
    assert "operator" in owed or "digestor" in owed


@pytest.mark.parametrize("role", CLERICAL_WHITELIST)
def test_a_raising_event_source_owes_operator_not_silence(role):
    name = CLERICAL_CONTRACTS[role].event_source

    def _boom():
        raise RuntimeError(f"{name} cannot see")

    events = guarded_events(name, _boom)
    assert len(events) == 1
    assert events[0]["kind"] == EVENT_DETECTOR_BLIND
    assert events[0]["ticker"] == name
    assert "operator" in roles_owed_for(events[0]["kind"])


def _clock_pair(role: str, tmp_path):
    """Two payloads that differ only by a clock field the token must ignore."""
    from golf_offshoot.learning_lane_15m import runner as R

    if role == "critic-invariants":
        path = tmp_path / R.CRITIC_FINDINGS_REL
        body = {
            "passed": False,
            "checks": [{"id": "a", "state": "FAIL", "detail": "105s old"}],
            "reviewed": [{"sha256": "aaa"}],
        }
        return (
            path,
            json.dumps({**body, "ran_at": "11:00"}),
            json.dumps({**body, "ran_at": "11:30", "checks": [
                {"id": "a", "state": "FAIL", "detail": "195s old"}
            ]}),
        )
    if role == "validator":
        path = tmp_path / R.VALIDATOR_REPORT_REL
        body = {"ok": True, "errors": [], "exit_code": 0, "sha256": "abc"}
        return (
            path,
            json.dumps({**body, "validated_at": "11:00"}),
            json.dumps({**body, "validated_at": "11:30"}),
        )
    if role == "digest-figures":
        path = tmp_path / R.DIGEST_REL
        return (
            path,
            "**Evidence as-of:** 11:00\nbankroll 94.13\n",
            "**Evidence as-of:** 11:30\nbankroll 94.13\n",
        )
    if role == "systems":
        path = tmp_path / R.MANIFEST_REL
        lane = {"id": "learning_lane_15m", "windows": []}
        return (
            path,
            json.dumps({"generated_at": "11:00", "lanes": [lane]}),
            json.dumps({"generated_at": "11:30", "lanes": [lane]}),
        )
    if role == "illustrator":
        png = tmp_path / R.PNG_REL
        png.parent.mkdir(parents=True, exist_ok=True)
        sidecar = tmp_path / "latest" / "board_fingerprint.json"
        sidecar.write_text(json.dumps({"drawn": "same-rows"}), encoding="utf-8")
        return png, "png-bytes-1", "png-bytes-2"
    raise AssertionError(role)
