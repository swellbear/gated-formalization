from golf_offshoot.data_feeds.hardrock import (
    HardRockBetOddsFeed,
    resolve_odds_book,
)
from golf_offshoot.models.enums import BetType, SourceKind


def test_resolve_odds_book_aliases():
    assert resolve_odds_book("hardrock") == "hardrockbet"
    assert resolve_odds_book("hard rock bet") == "hardrockbet"
    assert resolve_odds_book("bovada") == "bovada"
    assert resolve_odds_book("auto") == "auto"
    assert resolve_odds_book("") == "auto"


def test_hardrock_parser_uses_pinned_book_and_drops_unmatched():
    payload = [
        {
            "id": "ev-stjude",
            "sport_key": "golf_pga_tour",
            "sport_title": "FedEx St. Jude Championship",
            "bookmakers": [
                {
                    "key": "draftkings",
                    "markets": [
                        {
                            "key": "outrights",
                            "outcomes": [{"name": "Scottie Scheffler", "price": 4.0}],
                        }
                    ],
                },
                {
                    "key": "hardrockbet",
                    "markets": [
                        {
                            "key": "outrights",
                            "outcomes": [
                                {"name": "Scottie Scheffler", "price": 8.5},
                                {"name": "Nobody In Field", "price": 101.0},
                                {"name": "Tommy Fleetwood", "price": 12.0},
                            ],
                        }
                    ],
                },
            ],
        }
    ]
    feed = HardRockBetOddsFeed(api_key="unused-in-parse")
    quotes, unmatched, book = feed._parse_quotes(
        payload,
        {"Scottie Scheffler": "id-ss", "Tommy Fleetwood": "id-tf"},
        "FedEx St. Jude Championship",
    )
    assert book == "hardrockbet"
    assert unmatched == 1
    by = {q.player_id: q for q in quotes}
    assert set(by) == {"id-ss", "id-tf"}
    assert by["id-ss"].decimal_odds == 8.5
    assert by["id-ss"].book == "hardrockbet"
    assert by["id-ss"].bet_type == BetType.WIN
    assert by["id-ss"].implied_raw == 1.0 / 8.5
    assert all(q.line_role == "current" for q in quotes)


def test_hardrock_does_not_average_state_skins():
    payload = [
        {
            "id": "ev-stjude",
            "sport_title": "FedEx St. Jude Championship",
            "bookmakers": [
                {
                    "key": "hardrockbet_fl",
                    "markets": [
                        {"key": "outrights", "outcomes": [{"name": "Scottie Scheffler", "price": 9.0}]}
                    ],
                },
                {
                    "key": "hardrockbet",
                    "markets": [
                        {"key": "outrights", "outcomes": [{"name": "Scottie Scheffler", "price": 7.0}]}
                    ],
                },
            ],
        }
    ]
    feed = HardRockBetOddsFeed(api_key="unused-in-parse")
    quotes, unmatched, book = feed._parse_quotes(
        payload, {"Scottie Scheffler": "id-ss"}, "FedEx St. Jude Championship"
    )
    assert unmatched == 0
    assert book == "hardrockbet"
    assert quotes[0].decimal_odds == 7.0


def test_hardrock_does_not_invent_when_only_other_books_present():
    payload = [
        {
            "id": "ev-stjude",
            "sport_title": "FedEx St. Jude Championship",
            "bookmakers": [
                {
                    "key": "bovada",
                    "markets": [
                        {"key": "outrights", "outcomes": [{"name": "Scottie Scheffler", "price": 5.5}]}
                    ],
                }
            ],
        }
    ]
    feed = HardRockBetOddsFeed(api_key="unused-in-parse")
    quotes, unmatched, book = feed._parse_quotes(
        payload, {"Scottie Scheffler": "id-ss"}, "FedEx St. Jude Championship"
    )
    assert quotes == []
    assert unmatched == 0
    assert book == ""


def test_hardrock_openings_are_not_bovada_opens(tmp_path):
    from datetime import datetime, timezone

    from golf_offshoot.data_feeds.openings import merge_archived_openings, persist_prematch_openings
    from golf_offshoot.models.schemas import MarketQuote

    bovada = MarketQuote(
        player_id="id-ss",
        bet_type=BetType.WIN,
        decimal_odds=9.0,
        implied_raw=1.0 / 9.0,
        book="bovada",
        as_of=datetime.now(timezone.utc),
        line_role="current",
    )
    persist_prematch_openings("401811962", "St Jude", [bovada], directory=tmp_path, book_family="bovada")
    live = MarketQuote(
        player_id="id-ss",
        bet_type=BetType.WIN,
        decimal_odds=8.5,
        implied_raw=1.0 / 8.5,
        book="hardrockbet",
        as_of=datetime.now(timezone.utc),
        line_role="current",
    )
    merged = merge_archived_openings([live], "401811962", directory=tmp_path, book_family="hardrockbet")
    assert len(merged) == 1
    assert merged[0].book == "hardrockbet"
    assert merged[0].line_role == "current"


def test_hardrock_missing_key_is_unavailable_not_mocked():
    feed = HardRockBetOddsFeed(api_key="")
    quotes, q = feed.fetch(name_to_id={"Scottie Scheffler": "id-ss"}, tournament_name="St Jude")
    assert quotes == []
    assert q.missing is True
    assert q.source_kind == SourceKind.UNAVAILABLE
    assert "Bovada" in q.notes
    assert q.source_kind != SourceKind.MOCK
