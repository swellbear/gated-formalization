"""Discovery farm: unused slots, refuse, queue by declared_at, no live steal."""

from __future__ import annotations

import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.clerical_score import maybe_score_farm
from golf_offshoot.learning_lane_15m.cos_tick import (
    ACTION_ASSIGN,
    LAB_FARM_OPEN_JOB,
    LAB_FARM_PROMOTE_JOB,
    LAB_INVENT_JOB,
    decide_cos_action,
)
from golf_offshoot.learning_lane_15m.crew_tick import (
    REASON_F,
    REASON_I,
    REASON_J,
    compute_crew_tick,
)
from golf_offshoot.learning_lane_15m.farm import (
    clone_overlap,
    date_notebooks,
    farm_path,
    farm_scorecard_path,
    keeper_notebooks,
    live_look_closed,
    next_promote,
    notebook_face,
    notebook_status,
    product_skip_kinds,
    promote_ready,
    refuse_reason,
    unused_legal_kinds,
)

FARM_PY = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "golf_offshoot"
    / "learning_lane_15m"
    / "farm.py"
)

CATALOG = {
    "schema": 1,
    "lane": "learning_lane_15m",
    "kinds": [
        {
            "id": "CLOCK-CLOSE-MINUTE",
            "expected_skip_rate": 0.25,
            "legal_now": True,
            "params": ["skip_close_minute"],
        },
        {
            "id": "CLOCK-CIVIL-BOUNDARIES",
            "expected_skip_rate": 0.5,
            "legal_after": "hour-close parks",
            "params": ["skip_close_minutes"],
        },
        {
            "id": "HONER-FAMILY-AMEND",
            "legal_after": "dead honer exam",
        },
    ],
}

LIVE_CLOCK = {
    "id": "R-LIVE-CLOCK",
    "kind": "selection",
    "class": "CLOCK-CLOSE-MINUTE",
    "selects": True,
    "execution": True,
    "declared_at": "2026-09-01T00:00:00-04:00",
    "params": {"skip_close_minute": 0},
}


def _docs(root: Path) -> Path:
    docs = root / "golf-offshoot" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    return docs


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _seed(root: Path, *, executing=LIVE_CLOCK, farm_notebooks=None, burned=None):
    docs = _docs(root)
    _write_json(docs / "LEARNING_LANE_15M_MECHANISM_CATALOG.json", CATALOG)
    rules = [executing] if executing else []
    _write_json(
        docs / "LEARNING_LANE_15M_RULES.json",
        {"schema": 1, "trials_to_date": 2, "rules": rules},
    )
    _write_json(
        docs / "LEARNING_LANE_15M_FARM.json",
        {
            "schema": 1,
            "lane": "learning_lane_15m",
            "notebooks": list(farm_notebooks or []),
        },
    )
    _write_json(
        docs / "LEARNING_LANE_15M_BURNED_CLASSES.json",
        {"classes": list(burned or [])},
    )
    _write_json(
        docs / "LEARNING_LANE_15M_EVIDENCE_BAR.json",
        {
            "looks": {"first_look_n": 70},
            "distinguishable": {
                "effect_floor_usd_per_window": 0.01,
                "matched_exposure": {"draws": 8, "seed": 1},
            },
        },
    )


def _desk():
    return (
        "# Agent desk\n\n"
        "| Field | Value |\n"
        "|-------|--------|\n"
        "| Active role | chief-of-staff |\n"
        "| Job | — |\n"
        "| Status | idle |\n"
        "| Handoff | — |\n\n"
        "## Thread\n\n"
        "- 2026-09-10 17:00 ET  chief-of-staff: idle.\n"
    )


def _watch():
    return {
        "running": True,
        "cycles": "4",
        "interval_s": "90.0",
        "last_at": "2026-09-10T17:00:00-04:00",
    }


def test_farm_module_does_not_import_honer_or_hardcode_hour_close():
    src = FARM_PY.read_text(encoding="utf-8")
    assert "golf_offshoot.honer_15m" not in src
    assert "import honer_15m" not in src
    assert "R-SKIP-HOUR-CLOSE" not in src
    assert product_skip_kinds("learning_lane_15m") == (
        "CLOCK-CLOSE-MINUTE",
        "CLOCK-CIVIL-BOUNDARIES",
        "CLOCK-QUARTER-BOUNDARIES",
        "CLOCK-HOUR-FIRST-HALF",
    )


def test_unused_clock_minutes_ring_i_civil_blocked(tmp_path):
    _seed(tmp_path)
    unused = unused_legal_kinds(root=tmp_path)
    minutes = {
        slot["params"]["skip_close_minute"]
        for slot in unused
        if slot["kind"] == "CLOCK-CLOSE-MINUTE"
    }
    assert minutes == {15, 30, 45}
    assert all(slot["kind"] != "CLOCK-CIVIL-BOUNDARIES" for slot in unused)
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_desk(),
        hub_ok=True,
        live_trial_ids=["R-LIVE-CLOCK"],
        honer_freeze_open=False,
        root=tmp_path,
    )
    assert REASON_I in tick["reason_ids"]
    assert REASON_F not in tick["reason_ids"]
    assert REASON_J not in tick["reason_ids"]


def test_clone_burned_density_refuse(tmp_path):
    _seed(
        tmp_path,
        farm_notebooks=[
            {
                "id": "F-CLOCK-CLOSE-MINUTE-15",
                "kind": "CLOCK-CLOSE-MINUTE",
                "params": {"skip_close_minute": 15},
                "declared_at": "2026-09-10T12:00:00-04:00",
                "execution": False,
                "selects": True,
            }
        ],
        burned=[{"id": "RETUNE-CLOCK-MINUTE", "burned": True, "aliases": []}],
    )
    unused = unused_legal_kinds(root=tmp_path)
    minutes = {
        slot["params"]["skip_close_minute"]
        for slot in unused
        if slot["kind"] == "CLOCK-CLOSE-MINUTE"
    }
    assert 15 not in minutes
    assert 30 in minutes
    assert refuse_reason(
        {
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": 15},
            "expected_skip_rate": 0.25,
        },
        root=tmp_path,
    ).startswith("clone")
    assert "burned" in refuse_reason(
        {
            "kind": "RETUNE-CLOCK-MINUTE",
            "params": {"skip_close_minute": 30},
            "expected_skip_rate": 0.25,
        },
        root=tmp_path,
    )
    assert "density" in refuse_reason(
        {"kind": "THIN", "params": {"skip_close_minutes": []}, "expected_skip_rate": 0.0},
        root=tmp_path,
    )
    assert clone_overlap(
        {"params": {"skip_close_minute": 15}},
        {"params": {"skip_close_minute": 15}},
    )
    assert not clone_overlap(
        {"params": {"skip_close_minute": 15}},
        {"params": {"skip_close_minute": 30}},
    )


def test_mid_look_refuses_promote_four_keepers_declared_at_not_pnl(tmp_path):
    notebooks = [
        {
            "id": "F-CLOCK-CLOSE-MINUTE-15",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": 15},
            "declared_at": "2026-09-10T16:00:00-04:00",
            "execution": False,
            "selects": True,
        },
        {
            "id": "F-CLOCK-CLOSE-MINUTE-30",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": 30},
            "declared_at": "2026-09-10T12:00:00-04:00",
            "execution": False,
            "selects": True,
        },
        {
            "id": "F-CLOCK-CLOSE-MINUTE-45",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": 45},
            "declared_at": "2026-09-10T14:00:00-04:00",
            "execution": False,
            "selects": True,
        },
        {
            "id": "F-CLOCK-CLOSE-MINUTE-45B",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": 45},
            "declared_at": "2026-09-10T18:00:00-04:00",
            "execution": False,
            "selects": True,
        },
    ]
    _seed(tmp_path, farm_notebooks=notebooks)
    for i, row in enumerate(notebooks):
        _write_json(
            farm_scorecard_path(row["id"], root=tmp_path),
            {
                "passes_every_binding_clause": True,
                "n": 70,
                "clause_4_positive_side": {
                    "mean_pnl_rule_fee_adj": 50.0 - i,
                    "passes": True,
                },
            },
        )
    assert live_look_closed(root=tmp_path) is False
    assert promote_ready(root=tmp_path) is False
    tick_mid = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_desk(),
        hub_ok=True,
        live_trial_ids=["R-LIVE-CLOCK"],
        honer_freeze_open=False,
        farm_open=False,
        root=tmp_path,
    )
    assert REASON_J not in tick_mid["reason_ids"]
    docs = _docs(tmp_path)
    _write_json(
        docs / "LEARNING_LANE_15M_SCORECARD_R-LIVE-CLOCK_L1.json",
        {"n": 70, "passes_every_binding_clause": True},
    )
    assert live_look_closed(root=tmp_path) is True
    head = next_promote(root=tmp_path)
    assert head["id"] == "F-CLOCK-CLOSE-MINUTE-30"
    assert head["declared_at"] == "2026-09-10T12:00:00-04:00"
    keepers = keeper_notebooks(root=tmp_path)
    assert keepers[0]["id"] == "F-CLOCK-CLOSE-MINUTE-30"
    assert promote_ready(root=tmp_path) is True
    tick_j = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_desk(),
        hub_ok=True,
        live_trial_ids=[],
        honer_freeze_open=False,
        farm_open=False,
        root=tmp_path,
    )
    assert REASON_J in tick_j["reason_ids"]
    assert REASON_F not in tick_j["reason_ids"]
    decision = decide_cos_action(
        _desk(),
        wake={"roles_owed": [], "crew_tick": tick_j},
        crew_tick=tick_j,
    )
    assert decision["action"] == ACTION_ASSIGN
    assert decision["role"] == "lab"
    assert decision["job"] == LAB_FARM_PROMOTE_JOB


def test_farm_score_reconstructed_decide_does_not_flip_execution(monkeypatch, tmp_path):
    notebook = {
        "id": "F-CLOCK-CLOSE-MINUTE-15",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 15},
        "declared_at": "2026-09-10T12:00:00-04:00",
        "execution": False,
        "selects": True,
    }
    _seed(tmp_path, farm_notebooks=[notebook])
    windows = [
        {
            "window_id": f"w{i}",
            "close_at": "2026-09-10T13:00:00-04:00",
            "posted_yes": 0.4,
            "recorded_pnl": 1.5,
            "stake": 1.0,
        }
        for i in range(70)
    ]
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.gather_tape_windows",
        lambda rule: windows,
    )

    def fake_score(rule_id, scored_windows, **kwargs):
        assert rule_id == "F-CLOCK-CLOSE-MINUTE-15"
        assert scored_windows is windows
        assert kwargs.get("allow_nonbinding") is True
        assert kwargs.get("look") == "L1"
        assert kwargs.get("registry")["trials_to_date"] == 0
        return {
            "n": 70,
            "look": "L1",
            "passes_every_binding_clause": False,
            "windows": [],
        }

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.score_rule",
        fake_score,
    )
    out = maybe_score_farm(root=tmp_path)
    assert out["wrote"] is True
    dest = farm_scorecard_path("F-CLOCK-CLOSE-MINUTE-15", root=tmp_path)
    card = json.loads(dest.read_text(encoding="utf-8"))
    assert card["look"] == "FARM"
    assert card["execution"] is False
    assert "live trial" in card["framing"]
    registry = json.loads(
        (tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_RULES.json").read_text(
            encoding="utf-8"
        )
    )
    assert registry["rules"][0]["execution"] is True
    farm = json.loads(farm_path(root=tmp_path).read_text(encoding="utf-8"))
    assert farm["notebooks"][0]["execution"] is False


def test_quarter_boundaries_unused_then_clone_after_date(tmp_path):
    catalog = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "kinds": [
            {
                "id": "CLOCK-CLOSE-MINUTE",
                "expected_skip_rate": 0.25,
                "legal_now": True,
                "params": ["skip_close_minute"],
            },
            {
                "id": "CLOCK-CIVIL-BOUNDARIES",
                "expected_skip_rate": 0.5,
                "legal_after": "hour-close parks",
                "params": ["skip_close_minutes"],
            },
            {
                "id": "CLOCK-QUARTER-BOUNDARIES",
                "expected_skip_rate": 0.5,
                "legal_now": True,
                "params": ["skip_close_minutes"],
            },
        ],
    }
    farm_notebooks = [
        {
            "id": f"F-CLOCK-CLOSE-MINUTE-{minute}",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": minute},
            "declared_at": "2026-09-10T18:45:00-04:00",
            "execution": False,
            "selects": True,
        }
        for minute in (15, 30, 45)
    ]
    _seed(tmp_path, farm_notebooks=farm_notebooks)
    _write_json(tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_MECHANISM_CATALOG.json", catalog)
    unused = unused_legal_kinds(root=tmp_path)
    assert unused == [
        {
            "kind": "CLOCK-QUARTER-BOUNDARIES",
            "params": {"skip_close_minutes": [15, 45]},
            "expected_skip_rate": 0.5,
        }
    ]
    added = date_notebooks(
        unused,
        declared_at="2026-09-10T19:05:00-04:00",
        root=tmp_path,
    )
    assert len(added) == 1
    assert added[0]["id"] == "F-CLOCK-QUARTER-BOUNDARIES-15-45"
    assert added[0]["execution"] is False
    assert added[0]["params"]["skip_close_minutes"] == [15, 45]
    assert unused_legal_kinds(root=tmp_path) == []
    assert refuse_reason(
        {
            "kind": "CLOCK-QUARTER-BOUNDARIES",
            "params": {"skip_close_minutes": [15, 45]},
            "expected_skip_rate": 0.5,
        },
        root=tmp_path,
    ).startswith("clone")
    assert not clone_overlap(
        {"params": {"skip_close_minutes": [15, 45]}},
        {"params": {"skip_close_minutes": [0, 30]}},
    )


def test_hour_first_half_unused_then_clone_after_date(tmp_path):
    catalog = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "kinds": [
            {
                "id": "CLOCK-CLOSE-MINUTE",
                "expected_skip_rate": 0.25,
                "legal_now": True,
                "params": ["skip_close_minute"],
            },
            {
                "id": "CLOCK-CIVIL-BOUNDARIES",
                "expected_skip_rate": 0.5,
                "legal_after": "hour-close parks",
                "params": ["skip_close_minutes"],
            },
            {
                "id": "CLOCK-QUARTER-BOUNDARIES",
                "expected_skip_rate": 0.5,
                "legal_now": True,
                "params": ["skip_close_minutes"],
            },
            {
                "id": "CLOCK-HOUR-FIRST-HALF",
                "expected_skip_rate": 0.5,
                "legal_now": True,
                "params": ["skip_close_minutes"],
            },
        ],
    }
    farm_notebooks = [
        {
            "id": f"F-CLOCK-CLOSE-MINUTE-{minute}",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": minute},
            "declared_at": "2026-09-10T18:45:00-04:00",
            "execution": False,
            "selects": True,
        }
        for minute in (15, 30, 45)
    ]
    farm_notebooks.append(
        {
            "id": "F-CLOCK-QUARTER-BOUNDARIES-15-45",
            "kind": "CLOCK-QUARTER-BOUNDARIES",
            "params": {"skip_close_minutes": [15, 45]},
            "declared_at": "2026-09-10T19:05:00-04:00",
            "execution": False,
            "selects": True,
        }
    )
    _seed(tmp_path, farm_notebooks=farm_notebooks)
    _write_json(tmp_path / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_MECHANISM_CATALOG.json", catalog)
    unused = unused_legal_kinds(root=tmp_path)
    assert unused == [
        {
            "kind": "CLOCK-HOUR-FIRST-HALF",
            "params": {"skip_close_minutes": [15, 30]},
            "expected_skip_rate": 0.5,
        }
    ]
    added = date_notebooks(
        unused,
        declared_at="2026-09-10T19:34:00-04:00",
        root=tmp_path,
    )
    assert len(added) == 1
    assert added[0]["id"] == "F-CLOCK-HOUR-FIRST-HALF-15-30"
    assert added[0]["execution"] is False
    assert added[0]["params"]["skip_close_minutes"] == [15, 30]
    assert unused_legal_kinds(root=tmp_path) == []
    assert refuse_reason(
        {
            "kind": "CLOCK-HOUR-FIRST-HALF",
            "params": {"skip_close_minutes": [15, 30]},
            "expected_skip_rate": 0.5,
        },
        root=tmp_path,
    ).startswith("clone")
    assert not clone_overlap(
        {"params": {"skip_close_minutes": [15, 30]}},
        {"params": {"skip_close_minutes": [15, 45]}},
    )
    assert not clone_overlap(
        {"params": {"skip_close_minutes": [15, 30]}},
        {"params": {"skip_close_minutes": [0, 30]}},
    )


def test_date_unused_sets_execution_false(tmp_path):
    _seed(tmp_path)
    added = date_notebooks(
        unused_legal_kinds(root=tmp_path),
        declared_at="2026-09-10T17:00:00-04:00",
        root=tmp_path,
    )
    assert {row["params"]["skip_close_minute"] for row in added} == {15, 30, 45}
    assert all(row["execution"] is False for row in added)
    payload = json.loads(farm_path(root=tmp_path).read_text(encoding="utf-8"))
    assert all(row["execution"] is False for row in payload["notebooks"])


def test_cos_i_then_f_priority():
    i_only = {
        "needed": True,
        "reason_ids": [REASON_I],
        "handled_reason_ids": [],
    }
    decision = decide_cos_action(_desk(), wake={"roles_owed": []}, crew_tick=i_only)
    assert decision["job"] == LAB_FARM_OPEN_JOB
    both = {
        "needed": True,
        "reason_ids": [REASON_F, REASON_I],
        "handled_reason_ids": [],
    }
    starved = decide_cos_action(_desk(), wake={"roles_owed": []}, crew_tick=both)
    assert starved["job"] == LAB_INVENT_JOB


def test_gather_tape_windows_uses_fill_all_not_book_pnl(monkeypatch):
    from golf_offshoot.learning_lane_15m.clerical_score import gather_tape_windows
    from golf_offshoot.learning_lane_15m.farm import notebook_as_rule

    rule = notebook_as_rule(
        {
            "id": "F-CLOCK-CLOSE-MINUTE-15",
            "kind": "CLOCK-CLOSE-MINUTE",
            "params": {"skip_close_minute": 15},
            "declared_at": "2026-09-10T12:00:00-04:00",
        }
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.paper.load_decisions",
        lambda: {
            "KXBTC15M-X": {
                "window_id": "KXBTC15M-X",
                "close_at": "2026-09-10T13:15:00-04:00",
                "posted_yes": 0.5,
                "stake": 1.0,
            }
        },
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score._kalshi_results",
        lambda: {"KXBTC15M-X": "yes"},
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score._paper_pnl",
        lambda: {"KXBTC15M-X": -99.0},
    )
    windows = gather_tape_windows(rule)
    assert len(windows) == 1
    assert windows[0]["recorded_pnl"] == 1.0
    assert windows[0]["recorded_pnl"] != -99.0


def test_farm_panel_empty_and_meter(tmp_path):
    from golf_offshoot.learning_lane_15m.farm_hub import farm_panel_html

    empty = farm_panel_html(root=tmp_path)
    assert 'id="farm"' in empty
    assert "Not live" in empty
    assert "No farm file" in empty
    notebook = {
        "id": "F-CLOCK-CLOSE-MINUTE-15",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 15},
        "declared_at": "2026-09-10T12:00:00-04:00",
        "execution": False,
        "selects": True,
    }
    _seed(tmp_path, farm_notebooks=[notebook])
    _write_json(
        farm_scorecard_path("F-CLOCK-CLOSE-MINUTE-15", root=tmp_path),
        {"n": 12, "passes_every_binding_clause": False},
    )
    html = farm_panel_html(root=tmp_path)
    assert "12/70" in html
    assert "Not live" in html
    assert "<th>PnL</th>" not in html
    assert "farm-status-parked" in html
    assert "not a keeper" in html
    assert "farm-status-collecting" not in html
    assert "farm-status-score-owed" not in html


def test_farm_panel_score_owed_is_not_collecting(tmp_path, monkeypatch):
    from golf_offshoot.learning_lane_15m.farm_hub import farm_panel_html

    notebook = {
        "id": "F-CLOCK-HOUR-FIRST-HALF-15-30",
        "kind": "CLOCK-HOUR-FIRST-HALF",
        "params": {"skip_close_minutes": [15, 30]},
        "declared_at": "2026-09-10T19:34:00-04:00",
        "execution": False,
        "selects": True,
    }
    _seed(tmp_path, farm_notebooks=[notebook])
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.farm.settled_n",
        lambda *a, **k: 70,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.farm_hub.settled_n",
        lambda *a, **k: 70,
    )
    status, why = notebook_face(notebook, root=tmp_path, need=70)
    assert status == "score owed"
    assert notebook_status(notebook, root=tmp_path, need=70) == "score owed"
    assert "farm card not written" in why
    html = farm_panel_html(root=tmp_path)
    assert "70/70" in html
    assert "farm-status-score-owed" in html
    assert "farm card not written" in html
    assert "farm-status-collecting" not in html
    assert "<th>PnL</th>" not in html


def test_farm_panel_parked_why_names_clauses_not_pnl(tmp_path):
    from golf_offshoot.learning_lane_15m.farm_hub import farm_panel_html

    notebook = {
        "id": "F-CLOCK-CLOSE-MINUTE-15",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 15},
        "declared_at": "2026-09-10T12:00:00-04:00",
        "execution": False,
        "selects": True,
    }
    _seed(tmp_path, farm_notebooks=[notebook])
    _write_json(
        farm_scorecard_path("F-CLOCK-CLOSE-MINUTE-15", root=tmp_path),
        {
            "n": 70,
            "skip_count": 24,
            "skip_rate": 0.342857,
            "passes_every_binding_clause": False,
            "clause_1_paired_t_vs_floor": {"passes": False},
            "clause_4_positive_side": {
                "passes": False,
                "mean_pnl_rule_fee_adj": -0.016286,
            },
            "clause_5_matched_exposure": {"passes": False},
        },
    )
    html = farm_panel_html(root=tmp_path)
    assert "70/70" in html
    assert "farm-status-parked" in html
    assert "skip 34%" in html
    assert "clauses 1,4,5 fail" in html
    assert "not a keeper" in html
    assert "</code><div class=\"farm-status" in html
    assert "-0.016286" not in html
    assert "mean_pnl" not in html
    assert "<th>PnL</th>" not in html


def test_farm_panel_collecting_stays_collecting(tmp_path, monkeypatch):
    from golf_offshoot.learning_lane_15m.farm_hub import farm_panel_html

    notebook = {
        "id": "F-CLOCK-CLOSE-MINUTE-30",
        "kind": "CLOCK-CLOSE-MINUTE",
        "params": {"skip_close_minute": 30},
        "declared_at": "2026-09-10T12:00:00-04:00",
        "execution": False,
        "selects": True,
    }
    _seed(tmp_path, farm_notebooks=[notebook])
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.farm.settled_n",
        lambda *a, **k: 12,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.farm_hub.settled_n",
        lambda *a, **k: 12,
    )
    assert notebook_status(notebook, root=tmp_path, need=70) == "collecting"
    html = farm_panel_html(root=tmp_path)
    assert "12/70" in html
    assert "farm-status-collecting" in html
    assert "farm-status-score-owed" not in html
    assert "farm-status-parked" not in html
