from options_offshoot.__main__ import DEMO_BANNER, main


def test_fields_cli(capsys):
    rc = main(["fields"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "PREDECLARED FIELDS" in out
    assert "earnings_us_week" in out
    assert "Map only" in out
    assert "n/a" in out


def test_demo_cli(capsys, tmp_path, monkeypatch):
    monkeypatch.setattr(
        "options_offshoot.strategy.paper_book.paper_dir", lambda: tmp_path
    )
    monkeypatch.setattr(
        "options_offshoot.ranking.export_table.package_root",
        lambda: tmp_path,
    )
    (tmp_path / "data" / "exports").mkdir(parents=True)
    rc = main(["demo", "--field", "spx_this_friday"])
    assert rc == 0
    out = capsys.readouterr().out
    assert DEMO_BANNER.split(".")[0] in out or "MOCK DATA" in out
    assert "vs-ask" in out.lower() or "vsAsk" in out
    assert "LEFTOVER" in out
    assert "never_auto_trade" in out
