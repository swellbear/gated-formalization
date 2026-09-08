from golf_offshoot.learning_lane_15m.evidence_bar import (
    bar_is_binding,
    class_is_burned,
    fragile_not_null,
    load_burned_classes,
    load_evidence_bar,
)


def test_bar_is_a_nonbinding_draft():
    bar = load_evidence_bar()
    assert bar["binding"] is False
    assert bar["admit"] is False
    assert bar["edge_established"] is False
    assert bar["looks"]["first_look_n"] == 40
    assert bar["distinguishable"]["effect_floor_usd_per_window"] == 0.28
    assert "trials_to_date" in bar["distinguishable"]["alpha"]
    assert bar["verdicts"]["established"]["accepts_replay"] is False
    assert bar["calibration"]["post_declaration_windows_read"] is False
    assert bar_is_binding() is False


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
