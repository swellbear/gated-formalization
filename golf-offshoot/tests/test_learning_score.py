"""15m-1 quarantined replay scorer. Does not change fills or bind the bar."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from golf_offshoot.learning_lane_15m.paths import (
    golf_paper_dir,
    latest_dir_15m,
    paper_dir_15m,
    set_15m_root_override,
)
from golf_offshoot.learning_lane_15m.rules import decide, load_rules
from golf_offshoot.learning_lane_15m.runner import CLERICAL_WHITELIST
from golf_offshoot.learning_lane_15m.score import (
    GAP_TICKER,
    LINEAGE_B,
    MISSING_JOIN,
    SCORE_JSON_NAME,
    SCORE_NOTE_NAME,
    fee_adjust,
    fee_for_fill,
    score_replay,
    write_score,
)
from golf_offshoot.operator_surface.observability import repo_root

EASTERN = ZoneInfo("America/New_York")
SKIP_RULE = {
    "id": "R-SKIP-COINFLIP",
    "declared_at": "2026-09-08T05:56:00-04:00",
    "kind": "selection",
    "selects": True,
    "execution": False,
}


def _write_book(
    ticker: str,
    *,
    close_at: str,
    mark: float,
    pnl: float | None,
    settled: bool = True,
) -> Path:
    close = datetime.fromisoformat(close_at.replace("Z", "+00:00"))
    open_at = close - timedelta(minutes=15)
    window_id = (
        f"{ticker.rsplit('-', 1)[0] if ticker.count('-') >= 2 else ticker}"
        f"__{open_at.strftime('%Y-%m-%dT%H:%M:%SZ')}__"
        f"{close.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    )
    # Keep the Kalshi ticker as the first window_id token when it already has bounds.
    if "__" in ticker:
        window_id = ticker
    payload = {
        "tournament_id": window_id,
        "settled_at": "2026-09-08T12:00:00-04:00" if settled else None,
        "settlement_pnl": pnl,
        "movements": [
            {
                "kind": "new_bet",
                "player_id": ticker,
                "player_name": f"YES {ticker}",
                "model_win": mark,
                "stake_after": 1.0,
            }
        ],
        "book": {"positions": []},
    }
    dest = paper_dir_15m() / f"{ticker}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload), encoding="utf-8")
    return dest


def _eligible_close(i: int) -> tuple[str, str]:
    """i=0 is 2026-09-08T10:00:00Z = 06:00 EDT, strictly after declared_at."""
    close = datetime(2026, 9, 8, 10, 0, tzinfo=timezone.utc) + timedelta(minutes=15 * i)
    et = close.astimezone(EASTERN)
    ticker = f"KXBTC15M-26SEP{et.day:02d}{et.hour:02d}{et.minute:02d}-{et.minute:02d}"
    return ticker, close.strftime("%Y-%m-%dT%H:%M:%SZ")


def _lane(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    (tmp_path / "kalshi_15m" / "paper").mkdir(parents=True, exist_ok=True)
    (tmp_path / "kalshi_15m" / "latest").mkdir(parents=True, exist_ok=True)


def _end():
    set_15m_root_override(None)


def test_fee_term_matches_proposed_01_and_bar_draft():
    # Operator note PROPOSED 01 / evidence bar k=0.07, $1, ceil to the cent.
    assert fee_for_fill(0.9835, 1.0, k=0.07) == 0.01
    assert fee_for_fill(0.7050, 1.0, k=0.07) == 0.03
    assert fee_for_fill(0.4650, 1.0, k=0.07) == 0.04
    assert fee_for_fill(0.3850, 1.0, k=0.07) == 0.05
    assert fee_adjust(0.42, 0.7050, 1.0, k=0.07) == 0.39
    assert fee_adjust(-1.00, 0.4650, 1.0, k=0.07) == -1.04
    assert fee_adjust(-1.00, 0.50, 1.0, filled=False) == 0.0


def test_decide_skip_band_and_ineligible_clock():
    skip = decide(SKIP_RULE, posted_yes=0.50, close_at="2026-09-08T06:15:00-04:00")
    assert skip["action"] == "skip"
    fill_lo = decide(SKIP_RULE, posted_yes=0.45, close_at="2026-09-08T06:15:00-04:00")
    fill_hi = decide(SKIP_RULE, posted_yes=0.55, close_at="2026-09-08T06:15:00-04:00")
    assert fill_lo["action"] == "fill"
    assert fill_hi["action"] == "fill"
    historic = decide(SKIP_RULE, posted_yes=0.50, close_at="2026-09-08T05:56:00-04:00")
    assert historic["eligible"] is False
    assert historic["action"] == "ineligible"


def test_n_below_40_is_count_only_no_peeking_t_test(tmp_path):
    _lane(tmp_path)
    try:
        for i in range(3):
            ticker, close = _eligible_close(i)
            mark = 0.50 if i % 2 == 0 else 0.70
            pnl = -1.0 if mark == 0.50 else 0.42
            _write_book(ticker, close_at=close, mark=mark, pnl=pnl)
        payload = score_replay()
        assert payload["scored"] is False
        assert payload["n_eligible"] == 3
        assert payload["binding"] is False
        assert payload["lab_admits"] is False
        assert payload["lived"] is False
        assert payload["replay"] is True
        assert payload["trials_to_date"] == 0
        assert payload["trials_to_date_incremented"] is False
        assert "t_test" not in payload
        assert "mean_d" not in payload
        assert "windows" not in payload
        assert "no peeking t-test" in payload["reason"]
    finally:
        _end()


def test_ineligible_close_at_or_before_declared_not_in_n(tmp_path):
    _lane(tmp_path)
    try:
        ticker, close = _eligible_close(0)
        _write_book(ticker, close_at=close, mark=0.70, pnl=0.42)
        _write_book(
            "KXBTC15M-26SEP080545-45",
            close_at="2026-09-08T09:45:00Z",
            mark=0.50,
            pnl=-1.0,
        )
        payload = score_replay()
        assert payload["n_eligible"] == 1
        assert payload["n_ineligible"] == 1
        assert payload["scored"] is False
    finally:
        _end()


def test_lineage_b_gap_and_missing_join_never_in_n_or_mean(tmp_path):
    _lane(tmp_path)
    try:
        journal = {
            "windows": [
                {"ticker": LINEAGE_B, "result": "yes", "status": "finalized"},
                {"ticker": MISSING_JOIN, "result": "yes", "status": "finalized"},
                {"ticker": GAP_TICKER, "result": "yes", "status": "finalized"},
            ]
        }
        (latest_dir_15m() / "journal.json").write_text(json.dumps(journal), encoding="utf-8")
        # A planted lineage-B book after declared_at would pollute n if not excluded.
        _write_book(
            LINEAGE_B,
            close_at="2026-09-08T10:00:00Z",
            mark=0.37,
            pnl=1.67,
        )
        _write_book(
            GAP_TICKER + "-45",
            close_at="2026-09-08T10:15:00Z",
            mark=0.50,
            pnl=-1.0,
        )
        ticker, close = _eligible_close(2)
        _write_book(ticker, close_at=close, mark=0.70, pnl=0.42)
        payload = score_replay()
        assert payload["n_eligible"] == 1
        tickers = [row["ticker"] for row in payload["excluded"]]
        assert any("lineage B" in row["reason"] for row in payload["excluded"])
        assert any("072245" in row["reason"] or "gap" in row["reason"] for row in payload["excluded"])
        assert any("missing paper join" in row["reason"] for row in payload["excluded"])
        assert LINEAGE_B in tickers or any("071445" in t for t in tickers)
        assert MISSING_JOIN in tickers
        ids = " ".join(payload["eligible_window_ids"])
        assert "071445" not in ids
        assert "072245" not in ids
        assert "071500" not in ids
        assert "1.67" not in json.dumps(payload)
        assert payload["scored"] is False
    finally:
        _end()


def test_l1_scores_at_n40_uses_decide_holds_out_l2(tmp_path):
    _lane(tmp_path)
    try:
        for i in range(45):
            ticker, close = _eligible_close(i)
            mark = 0.50 if i % 2 == 0 else 0.70
            pnl = -1.0 if mark == 0.50 else 0.42
            _write_book(ticker, close_at=close, mark=mark, pnl=pnl)
        payload = score_replay()
        assert payload["scored"] is True
        assert payload["n_eligible"] == 45
        assert payload["n"] == 40
        assert payload["look"] == "L1"
        assert payload["n_held_out"] == 5
        assert payload["l2_peeked"] is False
        assert len(payload["windows"]) == 40
        held = set(payload["held_out_window_ids"])
        scored_ids = {row["window_id"] for row in payload["windows"]}
        assert held.isdisjoint(scored_ids)
        assert len(held) == 5
        for row in payload["windows"]:
            verdict = decide(
                SKIP_RULE, posted_yes=row["posted_yes"], close_at=row["close_at"]
            )
            assert row["action"] == verdict["action"]
            assert row["evidence"] == "replay"
            if row["action"] == "skip":
                assert 0.45 < row["posted_yes"] < 0.55
                assert row["pnl_rule_fee_adj"] == 0.0
                assert row["fee"] == 0.0
            else:
                assert row["fee"] == fee_for_fill(row["posted_yes"], 1.0, k=0.07)
                assert row["pnl_rule_fee_adj"] == fee_adjust(
                    row["recorded_pnl"], row["posted_yes"], 1.0, k=0.07
                )
        assert payload["t_test"]["n"] == 40
        assert payload["t_test"]["h0"] == "mean(d) <= 0"
        assert payload["binding"] is False
        assert payload["lab_admits"] is False
        assert payload["replay_vs_lived"] == "replay ≠ lived"
        assert payload["execution"] is False
        assert payload["trials_to_date_incremented"] is False
    finally:
        _end()


def test_write_score_quarantines_output_and_does_not_touch_manifest_or_trials(tmp_path):
    _lane(tmp_path)
    try:
        ticker, close = _eligible_close(0)
        _write_book(ticker, close_at=close, mark=0.70, pnl=0.42)
        rules_path = repo_root() / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_RULES.json"
        manifest_path = repo_root() / "docs" / "observability-hub" / "data" / "manifest.json"
        rules_before = hashlib.sha256(rules_path.read_bytes()).hexdigest()
        manifest_before = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        payload, paths = write_score()
        json_path = Path(paths["json"])
        note_path = Path(paths["note"])
        assert json_path.name == SCORE_JSON_NAME
        assert note_path.name == SCORE_NOTE_NAME
        assert json_path.parent == latest_dir_15m()
        body = json.loads(json_path.read_text(encoding="utf-8"))
        note = note_path.read_text(encoding="utf-8")
        assert payload["scored"] is False
        assert body["binding"] is False
        assert "Not an ADMIT" in note
        assert "binding" in note.lower()
        assert "manifest.json" in note
        assert json_path.parent != golf_paper_dir()
        assert not (golf_paper_dir() / SCORE_JSON_NAME).exists()
        assert hashlib.sha256(rules_path.read_bytes()).hexdigest() == rules_before
        assert hashlib.sha256(manifest_path.read_bytes()).hexdigest() == manifest_before
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        lane = next(
            item
            for item in manifest["lanes"]
            if item.get("lane_id") == "learning_lane_15m"
        )
        assert lane.get("records") == []
        dumped = json.dumps(body)
        assert "fee" in dumped
        assert "records[]" in body["fee_hurdle"]["display"]
        assert load_rules()["trials_to_date"] == 0
        assert load_rules()["lab_admits"] is False
        assert load_rules()["evidence_bar"]["binding"] is False
        skip = next(
            row for row in load_rules()["rules"] if row["id"] == "R-SKIP-COINFLIP"
        )
        assert skip["execution"] is False
    finally:
        _end()


def test_cli_score_15m_writes_latest_not_manifest(tmp_path):
    from golf_offshoot.__main__ import main

    _lane(tmp_path)
    try:
        ticker, close = _eligible_close(0)
        _write_book(ticker, close_at=close, mark=0.50, pnl=-1.0)
        code = main(["score-15m", "--json"])
        assert code == 0
        assert (latest_dir_15m() / SCORE_JSON_NAME).is_file()
        body = json.loads((latest_dir_15m() / SCORE_JSON_NAME).read_text(encoding="utf-8"))
        assert body["rule_id"] == "R-SKIP-COINFLIP"
        assert body["scored"] is False
    finally:
        _end()


def test_scorer_is_not_clerical_and_does_not_import_gym_factory():
    source = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "learning_lane_15m" / "score.py"
    text = source.read_text(encoding="utf-8")
    assert "clerical_score" not in text
    assert "consult_registry" not in text
    assert "record_trial" not in text
    assert "learning_lane_15m.paper" not in text
    assert "write_observability" not in text
    assert CLERICAL_WHITELIST == ("illustrator", "systems", "digestor")
    assert "score" not in CLERICAL_WHITELIST
