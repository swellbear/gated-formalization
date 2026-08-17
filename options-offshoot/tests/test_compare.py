from options_offshoot.compare.fights import fights_at, fights_document
from options_offshoot.compare.runner import run_compare_method
from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER
from pathlib import Path


def test_compare_method_demo_writes_pack(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "options_offshoot.strategy.paper_book.paper_dir", lambda: tmp_path / "paper"
    )
    (tmp_path / "paper").mkdir()
    monkeypatch.setattr(
        "options_offshoot.ranking.export_table.package_root",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "options_offshoot.compare.pack.package_root",
        lambda: tmp_path,
    )
    (tmp_path / "data" / "exports").mkdir(parents=True)
    payload = run_compare_method("spx_this_friday", demo=True, operating=False)
    pack = Path(payload["pack"])
    assert (pack / "00_full_readout.pdf").is_file()
    assert (pack / "00_trigger.txt").is_file()
    assert (pack / "02_fights.txt").is_file()
    leftover_path = pack / "05_leftover.txt"
    assert leftover_path.is_file()
    leftover = leftover_path.read_text(encoding="utf-8")
    assert "do not stuff" in leftover.lower()
    fights = Path(payload["pack"]).joinpath("02_fights.txt").read_text(encoding="utf-8")
    assert "b_guts" in fights
    assert "Honest theta" in fights
    assert "20000" in fights
    assert payload["books"]["a_replay"].never_auto_trade is True
    assert payload["lived"] is None


def test_fights_disagreement_plain():
    from options_offshoot.compare.fights import PathBookView

    views = {
        "a_replay": PathBookView(
            path_id="a_replay",
            n=1,
            names=["AAPL"],
            exposure=250,
            bankroll=20000,
            starting_bankroll=20000,
        ),
        "b_full": PathBookView(
            path_id="b_full",
            n=0,
            names=[],
            exposure=0,
            bankroll=20000,
            starting_bankroll=20000,
        ),
    }
    events = fights_at(views)
    assert events
    assert events[0]["player_name"] == "AAPL"
    doc = fights_document("spx_this_friday", views=views, events=events)
    assert INDEX_MAP_DISCLAIMER.split(".")[0] in doc or "Map only" in doc
