from options_offshoot.fields.index import format_index, map_stats
from options_offshoot.models.enums import RunMode
from options_offshoot.models.schemas import FieldRun


def test_index_sorts_by_field_id_not_n_clear():
    skinny = {
        "field_id": "aaa_first",
        "n": 2,
        "n_ask": 1,
        "n_clear_ask": 0,
    }
    fat = {
        "field_id": "zzz_last",
        "n": 9,
        "n_ask": 9,
        "n_clear_ask": 9,
    }
    text = format_index([fat, skinny])
    pos_a = text.index("aaa_first")
    pos_z = text.index("zzz_last")
    assert pos_a < pos_z
    assert "Map only" in text
    assert "Not a signal to dump the bankroll" in text


def test_map_stats_from_run():
    run = FieldRun(field_id="index_only", run_id="t", mode=RunMode.INGEST, extra={"map_only": True})
    stats = map_stats(run)
    assert stats["n"] == 0
    assert stats["map_only"] is True
