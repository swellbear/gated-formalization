from golf_offshoot.data_feeds.bovada import winner_outcome_names
from golf_offshoot.data_feeds.field_fallback import (
    attach_history_ids,
    field_quality,
    is_provisional_player_id,
    is_skip_field_name,
    provisional_player_id,
    stub_competitor,
)
from golf_offshoot.data_feeds.polymarket import winner_outcome_names as pm_winner_names
from golf_offshoot.models.enums import DataRole, SourceKind


def test_skip_other_and_field():
    assert is_skip_field_name("Other") is True
    assert is_skip_field_name("The Field") is True
    assert is_skip_field_name("Scottie Scheffler") is False


def test_provisional_id_is_not_espn():
    pid = provisional_player_id("Scottie Scheffler")
    assert pid == "name:scottie-scheffler"
    assert is_provisional_player_id(pid)
    assert not is_provisional_player_id("4240")


def test_attach_history_ids_recovers_espn_and_skips_other():
    hist = {"scottie scheffler": "4240", "tommy fleetwood": "101"}
    attached = attach_history_ids(
        ["Scottie Scheffler", "Other", "Nobody In Field", "Tommy Fleetwood"],
        hist,
    )
    by_name = {nm: (pid, ok) for nm, pid, ok in attached}
    assert by_name["Scottie Scheffler"] == ("4240", True)
    assert by_name["Tommy Fleetwood"] == ("101", True)
    assert "Other" not in by_name
    nobody_id, ok = by_name["Nobody In Field"]
    assert ok is False
    assert nobody_id.startswith("name:")


def test_stub_competitor_has_no_live_board():
    comp = stub_competitor("Scottie Scheffler", "4240")
    assert comp["athlete"]["id"] == "4240"
    assert comp["athlete"]["displayName"] == "Scottie Scheffler"
    assert "WITHDRAW" not in str(comp.get("status"))


def test_field_quality_provisional_not_espn():
    q = field_quality(
        n=50,
        source_name="bovada_outright_names",
        history_matched=48,
        notes="provisional field from bovada_outright_names",
        provisional=True,
    )
    assert q.source_name == "bovada_outright_names"
    assert q.source_kind == SourceKind.DERIVED_FROM_REAL
    assert q.role == DataRole.FALLBACK
    assert "not an official ESPN field" in q.notes
    assert "48/50" in q.notes


def test_bovada_winner_names_skip_top10_and_other():
    events = [
        {
            "displayGroups": [
                {
                    "markets": [
                        {
                            "description": "Winner",
                            "outcomes": [
                                {"description": "Scottie Scheffler"},
                                {"description": "Other"},
                                {"description": "Tommy Fleetwood"},
                            ],
                        },
                        {
                            "description": "Top 10 Finish",
                            "outcomes": [{"description": "Should Not Appear"}],
                        },
                    ]
                }
            ]
        }
    ]
    assert winner_outcome_names(events) == ["Scottie Scheffler", "Tommy Fleetwood"]


def test_polymarket_winner_names_skip_other():
    events = [
        {
            "markets": [
                {
                    "groupItemTitle": "Scottie Scheffler",
                    "question": "Will Scottie Scheffler win the 2026 BMW Championship?",
                    "sportsMarketType": "moneyline",
                    "closed": False,
                },
                {
                    "groupItemTitle": "Other",
                    "question": "Will Other win the 2026 BMW Championship?",
                    "sportsMarketType": "moneyline",
                    "negRiskOther": True,
                    "closed": False,
                },
            ]
        }
    ]
    assert pm_winner_names(events) == ["Scottie Scheffler"]
