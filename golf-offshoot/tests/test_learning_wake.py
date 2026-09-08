"""The learning wake: evidence in, owed roles out, and nothing claimed on a role's behalf."""

import json
from datetime import datetime, timezone

import pytest

from golf_offshoot.data_feeds.kalshi_15m import parse_event, parse_market
from golf_offshoot.learning_lane_15m import learn
from golf_offshoot.learning_lane_15m.learn import (
    EVENT_BOARD_STALE,
    EVENT_NEW_FILL,
    EVENT_NEW_SETTLE,
    EVENT_PENDING_CLEARED,
    HEARTBEAT_NOTE,
    ILLUSTRATOR_ROLE,
    LAB_ROLE,
    ROLE_ORDER,
    STATE_OFFICIAL_NO_BOOK,
    format_wake_line,
    format_wake_tick,
    learning_status_block,
    load_wake_state,
    mark_roles_served,
    record_learning_tick,
    scan_learning_evidence,
    wake_state_path,
)
from golf_offshoot.learning_lane_15m.loop import settle_join
from golf_offshoot.learning_lane_15m.paper import iter_books, paper_autobet_open_markets
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, set_15m_root_override

EVENT_RAW = {
    "event_ticker": "KXBTC15M-26SEP071545",
    "series_ticker": "KXBTC15M",
    "title": "BTC 15 min",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

MARKET_RAW = {
    "ticker": "KXBTC15M-26SEP071545-45",
    "event_ticker": "KXBTC15M-26SEP071545",
    "status": "finalized",
    "result": "yes",
    "yes_ask_dollars": "0.6100",
    "title": "BTC price up in next 15 mins?",
}

# The window the published lineage names a paper fill on. Its book is not on this tree.
ORPHAN_TICKER = "KXBTC15M-26SEP071500-00"
# The window the published lineage already settled paper_win. Also not on this tree.
PUBLISHED_TICKER = "KXBTC15M-26SEP071445-45"
# A window Kalshi has not spoken on yet, so the tree carries a genuine pending too.
STILL_OPEN_TICKER = "KXBTC15M-26SEP071900-00"

PUBLISHED_LANE = {
    "lane_id": "learning_lane_15m",
    "label": "15-minute Kalshi — learning lane",
    "tab_label": "15-min Kalshi · Learning",
    "lane_badge": "LEARNING LANE",
    "badges": ["LEARNING LANE", "NOT ARMED", "PAPER OBSERVATION ONLY", "AI: NO CASH IN/OUT"],
    "summary_line": "KXBTC15M learning lane. Paper observation only.",
    "source_kind": "paper observation journal (not a Kalshi cash account)",
    "lane_scope_note": "Everything in this tab is this lane.",
    "last_run": {
        "status": "published export",
        "headline": (
            f"First fill {PUBLISHED_TICKER} settled paper_win. "
            f"Live {ORPHAN_TICKER} is SETTLE_PENDING. Observation only."
        ),
        "fields": [
            {"label": "Settled paper fill", "value": PUBLISHED_TICKER},
            {"label": "Paper outcome", "value": "paper_win"},
            {"label": "Kalshi result", "value": "yes"},
            {"label": "paper settle_win pnl", "value": "+1.67"},
            {"label": "Live paper fill", "value": ORPHAN_TICKER},
            {"label": "Live paper fill status", "value": "SETTLE_PENDING"},
        ],
        "notes": [
            "Official settle is Kalshi result.",
            f"Live {ORPHAN_TICKER} stays SETTLE_PENDING. Do not invent that window's win/lose.",
        ],
    },
    "settle": {
        "banner": "SETTLE_PENDING",
        "banner_state": "pending",
        "headline": (
            "First fill settled paper_win. "
            f"Live window {ORPHAN_TICKER} is still SETTLE_PENDING until Kalshi result."
        ),
        "counts": [
            {"label": "Pending windows", "value": "1"},
            {"label": "Settled windows", "value": "1"},
            {"label": "paper_win", "value": "1"},
            {"label": "paper settle_win pnl", "value": "+1.67"},
            {"label": "paper observation after settle", "value": "101.67"},
        ],
        "sources": [],
        "residual": [
            {
                "label": ORPHAN_TICKER,
                "value": "SETTLE_PENDING",
                "note": "SETTLE_PENDING until Kalshi result on this window.",
            }
        ],
        "observation": None,
        "notes": [],
    },
    "paper_ledger": {
        "status": "counts only — no cash figures published",
        "headline": "Paper ticket counts.",
        "rows": [
            {"label": "paper_win", "value": "1"},
            {"label": "paper settle_win pnl", "value": "+1.67"},
        ],
        "absent_fields": [],
        "notes": [],
    },
    "records": [],
    "records_note": "No weekly operating record exists for this lane.",
    "charts": [],
    "charts_note": "No charts.",
}

DESK_FAILING = """# Agent desk

## Honesty checklist (CoS stamp — gate for Lab)

| Box | State |
|-----|-------|
| Lineage story readable | **PASS** — dual lineage drawn apart |
| `KXBTC15M-26SEP071500-00` honestly joined or pending with a true reason | **FAIL** — wording is stale |

## Thread

- a line
"""

DESK_PASSING = DESK_FAILING.replace("**FAIL** — wording is stale", "**PASS** — named honestly")


def _write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2) if not isinstance(payload, str) else payload,
        encoding="utf-8",
    )


def _write_desk(repo, text):
    _write(repo / "docs" / "agents" / "DESK.md", text)


def _write_manifest(repo, lane):
    _write(
        repo / "docs" / "observability-hub" / "data" / "manifest.json",
        {"schema_version": 1, "lanes": [{"lane_id": "golf"}, lane]},
    )


def _write_journal(windows):
    _write(latest_dir_15m() / "journal.json", {"lane": "learning_lane_15m", "windows": windows})


def _write_png(repo, *, mtime: float | None = None):
    """A board file the wake can age against. Contents are not read.

    Default mtime is far in the future so a 'current' fixture PNG is never
    behind the 26SEP07 fixture tickers, regardless of when the test runs.
    """
    import os

    dest = (
        repo
        / "docs"
        / "observability-hub"
        / "data"
        / "charts"
        / "learning_lane_15m"
        / "paper_window_strip.png"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b"png")
    when = mtime if mtime is not None else datetime(2099, 1, 1, tzinfo=timezone.utc).timestamp()
    os.utime(dest, (when, when))
    return dest


def _journal_row(ticker, result, status="finalized"):
    return {
        "ticker": ticker,
        "event_ticker": ticker.rsplit("-", 1)[0],
        "window_id": ticker.rsplit("-", 1)[0],
        "status": status,
        "result": result,
    }


@pytest.fixture()
def lane(tmp_path, monkeypatch):
    """A synthetic 15m tree, a published manifest, and a stamped desk — all on disk."""
    monkeypatch.setattr(
        "golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf"
    )
    set_15m_root_override(tmp_path / "kalshi_15m")
    repo = tmp_path / "repo"
    monkeypatch.setattr(learn, "repo_root", lambda: repo)
    _write_manifest(repo, PUBLISHED_LANE)
    _write_desk(repo, DESK_FAILING)
    _write_journal([_journal_row(ORPHAN_TICKER, "yes"), _journal_row(PUBLISHED_TICKER, "yes")])
    _write_png(repo)
    try:
        yield repo
    finally:
        set_15m_root_override(None)


def _open_a_paper_book():
    """One real paper fill on an open window, plus its SETTLE_PENDING join file."""
    event = parse_event(EVENT_RAW)
    market = parse_market({**MARKET_RAW, "status": "active", "result": ""}, event=event)
    paper_autobet_open_markets([market])
    settle_join([market], [event])
    return event, market


def _open_a_book_kalshi_has_not_spoken_on():
    """A second window that stays active, so a genuine SETTLE_PENDING is on the tree."""
    event = parse_event({**EVENT_RAW, "event_ticker": STILL_OPEN_TICKER.rsplit("-", 1)[0]})
    market = parse_market(
        {
            **MARKET_RAW,
            "ticker": STILL_OPEN_TICKER,
            "event_ticker": STILL_OPEN_TICKER.rsplit("-", 1)[0],
            "status": "active",
            "result": "",
        },
        event=event,
    )
    paper_autobet_open_markets([market])
    settle_join([market], [event])
    return event


def _kalshi_speaks_on_the_open_window(event):
    """The official result lands on that second window, after the wake already scanned."""
    official = parse_market(
        {
            **MARKET_RAW,
            "ticker": STILL_OPEN_TICKER,
            "event_ticker": STILL_OPEN_TICKER.rsplit("-", 1)[0],
        },
        event=event,
    )
    settle_join([official], [event])
    return official


def _settle_that_book(event):
    official = parse_market(MARKET_RAW, event=event)
    settle_join([official], [event])
    return official


def _events_of(state, kind):
    return [e for e in state["new_events"] if e["kind"] == kind]


def test_first_scan_seeds_without_false_events(lane):
    _open_a_paper_book()

    state = record_learning_tick()

    assert state["seeded_this_tick"] is True
    assert state["new_events"] == []
    assert state["roles_owed"] == []
    assert state["heartbeat"]["note"] == HEARTBEAT_NOTE
    # Gitignored lane state, never a book and never the golf tree.
    assert wake_state_path().parent == latest_dir_15m()
    assert wake_state_path().is_file()


def test_new_settle_raises_the_event_with_protocol_roles(lane):
    event, _ = _open_a_paper_book()
    record_learning_tick()

    _settle_that_book(event)
    state = record_learning_tick()

    settles = _events_of(state, EVENT_NEW_SETTLE)
    assert [e["ticker"] for e in settles] == [MARKET_RAW["ticker"]]
    assert settles[0]["detail"].startswith("official Kalshi result=yes")
    assert settles[0]["roles_owed"] == list(ROLE_ORDER)
    assert LAB_ROLE not in settles[0]["roles_owed"]
    assert [row["role"] for row in state["roles_owed"]] == list(ROLE_ORDER)
    assert all(row["served_at"] is None for row in state["roles_owed"])
    # The settle also takes the window off the pending list, which is its own event.
    assert _events_of(state, EVENT_PENDING_CLEARED)


def test_new_fill_raises_new_fill(lane):
    record_learning_tick()

    _open_a_paper_book()
    state = record_learning_tick()

    fills = _events_of(state, EVENT_NEW_FILL)
    assert len(fills) == 1
    assert fills[0]["roles_owed"] == list(ROLE_ORDER)


def test_no_change_yields_a_heartbeat(lane):
    _open_a_paper_book()
    record_learning_tick()

    state = record_learning_tick()

    assert state["new_events"] == []
    heartbeat = state["heartbeat"]
    assert heartbeat["note"] == HEARTBEAT_NOTE
    assert heartbeat["at"]
    assert heartbeat["pending"] == len(state["scan"]["pending"])
    assert "watch_cycles" in heartbeat
    assert "heartbeat" in format_wake_tick(state)


def test_roles_owed_never_auto_clears_and_keeps_ageing(lane):
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)
    first = record_learning_tick()
    owed_since = {row["role"]: row["owed_since"] for row in first["roles_owed"]}

    quiet = record_learning_tick()
    later = record_learning_tick()

    assert quiet["new_events"] == []
    assert [row["role"] for row in later["roles_owed"]] == list(ROLE_ORDER)
    # An unserved wake keeps its original clock so it ages instead of resetting.
    assert {row["role"]: row["owed_since"] for row in later["roles_owed"]} == owed_since
    assert all(row["age_s"] >= 0 for row in later["roles_owed"])
    assert all(row["age_text"] for row in later["roles_owed"])


def test_only_an_explicit_call_marks_a_role_served(lane):
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)
    record_learning_tick()

    served = mark_roles_served(["digestor"], by="digestor", note="posted the honesty digest")

    assert [row["role"] for row in served["roles_owed"]] == ["operator", "systems", "validator"]
    assert served["served"][0]["role"] == "digestor"
    assert served["served"][0]["served_at"]
    assert served["served"][0]["served_by"] == "digestor"
    # A later tick does not resurrect a served role and does not clear the rest.
    after = record_learning_tick()
    assert [row["role"] for row in after["roles_owed"]] == ["operator", "systems", "validator"]


def test_official_result_without_a_paper_book_is_not_pending_and_carries_no_pnl(lane):
    _open_a_paper_book()

    scan = scan_learning_evidence()

    missing = {row["ticker"]: row for row in scan["paper_join_missing"]}
    assert ORPHAN_TICKER in missing
    orphan = missing[ORPHAN_TICKER]
    assert orphan["official_result"] == "yes"
    assert orphan["paper_book_on_tree"] is False
    assert orphan["state"] == STATE_OFFICIAL_NO_BOOK
    assert orphan["paper_pnl"] is None
    assert "not a pending window" in orphan["reason"]
    # Not collapsed into pending, and not quietly dropped either.
    assert ORPHAN_TICKER not in {row["ticker"] for row in scan["pending"]}
    assert ORPHAN_TICKER in scan["settled"]


def test_published_paper_history_is_kept_not_recomputed(lane):
    _open_a_paper_book()

    scan = scan_learning_evidence()

    kept = {row["ticker"]: row for row in scan["published_only"]}
    assert PUBLISHED_TICKER in kept
    assert kept[PUBLISHED_TICKER]["paper_outcome"] == "paper_win"
    # Quoted from the published manifest, never derived here.
    assert kept[PUBLISHED_TICKER]["published_paper_pnl"] == "+1.67"
    assert kept[PUBLISHED_TICKER]["paper_book_on_tree"] is False
    assert PUBLISHED_TICKER not in {row["ticker"] for row in scan["paper_join_missing"]}


def test_no_pnl_is_invented(lane):
    event, _ = _open_a_paper_book()
    pending_scan = scan_learning_evidence()
    window = next(iter(pending_scan["fills"]))
    assert pending_scan["fills"][window]["paper_pnl"] is None

    _settle_that_book(event)
    settled_scan = scan_learning_evidence()

    book = iter_books()[0]
    assert settled_scan["fills"][window]["paper_pnl"] == f"{float(book.settlement_pnl):+.2f}"
    # A window with no book on this tree never grows a pnl, not even a zero.
    for row in settled_scan["paper_join_missing"]:
        assert row["paper_pnl"] is None
        assert "0.00" not in json.dumps(row)


def test_lab_is_not_owed_while_the_desk_carries_a_fail(lane):
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)

    state = record_learning_tick()

    gate = state["lab_gate"]
    assert gate["lab_owed"] is False
    assert gate["honesty_gate_passed"] is False
    assert "honesty gate has not passed" in gate["why"]
    assert all(LAB_ROLE not in e["roles_owed"] for e in state["new_events"])


def test_lab_stays_off_on_a_passing_desk_without_an_operator_residual(lane):
    _write_desk(lane, DESK_PASSING)
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)

    state = record_learning_tick()

    assert state["lab_gate"]["honesty_gate_passed"] is True
    assert state["lab_gate"]["lab_owed"] is False
    assert "Operator residual" in state["lab_gate"]["why"]
    assert all(LAB_ROLE not in e["roles_owed"] for e in state["new_events"])


def test_lab_is_owed_only_with_a_passing_gate_and_an_operator_residual(lane):
    _write_desk(lane, DESK_PASSING)
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)

    state = record_learning_tick(operator_residual_posted=True)

    assert state["lab_gate"]["lab_owed"] is True
    settles = _events_of(state, EVENT_NEW_SETTLE)
    assert settles[0]["roles_owed"] == list(ROLE_ORDER) + [LAB_ROLE]


def test_a_missing_desk_stamp_is_not_a_pass(lane):
    (lane / "docs" / "agents" / "DESK.md").unlink()

    gate = learn.honesty_gate_from_desk()

    assert gate["stamp_found"] is False
    assert gate["passed"] is False


def test_watch_cycle_records_a_wake_and_never_serves_a_role(lane, monkeypatch):
    from golf_offshoot.learning_lane_15m.watch import PaperWatch

    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)
    record_learning_tick()
    owed_before = [row["role"] for row in load_wake_state()["roles_owed"]]
    assert owed_before == list(ROLE_ORDER)

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.loop.run_loop",
        lambda *, refresh=True, feed=None: {
            "paper_autobet": {"fills": 0},
            "settle_join": {"settled": 1, "pending": 0},
        },
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.loop.format_loop_report", lambda payload: "report"
    )
    seen = {}
    watch = PaperWatch(interval_s=999, on_cycle=lambda payload: seen.update(payload))
    watch._cycle()

    assert seen["learning_wake"]["updated_at"]
    assert watch.last_wake_error == ""
    assert seen["learning_runner"]["mode"] == "dry-run"
    assert seen["learning_runner"]["served"] == []
    # The loop names owed roles. It never marks one served.
    assert [row["role"] for row in load_wake_state()["roles_owed"]] == owed_before


def test_wake_lines_reach_the_hub_journal_and_the_tick(lane):
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)
    state = record_learning_tick()

    line = format_wake_line(state)
    tick = format_wake_tick(state)

    assert "learning wake" in line
    assert "digestor" in line
    assert ORPHAN_TICKER in line
    assert "none is invented" in line
    assert "roles owed" in tick
    assert "not a pending window" in tick
    assert "+1.67" in tick
    assert "mark_roles_served" in tick


def test_manifest_carries_wake_status_and_keeps_published_paper_win(lane, monkeypatch):
    from golf_offshoot.operator_surface import observability

    monkeypatch.setattr(observability, "repo_root", lambda: lane)
    event, _ = _open_a_paper_book()
    record_learning_tick()
    _settle_that_book(event)
    record_learning_tick()

    payload = observability.build_hub_manifest(
        existing={"lanes": [{"lane_id": "golf"}, PUBLISHED_LANE]}
    )

    lane15 = payload["lanes"][1]
    status = lane15["learning_status"]
    assert status["status"] == "crew work owed"
    assert [row["label"] for row in status["roles_owed"]] == list(ROLE_ORDER)
    assert all(isinstance(row["value"], str) for row in status["rows"])

    fields = {row["label"]: row["value"] for row in lane15["last_run"]["fields"]}
    counts = {row["label"]: row["value"] for row in lane15["settle"]["counts"]}
    assert fields["Learning wake"] == "crew work owed"
    assert "digestor" in fields["Crew roles owed"]
    # Published lineage is not dropped and pending is not invented.
    assert fields["Settled paper fill"] == PUBLISHED_TICKER
    assert fields["paper settle_win pnl"] == "+1.67"
    assert counts["Lineage B · paper settle_win pnl"] == "+1.67"
    # The published win is still counted; a new local settle may add to it, never replace it.
    assert int(counts["Lineage B · paper_win"]) >= 1
    assert counts["Official result, paper book not on this tree"] == "1"
    assert counts["Published paper history kept"] == "1"
    assert "bankroll" not in json.dumps(lane15).lower()


def _export_lane(lane, monkeypatch, existing=None):
    from golf_offshoot.operator_surface import observability

    monkeypatch.setattr(observability, "repo_root", lambda: lane)
    return observability.build_hub_manifest(
        existing=existing or {"lanes": [{"lane_id": "golf"}, PUBLISHED_LANE]}
    )


def test_manifest_rewords_the_missing_paper_join_off_pending(lane, monkeypatch):
    """Kalshi spoke on that window, so SETTLE_PENDING is the wrong banner for it."""
    event, _ = _open_a_paper_book()
    _settle_that_book(event)
    _open_a_book_kalshi_has_not_spoken_on()
    record_learning_tick()

    lane15 = _export_lane(lane, monkeypatch)["lanes"][1]

    residual = {row["label"]: row for row in lane15["settle"]["residual"]}
    orphan = residual[ORPHAN_TICKER]
    assert "PENDING" not in orphan["value"].upper()
    assert "missing paper join" in orphan["value"]
    assert "not a pending window" in orphan["note"]
    assert "none is invented" in orphan["note"]
    # A window Kalshi has not spoken on is still honestly pending.
    assert residual[STILL_OPEN_TICKER]["value"] == "SETTLE_PENDING"

    for headline in (lane15["settle"]["headline"], lane15["last_run"]["headline"]):
        assert "SETTLE_PENDING until Kalshi result" not in headline
        assert "missing paper join" in headline
    notes = " ".join(lane15["last_run"]["notes"])
    assert f"{ORPHAN_TICKER} — Kalshi settled this window yes" in notes
    assert "stays SETTLE_PENDING" not in notes

    fields = {row["label"]: row for row in lane15["last_run"]["fields"]}
    assert fields["Live paper fill status"]["value"] == learn.MISSING_JOIN_BANNER

    # The window is off the pending count without ever gaining a pnl.
    counts = {row["label"]: row["value"] for row in lane15["settle"]["counts"]}
    assert counts["Pending windows"] == "1"
    assert lane15["learning_status"]["missing_paper_joins"][0]["paper_pnl"] == learn.NO_PAPER_PNL
    assert "+1.67" in json.dumps(lane15)


def test_the_reworded_manifest_survives_the_next_export(lane, monkeypatch):
    """A hand edit dies on the next export, so the writer restates it every time."""
    event, _ = _open_a_paper_book()
    _settle_that_book(event)
    _open_a_book_kalshi_has_not_spoken_on()
    record_learning_tick()

    first = _export_lane(lane, monkeypatch)
    second = _export_lane(lane, monkeypatch, existing=first)

    before, after = first["lanes"][1], second["lanes"][1]
    for block, key in (("settle", "headline"), ("last_run", "headline")):
        assert after[block][key] == before[block][key]
        assert "SETTLE_PENDING until Kalshi result" not in after[block][key]
    orphan = next(r for r in after["settle"]["residual"] if r["label"] == ORPHAN_TICKER)
    assert "PENDING" not in orphan["value"].upper()
    assert after["last_run"]["notes"] == before["last_run"]["notes"]
    assert f"{ORPHAN_TICKER} — Kalshi settled this window yes" in " ".join(
        after["last_run"]["notes"]
    )
    # Lineage B history rides through both exports untouched.
    counts = {row["label"]: row["value"] for row in after["settle"]["counts"]}
    assert counts["Lineage B · paper settle_win pnl"] == "+1.67"


def test_a_window_that_settled_after_the_wake_is_never_published_as_pending(
    lane, monkeypatch
):
    """The 19:00:48 race: wake cached X as pending, X settled ~115ms before the export.

    The wake file is written on the watch cycle; the export runs on its own clock. A
    window that gains its official Kalshi result in between must not ship as pending.
    """
    event, _ = _open_a_paper_book()
    _settle_that_book(event)
    open_event = _open_a_book_kalshi_has_not_spoken_on()
    # Wake scans while Kalshi has not spoken, so the cache names the window pending.
    cached = record_learning_tick()
    assert [row["label"] for row in learning_status_block(cached)["pending_windows"]] == [
        STILL_OPEN_TICKER
    ]

    # Kalshi speaks. The settle file on disk now says settled / result=yes, and no
    # second wake tick runs before the export — exactly the race Validator caught.
    _kalshi_speaks_on_the_open_window(open_event)
    lane15 = _export_lane(lane, monkeypatch)["lanes"][1]

    published_pending = [
        row["label"] for row in lane15["learning_status"]["pending_windows"]
    ]
    assert STILL_OPEN_TICKER not in published_pending
    assert published_pending == []
    residual = {row["label"]: row for row in lane15["settle"]["residual"]}
    assert residual[STILL_OPEN_TICKER]["value"] == "settled"
    assert "result=yes" in residual[STILL_OPEN_TICKER]["note"]

    # Ticker and count come off the same list, so they cannot disagree.
    counts = {row["label"]: row["value"] for row in lane15["settle"]["counts"]}
    assert counts["Pending windows"] == "0"
    assert f"{STILL_OPEN_TICKER} is SETTLE_PENDING" not in lane15["settle"]["headline"]
    assert "for want of a Kalshi result" not in lane15["settle"]["headline"]

    # Leaving the pending list never hands the window a pnl.
    blob = json.dumps(lane15)
    assert "won" not in residual[STILL_OPEN_TICKER]
    assert "pnl" not in residual[STILL_OPEN_TICKER]
    assert "+1.67" in blob  # lineage B history still untouched by any of this


def test_export_refuses_to_publish_a_settled_window_as_pending(lane, monkeypatch):
    """The invariant is enforced, not just arranged for."""
    from golf_offshoot.operator_surface import observability

    event, _ = _open_a_paper_book()
    _settle_that_book(event)
    record_learning_tick()

    monkeypatch.setattr(
        observability,
        "_reconcile_pending",
        lambda residual, wake_pending, live: [
            {"label": MARKET_RAW["ticker"], "value": "SETTLE_PENDING", "note": "", "kind": ""}
        ],
    )
    with pytest.raises(RuntimeError, match="settled window as pending"):
        _export_lane(lane, monkeypatch)


def test_paper_blocks_say_which_lineage_they_count(lane, monkeypatch):
    """So a later bot cannot 'fix' the published book against the local one."""
    event, _ = _open_a_paper_book()
    _settle_that_book(event)
    record_learning_tick()

    lane15 = _export_lane(lane, monkeypatch)["lanes"][1]

    ledger = lane15["paper_ledger"]
    labels = [row["label"] for row in ledger["rows"]]
    assert "Lineage B" in ledger["headline"]
    assert "paper settle_win pnl" in labels
    assert any(label.startswith("Lineage A") for label in labels)
    assert any("never added together" in note for note in ledger["notes"])

    status = lane15["learning_status"]
    assert status["lineage"].startswith("lineage A")
    assert status["published_history"][0]["lineage"].startswith("lineage B")
    assert status["published_history"][0]["published_paper_pnl"] == "+1.67"

    # settle.counts mixes both books, so every published row names the one it counts.
    counts = {row["label"]: row for row in lane15["settle"]["counts"]}
    for label in ("paper_win", "paper settle_win pnl", "paper observation after settle"):
        assert f"Lineage B · {label}" in counts
        assert label not in counts
    assert "not a denominator" in counts["Settled windows"]["note"]


def test_learning_status_is_honest_when_no_wake_has_been_recorded(lane):
    block = learning_status_block()

    assert block["status"] == "not yet available"
    assert block["rows"] == []
    assert block["roles_owed"] == []
    assert "not been recorded" in block["headline"]


def test_illustrator_is_owed_when_png_lags_more_than_one_window(lane):
    _write_png(lane, mtime=1.0)

    state = record_learning_tick()

    stale = _events_of(state, EVENT_BOARD_STALE)
    assert stale
    assert stale[0]["roles_owed"] == [ILLUSTRATOR_ROLE]
    assert [row["role"] for row in state["roles_owed"]] == [ILLUSTRATOR_ROLE]
    assert state["board"]["stale"] is True
    assert state["board"]["lag_windows"] > 1


def test_one_window_of_trail_does_not_owe_illustrator(lane):
    # Between the 14:45 and 15:00 ET closes (EDT = UTC-4).
    mid = datetime(2026, 9, 7, 18, 50, tzinfo=timezone.utc).timestamp()
    _write_png(lane, mtime=mid)

    state = record_learning_tick()

    assert not _events_of(state, EVENT_BOARD_STALE)
    assert ILLUSTRATOR_ROLE not in [row["role"] for row in state["roles_owed"]]
    assert state["board"]["stale"] is False
    assert state["board"]["lag_windows"] <= 1


def test_missing_png_with_two_windows_owes_illustrator(lane):
    png = (
        lane
        / "docs"
        / "observability-hub"
        / "data"
        / "charts"
        / "learning_lane_15m"
        / "paper_window_strip.png"
    )
    png.unlink()

    state = record_learning_tick()

    assert _events_of(state, EVENT_BOARD_STALE)
    assert ILLUSTRATOR_ROLE in [row["role"] for row in state["roles_owed"]]
    assert state["board"]["png_exists"] is False


def test_serving_illustrator_without_a_new_png_re_owes_on_the_next_tick(lane):
    _write_png(lane, mtime=1.0)
    record_learning_tick()
    mark_roles_served([ILLUSTRATOR_ROLE])

    later = record_learning_tick()

    assert _events_of(later, EVENT_BOARD_STALE)
    assert ILLUSTRATOR_ROLE in [row["role"] for row in later["roles_owed"]]


def test_fresh_png_clears_the_lag_and_does_not_re_owe(lane):
    _write_png(lane, mtime=1.0)
    record_learning_tick()
    mark_roles_served([ILLUSTRATOR_ROLE])
    _write_png(lane)

    later = record_learning_tick()

    assert not _events_of(later, EVENT_BOARD_STALE)
    assert ILLUSTRATOR_ROLE not in [row["role"] for row in later["roles_owed"]]
    assert later["board"]["stale"] is False
