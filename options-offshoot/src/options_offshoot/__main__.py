"""CLI: options-offshoot demo | fields | ingest | live | paper-ledger"""

from __future__ import annotations

import argparse
import sys

from options_offshoot.compare.law import law_hash
from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER, menu_lines
from options_offshoot.fields.index import empty_index, format_index, map_stats
from options_offshoot.leftover import format_leftover_callout
from options_offshoot.models.enums import RunMode

DEMO_BANNER = (
    "OFFLINE DEMO — MOCK DATA. Not live, not historical, not for rankings in the "
    "operating path. Mocks are allowed here only."
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
        choices=["demo", "fields", "ingest", "live", "paper-ledger"],
    )
    parser.add_argument("--field", default="spx_this_friday")
    parser.add_argument("--compare-method", action="store_true")
    parser.add_argument("--max-underlyings", type=int, default=None)
    parser.add_argument("--honest", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "demo":
        print(DEMO_BANNER)
        return _ingest(args.field, demo=True, compare=args.compare_method)
    if args.command == "fields":
        print("\n".join(menu_lines()))
        print()
        print(format_index(empty_index()))
        print(f"law_hash={law_hash()}")
        return 0
    if args.command == "ingest":
        return _ingest(
            args.field,
            demo=False,
            compare=False,
            honest=args.honest,
            max_underlyings=args.max_underlyings,
            mode=RunMode.INGEST,
        )
    if args.command == "live":
        return _ingest(
            args.field,
            demo=False,
            compare=args.compare_method,
            honest=args.honest,
            max_underlyings=args.max_underlyings,
            mode=RunMode.LIVE,
        )
    if args.command == "paper-ledger":
        from options_offshoot.strategy.paper_book import load_paper_file, paper_path

        rec = load_paper_file(args.field, "lived")
        print(paper_path(args.field, "lived"))
        if rec is None:
            print("no lived book")
            return 0
        print(
            f"bankroll=${rec.bankroll:.2f} cash=${rec.cash:.2f} "
            f"n={len(rec.positions)} never_auto_trade={rec.never_auto_trade}"
        )
        return 0
    return 1


def _ingest(
    field_id: str,
    *,
    demo: bool,
    compare: bool,
    honest: bool = False,
    max_underlyings: int | None = None,
    mode: RunMode = RunMode.INGEST,
) -> int:
    if compare:
        from options_offshoot.compare.runner import run_compare_method

        payload = run_compare_method(
            field_id,
            demo=demo,
            operating=not demo,
            max_underlyings=max_underlyings,
        )
        print(INDEX_MAP_DISCLAIMER)
        print(payload["leftover"])
        print(f"fights law={payload['law_hash']}")
        print(f"batch pack: {payload['pack']}")
        print(f"full readout: {payload['full_readout']}")
        print("never_auto_trade=true")
        return 0
    from options_offshoot.data_feeds.ingest import ingest_field
    from options_offshoot.ranking.export_table import export_table, format_table
    from options_offshoot.strategy.paper_book import load_paper_file

    run = ingest_field(
        field_id,
        honest=honest,
        operating=not demo,
        demo=demo,
        max_underlyings=max_underlyings,
        mode=mode,
    )
    print(format_table(run))
    book = load_paper_file(field_id, "lived")
    print(format_leftover_callout(run, book))
    paths = export_table(run)
    print(f"table PDF: {paths['pdf']}")
    print("never_auto_trade=true  observation only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
