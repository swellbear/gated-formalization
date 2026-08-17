"""Advisory layer for contracts. Suggestions only. Never auto-trades."""

from __future__ import annotations

from options_offshoot.config import COLLAPSE_FAIR_FRAC, RUNNER_MTM_FRAC
from options_offshoot.models.enums import AdviceKind, StrategyMode, TicketScreen
from options_offshoot.models.schemas import (
    FieldRun,
    PaperBookFile,
    PaperMovement,
    PaperPosition,
    RankedContract,
)
from options_offshoot.ranking.rank import clears_screen
from options_offshoot.strategy.cashout import compare_bid, typed_bid
from options_offshoot.strategy.sizing import (
    lot_cost,
    open_exposure,
    same_underlying_cap,
    size_new,
    total_cap,
)


def _by_id(run: FieldRun) -> dict[str, RankedContract]:
    return {r.contract.contract_id: r for r in run.rows}


def _mtm(pos: PaperPosition, row: RankedContract | None) -> float | None:
    if row is None or not row.contract.quote.has_real_bid:
        return None
    n = int(pos.n_contracts or 0)
    if n <= 0:
        return None
    return float(row.contract.quote.bid) * int(pos.multiplier) * n


def _entry_vs_ask(pos: PaperPosition) -> float | None:
    if pos.entry_fair is None or pos.entry_ask is None:
        return None
    return float(pos.entry_fair) - float(pos.entry_ask)


def recommend(
    run: FieldRun,
    book: PaperBookFile | None,
    *,
    screen: TicketScreen | str = TicketScreen.ASK,
    mode: StrategyMode = StrategyMode.STAY_SELECTIVE,
    cash_out: dict[str, float] | None = None,
    leftover: list[str] | None = None,
) -> list[PaperMovement]:
    notes = leftover if leftover is not None else []
    cashouts = cash_out or {}
    held = [p for p in (book.positions if book else []) if not p.settled]
    held_ids = {p.contract_id for p in held}
    rows = _by_id(run)
    out: list[PaperMovement] = []

    for pos in held:
        row = rows.get(pos.contract_id)
        per_share = typed_bid(cashouts, pos)
        live_bid = None
        if row is not None and row.contract.quote.has_real_bid:
            live_bid = float(row.contract.quote.bid)
        bid = per_share if per_share is not None else live_bid
        if bid is None:
            out.append(
                PaperMovement(
                    kind=AdviceKind.HOLD,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    reason="No venue bid; ride to expiry. Not a cash-out. Not edge intact.",
                    unmarked=True,
                )
            )
            continue
        cmp = compare_bid(pos, row, bid, mode=mode)
        if cmp is not None and cmp.beats_hold:
            out.append(
                PaperMovement(
                    kind=AdviceKind.EXIT,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    amount=cmp.proceeds,
                    n_contracts=pos.n_contracts,
                    reason=(
                        f"Bid ${bid:.2f} proceeds ${cmp.proceeds:.2f} beat hold-to-expiry "
                        f"${cmp.hold_value:.2f} (threshold ${cmp.threshold:.2f})"
                    ),
                )
            )
            continue
        mtm = _mtm(pos, row)
        if (
            mode == StrategyMode.PROTECT_PROFITS
            and mtm is not None
            and mtm >= RUNNER_MTM_FRAC * pos.stake
            and pos.n_contracts >= 2
        ):
            sold_n = pos.n_contracts // 2
            out.append(
                PaperMovement(
                    kind=AdviceKind.REDUCE,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    amount=sold_n * bid * pos.multiplier,
                    n_contracts=sold_n,
                    reason="Protect Profits: runner MTM already up; partial sell at bid",
                )
            )
            continue
        if (
            row is not None
            and pos.entry_fair is not None
            and row.model.fair is not None
            and row.model.fair < COLLAPSE_FAIR_FRAC * pos.entry_fair
        ):
            out.append(
                PaperMovement(
                    kind=AdviceKind.SELL,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    amount=pos.n_contracts * bid * pos.multiplier,
                    n_contracts=pos.n_contracts,
                    reason="Original edge has collapsed; sell at bid",
                )
            )
            continue
        out.append(
            PaperMovement(
                kind=AdviceKind.HOLD,
                contract_id=pos.contract_id,
                underlying=pos.underlying,
                reason="Original edge is still intact; live mark exists",
            )
        )

    if book is None:
        cash = 0.0
        bankroll = 20000.0
    else:
        cash = float(book.cash)
        bankroll = float(book.bankroll)

    actionable_held = {
        m.contract_id
        for m in out
        if m.kind in (AdviceKind.SELL, AdviceKind.EXIT, AdviceKind.REDUCE)
    }

    if mode != StrategyMode.PROTECT_PROFITS:
        for pos in held:
            if pos.contract_id in actionable_held:
                continue
            row = rows.get(pos.contract_id)
            if row is None or not row.contract.quote.has_real_ask:
                continue
            entry = _entry_vs_ask(pos)
            if entry is None or row.vs_ask is None or row.vs_ask < entry:
                continue
            if not clears_screen(row, screen):
                continue
            n, stake, block = size_new(row, book, bankroll=bankroll, cash=cash, leftover=notes)
            if block or n < 1:
                continue
            out.append(
                PaperMovement(
                    kind=AdviceKind.ADD,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    amount=stake,
                    n_contracts=n,
                    reason="Live vs-ask improved vs entry",
                )
            )
            cash -= stake

    at_cap = open_exposure(book) >= total_cap(bankroll) * 0.98
    candidates = [
        r
        for r in run.rows
        if r.contract.contract_id not in held_ids and clears_screen(r, screen)
    ]
    if at_cap and candidates:
        held_marks = []
        for pos in held:
            if pos.contract_id in actionable_held:
                continue
            row = rows.get(pos.contract_id)
            vs = row.vs_ask if row is not None else None
            held_marks.append((vs if vs is not None else 1e9, pos))
        held_marks.sort(key=lambda x: x[0])
        best = max(candidates, key=lambda r: r.vs_ask or -1e9)
        if held_marks and (held_marks[0][0] < (best.vs_ask or 0)):
            worst = held_marks[0][1]
            n, stake, block = size_new(
                best, book, bankroll=bankroll, cash=cash + worst.stake, leftover=notes
            )
            if not block and n >= 1:
                out.append(
                    PaperMovement(
                        kind=AdviceKind.REALLOCATE,
                        contract_id=best.contract.contract_id,
                        underlying=best.contract.underlying,
                        amount=stake,
                        n_contracts=n,
                        from_contract_id=worst.contract_id,
                        reason=f"At cap; from worse vs-ask {worst.contract_id}",
                    )
                )
                cash = cash + worst.stake - stake
                held_ids.add(best.contract.contract_id)

    if not at_cap or cash > 0:
        for row in candidates:
            if row.contract.contract_id in held_ids:
                continue
            used_und = sum(
                p.stake
                for p in held
                if p.underlying == row.contract.underlying and not p.settled
            )
            if used_und >= same_underlying_cap(bankroll) * 0.99:
                notes.append(
                    f"same-underlying cap {row.contract.underlying}; two strikes are one stack"
                )
                continue
            n, stake, block = size_new(row, book, bankroll=bankroll, cash=cash, leftover=notes)
            if block or n < 1:
                continue
            cost = lot_cost(row.contract.quote.ask, row.contract.multiplier)
            out.append(
                PaperMovement(
                    kind=AdviceKind.NEW,
                    contract_id=row.contract.contract_id,
                    underlying=row.contract.underlying,
                    amount=stake,
                    n_contracts=n,
                    reason=f"vs-ask clears t; {n} lot(s) at ask (lot ${cost:.2f})"
                    if cost
                    else "vs-ask clears t",
                )
            )
            cash -= stake
            held_ids.add(row.contract.contract_id)

    return out


def format_advice(moves: list[PaperMovement]) -> str:
    lines = ["STRATEGY  (advice only; never auto-trade)", ""]
    if not moves:
        lines.append("(no actions)")
        return "\n".join(lines)
    for m in moves:
        amt = ""
        if m.kind != AdviceKind.HOLD and m.amount:
            amt = f"  ${m.amount:.2f}"
        extra = f"  from {m.from_contract_id}" if m.from_contract_id else ""
        lines.append(
            f"  {m.kind.value.upper():12} {m.underlying}  {m.contract_id}{amt}{extra}"
        )
        if m.reason:
            lines.append(f"               {m.reason}")
    return "\n".join(lines)
