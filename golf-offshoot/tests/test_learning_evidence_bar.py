from golf_offshoot.learning_lane_15m.critic import run_only_fee_rows
from golf_offshoot.learning_lane_15m.evidence_bar import (
    bar_is_binding,
    class_is_burned,
    fee_adjust,
    fragile_not_null,
    load_burned_classes,
    load_evidence_bar,
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
    assert class_is_burned("R-SKIP-INCOMPLETE-BOOK") is False
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
