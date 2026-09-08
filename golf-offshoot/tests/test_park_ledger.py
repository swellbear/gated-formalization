"""Park ledger is an honesty instrument. It must not read as progress theater."""

import json
from pathlib import Path

LEDGER = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "LEARNING_LANE_15M_PARK_LEDGER.json"
)
PARK = Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_METHOD_PARK.md"


def test_park_ledger_framing_is_not_progress_theater():
    payload = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert payload["schema"] == 1
    framing = payload["framing"].lower()
    assert "honesty" in framing
    assert "not a productivity" in framing
    assert "not progress" in framing
    assert payload["admits"] == 0
    assert payload["open"]["unreachable"] == 0
    assert payload["closed"]["unreachable"] >= 1


def test_unreachable_rows_are_named_closed_in_the_park_file():
    text = PARK.read_text(encoding="utf-8")
    assert "CLOSED / unreachable" in text
    assert "### 4. Unmeasured tape — **CLOSED / unreachable**" in text
    assert "OPEN · unreachable" not in text or "| Open · unreachable | 0 |" in text
