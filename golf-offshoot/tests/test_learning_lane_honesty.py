"""15m-0 honesty regressions: lineage, missing-join, gap window, fees, HOLD.

Tests only. These lock monitor facts so later fill/score PRs cannot "clean" them
by summing books, calling a missing join pending, backfilling 072245, printing a
fee-accurate total on the hub/digest/records[], or widening ALLOWED_SERIES.

Export and the wake scan (fills / published_only) are the score-adjacent paths on
this tree. A later `score.py` artifact under latest/ is checked if present.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pytest

from golf_offshoot.data_feeds.kalshi_15m import (
    ALLOWED_SERIES,
    Kalshi15mFeed,
    SeriesNotAllowedError,
    TickerParseError,
    parse_event,
    parse_event_ticker,
    parse_market,
    parse_market_ticker,
)
from golf_offshoot.learning_lane_15m import digest, learn
from golf_offshoot.learning_lane_15m.digest import (
    CAVEATS_BANNER,
    GAP_TICKER,
    MISSING_JOIN,
    collect_figures,
    render_figures,
    write_digest,
)
from golf_offshoot.learning_lane_15m.learn import (
    MISSING_JOIN_BANNER,
    NO_PAPER_PNL,
    STATE_OFFICIAL_NO_BOOK,
    record_learning_tick,
    scan_learning_evidence,
)
from golf_offshoot.learning_lane_15m.loop import settle_join
from golf_offshoot.learning_lane_15m.paper import iter_books, load_ledger, paper_autobet_open_markets
from golf_offshoot.learning_lane_15m.paths import (
    PRIMARY_SERIES,
    latest_dir_15m,
    paper_dir_15m,
    set_15m_root_override,
    settlements_dir_15m,
)
from golf_offshoot.learning_lane_15m.settle import SETTLE_PENDING, SETTLE_SETTLED, classify_settle
from golf_offshoot.operator_surface import observability

LINEAGE_A_TICKER = "KXBTC15M-26SEP071545-45"
LINEAGE_B_TICKER = "KXBTC15M-26SEP071445-45"
MISSING_JOIN_TICKER = "KXBTC15M-26SEP071500-00"
LINEAGE_B_PNL = 1.67
LINEAGE_B_PNL_TEXT = "+1.67"
MARK = 0.40
CFB = [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}]
JOURNAL_AT = "2026-09-07T20:00:00Z"

FEE_TOTAL_KEYS = frozenset(
    {
        "fee_accurate",
        "fee_accurate_pnl",
        "fee_accurate_total",
        "fee_adjusted",
        "fee_adjusted_pnl",
        "corrected_pnl",
        "corrected_total",
        "fee_total",
        "total_fee",
        "hurdle_pnl",
    }
)

FOREIGN_SERIES = (
    "KXBTC",
    "KXBTC-26SEP071400",
    "KXETH15M",
    "KXETH15M-26SEP071400",
    "KXNFLGAME",
    "KXPALLADIUM15M-26SEP071415-15",
)

MONEY_RE = re.compile(r"[+-]?\d+\.\d{2}")


def _event_raw(event_ticker: str) -> dict:
    return {
        "event_ticker": event_ticker,
        "series_ticker": "KXBTC15M",
        "title": "BTC 15 min",
        "settlement_sources": CFB,
    }


def _market_raw(ticker: str, *, status: str, result: str, yes_ask: str = "0.4000") -> dict:
    return {
        "ticker": ticker,
        "event_ticker": ticker.rsplit("-", 1)[0],
        "status": status,
        "result": result,
        "yes_ask_dollars": yes_ask,
        "title": "BTC price up in next 15 mins?",
        "settlement_sources": CFB,
    }


def _write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
        return
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _published_lane() -> dict:
    return {
        "lane_id": "learning_lane_15m",
        "last_run": {
            "status": "published export",
            "headline": (
                f"First fill {LINEAGE_B_TICKER} settled paper_win. "
                f"Live {MISSING_JOIN_TICKER} is SETTLE_PENDING. Observation only."
            ),
            "fields": [
                {"label": "Settled paper fill", "value": LINEAGE_B_TICKER},
                {"label": "Paper outcome", "value": "paper_win"},
                {"label": "paper settle_win pnl", "value": LINEAGE_B_PNL_TEXT},
                {"label": "Live paper fill", "value": MISSING_JOIN_TICKER},
                {"label": "Live paper fill status", "value": "SETTLE_PENDING"},
            ],
            "notes": [
                f"Live {MISSING_JOIN_TICKER} stays SETTLE_PENDING. Do not invent that window's win/lose.",
            ],
        },
        "settle": {
            "banner": "SETTLE_PENDING",
            "headline": (
                f"Live window {MISSING_JOIN_TICKER} is still SETTLE_PENDING until Kalshi result."
            ),
            "counts": [
                {"label": "Pending windows", "value": "1"},
                {"label": "Settled windows", "value": "1"},
                {"label": "paper_win", "value": "1"},
                {"label": "paper settle_win pnl", "value": LINEAGE_B_PNL_TEXT},
                {"label": "paper observation after settle", "value": "101.67"},
            ],
            "residual": [
                {
                    "label": MISSING_JOIN_TICKER,
                    "value": "SETTLE_PENDING",
                    "note": "SETTLE_PENDING until Kalshi result on this window.",
                }
            ],
            "notes": [],
        },
        "paper_ledger": {
            "status": "counts only — no cash figures published",
            "headline": "Paper ticket counts.",
            "rows": [
                {"label": "paper_win", "value": "1"},
                {"label": "paper settle_win pnl", "value": LINEAGE_B_PNL_TEXT},
            ],
            "notes": [],
        },
        "records": [],
        "records_note": "No weekly operating record exists for this lane.",
    }


def _journal_row(ticker: str, result: str, status: str = "finalized") -> dict:
    return {
        "ticker": ticker,
        "event_ticker": ticker.rsplit("-", 1)[0],
        "window_id": ticker.rsplit("-", 1)[0],
        "status": status,
        "result": result,
    }


@pytest.fixture()
def honesty(tmp_path, monkeypatch):
    """Lineage A ledger on this tree + lineage B paper_win on a published manifest."""
    monkeypatch.setattr(
        "golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf"
    )
    set_15m_root_override(tmp_path / "kalshi_15m")
    repo = tmp_path / "repo"
    monkeypatch.setattr(learn, "repo_root", lambda: repo)
    monkeypatch.setattr(observability, "repo_root", lambda: repo)
    monkeypatch.setattr(digest, "repo_root", lambda: repo)
    _write(
        repo / "docs" / "observability-hub" / "data" / "manifest.json",
        {"schema_version": 1, "lanes": [{"lane_id": "golf"}, _published_lane()]},
    )
    _write(
        repo / "docs" / "agents" / "DESK.md",
        "# Agent desk\n\n## Honesty checklist (CoS stamp — gate for Lab)\n",
    )
    caveats_src = Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
    _write(
        repo / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md",
        caveats_src.read_text(encoding="utf-8"),
    )
    event = parse_event(_event_raw(LINEAGE_A_TICKER.rsplit("-", 1)[0]))
    open_mkt = parse_market(
        _market_raw(LINEAGE_A_TICKER, status="active", result="", yes_ask="0.4000"),
        event=event,
    )
    paper_autobet_open_markets([open_mkt])
    official = parse_market(
        _market_raw(LINEAGE_A_TICKER, status="finalized", result="yes", yes_ask="0.4000"),
        event=event,
    )
    settle_join([official], [event])
    _write(
        latest_dir_15m() / "journal.json",
        {
            "lane": "learning_lane_15m",
            "generated_at": JOURNAL_AT,
            "windows": [
                _journal_row(MISSING_JOIN_TICKER, "yes"),
                _journal_row(LINEAGE_B_TICKER, "yes"),
                _journal_row(LINEAGE_A_TICKER, "yes"),
            ],
        },
    )
    try:
        yield repo
    finally:
        set_15m_root_override(None)


def _export_lane(repo, monkeypatch, existing=None):
    monkeypatch.setattr(observability, "repo_root", lambda: repo)
    return observability.build_hub_manifest(
        existing=existing
        or {
            "lanes": [{"lane_id": "golf"}, _published_lane()],
        }
    )


def _money_tokens(node) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        for value in node.values():
            found |= _money_tokens(value)
    elif isinstance(node, list):
        for item in node:
            found |= _money_tokens(item)
    elif isinstance(node, bool):
        return found
    elif isinstance(node, (int, float)):
        found.add(f"{float(node):.2f}")
        found.add(f"{float(node):+.2f}")
    elif isinstance(node, str):
        found.update(MONEY_RE.findall(node))
    return found


def _combined_tokens(lineage_a: float, lineage_b: float) -> set[str]:
    summed = round(lineage_a + lineage_b, 2)
    net_ab = round(lineage_a - lineage_b, 2)
    net_ba = round(lineage_b - lineage_a, 2)
    avg = round((lineage_a + lineage_b) / 2.0, 2)
    into_seed = round(100.0 + lineage_a + lineage_b, 2)
    out = set()
    for value in (summed, net_ab, net_ba, avg, into_seed):
        out.add(f"{value:.2f}")
        out.add(f"{value:+.2f}")
    return out


def _lineage_a_pnl() -> float:
    books = [rec for rec in iter_books() if rec.settled_at is not None]
    assert books, "lineage A fixture must settle one book"
    return float(books[0].settlement_pnl)


def _fee_accurate_pnl(recorded: float, mark: float) -> float:
    raw = 0.07 * 1.0 * mark * (1.0 - mark)
    fee = math.ceil(raw * 100.0) / 100.0
    return round(recorded - fee, 2)


def _fill_settle_score_tickers(scan: dict, lane15: dict) -> set[str]:
    tickers: set[str] = set()
    tickers.update(scan.get("settled") or {})
    for book in (scan.get("fills") or {}).values():
        tickers.update(book.get("tickers") or [])
        tickers.add(book.get("window_id") or "")
    for row in scan.get("pending") or []:
        tickers.add(row.get("ticker") or "")
    for row in scan.get("published_only") or []:
        tickers.add(row.get("ticker") or "")
    for row in scan.get("paper_join_missing") or []:
        tickers.add(row.get("ticker") or "")
    for row in (lane15.get("settle") or {}).get("residual") or []:
        tickers.add(row.get("label") or "")
    for row in (lane15.get("learning_status") or {}).get("pending_windows") or []:
        tickers.add(row.get("label") or "")
    for row in (lane15.get("learning_status") or {}).get("missing_paper_joins") or []:
        tickers.add(row.get("label") or "")
    for row in (lane15.get("learning_status") or {}).get("published_history") or []:
        tickers.add(row.get("label") or "")
    score_path = latest_dir_15m() / "score_15m.json"
    if score_path.is_file():
        payload = json.loads(score_path.read_text(encoding="utf-8"))
        for row in payload.get("rows") or payload.get("windows") or []:
            if isinstance(row, dict):
                tickers.add(str(row.get("ticker") or row.get("label") or ""))
    tickers.discard("")
    return tickers


def _walk_fee_total_keys(node, path: str = "") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            norm = str(key).lower().replace("-", "_")
            assert norm not in FEE_TOTAL_KEYS, f"fee-accurate total key {key!r} at {child}"
            _walk_fee_total_keys(value, child)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _walk_fee_total_keys(item, f"{path}[{index}]")


def test_allowed_series_still_raises_on_non_kxbtc15m():
    assert ALLOWED_SERIES == "KXBTC15M"
    assert PRIMARY_SERIES == "KXBTC15M"
    assert ALLOWED_SERIES == PRIMARY_SERIES
    with pytest.raises(SeriesNotAllowedError):
        parse_event(
            {
                "event_ticker": "KXBTC15M-26SEP071400",
                "series_ticker": "KXNFLGAME",
                "settlement_sources": CFB,
            }
        )
    for raw in FOREIGN_SERIES:
        with pytest.raises((SeriesNotAllowedError, TickerParseError)):
            parse_event_ticker(raw)
        with pytest.raises((SeriesNotAllowedError, TickerParseError)):
            parse_market_ticker(raw)
    feed = Kalshi15mFeed()
    with pytest.raises(SeriesNotAllowedError):
        feed.fetch(series="KXETH15M")
    with pytest.raises(SeriesNotAllowedError):
        feed.fetch(series="KXBTC")


def test_lineage_a_and_b_never_summed_netted_or_averaged(honesty, monkeypatch):
    record_learning_tick()
    scan = scan_learning_evidence()
    lane15 = _export_lane(honesty, monkeypatch)["lanes"][1]
    figures = collect_figures(root=honesty)
    generated = render_figures(figures)

    a_pnl = _lineage_a_pnl()
    assert a_pnl == pytest.approx(1.50)
    ledger = load_ledger()
    assert float(ledger.betting_pnl) == pytest.approx(a_pnl)
    assert float(figures["betting_pnl"]) == pytest.approx(a_pnl)

    kept = {row["ticker"]: row for row in scan["published_only"]}
    assert LINEAGE_B_TICKER in kept
    assert kept[LINEAGE_B_TICKER]["paper_outcome"] == "paper_win"
    assert kept[LINEAGE_B_TICKER]["published_paper_pnl"] == LINEAGE_B_PNL_TEXT
    local_tickers = {t for book in scan["fills"].values() for t in book["tickers"]}
    assert LINEAGE_A_TICKER in local_tickers
    assert LINEAGE_B_TICKER not in local_tickers

    counts = {row["label"]: row["value"] for row in lane15["settle"]["counts"]}
    assert counts["Lineage B · paper settle_win pnl"] == LINEAGE_B_PNL_TEXT
    assert "paper settle_win pnl" not in counts
    notes = " ".join(lane15["paper_ledger"].get("notes") or [])
    assert "never added together" in notes
    assert lane15["learning_status"]["lineage"].startswith("lineage A")
    history = lane15["learning_status"]["published_history"]
    assert history[0]["lineage"].startswith("lineage B")
    assert history[0]["published_paper_pnl"] == LINEAGE_B_PNL_TEXT

    combined = _combined_tokens(a_pnl, LINEAGE_B_PNL)
    own = {f"{a_pnl:.2f}", f"{a_pnl:+.2f}", f"{LINEAGE_B_PNL:.2f}", LINEAGE_B_PNL_TEXT, "101.67"}
    forbidden = combined - own
    published = (
        _money_tokens(lane15)
        | _money_tokens(scan)
        | _money_tokens(figures)
        | _money_tokens(generated)
    )
    leaked = forbidden & published
    assert not leaked, f"lineage A {a_pnl:+.2f} and B {LINEAGE_B_PNL_TEXT} were combined: {leaked}"
    assert f"{a_pnl + LINEAGE_B_PNL:.2f}" not in generated
    assert "never added to lineage A" in generated


def test_missing_join_is_not_settle_pending_and_invents_no_pnl(honesty, monkeypatch):
    assert MISSING_JOIN == MISSING_JOIN_TICKER
    record_learning_tick()
    scan = scan_learning_evidence()
    missing = {row["ticker"]: row for row in scan["paper_join_missing"]}
    assert MISSING_JOIN_TICKER in missing
    row = missing[MISSING_JOIN_TICKER]
    assert row["official_result"] == "yes"
    assert row["paper_book_on_tree"] is False
    assert row["state"] == STATE_OFFICIAL_NO_BOOK
    assert row["paper_pnl"] is None
    assert "not a pending window" in row["reason"]
    assert MISSING_JOIN_TICKER not in {p["ticker"] for p in scan["pending"]}
    assert MISSING_JOIN_TICKER in scan["settled"]
    assert "0.00" not in json.dumps(row)

    market = parse_market(
        _market_raw(MISSING_JOIN_TICKER, status="finalized", result="yes"),
        event=parse_event(_event_raw(MISSING_JOIN_TICKER.rsplit("-", 1)[0])),
    )
    classified = classify_settle(market, event=parse_event(_event_raw(MISSING_JOIN_TICKER.rsplit("-", 1)[0])))
    assert classified.settle_status == SETTLE_SETTLED
    assert classified.settle_status != SETTLE_PENDING
    assert classified.won is None
    assert classified.pnl is None

    lane15 = _export_lane(honesty, monkeypatch)["lanes"][1]
    residual = {r["label"]: r for r in lane15["settle"]["residual"]}
    orphan = residual[MISSING_JOIN_TICKER]
    assert "PENDING" not in orphan["value"].upper()
    assert "missing paper join" in orphan["value"]
    assert orphan["value"] == MISSING_JOIN_BANNER
    assert "none is invented" in orphan["note"]
    joins = lane15["learning_status"]["missing_paper_joins"]
    assert joins[0]["label"] == MISSING_JOIN_TICKER
    assert joins[0]["paper_pnl"] == NO_PAPER_PNL
    assert joins[0]["value"] != SETTLE_PENDING
    blob = json.dumps(joins[0])
    assert "paper_win" not in blob
    assert SETTLE_PENDING not in blob


def test_gap_window_072245_is_not_a_fill_settle_or_score_row(honesty, monkeypatch):
    assert GAP_TICKER == "KXBTC15M-26SEP072245"
    record_learning_tick()
    scan = scan_learning_evidence()
    lane15 = _export_lane(honesty, monkeypatch)["lanes"][1]
    figures = collect_figures(root=honesty)
    generated = render_figures(figures)

    assert figures["gap_absent"] is True
    assert list(paper_dir_15m().glob("*072245*")) == []
    assert list(settlements_dir_15m().glob("*072245*")) == []
    tickers = _fill_settle_score_tickers(scan, lane15)
    assert GAP_TICKER not in tickers
    assert GAP_TICKER not in json.dumps(scan)
    assert GAP_TICKER not in json.dumps(lane15)
    assert GAP_TICKER not in json.dumps({k: v for k, v in figures.items() if k != "gap_absent"})
    absences = generated.split("### Absences", 1)[1]
    before_absences = generated.split("### Absences", 1)[0]
    assert GAP_TICKER not in before_absences
    assert f"`{GAP_TICKER}` paper+settle files present? `False`" in absences


def test_hub_digest_records_refuse_fee_accurate_totals(honesty, monkeypatch):
    record_learning_tick()
    a_pnl = _lineage_a_pnl()
    fee_pnl = _fee_accurate_pnl(a_pnl, MARK)
    assert fee_pnl != a_pnl

    poisoned = _published_lane()
    poisoned["records"] = [
        {
            "record_id": "FEE-TOTAL",
            "verdict": "n/a",
            "note": f"fee-accurate pnl {fee_pnl:+.2f}",
        }
    ]
    payload = _export_lane(honesty, monkeypatch, existing={"lanes": [{"lane_id": "golf"}, poisoned]})
    lane15 = payload["lanes"][1]
    assert lane15["records"] == []
    assert "FEE-TOTAL" not in json.dumps(lane15["records"])
    _walk_fee_total_keys(lane15)
    _walk_fee_total_keys(lane15.get("paper_ledger"))

    figures = collect_figures(root=honesty)
    _walk_fee_total_keys(figures)
    assert float(figures["betting_pnl"]) == a_pnl
    assert figures["lineage_b_records_n"] == 0
    generated = render_figures(figures)
    assert "fee-accurate" not in generated.lower()
    figure_tokens = _money_tokens(figures) | _money_tokens(generated) | _money_tokens(lane15["records"])
    assert f"{fee_pnl:.2f}" not in figure_tokens
    assert f"{fee_pnl:+.2f}" not in figure_tokens

    written = write_digest(root=honesty).read_text(encoding="utf-8")
    generated_half, caveats_half = written.split(CAVEATS_BANNER, 1)
    assert "fee-accurate" not in generated_half.lower()
    assert f"{fee_pnl:+.2f}" not in _money_tokens(generated_half)
    assert "omit the known fee" in generated_half
    assert "fee-accurate" in caveats_half
    assert "records[]" in caveats_half
