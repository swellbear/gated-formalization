from options_offshoot.compare.law import (
    METHOD_LAW_V1,
    index_shop_forbidden,
    law_hash,
    learner_may_move_t,
)


def test_law_hash_stable():
    assert len(law_hash()) == 16
    assert law_hash() == law_hash()


def test_bankroll_is_20k_per_field():
    assert METHOD_LAW_V1["independent_compare_bankroll"] == 20000.0
    assert METHOD_LAW_V1["bankroll_per_field_per_path"] is True
    assert METHOD_LAW_V1["never_auto_trade"] is True
    assert METHOD_LAW_V1["hunter_in_v1"] is False
    assert METHOD_LAW_V1["sort_key"] == "vs_ask"
    assert METHOD_LAW_V1["not_sort_key"] == "p_itm"


def test_shop_index_is_forbidden():
    assert index_shop_forbidden("shop the index fattest rows") is True
    ok, code = learner_may_move_t(n_events=99, reason="shop_index_fattest_rows")
    assert ok is False
    assert "shop_index" in code


def test_copy_a_won_rejected():
    ok, code = learner_may_move_t(n_events=99, reason="copy_a_because_a_won")
    assert ok is False
    assert "copy_a" in code


def test_keep_t_this_week():
    ok, code = learner_may_move_t(n_events=99, reason="holdout named")
    assert ok is False
    assert "keep_t" in code
