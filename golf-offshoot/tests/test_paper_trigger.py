from golf_offshoot.models.strategy import PortfolioState, new_id
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement
from golf_offshoot.strategy.paper_trigger import (
    group_trigger_actions,
    market_label,
    pre_tee_trigger_note,
    sanitize_pre_tee_advice,
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


def test_pre_tee_sanitize_converts_collapse_sell_to_hold():
    exit_mv = _mv(kind="exit", name="Eric Cole", delta=-2.19)
    held = sanitize_pre_tee_advice([exit_mv], rows=None)
    assert held[0].kind == "hold"
    assert held[0].stake_delta == 0.0
    assert "has not started" in held[0].reason_plain.lower()
    assert pre_tee_trigger_note(held)
    text = trigger_document(
        PaperBookFile(
            tournament_id="401811963",
            tournament_name="BMW Championship",
            bankroll=250,
            book=PortfolioState(bankroll=250),
        ),
        advice=held,
    )
    assert "SELL" not in text
    assert "HOLD" in text
    assert "Tournament has not started" in text


def test_pre_tee_sanitize_keeps_typed_cashout_sell():
    typed = _mv(kind="exit", name="Eric Cole", delta=-2.19).model_copy(
        update={"cashout_quote": 12.4, "cashout_estimated": False, "mtm_is_bid": False}
    )
    out = sanitize_pre_tee_advice([typed], rows=None)
    assert out[0].kind == "exit"


def test_pre_tee_sanitize_holds_estimated_or_bid_sell():
    estimated = _mv(kind="exit", name="Eric Cole", delta=-2.19).model_copy(
        update={"cashout_quote": 1.53, "cashout_estimated": True}
    )
    bid = _mv(kind="exit", name="Eric Cole", delta=-2.19).model_copy(
        update={"cashout_quote": 1.53, "mtm_is_bid": True}
    )
    assert sanitize_pre_tee_advice([estimated], rows=None)[0].kind == "hold"
    assert sanitize_pre_tee_advice([bid], rows=None)[0].kind == "hold"


def test_pre_tee_sanitize_leaves_sell_once_board_exists():
    from types import SimpleNamespace

    board = [SimpleNamespace(live_holes_completed=9, live_place=4, live_score_to_par=-2)]
    exit_mv = _mv(kind="exit", name="Eric Cole", delta=-2.19)
    out = sanitize_pre_tee_advice([exit_mv], rows=board)
    assert out[0].kind == "exit"
