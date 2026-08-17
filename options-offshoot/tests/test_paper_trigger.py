from datetime import date

from options_offshoot.models.enums import AdviceKind, QuoteVenue
from options_offshoot.models.schemas import PaperMovement
from options_offshoot.strategy.paper_trigger import (
    group_trigger_actions,
    trigger_document,
    trigger_headline,
)


def test_trigger_order_is_sell_then_reallocate_partial_add_new_hold():
    moves = [
        PaperMovement(kind=AdviceKind.HOLD, contract_id="h", underlying="ZZZ"),
        PaperMovement(kind=AdviceKind.NEW, contract_id="n", underlying="AAA", amount=100),
        PaperMovement(kind=AdviceKind.ADD, contract_id="a", underlying="BBB", amount=50),
        PaperMovement(kind=AdviceKind.REDUCE, contract_id="r", underlying="CCC", amount=25),
        PaperMovement(
            kind=AdviceKind.REALLOCATE,
            contract_id="x",
            underlying="DDD",
            amount=80,
            from_contract_id="old",
        ),
        PaperMovement(kind=AdviceKind.EXIT, contract_id="e", underlying="EEE", amount=200),
    ]
    labels = [s.label for s in group_trigger_actions(moves)]
    assert labels == ["SELL", "REALLOCATE", "PARTIAL SELL", "ADD", "NEW", "HOLD"]


def test_hold_has_no_dollars():
    text = trigger_document(
        [PaperMovement(kind=AdviceKind.HOLD, contract_id="h", underlying="AAPL", amount=99)]
    )
    hold_block = text.split("HOLD", 1)[1]
    assert "$" not in hold_block.split("This snapshot")[0]


def test_unmarked_ride_copy():
    from options_offshoot.data_feeds.ingest import ingest_field
    from options_offshoot.models.enums import ComparePath, ContractType
    from options_offshoot.models.schemas import PaperBookFile, PaperPosition
    from options_offshoot.strategy.paper_book import advice_for_book

    run = ingest_field("spx_this_friday", demo=True)
    rec = PaperBookFile(
        field_id=run.field_id,
        path_id=ComparePath.LIVED,
        positions=[
            PaperPosition(
                position_id="1",
                contract_id="missing-id",
                underlying="AAPL",
                expiry=date(2026, 8, 21),
                strike=200,
                contract_type=ContractType.CALL,
                stake=320,
                n_contracts=1,
                multiplier=100,
                quote_venue=QuoteVenue.POLYGON,
            )
        ],
    )
    adv = advice_for_book(rec, run)
    assert adv
    assert adv[0].kind == AdviceKind.HOLD
    assert adv[0].unmarked is True
    assert "Not edge intact" in adv[0].reason or "ride to expiry" in adv[0].reason.lower()


def test_headline_all_hold():
    sections = group_trigger_actions(
        [PaperMovement(kind=AdviceKind.HOLD, contract_id="h", underlying="AAPL")]
    )
    assert trigger_headline(sections) == "NOTHING TO PULL — all HOLD"
