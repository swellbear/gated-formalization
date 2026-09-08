"""Parts 2, 4 and 5: who a tick owes, when Operator clears, and the Critic's body."""

from __future__ import annotations

import json

from golf_offshoot.learning_lane_15m import critic, triggers
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
        "honesty_stamp_is_fresh",
    ]


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
    assert check["evidence"]["ratio"] < 1.10


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


def test_an_unpinned_fee_schedule_fails(tmp_path):
    bar = tmp_path / critic.BAR_JSON_REL
    bar.parent.mkdir(parents=True, exist_ok=True)
    bar.write_text(json.dumps({"fee_hurdle": {"k": 0.07}}), encoding="utf-8")

    check = critic.check_fee_schedule_hash_recorded(root=tmp_path)

    assert check["state"] == critic.FAIL
    assert "habit" in check["detail"]
