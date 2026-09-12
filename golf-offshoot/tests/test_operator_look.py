"""Operator L1 look: no card does not invent tape; PARK/CONTINUE from the card."""

import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.operator_look import (
    LOOK_CONTINUE,
    LOOK_NO_CARD,
    LOOK_PARK,
    apply_operator_look,
)
from golf_offshoot.learning_lane_15m.rules import load_rules


def _seed(root: Path, *, execution=True, card=None):
    docs = root / "golf-offshoot" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "LEARNING_LANE_15M_RULES.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "rules": [
                    {
                        "id": "R-SKIP-HOUR-CLOSE",
                        "kind": "selection",
                        "selects": True,
                        "execution": execution,
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    if card is not None:
        dest = docs / "LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json"
        dest.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")


def test_operator_no_card_does_not_invent_tape(monkeypatch, tmp_path):
    _seed(tmp_path, execution=True, card=None)

    def boom(*a, **k):
        raise AssertionError("must not gather or score tape when the card is missing")

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.gather_lived_windows",
        boom,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.score_rule",
        boom,
    )
    out = apply_operator_look(root=tmp_path)
    assert out["verdict"] == LOOK_NO_CARD
    assert out["mutated"] is False
    assert out["invented_tape"] is False
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is True


def test_operator_park_from_failing_card(tmp_path):
    _seed(
        tmp_path,
        execution=True,
        card={"n": 70, "passes_every_binding_clause": False, "windows": [{"window_id": "x"}]},
    )
    out = apply_operator_look(root=tmp_path)
    assert out["verdict"] == LOOK_PARK
    assert out["mutated"] is True
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is False
    card = json.loads(
        (tmp_path / "golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json").read_text(
            encoding="utf-8"
        )
    )
    assert card["operator_look"] == LOOK_PARK


def test_operator_park_from_density_fail_card(tmp_path):
    _seed(
        tmp_path,
        execution=True,
        card={
            "n": 70,
            "skip_count": 1,
            "density_fail": True,
            "undecidable": True,
            "passes_every_binding_clause": False,
            "clause_1_paired_t_vs_floor": {"passes": None, "not_scored": "density-fail"},
            "windows": [{"window_id": "x"}],
        },
    )
    out = apply_operator_look(root=tmp_path)
    assert out["verdict"] == LOOK_PARK
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is False


def test_operator_continue_from_passing_card(tmp_path):
    _seed(
        tmp_path,
        execution=True,
        card={"n": 70, "passes_every_binding_clause": True},
    )
    out = apply_operator_look(root=tmp_path)
    assert out["verdict"] == LOOK_CONTINUE
    assert out["mutated"] is False
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is True


def test_already_stamped_park_finishes_execution_drop(tmp_path):
    _seed(
        tmp_path,
        execution=True,
        card={
            "n": 70,
            "passes_every_binding_clause": False,
            "operator_look": LOOK_PARK,
        },
    )
    out = apply_operator_look(root=tmp_path)
    assert out["ok"] is True
    assert out["verdict"] == LOOK_PARK
    assert out["reason"] == "already_stamped"
    assert out["mutated"] is True
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is False
    card = json.loads(
        (tmp_path / "golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json").read_text(
            encoding="utf-8"
        )
    )
    assert card["operator_look"] == LOOK_PARK


def test_already_stamped_continue_does_not_drop_execution(tmp_path):
    _seed(
        tmp_path,
        execution=True,
        card={
            "n": 70,
            "passes_every_binding_clause": True,
            "operator_look": LOOK_CONTINUE,
        },
    )
    out = apply_operator_look(root=tmp_path)
    assert out["reason"] == "already_stamped"
    assert out["verdict"] == LOOK_CONTINUE
    assert out["mutated"] is False
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is True


def test_park_drops_execution_before_stamping(monkeypatch, tmp_path):
    _seed(
        tmp_path,
        execution=True,
        card={"n": 70, "passes_every_binding_clause": False},
    )

    def boom(*a, **k):
        raise OSError("registry write failed")

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.operator_look.set_selecting_execution",
        boom,
    )
    try:
        apply_operator_look(root=tmp_path)
        raise AssertionError("registry failure must surface")
    except OSError:
        pass
    card = json.loads(
        (tmp_path / "golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json").read_text(
            encoding="utf-8"
        )
    )
    assert "operator_look" not in card
    assert load_rules(root=tmp_path)["rules"][0]["execution"] is True
