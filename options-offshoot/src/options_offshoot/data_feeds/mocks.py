"""Demo/test mocks. Banned on operating=True."""

from __future__ import annotations

from datetime import date

from options_offshoot.models.enums import ContractType
from options_offshoot.models.schemas import Contract, Quote


def demo_contracts(*, expiry: date) -> list[Contract]:
    """Two underlyings, mix of liquid, illiquid, and missing ask."""
    return [
        Contract(
            contract_id="O:AAPL250000C00200000",
            underlying="AAPL",
            expiry=expiry,
            strike=200.0,
            contract_type=ContractType.CALL,
            quote=Quote(bid=8.0, ask=8.20, last=8.10, open_interest=5000, volume=800),
            spot=205.0,
            realized_vol=0.28,
        ),
        Contract(
            contract_id="O:AAPL250000C00300000",
            underlying="AAPL",
            expiry=expiry,
            strike=300.0,
            contract_type=ContractType.CALL,
            quote=Quote(bid=0.05, ask=0.25, last=0.10, open_interest=12, volume=1),
            spot=205.0,
            realized_vol=0.28,
        ),
        Contract(
            contract_id="O:MSFT250000C00400000",
            underlying="MSFT",
            expiry=expiry,
            strike=400.0,
            contract_type=ContractType.CALL,
            quote=Quote(bid=None, ask=None, last=2.00, open_interest=800, volume=10),
            spot=410.0,
            realized_vol=None,
        ),
        Contract(
            contract_id="O:MSFT250000P00400000",
            underlying="MSFT",
            expiry=expiry,
            strike=400.0,
            contract_type=ContractType.PUT,
            quote=Quote(bid=3.10, ask=3.20, last=3.15, open_interest=2000, volume=400),
            spot=410.0,
            realized_vol=None,
        ),
    ]
