"""Maybe apply paper when advice set changes. Mock only."""

from __future__ import annotations

from options_offshoot.models.schemas import FieldRun, PaperBookFile, PaperMovement
from options_offshoot.strategy.paper_book import actionable, apply_advice


def advice_signature(advice: list[PaperMovement]) -> str:
    items = [
        f"{a.kind.value}:{a.contract_id}:{a.underlying}:{a.n_contracts}"
        for a in advice
        if a.kind.value != "hold"
    ]
    return "|".join(sorted(items))


def maybe_apply_paper(
    record: PaperBookFile,
    advice: list[PaperMovement],
    *,
    prior_sig: str | None = None,
    run: FieldRun | None = None,
) -> tuple[PaperBookFile, bool]:
    if not actionable(advice):
        record.last_advice = advice
        return record, False
    sig = advice_signature(advice)
    if prior_sig is not None and sig == prior_sig:
        return record, False
    if record.last_advice_sig and sig == record.last_advice_sig:
        record.last_advice = advice
        return record, False
    rec = apply_advice(record, advice, run)
    rec.last_advice_sig = sig
    return rec, True
