from types import SimpleNamespace

from golf_offshoot.models.strategy import new_id
from golf_offshoot.strategy.paper_book import PaperMovement
from golf_offshoot.strategy.watch import (
    WatchConfigError,
    _header_text,
    decide_watch,
    ntfy_topic,
    publish_ntfy,
    pull_moves,
)

_STARTED = [SimpleNamespace(live_holes_completed=9, live_place=1, live_score_to_par=-2)]


def _mv(kind: str, name: str, *, extra: str = "") -> PaperMovement:
    return PaperMovement(
        movement_id=new_id("mv"),
        kind=kind,
        status="advised",
        player_id=name.lower().replace(" ", "-"),
        player_name=name,
        bet_type="win",
        reason_plain=extra,
        reason_technical=extra,
    )


def test_hold_only_arms_once():
    holds = [_mv("hold", "Matt Fitzpatrick")]
    first = decide_watch(holds, [], event="BMW", prev_signature="", armed=False)
    assert first.kind == "armed"
    assert first.should_ping is True
    second = decide_watch(holds, [], event="BMW", prev_signature=first.signature, armed=True)
    assert second.kind == "hold"
    assert second.should_ping is False


def test_pull_pings_then_stays_quiet_on_same_set():
    pulls = [_mv("exit", "Matt McCarty", extra="TAKE THE POP")]
    first = decide_watch(pulls, _STARTED, event="BMW", prev_signature="", armed=True)
    assert first.kind == "pull"
    assert first.should_ping is True
    assert first.priority == "high"
    assert "Matt McCarty" in first.body
    assert "TAKE THE POP" in first.body
    again = decide_watch(pulls, _STARTED, event="BMW", prev_signature=first.signature, armed=True)
    assert again.should_ping is False


def test_watch_keeps_pulls_on_decision():
    pulls = [_mv("add", "Gary Woodland", extra="live improved")]
    first = decide_watch(pulls, _STARTED, event="BMW", prev_signature="", armed=True)
    assert first.kind == "pull"
    assert first.pulls
    assert first.pulls[0].kind == "add"
    assert "Gary Woodland" in first.body


def test_new_pull_after_hold_is_a_ping():
    hold = decide_watch([_mv("hold", "Eric Cole")], [], event="BMW", armed=True)
    nxt = decide_watch(
        [_mv("new_bet", "Adam Scott")],
        [],
        event="BMW",
        prev_signature=hold.signature,
        armed=True,
    )
    assert nxt.kind == "pull"
    assert nxt.should_ping is True
    assert "Adam Scott" in nxt.body


def test_pre_tee_exit_is_not_a_pull():
    moves = [_mv("exit", "Eric Cole", extra="original edge collapsed")]
    assert pull_moves(moves, []) == []
    decision = decide_watch(moves, [], event="BMW", armed=True)
    assert decision.kind == "hold"
    assert decision.should_ping is False


def test_ntfy_topic_rejects_junk(monkeypatch):
    monkeypatch.delenv("NTFY_TOPIC", raising=False)
    try:
        ntfy_topic("")
        raise AssertionError("expected WatchConfigError")
    except WatchConfigError:
        pass
    monkeypatch.setenv("NTFY_TOPIC", "bad topic")
    try:
        ntfy_topic()
        raise AssertionError("expected WatchConfigError")
    except WatchConfigError:
        pass


def test_publish_dry_run_does_not_post(monkeypatch):
    monkeypatch.setenv("NTFY_TOPIC", "golf-bmw-test")
    url = publish_ntfy("hello", title="t", dry_run=True)
    assert url.endswith("/golf-bmw-test")


def test_ntfy_title_strips_em_dash():
    assert "PULL - 2" == _header_text("PULL — 2")
