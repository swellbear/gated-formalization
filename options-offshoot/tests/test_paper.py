from options_offshoot.compare.law import METHOD_LAW_V1
from options_offshoot.data_feeds.ingest import ingest_field
from options_offshoot.models.enums import ComparePath
from options_offshoot.strategy.paper_book import (
    advice_for_book,
    lock_paper_positions,
    paper_dir,
    starting_bankroll,
    trigger_lines,
)


def test_starting_bankroll_20k():
    assert starting_bankroll() == 20000.0
    assert METHOD_LAW_V1["independent_compare_bankroll"] == 20000.0


def test_lock_and_hold_no_ask(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "options_offshoot.strategy.paper_book.paper_dir", lambda: tmp_path
    )
    run = ingest_field("spx_this_friday", demo=True)
    rec = lock_paper_positions(
        run, path=ComparePath.A_REPLAY, run_id=run.run_id, write=True
    )
    assert rec.starting_bankroll == 20000.0
    assert rec.never_auto_trade is True
    assert (tmp_path / f"{run.field_id}_a_replay.json").is_file()
    adv = advice_for_book(rec, run)
    text = "\n".join(trigger_lines(adv))
    assert "Never auto-trade" in text
