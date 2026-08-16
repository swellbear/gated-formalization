"""Disagreement sheet. Display only. Never auto-trades."""

from __future__ import annotations

from dataclasses import dataclass, field

from options_offshoot.compare.law import METHOD_LAW_V1, law_hash
from options_offshoot.compare.paths import COMPARE_LEDGERS, config_for
from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER
from options_offshoot.localtime import now_eastern_text
from options_offshoot.models.enums import ComparePath
from options_offshoot.models.schemas import PaperBookFile
from options_offshoot.strategy.paper_book import load_paper_file, starting_bankroll

PATH_LAW = {
    "lived": {"label": "Lived", "screen": "both", "ranking": "current"},
    "a_replay": {"label": "A-replay", "screen": "mid", "ranking": "current"},
    "b_guts": {"label": "B-guts", "screen": "mid", "ranking": "honest"},
    "b_nerves": {"label": "B-nerves", "screen": "ask", "ranking": "current"},
    "b_full": {"label": "B-full", "screen": "ask", "ranking": "honest"},
}


@dataclass
class PathBookView:
    path_id: str
    n: int
    names: list[str]
    exposure: float
    bankroll: float
    starting_bankroll: float
    notes: list[str] = field(default_factory=list)


def book_view(record: PaperBookFile | None, path_id: str) -> PathBookView:
    start = starting_bankroll()
    if record is None:
        return PathBookView(
            path_id=path_id,
            n=0,
            names=[],
            exposure=0.0,
            bankroll=start,
            starting_bankroll=start,
            notes=["empty"],
        )
    names = sorted({p.underlying for p in record.positions})
    exp = sum(p.stake for p in record.positions)
    return PathBookView(
        path_id=path_id,
        n=len(record.positions),
        names=names,
        exposure=exp,
        bankroll=record.bankroll,
        starting_bankroll=record.starting_bankroll,
    )


def load_path_views(field_id: str) -> dict[str, PathBookView]:
    views = {}
    for pid in ["lived", *[p.value for p in COMPARE_LEDGERS]]:
        rec = load_paper_file(field_id, pid)
        views[pid] = book_view(rec, pid)
    return views


def fights_at(views: dict[str, PathBookView]) -> list[dict]:
    keys = {n for v in views.values() for n in v.names}
    events = []
    for name in sorted(keys):
        owned = [pid for pid, v in views.items() if name in v.names]
        missing = [pid for pid, v in views.items() if name not in v.names]
        if not missing:
            continue
        plain = _plain(name, owned, missing)
        events.append(
            {
                "player_name": name,
                "owned_by": owned,
                "missing_from": missing,
                "plain": plain,
            }
        )
    return events


def _plain(name: str, owned: list[str], missing: list[str]) -> str:
    bits = []
    for pid in owned:
        law = PATH_LAW.get(pid, {})
        bits.append(
            f"{law.get('label', pid)} holds {name} because {law.get('ranking')} "
            f"clears {law.get('screen')}."
        )
    for pid in missing:
        law = PATH_LAW.get(pid, {})
        bits.append(
            f"{law.get('label', pid)} is out ({law.get('ranking')} / {law.get('screen')})."
        )
    return " ".join(bits)


def fights_document(
    field_id: str,
    *,
    views: dict[str, PathBookView] | None = None,
    events: list[dict] | None = None,
) -> str:
    views = views if views is not None else load_path_views(field_id)
    events = events if events is not None else fights_at(views)
    lines = [
        f"FIGHTS  {field_id}",
        f"method_law={METHOD_LAW_V1['id']} hash={law_hash()}",
        f"as_of={now_eastern_text(with_seconds=True)}",
        "never_auto_trade=true  paper/mock only",
        INDEX_MAP_DISCLAIMER,
        "",
        "== what these books are ==",
        "  lived      Current pipeline. Mid AND ask. Lock frozen; live apply still mutates.",
        "  a_replay   Current ranking. Mid screen. Started $20000.",
        "  b_guts     Honest theta. Mid screen. Started $20000.",
        "  b_nerves   Current ranking. Ask (the number you would lift). Started $20000.",
        "  b_full     Honest theta. Ask. Started $20000.",
        "  t=0.03     Ticket bar this week. vs-ask = model fair minus ask (dollars of premium).",
        "",
        "== books (who is held right now) ==",
    ]
    for pid, view in views.items():
        names = ", ".join(view.names) if view.names else "(empty)"
        lines.append(
            f"  {pid:12} n={view.n:2d}  ${view.exposure:.2f} / ${view.bankroll:.0f} "
            f"(started ${view.starting_bankroll:.0f})  {names}"
        )
    lines += ["", "== disagreements =="]
    if not events:
        lines.append("  none this snapshot")
    for ev in events:
        lines.append(
            f"  {ev['player_name']}: in [{', '.join(ev['owned_by'])}]  "
            f"out [{', '.join(ev['missing_from'])}]"
        )
        if ev.get("plain"):
            lines.append(f"      plain: {ev['plain']}")
    return "\n".join(lines)
