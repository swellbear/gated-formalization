"""The 15m board must stay a render of files on disk.

These cover the honesty rules the board exists for: a window with no Kalshi result on disk
stays SETTLE_PENDING, a window with no paper pnl on disk says so instead of showing 0, and the
two paper lineages over this series keep separate books.
"""

import json

import pytest

from golf_offshoot.learning_lane_15m import illustrate
from golf_offshoot.learning_lane_15m.illustrate import (
    LINEAGE_LOCAL,
    LINEAGE_PUBLISHED,
    LINEAGE_TAPE,
    REL_PNG,
    chart_png_path,
    collect_board,
    collect_rows,
    render_paper_window_strip,
)
from golf_offshoot.learning_lane_15m.paths import (
    latest_dir_15m,
    paper_dir_15m,
    set_15m_root_override,
    settlements_dir_15m,
)

SETTLED = "KXBTC15M-26SEP071700-00"
OPEN = "KXBTC15M-26SEP071715-15"
PUBLISHED_WIN = "KXBTC15M-26SEP071445-45"
PUBLISHED_PENDING = "KXBTC15M-26SEP071500-00"
TAPE = "KXBTC15M-26SEP071345-45"


def _window_id(stem: str, open_z: str, close_z: str) -> str:
    return f"{stem}__2026-09-07T{open_z}:00Z__2026-09-07T{close_z}:00Z"


def _paper_book(window_id: str, ticker: str, *, mark: float, pnl: float | None, winner: str) -> dict:
    """A window's own paper book. A settled book clears positions and keeps the movement."""
    return {
        "tournament_id": window_id,
        "settled_at": "2026-09-07T17:00:56-04:00" if pnl is not None else None,
        "settlement_pnl": pnl,
        "settlement_winner": winner,
        "book": {
            "positions": []
            if pnl is not None
            else [{"position_id": "paper-1", "player_id": ticker, "player_name": f"YES {ticker}", "fill_price": mark}],
        },
        "movements": [
            {
                "kind": "new_bet",
                "player_id": ticker,
                "player_name": f"YES {ticker}",
                "reason_technical": f"lane=learning_lane_15m ticker={ticker} paper_mark={mark} paper_autobet observation",
            }
        ],
    }


@pytest.fixture()
def lane(tmp_path, monkeypatch):
    """A synthetic 15m tree plus a synthetic published manifest, both on disk."""
    set_15m_root_override(tmp_path / "kalshi_15m")
    repo = tmp_path / "repo"
    monkeypatch.setattr(illustrate, "repo_root", lambda: repo)

    settled_id = _window_id("KXBTC15M-26SEP071700", "20:45", "21:00")
    open_id = _window_id("KXBTC15M-26SEP071715", "21:00", "21:15")

    (paper_dir_15m() / "settled.json").write_text(
        json.dumps(_paper_book(settled_id, SETTLED, mark=0.385, pnl=1.6, winner="kalshi:yes")), encoding="utf-8"
    )
    (paper_dir_15m() / "open.json").write_text(
        json.dumps(_paper_book(open_id, OPEN, mark=0.645, pnl=None, winner="")), encoding="utf-8"
    )
    (paper_dir_15m() / "ledger.json").write_text(
        json.dumps({"bankroll": 99.04, "starting_bankroll": 100.0, "betting_pnl": -0.96, "entries": [1, 2]}),
        encoding="utf-8",
    )
    (settlements_dir_15m() / "settled.json").write_text(
        json.dumps(
            {
                "window_id": settled_id,
                "rows": [
                    {
                        "ticker": SETTLED,
                        "window_id": settled_id,
                        "settle_status": "settled",
                        "kalshi_result": "yes",
                        "status": "finalized",
                        "expiration_value": "79218.12",
                        "source_name": "CF Benchmarks",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (latest_dir_15m() / "journal.json").write_text(
        json.dumps(
            {
                "lane": "learning_lane_15m",
                "series": "KXBTC15M",
                "cf_index_id": "BRTI",
                "generated_at": "2026-09-07T17:01:00-04:00",
                "windows": [
                    {"ticker": OPEN, "window_id": open_id, "status": "active", "result": ""},
                    {"ticker": SETTLED, "window_id": settled_id, "status": "finalized", "result": "yes"},
                    {
                        "ticker": PUBLISHED_WIN,
                        "window_id": _window_id("KXBTC15M-26SEP071445", "18:30", "18:45"),
                        "status": "finalized",
                        "result": "yes",
                    },
                    {
                        "ticker": PUBLISHED_PENDING,
                        "window_id": _window_id("KXBTC15M-26SEP071500", "18:45", "19:00"),
                        "status": "finalized",
                        "result": "yes",
                    },
                    {
                        "ticker": TAPE,
                        "window_id": _window_id("KXBTC15M-26SEP071345", "17:30", "17:45"),
                        "status": "finalized",
                        "result": "no",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    manifest = repo / illustrate.REL_MANIFEST
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "lanes": [
                    {"lane_id": "golf", "last_run": {"fields": [{"label": "Run id", "value": "golf-should-be-ignored"}]}},
                    {
                        "lane_id": "learning_lane_15m",
                        "last_run": {
                            "fields": [
                                {"label": "Settled paper fill", "value": PUBLISHED_WIN},
                                {"label": "Paper outcome", "value": "paper_win"},
                                {"label": "Kalshi result", "value": "yes"},
                                {"label": "Kalshi status", "value": "finalized"},
                                {"label": "expiration_value", "value": "79148.63"},
                                {"label": "paper settle_win pnl", "value": "+1.67"},
                                {"label": "paper observation after settle", "value": "101.67"},
                                {"label": "Live paper fill", "value": PUBLISHED_PENDING},
                                {"label": "Live paper fill status", "value": "SETTLE_PENDING"},
                            ]
                        },
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    try:
        yield repo
    finally:
        set_15m_root_override(None)


def _by_ticker(blocks):
    return {row.ticker: row for block in blocks for row in block.rows}


def test_board_splits_the_two_paper_books_and_keeps_the_published_win(lane):
    blocks = {block.key: block for block in collect_board()}
    assert set(blocks) == {LINEAGE_LOCAL, LINEAGE_PUBLISHED, LINEAGE_TAPE}

    local = {row.ticker for row in blocks[LINEAGE_LOCAL].rows}
    published = {row.ticker for row in blocks[LINEAGE_PUBLISHED].rows}
    tape = {row.ticker for row in blocks[LINEAGE_TAPE].rows}
    assert local == {SETTLED, OPEN}
    # A published paper_win is never dropped off the board just because the local book is newer.
    assert published == {PUBLISHED_WIN, PUBLISHED_PENDING}
    assert tape == {TAPE}
    assert not local & published

    # Each book states its own figures and no block states a combined bankroll.
    assert any("100.00 → 99.04" in line for line in blocks[LINEAGE_LOCAL].book_lines)
    assert any("+1.67" in line and "101.67" in line for line in blocks[LINEAGE_PUBLISHED].book_lines)
    for block in blocks.values():
        for line in block.book_lines:
            assert "99.04" not in line or block.key == LINEAGE_LOCAL
            assert "101.67" not in line or block.key == LINEAGE_PUBLISHED


def test_pnl_is_only_shown_where_that_window_file_records_one(lane):
    rows = _by_ticker(collect_board())

    assert rows[SETTLED].paper_pnl == pytest.approx(1.6)
    assert rows[SETTLED].paper_pnl_text == "+1.60"
    assert rows[PUBLISHED_WIN].paper_pnl == pytest.approx(1.67)

    # An open paper position and a journal-only window both refuse to show a number.
    for ticker in (OPEN, PUBLISHED_PENDING, TAPE):
        assert rows[ticker].paper_pnl is None
        assert rows[ticker].paper_pnl_text in (illustrate.NO_PNL, illustrate.NO_PAPER)
        assert "0" not in rows[ticker].paper_pnl_text
    assert rows[OPEN].paper_settle == "open position"
    assert rows[PUBLISHED_PENDING].paper_settle == "SETTLE_PENDING"
    assert rows[TAPE].paper_settle == illustrate.NO_PAPER


def test_active_window_stays_pending_and_settled_words_come_from_the_file(lane):
    rows = _by_ticker(collect_board())

    assert rows[OPEN].kalshi_result == ""
    assert rows[OPEN].settle_status == "SETTLE_PENDING"
    assert rows[OPEN].kalshi_status == "active"

    assert rows[SETTLED].kalshi_result == "yes"
    assert rows[SETTLED].settle_status == "settled"
    assert rows[SETTLED].expiry_value == "79218.12"
    assert "settlements/*.json" in rows[SETTLED].settle_src

    # The Kalshi window can be finalized while that paper book recorded no paper settle.
    assert rows[PUBLISHED_PENDING].kalshi_result == "yes"
    assert rows[PUBLISHED_PENDING].paper_pnl is None


def test_collect_rows_keeps_the_hub_two_tuple_contract(lane):
    paper_rows, tape_rows = collect_rows()

    assert {row.ticker for row in paper_rows} == {SETTLED, OPEN, PUBLISHED_WIN, PUBLISHED_PENDING}
    assert {row.ticker for row in tape_rows} == {TAPE}
    assert all(row.paper_join for row in paper_rows)
    assert not any(row.paper_join for row in tape_rows)
    # Fields the operator-surface caption reads off these rows.
    for row in paper_rows + tape_rows:
        assert isinstance(row.ticker, str) and isinstance(row.settle_status, str)
        assert isinstance(row.kalshi_result, str)


def test_png_path_stays_bound_to_the_hub_slot(lane):
    assert REL_PNG.as_posix() == "docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png"
    assert chart_png_path() == lane / REL_PNG


def test_render_writes_a_png_from_the_files(lane):
    pytest.importorskip("matplotlib")

    dest = render_paper_window_strip()
    assert dest is not None
    assert dest == chart_png_path()
    assert dest.read_bytes().startswith(b"\x89PNG\r\n")
    # A board, not a thumbnail strip.
    assert dest.stat().st_size > 20_000


def test_skip_rows_sit_on_lineage_a_with_no_would_have_pnl(lane):
    skip_ticker = "KXBTC15M-26SEP071400-00"
    skip_id = _window_id("KXBTC15M-26SEP071400", "18:00", "18:15")
    journal_path = latest_dir_15m() / "journal.json"
    payload = json.loads(journal_path.read_text(encoding="utf-8"))
    payload["windows"].append(
        {
            "ticker": skip_ticker,
            "window_id": skip_id,
            "status": "finalized",
            "result": "yes",
        }
    )
    journal_path.write_text(json.dumps(payload), encoding="utf-8")
    (paper_dir_15m() / "rule_decisions.json").write_text(
        json.dumps(
            {
                "decisions": {
                    skip_ticker: {
                        "ticker": skip_ticker,
                        "window_id": skip_id,
                        "action": "skip",
                        "pnl": None,
                        "note": "no fill, no position, no pnl; a skip is not a loss",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    blocks = {block.key: block for block in collect_board()}
    local = {row.ticker: row for row in blocks[LINEAGE_LOCAL].rows}
    tape = {row.ticker for row in blocks[LINEAGE_TAPE].rows}
    assert skip_ticker in local
    assert skip_ticker not in tape
    assert TAPE in tape
    row = local[skip_ticker]
    assert row.skipped is True
    assert row.paper_join is False
    assert row.paper_pnl is None
    assert row.paper_pnl_text == illustrate.SKIP_PNL
    assert "would" not in row.paper_pnl_text.lower()
    assert "0" not in row.paper_pnl_text


def test_no_rows_writes_nothing(tmp_path, monkeypatch):
    set_15m_root_override(tmp_path / "empty")
    monkeypatch.setattr(illustrate, "repo_root", lambda: tmp_path / "repo")
    try:
        assert collect_board() == []
        assert render_paper_window_strip() is None
        assert not (tmp_path / "repo" / REL_PNG).exists()
    finally:
        set_15m_root_override(None)


def test_board_carries_no_golf_lane_language():
    blob = " ".join(
        [illustrate.TITLE, illustrate.SUBTITLE, illustrate.LOCAL_TITLE, illustrate.PUBLISHED_TITLE, illustrate.TAPE_TITLE]
        + list(illustrate.BADGES)
    ).lower()
    for banned in ("wc1", "calibration weather", "shadow honesty", "edge established", "banked"):
        assert banned not in blob
