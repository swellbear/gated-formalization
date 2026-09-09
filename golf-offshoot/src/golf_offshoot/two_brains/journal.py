"""Action-only factory vs honer contrast. No money. No winner."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.board import window_et_label
from golf_offshoot.honer_15m.books import load_decisions as load_honer_decisions
from golf_offshoot.honer_15m.policy import load_policy
from golf_offshoot.localtime import now
from golf_offshoot.two_brains.paths import assert_two_brains_path, journal_path

MONEY_KEYS = frozenset({"pnl", "d", "bankroll", "winner"})
ACTIONS = frozenset({"fill", "skip"})


def _near_line(posted: Any, theta: Any, band: float) -> bool | None:
    if posted is None or theta is None:
        return None
    try:
        return abs(float(posted) - float(theta)) <= float(band)
    except (TypeError, ValueError):
        return None


def _action(row: dict[str, Any] | None) -> str:
    if not row:
        return ""
    value = str(row.get("action") or "").strip().lower()
    return value if value in ACTIONS else value


def _strip_money(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if k not in MONEY_KEYS}


def load_journal() -> list[dict[str, Any]]:
    path = journal_path()
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            payload = json.loads(text)
        except ValueError:
            continue
        if isinstance(payload, dict):
            rows.append(_strip_money(payload))
    return rows


def last_disagreements(limit: int = 8) -> list[dict[str, Any]]:
    rows = []
    for row in reversed(load_journal()):
        factory = str(row.get("factory_action") or "")
        honer = str(row.get("honer_search_action") or "")
        if factory in ACTIONS and honer in ACTIONS and factory != honer:
            rows.append(row)
        if len(rows) >= int(limit):
            break
    return rows


def sync() -> list[dict[str, Any]]:
    """Join factory and honer decisions by ticker. Idempotent. Actions only."""
    from golf_offshoot.learning_lane_15m.paper import load_decisions as load_factory_decisions

    band = float(load_policy()["step_band"])
    factory = load_factory_decisions()
    search = load_honer_decisions("search")
    exam = load_honer_decisions("exam")
    tickers = sorted({*factory, *search, *exam})
    existing = {str(r.get("ticker") or ""): r for r in load_journal()}
    rows: list[dict[str, Any]] = []
    for ticker in tickers:
        if not ticker:
            continue
        fac = factory.get(ticker) if isinstance(factory.get(ticker), dict) else {}
        hon = search.get(ticker) if isinstance(search.get(ticker), dict) else {}
        ex = exam.get(ticker) if isinstance(exam.get(ticker), dict) else {}
        posted = hon.get("posted_yes")
        if posted is None:
            posted = fac.get("posted_yes")
        theta = hon.get("theta")
        close_at = str(hon.get("close_at") or fac.get("close_at") or "")
        window_id = str(hon.get("window_id") or fac.get("window_id") or "")
        row = {
            "ticker": ticker,
            "window_et": window_et_label(ticker=ticker, close_at=close_at, window_id=window_id),
            "factory_action": _action(fac),
            "honer_search_action": _action(hon),
            "honer_exam_action": _action(ex),
            "near_line": _near_line(posted, theta, band),
            "posted_yes": posted,
            "honer_theta": theta,
            "factory_rule_id": str(fac.get("rule_id") or ""),
            "updated_at": now().isoformat(),
        }
        prior = existing.get(ticker) or {}
        if prior and all(prior.get(k) == row.get(k) for k in row if k != "updated_at"):
            row["updated_at"] = prior.get("updated_at") or row["updated_at"]
        for banned in MONEY_KEYS:
            row.pop(banned, None)
        rows.append(row)
    path = journal_path()
    assert_two_brains_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(row, default=str) + "\n" for row in rows)
    path.write_text(body, encoding="utf-8")
    return rows
