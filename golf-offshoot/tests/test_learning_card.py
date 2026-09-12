"""Learning card: quotes and registry fields only. No invented horse."""

from __future__ import annotations

import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.learning_card import (
    CAVEATS_REL,
    DIGEST_REL,
    EMPTY_ON_TRIAL,
    build_card,
    card_proof_token,
    write_learning_card,
)
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.operator_surface.hub import render_hub


def _registry(*, execution_baseline=True, extra=None):
    rules = [
        {
            "id": "R-BASELINE-FILL-ALL",
            "kind": "baseline",
            "execution": execution_baseline,
            "selects": False,
            "rule": "Fill every candidate window.",
            "falsifier": "Not a claim.",
        }
    ]
    if extra:
        rules.append(extra)
    return {
        "schema": 1,
        "lane": "learning_lane_15m",
        "rules": rules,
    }


def _tree(tmp_path: Path, *, registry=None, proposed=None, note=None, decisions=None, journal_at="11:00"):
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True)
    (tmp_path / "latest").mkdir(parents=True)
    (tmp_path / "paper").mkdir(parents=True)
    (docs / "LEARNING_LANE_15M_RULES.json").write_text(
        json.dumps(registry or _registry()), encoding="utf-8"
    )
    (docs / "LEARNING_LANE_15M_METHOD_PARK.md").write_text(
        "# park\nNo selection rule rows.\n", encoding="utf-8"
    )
    (docs / "LEARNING_LANE_15M_SOURCE_DIGEST.md").write_text(
        "**Evidence as-of:** old\nbankroll 1\n", encoding="utf-8"
    )
    (docs / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md").write_text(
        "caveats stay\n", encoding="utf-8"
    )
    (tmp_path / "latest" / "journal.json").write_text(
        json.dumps({"generated_at": journal_at, "windows": []}), encoding="utf-8"
    )
    if proposed:
        name, text = proposed
        (docs / name).write_text(text, encoding="utf-8")
    if note:
        name, text = note
        (docs / name).write_text(text, encoding="utf-8")
    if decisions:
        (tmp_path / "paper" / "rule_decisions.json").write_text(
            json.dumps({"decisions": decisions}), encoding="utf-8"
        )
    return tmp_path


def test_empty_state_baseline_only_invents_no_horse(tmp_path):
    root = _tree(tmp_path)
    text = build_card(root=root)
    assert EMPTY_ON_TRIAL in text
    assert "R-BASELINE-FILL-ALL" in text
    assert "execution: true" in text
    assert "R-FIXTURE" not in text
    assert "edge" not in text.lower()
    assert "established" not in text.lower()
    assert "skill-met" not in text.lower()
    assert "WC1" not in text


def test_parked_selection_proposed_quotes_id_falsifier_and_park(tmp_path):
    extra = {
        "id": "R-FIXTURE-SKIP",
        "kind": "selection",
        "execution": False,
        "selects": True,
        "rule": "Skip when the posted mark is a coin flip.",
        "falsifier": "If n fills cannot be told from baseline, park. Do not retune.",
    }
    root = _tree(
        tmp_path,
        registry=_registry(extra=extra),
        proposed=(
            "LEARNING_LANE_15M_LAB_PROPOSED_99.md",
            "# Lab\n\nkind: selection\n\nThis proposes R-FIXTURE-SKIP.\n\n"
            "## Why we tried it\n\nThe book never selects anything.\n",
        ),
        note=(
            "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_99.md",
            "**Verdict:** **PARK** · Operator\nThe test is parked.\n",
        ),
    )
    text = build_card(root=root)
    assert "R-FIXTURE-SKIP" in text
    assert "If n fills cannot be told from baseline, park. Do not retune." in text
    assert "PARK" in text
    assert "execution: false" in text
    assert "The book never selects anything." in text


def test_burned_parked_class_is_not_on_trial(tmp_path):
    extra = {
        "id": "R-FIXTURE-SKIP",
        "kind": "selection",
        "execution": False,
        "selects": True,
        "rule": "Skip when the posted mark is a coin flip.",
        "falsifier": "Park. Do not retune.",
    }
    root = _tree(
        tmp_path,
        registry=_registry(extra=extra),
        proposed=(
            "LEARNING_LANE_15M_LAB_PROPOSED_99.md",
            "# Lab\n\nkind: selection\n\nThis proposes R-FIXTURE-SKIP.\n",
        ),
        note=(
            "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_99.md",
            "**Verdict:** **PARK** · Operator\n",
        ),
    )
    (root / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_BURNED_CLASSES.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "classes": [
                    {
                        "id": "SKIP-FIXTURE",
                        "aliases": ["R-FIXTURE-SKIP"],
                        "burned": True,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    text = build_card(root=root)
    assert EMPTY_ON_TRIAL in text
    assert "No selection rule has `execution: true`" in text


def test_execution_true_skip_count_says_book_followed(tmp_path):
    extra = {
        "id": "R-FIXTURE-SKIP",
        "kind": "selection",
        "execution": True,
        "selects": True,
        "rule": "Skip the coin-flip band.",
        "falsifier": "Park if indistinguishable.",
    }
    root = _tree(
        tmp_path,
        registry=_registry(execution_baseline=False, extra=extra),
        proposed=(
            "LEARNING_LANE_15M_LAB_PROPOSED_99.md",
            "kind: selection\nR-FIXTURE-SKIP is the trial.\n",
        ),
        note=(
            "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_99.md",
            "**Verdict:** **RUN-ONLY**\nOperator licenses paper implementation.\n",
        ),
        decisions={
            "KXBTC15M-A": {"rule_id": "R-FIXTURE-SKIP", "action": "skip"},
            "KXBTC15M-B": {"rule_id": "R-FIXTURE-SKIP", "action": "fill"},
        },
    )
    text = build_card(root=root)
    assert "Book followed R-FIXTURE-SKIP: 1 fills, 1 skips" in text
    assert "execution: true" in text


def test_card_rewrite_does_not_write_source(tmp_path):
    root = _tree(tmp_path)
    digest = root / DIGEST_REL
    before = digest.read_text(encoding="utf-8")
    write_learning_card(root=root)
    assert digest.read_text(encoding="utf-8") == before


def test_serving_card_does_not_clear_digest_figures(tmp_path):
    from golf_offshoot.learning_lane_15m.runner import serve_role

    root = _tree(tmp_path)
    set_15m_root_override(root)
    try:
        (root / "latest" / "learning_wake.json").write_text(
            json.dumps(
                {
                    "roles_owed": [
                        {"role": "learning-card"},
                        {"role": "digest-figures"},
                    ],
                    "served": [],
                }
            ),
            encoding="utf-8",
        )
        result = serve_role(
            "learning-card",
            do_work=lambda: write_learning_card(root=root),
            root=root,
        )
        assert result["marked"] is True
        state = json.loads((root / "latest" / "learning_wake.json").read_text(encoding="utf-8"))
        owed = [row["role"] for row in state.get("roles_owed") or []]
        assert "digest-figures" in owed
        assert "learning-card" not in owed
    finally:
        set_15m_root_override(None)


def test_generator_does_not_write_caveats(tmp_path):
    root = _tree(tmp_path)
    caveats = root / CAVEATS_REL
    before = caveats.read_text(encoding="utf-8")
    write_learning_card(root=root)
    assert caveats.read_text(encoding="utf-8") == before
    assert (root / "golf-offshoot/docs/LEARNING_LANE_15M_LEARNING_CARD.md").is_file()


def test_source_only_rewrite_does_not_change_the_card(tmp_path, monkeypatch):
    root = _tree(tmp_path)
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learning_card.repo_root", lambda: root
    )
    dest = write_learning_card(root=root)
    before = dest.read_text(encoding="utf-8")
    token = card_proof_token(dest)
    digest = root / DIGEST_REL
    digest.write_text("**Evidence as-of:** 99:00\nbankroll 2\nrewritten\n", encoding="utf-8")
    after = dest.read_text(encoding="utf-8")
    assert after == before
    assert card_proof_token(dest) == token


def test_fee_proposed_01_is_not_a_selection_trial_on_this_shape(tmp_path):
    """PROPOSED 01 says it is not a named horse. The card must stay empty."""
    root = _tree(
        tmp_path,
        proposed=(
            "LEARNING_LANE_15M_LAB_PROPOSED_01.md",
            "Not a new named horse.\nCharge the documented fee.\n",
        ),
    )
    text = build_card(root=root)
    assert EMPTY_ON_TRIAL in text


def test_hub_15m_shows_fixture_card_golf_does_not(tmp_path, monkeypatch):
    card = tmp_path / "card.md"
    card.write_text("FIXTURE-CARD-TEXT R-FIXTURE-SKIP PARK\n", encoding="utf-8")
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learning_card.card_path", lambda root=None: card
    )
    set_15m_root_override(tmp_path)
    try:
        page_15 = render_hub("learning_lane_15m")
        page_golf = render_hub("golf")
    finally:
        set_15m_root_override(None)
    assert 'class="learning-card"' in page_15
    assert "What is on trial" in page_15
    assert "FIXTURE-CARD-TEXT R-FIXTURE-SKIP PARK" in page_15
    assert 'class="learning-card"' not in page_golf
    assert "FIXTURE-CARD-TEXT" not in page_golf


def test_hub_15m_missing_card_is_honest(tmp_path, monkeypatch):
    missing = tmp_path / "no-such-card.md"
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learning_card.card_path",
        lambda root=None: missing,
    )
    set_15m_root_override(tmp_path)
    try:
        page = render_hub("learning_lane_15m")
    finally:
        set_15m_root_override(None)
    assert "learning card not yet available" in page


def test_trial_glance_quotes_card_and_points_to_lab(tmp_path, monkeypatch):
    card = tmp_path / "card.md"
    card.write_text(
        "# 15m learning card\n\n"
        "## On trial\n\n"
        "`R-SKIP-CIVIL-BOUNDARIES` — Skip the paper fill when close_at clock minute is 0 or 30.\n\n"
        "## Verdict\n\n"
        "not yet ruled.\n\n"
        "## Implemented?\n\n"
        "`execution: false`\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learning_card.card_path", lambda root=None: card
    )
    from golf_offshoot.operator_surface.desk import trial_glance_html

    html = trial_glance_html()
    assert 'id="trial-glance"' in html
    assert "R-SKIP-CIVIL-BOUNDARIES" in html
    assert "R-SKIP-CIVIL-BOUNDARIES`" not in html
    assert "execution: false" in html
    assert "not yet ruled" in html
    assert "Lab" in html
    assert "Not a verdict" in html
    assert "<pre>" not in html
    assert 'class="learning-card"' not in html
    assert "Skip the paper fill" not in html


def test_trial_glance_empty_on_trial(tmp_path, monkeypatch):
    card = tmp_path / "card.md"
    card.write_text(f"## On trial\n\n{EMPTY_ON_TRIAL}\n", encoding="utf-8")
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learning_card.card_path", lambda root=None: card
    )
    from golf_offshoot.operator_surface.desk import trial_glance_html

    html = trial_glance_html()
    assert EMPTY_ON_TRIAL in html
    assert "Lab" in html
    assert 'id="trial-glance"' in html


def test_trial_glance_fail_open_without_on_trial(tmp_path, monkeypatch):
    card = tmp_path / "card.md"
    card.write_text("FIXTURE-CARD-TEXT R-FIXTURE-SKIP PARK\n", encoding="utf-8")
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learning_card.card_path", lambda root=None: card
    )
    from golf_offshoot.operator_surface.desk import trial_glance_html

    html = trial_glance_html()
    assert 'id="trial-glance"' in html
    assert "FIXTURE-CARD-TEXT" in html
    assert "Lab" in html
    assert "<pre>" not in html
