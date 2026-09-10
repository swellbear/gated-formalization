"""Parts 2, 4 and 5: who a tick owes, when Operator clears, and the Critic's body."""

from __future__ import annotations

import json

from golf_offshoot.learning_lane_15m import critic, triggers
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.learn import (
    CRITIC_INVARIANTS_ROLE,
    LAB_ROLE,
    ROUTINE_ROLES,
    SOFTEN_CRITIC_ROLE,
    roles_owed_for,
)
from golf_offshoot.learning_lane_15m.runner import (
    CLERICAL_WHITELIST,
    JUDICIAL_NEVER,
    operator_write_addresses_owed,
)


# ------------------------------------------- Part 4: Operator stops over-firing


def test_a_routine_settle_owes_nobody_judicial():
    for kind in ("new_settle", "new_fill", "pending_cleared"):
        owed = roles_owed_for(kind)
        assert owed == list(ROUTINE_ROLES), kind
        assert "operator" not in owed, kind
        assert "digestor" not in owed, kind


def test_each_operator_exception_names_operator():
    for kind in (
        triggers.EVENT_PARK_AGED,
        triggers.EVENT_SETTLE_CONTRADICTS_BOOK,
        triggers.EVENT_PAPER_JOIN_MISSING_GREW,
        triggers.EVENT_WINDOW_SEQUENCE_GAP,
        triggers.EVENT_FALSIFIER_FIRED,
        triggers.EVENT_RULE_REACHED_N,
        triggers.EVENT_LAB_PROPOSED,
    ):
        assert "operator" in roles_owed_for(kind), kind


# --------------------------------- Part 2: human digestor has triggers again


def test_each_digestor_exception_names_digestor():
    # Not zero and not every settle: the five cases where the generated
    # figures cannot express what changed.
    for kind in (
        triggers.EVENT_PAPER_JOIN_MISSING_GREW,
        triggers.EVENT_BOOK_OPEN_NO_JOIN,
        triggers.EVENT_WINDOW_SEQUENCE_GAP,
        triggers.EVENT_SETTLE_CONTRADICTS_BOOK,
        triggers.EVENT_UNRECORDED_COST,
    ):
        assert "digestor" in roles_owed_for(kind), kind


def test_a_growing_missing_join_list_owes_digestor():
    previous = {"paper_join_missing": [{"ticker": "A"}]}
    current = {"paper_join_missing": [{"ticker": "A"}, {"ticker": "B"}]}

    events = triggers.paper_join_missing_grew(previous, current)

    assert [e["ticker"] for e in events] == ["B"]
    assert "digestor" in roles_owed_for(events[0]["kind"])


def test_a_hole_in_the_window_sequence_is_raised_once():
    def scan(*starts):
        return {
            "settled": {
                f"T{i}": {"window_id": f"KXBTC15M-x__{s}__y"} for i, s in enumerate(starts)
            }
        }

    # 14:00, 14:15, then a jump to 14:45 — one window missing.
    current = scan("2026-09-08T14:00:00Z", "2026-09-08T14:15:00Z", "2026-09-08T14:45:00Z")
    events = triggers.window_sequence_gaps(scan("2026-09-08T14:00:00Z"), current)

    assert len(events) == 1
    assert "1 window(s) missing" in events[0]["detail"]
    assert "Do not backfill" in events[0]["detail"]


def test_an_unbroken_sequence_raises_nothing():
    scan = {
        "settled": {
            "A": {"window_id": "KXBTC15M-a__2026-09-08T14:00:00Z__y"},
            "B": {"window_id": "KXBTC15M-b__2026-09-08T14:15:00Z__y"},
        }
    }
    assert triggers.window_sequence_gaps({"settled": {}}, scan) == []


# ------------------------------- Part 4: Operator stops clearing falsely


def test_an_unrelated_park_write_does_not_clear_operator(tmp_path):
    # #174 edited the park to reconcile Hard NO lists and cleared an Operator
    # line raised by settles nothing had ruled on.
    state = {
        "roles_owed": [
            {"role": "operator", "reasons": ["new_settle KXBTC15M-26SEP080745-45"]}
        ]
    }
    park = tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_METHOD_PARK.md"
    park.parent.mkdir(parents=True, exist_ok=True)
    park.write_text("reconciled the Soften Critic Hard NO lists\n", encoding="utf-8")

    verdict = operator_write_addresses_owed(state, root=tmp_path)

    assert verdict["material"] is False
    assert "080745" in verdict["why"]


def test_a_park_write_that_names_the_owed_window_clears_operator(tmp_path):
    state = {
        "roles_owed": [
            {"role": "operator", "reasons": ["new_settle KXBTC15M-26SEP080745-45"]}
        ]
    }
    park = tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_METHOD_PARK.md"
    park.parent.mkdir(parents=True, exist_ok=True)
    park.write_text("ruled KXBTC15M-26SEP080745-45 CLOSED on its falsifier\n", encoding="utf-8")

    verdict = operator_write_addresses_owed(state, root=tmp_path)

    assert verdict["material"] is True
    assert verdict["matched"] == ["new_settle KXBTC15M-26SEP080745-45"]


def test_an_owed_line_with_no_reason_leaves_operator_owed(tmp_path):
    # If unsure, it stays owing Operator. An exception class is never dropped
    # to shorten the list.
    verdict = operator_write_addresses_owed(
        {"roles_owed": [{"role": "operator", "reasons": []}]}, root=tmp_path
    )
    assert verdict["material"] is False


# ----------------------------------------------- Part 5: the Critic has a body


def test_the_critic_is_split_across_the_trust_boundary():
    assert CRITIC_INVARIANTS_ROLE in CLERICAL_WHITELIST
    assert CRITIC_INVARIANTS_ROLE not in JUDICIAL_NEVER
    assert SOFTEN_CRITIC_ROLE in JUDICIAL_NEVER
    assert SOFTEN_CRITIC_ROLE not in CLERICAL_WHITELIST


def test_a_repo_side_event_can_name_the_critic_owed():
    owed = roles_owed_for(triggers.EVENT_ARTIFACT_UNREVIEWED)
    assert owed == [CRITIC_INVARIANTS_ROLE, SOFTEN_CRITIC_ROLE]


def test_a_lab_proposed_arriving_also_owes_operator():
    owed = roles_owed_for(triggers.EVENT_ARTIFACT_UNREVIEWED, also_owes=("operator",))
    assert "operator" in owed
    assert SOFTEN_CRITIC_ROLE in owed


def test_an_unreviewed_artifact_is_named_and_a_reviewed_one_is_not(tmp_path):
    bar = tmp_path / critic.BAR_MD_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text("# bar v1\n", encoding="utf-8")

    named = {row["id"] for row in critic.unreviewed(root=tmp_path)}
    assert "evidence_bar" in named

    digest = critic.artifact_digest(critic.WATCHED[0], root=tmp_path)
    critic.write_critic_findings(
        {"reviewed": [{"id": "evidence_bar", "sha256": digest["sha256"]}]}, root=tmp_path
    )
    assert "evidence_bar" not in {row["id"] for row in critic.unreviewed(root=tmp_path)}

    # Editing the bar re-owes the Critic on the new text.
    bar.write_text("# bar v2\n", encoding="utf-8")
    assert "evidence_bar" in {row["id"] for row in critic.unreviewed(root=tmp_path)}


def test_the_findings_artifact_is_the_proof(tmp_path):
    path = critic.write_critic_findings(
        critic.run_critic_invariants(root=tmp_path), root=tmp_path
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["role"] == "critic-invariants"
    assert [c["id"] for c in payload["checks"]] == [
        "matched_exposure_control",
        "delta_above_detection_floor",
        "holdout_is_forward_only",
        "fee_adjusted_book_is_binding",
        "declared_at_precedes_scored_windows",
        "trials_counter_is_consistent",
        "fee_schedule_hash_recorded",
        "series_fee_regime_matches",
        "bind_has_no_founder_read_once",
        "half_spread_profile_recorded",
        "hub_autostart_registered",
    ]
    assert [c["id"] for c in payload["desk_checks"]] == ["honesty_stamp_is_fresh"]


# ------------------------------------- Part 6: the ratchet catches the bar


def test_a_delta_at_its_own_detection_floor_fails(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps(
            {
                "looks": {"first_look_n": 40},
                "distinguishable": {
                    "effect_floor_usd_per_window": 0.28,
                    "effect_floor_rationale": "sd ~0.66 => SE_40 ~0.104; 2.69*SE ~0.28",
                },
            }
        ),
        encoding="utf-8",
    )

    check = critic.check_delta_above_detection_floor(root=tmp_path)

    assert check["state"] == critic.FAIL
    # The check now reads the bar's H0. A draft with no h0, or a zero-null
    # design with δ sitting on its own MDE, is a fail either way.
    ev = check["evidence"]
    if "delta_over_zero_null_mde" in ev:
        assert ev["delta_over_zero_null_mde"] < 1.10
    else:
        assert ev.get("h0") in (None, "") or "null" in check["detail"]


def test_a_skip_scored_as_zero_against_a_filling_baseline_fails(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps({"distinguishable": {"contrast": "d_i = a - b", "skip_contributes": 0}}),
        encoding="utf-8",
    )

    assert critic.check_matched_exposure(root=tmp_path)["state"] == critic.FAIL


def test_an_index_sliced_holdout_fails(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps({"looks": {"held_out_windows": "eligible windows 41 through 80"}}),
        encoding="utf-8",
    )

    assert critic.check_holdout_is_forward_only(root=tmp_path)["state"] == critic.FAIL


def test_a_rule_scored_before_it_was_declared_fails(tmp_path):
    reg = tmp_path / critic.REGISTRY_REL
    reg.parent.mkdir(parents=True, exist_ok=True)
    reg.write_text(
        json.dumps(
            {
                "rules": [
                    {
                        "id": "R-X",
                        "declared_at": "2026-09-08T05:56:00-04:00",
                        "scored_windows": [{"close_at": "2026-09-08T04:00:00-04:00"}],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    check = critic.check_declared_at_precedes_scored_windows(root=tmp_path)

    assert check["state"] == critic.FAIL
    assert check["evidence"]["violations"][0]["rule"] == "R-X"


# ------------ X7: what the Critic found in the Critic's own body, and the fix


def test_a_timestamp_only_rewrite_does_not_clear_the_critic(tmp_path):
    # run_critic_invariants stamps ran_at and checked_at every pass, so the raw
    # file hash moves on a heartbeat. The proof token must follow the verdicts.
    from golf_offshoot.learning_lane_15m.runner import _critic_token

    path = tmp_path / "findings.json"
    checks = [{"id": "a", "state": "FAIL", "detail": "why"}]
    path.write_text(
        json.dumps({"ran_at": "11:00", "passed": False, "checks": checks}), encoding="utf-8"
    )
    first = _critic_token(path)

    path.write_text(
        json.dumps({"ran_at": "11:30", "passed": False, "checks": checks}), encoding="utf-8"
    )
    assert _critic_token(path) == first

    checks[0]["state"] = "PASS"
    path.write_text(
        json.dumps({"ran_at": "11:30", "passed": True, "checks": checks}), encoding="utf-8"
    )
    assert _critic_token(path) != first


def test_serve_role_does_not_clear_the_critic_on_a_heartbeat(tmp_path):
    # Operator's admit pass caught this: _critic_token was wired only into the
    # human artifact-proof path, and serve_role still compared raw fingerprints
    # including ran_at, so the runner cleared the role every tick regardless.
    from golf_offshoot.learning_lane_15m import runner as R

    set_15m_root_override(tmp_path)
    try:
        (tmp_path / "latest").mkdir(parents=True, exist_ok=True)
        (tmp_path / "latest" / "learning_wake.json").write_text(
            json.dumps({"roles_owed": [{"role": "critic-invariants"}], "served": []}),
            encoding="utf-8",
        )
        dest = tmp_path / R.CRITIC_FINDINGS_REL
        dest.parent.mkdir(parents=True, exist_ok=True)
        verdicts = {
            "passed": False,
            "checks": [{"id": "a", "state": "FAIL", "detail": "why"}],
            "reviewed": [{"id": "bar", "sha256": "deadbeef"}],
        }
        dest.write_text(json.dumps({**verdicts, "ran_at": "11:00"}), encoding="utf-8")

        def _restamp_only():
            dest.write_text(json.dumps({**verdicts, "ran_at": "11:30"}), encoding="utf-8")

        heartbeat = R.serve_role("critic-invariants", do_work=_restamp_only, root=tmp_path)
        assert heartbeat["marked"] is False
        assert "heartbeat" in heartbeat["reason"]

        def _new_verdict():
            moved = {**verdicts, "checks": [{"id": "a", "state": "PASS", "detail": "fixed"}]}
            dest.write_text(json.dumps({**moved, "ran_at": "11:45"}), encoding="utf-8")

        real = R.serve_role("critic-invariants", do_work=_new_verdict, root=tmp_path)
        assert real["marked"] is True
    finally:
        set_15m_root_override(None)


def test_reviewing_a_new_artifact_hash_is_real_work(tmp_path):
    # Guard against the opposite failure: if only the checks counted, a run
    # that reviewed a newly-changed bar would never clear and the role would
    # deadlock once artifact_unreviewed stopped firing.
    from golf_offshoot.learning_lane_15m.runner import critic_verdicts

    base = {"passed": True, "checks": [{"id": "a", "state": "PASS", "detail": "ok"}]}
    before = {**base, "reviewed": [{"sha256": "aaa"}]}
    after = {**base, "reviewed": [{"sha256": "bbb"}]}

    assert critic_verdicts(before) != critic_verdicts(after)


def test_a_failing_findings_report_owes_operator(tmp_path):
    # A failing method check may not be retired by the machine that found it.
    critic.write_critic_findings(
        {"passed": False, "failing": ["delta_above_detection_floor"], "checks": []},
        root=tmp_path,
    )

    events = triggers.critic_findings_failing(wake={}, root=tmp_path)

    assert len(events) == 1
    assert "delta_above_detection_floor" in events[0]["detail"]
    # Owes the judicial role that owns the bar, and nobody else. A failing
    # method check does not need the digest regenerated.
    assert roles_owed_for(events[0]["kind"]) == ["operator"]


def test_a_passing_findings_report_owes_nobody(tmp_path):
    critic.write_critic_findings({"passed": True, "failing": [], "checks": []}, root=tmp_path)
    assert triggers.critic_findings_failing(wake={}, root=tmp_path) == []


def test_the_same_disclosed_failing_set_does_not_reowe_operator(tmp_path):
    # 4a: empty schedule_sha256 after a recorded 429 is already on the bar's
    # face. Re-paging Operator for it every tick is the judicial heartbeat.
    critic.write_critic_findings(
        {"passed": False, "failing": ["fee_schedule_hash_recorded"], "checks": []},
        root=tmp_path,
    )
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps({"binding_conditions": [{"detail": "fee_schedule_hash_recorded still FAILS"}]}),
        encoding="utf-8",
    )
    already = {
        "events": [
            {
                "kind": triggers.EVENT_CRITIC_FINDINGS_FAILING,
                "critic_failing": ["fee_schedule_hash_recorded"],
            }
        ]
    }

    assert triggers.critic_findings_failing(wake=already, root=tmp_path) == []


def test_a_new_failing_check_does_reowe_operator(tmp_path):
    critic.write_critic_findings(
        {
            "passed": False,
            "failing": ["fee_schedule_hash_recorded", "matched_exposure_control"],
            "checks": [],
        },
        root=tmp_path,
    )
    already = {
        "events": [
            {
                "kind": triggers.EVENT_CRITIC_FINDINGS_FAILING,
                "critic_failing": ["fee_schedule_hash_recorded"],
            }
        ]
    }

    events = triggers.critic_findings_failing(wake=already, root=tmp_path)
    assert len(events) == 1
    assert "matched_exposure_control" in events[0]["detail"]


def test_leftover_settle_reasons_are_dropped_from_judicial_lines():
    from golf_offshoot.learning_lane_15m.learn import rekey_leftover_owed

    leftover = [
        {
            "role": "digestor",
            "reasons": [
                "new_settle KXBTC15M-26SEP081000-00",
                "pending_cleared KXBTC15M-26SEP081000-00",
            ],
        },
        {
            "role": "operator",
            "reasons": [
                "new_settle KXBTC15M-26SEP080845-45",
                "artifact_unreviewed lab_proposed",
                "critic_findings_failing critic-invariants",
            ],
        },
        {"role": "soften-critic", "reasons": ["artifact_unreviewed evidence_bar"]},
    ]

    cleaned = rekey_leftover_owed(leftover, drop_disclosed_critic_failing=True)
    by_role = {row["role"]: row["reasons"] for row in cleaned}
    assert "digestor" not in by_role
    assert by_role["operator"] == ["artifact_unreviewed lab_proposed"]
    assert by_role["soften-critic"] == ["artifact_unreviewed evidence_bar"]


def test_critic_verdicts_ignore_a_clock_in_detail():
    from golf_offshoot.learning_lane_15m.runner import critic_verdicts

    a = {
        "passed": False,
        "checks": [{"id": "honesty_stamp_is_fresh", "state": "FAIL", "detail": "105s old"}],
        "reviewed": [{"sha256": "aaa"}],
    }
    b = {
        "passed": False,
        "checks": [{"id": "honesty_stamp_is_fresh", "state": "FAIL", "detail": "195s old"}],
        "reviewed": [{"sha256": "aaa"}],
    }
    assert critic_verdicts(a) == critic_verdicts(b)


def test_a_blind_detector_raises_instead_of_reporting_nothing(monkeypatch):
    from golf_offshoot.learning_lane_15m import learn

    def _boom(**_):
        raise RuntimeError("cannot read the tree")

    monkeypatch.setattr(critic, "unreviewed", _boom)
    monkeypatch.setattr(learn, "repo_events", learn.repo_events)
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.paths.has_15m_root_override", lambda: False
    )

    events = learn.repo_events()

    assert len(events) == 1
    assert events[0]["kind"] == triggers.EVENT_DETECTOR_BLIND
    assert "not a detector that saw nothing" in events[0]["detail"]
    assert "operator" in roles_owed_for(events[0]["kind"])


def test_an_unpinned_fee_schedule_fails(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(json.dumps({"fee_hurdle": {"k": 0.07}}), encoding="utf-8")

    check = critic.check_fee_schedule_hash_recorded(root=tmp_path)

    assert check["state"] == critic.FAIL
    assert "habit" in check["detail"]


def test_bind_has_no_founder_read_once_passes_on_empty_scratch_bar(tmp_path):
    check = critic.check_bind_has_no_founder_read_once(root=tmp_path)
    assert check["state"] == critic.PASS


def test_bind_has_no_founder_read_once_fails_if_the_id_returns(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps(
            {
                "binding_rule": "crew only",
                "binding_conditions": [{"id": "founder_read_once", "met": False}],
            }
        ),
        encoding="utf-8",
    )
    check = critic.check_bind_has_no_founder_read_once(root=tmp_path)
    assert check["state"] == critic.FAIL
    assert "founder_read_once" in check["detail"]


def test_bind_has_no_founder_read_once_fails_on_numbered_gate(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps(
            {
                "binding_rule": (
                    "Becomes binding only after (1) crew; (2) machine; "
                    "and (3) Founder read-once acknowledgement."
                )
            }
        ),
        encoding="utf-8",
    )
    check = critic.check_bind_has_no_founder_read_once(root=tmp_path)
    assert check["state"] == critic.FAIL


def test_bind_has_no_founder_read_once_fails_on_dropped_md_gate(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    md = tmp_path / critic.BAR_MD_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text("{}", encoding="utf-8")
    md.write_text("3. Founder reads it once and acknowledges.\n", encoding="utf-8")
    check = critic.check_bind_has_no_founder_read_once(root=tmp_path)
    assert check["state"] == critic.FAIL


def test_bind_has_no_founder_read_once_allows_dropped_notice(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    md = tmp_path / critic.BAR_MD_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps(
            {
                "binding_rule": (
                    "Becomes binding only after (1) Critic+Operator; "
                    "and (2) critic-invariants. Founder read-once is not a bind condition."
                )
            }
        ),
        encoding="utf-8",
    )
    md.write_text(
        "Founder read-once is **not** a bind condition (dropped 2026-09-09).\n",
        encoding="utf-8",
    )
    check = critic.check_bind_has_no_founder_read_once(root=tmp_path)
    assert check["state"] == critic.PASS


def test_live_factory_bar_has_no_founder_read_once_bind_condition():
    from golf_offshoot.operator_surface.observability import repo_root

    check = critic.check_bind_has_no_founder_read_once(root=repo_root())
    assert check["state"] == critic.PASS


def test_half_spread_profile_fails_when_unmeasured(tmp_path):
    check = critic.check_half_spread_profile(root=tmp_path)
    assert check["state"] == critic.FAIL
    assert check["id"] == "half_spread_profile_recorded"


def test_half_spread_profile_passes_when_named_and_measured(tmp_path):
    from golf_offshoot.learning_lane_15m.spread_profile import PROFILE_REL, build_profile, write_profile

    profile = build_profile(
        [{"mark": 0.50, "half_spread": 0.005, "yes_bid": 0.49, "yes_ask": 0.51}]
    )
    write_profile(profile, root=tmp_path, latest_dir=tmp_path / "latest")
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps({"fee_hurdle": {}, "half_spread_profile": PROFILE_REL.name}),
        encoding="utf-8",
    )
    md = tmp_path / critic.BAR_MD_REL
    md.write_text(f"named {PROFILE_REL.name}\n", encoding="utf-8")
    check = critic.check_half_spread_profile(root=tmp_path)
    assert check["state"] == critic.PASS


def test_hub_autostart_scratch_tree_skips_schtasks(tmp_path):
    check = critic.check_hub_autostart_registered(root=tmp_path)
    assert check["state"] == critic.PASS
    assert check["id"] == "hub_autostart_registered"


def test_alpha_first_look_is_the_schedule_first_term(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(
        json.dumps(
            {
                "looks": {"first_look_n": 70},
                "distinguishable": {
                    "h0": "mean(d) <= delta",
                    "effect_floor_usd_per_window": 0.28,
                    "sd_used": 0.784,
                    "se_at_n": 0.0937,
                    "mde": 0.2243,
                    "reject_if_mean_d_exceeds": 0.504,
                    "alpha_first_look": 0.025,
                    "next_look_alpha": 0.008333,
                    "effect_floor_rationale": "sd ~0.784 next look",
                    "power": {
                        "disclosed_on_face": True,
                        "effect_at_50pct_power": 0.504,
                        "effect_at_80pct_power": 0.583,
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    registry = tmp_path / critic.REGISTRY_REL
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({"trials_to_date": 1}), encoding="utf-8")
    check = critic.check_delta_above_detection_floor(root=tmp_path)
    disagreements = check["evidence"].get("disagreements") or []
    assert not any("alpha_first_look" in row for row in disagreements)
    assert not any("next_look_alpha" in row for row in disagreements)

