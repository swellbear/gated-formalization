"""Part 3: the honesty gate is derived from files, not from typed prose."""

from __future__ import annotations

from golf_offshoot.learning_lane_15m import honesty
from golf_offshoot.learning_lane_15m.learn import honesty_gate_from_desk

CLEAN_SCAN = {
    "ledger": {"bankroll": 91.8},
    "published_only": [{"ticker": "KXBTC15M-26SEP041500-00"}],
    "paper_join_missing": [{"ticker": honesty.MISSING_JOIN_TICKER}],
    "pending": [],
}


def _desk(tmp_path, rows, *, hub_ok=True):
    path = tmp_path / "DESK.md"
    body = ["# Desk", "", "## Honesty checklist 2026-09-08 11:00", "", "| Box | State |", "|---|---|"]
    body.extend(rows)
    body.extend(["", "## Thread", "", "nothing"])
    path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return path


def _all_pass_rows():
    return [
        "| Lineage story readable, dual lineage labeled not merged | **PASS** fine |",
        f"| {honesty.MISSING_JOIN_TICKER} honestly joined or pending | **PASS** fine |",
        "| One hub process | **PASS** fine |",
        "| No invented charts or pnl | **PASS** digest sha256 "
        "abcdef0123456789abcdef0123456789 at 2026-09-08 11:00 |",
    ]


# ------------------------------------------------------------ derived boxes


def test_the_derived_boxes_come_off_the_scan():
    boxes = honesty.derive_boxes(CLEAN_SCAN, hub={"ok": True, "note": "one tree"})

    assert boxes[honesty.BOX_LINEAGE]["ok"] is True
    assert boxes[honesty.BOX_MISSING_JOIN]["ok"] is True
    assert boxes[honesty.BOX_HUB_TREE]["ok"] is True


def test_a_combined_bankroll_shuts_the_lineage_box():
    scan = {**CLEAN_SCAN, "ledger": {"bankroll": 91.8, "combined_bankroll": 191.8}}

    boxes = honesty.derive_boxes(scan, hub={"ok": True, "note": ""})

    assert boxes[honesty.BOX_LINEAGE]["ok"] is False


def test_a_missing_join_reported_pending_shuts_its_box():
    scan = {**CLEAN_SCAN, "pending": [{"ticker": honesty.MISSING_JOIN_TICKER}]}

    boxes = honesty.derive_boxes(scan, hub={"ok": True, "note": ""})

    assert boxes[honesty.BOX_MISSING_JOIN]["ok"] is False


def test_a_missing_join_carrying_a_pnl_shuts_its_box():
    scan = {
        **CLEAN_SCAN,
        "paper_join_missing": [{"ticker": honesty.MISSING_JOIN_TICKER, "paper_pnl": 1.02}],
    }

    boxes = honesty.derive_boxes(scan, hub={"ok": True, "note": ""})

    assert boxes[honesty.BOX_MISSING_JOIN]["ok"] is False


def test_two_hub_trees_shut_the_hub_box_and_one_tree_does_not():
    # The criterion is one tree, not one OS process: a supervisor plus its
    # child is one hub.
    assert honesty.derive_boxes(CLEAN_SCAN, hub={"ok": True, "note": "supervisor + child"})[
        honesty.BOX_HUB_TREE
    ]["ok"]
    assert not honesty.derive_boxes(CLEAN_SCAN, hub={"ok": False, "note": "2 trees"})[
        honesty.BOX_HUB_TREE
    ]["ok"]


# --------------------------------------------------- the derived verdict wins


def test_typed_prose_cannot_open_a_derived_box(tmp_path, monkeypatch):
    monkeypatch.setattr(honesty, "hub_trees", lambda: {"ok": True, "note": "one tree"})
    scan = {**CLEAN_SCAN, "pending": [{"ticker": honesty.MISSING_JOIN_TICKER}]}

    gate = honesty_gate_from_desk(_desk(tmp_path, _all_pass_rows()), scan=scan)

    assert gate["passed"] is False
    row = next(b for b in gate["boxes"] if honesty.MISSING_JOIN_TICKER in b["box"])
    assert row["typed"] == "PASS"
    assert row["state"] == "FAIL"
    assert row["source"] == "derived"


def test_typed_prose_can_still_shut_a_derived_box(tmp_path, monkeypatch):
    monkeypatch.setattr(honesty, "hub_trees", lambda: {"ok": True, "note": "one tree"})
    rows = _all_pass_rows()
    rows[0] = "| Lineage story readable | **FAIL** I do not believe it |"

    gate = honesty_gate_from_desk(_desk(tmp_path, rows), scan=CLEAN_SCAN)

    assert gate["passed"] is False


def test_deleting_a_derived_row_does_not_open_the_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(honesty, "hub_trees", lambda: {"ok": False, "note": "2 trees"})
    rows = [r for r in _all_pass_rows() if "hub process" not in r.lower()]

    gate = honesty_gate_from_desk(_desk(tmp_path, rows), scan=CLEAN_SCAN)

    assert gate["passed"] is False
    assert any("hub_tree (not on the desk)" == b["box"] for b in gate["boxes"])


# -------------------------------------------- judgment boxes need evidence


def test_a_judgment_box_with_no_evidence_does_not_open_the_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(honesty, "hub_trees", lambda: {"ok": True, "note": "one tree"})
    rows = _all_pass_rows()
    rows[3] = "| No invented charts or pnl | **PASS** everything looks honest |"

    gate = honesty_gate_from_desk(_desk(tmp_path, rows), scan=CLEAN_SCAN)

    assert gate["passed"] is False
    row = next(b for b in gate["boxes"] if "invented" in b["box"].lower())
    assert row["source"] == "judgment"
    assert row["has_evidence"] is False
    assert "no evidence" in row["note"]


def test_a_fully_evidenced_all_pass_desk_opens_the_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(honesty, "hub_trees", lambda: {"ok": True, "note": "one tree"})

    gate = honesty_gate_from_desk(_desk(tmp_path, _all_pass_rows()), scan=CLEAN_SCAN)

    assert gate["passed"] is True
    assert all(b["state"] == "PASS" for b in gate["boxes"])


def test_evidence_is_a_pid_a_hash_or_a_timestamp_not_an_adjective():
    assert honesty.has_evidence("PID 11532 holds the listener")
    assert honesty.has_evidence("sha256 abcdef0123456789abcdef0123456789")
    assert honesty.has_evidence("verified 2026-09-08 11:00")
    assert not honesty.has_evidence("**PASS** carefully checked and clean")


def test_a_missing_desk_is_still_not_a_pass(tmp_path, monkeypatch):
    monkeypatch.setattr(honesty, "hub_trees", lambda: {"ok": True, "note": "one tree"})

    gate = honesty_gate_from_desk(tmp_path / "nope.md", scan=CLEAN_SCAN)

    assert gate["passed"] is False
    assert gate["stamp_found"] is False
