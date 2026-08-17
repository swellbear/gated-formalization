"""CLI: options-offshoot demo | fields | ingest | live | paper-ledger | paper-deposit | paper-withdraw | paper-settle

Never auto-trades.
"""

from __future__ import annotations

import argparse
import sys

from options_offshoot.compare.law import law_hash
from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER, menu_lines
from options_offshoot.fields.index import format_index, last_snapshots_index
from options_offshoot.leftover import format_leftover_callout
from options_offshoot.models.enums import ComparePath, RunMode, StrategyMode
from options_offshoot.strategy.cashout import parse_cashout_cli
from options_offshoot.strategy.engine import format_advice

DEMO_BANNER = (
    "OFFLINE DEMO — MOCK DATA. Not live, not historical, not for rankings in the "
    "operating path. Mocks are allowed here only. Demo does not mint a lived lock."
)


def main(argv: list[str] | None = None) -> int:
    from options_offshoot.data_feeds.local_env import load_local_env

    load_local_env()
    parser = argparse.ArgumentParser(
        description="Options Offshoot (never auto-trades)"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="demo",
        choices=[
            "demo",
            "fields",
            "ingest",
            "live",
            "paper-ledger",
            "paper-deposit",
            "paper-withdraw",
            "paper-settle",
        ],
    )
    parser.add_argument("--field", default="spx_this_friday")
    parser.add_argument("--compare-method", action="store_true")
    parser.add_argument("--max-underlyings", type=int, default=None)
    parser.add_argument("--honest", action="store_true")
    parser.add_argument("--quotes", default=None, choices=["polygon", "ibkr"])
    parser.add_argument("--cash-out", action="append", default=None)
    parser.add_argument("--lock-paper", action="store_true")
    parser.add_argument("--no-apply-paper", action="store_true")
    parser.add_argument(
        "--mode",
        default="stay_selective",
        choices=["stay_selective", "protect_profits", "press_edges"],
    )
    parser.add_argument("--amount", type=float, default=None)
    parser.add_argument("--note", default="")
    parser.add_argument("--path", default="lived")
    args = parser.parse_args(argv)

    if args.command == "demo":
        print(DEMO_BANNER)
        return _ingest(args, demo=True, mode=RunMode.DEMO)
    if args.command == "fields":
        print("\n".join(menu_lines()))
        print()
        print(format_index(last_snapshots_index()))
        print(f"law_hash={law_hash()}")
        return 0
    if args.command == "ingest":
        return _ingest(args, demo=False, mode=RunMode.INGEST)
    if args.command == "live":
        return _ingest(args, demo=False, mode=RunMode.LIVE)
    if args.command.startswith("paper-"):
        return _paper_cmd(args)
    return 1


def _ingest(args: argparse.Namespace, *, demo: bool, mode: RunMode) -> int:
    compare = bool(getattr(args, "compare_method", False))
    if compare:
        from options_offshoot.compare.runner import run_compare_method

        payload = run_compare_method(
            args.field,
            demo=demo,
            operating=not demo,
            max_underlyings=args.max_underlyings,
            quotes=args.quotes,
        )
        print(INDEX_MAP_DISCLAIMER)
        print(payload["leftover"])
        print(f"fights law={payload['law_hash']}")
        print(f"batch pack: {payload['pack']}")
        print(f"full readout: {payload['full_readout']}")
        print("never_auto_trade=true  compare does not lock lived")
        return 0

    from options_offshoot.compare.apply import maybe_apply_paper
    from options_offshoot.compare.pack import write_live_pack
    from options_offshoot.data_feeds.ingest import ingest_field
    from options_offshoot.ranking.export_table import export_table, format_table
    from options_offshoot.models.enums import ComparePath, StrategyMode
    from options_offshoot.models.schemas import PaperBookFile
    from options_offshoot.strategy.engine import format_advice, recommend
    from options_offshoot.strategy.paper_book import (
        advice_for_book,
        load_paper_file,
        lock_paper_positions,
        mark_scores,
        save_paper_book,
        starting_bankroll,
    )
    from options_offshoot.strategy.paper_settle import maybe_auto_settle

    run = ingest_field(
        args.field,
        honest=args.honest,
        operating=not demo,
        demo=demo,
        max_underlyings=args.max_underlyings,
        mode=mode if mode != RunMode.DEMO else RunMode.INGEST,
        quotes=args.quotes,
    )
    print(format_table(run))
    book = load_paper_file(args.field, "lived")
    cashouts = parse_cashout_cli(args.cash_out)
    strat_mode = StrategyMode(args.mode)
    if demo:
        book = None
    elif book is not None:
        book = maybe_auto_settle(book)
        mark_scores(book, run)
        save_paper_book(book)
    if (not demo) and args.lock_paper and book is None:
        book = lock_paper_positions(
            run, path=ComparePath.LIVED, run_id=run.run_id, write=True
        )
        print(f"locked lived identity={book.lock_identity}")
    advice = []
    if book is not None:
        advice = advice_for_book(book, run, cash_out=cashouts, mode=strat_mode)
        if (not demo) and (not args.no_apply_paper) and mode == RunMode.LIVE:
            book, applied = maybe_apply_paper(book, advice, run=run)
            if applied:
                print("applied paper advice (mock only)")
        mark_scores(book, run)
        save_paper_book(book)
        print(format_advice(advice))
    else:
        ghost = PaperBookFile(
            field_id=run.field_id,
            path_id=ComparePath.LIVED,
            cash=starting_bankroll(),
            bankroll=starting_bankroll(),
            starting_bankroll=starting_bankroll(),
        )
        from options_offshoot.models.enums import TicketScreen

        advice = recommend(
            run,
            ghost,
            screen=TicketScreen.ASK,
            mode=strat_mode,
            cash_out=cashouts,
        )
        print(format_advice(advice))
    leftover = format_leftover_callout(run, book)
    print(leftover)
    if run.notes:
        print("RUN NOTES")
        for note in run.notes:
            print(f"  {note}")
    paths = export_table(run)
    print(f"table PDF: {paths['pdf']}")
    if mode == RunMode.LIVE or demo:
        pack = write_live_pack(run=run, lived=book, leftover=leftover, advice=advice)
        print(f"pack: {pack}")
        print(f"full readout: {pack / '00_full_readout.pdf'}")
    print("never_auto_trade=true  observation only")
    return 0


def _paper_cmd(args: argparse.Namespace) -> int:
    from options_offshoot.strategy.paper_book import (
        deposit,
        load_paper_file,
        mark_scores,
        paper_path,
        withdraw,
    )
    from options_offshoot.strategy.paper_settle import maybe_auto_settle

    path_id = args.path
    rec = load_paper_file(args.field, path_id)
    print(paper_path(args.field, path_id))
    if args.command == "paper-ledger":
        if rec is None:
            print("no book")
            return 0
        rec = maybe_auto_settle(rec)
        mark_scores(rec, None)
        print(
            f"bankroll=${rec.bankroll:.2f} cash=${rec.cash:.2f} "
            f"n={sum(1 for p in rec.positions if not p.settled)} "
            f"identity={rec.lock_identity} never_auto_trade={rec.never_auto_trade}"
        )
        print(
            f"posted_ask_pnl={rec.posted_ask_pnl} expiry_settle_pnl={rec.expiry_settle_pnl}"
        )
        return 0
    if rec is None:
        print("no book")
        return 2
    if args.command == "paper-deposit":
        if args.amount is None:
            print("--amount required")
            return 2
        rec = deposit(rec, args.amount, args.note)
        print(f"cash=${rec.cash:.2f} bankroll=${rec.bankroll:.2f}")
        return 0
    if args.command == "paper-withdraw":
        if args.amount is None:
            print("--amount required")
            return 2
        rec = withdraw(rec, args.amount, args.note)
        print(f"cash=${rec.cash:.2f} bankroll=${rec.bankroll:.2f}")
        return 0
    if args.command == "paper-settle":
        rec = maybe_auto_settle(rec, require_close=True)
        print(
            f"settled expiry_settle_pnl={rec.expiry_settle_pnl} "
            f"cash=${rec.cash:.2f}"
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
