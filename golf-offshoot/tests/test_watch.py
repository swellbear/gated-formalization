from types import SimpleNamespace

from golf_offshoot.models.enums import BetType
from golf_offshoot.models.strategy import StrategyPosition, new_id
from golf_offshoot.strategy.paper_book import PaperMovement
from golf_offshoot.strategy.watch import (
    WatchConfigError,
    _header_text,
    decide_watch,
    ntfy_topic,
    publish_ntfy,
    pull_moves,
    suppress_executed_pulls,
)

_STARTED = [SimpleNamespace(live_holes_completed=9, live_place=1, live_score_to_par=-2)]


def _mv(
    kind: str,
    name: str,
    *,
    extra: str = "",
    bet: str = "win",
    delta: float = 0.0,
    player_id: str = "",
) -> PaperMovement:
    return PaperMovement(
        movement_id=new_id("mv"),
        kind=kind,
        status="advised",
        player_id=player_id or name.lower().replace(" ", "-"),
        player_name=name,
        bet_type=bet,
        stake_delta=delta,
        reason_plain=extra,
        reason_technical=extra,
    )


def _fill(
    name: str,
    *,
    bet: BetType = BetType.WIN_AFTER_R1,
    stake: float = 0.12,
    shares: float = 0.27,
    fill: float = 0.44,
    player_id: str = "3550",
) -> StrategyPosition:
    return StrategyPosition(
        position_id=new_id("fill"),
        player_id=player_id,
        player_name=name,
        bet_type=bet,
        stake=stake,
        decimal_odds=shares / stake,
        entry_edge=0.15,
        entry_model_p=0.56,
        user_recorded=True,
        shares=shares,
        fill_price=fill,
        cost_usd=stake,
        intent="hold",
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


def test_filled_r1_add_at_ticket_dollars_is_the_old_ticket():
    woodland = _fill("Gary Woodland")
    leftover = _mv(
        "add",
        "Gary Woodland",
        bet="win_after_r1",
        delta=0.12,
        player_id="3550",
    )
    spaun = _mv(
        "new_bet",
        "J.J. Spaun",
        bet="win_after_r2",
        delta=0.27,
        player_id="10166",
    )
    kim = _mv(
        "exit",
        "Tom Kim",
        bet="win_after_r1",
        delta=0.17,
        player_id="4602673",
    )
    kept = suppress_executed_pulls([kim, leftover, spaun], [woodland])
    names = [m.player_name for m in kept]
    assert "Gary Woodland" not in names
    assert names == ["Tom Kim", "J.J. Spaun"]


def test_residual_add_on_filled_ticket_still_pings():
    woodland = _fill("Gary Woodland")
    bump = _mv(
        "add",
        "Gary Woodland",
        bet="win_after_r1",
        delta=0.02,
        player_id="3550",
    )
    kept = suppress_executed_pulls([bump], [woodland])
    assert len(kept) == 1
    assert kept[0].stake_delta == 0.02


def test_watch_omits_filled_add_when_a_later_new_arrives():
    woodland = _fill("Gary Woodland")
    advice = [
        _mv("add", "Gary Woodland", bet="win_after_r1", delta=0.12, player_id="3550"),
        _mv("new_bet", "J.J. Spaun", bet="win_after_r2", delta=0.27, player_id="10166"),
    ]
    decision = decide_watch(
        advice,
        _STARTED,
        event="BMW Championship",
        armed=True,
        positions=[woodland],
    )
    assert decision.should_ping is True
    assert "J.J. Spaun" in decision.body
    assert "Gary Woodland" not in decision.body
    assert decision.headline == "PULL — 1"


def test_filled_new_on_same_name_market_does_not_repull():
    spaun = _fill(
        "J.J. Spaun",
        bet=BetType.WIN_AFTER_R2,
        stake=0.28,
        shares=10.39,
        fill=0.02,
        player_id="10166",
    )
    nxt = _mv("new_bet", "J.J. Spaun", bet="win_after_r2", delta=0.27, player_id="10166")
    assert suppress_executed_pulls([nxt], [spaun]) == []
