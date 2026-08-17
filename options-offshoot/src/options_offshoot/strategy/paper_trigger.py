"""Front-of-pack trigger list: this snapshot's actions, nothing else."""

from __future__ import annotations

from dataclasses import dataclass

from options_offshoot.models.enums import AdviceKind
from options_offshoot.models.schemas import PaperMovement

_KIND_SECTION: dict[str, tuple[int, str]] = {
    "exit": (0, "SELL"),
    "sell": (0, "SELL"),
    "reallocate": (1, "REALLOCATE"),
    "reduce": (2, "PARTIAL SELL"),
    "add": (3, "ADD"),
    "new": (4, "NEW"),
    "hold": (5, "HOLD"),
}


@dataclass(frozen=True)
class TriggerRow:
    name: str
    extra: str = ""
    amount: str = ""
    sort_stake: float = 0.0


@dataclass(frozen=True)
class TriggerSection:
    order: int
    label: str
    rows: list[TriggerRow]


def group_trigger_actions(moves: list[PaperMovement]) -> list[TriggerSection]:
    buckets: dict[int, tuple[str, list[TriggerRow]]] = {}
    for m in moves:
        kind = m.kind.value if hasattr(m.kind, "value") else str(m.kind)
        mapped = _KIND_SECTION.get(kind.lower())
        if mapped is None:
            continue
        order, label = mapped
        extra = f"from {m.from_contract_id}" if m.from_contract_id else ""
        amt = ""
        if kind.lower() != "hold" and m.amount:
            amt = f"${m.amount:.2f}"
        row = TriggerRow(
            name=f"{m.underlying}  {m.contract_id}",
            extra=extra,
            amount=amt,
            sort_stake=abs(float(m.amount or 0.0)),
        )
        if order not in buckets:
            buckets[order] = (label, [])
        buckets[order][1].append(row)
    sections: list[TriggerSection] = []
    for order in sorted(buckets):
        label, rows = buckets[order]
        rows.sort(key=lambda r: (-r.sort_stake, r.name.lower()))
        sections.append(TriggerSection(order=order, label=label, rows=rows))
    return sections


def trigger_headline(sections: list[TriggerSection]) -> str:
    if not sections:
        return "NO ACTIONS THIS SNAPSHOT"
    pull = [s for s in sections if s.label != "HOLD"]
    if not pull:
        return "NOTHING TO PULL — all HOLD"
    n = sum(len(s.rows) for s in pull)
    return f"PULL — {n}"


def trigger_document(
    advice: list[PaperMovement],
    *,
    field_id: str = "",
) -> str:
    sections = group_trigger_actions(advice)
    lines = [
        f"TRIGGER  {field_id}".rstrip(),
        trigger_headline(sections),
        "",
    ]
    if not sections:
        lines.append("(none)")
    for section in sections:
        lines.append(section.label)
        for row in section.rows:
            extra = f"  {row.extra}" if row.extra else ""
            amt = f"  {row.amount}" if row.amount else ""
            lines.append(f"  {row.name}{amt}{extra}")
        lines.append("")
    lines.append("This snapshot only. Mock. Never auto-trade.")
    return "\n".join(lines).rstrip() + "\n"


def trigger_lines(advice: list[PaperMovement]) -> list[str]:
    return trigger_document(advice).splitlines()
