"""Factory English standing. Files only. No honer import. No invented pnl."""

from __future__ import annotations

import ast
from pathlib import Path

from golf_offshoot.learning_lane_15m.standing import collect_factory_standing


STANDING = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "learning_lane_15m" / "standing.py"


def test_factory_standing_does_not_import_honer():
    tree = ast.parse(STANDING.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "honer_15m" not in node.module
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "honer_15m" not in alias.name


def test_factory_standing_names_two_lineages_and_not_a_direction_model():
    standing = collect_factory_standing()
    text = " ".join(
        (
            standing.what_it_is,
            standing.where_it_stands,
            standing.last_happened,
            standing.this_book,
        )
    ).lower()
    assert "not predicting up or down" in text
    assert "lineage a" in text
    assert "lineage b" in text
    assert "never added" in text
    assert "not scored" in text
    assert "keep" in standing.where_it_stands.lower() or "not a keep" in text
