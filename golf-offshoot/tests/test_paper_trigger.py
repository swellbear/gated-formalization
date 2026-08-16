from golf_offshoot.models.strategy import PortfolioState, new_id
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement
from golf_offshoot.strategy.paper_trigger import (
    group_trigger_actions,
    market_label,
    trigger_document,
    trigger_headline,
    trigger_movements,
)


def _mv(*, kind: str, name: str, bet: str = "win", delta: float = 0.0, donor: str = "") -> PaperMovement:
    return PaperMovement(
        movement_id=new_id("mv"),
        kind=kind,
        status="advised",
        player_name=name,
        bet_type=bet,
        stake_delta=delta,
        from_player_name=donor,
    )


def test_trigger_order_is_sell_then_reallocate_partial_add_new_hold():
    moves = [
        _mv(kind="hold", name="Scottie Scheffler", bet="win"),
        _mv(kind="new_bet", name="Matti Schmid", bet="top_20", delta=0.51),
        _mv(kind="add", name="Scottie Scheffler", bet="win", delta=0.18),
        _mv(kind="reduce", name="Kurt Kitayama", bet="win", delta=-3.06),
        _mv(kind="reallocate", name="Sungjae Im", bet="win", delta=1.0, donor="Sam Burns"),
        _mv(kind="exit", name="Sam Burns", bet="win", delta=-0.54),
        _mv(kind="lock", name="Tommy Fleetwood", bet="win", delta=8.75),
    ]
    labels = [s.label for s in group_trigger_actions(moves)]
    assert labels == ["SELL", "REALLOCATE", "PARTIAL SELL", "ADD", "NEW", "HOLD"]
    sell = group_trigger_actions(moves)[0]
    assert sell.rows[0].name == "Sam Burns"
    assert sell.rows[0].market == "Win"
    assert sell.rows[0].amount == "$0.54"
    realloc = group_trigger_actions(moves)[1]
    assert realloc.rows[0].extra == "from Sam Burns"
    assert realloc.rows[0].amount == "$1.00"
    partial = group_trigger_actions(moves)[2]
    assert partial.rows[0].amount == "$3.06"
    add = group_trigger_actions(moves)[3]
    assert add.rows[0].amount == "$0.18"
    hold = [s for s in group_trigger_actions(moves) if s.label == "HOLD"][0]
    assert hold.rows[0].amount == ""
    new = [s for s in group_trigger_actions(moves) if s.label == "NEW"][0]
    names = [r.name for r in new.rows]
    assert names[0] == "Tommy Fleetwood"
    assert "Matti Schmid" in names


def test_trigger_headline_all_hold():
    sections = group_trigger_actions(
        [_mv(kind="hold", name="A", bet="top_5"), _mv(kind="hold", name="B", bet="win")]
    )
    assert trigger_headline(sections) == "NOTHING TO PULL — all HOLD"


def test_trigger_headline_pull():
    sections = group_trigger_actions(
        [_mv(kind="exit", name="A"), _mv(kind="hold", name="B")]
    )
    assert trigger_headline(sections) == "PULL — 1"


def test_trigger_uses_advice_not_old_applied():
    rec = PaperBookFile(
        tournament_id="401811962",
        tournament_name="FedEx St. Jude Championship",
        bankroll=250,
        book=PortfolioState(bankroll=250),
        movements=[
            _mv(kind="exit", name="Old Exit").model_copy(update={"status": "applied", "run_id": "old"})
        ],
    )
    advice = [_mv(kind="hold", name="Scottie Scheffler")]
    moves = trigger_movements(rec, advice, run_id="now")
    assert [m.player_name for m in moves] == ["Scottie Scheffler"]


def test_trigger_page_is_name_and_action_only():
    rec = PaperBookFile(
        tournament_id="401811962",
        tournament_name="FedEx St. Jude Championship",
        bankroll=250,
        book=PortfolioState(bankroll=250),
    )
    text = trigger_document(
        rec,
        advice=[
            _mv(kind="exit", name="Sam Burns", bet="win", delta=-0.54),
            _mv(kind="hold", name="Sungjae Im", bet="top_20"),
        ],
    )
    assert "TRIGGER" in text
    assert "SELL" in text
    assert "Sam Burns  Win  $0.54" in text
    assert "HOLD" in text
    assert "Sungjae Im  Top 20" in text
    hold_line = next(ln for ln in text.splitlines() if "Sungjae Im" in ln)
    assert "$" not in hold_line
    assert "EdgeW" not in text
    assert "entry edge" not in text
    assert market_label("top_10") == "Top 10"
