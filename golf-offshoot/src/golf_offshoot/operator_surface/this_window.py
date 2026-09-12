"""One Kalshi clock, factory vs honer actions only. No money."""

from __future__ import annotations

import html


def consult_is_live() -> bool:
    """True only when honer_consult.json has consult_enabled exactly true."""
    try:
        from golf_offshoot.learning_lane_15m.consult_honer import (
            consult_is_enabled,
            load_consult_snapshot,
        )

        return consult_is_enabled(load_consult_snapshot())
    except Exception:
        return False


def factory_chair_selects() -> bool:
    """True when the paper loop honours a selecting rule, not fill-all."""
    try:
        from golf_offshoot.learning_lane_15m.rules import active_execution_rule

        rule = active_execution_rule()
    except Exception:
        return False
    return bool(rule and rule.get("selects"))


def factory_title() -> str:
    if factory_chair_selects():
        return "Factory — live 70"
    try:
        from golf_offshoot.learning_lane_15m.rules import active_execution_rule

        rule = active_execution_rule()
    except Exception:
        rule = None
    if rule:
        return "Factory — fill-all baseline"
    return "Factory"


def factory_spine_blurb() -> str:
    if factory_chair_selects():
        return (
            "Paper diary of YES tickets under the executing selection rule. "
            "Named baseline is the comparison, not a second live brain. "
            "Not scored. Not bound. Not a keep."
        )
    return (
        "Paper diary of YES tickets under the executing fill-all baseline. "
        "No selecting look is on the chair. Not scored. Not bound. Not a keep."
    )


def _disagreements_html() -> str:
    try:
        from golf_offshoot.two_brains import last_disagreements

        rows = last_disagreements(8)
    except Exception:
        return ""
    if not rows:
        if consult_is_live():
            empty_help = "None yet. Skip vs fill only. Pending is not zero."
        else:
            empty_help = (
                "None yet. Factory book vs honer observation. Consult is off. Pending is not zero."
            )
        return (
            "<h3>Last disagreements</h3>"
            f'<p class="help">{html.escape(empty_help)}</p>'
        )
    items = []
    for row in rows:
        ticker = html.escape(str(row.get("ticker") or ""))
        factory = html.escape(str(row.get("factory_action") or "n/a"))
        honer = html.escape(str(row.get("honer_search_action") or "n/a"))
        window = html.escape(str(row.get("window_et") or ""))
        items.append(f"<li><code>{ticker}</code> {window}: factory {factory} / honer search {honer}</li>")
    if consult_is_live():
        head = "Last disagreements"
        help_bit = "Skip vs fill only. Actions only. Pending is not zero."
    else:
        head = "Last disagreements"
        help_bit = (
            "Factory book vs honer observation. Consult is off. "
            "Skip vs fill only. Actions only. Pending is not zero."
        )
    return (
        f"<h3>{head}</h3>"
        f'<p class="help">{help_bit}</p>'
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
        from golf_offshoot.learning_lane_15m.standing import (
            cached_factory_standing,
            current_factory_action,
        )

        factory_standing = cached_factory_standing()
        factory = current_factory_action(standing=factory_standing)
        factory_phrase = str(factory.get("phrase") or "no decision yet")
        ticker = str(factory.get("ticker") or "")
        window_et = str(factory.get("window_et") or "")
        kalshi = str(factory.get("kalshi") or "n/a")
    except Exception:
        factory_phrase = "factory standing unavailable"
    try:
        from golf_offshoot.honer_15m.board import (
            cached_honer_standing,
            current_exam_action,
            current_search_action,
        )

        honer_standing = cached_honer_standing()
        honer = current_search_action(standing=honer_standing)
        exam = current_exam_action(standing=honer_standing)
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
    live = consult_is_live()
    if live:
        heading = "This window — two brains, one clock"
        help_bit = (
            "Actions only. Do not add factory and honer money. "
            "A skip is not a loss. Pending is not zero."
        )
        honer_label = "Honer search"
        exam_label = "Honer exam"
    else:
        heading = "This window — one clock"
        help_bit = (
            "Factory is the live book. Honer search and exam are observation — consult is off. "
            "Do not add factory and honer money. A skip is not a loss. Pending is not zero."
        )
        honer_label = "Honer search (observation)"
        exam_label = "Honer exam (observation)"
    return (
        '<section class="panel this-window-panel" id="this-window">'
        f"<h2>{html.escape(heading)}</h2>"
        f'<p class="help">{html.escape(help_bit)}</p>'
        f"<p><strong>{html.escape(clock)}</strong> · <code>{name}</code></p>"
        "<ul>"
        f"<li>Factory: {html.escape(factory_phrase)}</li>"
        f"<li>{html.escape(honer_label)}: {html.escape(honer_phrase)}</li>"
        f"<li>{html.escape(exam_label)}: {html.escape(exam_phrase)}</li>"
        f"<li>Kalshi: {html.escape(kalshi)}</li>"
        "</ul>"
        f"{_disagreements_html()}"
        "</section>"
    )
