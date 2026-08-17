"""Live compare: independent A/B books. Does not lock or write lived."""

from __future__ import annotations

from options_offshoot.compare.apply import maybe_apply_paper
from options_offshoot.compare.fights import fights_at, fights_document, load_path_views
from options_offshoot.compare.law import law_hash
from options_offshoot.compare.pack import write_batch_pack
from options_offshoot.compare.paths import COMPARE_LEDGERS, uses_honest_theta
from options_offshoot.data_feeds.ingest import ingest_field
from options_offshoot.leftover import format_leftover_callout
from options_offshoot.models.enums import ComparePath, RunMode
from options_offshoot.ranking.export_table import export_table
from options_offshoot.strategy.paper_book import (
    advice_for_book,
    lock_paper_positions,
    load_paper_file,
    mark_scores,
    save_paper_book,
)
from options_offshoot.strategy.paper_settle import maybe_auto_settle


def run_compare_method(
    field_id: str,
    *,
    demo: bool = False,
    operating: bool = True,
    max_underlyings: int | None = None,
    quotes: str | None = None,
) -> dict:
    current = ingest_field(
        field_id,
        honest=False,
        operating=operating,
        demo=demo,
        max_underlyings=max_underlyings,
        mode=RunMode.LIVE,
        quotes=quotes,
    )
    guts = ingest_field(
        field_id,
        honest=True,
        operating=operating,
        demo=demo,
        max_underlyings=max_underlyings,
        mode=RunMode.LIVE,
        quotes=quotes,
    )
    books: dict = {}
    # Compare does not --lock-paper lived and does not write the lived ledger.
    lived = load_paper_file(field_id, ComparePath.LIVED.value)
    if lived is not None:
        mark_scores(lived, current)
    books["lived"] = lived
    for path in COMPARE_LEDGERS:
        run = guts if uses_honest_theta(path) else current
        rec = load_paper_file(field_id, path.value)
        if rec is None:
            rec = lock_paper_positions(run, path=path, run_id=run.run_id)
        else:
            rec = maybe_auto_settle(rec)
            adv = advice_for_book(rec, run)
            rec, _ = maybe_apply_paper(rec, adv, run=run)
            mark_scores(rec, run)
            save_paper_book(rec)
        books[path.value] = rec
    views = load_path_views(field_id)
    events = fights_at(views)
    fights = fights_document(field_id, views=views, events=events)
    leftover = format_leftover_callout(current, lived)
    exports = export_table(current)
    pack = write_batch_pack(
        run=current,
        lived=lived,
        books=books,
        fights=fights,
        leftover=leftover,
        guts=guts,
    )
    return {
        "field_id": field_id,
        "current": current,
        "guts": guts,
        "lived": lived,
        "books": books,
        "fights": fights,
        "leftover": leftover,
        "pack": str(pack),
        "exports": exports,
        "law_hash": law_hash(),
        "full_readout": str(pack / "00_full_readout.pdf"),
    }
