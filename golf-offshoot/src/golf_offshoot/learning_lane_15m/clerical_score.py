"""Clerical score_rule for the executing factory selection only.

Never scores R-SKIP-COINFLIP. Never re-scores PARK'd R-SKIP-2TO1-FAVORITE.
Never an ADMIT. Does not drop execution. Does not arm.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import (
    paper_dir_15m,
    settlements_dir_15m,
)
from golf_offshoot.learning_lane_15m.rules import (
    SCORECARD_DIR_REL,
    RuleNotScorable,
    active_execution_rule,
    score_rule,
    window_is_lived,
)
from golf_offshoot.localtime import isoformat_now
from golf_offshoot.repo_paths import repo_root

FORBIDDEN_SCORE_IDS = frozenset(
    {
        "R-SKIP-COINFLIP",
        "R-SKIP-2TO1-FAVORITE",
    }
)
STAKE = 1.0


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def scorecard_path(rule_id: str, *, root: Path | None = None, look: str = "L1") -> Path:
    base = (root or repo_root()) / SCORECARD_DIR_REL
    return base / f"LEARNING_LANE_15M_SCORECARD_{rule_id}_{look}.json"


def _fill_all_pnl(posted_yes: float, result: str, *, stake: float = STAKE) -> float:
    outcome = str(result or "").strip().lower()
    if outcome == "yes":
        return round(stake / float(posted_yes) - stake, 2)
    if outcome == "no":
        return round(-stake, 2)
    raise ValueError("fill_all_pnl needs yes/no")


def _kalshi_results() -> dict[str, str]:
    out: dict[str, str] = {}
    root = settlements_dir_15m()
    if not root.is_dir():
        return out
    for path in root.glob("*.json"):
        payload = _load_json(path)
        result = str(payload.get("kalshi_result") or payload.get("result") or "").strip().lower()
        ticker = str(payload.get("ticker") or path.stem)
        if result in {"yes", "no"}:
            out[ticker] = result
        for row in payload.get("rows") or []:
            if not isinstance(row, dict):
                continue
            r = str(row.get("kalshi_result") or "").strip().lower()
            t = str(row.get("ticker") or "")
            if r in {"yes", "no"} and t:
                out[t] = r
    return out


def _paper_pnl() -> dict[str, float]:
    out: dict[str, float] = {}
    root = paper_dir_15m()
    if not root.is_dir():
        return out
    for path in root.glob("*.json"):
        if path.name in {"ledger.json", "rule_decisions.json"}:
            continue
        payload = _load_json(path)
        raw = payload.get("settlement_pnl")
        if isinstance(raw, (int, float)):
            out[path.stem] = float(raw)
            tid = str(payload.get("tournament_id") or "")
            if tid:
                out[tid] = float(raw)
    return out


def gather_lived_windows(rule: dict[str, Any]) -> list[dict[str, Any]]:
    from golf_offshoot.learning_lane_15m.paper import load_decisions

    decisions = load_decisions()
    results = _kalshi_results()
    pnls = _paper_pnl()
    windows: list[dict[str, Any]] = []
    for ticker, row in decisions.items():
        if not isinstance(row, dict):
            continue
        close_at = str(row.get("close_at") or "")
        if not close_at:
            continue
        try:
            if not window_is_lived(rule, close_at=close_at):
                continue
        except Exception:  # noqa: BLE001 — bad close stamp is not a window
            continue
        posted = row.get("posted_yes")
        try:
            posted_f = float(posted)
        except (TypeError, ValueError):
            continue
        result = results.get(str(ticker))
        if result not in {"yes", "no"}:
            continue
        try:
            recorded = _fill_all_pnl(posted_f, result)
        except ValueError:
            continue
        book_pnl = pnls.get(str(ticker))
        if book_pnl is None:
            stem = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(ticker))
            book_pnl = pnls.get(stem)
        windows.append(
            {
                "window_id": str(row.get("window_id") or ticker),
                "close_at": close_at,
                "posted_yes": posted_f,
                "recorded_pnl": float(book_pnl) if book_pnl is not None else recorded,
                "stake": float(row.get("stake") or STAKE) or STAKE,
            }
        )
    return windows


def maybe_score_executing(*, root: Path | None = None) -> dict[str, Any]:
    """Write an L1 scorecard when the executing selection reaches n. Not an ADMIT."""
    rule = active_execution_rule(root=root)
    if rule is None:
        return {"wrote": False, "reason": "no executing selection"}
    rule_id = str(rule.get("id") or "")
    if rule_id in FORBIDDEN_SCORE_IDS:
        return {"wrote": False, "reason": f"forbidden {rule_id}"}
    dest = scorecard_path(rule_id, root=root)
    if dest.is_file():
        return {"wrote": False, "reason": "scorecard already exists", "path": str(dest)}
    windows = gather_lived_windows(rule)
    from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar

    bar = load_evidence_bar(root=root)
    need = int((bar.get("looks") or {}).get("first_look_n") or 70)
    if len(windows) < need:
        return {"wrote": False, "reason": f"n={len(windows)} < {need}", "n": len(windows)}
    try:
        card = score_rule(rule_id, windows, look="L1", root=root)
    except RuleNotScorable as exc:
        return {"wrote": False, "reason": str(exc), "n": len(windows)}
    card["framing"] = (
        "Clerical score_rule card. Not an ADMIT, not arm, not a Founder GO. "
        "Park vs continue is the registry falsifier; this write does not drop execution."
    )
    card["clerical"] = True
    card["scored_at"] = isoformat_now()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    return {"wrote": True, "path": str(dest), "n": card.get("n"), "passes": card.get("passes_every_binding_clause")}
