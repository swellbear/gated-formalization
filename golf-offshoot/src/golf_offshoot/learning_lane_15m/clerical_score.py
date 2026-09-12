"""Clerical score_rule for the executing factory selection only.

Never scores R-SKIP-COINFLIP. Never re-scores PARK'd R-SKIP-2TO1-FAVORITE.
Never an ADMIT. Does not drop execution. Does not arm.
"""

from __future__ import annotations

import json
import subprocess
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


def load_l1_card(rule_id: str, *, root: Path | None = None) -> dict[str, Any]:
    return _load_json(scorecard_path(rule_id, root=root, look="L1"))


def operator_look_stamp(card: dict[str, Any] | None) -> str:
    return str((card or {}).get("operator_look") or "").strip().upper()


def _head_commit_sha(*, root: Path | None = None) -> str:
    git_root = root if root is not None and (Path(root) / ".git").exists() else repo_root()
    try:
        from golf_offshoot.operator_surface.reload import read_git_tip

        tip = str(read_git_tip(git_root) or "")
        if "@" in tip:
            sha = tip.rsplit("@", 1)[-1].strip()
            if sha:
                return sha
    except Exception:  # noqa: BLE001 — stamp empty rather than invent
        pass
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(git_root),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if proc.returncode == 0:
            return (proc.stdout or "").strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


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


def gather_tape_windows(rule: dict[str, Any]) -> list[dict[str, Any]]:
    """Settled tape after declared_at. Fill-all pnl only. Never live skip/fill book pnl."""
    from golf_offshoot.learning_lane_15m.paper import load_decisions

    decisions = load_decisions()
    results = _kalshi_results()
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
        windows.append(
            {
                "window_id": str(row.get("window_id") or ticker),
                "close_at": close_at,
                "posted_yes": posted_f,
                "recorded_pnl": recorded,
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
    windows.sort(key=lambda row: str(row.get("close_at") or ""))
    from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar

    bar = load_evidence_bar(root=root)
    need = int((bar.get("looks") or {}).get("first_look_n") or 70)
    if len(windows) < need:
        return {"wrote": False, "reason": f"n={len(windows)} < {need}", "n": len(windows)}
    # Extra fills after the first 70 are not L2. L1 is the first 70 lived windows.
    windows = windows[:need]
    try:
        card = score_rule(rule_id, windows, look="L1", root=root, allow_nonbinding=True)
    except RuleNotScorable as exc:
        return {"wrote": False, "reason": str(exc), "n": len(windows)}
    card["framing"] = (
        "Clerical score_rule card. Not an ADMIT, not arm, not a Founder GO. "
        "Park vs continue is the registry falsifier; this write does not drop execution."
    )
    card["clerical"] = True
    card["allow_nonbinding"] = True
    card["scored_at"] = isoformat_now()
    card["commit_sha"] = _head_commit_sha(root=root)
    card["committed_at"] = str(card.get("scored_at") or isoformat_now())
    if card.get("passes_every_binding_clause") is not True:
        if card.get("density_fail") or card.get("undecidable"):
            card["caveat"] = (
                "L1 written as undecidable / density-fail. Lived skip_count "
                "is below the 10/n density floor, or the look filled none. "
                "Not a t-test vs δ. Not an ADMIT. Operator PARK "
                "from this card. This write does not drop execution."
            )
        else:
            card["caveat"] = (
                "L1 written even though a binding clause or critic δ FAIL. "
                "Not an ADMIT. Operator PARK or CONTINUE from this card. "
                "This write does not drop execution."
            )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    return {"wrote": True, "path": str(dest), "n": card.get("n"), "passes": card.get("passes_every_binding_clause")}


def maybe_score_farm(*, root: Path | None = None) -> dict[str, Any]:
    """Score farm notebooks on reconstructed decide(). Never drops execution. Not an ADMIT."""
    from golf_offshoot.learning_lane_15m.farm import (
        FORBIDDEN_FARM_IDS,
        farm_scorecard_path,
        notebook_as_rule,
    )
    from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar
    from golf_offshoot.learning_lane_15m.sibling_sync import observed_farm_payload

    payload, _meta = observed_farm_payload(root=root)
    notebooks = [row for row in (payload.get("notebooks") or []) if isinstance(row, dict)]
    if not notebooks:
        return {"wrote": False, "reason": "no farm notebooks", "cards": []}
    try:
        bar = load_evidence_bar(root=root)
    except Exception as exc:  # noqa: BLE001
        return {"wrote": False, "reason": f"bar unreadable: {exc}", "cards": []}
    need = int((bar.get("looks") or {}).get("first_look_n") or 70)
    wrote = False
    cards: list[dict[str, Any]] = []
    for notebook in notebooks:
        rid = str(notebook.get("id") or "")
        if not rid or rid in FORBIDDEN_SCORE_IDS or rid in FORBIDDEN_FARM_IDS:
            continue
        if notebook.get("execution") is True:
            continue
        dest = farm_scorecard_path(rid, root=root)
        if dest.is_file():
            continue
        rule = notebook_as_rule(notebook)
        windows = gather_tape_windows(rule)
        if len(windows) < need:
            cards.append({"id": rid, "wrote": False, "reason": f"n={len(windows)} < {need}", "n": len(windows)})
            continue
        synth = {"rules": [rule], "trials_to_date": 0}
        try:
            card = score_rule(
                rid,
                windows,
                look="L1",
                root=root,
                bar=bar,
                registry=synth,
                allow_nonbinding=True,
            )
        except RuleNotScorable as exc:
            cards.append({"id": rid, "wrote": False, "reason": str(exc), "n": len(windows)})
            continue
        card["look"] = "FARM"
        card["framing"] = (
            "Farm notebook score. Isolated decide() on the shared tape. "
            "Not an ADMIT, not a live trial, not Established, not Lineage A."
        )
        card["notebook"] = True
        card["clerical"] = True
        card["execution"] = False
        card["scored_at"] = isoformat_now()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
        wrote = True
        cards.append(
            {
                "id": rid,
                "wrote": True,
                "path": str(dest),
                "n": card.get("n"),
                "passes": card.get("passes_every_binding_clause"),
            }
        )
    return {"wrote": wrote, "cards": cards}
