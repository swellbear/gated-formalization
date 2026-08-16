from datetime import date

from options_offshoot.models.enums import ContractType
from options_offshoot.models.schemas import Contract, ModelView, Quote, RankedContract
from options_offshoot.ranking.rank import sort_rows


def _row(*, vs_ask, p_itm, und="AAPL", strike=100.0):
    return RankedContract(
        contract=Contract(
            contract_id=f"{und}{strike}",
            underlying=und,
            expiry=date(2026, 8, 21),
            strike=strike,
            contract_type=ContractType.CALL,
            quote=Quote(bid=1.0, ask=1.1, open_interest=500, volume=50),
            liquid=True,
        ),
        model=ModelView(fair=2.0, p_itm=p_itm, p_itm_low=p_itm, p_itm_high=p_itm, reliability=0.7),
        vs_ask=vs_ask,
        vs_mid=vs_ask,
        clears_ask=vs_ask is not None and vs_ask >= 0.03,
        clears_mid=vs_ask is not None and vs_ask >= 0.03,
    )


def test_sort_key_is_vs_ask_not_p_itm():
    deep_itm = _row(vs_ask=-0.50, p_itm=0.95, und="AAA", strike=10)
    cheaper = _row(vs_ask=+0.40, p_itm=0.20, und="BBB", strike=50)
    missing = _row(vs_ask=None, p_itm=0.99, und="CCC", strike=1)
    ordered = sort_rows([deep_itm, cheaper, missing])
    assert ordered[0].contract.underlying == "BBB"
    assert ordered[1].contract.underlying == "AAA"
    assert ordered[2].contract.underlying == "CCC"
    assert ordered[0].model.p_itm < ordered[1].model.p_itm
