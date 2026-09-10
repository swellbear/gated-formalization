import json

import pytest
from golf_offshoot.learning_lane_15m.critic import run_only_fee_rows
from golf_offshoot.learning_lane_15m.evidence_bar import (
    bar_is_binding,
    class_is_burned,
    fee_adjust,
    fee_probe_due,
    fragile_not_null,
    gym_fee_tick,
    load_burned_classes,
    load_evidence_bar,
    load_fee_schedule_probe,
    record_fee_schedule_probe,
)


def test_bar_is_a_nonbinding_draft():
    bar = load_evidence_bar()
    assert bar["binding"] is False
    assert bar["admit"] is False
    assert bar["edge_established"] is False
    assert bar["lab_admits"] is False
    assert bar["trading_armed"] is False
    assert bar["distinguishable"]["effect_floor_usd_per_window"] == 0.28
    assert "trials_to_date" in bar["distinguishable"]["alpha"]
    assert bar["verdicts"]["established"]["accepts_replay"] is False
    assert bar["calibration"]["post_declaration_windows_read"] is False
    assert bar_is_binding() is False
    assert bar["discovery_organ"]["consult_enabled"] is False
    assert bar["fee_hurdle"]["expected_fee_type"] == "quadratic"
    assert bar["fee_hurdle"]["expected_fee_multiplier"] == 1
    assert "series_fee_regime_matches" in bar["fee_hurdle"]["series_fee_check"]


def test_the_admit_pass_amendments_are_pinned():
    """What Operator sustained in the admit pass, held in place by a test.

    A bar that can quietly revert to its drafted numbers is not a bar. n went
    40 -> 70 because δ sat at ratio 0.997 of the minimum detectable effect at
    n=40; the null moved off zero because a fee-free EV-zero fill makes
    ``mean(d) <= 0`` known-false before any data; and α gained a summable
    weight because Σ0.05/k diverges to ~15% family-wise error.
    """
    bar = load_evidence_bar()

    assert bar["looks"]["first_look_n"] == 70
    assert bar["distinguishable"]["h0"] == "mean(d) <= delta"
    assert "k * (k + 1)" in bar["distinguishable"]["alpha"]


def test_burned_registry_seeds_oil_and_keeps_moy_cont_fragile():
    burned = load_burned_classes()
    ids = {row["id"] for row in burned["classes"]}
    assert "MAG" in ids
    assert "QUANT" in ids
    assert "RETUNE-COINFLIP-BAND" in ids
    assert class_is_burned("MAG-WEAK") is True
    assert class_is_burned("magnitude-gate") is True
    assert class_is_burned("R-SKIP-COINFLIP") is False
    assert fragile_not_null("H-SPOT-MOY-CONT") is True
    assert class_is_burned("H-SPOT-MOY-CONT") is False


def test_fee_adjust_reproduces_the_run_only_raw_fee_column():
    rows = run_only_fee_rows()
    assert len(rows) >= 8
    for row in rows:
        got = fee_adjust(row["recorded_pnl"], row["mark"], 1.0)
        assert abs(got - row["fee_adjusted_pnl"]) <= 5e-3
        raw = 0.07 * 1.0 * (1.0 - row["mark"])
        assert abs(raw - row["raw_fee"]) <= 5e-4


def test_a_429_does_not_amend_the_bar(tmp_path):
    import json
    from golf_offshoot.learning_lane_15m import critic

    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(json.dumps({"fee_hurdle": {"k": 0.07, "schedule_sha256": ""}}), encoding="utf-8")
    latest = tmp_path / "latest"

    def opener_429(_url, _timeout):
        return 429, b""

    result = record_fee_schedule_probe(opener=opener_429, root=tmp_path, latest_dir=latest)
    payload = json.loads(bar.read_text(encoding="utf-8"))
    probe = load_fee_schedule_probe(latest_dir=latest)

    assert result["status"] == 429
    assert result["sha256"] == ""
    assert result["pinned"] is False
    assert payload["fee_hurdle"]["schedule_sha256"] == ""
    assert probe["status"] == 429
    assert "schedule_checked_at" not in payload["fee_hurdle"] or payload["fee_hurdle"].get(
        "schedule_checked_at"
    ) in (None, "")


def test_a_200_pins_and_a_later_429_keeps_the_hash(tmp_path):
    import hashlib
    import json
    from golf_offshoot.learning_lane_15m import critic

    body = b"%PDF-1.4 gym-fee-schedule-test"
    digest = hashlib.sha256(body).hexdigest()
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(json.dumps({"fee_hurdle": {"k": 0.07, "schedule_sha256": ""}}), encoding="utf-8")
    latest = tmp_path / "latest"

    def opener_200(_url, _timeout):
        return 200, body

    first = record_fee_schedule_probe(opener=opener_200, root=tmp_path, latest_dir=latest)
    assert first["pinned"] is True
    assert json.loads(bar.read_text(encoding="utf-8"))["fee_hurdle"]["schedule_sha256"] == digest

    def opener_429(_url, _timeout):
        return 429, b""

    second = record_fee_schedule_probe(opener=opener_429, root=tmp_path, latest_dir=latest)
    assert second["pinned"] is False
    assert json.loads(bar.read_text(encoding="utf-8"))["fee_hurdle"]["schedule_sha256"] == digest
    assert load_fee_schedule_probe(latest_dir=latest)["status"] == 429


def test_a_placeholder_hash_is_not_writable(tmp_path):
    import json
    from golf_offshoot.learning_lane_15m import critic

    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(json.dumps({"fee_hurdle": {"k": 0.07, "schedule_sha256": ""}}), encoding="utf-8")
    latest = tmp_path / "latest"
    fake = {
        "url": "https://kalshi.com/docs/kalshi-fee-schedule.pdf",
        "checked_at": "2026-09-09T19:51:00-04:00",
        "status": 200,
        "sha256": "not-a-hash",
        "bytes": 4,
        "error": "",
    }
    result = record_fee_schedule_probe(probe=fake, root=tmp_path, latest_dir=latest)
    assert result["pinned"] is False
    assert json.loads(bar.read_text(encoding="utf-8"))["fee_hurdle"]["schedule_sha256"] == ""
    check = critic.check_fee_schedule_hash_recorded(root=tmp_path)
    assert check["state"] == critic.FAIL


def test_fee_probe_cooldown_skips_a_second_fetch(tmp_path):
    import json
    from golf_offshoot.learning_lane_15m import critic

    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(json.dumps({"fee_hurdle": {"k": 0.07, "schedule_sha256": ""}}), encoding="utf-8")
    latest = tmp_path / "latest"
    calls = {"n": 0}

    def opener_429(_url, _timeout):
        calls["n"] += 1
        return 429, b""

    first = gym_fee_tick({}, opener=opener_429, root=tmp_path, latest_dir=latest)
    assert first["probed"] is True
    assert calls["n"] == 1
    assert fee_probe_due(latest_dir=latest) is False

    def opener_must_not_run(_url, _timeout):
        raise AssertionError("cooldown must skip the second fetch")

    second = gym_fee_tick({}, opener=opener_must_not_run, root=tmp_path, latest_dir=latest)
    assert second["probed"] is False
    assert second["skipped_cooldown"] is True
    assert calls["n"] == 1


def test_series_fee_snapshot_absent_does_not_fail_the_suite(tmp_path):
    from golf_offshoot.learning_lane_15m import critic

    check = critic.check_series_fee_regime_matches(root=tmp_path)
    assert check["state"] == critic.PASS
    assert check["evidence"]["snapshot_absent"] is True


def test_series_fee_mismatch_and_missing_field_fail(tmp_path):
    from golf_offshoot.learning_lane_15m import critic
    from golf_offshoot.learning_lane_15m.evidence_bar import write_series_fee_snapshot

    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps(
            {
                "fee_hurdle": {
                    "k": 0.07,
                    "expected_fee_type": "quadratic",
                    "expected_fee_multiplier": 1,
                }
            }
        ),
        encoding="utf-8",
    )
    write_series_fee_snapshot(
        {
            "series": "KXBTC15M",
            "fee_type": "quadratic",
            "fee_multiplier": 0.5,
            "fee_type_present": True,
            "fee_multiplier_present": True,
        },
        root=tmp_path,
    )
    mismatch = critic.check_series_fee_regime_matches(root=tmp_path)
    assert mismatch["state"] == critic.FAIL
    assert "fee_multiplier" in mismatch["detail"]

    write_series_fee_snapshot(
        {
            "series": "KXBTC15M",
            "fee_type": "quadratic",
            "fee_multiplier": None,
            "fee_type_present": True,
            "fee_multiplier_present": False,
        },
        root=tmp_path,
    )
    missing = critic.check_series_fee_regime_matches(root=tmp_path)
    assert missing["state"] == critic.FAIL
    assert "omitted fee_multiplier" in missing["detail"]


def test_score_rule_still_refuses_an_unbound_bar():
    from golf_offshoot.learning_lane_15m.rules import RuleNotScorable, score_rule

    windows = []
    for i in range(70):
        minutes = i * 15
        h, m = divmod(minutes, 60)
        d, h = divmod(h, 24)
        windows.append(
            {
                "window_id": f"SYNTH-{d:02d}{h:02d}{m:02d}",
                "close_at": f"2026-09-09T{h:02d}:{m:02d}:00-04:00",
                "posted_yes": 0.50,
                "recorded_pnl": 0.0,
                "stake": 1.0,
            }
        )
    with pytest.raises(RuleNotScorable, match="not binding"):
        score_rule("R-SKIP-2TO1-FAVORITE", windows)


def test_founder_browser_bytes_pin_the_bar_and_gym_does_not_overwrite(tmp_path):
    import hashlib
    from golf_offshoot.learning_lane_15m import critic
    from golf_offshoot.learning_lane_15m.evidence_bar import apply_founder_fee_pin

    body = b"%PDF-1.7 founder-bytes"
    digest = hashlib.sha256(body).hexdigest()
    pdf = tmp_path / "kalshi-fee-schedule.pdf"
    pdf.write_bytes(body)
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps({"fee_hurdle": {"k": 0.07, "schedule_sha256": "", "schedule_fetch_status": 429}}),
        encoding="utf-8",
    )
    out = apply_founder_fee_pin(pdf, root=tmp_path)
    assert out["sha256"] == digest
    assert out["source"] == "founder_browser_bytes"
    fee = json.loads(bar.read_text(encoding="utf-8"))["fee_hurdle"]
    assert fee["schedule_sha256"] == digest
    assert fee["schedule_pin_source"] == "founder_browser_bytes"
    assert fee["schedule_fetch_status"] == 429
    assert "HTTP 200 gym GET" not in fee["schedule_fetch_note"] or "Not an HTTP 200" in fee["schedule_fetch_note"]

    latest = tmp_path / "latest"

    def opener_200(_url, _timeout):
        return 200, b"%PDF-1.4 other-gym-bytes"

    from golf_offshoot.learning_lane_15m.evidence_bar import record_fee_schedule_probe

    second = record_fee_schedule_probe(opener=opener_200, root=tmp_path, latest_dir=latest)
    assert second["pinned"] is False
    assert json.loads(bar.read_text(encoding="utf-8"))["fee_hurdle"]["schedule_sha256"] == digest


def test_live_fee_pin_is_founder_browser_bytes():
    from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar

    fee = load_evidence_bar()["fee_hurdle"]
    assert fee.get("schedule_pin_source") == "founder_browser_bytes"
    assert len(str(fee.get("schedule_sha256") or "")) == 64

