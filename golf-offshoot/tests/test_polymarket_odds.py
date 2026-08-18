from golf_offshoot.data_feeds.hardrock import resolve_odds_book
from golf_offshoot.data_feeds.polymarket import (
    PolymarketOddsFeed,
    classify_market,
    quotes_from_event,
    slug_candidates,
    winner_outcome_names,
    yes_price,
)
from golf_offshoot.models.enums import BetType


def test_resolve_odds_book_polymarket():
    assert resolve_odds_book("polymarket") == "polymarket"
    assert resolve_odds_book("auto") != "polymarket"
    assert resolve_odds_book("bovada") == "bovada"


def test_slug_candidates_bmw():
    slugs = slug_candidates("BMW Championship", year=2026)
    assert "2026-bmw-championship-winner" in slugs
    assert "2026-bmw-championship-first-round-leader" in slugs
    assert "2026-bmw-championship-top10" not in slugs


def test_classify_polymarket_questions():
    assert classify_market("Will Scottie Scheffler win the 2026 BMW Championship?", sports_type="moneyline") == BetType.WIN
    assert classify_market("Will Scottie Scheffler finish top 10 at the BMW Championship?") == BetType.TOP_10
    assert classify_market("Will Scottie Scheffler win after round 1 of the 2026 BMW Championship?") == BetType.WIN_AFTER_R1
    assert classify_market("BMW Championship End of Round 1 Leader") == BetType.WIN_AFTER_R1
    assert classify_market("BMW Championship End of Round 2 Leader") == BetType.WIN_AFTER_R2
    assert classify_market("BMW Championship End of Round 3 Leader") == BetType.WIN_AFTER_R3
    assert classify_market("BMW Championship Winner", sports_type="futures") == BetType.WIN
    assert classify_market("Will Scottie Scheffler lead the 2026 BMW Championship following the second round?") == BetType.WIN_AFTER_R2
    assert classify_market("Will Scottie Scheffler lead the 2026 BMW Championship following the third round?") == BetType.WIN_AFTER_R3
    assert classify_market("Will Scottie Scheffler finish in the Top 10 at the 2026 BMW Championship?") == BetType.TOP_10
    assert classify_market(
        "Will Scottie Scheffler win the 2026 BMW Championship?",
        sports_type="moneyline",
        context="PGA Tour: BMW Championship Top 10",
    ) == BetType.WIN
    assert classify_market(
        "Scottie Scheffler",
        sports_type="moneyline",
        context="BMW Championship First Round Leader",
    ) == BetType.WIN_AFTER_R1
    assert classify_market(
        "Keith Mitchell",
        sports_type="moneyline",
        context="2026-bmw-championship-top10",
    ) == BetType.TOP_10
    assert classify_market("Round 1 2-ball") is None


def test_yes_price_prefers_ask():
    assert yes_price({"bestAsk": 0.05, "outcomePrices": '["0.035", "0.965"]'}) == 0.05
    assert yes_price({"bestAskQuote": {"value": "0.2260", "currency": "USD"}}) == 0.226
    assert yes_price({"bestAsk": 1.0, "outcomePrices": '["0.12", "0.88"]'}) == 0.12
    assert yes_price({"bestAsk": 0.0}) is None


def test_yes_book_caps_skip_juiced_place_cards():
    from golf_offshoot.market.odds import yes_ask_sum, yes_book_is_ticketable

    assert yes_book_is_ticketable(BetType.WIN, 2.59) is True
    assert yes_book_is_ticketable(BetType.TOP_10, 25.76) is False
    assert yes_book_is_ticketable(BetType.WIN_AFTER_R1, 16.65) is False
    assert abs(yes_ask_sum([10.0] * 50) - 5.0) < 1e-9


def test_quotes_match_espn_names_and_skip_other():
    event = {
        "title": "PGA Tour: BMW Championship Winner",
        "slug": "2026-bmw-championship-winner",
        "markets": [
            {
                "groupItemTitle": "Scottie Scheffler",
                "question": "Will Scottie Scheffler win the 2026 BMW Championship?",
                "sportsMarketType": "moneyline",
                "bestAsk": 0.20,
                "outcomePrices": '["0.18", "0.82"]',
                "closed": False,
            },
            {
                "groupItemTitle": "Other",
                "question": "Will Other win the 2026 BMW Championship?",
                "sportsMarketType": "moneyline",
                "negRiskOther": True,
                "bestAsk": 0.04,
                "closed": False,
            },
            {
                "groupItemTitle": "Nobody In Field",
                "question": "Will Nobody In Field win the 2026 BMW Championship?",
                "sportsMarketType": "moneyline",
                "bestAsk": 0.03,
                "closed": False,
            },
        ],
    }
    quotes, unmatched, _seen = quotes_from_event(
        event,
        {"Scottie Scheffler": "id-ss", "Tommy Fleetwood": "id-tf"},
    )
    assert unmatched == 2
    assert len(quotes) == 1
    q = quotes[0]
    assert q.player_id == "id-ss"
    assert q.book == "polymarket"
    assert q.bet_type == BetType.WIN
    assert q.implied_raw == 0.20
    assert q.decimal_odds == 5.0
    assert q.line_role == "current"


def test_polymarket_does_not_synthesize_top10_from_winner():
    event = {
        "title": "PGA Tour: BMW Championship Winner",
        "markets": [
            {
                "groupItemTitle": "Scottie Scheffler",
                "question": "Will Scottie Scheffler win the 2026 BMW Championship?",
                "sportsMarketType": "moneyline",
                "bestAsk": 0.20,
                "closed": False,
            }
        ],
    }
    quotes, _um, _seen = quotes_from_event(event, {"Scottie Scheffler": "id-ss"})
    assert [q.bet_type for q in quotes] == [BetType.WIN]


def test_polymarket_paper_file_is_not_lived():
    from golf_offshoot.strategy.paper_book import paper_book_path

    assert paper_book_path("401811963").name == "401811963.json"
    assert paper_book_path("401811963", "polymarket").name == "401811963_polymarket.json"


def test_polymarket_pack_is_not_bovada_batch(tmp_path):
    from golf_offshoot.strategy.paper_pack import write_polymarket_pack

    root = write_polymarket_pack(
        event_id="401811963",
        event_name="BMW Championship",
        run_id="run-a",
        directory=tmp_path,
    )
    assert root.name.endswith("_polymarket")
    assert "_batch" not in root.name
    readme = (root / "00_README.txt").read_text(encoding="utf-8")
    assert "Polymarket" in readme
    assert "Bovada" in readme


def test_polymarket_pack_writes_bankroll_page(tmp_path, monkeypatch):
    from golf_offshoot.models.enums import BetType
    from golf_offshoot.models.strategy import PortfolioState, StrategyPosition
    from golf_offshoot.strategy.paper_bankroll_export import independent_ledger_from_book
    from golf_offshoot.strategy.paper_book import PaperBookFile
    from golf_offshoot.strategy.paper_pack import _pack_pdf_sources, write_polymarket_pack

    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250.0,
        starting_bankroll=250.0,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(
            bankroll=250.0,
            positions=[
                StrategyPosition(
                    position_id="p-fitz",
                    player_id="fitz",
                    player_name="Matt Fitzpatrick",
                    bet_type=BetType.WIN,
                    stake=2.19,
                    decimal_odds=29.41,
                    entry_edge=0.023,
                    entry_model_p=0.036,
                    user_recorded=True,
                )
            ],
        ),
    )
    led = independent_ledger_from_book(rec)
    assert led.starting_bankroll == 250.0
    assert led.deposits == 250.0
    assert led.bankroll == 250.0
    assert led.betting_pnl == 0.0
    assert any(e.kind == "deposit" for e in led.entries)
    assert "ledger.json" in led.entries[0].note
    root = write_polymarket_pack(
        event_id="401811963",
        event_name="BMW Championship",
        run_id="run-bank",
        directory=tmp_path,
        record=rec,
    )
    assert (root / "05_bankroll.pdf").is_file()
    assert (root / "05_bankroll.pdf").read_bytes().startswith(b"%PDF")
    txt = (root / "05_bankroll.txt").read_text(encoding="utf-8")
    assert "Independent polymarket" in txt
    assert "ledger.json" in txt
    assert "Matt Fitzpatrick" in txt
    assert "current $250.00" in txt.lower() or "Current $250.00" in txt or "current $250.00" in txt
    leftover = (root / "04_leftover.txt").read_text(encoding="utf-8")
    assert "round-leader leftover" in leftover or "tee/wave" in leftover
    assert "paper-fill" in leftover
    assert "rerun live" in leftover
    assert (root / "04_leftover.pdf").is_file()
    tickets = (root / "01_paper_tickets.txt").read_text(encoding="utf-8")
    assert "[observation]" in tickets
    assert "tracking tickets, not fills" in tickets
    names = [p.name for p, _ in _pack_pdf_sources(root)]
    assert names[-1] == "05_bankroll.pdf"
    assert "04_leftover.pdf" in names
    assert names.index("04_leftover.pdf") < names.index("05_bankroll.pdf")


def test_polymarket_deposit_does_not_write_lived_ledger(tmp_path, monkeypatch):
    from golf_offshoot.models.enums import BetType
    from golf_offshoot.models.strategy import PortfolioState, StrategyPosition
    from golf_offshoot.strategy.paper_book import PaperBookFile, load_paper_file, save_paper_book
    from golf_offshoot.strategy.paper_ledger import ledger_path, record_deposit

    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250.0,
        starting_bankroll=250.0,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(
            bankroll=250.0,
            positions=[
                StrategyPosition(
                    position_id="p-fitz",
                    player_id="fitz",
                    player_name="Matt Fitzpatrick",
                    bet_type=BetType.WIN,
                    stake=2.19,
                    decimal_odds=29.41,
                    entry_edge=0.023,
                    entry_model_p=0.036,
                    user_recorded=True,
                )
            ],
        ),
    )
    save_paper_book(rec)
    led = record_deposit(50, note="add cash", event_id="401811963", path_id="polymarket")
    assert led.bankroll == 300.0
    assert led.deposits == 300.0
    assert led.betting_pnl == 0.0
    assert not ledger_path("lived").is_file()
    assert ledger_path("polymarket").is_file()
    rec2 = load_paper_file("401811963", path_id="polymarket")
    assert rec2 is not None
    assert rec2.bankroll == 300.0


def test_polymarket_pack_pre_tee_does_not_print_stale_sell(tmp_path, monkeypatch):
    from golf_offshoot.models.enums import BetType
    from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id
    from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement
    from golf_offshoot.strategy.paper_pack import _pack_pdf_sources, write_polymarket_pack

    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path)
    rec = PaperBookFile(
        tournament_id="401811963",
        tournament_name="BMW Championship",
        bankroll=250.0,
        starting_bankroll=250.0,
        odds_book="polymarket",
        path_id="polymarket",
        independent_bankroll=True,
        book=PortfolioState(
            bankroll=250.0,
            positions=[
                StrategyPosition(
                    position_id="p-cole",
                    player_id="cole",
                    player_name="Eric Cole",
                    bet_type=BetType.WIN,
                    stake=2.19,
                    decimal_odds=125.0,
                    entry_edge=0.007,
                    entry_model_p=0.01,
                    user_recorded=True,
                )
            ],
        ),
        latest_advice=[
            PaperMovement(
                movement_id=new_id("mv"),
                kind="exit",
                status="advised",
                player_name="Eric Cole",
                bet_type="win",
                stake_delta=-2.19,
                reason_plain="Original edge has collapsed.",
            )
        ],
    )
    extra = tmp_path / "03_zzz_extra.pdf"
    extra.write_bytes(b"%PDF-1.4\n%\n")
    root = write_polymarket_pack(
        event_id="401811963",
        event_name="BMW Championship",
        run_id="run-stale",
        directory=tmp_path,
        record=rec,
        extra_files=[extra],
    )
    trigger = (root / "00_trigger.txt").read_text(encoding="utf-8")
    assert "SELL" not in trigger
    assert "HOLD" in trigger
    assert "has not started" in trigger.lower()
    names = [p.name for p, _ in _pack_pdf_sources(root)]
    assert names[-1] == "05_bankroll.pdf"


def test_quotes_round_leader_is_not_win():
    event = {
        "title": "BMW Championship Win After Round 1",
        "slug": "2026-bmw-championship-win-after-round-1",
        "markets": [
            {
                "groupItemTitle": "Scottie Scheffler",
                "question": "Will Scottie Scheffler win after round 1 of the 2026 BMW Championship?",
                "sportsMarketType": "moneyline",
                "bestAsk": 0.08,
                "closed": False,
            }
        ],
    }
    quotes, _um, _seen = quotes_from_event(event, {"Scottie Scheffler": "id-ss"})
    assert len(quotes) == 1
    assert quotes[0].bet_type == BetType.WIN_AFTER_R1
    assert winner_outcome_names([event]) == []


def test_quotes_skip_closed_event_and_untradable_books():
    closed = {
        "title": "BMW Championship Top 10",
        "slug": "2026-bmw-championship-top10",
        "closed": True,
        "markets": [
            {
                "groupItemTitle": "Keith Mitchell",
                "question": "Will Keith Mitchell finish in the Top 10 at the 2026 BMW Championship?",
                "bestAsk": 0.10,
                "closed": False,
            }
        ],
    }
    quotes, unmatched, seen = quotes_from_event(closed, {"Keith Mitchell": "id-km"})
    assert quotes == []
    assert unmatched == 0
    assert seen == []
    blocked = {
        "title": "BMW Championship Winner",
        "slug": "2026-bmw-championship-winner",
        "closed": False,
        "markets": [
            {
                "groupItemTitle": "Scottie Scheffler",
                "question": "Will Scottie Scheffler win the 2026 BMW Championship?",
                "bestAsk": 0.20,
                "enableOrderBook": False,
                "closed": False,
            }
        ],
    }
    quotes, unmatched, _seen = quotes_from_event(blocked, {"Scottie Scheffler": "id-ss"})
    assert quotes == []


def test_discover_keeps_round_leader_cards():
    winner = {
        "id": "81983",
        "slug": "pga-bmwcham-2026-08-20-w",
        "title": "BMW Championship Winner",
        "closed": False,
        "endDate": "2026-08-23T23:59:00Z",
        "markets": [
            {
                "title": "Scottie Scheffler",
                "question": "BMW Championship Winner",
                "sportsMarketType": "futures",
                "bestAskQuote": {"value": "0.2260", "currency": "USD"},
                "closed": False,
                "status": "MARKET_STATUS_OPEN",
            }
        ],
    }
    round1 = {
        "id": "82914",
        "slug": "pga-bmwcham-2026-08-20-r1l",
        "title": "BMW Championship End of Round 1 Leader",
        "closed": False,
        "endDate": "2026-08-23T23:59:00Z",
        "markets": [
            {
                "title": "Scottie Scheffler",
                "question": "BMW Championship End of Round 1 Leader",
                "sportsMarketType": "futures",
                "bestAskQuote": {"value": "0.0840", "currency": "USD"},
                "closed": False,
                "status": "MARKET_STATUS_OPEN",
            }
        ],
    }
    intl_top10 = {
        "id": "gamma-top10",
        "slug": "2026-bmw-championship-top10",
        "title": "PGA Tour: BMW Championship Top 10",
        "closed": False,
        "endDate": "2026-08-23T23:59:00Z",
        "markets": [
            {
                "title": "Keith Mitchell",
                "question": "Will Keith Mitchell finish in the Top 10 at the 2026 BMW Championship?",
                "bestAsk": 0.10,
                "closed": False,
            }
        ],
    }
    lpga = {
        "id": "84821",
        "slug": "lpga-cpkcwome-2026-08-20-w",
        "title": "CPKC Women's Open Winner",
        "closed": False,
        "endDate": "2026-08-23T23:59:00Z",
        "markets": [
            {
                "title": "Nelly Korda",
                "question": "CPKC Women's Open Winner",
                "bestAskQuote": {"value": "0.20", "currency": "USD"},
                "closed": False,
                "status": "MARKET_STATUS_OPEN",
            }
        ],
    }
    feed = PolymarketOddsFeed()
    feed._golf_futures_events = lambda **_kw: [winner, round1, lpga]
    found = feed._discover_events("BMW Championship", ttl_seconds=1.0, refresh=False)
    slugs = {ev["slug"] for ev in found}
    assert winner["slug"] in slugs
    assert round1["slug"] in slugs
    assert lpga["slug"] not in slugs
    feed._golf_futures_events = lambda **_kw: [intl_top10]
    assert feed._discover_events("BMW Championship", ttl_seconds=1.0, refresh=False) == []


def test_quotes_from_us_gateway_payload():
    event = {
        "title": "BMW Championship Winner",
        "slug": "pga-bmwcham-2026-08-20-w",
        "markets": [
            {
                "title": "Scottie Scheffler",
                "titleShort": "Scottie Scheffler",
                "question": "BMW Championship Winner",
                "sportsMarketType": "futures",
                "bestAskQuote": {"value": "0.2260", "currency": "USD"},
                "bestBidQuote": {"value": "0.2220", "currency": "USD"},
                "closed": False,
                "status": "MARKET_STATUS_OPEN",
            }
        ],
    }
    quotes, unmatched, seen = quotes_from_event(event, {"Scottie Scheffler": "id-ss"})
    assert unmatched == 0
    assert quotes[0].bet_type == BetType.WIN
    assert quotes[0].implied_raw == 0.226
    assert quotes[0].bid_raw == 0.222
    assert seen == ["pga-bmwcham-2026-08-20-w"]


def test_discover_skips_closed_prior_year():
    old = {
        "id": "ev-old",
        "slug": "pga-bmwcham-2025-08-14-w",
        "title": "BMW Championship Winner",
        "closed": True,
        "endDate": "2025-08-18T00:00:00Z",
        "markets": [
            {
                "title": "Scottie Scheffler",
                "question": "BMW Championship Winner",
                "bestAskQuote": {"value": "0.20", "currency": "USD"},
                "closed": False,
                "status": "MARKET_STATUS_OPEN",
            }
        ],
    }
    live = {
        "id": "81983",
        "slug": "pga-bmwcham-2026-08-20-w",
        "title": "BMW Championship Winner",
        "closed": False,
        "endDate": "2026-08-23T23:59:00Z",
        "markets": [
            {
                "title": "Scottie Scheffler",
                "question": "BMW Championship Winner",
                "bestAskQuote": {"value": "0.20", "currency": "USD"},
                "closed": False,
                "status": "MARKET_STATUS_OPEN",
            }
        ],
    }
    feed = PolymarketOddsFeed()
    feed._golf_futures_events = lambda **_kw: [old, live]
    found = feed._discover_events("BMW Championship", ttl_seconds=1.0, refresh=False)
    slugs = {ev["slug"] for ev in found}
    assert live["slug"] in slugs
    assert old["slug"] not in slugs
