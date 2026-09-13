"""Factory overlay F-SKIP-FOREIGN-HORIZON. Not a P-* row. Not Q7. Not G-SKIP-*."""

from __future__ import annotations

import json
from pathlib import Path

from golf_offshoot.factory_overlay.foreign_horizon import ACTION_FILL, ACTION_SKIP, decide
from golf_offshoot.factory_overlay.library import (
    FROZEN_IDS,
    FactoryOverlayError,
    load_library,
    policy_by_id,
    policy_ids,
)
from golf_offshoot.policy_family.library import FROZEN_IDS as P_FROZEN_IDS

DOCS = Path(__file__).resolve().parents[1] / "docs"


def test_library_loads_frozen_id_and_stays_unseated():
    ids = policy_ids()
    assert ids == FROZEN_IDS
    payload = load_library()
    assert payload["lab_admits"] is False
    assert payload["trading_armed"] is False
    assert payload["execution"] is False
    assert payload["queued_next"] == ["F-SKIP-NON-PRIMARY-CONTRACT"]
    assert "G-SKIP-SLOW-SLEEVE" in payload["not"]
    assert "Q7" in payload["not"]
    row = policy_by_id("F-SKIP-FOREIGN-HORIZON")
    assert row["side"] == "yes"
    assert row["else"].lower().startswith("fill yes")
    assert row["params"]["missing_horizon"] == "fill"
    assert row["params"]["fifteen_m_in_play_series"] == "KXBTC15M"
    blob = json.dumps(payload).lower().replace("never fill no", "")
    assert "fill-no" not in blob
    assert "buy no" not in blob


def test_factory_skip_is_not_a_p_row_or_golf_only_name():
    assert "F-SKIP-FOREIGN-HORIZON" not in P_FROZEN_IDS
    assert all(not ident.startswith("P-") for ident in FROZEN_IDS)
    assert all(not ident.startswith("G-SKIP-") for ident in FROZEN_IDS)
    text = (DOCS / "FACTORY_OVERLAY.json").read_text(encoding="utf-8")
    assert "G-SKIP-SLOW-SLEEVE" in text
    assert "P-SKIP-CLOSE-MINUTES-15-30" in text


def test_factory_skip_is_not_a_clock_farm_notebook():
    from golf_offshoot.learning_lane_15m.farm import unused_legal_kinds

    farm = json.loads((DOCS / "LEARNING_LANE_15M_FARM.json").read_text(encoding="utf-8"))
    ids = [str(row.get("id") or "") for row in farm["notebooks"]]
    assert "F-SKIP-FOREIGN-HORIZON" not in ids
    assert not any("G-SKIP" in ident for ident in ids)
    golf = (DOCS / "GOLF_KALSHI.md").read_text(encoding="utf-8")
    assert "F-SKIP-FOREIGN-HORIZON" in golf
    assert "G-SKIP-SLOW-SLEEVE" in golf
    assert all(slot["kind"] != "F-SKIP-FOREIGN-HORIZON" for slot in unused_legal_kinds())


def test_missing_horizon_fills():
    verdict = decide({})
    assert verdict["action"] == ACTION_FILL
    assert verdict["side"] == "yes"
    golf_blank = decide({"lane": "golf_kalshi"})
    assert golf_blank["action"] == ACTION_FILL
    fifteen = decide({"lane": "learning_lane_15m"})
    assert fifteen["action"] == ACTION_FILL
    assert "missing" in fifteen["reason"]


def test_fifteen_m_kxbtc15m_always_fills_even_with_clock_fields():
    row = {
        "lane": "learning_lane_15m",
        "series_ticker": "KXBTC15M",
        "ticker": "KXBTC15M-26SEP130915-15",
        "close_at": "2026-09-13T09:15:00-04:00",
        "fill_at": "2026-09-13T09:14:50-04:00",
        "posted_yes": 0.51,
    }
    verdict = decide(row)
    assert verdict["action"] == ACTION_FILL
    assert "KXBTC15M" in verdict["reason"]
    by_ticker = decide({"ticker": "KXBTC15M-26SEP130930-30"})
    assert by_ticker["action"] == ACTION_FILL


def test_fifteen_m_foreign_series_skips():
    verdict = decide({"lane": "learning_lane_15m", "series_ticker": "KXETH15M"})
    assert verdict["action"] == ACTION_SKIP
    assert verdict["side"] == "yes"


def test_golf_slow_or_season_skips():
    slow = decide({"lane": "golf_kalshi", "sleeve": "slow"})
    assert slow["action"] == ACTION_SKIP
    season = decide({"lane": "golf_kalshi", "sleeve": "week", "market_horizon": "season"})
    assert season["action"] == ACTION_SKIP
    title = decide({"title": "2026 FedEx Cup winner"})
    assert title["action"] == ACTION_SKIP


def test_golf_fast_and_week_fill():
    week = decide({"lane": "golf_kalshi", "sleeve": "week", "market_horizon": "win"})
    assert week["action"] == ACTION_FILL
    fast = decide({"title": "Irish Open 3-ball: Scottie Scheffler"})
    assert fast["action"] == ACTION_FILL
    cut = decide({"title": "Make the cut: Rory McIlroy"})
    assert cut["action"] == ACTION_FILL


def test_generic_horizon_vs_in_play_class():
    skip = decide({"horizon": "season", "in_play_class": "event"})
    assert skip["action"] == ACTION_SKIP
    fill = decide({"horizon": "event", "in_play_class": "event"})
    assert fill["action"] == ACTION_FILL


def test_never_fill_no():
    for row in ({}, {"lane": "golf_kalshi", "sleeve": "slow"}, {"series_ticker": "KXBTC15M"}):
        verdict = decide(row)
        assert verdict["action"] in {ACTION_FILL, ACTION_SKIP}
        assert verdict["side"] == "yes"
        assert verdict["action"] != "fill_no"


def test_docs_name_factory_skip_not_q7_or_honer_copy():
    blobs = [
        (DOCS / "GOLF_KALSHI.md").read_text(encoding="utf-8"),
        (DOCS / "LEARNING_LANE_15M.md").read_text(encoding="utf-8"),
        (DOCS / "LEARNING_LANE_15M_FARM.md").read_text(encoding="utf-8"),
        (DOCS / "LEARNING_LANE_15M_MECHANISM_CATALOG.json").read_text(encoding="utf-8"),
        (DOCS / "HONER_15M.md").read_text(encoding="utf-8"),
    ]
    for blob in blobs:
        assert "F-SKIP-FOREIGN-HORIZON" in blob
        assert "Q7" in blob
    catalog = json.loads((DOCS / "LEARNING_LANE_15M_MECHANISM_CATALOG.json").read_text(encoding="utf-8"))
    kind_ids = [str(row.get("id") or "") for row in catalog["kinds"]]
    assert "F-SKIP-FOREIGN-HORIZON" in kind_ids
    assert "CLOCK-HOUR-FIRST-HALF" in kind_ids
    farm_kinds = [row["kind"] for row in json.loads((DOCS / "LEARNING_LANE_15M_FARM.json").read_text())["notebooks"]]
    assert "F-SKIP-FOREIGN-HORIZON" not in farm_kinds


def test_express_rejects_other_ids():
    try:
        from golf_offshoot.factory_overlay.foreign_horizon import express

        express({"id": "G-SKIP-SLOW-SLEEVE"}, {"sleeve": "slow"})
    except FactoryOverlayError as exc:
        assert "G-SKIP-SLOW-SLEEVE" in str(exc)
    else:
        raise AssertionError("golf-only id must not express")
