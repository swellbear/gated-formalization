"""Index map of predeclared fields. Not an allocator."""

from __future__ import annotations

from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER, listed_field_ids
from options_offshoot.models.schemas import FieldRun


def map_stats(run: FieldRun) -> dict:
    n = len(run.rows)
    n_ask = sum(
        1
        for r in run.rows
        if r.contract.quote.has_real_ask and r.contract.liquid
    )
    n_clear = sum(1 for r in run.rows if r.clears_ask)
    return {
        "field_id": run.field_id,
        "n": n,
        "n_ask": n_ask,
        "n_clear_ask": n_clear,
        "map_only": bool(run.extra.get("map_only")),
    }


def format_index(stats: list[dict]) -> str:
    """Always sorted by field_id. Never by n_clear_ask (no shopping)."""
    ordered = sorted(stats, key=lambda r: str(r.get("field_id") or ""))
    lines = [
        "FIELDS INDEX  (map only)",
        INDEX_MAP_DISCLAIMER,
        "Do not retune t from one expiry. Do not merge $20k books.",
        "",
        f"{'field':<22} {'n':>6} {'n_ask':>8} {'n_clear':>8}",
        "-" * 48,
    ]
    for row in ordered:
        if row.get("n") is None:
            lines.append(
                f"{row['field_id']:<22} {'n/a':>6} {'n/a':>8} {'n/a':>8}"
            )
        else:
            lines.append(
                f"{row['field_id']:<22} {int(row['n']):6d} "
                f"{int(row['n_ask']):8d} {int(row['n_clear_ask']):8d}"
            )
    lines += [
        "",
        "n       contracts in the last snapshot (0 for index_only).",
        "n_ask   real bid/ask and size floor.",
        "n_clear vs-ask clears t. Not a signal to dump the bankroll here.",
    ]
    return "\n".join(lines)


def empty_index() -> list[dict]:
    return [
        {"field_id": fid, "n": None, "n_ask": None, "n_clear_ask": None}
        for fid in listed_field_ids()
    ]
