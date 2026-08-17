"""Walk persisted audits into A-replay + B-nerves. Does not rewrite lived paper."""

from __future__ import annotations

from golf_offshoot.audit.journal import list_event_audits
from golf_offshoot.compare.apply import maybe_apply_paper
from golf_offshoot.compare.fights import FightEvent, book_view, fights_at, write_fights
from golf_offshoot.compare.law import law_hash
from golf_offshoot.compare.paths import ComparePath, config_for, ledger_id
from golf_offshoot.models.enums import RunMode
from golf_offshoot.strategy.engine import run_strategy
from golf_offshoot.strategy.paper_book import (
    advice_from_recommendation,
    load_paper_file,
    lock_paper_positions,
    save_paper_book,
    void_post_settle_open_tickets,
)


_RETROFIT_PATHS = (ComparePath.A_REPLAY, ComparePath.B_NERVES)


def replay_event(
    event_id: str,
    *,
    write_exports: bool = True,
    snapshot_dir=None,
) -> dict:
    audits = list_event_audits(event_id, snapshot_dir, skip_compare=True)
    notes: list[str] = [
        "Retrofit uses A's persisted ranked rows. B-guts needs extra.field (not on this week's older audits).",
        "Lived paper is not opened, not resized, not re-locked.",
    ]
    if not audits:
        notes.append("No snapshots found; nothing to replay.")
        fights = write_fights(event_id, extra_notes=notes)
        return {
            "event_id": event_id,
            "n_snapshots": 0,
            "fights": str(fights),
            "notes": notes,
            "law_hash": law_hash(),
        }

    event_name = ""
    fight_log: list[FightEvent] = []
    for audit in audits:
        rows = list(audit.outputs)
        if not rows:
            continue
        event_name = event_name or str(audit.extra.get("event_name") or "")
        odds_book = str(audit.extra.get("odds_book") or "")
        views = {}
        for path in _RETROFIT_PATHS:
            pid = ledger_id(path)
            cfg = config_for(path, event_id=event_id)
            existing = load_paper_file(event_id, path_id=pid)
            if existing is None:
                from golf_offshoot.strategy.paper_book import paper_candidate_slots

                slots = paper_candidate_slots(
                    rows,
                    cfg,
                    require_cleared=cfg.ticket_screen == "posted",
                )
                if not slots:
                    continue
                rec = lock_paper_positions(
                    rows,
                    cfg,
                    event_id=event_id,
                    event_name=event_name or event_id,
                    run_id=audit.run_id,
                    odds_book=odds_book,
                    path_id=pid,
                    independent_bankroll=True,
                    write_exports=write_exports,
                    method_law_hash=law_hash(),
                    require_cleared=cfg.ticket_screen == "posted",
                )
            elif existing.settled_at is not None:
                rec, voided = void_post_settle_open_tickets(existing)
                if voided:
                    save_paper_book(rec)
            else:
                rec_strat = run_strategy(
                    rows,
                    cfg,
                    run_mode=audit.mode if isinstance(audit.mode, RunMode) else RunMode.LIVE,
                    book=existing.book,
                )
                advice = advice_from_recommendation(existing, rec_strat, run_id=audit.run_id)
                rec, _applied = maybe_apply_paper(existing, advice)
                save_paper_book(rec)
            views[pid] = book_view(rec, pid)
        fight_log.extend(
            fights_at(views, as_of=str(audit.as_of), run_id=audit.run_id, event_id=event_id)
        )

    from golf_offshoot.compare.fights import load_path_views

    views = load_path_views(event_id, paths=_RETROFIT_PATHS)
    fights = write_fights(
        event_id,
        event_name=event_name,
        views=views,
        events=fight_log or fights_at(views, event_id=event_id),
        extra_notes=notes + [f"snapshots_walked={len(audits)}"],
    )
    batch = None
    if write_exports:
        from golf_offshoot.compare.pack import write_batch_pack

        batch = write_batch_pack(
            event_id,
            event_name=event_name,
            run_id=audits[-1].run_id if audits else "replay",
        )
    return {
        "event_id": event_id,
        "n_snapshots": len(audits),
        "fights": str(fights),
        "batch_pack": str(batch) if batch else "",
        "notes": notes,
        "law_hash": law_hash(),
        "never_auto_bet": True,
    }
