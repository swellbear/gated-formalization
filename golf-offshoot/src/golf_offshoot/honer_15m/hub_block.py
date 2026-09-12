"""8765 honer panel. No combined bankroll. No winner vs Lineage A."""

from __future__ import annotations

import html

from golf_offshoot.data_feeds.kalshi_15m import quote_text
from golf_offshoot.honer_15m.board import HonerRow, HonerStanding, collect_standing


def _bold_stars(text: str) -> str:
    out = html.escape(text)
    while "**" in out:
        out = out.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return out


def _search_table(rows: list[HonerRow]) -> str:
    if not rows:
        return "<p class=\"help\">Honer has not taken a search window yet.</p>"
    head = (
        "<thead><tr>"
        "<th>Ticker</th><th>Window ET</th><th>Action</th><th>Posted YES</th>"
        "<th>Cutoff</th><th>Near line</th><th>Spread</th><th>Wide-book</th><th>Thin-book</th>"
        "<th>Kalshi</th><th>Paper pnl</th><th>Why</th><th>Source</th>"
        "</tr></thead>"
    )
    body = ["<tbody>"]
    for row in rows:
        kalshi = "still waiting on Kalshi" if row.pending else (row.kalshi_result.upper() or "n/a")
        posted = row.posted_display()
        cutoff = quote_text(row.theta)
        body.append(
            "<tr>"
            f"<td><code>{html.escape(row.ticker)}</code></td>"
            f"<td>{html.escape(row.window_et)}</td>"
            f"<td>{html.escape(row.action_label)}</td>"
            f"<td>{html.escape(posted)}</td>"
            f"<td>{html.escape(cutoff)}</td>"
            f"<td>{html.escape(row.near_line_text)}</td>"
            f"<td>{html.escape(row.spread_text)}</td>"
            f"<td>{html.escape(row.delta_text)}</td>"
            f"<td>{html.escape(row.gamma_text)}</td>"
            f"<td>{html.escape(kalshi)}</td>"
            f"<td>{html.escape(row.pnl_text)}</td>"
            f"<td>{html.escape(row.why)}</td>"
            f"<td class=\"src\">{html.escape(row.source)}</td>"
            "</tr>"
        )
    body.append("</tbody>")
    return f'<div class="honer-table-wrap"><table class="honer-board">{head}{"".join(body)}</table></div>'


def _exam_table(rows: list[HonerRow], standing: HonerStanding) -> str:
    if standing.phase in {"searching", "freeze_ready"} and not rows:
        return f'<p class="help">Exam idle. {html.escape(standing.freeze_meter)}</p>'
    if not rows:
        return f'<p class="help">Exam idle. {html.escape(standing.freeze_meter)}</p>'
    head = (
        "<thead><tr>"
        "<th>Ticker</th><th>Window ET</th><th>Action</th><th>Posted YES</th>"
        "<th>Frozen cutoff</th><th>Near line</th><th>Spread</th><th>Wide-book</th><th>Thin-book</th>"
        "<th>Exam k</th><th>Kalshi</th><th>Exam pnl</th>"
        "<th>Always-buy</th><th>d</th><th>Why</th><th>Source</th>"
        "</tr></thead>"
    )
    body = ["<tbody>"]
    for row in rows:
        kalshi = "still waiting on Kalshi" if row.pending else (row.kalshi_result.upper() or "n/a")
        posted = row.posted_display()
        cutoff = quote_text(row.theta)
        always = row.fill_all_text or ("n/a" if row.pending else "")
        d = row.d_text or ("n/a" if row.pending else "")
        k = str(row.exam_k) if row.exam_k is not None else "n/a"
        body.append(
            "<tr>"
            f"<td><code>{html.escape(row.ticker)}</code></td>"
            f"<td>{html.escape(row.window_et)}</td>"
            f"<td>{html.escape(row.action_label)}</td>"
            f"<td>{html.escape(posted)}</td>"
            f"<td>{html.escape(cutoff)}</td>"
            f"<td>{html.escape(row.near_line_text)}</td>"
            f"<td>{html.escape(row.spread_text)}</td>"
            f"<td>{html.escape(row.delta_text)}</td>"
            f"<td>{html.escape(row.gamma_text)}</td>"
            f"<td>{html.escape(k)}</td>"
            f"<td>{html.escape(kalshi)}</td>"
            f"<td>{html.escape(row.pnl_text)}</td>"
            f"<td>{html.escape(always)}</td>"
            f"<td>{html.escape(d)}</td>"
            f"<td>{html.escape(row.why)}</td>"
            f"<td class=\"src\">{html.escape(row.source)}</td>"
            "</tr>"
        )
    body.append("</tbody>")
    return f'<div class="honer-table-wrap"><table class="honer-board">{head}{"".join(body)}</table></div>'


def _exam_action_strip(standing: HonerStanding) -> str:
    if standing.phase not in {"exam_open", "exam_complete"}:
        return ""
    search = standing.current_search
    exam = standing.current_exam
    if search is None:
        return ""
    exam_bit = exam.action_label if exam is not None else "no exam decision"
    return (
        f'<p class="this-window">Same window {html.escape(search.ticker)} · '
        f"search={html.escape(search.action_label)} · exam={html.escape(exam_bit)}. "
        "Actions only — do not add the books.</p>"
    )


def board_html(*, extra_html: str = "") -> str:
    standing = collect_standing()
    happened = "".join(f"<li>{html.escape(line)}</li>" for line in standing.happened)
    if not happened:
        happened = "<li>Honer has not taken a window yet.</li>"
    keep = f"<p class=\"loud\">{html.escape(standing.not_a_keep)}</p>" if standing.not_a_keep else ""
    return (
        '<section class="panel honer-sandbox book-honer" id="honer" data-book="honer">'
        "<h2>Honer — sibling search and exam</h2>"
        '<p class="help">Discovery organ for this gym. Factory AND-skip consult is off. '
        "Freeze still in-band. Not Lineage A, not a keep, books do not merge, zero-fee. "
        "Trading NOT ARMED. Skips are rows. Do not add these bankrolls to Lineage A.</p>"
        '<div class="standing">'
        "<h3>What it is</h3>"
        f"<p>{_bold_stars(standing.what_it_is)}</p>"
        "<h3>Where it stands</h3>"
        f"<p>{_bold_stars(standing.where_it_stands)}</p>"
        "<h3>Library</h3>"
        f"<p>{_bold_stars(standing.library_line)}</p>"
        "<h3>Last thing that happened</h3>"
        f"<p>{_bold_stars(standing.last_happened)}</p>"
        "<h3>The two books</h3>"
        f"<p>{html.escape(standing.two_books)}</p>"
        f"<p class=\"help\">{html.escape(standing.glossary)}</p>"
        f'<p class="help">Cutoff trail (search): {html.escape(standing.theta_trail)}</p>'
        f"{keep}"
        "</div>"
        "<h3>What just happened</h3>"
        f"<ul class=\"happened\">{happened}</ul>"
        f"{extra_html}"
        "<h3>Search book</h3>"
        f"{_search_table(standing.search_rows)}"
        "<h3>Exam book</h3>"
        f"{_exam_table(standing.exam_rows, standing)}"
        f"{_exam_action_strip(standing)}"
        "</section>"
    )


def sandbox_html(*, extra_html: str = "") -> str:
    """Full honer panel. Kept name so the hub import stays stable."""
    try:
        return board_html(extra_html=extra_html)
    except Exception:
        return (
            '<section class="panel honer-sandbox book-honer" id="honer" data-book="honer">'
            "<h2>honer_15m sandbox</h2>"
            '<p class="help">honer_15m sandbox unavailable this render. Live 15m journal is unchanged. '
            "Do not add honer bankrolls to Lineage A. Books do not merge.</p>"
            "</section>"
        )
