"""One Kalshi clock, factory vs honer actions only. No money."""

from __future__ import annotations

import html


def _disagreements_html() -> str:
    try:
        from golf_offshoot.two_brains import last_disagreements, sync

        sync()
        rows = last_disagreements(8)
    except Exception:
        return ""
    if not rows:
        return (
            "<h3>Last disagreements</h3>"
            '<p class="help">None yet. Skip vs fill only. Pending is not zero.</p>'
        )
    items = []
    for row in rows:
        ticker = html.escape(str(row.get("ticker") or ""))
        factory = html.escape(str(row.get("factory_action") or "n/a"))
        honer = html.escape(str(row.get("honer_search_action") or "n/a"))
        window = html.escape(str(row.get("window_et") or ""))
        items.append(f"<li><code>{ticker}</code> {window}: factory {factory} / honer search {honer}</li>")
    return (
        "<h3>Last disagreements</h3>"
        '<p class="help">Skip vs fill only. Actions only. Pending is not zero.</p>'
        f"<ul>{''.join(items)}</ul>"
    )


def this_window_html() -> str:
    factory_phrase = "no decision yet"
    honer_phrase = "no decision yet"
    exam_phrase = "not started"
    ticker = ""
    window_et = ""
    kalshi = "n/a"
    try:
        from golf_offshoot.learning_lane_15m.standing import current_factory_action

        factory = current_factory_action()
        factory_phrase = str(factory.get("phrase") or "no decision yet")
        ticker = str(factory.get("ticker") or "")
        window_et = str(factory.get("window_et") or "")
        kalshi = str(factory.get("kalshi") or "n/a")
    except Exception:
        factory_phrase = "factory standing unavailable"
    try:
        from golf_offshoot.honer_15m.board import current_exam_action, current_search_action

        honer = current_search_action()
        exam = current_exam_action()
        honer_phrase = str(honer.get("phrase") or "no decision yet")
        if not ticker:
            ticker = str(honer.get("ticker") or "")
        if not window_et:
            window_et = str(honer.get("window_et") or "")
        if kalshi in {"n/a", ""} and honer.get("kalshi"):
            kalshi = str(honer.get("kalshi"))
        exam_phrase = str(exam.get("phrase") or "not started")
    except Exception:
        honer_phrase = "honer standing unavailable"
    clock = window_et or "this window"
    name = html.escape(ticker) if ticker else "no shared ticker yet"
    return (
        '<section class="panel this-window-panel" id="this-window">'
        "<h2>This window — two brains, one clock</h2>"
        '<p class="help">Actions only. Do not add factory and honer money. '
        "A skip is not a loss. Pending is not zero.</p>"
        f"<p><strong>{html.escape(clock)}</strong> · <code>{name}</code></p>"
        "<ul>"
        f"<li>Factory: {html.escape(factory_phrase)}</li>"
        f"<li>Honer search: {html.escape(honer_phrase)}</li>"
        f"<li>Honer exam: {html.escape(exam_phrase)}</li>"
        f"<li>Kalshi: {html.escape(kalshi)}</li>"
        "</ul>"
        f"{_disagreements_html()}"
        "</section>"
    )
