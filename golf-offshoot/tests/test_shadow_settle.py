import json
from datetime import datetime, timezone
from pathlib import Path

from golf_offshoot.audit.shadow import ShadowAdvise, load_shadow
from golf_offshoot.audit.shadow_settle import (
    SOURCE_ABSENT_FIELD,
    SOURCE_ESPN_OFFICIAL,
    SOURCE_FINISH_UNKNOWN,
    SOURCE_LEDGER_TICKET,
    SOURCE_PAPER_BOOK_WINNER,
    SOURCE_ROUND_LEADER,
    backfill_shadow_settles,
    is_absent_from_official_field,
    is_relevant_advise,
    join_shadow_settles,
    settle_banner_for_rows,
    settle_counts,
)
from golf_offshoot.operator_surface.artifacts import SETTLE_PENDING, load_honesty
from golf_offshoot.strategy.paper_book import PaperBookFile
from golf_offshoot.strategy.paper_ledger import (
    EventInspect,
    EventWeek,
    LedgerEntry,
    PaperLedger,
    TicketResult,
)
from golf_offshoot.models.strategy import PortfolioState

import pytest


def _advise(**overrides) -> dict:
    row = {
        "timestamp": "2026-08-13T12:00:00+00:00",
        "tournament": "FedEx St. Jude Championship",
        "tournament_id": "401811962",
        "player": "Kurt Kitayama",
        "player_id": "kita",
        "market": "win",
        "model_probability": 0.09,
        "model_p_low": 0.06,
        "model_p_high": 0.12,
        "posted_decimal": 19.0,
        "odds_as_of": "2026-08-13T12:00:00+00:00",
        "run_mode": "live",
        "mode": "stay_selective",
        "action_kind": "new_bet",
        "suggested_stake": 8.75,
        "never_auto_bet": True,
        "paper_observation_only": True,
        "run_id": "run-1",
        "recommendation_id": "rec-1",
        "reason": "operating advise",
    }
    row.update(overrides)
    return row


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def _official_st_jude() -> EventInspect:
    return EventInspect(
        completed=True,
        finishes={
            "kita": (1, "Kurt Kitayama"),
            "fleet": (12, "Tommy Fleetwood"),
        },
        winner_ids=["kita"],
        event_name="FedEx St. Jude Championship",
        status_note="state=post name=STATUS_FINAL",
    )


def _ledger_with_tickets() -> PaperLedger:
    week = EventWeek(
        event_id="401811962",
        event_name="St Jude",
        settled_at=datetime(2026, 8, 18, 22, 0, tzinfo=timezone.utc),
        winner_id="kita",
        winner_name="Kurt Kitayama",
        tickets=[
            TicketResult(
                player_id="kita",
                player_name="Kurt Kitayama",
                bet_type="win",
                stake=8.75,
                decimal_odds=19.0,
                finish=1,
                won=True,
                payout=166.25,
                pnl=157.5,
            ),
            TicketResult(
                player_id="fleet",
                player_name="Tommy Fleetwood",
                bet_type="win",
                stake=2.19,
                decimal_odds=9.5,
                finish=12,
                won=False,
                payout=0.0,
                pnl=-2.19,
            ),
        ],
        betting_pnl=155.31,
        never_auto_bet=True,
    )
    return PaperLedger(
        bankroll=405.31,
        entries=[
            LedgerEntry(
                entry_id="led-1",
                kind="settle_win",
                amount=157.5,
                bankroll_after=405.31,
                event_id="401811962",
                never_auto_bet=True,
            )
        ],
        events=[week],
        never_auto_bet=True,
        paper_observation_only=True,
    )


def test_official_inspect_paper_win_and_lose():
    rows = join_shadow_settles(
        [
            _advise(),
            _advise(player="Tommy Fleetwood", player_id="fleet", recommendation_id="rec-2"),
        ],
        inspect_events=_official_st_jude(),
    )
    assert rows[0]["settle_status"] == "paper_win"
    assert rows[0]["settle_source"] == SOURCE_ESPN_OFFICIAL
    assert rows[1]["settle_status"] == "paper_lose"
    assert settle_banner_for_rows(rows) is None


def test_unofficial_field_stays_pending():
    inspect = EventInspect(
        completed=False,
        finishes={"kita": (1, "Kurt Kitayama")},
        winner_ids=["kita"],
        status_note="state=in name=STATUS_IN_PROGRESS",
    )
    rows = join_shadow_settles([_advise()], inspect_events=inspect)
    assert rows[0].get("settle_status") is None
    assert settle_banner_for_rows(rows) == SETTLE_PENDING


def test_playoff_two_winners_stays_pending():
    inspect = EventInspect(
        completed=True,
        finishes={"kita": (1, "Kurt Kitayama"), "fleet": (1, "Tommy Fleetwood")},
        winner_ids=["kita", "fleet"],
        status_note="state=post playoff unresolved",
    )
    rows = join_shadow_settles([_advise()], inspect_events=inspect)
    assert rows[0].get("settle_status") is None
    assert settle_banner_for_rows(rows) == SETTLE_PENDING


def test_unknown_finish_place_none_is_never_settled_and_blocks():
    inspect = EventInspect(
        completed=True,
        finishes={"kita": (None, "Kurt Kitayama"), "fleet": (12, "Tommy Fleetwood")},
        winner_ids=["fleet"],
        event_name="FedEx St. Jude Championship",
        status_note="state=post name=STATUS_FINAL",
    )
    rows = join_shadow_settles([_advise()], inspect_events=inspect)
    assert rows[0]["settle_status"] == "never_settled"
    assert rows[0]["settle_source"] == SOURCE_FINISH_UNKNOWN
    assert rows[0]["settle_status"] != "paper_win"
    assert rows[0]["settle_status"] != "paper_lose"
    assert is_relevant_advise(rows[0]) is True
    assert settle_banner_for_rows(rows) == SETTLE_PENDING


def test_absent_from_official_field_win_is_never_settled_excluded_from_banner():
    inspect = EventInspect(
        completed=True,
        finishes={"fleet": (12, "Tommy Fleetwood")},
        winner_ids=["fleet"],
        status_note="state=post name=STATUS_FINAL",
    )
    rows = join_shadow_settles([_advise()], inspect_events=inspect)
    assert rows[0]["settle_status"] == "never_settled"
    assert rows[0]["settle_source"] == SOURCE_ABSENT_FIELD
    assert "paper_win" not in (rows[0].get("settle_status"),)
    assert rows[0].get("settle_status") != "paper_lose"
    assert is_absent_from_official_field(rows[0]) is True
    assert is_relevant_advise(rows[0]) is False
    assert settle_banner_for_rows(rows) is None


def test_round_leader_is_never_settled():
    rows = join_shadow_settles(
        [_advise(market="win_after_r1")],
        inspect_events=_official_st_jude(),
    )
    assert rows[0]["settle_status"] == "never_settled"
    assert rows[0]["settle_source"] == SOURCE_ROUND_LEADER
    assert settle_banner_for_rows(rows) == SETTLE_PENDING


def test_place_market_uses_ticket_hit():
    rows = join_shadow_settles(
        [
            _advise(market="top_10"),
            _advise(player="Tommy Fleetwood", player_id="fleet", market="top_10"),
        ],
        inspect_events=_official_st_jude(),
    )
    assert rows[0]["settle_status"] == "paper_win"
    assert rows[1]["settle_status"] == "paper_lose"


def _official_bmw() -> EventInspect:
    return EventInspect(
        completed=True,
        finishes={
            "scheffler": (1, "Scottie Scheffler"),
            "mcilroy": (4, "Rory McIlroy"),
        },
        winner_ids=["scheffler"],
        event_name="BMW Championship",
        status_note="state=post name=STATUS_FINAL",
    )


def _keith_bmw_place(market: str, rec: str) -> dict:
    return _advise(
        tournament="BMW Championship",
        tournament_id="401734784",
        player="Keith Mitchell",
        player_id="keith-mitchell",
        market=market,
        recommendation_id=rec,
    )


def test_keith_mitchell_bmw_place_absent_from_official_field():
    inspect = _official_bmw()
    winner = _advise(
        tournament="BMW Championship",
        tournament_id="401734784",
        player="Scottie Scheffler",
        player_id="scheffler",
        market="win",
        recommendation_id="rec-win",
    )
    keith_rows = [
        _keith_bmw_place(market, f"rec-{market}")
        for market in ("top_5", "top_10", "top_20", "make_cut")
    ]
    rows = join_shadow_settles([winner, *keith_rows], inspect_events=inspect)
    assert len(rows) == 5
    assert rows[0]["settle_status"] == "paper_win"
    assert rows[0]["settle_source"] == SOURCE_ESPN_OFFICIAL
    keith = [row for row in rows if row["player"] == "Keith Mitchell"]
    assert len(keith) == 4
    for row in keith:
        assert row["settle_status"] == "never_settled"
        assert row["settle_source"] == SOURCE_ABSENT_FIELD
        assert row["settle_status"] not in {"paper_win", "paper_lose"}
        assert is_relevant_advise(row) is False
    counts = settle_counts(rows)
    assert counts["relevant"] == 1
    assert counts["absent_from_official_field"] == 4
    assert counts["never_settled"] == 4
    assert settle_banner_for_rows(rows) is None


def test_keith_mitchell_bmw_place_only_does_not_block_banner():
    rows = join_shadow_settles(
        [_keith_bmw_place(market, f"rec-{market}") for market in ("top_5", "top_10", "top_20", "make_cut")],
        inspect_events=_official_bmw(),
    )
    assert len(rows) == 4
    assert all(row["settle_status"] == "never_settled" for row in rows)
    assert all(row["settle_source"] == SOURCE_ABSENT_FIELD for row in rows)
    assert settle_banner_for_rows(rows) is None


def test_keith_mitchell_bmw_honesty_strip_keeps_rows_clears_banner(tmp_path):
    root = tmp_path
    (root / "settlements").mkdir()
    (root / "settlements" / "401734784.json").write_text(
        json.dumps(
            {
                "event_id": "401734784",
                "completed": True,
                "finishes": {
                    "scheffler": [1, "Scottie Scheffler"],
                    "mcilroy": [4, "Rory McIlroy"],
                },
                "winner_ids": ["scheffler"],
                "event_name": "BMW Championship",
                "status_note": "state=post name=STATUS_FINAL",
            }
        ),
        encoding="utf-8",
    )
    _write_jsonl(
        root / "shadow" / "advises.jsonl",
        [
            _advise(
                tournament="BMW Championship",
                tournament_id="401734784",
                player="Scottie Scheffler",
                player_id="scheffler",
                market="win",
                recommendation_id="rec-win",
            ),
            _keith_bmw_place("top_10", "rec-km-t10"),
        ],
    )
    honesty = load_honesty(artifact_root=root, viz_root=tmp_path / "viz")
    assert len(honesty.shadow.rows) == 2
    keith = next(row for row in honesty.shadow.rows if row["player"] == "Keith Mitchell")
    assert keith["settle_status"] == "never_settled"
    assert keith["settle_source"] == SOURCE_ABSENT_FIELD
    assert keith["settle_status"] not in {"paper_win", "paper_lose"}
    assert honesty.shadow.settle_banner is None
    assert SETTLE_PENDING not in honesty.shadow.text
    assert "Keith Mitchell" in honesty.shadow.text
    assert SOURCE_ABSENT_FIELD in honesty.shadow.text
    assert "absent_from_official_field=" in honesty.shadow.text
    assert "excluded from that denominator" in honesty.shadow.text


def test_on_disk_absent_source_short_form_excluded_from_banner():
    rows = [
        _advise(settle_status="paper_win", settle_source=SOURCE_ESPN_OFFICIAL),
        _keith_bmw_place("top_10", "rec-km"),
    ]
    rows[1]["settle_status"] = "never_settled"
    rows[1]["settle_source"] = "absent_from_official_field"
    assert is_absent_from_official_field(rows[1]) is True
    assert settle_banner_for_rows(rows) is None


def test_ledger_ticket_join_and_honesty_clears(tmp_path):
    root = tmp_path / "exports"
    (root / "paper").mkdir(parents=True)
    (root / "paper" / "ledger.json").write_text(_ledger_with_tickets().model_dump_json(), encoding="utf-8")
    _write_jsonl(
        root / "shadow" / "advises.jsonl",
        [
            _advise(),
            _advise(player="Tommy Fleetwood", player_id="fleet", recommendation_id="rec-2"),
        ],
    )
    honesty = load_honesty(artifact_root=root, viz_root=tmp_path / "viz")
    assert honesty.shadow.rows[0]["settle_status"] == "paper_win"
    assert honesty.shadow.rows[0]["settle_source"] == SOURCE_LEDGER_TICKET
    assert honesty.shadow.rows[0]["settled_at"]
    assert honesty.shadow.rows[1]["settle_status"] == "paper_lose"
    assert honesty.shadow.settle_banner is None
    assert SETTLE_PENDING not in honesty.shadow.text
    assert "settle banner off" in honesty.shadow.text


def test_missing_settle_stays_pending_on_external_sot(tmp_path):
    root = tmp_path / "golf_offshoot_real_exports"
    _write_jsonl(root / "shadow" / "advises.jsonl", [_advise()])
    honesty = load_honesty(artifact_root=root, viz_root=tmp_path / "viz")
    assert honesty.shadow.status == "SHADOW_OK"
    assert honesty.shadow.settle_banner == SETTLE_PENDING
    assert SETTLE_PENDING in honesty.shadow.text
    assert honesty.shadow.rows[0].get("settle_status") in (None, "")


def test_on_disk_never_settled_keeps_pending(tmp_path):
    root = tmp_path
    _write_jsonl(root / "shadow" / "advises.jsonl", [_advise(settle_status="never_settled")])
    honesty = load_honesty(artifact_root=root, viz_root=tmp_path / "viz")
    assert honesty.shadow.rows[0]["settle_status"] == "never_settled"
    assert honesty.shadow.settle_banner == SETTLE_PENDING


def test_mixed_never_settled_blocks_clear(tmp_path):
    root = tmp_path
    _write_jsonl(
        root / "shadow" / "advises.jsonl",
        [
            _advise(settle_status="paper_win", settle_source=SOURCE_ESPN_OFFICIAL),
            _advise(player="WD Golfer", player_id="wd", settle_status="never_settled"),
        ],
    )
    honesty = load_honesty(artifact_root=root, viz_root=tmp_path / "viz")
    assert honesty.shadow.settle_banner == SETTLE_PENDING


def test_paper_book_winner_win_market_only(tmp_path):
    root = tmp_path
    book = PaperBookFile(
        tournament_id="401811962",
        tournament_name="St Jude",
        bankroll=400.0,
        book=PortfolioState(bankroll=400.0),
        settled_at=datetime(2026, 8, 18, 22, 0, tzinfo=timezone.utc),
        settlement_winner="Kurt Kitayama",
        path_id="lived",
    )
    paper = root / "paper"
    paper.mkdir()
    (paper / "401811962.json").write_text(book.model_dump_json(), encoding="utf-8")
    win_rows = join_shadow_settles(
        [_advise(), _advise(player="Tommy Fleetwood", player_id="fleet", market="win")],
        artifact_root=root,
    )
    assert win_rows[0]["settle_status"] == "paper_win"
    assert win_rows[0]["settle_source"] == SOURCE_PAPER_BOOK_WINNER
    assert win_rows[1]["settle_status"] == "paper_lose"
    place = join_shadow_settles([_advise(market="top_10")], artifact_root=root)
    assert place[0].get("settle_status") is None


def test_settlements_cache_on_artifact_root(tmp_path):
    root = tmp_path
    (root / "settlements").mkdir()
    (root / "settlements" / "401811962.json").write_text(
        json.dumps(
            {
                "event_id": "401811962",
                "completed": True,
                "finishes": {"kita": [1, "Kurt Kitayama"], "fleet": [12, "Tommy Fleetwood"]},
                "winner_ids": ["kita"],
                "status_note": "state=post name=STATUS_FINAL",
            }
        ),
        encoding="utf-8",
    )
    _write_jsonl(root / "shadow" / "advises.jsonl", [_advise()])
    honesty = load_honesty(artifact_root=root, viz_root=tmp_path / "viz")
    assert honesty.shadow.rows[0]["settle_status"] == "paper_win"
    assert honesty.shadow.settle_banner is None


def test_mock_journal_cannot_invent_settles(tmp_path):
    path = tmp_path / "shadow" / "advises.jsonl"
    path.parent.mkdir()
    path.write_text("OFFLINE DEMO — MOCK DATA\n", encoding="utf-8")
    honesty = load_honesty(
        artifact_root=tmp_path,
        viz_root=tmp_path / "viz",
        inspect_events=_official_st_jude(),
    )
    assert honesty.shadow.barred_mock is True
    assert honesty.shadow.rows == []
    with pytest.raises(ValueError, match="barred"):
        backfill_shadow_settles(path, inspect_events=_official_st_jude())


def test_mock_inspect_cannot_invent_settles():
    inspect = EventInspect(
        completed=True,
        finishes={"kita": (1, "Kurt Kitayama")},
        winner_ids=["kita"],
        event_name="OFFLINE DEMO — MOCK DATA",
        status_note="MOCK DATA",
    )
    rows = join_shadow_settles([_advise()], inspect_events=inspect)
    assert rows[0].get("settle_status") is None
    assert settle_banner_for_rows(rows) == SETTLE_PENDING


def test_kalshi_demo_ledger_cannot_invent_settles(tmp_path):
    root = tmp_path
    (root / "paper").mkdir()
    (root / "paper" / "ledger.json").write_text(
        '{"bankroll": 1, "events": [], "note": "KALSHI DEMO fill"}',
        encoding="utf-8",
    )
    rows = join_shadow_settles([_advise()], artifact_root=root)
    assert rows[0].get("settle_status") is None


def test_backfill_writes_only_known_win_lose(tmp_path):
    path = tmp_path / "shadow" / "advises.jsonl"
    original = [
        _advise(),
        _advise(player="Ghost", player_id="ghost", recommendation_id="rec-ghost"),
        _advise(player="Tommy Fleetwood", player_id="fleet", recommendation_id="rec-2"),
    ]
    _write_jsonl(path, original)
    n = backfill_shadow_settles(path, inspect_events=_official_st_jude())
    assert n == 2
    loaded = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert loaded[0]["settle_status"] == "paper_win"
    assert loaded[0]["settle_source"] == SOURCE_ESPN_OFFICIAL
    assert "settle_status" not in loaded[1]
    assert loaded[1]["player"] == "Ghost"
    assert loaded[2]["settle_status"] == "paper_lose"
    assert loaded[0]["never_auto_bet"] is True
    assert loaded[0]["player"] == "Kurt Kitayama"


def test_backfill_does_not_rewrite_existing_status(tmp_path):
    path = tmp_path / "shadow" / "advises.jsonl"
    _write_jsonl(path, [_advise(settle_status="never_settled", settle_source="operator")])
    n = backfill_shadow_settles(path, inspect_events=_official_st_jude())
    assert n == 0
    loaded = load_shadow(path)
    assert loaded[0].settle_status == "never_settled"
    assert loaded[0].settle_source == "operator"


def test_schema_accepts_old_journal_without_settle_fields():
    row = ShadowAdvise.model_validate(_advise())
    assert row.settle_status is None
    assert row.settled_at is None
    assert row.settle_source is None
    assert row.never_auto_bet is True


def test_does_not_invent_without_evidence():
    rows = join_shadow_settles([_advise()])
    assert rows[0].get("settle_status") is None
    assert settle_banner_for_rows(rows) == SETTLE_PENDING
