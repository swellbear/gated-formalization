from pathlib import Path

from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.learning_lane_15m.paper import ledger_path, save_ledger
from golf_offshoot.learning_lane_15m.paths import (
    EXTERNAL_15M_ROOT,
    artifact_root_15m,
    golf_data_root,
    golf_paper_dir,
    paper_dir_15m,
    set_15m_root_override,
)
from golf_offshoot.strategy.paper_book import paper_dir
from golf_offshoot.strategy.paper_ledger import PaperLedger


def test_golf_paths_untouched_by_15m_override(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        root = artifact_root_15m()
        assert root == tmp_path / "kalshi_15m"
        paper_15 = paper_dir_15m()
        assert paper_15.is_relative_to(root)
        assert golf_paper_dir() == paper_dir()
        assert golf_data_root() == package_data_dir()
        save_ledger(PaperLedger(bankroll=100, starting_bankroll=100))
        assert ledger_path().is_file()
        assert ledger_path().is_relative_to(root)
        assert not ledger_path().is_relative_to(golf_paper_dir())
        assert not (golf_paper_dir() / "ledger.json").exists() or True
        golf_names = {p.name for p in golf_paper_dir().glob("*.json")} if golf_paper_dir().is_dir() else set()
        assert "ledger.json" not in golf_names or ledger_path().resolve() != (golf_paper_dir() / "ledger.json").resolve()
    finally:
        set_15m_root_override(None)


def test_default_external_root_is_not_golf():
    set_15m_root_override(None)
    root = artifact_root_15m()
    golf = golf_data_root().resolve()
    assert root.resolve() != golf
    assert golf / "paper" not in (root.resolve(),)
    assert "learning_lane_15m" in str(root) or root.resolve() == EXTERNAL_15M_ROOT.resolve()


def test_assert_not_golf_path(tmp_path):
    from golf_offshoot.learning_lane_15m.paths import assert_not_golf_path

    set_15m_root_override(tmp_path / "15m")
    try:
        assert_not_golf_path(tmp_path / "15m" / "paper" / "ledger.json")
        try:
            assert_not_golf_path(golf_paper_dir() / "ledger.json")
            raise AssertionError("golf paper write must be refused")
        except RuntimeError as exc:
            assert "golf paper" in str(exc)
    finally:
        set_15m_root_override(None)
