"""8765 Farm panel. File-derived n/70 meters. Not live. No farm pnl."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.farm import (
    farm_path,
    first_look_n,
    keeper_notebooks,
    notebook_status,
    progress_meter,
    progress_pct,
    settled_n,
)
from golf_offshoot.learning_lane_15m.sibling_sync import ORIGIN_SIBLING, observed_farm_payload


def _params_text(params: dict[str, Any]) -> str:
    if not params:
        return "—"
    if params.get("skip_close_minute") is not None:
        return f"skip :{int(params['skip_close_minute']):02d}"
    if params.get("skip_close_minutes") is not None:
        mins = ",".join(f":{int(x):02d}" for x in params["skip_close_minutes"])
        return f"skip {mins}"
    return html.escape(str(params))


def _origin_label(meta: dict[str, Any]) -> str:
    if str(meta.get("source") or "") != "origin":
        return ""
    sha = str(meta.get("sha") or "").strip()
    short = sha[:7] if sha else ""
    ref = str(meta.get("ref") or ORIGIN_SIBLING)
    if short:
        return f"from {ref} @ {short}"
    return f"from {ref}"


def farm_panel_html(*, root: Path | None = None) -> str:
    path = farm_path(root=root)
    payload, meta = observed_farm_payload(root=root)
    notebooks = [row for row in (payload.get("notebooks") or []) if isinstance(row, dict)]
    help_txt = (
        "Discovery notebooks on the shared tape. Not live. Not an ADMIT. "
        "One chair stays What is on trial. Do not add farm pnl to Lineage A."
    )
    origin_line = _origin_label(meta)
    loud = "Not live"
    if origin_line:
        loud = f"Not live. {origin_line}"
    if not notebooks and not path.is_file() and str(meta.get("source") or "") != "origin":
        return (
            '<section class="panel farm-sandbox" id="farm">'
            "<h2>Farm — discovery notebooks</h2>"
            f'<p class="help">{html.escape(help_txt)}</p>'
            f'<p class="loud">{html.escape(loud)}</p>'
            '<p class="help">Farm idle. No farm file. Not invented rows.</p>'
            "</section>"
        )
    if not notebooks:
        idle = (
            '<section class="panel farm-sandbox" id="farm">'
            "<h2>Farm — discovery notebooks</h2>"
            f'<p class="help">{html.escape(help_txt)}</p>'
            f'<p class="loud">{html.escape(loud)}</p>'
            '<p class="help">Farm idle. No notebooks dated. Not live.</p>'
            "</section>"
        )
        return idle
    need = first_look_n(root=root)
    keepers = keeper_notebooks(root=root, farm=payload)
    head = keepers[0] if keepers else None
    head_id = str(head.get("id") or "") if head else ""
    ordered = sorted(
        notebooks,
        key=lambda row: (
            str(row.get("declared_at") or ""),
            str(row.get("kind") or ""),
            str(row.get("id") or ""),
        ),
    )
    body = ["<tbody>"]
    for row in ordered:
        rid = str(row.get("id") or "")
        n = settled_n(row, root=root)
        meter = progress_meter(n, need)
        pct = progress_pct(n, need)
        status = notebook_status(row, root=root, farm=payload, need=need)
        next_line = "next-in-line" if rid and rid == head_id else ""
        body.append(
            "<tr>"
            f"<td><code>{html.escape(rid)}</code></td>"
            f"<td>{html.escape(str(row.get('kind') or ''))}</td>"
            f"<td>{_params_text(row.get('params') or {})}</td>"
            f"<td>{html.escape(str(row.get('declared_at') or ''))}</td>"
            "<td>"
            f'<div class="farm-meter" aria-label="{html.escape(meter)}">'
            f'<span class="farm-meter-fill" style="width:{pct}%"></span>'
            "</div>"
            f"<span>{html.escape(meter)}</span>"
            "</td>"
            f"<td>{html.escape(status)}</td>"
            f"<td>{html.escape(next_line)}</td>"
            "</tr>"
        )
    body.append("</tbody>")
    head_row = (
        "<thead><tr>"
        "<th>Notebook</th><th>Kind</th><th>Params</th><th>declared_at</th>"
        "<th>Progress</th><th>Status</th><th>Queue</th>"
        "</tr></thead>"
    )
    return (
        '<section class="panel farm-sandbox" id="farm">'
        "<h2>Farm — discovery notebooks</h2>"
        f'<p class="help">{html.escape(help_txt)}</p>'
        f'<p class="loud">{html.escape(loud)}</p>'
        '<div class="farm-table-wrap">'
        f'<table class="farm-board">{head_row}{"".join(body)}</table>'
        "</div>"
        "</section>"
    )
