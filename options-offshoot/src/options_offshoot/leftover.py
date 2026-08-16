"""Leftover callout. Display only. No hunter. Do not stuff into theta."""

from __future__ import annotations

from options_offshoot.models.enums import SourceKind
from options_offshoot.models.schemas import FieldRun, PaperBookFile, SourceInventoryItem


def format_leftover_callout(
    run: FieldRun,
    open_book: PaperBookFile | None = None,
) -> str:
    used = [i for i in run.inventory if i.used]
    unconstrained = [
        i for i in run.inventory if (not i.used) or i.quality.missing
        or i.quality.source_kind == SourceKind.UNAVAILABLE
    ]
    # Dedup unconstrained by name if also used with missing parts
    seen_u = set()
    unc_lines = []
    for item in unconstrained:
        if item.name in seen_u:
            continue
        if item.used and not item.quality.missing:
            continue
        seen_u.add(item.name)
        note = item.quality.notes or item.impact or "unavailable"
        unc_lines.append(f"  {item.name} - {note}")
    if not unc_lines:
        unc_lines = ["  (none listed this run)"]

    used_lines = []
    for item in used:
        if item.quality.missing:
            continue
        used_lines.append(f"  {item.name} - {item.quality.source or item.impact or 'used'}")
    if not used_lines:
        used_lines = ["  (nothing admitted this run)"]

    held_lines = _held_lines(run, open_book)

    lines = [
        "LEFTOVER CALLOUT  (display only; not GPF gates)",
        f"field={run.field_id}  honest={run.honest}  never_auto_trade=true",
        "",
        "== already used ==",
        *used_lines,
        "",
        "== still unconstrained ==",
        *unc_lines,
        "",
        "== on held tickets ==",
        *held_lines,
        "",
        "== do not stuff into theta ==",
        "  Earnings narrative, IV from blogs, missing greeks as 0,",
        "  invented bid from last, 'this ticker should be in', unseeded news.",
        "  Overrides stay documented or they do not happen. No hunter in v1.",
    ]
    return "\n".join(lines)


def _held_lines(run: FieldRun, open_book: PaperBookFile | None) -> list[str]:
    if open_book is None or not open_book.positions:
        return ["  (none held)"]
    by_id = {r.contract.contract_id: r for r in run.rows}
    out = []
    for pos in open_book.positions:
        row = by_id.get(pos.contract_id)
        if row is None:
            out.append(
                f"  {pos.underlying} {pos.contract_type.value} {pos.strike} {pos.expiry} "
                f"- no live row; ride to expiry. Not a cash-out."
            )
            continue
        q = row.contract.quote
        if not q.has_real_ask:
            out.append(
                f"  {pos.underlying} {pos.contract_type.value} {pos.strike} {pos.expiry} "
                f"stake=${pos.stake:.2f} ask=n/a - ride to expiry. Not a cash-out."
            )
            continue
        pitm = "n/a" if row.model.p_itm is None else f"{row.model.p_itm:.3f}"
        out.append(
            f"  {pos.underlying} {pos.contract_type.value} {pos.strike} {pos.expiry} "
            f"stake=${pos.stake:.2f} ask={q.ask:.2f} P(ITM)={pitm}"
        )
    return out or ["  (none held)"]


def inventory_item(
    name: str,
    *,
    used: bool,
    missing: bool,
    source: str = "",
    notes: str = "",
    kind: SourceKind | None = None,
    impact: str = "",
    score: float = 0.0,
    n: int = 0,
) -> SourceInventoryItem:
    from options_offshoot.models.enums import SourceKind as SK

    k = kind if kind is not None else (SK.UNAVAILABLE if missing else SK.REAL_LIVE)
    from options_offshoot.models.schemas import DataQuality

    return SourceInventoryItem(
        name=name,
        used=used,
        impact=impact,
        quality=DataQuality(
            score=score,
            source_kind=k,
            source=source,
            missing=missing,
            notes=notes,
            n=n,
        ),
    )
