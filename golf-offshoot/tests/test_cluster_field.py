from golf_offshoot.clustering.similars import comparable_borrows
from golf_offshoot.demo import demo_field
from golf_offshoot.field_effects.interaction import field_interaction_adjustments
from golf_offshoot.demo import demo_tournament


def test_thin_players_get_borrows():
    field = demo_field().players
    borrows = comparable_borrows(field)
    # lesser-known names in demo have thin course history
    assert any(pid in {"p14", "p15", "p19"} for pid in borrows)


def test_field_interaction_not_global_constant():
    t = demo_tournament()
    field = demo_field().players
    adj = field_interaction_adjustments(field, t.course)
    vals = list(adj.values())
    assert max(vals) - min(vals) > 0.01
