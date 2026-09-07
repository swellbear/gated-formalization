from golf_offshoot.data_feeds.kalshi_15m import (
    ALLOWED_SERIES,
    CF_INDEX_ID,
    CFB_WS_AVERAGE_ROLE,
    Kalshi15mFeed,
    PrivateEndpointRefused,
    SeriesNotAllowedError,
    TickerParseError,
    assert_public_read_url,
    is_paper_autobet_candidate,
    parse_dollar_unit,
    parse_event,
    parse_event_ticker,
    parse_kalshi_result,
    parse_market,
    parse_market_ticker,
    parse_settlement_sources,
    public_mid_or_last,
    source_is_cf_benchmarks,
    window_id,
)
from golf_offshoot.models.enums import SourceKind


EVENT = {
    "event_ticker": "KXBTC15M-26SEP071400",
    "series_ticker": "KXBTC15M",
    "title": "BTC 15 min · $79,177.08 target",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

OPEN_MARKET = {
    "ticker": "KXBTC15M-26SEP071415-15",
    "event_ticker": "KXBTC15M-26SEP071415",
    "status": "active",
    "result": "",
    "yes_ask_dollars": "0.5200",
    "yes_bid_dollars": "0.4800",
    "last_price_dollars": "0.5100",
    "title": "BTC price up in next 15 mins?",
}

INITIALIZED_MARKET = {
    "ticker": "KXBTC15M-26SEP071600-00",
    "event_ticker": "KXBTC15M-26SEP071600",
    "status": "initialized",
    "result": "",
    "yes_ask_dollars": None,
    "yes_bid_dollars": None,
    "last_price_dollars": None,
    "title": "BTC price up in next 15 mins?",
}

SETTLED_MARKET = {
    "ticker": "KXBTC15M-26SEP071400-00",
    "event_ticker": "KXBTC15M-26SEP071400",
    "status": "finalized",
    "result": "yes",
    "yes_ask_dollars": "1.0000",
    "expiration_value": "79177.08",
    "settlement_ts": "2026-09-07T18:00:05Z",
    "settlement_value_dollars": "1.0000",
    "floor_strike": 79143.14,
    "can_close_early": True,
    "price_level_structure": "tapered_deci_cent",
    "rules_primary": "If the simple average of the sixty seconds of CF Benchmarks' BRTI before 2:00 PM EDT",
    "rules_secondary": "60 RTI prices are collected. The official and final value is the average.",
}

SERIES = {
    "ticker": "KXBTC15M",
    "fee_type": "quadratic",
    "fee_multiplier": 1,
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}


def test_parse_dollar_and_result():
    assert parse_dollar_unit("0.5200") == 0.52
    assert parse_dollar_unit("0.0000") is None
    assert parse_dollar_unit("1.0000") is None
    assert parse_kalshi_result("yes") == "yes"
    assert parse_kalshi_result("") == ""
    assert parse_kalshi_result("maybe") == ""


def test_parse_event_requires_kxbtc15m():
    ev = parse_event(EVENT)
    assert ev["series_ticker"] == ALLOWED_SERIES
    assert ev["source_is_cf_benchmarks"] is True
    sources = parse_settlement_sources(EVENT["settlement_sources"])
    assert source_is_cf_benchmarks(sources)
    try:
        parse_event({**EVENT, "series_ticker": "KXNFLGAME"})
        raise AssertionError("other series must be refused")
    except SeriesNotAllowedError:
        pass


def test_event_ticker_grammar_kxbtc15m_yymonddhhmm():
    parsed = parse_event_ticker("KXBTC15M-26SEP071400")
    assert parsed["series_ticker"] == "KXBTC15M"
    assert parsed["window_token"] == "26SEP071400"
    assert parsed["ticker"] == "KXBTC15M-26SEP071400"
    try:
        parse_event_ticker("KXBTC15M-26SEP071400-15")
        raise AssertionError("event ticker must not carry a trailing minute suffix")
    except TickerParseError as exc:
        assert "series" in str(exc).lower() or "YYMONDDHHMM" in str(exc)


def test_market_trailing_minute_suffix_is_not_series():
    parsed = parse_market_ticker("KXBTC15M-26SEP071415-15")
    assert parsed["series_ticker"] == "KXBTC15M"
    assert parsed["event_ticker"] == "KXBTC15M-26SEP071415"
    assert parsed["minute_suffix"] == "15"
    assert parsed["minute_suffix"] != parsed["series_ticker"]
    assert parsed["window_token"] == "26SEP071415"


def test_refuse_kxbtc_threshold_and_btc_substring():
    for raw in ("KXBTC", "KXBTC-26SEP071400", "FOOBTCBAR-26SEP071400", "BTC-26SEP071400"):
        try:
            parse_event_ticker(raw)
            raise AssertionError(raw)
        except SeriesNotAllowedError:
            pass
    try:
        parse_event_ticker("KXETH15M-26SEP071400")
        raise AssertionError("ETH must be refused")
    except (SeriesNotAllowedError, TickerParseError):
        pass
    try:
        parse_market_ticker("KXPALLADIUM15M-26SEP071415-15")
        raise AssertionError("Pyth metals must be refused")
    except (SeriesNotAllowedError, TickerParseError):
        pass


def test_window_id_from_utc_open_close_not_edt_title():
    mkt = parse_market(
        {
            "ticker": "KXBTC15M-26SEP071415-15",
            "event_ticker": "KXBTC15M-26SEP071400",
            "open_time": "2026-09-07T14:00:00Z",
            "close_time": "2026-09-07T14:15:00Z",
            "status": "active",
            "title": "Bitcoin price at Sep 7, 2026 at 10am EDT",
            "yes_ask_dollars": "0.5200",
            "yes_bid_dollars": "0.4800",
            "can_close_early": True,
        },
        event=EVENT,
    )
    assert mkt["window_id"] == "KXBTC15M-26SEP071400__2026-09-07T14:00:00Z__2026-09-07T14:15:00Z"
    assert mkt["et_title_display_only"] is True
    assert mkt["can_close_early"] is True
    assert "EDT" in mkt["title"]
    assert mkt["open_time"] == "2026-09-07T14:00:00Z"
    assert mkt["cf_index_id"] == "BRTI"
    assert mkt["cfb_ws_average_role"] == "observe_only"
    moved = window_id(
        event_ticker="KXBTC15M-26SEP071400",
        open_time="2026-09-07T14:00:00Z",
        close_time="2026-09-07T14:12:00Z",
    )
    assert moved != mkt["window_id"]
    assert moved.endswith("2026-09-07T14:12:00Z")


def test_initialized_null_mark_is_not_paper_candidate():
    initialized = parse_market(INITIALIZED_MARKET, event=EVENT)
    assert initialized["status"] == "initialized"
    assert initialized["is_open"] is False
    assert initialized["paper_mark"] is None
    assert initialized["yes_ask"] is None
    assert is_paper_autobet_candidate(initialized) is False
    open_m = parse_market(OPEN_MARKET, event=EVENT)
    assert open_m["is_open"] is True
    assert open_m["paper_mark"] is not None
    assert is_paper_autobet_candidate(open_m) is True


def test_parse_open_and_settled_market():
    open_m = parse_market(OPEN_MARKET, event=EVENT)
    assert open_m["is_open"] is True
    assert open_m["yes_ask"] == 0.52
    assert open_m["paper_mark"] == 0.50
    assert abs(open_m["decimal_odds"] - 2.0) < 1e-9
    assert open_m["result"] == ""
    assert open_m["trading_armed"] is False
    assert open_m["cf_index_id"] == CF_INDEX_ID == "BRTI"
    assert open_m["floor_strike"] is None
    assert open_m["display_only_prices"] is True
    settled = parse_market(SETTLED_MARKET, event=EVENT)
    assert settled["is_open"] is False
    assert settled["result"] == "yes"
    assert settled["source_is_cf_benchmarks"] is True
    assert settled["floor_strike"] == 79143.14
    assert settled["settlement_value_dollars"] == 1.0
    assert settled["expiration_value"] == "79177.08"
    assert settled["price_level_structure"] == "tapered_deci_cent"


def test_public_url_guard():
    assert_public_read_url(
        "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXBTC15M"
    )
    try:
        assert_public_read_url(
            "https://api.elections.kalshi.com/trade-api/v2/portfolio/orders"
        )
        raise AssertionError("orders must be refused")
    except PrivateEndpointRefused:
        pass
    try:
        assert_public_read_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXETH15M"
        )
        raise AssertionError("other series must be refused")
    except SeriesNotAllowedError:
        pass
    try:
        assert_public_read_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXBTC"
        )
        raise AssertionError("threshold KXBTC must be refused")
    except SeriesNotAllowedError:
        pass
    try:
        assert_public_read_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXPALLADIUM15M"
        )
        raise AssertionError("Pyth metals must be refused")
    except SeriesNotAllowedError:
        pass
    try:
        assert_public_read_url(
            "https://api.elections.kalshi.com/trade-api/v2/exchange/deposit"
        )
        raise AssertionError("deposit must be refused")
    except PrivateEndpointRefused:
        pass


def test_feed_fetch_uses_injected_payload(monkeypatch):
    feed = Kalshi15mFeed()
    urls: list[str] = []

    def fake_get(url, *, label, ttl_seconds, refresh):
        urls.append(url)
        if "/series/" in url:
            return {"series": {**SERIES, "volume_fp": "1234.0"}}
        if "/events" in url:
            return {"events": [EVENT]}
        if "status=open" in url:
            return {"markets": [OPEN_MARKET]}
        if "status=settled" in url:
            return {"markets": [SETTLED_MARKET]}
        return {"markets": [INITIALIZED_MARKET]}

    monkeypatch.setattr(feed, "_get", fake_get)
    payload, q = feed.fetch()
    assert payload["series"] == "KXBTC15M"
    assert payload["trading_armed"] is False
    assert any("/series/KXBTC15M?include_volume=true" in u for u in urls)
    assert any("/markets?" in u and "status=open" in u for u in urls)
    assert any("/markets?" in u and "status=settled" in u for u in urls)
    assert any("/events?" in u and "status=open" in u for u in urls)
    assert payload["series_meta"].get("volume") == 1234.0
    tickers = [m["ticker"] for m in payload["markets"]]
    assert OPEN_MARKET["ticker"] in tickers
    assert SETTLED_MARKET["ticker"] in tickers
    assert INITIALIZED_MARKET["ticker"] not in tickers
    assert payload["markets"][0]["source_is_cf_benchmarks"] is True
    assert q.source_kind == SourceKind.REAL_LIVE
    try:
        feed.fetch(series="KXETH15M")
        raise AssertionError("must not widen series")
    except SeriesNotAllowedError:
        pass
    assert payload["cf_index_id"] == "BRTI"
    assert payload["cfb_ws_average_role"] == CFB_WS_AVERAGE_ROLE == "observe_only"
    assert payload["fee_type"] == "quadratic"


def test_feed_prefers_open_over_initialized_default(monkeypatch):
    feed = Kalshi15mFeed()

    def fake_get(url, *, label, ttl_seconds, refresh):
        if "/series/" in url:
            return {"series": SERIES}
        if "/events" in url:
            return {"events": [EVENT]}
        if "status=open" in url:
            return {"markets": [OPEN_MARKET]}
        if "status=settled" in url:
            return {"markets": []}
        return {"markets": [INITIALIZED_MARKET]}

    monkeypatch.setattr(feed, "_get", fake_get)
    payload, _q = feed.fetch()
    assert [m["ticker"] for m in payload["markets"]] == [OPEN_MARKET["ticker"]]
    assert payload["markets"][0]["status"] == "active"
    assert is_paper_autobet_candidate(payload["markets"][0]) is True


def test_feed_skips_foreign_series_tickers(monkeypatch):
    feed = Kalshi15mFeed()

    def fake_get(url, *, label, ttl_seconds, refresh):
        if "/series/" in url:
            return {"series": SERIES}
        if "events" in url:
            return {
                "events": [
                    EVENT,
                    {"event_ticker": "KXBTC-26SEP071400", "series_ticker": "KXBTC"},
                    {"event_ticker": "KXETH15M-26SEP071400", "series_ticker": "KXETH15M"},
                ]
            }
        return {
            "markets": [
                OPEN_MARKET,
                {"ticker": "KXBTC-T1", "event_ticker": "KXBTC-26SEP071400", "status": "active"},
                {
                    "ticker": "KXPALLADIUM15M-26SEP071415-15",
                    "event_ticker": "KXPALLADIUM15M-26SEP071400",
                    "status": "active",
                },
            ]
        }

    monkeypatch.setattr(feed, "_get", fake_get)
    payload, _q = feed.fetch()
    assert [e["event_ticker"] for e in payload["events"]] == ["KXBTC15M-26SEP071400"]
    assert all(m["series_ticker"] == "KXBTC15M" for m in payload["markets"])
    assert all(not str(m["ticker"]).startswith("KXBTC-") for m in payload["markets"])


def test_public_mid_or_last():
    assert public_mid_or_last(yes_bid=0.40, yes_ask=0.50, last=0.42) == 0.45
    assert public_mid_or_last(yes_bid=None, yes_ask=0.50, last=0.42) == 0.42
    assert public_mid_or_last(yes_bid=None, yes_ask=0.50, last=None) == 0.50
