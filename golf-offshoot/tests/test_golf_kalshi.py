"""golf-1 ingest island. Isolation + refuse. No paper, watch, or hub tab."""

from __future__ import annotations

from pathlib import Path

import pytest

from golf_offshoot.data_feeds.kalshi_15m import ALLOWED_SERIES, PrivateEndpointRefused
from golf_offshoot.data_feeds.names import normalize_name
from golf_offshoot.golf_kalshi import TRADING_ARMED
from golf_offshoot.golf_kalshi.adapter import (
    GolfKalshiFeed,
    GolfSeriesRefused,
    assert_golf_public_url,
    golf_only_catalog,
    is_golf_series,
    parse_market,
    parse_series,
)
from golf_offshoot.golf_kalshi.ingest import run_ingest
from golf_offshoot.golf_kalshi.matcher import extract_player_name, match_market_player
from golf_offshoot.golf_kalshi.paths import (
    REPO_FALLBACK,
    assert_golf_kalshi_path,
    catalog_path,
    golf_kalshi_root,
    set_golf_kalshi_root_override,
    unmatched_path,
)
from golf_offshoot.learning_lane_15m.paths import golf_paper_dir, set_15m_root_override
from golf_offshoot.operator_surface.lanes import lane_header_name, parse_lane


@pytest.fixture
def gk_root(tmp_path):
    root = tmp_path / "golf_kalshi"
    set_golf_kalshi_root_override(root)
    try:
        yield root
    finally:
        set_golf_kalshi_root_override(None)


def _series_golf(**kwargs) -> dict:
    row = {
        "ticker": "KXPGA",
        "title": "PGA Tour",
        "category": "Sports",
        "tags": ["Golf"],
        "fee_type": "quadratic",
        "fee_multiplier": 1,
    }
    row.update(kwargs)
    return row


def _market_raw(**kwargs) -> dict:
    row = {
        "ticker": "KXPGA-26-SSCHEFF",
        "event_ticker": "KXPGA-26",
        "series_ticker": "KXPGA",
        "title": "Will Scottie Scheffler win the Masters?",
        "yes_sub_title": "Scottie Scheffler",
        "yes_ask": 0.08,
        "status": "open",
    }
    row.update(kwargs)
    return row


def test_15m_allowlist_unchanged():
    assert ALLOWED_SERIES == "KXBTC15M"


def test_trading_never_armed():
    assert TRADING_ARMED is False
    from golf_offshoot.golf_kalshi.adapter import TRADING_ARMED as ADAPTER_ARMED

    assert ADAPTER_ARMED is False


def test_selector_still_phase1_golf():
    assert parse_lane("golf") == "golf"
    assert parse_lane("15m") == "golf"
    assert parse_lane("learning_lane_15m") == "learning_lane_15m"
    assert parse_lane("golf_kalshi") == "golf"
    assert lane_header_name("golf") == "Golf Phase 1"
    assert lane_header_name("15m") == "Golf Phase 1"
    assert lane_header_name("golf_kalshi") == "Golf Phase 1"


def test_default_root_is_own_tree():
    assert REPO_FALLBACK.name == "golf_kalshi"
    assert REPO_FALLBACK.parent.name == "data"
    assert "learning_lane_15m" not in REPO_FALLBACK.parts
    assert REPO_FALLBACK.parent / "paper" != REPO_FALLBACK


def test_adapter_refuses_crypto_and_private():
    assert is_golf_series("KXPGA", category="Sports", title="PGA Tour Golf")
    assert is_golf_series("KXLIVTOP10", category="Sports", title="Liv Top 10 Finisher", tags=["Golf"])
    assert is_golf_series("KXPGAALBATROSS", category="Sports", title="Golf Albatross", tags=[])
    assert not is_golf_series("KXBTC15M", category="Crypto", title="Bitcoin")
    assert not is_golf_series(
        "KXLEAGUESCUPGAME", category="Sports", title="Leagues Cup Game", tags=["Soccer"]
    )
    assert not is_golf_series("CAPGAIN", category="Politics", title="Capital gains tax increase")
    assert not is_golf_series(
        "KXMCMMEN", category="Sports", title="ATP Monte-Carlo Masters Winner", tags=["Tennis"]
    )
    assert not is_golf_series(
        "KXUSOPENCUP", category="Sports", title="US Open Cup Soccer", tags=["Soccer"]
    )
    with pytest.raises(PrivateEndpointRefused):
        assert_golf_public_url("https://api.elections.kalshi.com/trade-api/v2/portfolio/orders")
    with pytest.raises(PrivateEndpointRefused):
        assert_golf_public_url("https://api.elections.kalshi.com/trade-api/v2/orders")
    with pytest.raises(PrivateEndpointRefused):
        assert_golf_public_url("https://api.elections.kalshi.com/trade-api/v2/login")
    with pytest.raises(GolfSeriesRefused):
        assert_golf_public_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXBTC15M"
        )
    with pytest.raises(GolfSeriesRefused):
        assert_golf_public_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?limit=1000&status=open"
        )
    assert_golf_public_url(
        "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXPGA&status=open"
    )
    assert parse_series({"ticker": "KXBTC15M", "title": "Bitcoin", "category": "Crypto"}) is None
    assert parse_market({"ticker": "KXMV-1", "series_ticker": "", "title": "yes Chelsea"}) is None
    m = parse_market(
        {
            "ticker": "KXPGA-1",
            "series_ticker": "KXPGA",
            "title": "Will X win",
            "yes_ask_dollars": "0.12",
            "fee_multiplier": 1,
        },
        series={"series_ticker": "KXPGA", "title": "PGA Golf", "category": "Sports", "tags": ["Golf"]},
    )
    assert m is not None
    assert m["yes_ask"] == pytest.approx(0.12)
    assert m["trading_armed"] is False


def test_catalog_drops_nongolf_dump():
    cleaned = golf_only_catalog(
        {
            "series": [
                {"ticker": "KXPGA", "title": "PGA Tour", "category": "Sports", "tags": ["Golf"]},
                {
                    "ticker": "KXLEAGUESCUPGAME",
                    "title": "Leagues Cup Game",
                    "category": "Sports",
                    "tags": ["Soccer"],
                },
            ],
            "markets": [
                {
                    "ticker": "KXMVECROSSCATEGORY-1",
                    "series_ticker": "",
                    "title": "yes Chelsea,yes Liverpool",
                },
                {
                    "ticker": "KXPGA-1",
                    "series_ticker": "KXPGA",
                    "title": "Will Scottie Scheffler win?",
                    "yes_ask": 0.08,
                },
            ],
        }
    )
    assert [s["series_ticker"] for s in cleaned["series"]] == ["KXPGA"]
    assert [m["ticker"] for m in cleaned["markets"]] == ["KXPGA-1"]


def test_fetch_catalog_is_per_series_not_global_open_book(gk_root):
    urls: list[str] = []

    def fake_get(url, *, label, ttl_seconds, refresh):
        del label, ttl_seconds, refresh
        urls.append(url)
        assert_golf_public_url(url)
        if "/series?" in url and "tags=" in url:
            return {
                "series": [
                    _series_golf(),
                    {
                        "ticker": "KXLEAGUESCUPGAME",
                        "title": "Leagues Cup Game",
                        "category": "Sports",
                        "tags": ["Soccer"],
                    },
                ]
            }
        if "series_ticker=KXPGA" in url:
            return {"markets": [_market_raw(ticker="KXPGA-1")]}
        return {"series": [], "markets": []}

    feed = GolfKalshiFeed()
    feed._get = fake_get  # noqa: SLF001
    catalog = feed.fetch_catalog(refresh=True)
    assert catalog["series"][0]["series_ticker"] == "KXPGA"
    assert [m["ticker"] for m in catalog["markets"]] == ["KXPGA-1"]
    assert all("limit=1000" not in u for u in urls)
    assert all(("/markets?" not in u) or ("series_ticker=" in u) for u in urls)
    assert any("tags=Golf" in u or "tags=golf" in u for u in urls)
    assert any("series_ticker=KXPGA" in u for u in urls)
    assert any("status=settled" in u for u in urls)
    assert ALLOWED_SERIES == "KXBTC15M"


def test_unmatched_tickers_stay_unmatched(gk_root):
    market = parse_market(
        _market_raw(),
        series={"series_ticker": "KXPGA", "title": "PGA Golf", "category": "Sports", "tags": ["Golf"]},
    )
    assert market is not None
    assert extract_player_name(market) == "Scottie Scheffler"
    assert match_market_player(market, {}) is None
    assert match_market_player(market, {normalize_name("rory mcilroy"): "rory"}) is None
    hit = match_market_player(market, {normalize_name("Scottie Scheffler"): "scottie"})
    assert hit == "scottie"

    catalog = golf_only_catalog(
        {
            "series": [_series_golf()],
            "markets": [_market_raw(), _market_raw(ticker="KXPGA-FIELD", yes_sub_title="the field", title="Will the field win?")],
        }
    )
    out = run_ingest(catalog=catalog, candidates={})
    assert out["trading_armed"] is False
    assert out["unmatched"] >= 1
    payload = unmatched_path().read_text(encoding="utf-8")
    assert "KXPGA-26-SSCHEFF" in payload
    assert "Scottie Scheffler" in payload
    assert "player_id" not in payload


def test_matched_name_still_writes_no_paper_fill(gk_root):
    catalog = golf_only_catalog({"series": [_series_golf()], "markets": [_market_raw()]})
    out = run_ingest(
        catalog=catalog,
        candidates={normalize_name("Scottie Scheffler"): "scottie"},
    )
    assert out["unmatched"] == 0
    assert not (gk_root / "paper" / "ledger.json").exists()
    payload = unmatched_path().read_text(encoding="utf-8")
    assert "KXPGA-26-SSCHEFF" not in payload


def test_ingest_writes_own_root_not_15m_or_phase1(gk_root, tmp_path):
    fifteen = tmp_path / "learning_lane_15m"
    set_15m_root_override(fifteen)
    try:
        before_phase1 = set(golf_paper_dir().glob("*.json")) if golf_paper_dir().is_dir() else set()
        catalog = golf_only_catalog({"series": [_series_golf()], "markets": [_market_raw()]})
        out = run_ingest(catalog=catalog, candidates={})
        root = golf_kalshi_root()
        assert Path(out["root"]) == root
        assert catalog_path().is_file()
        assert unmatched_path().is_file()
        assert catalog_path().is_relative_to(root)
        assert unmatched_path().is_relative_to(root)
        assert not (fifteen / "catalog.json").exists()
        assert not list(fifteen.rglob("*.json"))
        after_phase1 = set(golf_paper_dir().glob("*.json")) if golf_paper_dir().is_dir() else set()
        assert after_phase1 == before_phase1
        assert not (golf_paper_dir() / "catalog.json").exists()
        assert "learning_lane_15m" not in catalog_path().parts
    finally:
        set_15m_root_override(None)


def test_assert_refuses_15m_and_phase1_paths(tmp_path):
    with pytest.raises(RuntimeError, match="learning_lane_15m"):
        assert_golf_kalshi_path(tmp_path / "learning_lane_15m" / "paper")
    with pytest.raises(RuntimeError, match="Phase 1"):
        assert_golf_kalshi_path(Path(__file__).resolve().parents[1] / "data" / "paper" / "ledger.json")


def test_golf_kalshi_does_not_import_forbidden():
    pkg = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "golf_kalshi"
    forbidden = ("polymarket", "honer_15m", "quote_bus", "operator_surface.app", "operator_surface.lanes")
    for path in pkg.glob("*.py"):
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                low = stripped.lower()
                for token in forbidden:
                    assert token not in low, path.name


def test_golf_kalshi_watch_is_refused(capsys):
    from golf_offshoot.__main__ import main

    code = main(["golf-kalshi", "--watch"])
    assert code == 2
    captured = capsys.readouterr()
    blob = captured.out + captured.err
    assert "out of scope" in blob.lower()
    assert "watch" in blob.lower()


def test_cli_golf_kalshi_one_shot(gk_root, capsys, monkeypatch):
    from golf_offshoot.__main__ import main

    def fake_fetch(self, *, refresh=False):
        del self, refresh
        return golf_only_catalog({"series": [_series_golf()], "markets": [_market_raw()]})

    monkeypatch.setattr(GolfKalshiFeed, "fetch_catalog", fake_fetch)
    code = main(["golf-kalshi", "--json"])
    assert code == 0
    out = capsys.readouterr().out
    assert "TRADING_ARMED" in out
    assert catalog_path().is_file()
    assert unmatched_path().is_file()
