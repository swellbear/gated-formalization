import os

from golf_offshoot.data_feeds.local_env import load_local_env


def test_load_local_env_fills_empty_and_does_not_override(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "THE_ODDS_API_KEY=from-file\nGOLF_ODDS_BOOK=hardrockbet\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("THE_ODDS_API_KEY", raising=False)
    monkeypatch.setenv("GOLF_ODDS_BOOK", "bovada")
    loaded = load_local_env(path=env_file, force=True)
    assert loaded == env_file
    assert os.environ["THE_ODDS_API_KEY"] == "from-file"
    assert os.environ["GOLF_ODDS_BOOK"] == "bovada"


def test_load_local_env_skipped_under_pytest_without_force(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("THE_ODDS_API_KEY=should-not-load\n", encoding="utf-8")
    monkeypatch.delenv("THE_ODDS_API_KEY", raising=False)
    assert load_local_env(path=env_file, force=False) is None
    assert os.environ.get("THE_ODDS_API_KEY", "") == ""
