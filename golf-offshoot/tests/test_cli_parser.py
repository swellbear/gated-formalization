"""The CLI parser must build. A duplicate option string takes down every command, loop included."""

import pytest

from golf_offshoot.__main__ import main


def test_parser_builds_without_duplicate_option_strings():
    # --help runs every add_argument call and exits before any dispatch, so a
    # duplicate option string surfaces here as ArgumentError instead of SystemExit.
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_watch_once_and_runner_once_stay_distinct_flags(capsys):
    with pytest.raises(SystemExit):
        main(["--help"])
    helptext = capsys.readouterr().out
    assert "--once" in helptext
    assert "--runner-once" in helptext
    assert "golf-kalshi" in helptext
    assert "score-15m" in helptext
