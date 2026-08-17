"""Predeclared fields. Add later only via method law, one at a time."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from options_offshoot.compare.law import METHOD_LAW_V1
from options_offshoot.localtime import now

INDEX_MAP_DISCLAIMER = (
    "Map only. Do not allocate $20k to the fattest table. "
    "Do not shop the index. Each field is its own tape."
)

NO_TICKETS_FIELD = "index_only"


@dataclass(frozen=True)
class FieldSpec:
    field_id: str
    title: str
    meaning: str
    allows_tickets: bool
    universe_file: str | None
    expiry_rule: str


FIELDS: dict[str, FieldSpec] = {
    "earnings_us_week": FieldSpec(
        field_id="earnings_us_week",
        title="US earnings this week",
        meaning="US names reporting this week, options OI/volume floor",
        allows_tickets=True,
        universe_file="earnings_us_week.txt",
        expiry_rule="nearest_listed_on_or_after_event",
    ),
    "spx_this_friday": FieldSpec(
        field_id="spx_this_friday",
        title="Equity weeklies this Friday",
        meaning="Equity weeklies on an operator freeze list (not SPX index options)",
        allows_tickets=True,
        universe_file="spx_this_friday.txt",
        expiry_rule="this_friday",
    ),
    "index_only": FieldSpec(
        field_id="index_only",
        title="Index map",
        meaning="The index page itself (no tickets)",
        allows_tickets=False,
        universe_file=None,
        expiry_rule="none",
    ),
}


def package_root() -> Path:
    return Path(__file__).resolve().parents[3]


def fields_dir() -> Path:
    return package_root() / "data" / "fields"


def listed_field_ids() -> list[str]:
    return list(METHOD_LAW_V1["predeclared_fields"])


def get_field(field_id: str) -> FieldSpec:
    fid = str(field_id or "").strip()
    if fid not in FIELDS:
        raise KeyError(
            f"unknown field {fid!r}; predeclared={listed_field_ids()}"
        )
    if fid not in listed_field_ids():
        raise KeyError(f"field {fid!r} is not in method_law predeclared_fields")
    return FIELDS[fid]


def this_friday(today: date | None = None) -> date:
    day = today or now().date()
    delta = (4 - day.weekday()) % 7
    return day + timedelta(days=delta)


def load_universe(spec: FieldSpec) -> list[str]:
    if not spec.universe_file:
        return []
    path = fields_dir() / spec.universe_file
    if not path.is_file():
        return []
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.split("#", 1)[0].strip().upper()
        if text:
            out.append(text)
    return out


def freeze_header(spec: FieldSpec) -> dict[str, str]:
    """as_of / source from comment header. Not a reconstitution."""
    meta = {"as_of": "", "source": "", "n": "0"}
    if not spec.universe_file:
        return meta
    path = fields_dir() / spec.universe_file
    if not path.is_file():
        return meta
    names = load_universe(spec)
    meta["n"] = str(len(names))
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw.startswith("#"):
            if raw:
                break
            continue
        body = raw[1:].strip()
        lowered = body.lower()
        if lowered.startswith("as_of:"):
            meta["as_of"] = body.split(":", 1)[1].strip()
        elif lowered.startswith("source:"):
            meta["source"] = body.split(":", 1)[1].strip()
    return meta


def menu_lines() -> list[str]:
    lines = [
        "PREDECLARED FIELDS",
        INDEX_MAP_DISCLAIMER,
        "Pick one. live --field <id>. Do not merge bankrolls.",
        "",
    ]
    for fid in listed_field_ids():
        spec = FIELDS[fid]
        tickets = "tickets" if spec.allows_tickets else "no tickets"
        lines.append(f"  {fid:20}  {tickets:11}  {spec.meaning}")
    return lines
