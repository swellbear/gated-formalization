"""Shell paper-book auto-apply. Paper observation only. Never cash. Never a real bet."""

from __future__ import annotations

from dataclasses import dataclass

from golf_offshoot.compare.apply import maybe_apply_paper
from golf_offshoot.compare.paths import allowed_bets_from_rows
from golf_offshoot.models.enums import RiskPreference, StrategyMode
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.operator_hints import is_empty_field
from golf_offshoot.operator_surface.modes import (
    CASH_BADGE,
    NOT_ARMED,
    PAPER_ONLY,
    PHASE_1_OBSERVATION,
    is_mock_or_demo_text,
)
from golf_offshoot.strategy.paper_book import (
    EmptyFieldLockError,
    PaperBookFile,
    advice_from_recommendation,
    format_paper_book,
    load_paper_file,
    lock_paper_positions,
    save_paper_book,
)

PAPER_APPLIED = "PAPER_APPLIED"
PAPER_LOCKED = "PAPER_LOCKED"
PAPER_UNCHANGED = "PAPER_UNCHANGED"
PAPER_ADVICE_EMPTY = "PAPER_ADVICE_EMPTY"
PAPER_EMPTY_FIELD = "PAPER_EMPTY_FIELD"
PAPER_SETTLED = "PAPER_SETTLED"
PAPER_BARRED_MOCK = "PAPER_BARRED_MOCK"
PAPER_NO_EVENT = "PAPER_NO_EVENT"

_WALL = (
    f"{PHASE_1_OBSERVATION}. Paper bankroll auto-apply ≠ trading armed. "
    f"{NOT_ARMED}. {PAPER_ONLY}. {CASH_BADGE}."
)


@dataclass
class PaperApplyResult:
    status: str
    text: str
    record: PaperBookFile | None = None
    applied: bool = False
    locked: bool = False


def apply_observation_paper(result, *, event_hint: str | None = None) -> PaperApplyResult:
    """Lock an observation paper book if needed, then maybe_apply_paper.

    Does not deposit/withdraw/transfer cash. Does not place a real bet.
    """
    if result is None:
        return PaperApplyResult(
            status=PAPER_ADVICE_EMPTY,
            text=f"{PAPER_ADVICE_EMPTY}: no operating result. Paper book is not invented. {_WALL}",
        )
    if _barred_demo(result):
        return PaperApplyResult(
            status=PAPER_BARRED_MOCK,
            text=(
                f"{PAPER_BARRED_MOCK}: MOCK/DEMO result is barred from the observation paper book. "
                f"No silent demo fill. {_WALL}"
            ),
        )
    tid = str(
        result.tournament.espn_event_id
        or result.tournament.tournament_id
        or event_hint
        or ""
    ).strip()
    if not tid:
        return PaperApplyResult(
            status=PAPER_NO_EVENT,
            text=f"{PAPER_NO_EVENT}: no ESPN/event id. Paper book is not invented. {_WALL}",
        )
    if is_empty_field(result.ranked):
        return PaperApplyResult(
            status=PAPER_EMPTY_FIELD,
            text=(
                f"{PAPER_EMPTY_FIELD}: empty field; not locking or applying paper. "
                f"This is not a demo book. {_WALL}"
            ),
        )
    record = load_paper_file(tid)
    locked = False
    if record is None:
        if not _has_posted_odds(result):
            return PaperApplyResult(
                status=PAPER_EMPTY_FIELD,
                text=(
                    f"{PAPER_EMPTY_FIELD}: no posted odds on the field; "
                    f"paper book not locked and paper advises not applied. "
                    f"Not a silent demo fill. {_WALL}"
                ),
            )
        try:
            record = _lock_observation_book(result, tid)
        except EmptyFieldLockError:
            return PaperApplyResult(
                status=PAPER_EMPTY_FIELD,
                text=(
                    f"{PAPER_EMPTY_FIELD}: empty field; not locking paper. "
                    f"This is not a demo book. {_WALL}"
                ),
            )
        record.notes = list(record.notes) + [
            f"{PHASE_1_OBSERVATION} shell auto-lock. {PAPER_ONLY}. "
            f"Paper bankroll auto-apply ≠ trading armed. {NOT_ARMED}.",
            CASH_BADGE,
        ]
        save_paper_book(record)
        locked = True
    if record.settled_at is not None:
        return PaperApplyResult(
            status=PAPER_SETTLED,
            text=(
                f"{PAPER_SETTLED}: event already settled; not applying new paper tickets. "
                f"{_WALL}\n{format_paper_book(record)}"
            ),
            record=record,
            locked=locked,
        )
    if result.strategy is None or not result.strategy.enabled:
        extra = " Locked a paper-observation book this run." if locked else ""
        return PaperApplyResult(
            status=PAPER_ADVICE_EMPTY if not locked else PAPER_LOCKED,
            text=(
                f"{PAPER_ADVICE_EMPTY if not locked else PAPER_LOCKED}: "
                f"no strategy advises to apply.{extra} {_WALL}\n"
                f"{format_paper_book(record)}"
            ),
            record=record,
            locked=locked,
        )
    advice = advice_from_recommendation(record, result.strategy, run_id=result.run_id or "")
    if not advice:
        extra = " Locked a paper-observation book this run." if locked else ""
        return PaperApplyResult(
            status=PAPER_ADVICE_EMPTY if not locked else PAPER_LOCKED,
            text=(
                f"{PAPER_ADVICE_EMPTY if not locked else PAPER_LOCKED}: "
                f"strategy returned no paper advises.{extra} {_WALL}\n"
                f"{format_paper_book(record)}"
            ),
            record=record,
            locked=locked,
        )
    record, applied = maybe_apply_paper(record, advice)
    record.latest_advice = advice
    save_paper_book(record)
    if applied:
        status = PAPER_APPLIED
        note = (
            f"{PAPER_APPLIED}: applied strategy advises to the paper book. "
            "Paper observation only. Not a real ticket. Not cash."
        )
    elif locked:
        status = PAPER_LOCKED
        note = (
            f"{PAPER_LOCKED}: observation paper book is in place; advice set did not apply new moves."
        )
    else:
        status = PAPER_UNCHANGED
        note = (
            f"{PAPER_UNCHANGED}: paper advice set unchanged (HOLD-only or same signature). "
            "Not invented."
        )
    return PaperApplyResult(
        status=status,
        text=f"{note} {_WALL}\n{format_paper_book(record)}",
        record=record,
        applied=applied,
        locked=locked,
    )


def _has_posted_odds(result) -> bool:
    for row in result.ranked or []:
        posted = getattr(row, "posted_odds_by_bet", None) or {}
        if any(v is not None and float(v) > 1.0 for v in posted.values()):
            return True
        if getattr(row, "posted_american", None) is not None:
            return True
    return False


def _barred_demo(result) -> bool:
    extra = getattr(result, "audit", None)
    operating = None
    blob = ""
    if extra is not None:
        payload = extra.extra or {}
        operating = payload.get("operating")
        blob = " ".join(str(payload.get(k) or "") for k in ("weight_source", "odds_book"))
    name = getattr(getattr(result, "tournament", None), "name", "") or ""
    if is_mock_or_demo_text(name) or is_mock_or_demo_text(blob):
        return True
    if operating is False:
        return True
    return False


def _lock_observation_book(result, event_id: str) -> PaperBookFile:
    from golf_offshoot.strategy.paper_ledger import load_ledger, working_bankroll

    led = load_ledger()
    if led.entries:
        bankroll = working_bankroll(except_event_id=event_id)
    else:
        bankroll = float(result.audit.extra.get("bankroll") or 2000.0)
    cfg = StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=bankroll,
        ticket_screen="both",
        never_auto_bet=True,
        allowed_bet_types=allowed_bets_from_rows(event_id, result.ranked),
    )
    return lock_paper_positions(
        result.ranked,
        cfg,
        event_id=event_id,
        event_name=result.tournament.name,
        run_id=result.run_id,
        odds_book=str(result.audit.extra.get("odds_book") or ""),
        require_cleared=False,
        write_exports=False,
    )
