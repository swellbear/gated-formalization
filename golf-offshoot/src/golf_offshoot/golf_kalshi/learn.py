"""Two learning clocks. Promote by declared_at / hold-out, never by richest pnl."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.golf_kalshi.paper import load_ledger
from golf_offshoot.golf_kalshi.paths import assert_golf_kalshi_path, brain_score_path, recipe_exam_path
from golf_offshoot.golf_kalshi.recipe import PLAYER_BRAIN_VERSION, RECIPE_ID, recipe_v1
from golf_offshoot.learning.loop import brier, logloss
from golf_offshoot.localtime import isoformat_now

LANE = "golf_kalshi"


def settled_tickets(ledger: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    led = ledger if ledger is not None else load_ledger()
    return [
        t
        for t in led.get("tickets") or []
        if str(t.get("status") or "") in {"paper_win", "paper_lose", "void"}
    ]


def recipe_exam(*, new_only: bool = True) -> dict[str, Any]:
    """Wallet-recipe exam on a dated batch of new settles. Declaration order, not pnl."""
    rec = recipe_v1()
    tickets = settled_tickets()
    n = len(tickets)
    wins = sum(1 for t in tickets if t.get("status") == "paper_win")
    payload = {
        "lane": LANE,
        "recipe_id": rec.recipe_id,
        "declared_at": rec.declared_at,
        "at": isoformat_now(),
        "n_settled": n,
        "wins": wins,
        "promote": False,
        "promote_by": "declared_at",
        "not_pnl_ranked": True,
        "next_recipe": None,
        "n_paper_exit": sum(1 for t in (load_ledger().get("tickets") or []) if str(t.get("status") or "") == "paper_exit"),
        "notes": "live mix stays v1.2 paper pause until a later dated recipe survives this exam; paper_exit is path not a Brier label",
    }
    if new_only and n == 0:
        payload["notes"] = "no new settles yet"
    path = recipe_exam_path()
    assert_golf_kalshi_path(path)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def player_brain_score() -> dict[str, Any]:
    """Brier/log-loss on golf Kalshi tickets. suggest_alpha_update stays a candidate."""
    tickets = [t for t in settled_tickets() if t.get("status") in {"paper_win", "paper_lose"}]
    espn_tickets = [t for t in tickets if str(t.get("field_source") or "") == "espn"]
    listed_n = sum(1 for t in tickets if str(t.get("field_source") or "") == "kalshi_listed")
    briers = []
    logs = []
    for ticket in espn_tickets:
        p = ticket.get("model_p")
        if p is None:
            continue
        y = ticket.get("status") == "paper_win"
        briers.append(brier(float(p), y))
        logs.append(logloss(float(p), y))
    holdout_beats_expert = False
    payload = {
        "lane": LANE,
        "brain_version": PLAYER_BRAIN_VERSION,
        "production": "keep_expert",
        "at": isoformat_now(),
        "n": len(briers),
        "n_listed_observation": listed_n,
        "promote_field_source": "espn",
        "brier": float(sum(briers) / len(briers)) if briers else None,
        "logloss": float(sum(logs) / len(logs)) if logs else None,
        "holdout_beats_expert": holdout_beats_expert,
        "candidate": "suggest_alpha_update",
        "promote": False,
        "not_pnl_ranked": True,
        "recipe_id": RECIPE_ID,
    }
    path = brain_score_path()
    assert_golf_kalshi_path(path)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def maybe_promote(*, holdout_beats_expert: bool = False) -> dict[str, Any]:
    """Production stays keep_expert until hold-out actually wins."""
    exam = recipe_exam()
    score = player_brain_score()
    score["holdout_beats_expert"] = bool(holdout_beats_expert)
    score["promote"] = bool(holdout_beats_expert)
    if not holdout_beats_expert:
        score["production"] = "keep_expert"
    path = brain_score_path()
    path.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    return {"recipe_exam": exam, "brain_score": score}
