"""Frozen P-* library vs fill-all after fees. Search card, not an ADMIT."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from golf_offshoot.learning_lane_15m.evidence_bar import FEE_ADJUST_PATH, fee_adjust
from golf_offshoot.policy_family.express import express
from golf_offshoot.policy_family.library import (
    FROZEN_IDS,
    PolicyFamilyError,
    load_library,
    policy_by_id,
    policy_ids,
)
from golf_offshoot.policy_family.replay import replay, replay_family, run_search, write_lessons

PKG = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "policy_family"


def _window(
    *,
    posted_yes: float = 0.50,
    close_at: str = "2026-09-12T16:15:00-04:00",
    fill_at: str = "2026-09-12T16:01:00-04:00",
    recorded_pnl: float = 1.0,
    stake: float = 1.0,
    yes_bid=None,
    yes_ask=None,
    spread=None,
    quote_age_s=None,
    quote_fetched_at=None,
    quote_snapshot=None,
    last=None,
    last_price=None,
    last_price_dollars=None,
    quote_bus=None,
    window_id: str = "w",
) -> dict:
    row = {
        "window_id": window_id,
        "posted_yes": posted_yes,
        "close_at": close_at,
        "fill_at": fill_at,
        "decision_at": fill_at,
        "recorded_pnl": recorded_pnl,
        "stake": stake,
    }
    if yes_bid is not None:
        row["yes_bid"] = yes_bid
    if yes_ask is not None:
        row["yes_ask"] = yes_ask
    if spread is not None:
        row["spread"] = spread
    if quote_age_s is not None:
        row["quote_age_s"] = quote_age_s
    if quote_fetched_at is not None:
        row["quote_fetched_at"] = quote_fetched_at
    if quote_snapshot is not None:
        row["quote_snapshot"] = quote_snapshot
    if last is not None:
        row["last"] = last
    if last_price is not None:
        row["last_price"] = last_price
    if last_price_dollars is not None:
        row["last_price_dollars"] = last_price_dollars
    if quote_bus is not None:
        row["quote_bus"] = quote_bus
    return row


def test_library_loads_frozen_ids_in_file_order():
    ids = policy_ids()
    assert ids == FROZEN_IDS
    payload = load_library()
    assert payload["lab_admits"] is False
    assert payload["trading_armed"] is False
    assert payload["execution"] is False
    assert payload["series"] == "KXBTC15M"
    for row in payload["policies"]:
        assert row["side"] == "yes"
        assert "fill-no" not in json.dumps(row).lower()


def test_burned_honer_ids_refused(tmp_path):
    src = json.loads(
        (Path(__file__).resolve().parents[1] / "docs" / "POLICY_FAMILY.json").read_text(
            encoding="utf-8"
        )
    )
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True)
    for burned in ("FLIP", "PERSIST"):
        clone = json.loads(json.dumps(src))
        clone["policies"][0]["id"] = burned
        (docs / "POLICY_FAMILY.json").write_text(json.dumps(clone), encoding="utf-8")
        with pytest.raises(PolicyFamilyError, match="burned"):
            load_library(root=tmp_path)


def test_wide_missing_bid_ask_fills():
    policy = policy_by_id("P-SKIP-WIDE-0400")
    missing = express(policy, _window(posted_yes=0.50))
    assert missing["action"] == "fill"
    none_sides = express(policy, _window(posted_yes=0.50, yes_bid=None, yes_ask=None))
    assert none_sides["action"] == "fill"


def test_wide_spread_skip_and_fill():
    policy = policy_by_id("P-SKIP-WIDE-0400")
    skip = express(policy, _window(yes_bid=0.50, yes_ask=0.55))
    assert skip["action"] == "skip"
    fill = express(policy, _window(yes_bid=0.50, yes_ask=0.53))
    assert fill["action"] == "fill"
    assert express(policy, _window(spread=0.05))["action"] == "skip"
    assert express(policy, _window(spread=0.03))["action"] == "fill"


def test_stale_quote_180_skip_fill_missing_is_fill_not_thin_book():
    """Skip iff quote age > 180s. Missing age/snapshot fills. Not #200 thin-book."""
    policy = policy_by_id("P-SKIP-STALE-QUOTE-180")
    fill_at = "2026-09-12T16:01:00-04:00"
    assert express(policy, _window(quote_age_s=181, fill_at=fill_at))["action"] == "skip"
    assert express(policy, _window(quote_age_s=180, fill_at=fill_at))["action"] == "fill"
    assert express(policy, _window(quote_age_s=0, fill_at=fill_at))["action"] == "fill"
    assert express(policy, _window(fill_at=fill_at))["action"] == "fill"
    assert express(policy, _window(quote_snapshot={}, fill_at=fill_at))["action"] == "fill"
    missing_sides = express(
        policy, _window(quote_age_s=1, fill_at=fill_at, yes_bid=None, yes_ask=None)
    )
    assert missing_sides["action"] == "fill"
    assert (
        express(
            policy,
            _window(quote_fetched_at="2026-09-12T15:57:59-04:00", fill_at=fill_at),
        )["action"]
        == "skip"
    )
    assert (
        express(
            policy,
            _window(quote_fetched_at="2026-09-12T16:00:00-04:00", fill_at=fill_at),
        )["action"]
        == "fill"
    )


def test_stale_quote_skip_never_fires_is_untestable_not_a_retune():
    policy = policy_by_id("P-SKIP-STALE-QUOTE-180")
    windows = [_window(posted_yes=0.60, recorded_pnl=0.0, window_id=f"w{i}") for i in range(70)]
    card = replay(policy, windows)
    assert card["skip_count"] == 0
    assert card["card"] == "untestable"
    assert "retune 180" in card["lesson"]


def test_unless_cheap_040_fills_cheap_yes_only_missing_is_fill_not_thin_book():
    """Skip unless posted YES <= 0.40. 0.40 fills, 0.41 skips. Missing posted_yes fills."""
    policy = policy_by_id("P-SKIP-UNLESS-CHEAP-040")
    assert express(policy, _window(posted_yes=0.40))["action"] == "fill"
    assert express(policy, _window(posted_yes=0.0))["action"] == "fill"
    assert express(policy, _window(posted_yes=0.41))["action"] == "skip"
    missing = _window(posted_yes=0.50)
    del missing["posted_yes"]
    assert express(policy, missing)["action"] == "fill"
    none_mark = express(policy, _window(posted_yes=None))
    assert none_mark["action"] == "fill"
    coin = express(policy, _window(posted_yes=0.50))
    assert coin["action"] == "skip"
    rich = express(policy, _window(posted_yes=0.75))
    assert rich["action"] == "skip"
    assert express(policy_by_id("P-SKIP-RICH-075"), _window(posted_yes=0.50))["action"] == "fill"
    assert express(policy_by_id("P-SKIP-COINFLIP"), _window(posted_yes=0.45))["action"] == "fill"
    assert express(policy, _window(posted_yes=0.45))["action"] == "skip"


def test_unless_cheap_count_only_below_first_look_n():
    policy = policy_by_id("P-SKIP-UNLESS-CHEAP-040")
    windows = [_window(posted_yes=0.50, recorded_pnl=0.0, window_id=f"w{i}") for i in range(10)]
    card = replay(policy, windows)
    assert card["n"] == 10
    assert card["skip_count"] == 10
    assert card["card"] == "count_only"
    assert "first_look_n" in card["lesson"]
    assert "t-test" in card["lesson"]


def test_last_vs_mid_0200_skip_fill_missing_is_fill_not_thin_book():
    """Skip iff |last-mid| >= 0.02. Missing last or mid fills. Never posted_yes as last."""
    policy = policy_by_id("P-SKIP-LAST-VS-MID-0200")
    assert express(policy, _window(last=0.52, yes_bid=0.50, yes_ask=0.50))["action"] == "skip"
    assert express(policy, _window(last=0.519, yes_bid=0.50, yes_ask=0.50))["action"] == "fill"
    missing_last = express(policy, _window(yes_bid=0.50, yes_ask=0.52, posted_yes=0.90))
    assert missing_last["action"] == "fill"
    assert "missing last" in missing_last["reason"]
    missing_mid = express(policy, _window(last=0.40, posted_yes=0.90))
    assert missing_mid["action"] == "fill"
    assert "missing mid" in missing_mid["reason"]
    only_bid = express(policy, _window(last=0.40, yes_bid=0.50))
    assert only_bid["action"] == "fill"
    dollars = express(
        policy, _window(last_price_dollars=0.54, yes_bid=0.50, yes_ask=0.50)
    )
    assert dollars["action"] == "skip"
    nested = express(
        policy,
        _window(yes_bid=0.50, yes_ask=0.50, quote_bus={"last": 0.52}),
    )
    assert nested["action"] == "skip"
    bait = _window(posted_yes=0.90, yes_bid=0.50, yes_ask=0.52)
    assert "last" not in bait
    assert express(policy, bait)["action"] == "fill"
    for row in (
        _window(last=0.52, yes_bid=0.50, yes_ask=0.50),
        _window(last=0.50, yes_bid=0.50, yes_ask=0.50),
        bait,
    ):
        assert express(policy, row)["action"] in {"fill", "skip"}
        assert express(policy, row)["action"] != "fill_no"


def test_last_vs_mid_wide_spread_last_near_mid_fills_this_policy():
    """Distinct from P-SKIP-WIDE-0400. Last≈mid fills even when the spread is wide."""
    last_vs_mid = policy_by_id("P-SKIP-LAST-VS-MID-0200")
    wide = policy_by_id("P-SKIP-WIDE-0400")
    window = _window(posted_yes=0.525, yes_bid=0.50, yes_ask=0.55, last=0.525)
    assert express(wide, window)["action"] == "skip"
    assert express(last_vs_mid, window)["action"] == "fill"


def test_last_vs_mid_last_seconds_window_is_independent():
    """Distinct from P-SKIP-LAST-SECONDS-60. Time-to-close does not skip last-vs-mid."""
    last_vs_mid = policy_by_id("P-SKIP-LAST-VS-MID-0200")
    last_seconds = policy_by_id("P-SKIP-LAST-SECONDS-60")
    close = "2026-09-12T16:15:00-04:00"
    window = _window(
        close_at=close,
        fill_at="2026-09-12T16:14:01-04:00",
        last=0.50,
        yes_bid=0.50,
        yes_ask=0.50,
    )
    assert express(last_seconds, window)["action"] == "skip"
    assert express(last_vs_mid, window)["action"] == "fill"


def test_last_vs_mid_skip_never_fires_is_untestable_not_a_retune():
    policy = policy_by_id("P-SKIP-LAST-VS-MID-0200")
    windows = [_window(posted_yes=0.60, recorded_pnl=0.0, window_id=f"w{i}") for i in range(70)]
    card = replay(policy, windows)
    assert card["skip_count"] == 0
    assert card["card"] == "untestable"
    assert "retune 0.02" in card["lesson"]
    assert "retune 180" not in card["lesson"]


def test_q1_q2_still_on_the_tree_q3_is_file_order_after_q2():
    ids = policy_ids()
    assert ids == FROZEN_IDS
    assert "P-SKIP-STALE-QUOTE-180" in ids
    assert "P-SKIP-UNLESS-CHEAP-040" in ids
    assert ids[-1] == "P-SKIP-LAST-VS-MID-0200"
    assert ids[-2] == "P-SKIP-UNLESS-CHEAP-040"
    q1 = policy_by_id("P-SKIP-STALE-QUOTE-180")
    assert q1["params"]["max_age_s"] == 180
    q2 = policy_by_id("P-SKIP-UNLESS-CHEAP-040")
    assert q2["params"]["theta"] == 0.4
    q3 = policy_by_id("P-SKIP-LAST-VS-MID-0200")
    assert q3["params"]["delta"] == 0.02
    assert q3["side"] == "yes"
    assert q3["declared_at"] == "2026-09-12T20:40:00-04:00"


def test_rich_075_boundary():
    policy = policy_by_id("P-SKIP-RICH-075")
    assert express(policy, _window(posted_yes=0.75))["action"] == "skip"
    assert express(policy, _window(posted_yes=0.749))["action"] == "fill"


def test_coinflip_band_is_exclusive():
    policy = policy_by_id("P-SKIP-COINFLIP")
    assert express(policy, _window(posted_yes=0.50))["action"] == "skip"
    assert express(policy, _window(posted_yes=0.451))["action"] == "skip"
    assert express(policy, _window(posted_yes=0.549))["action"] == "skip"
    assert express(policy, _window(posted_yes=0.45))["action"] == "fill"
    assert express(policy, _window(posted_yes=0.55))["action"] == "fill"


def test_last_seconds_and_ineligible_closed():
    last = policy_by_id("P-SKIP-LAST-SECONDS-60")
    closed = policy_by_id("P-SKIP-INELIGIBLE-CLOSED")
    close = "2026-09-12T16:15:00-04:00"
    assert (
        express(last, _window(close_at=close, fill_at="2026-09-12T16:14:01-04:00"))["action"]
        == "skip"
    )
    assert (
        express(last, _window(close_at=close, fill_at="2026-09-12T16:14:00-04:00"))["action"]
        == "fill"
    )
    assert (
        express(closed, _window(close_at=close, fill_at="2026-09-12T16:15:00-04:00"))["action"]
        == "skip"
    )
    assert (
        express(closed, _window(close_at=close, fill_at="2026-09-12T16:14:00-04:00"))["action"]
        == "fill"
    )


def test_replay_uses_fee_adjust_skip_is_zero_no_fill_no():
    policy_skip = policy_by_id("P-SKIP-COINFLIP")
    policy_fill = policy_by_id("P-FILL-ALL-YES")
    windows = [_window(posted_yes=0.50, recorded_pnl=1.0, stake=1.0)]
    skip_card = replay(policy_skip, windows)
    fill_card = replay(policy_fill, windows)
    assert skip_card["fee_adjust"] == FEE_ADJUST_PATH
    assert skip_card["skip_count"] == 1
    assert skip_card["fee_adj_pnl"] == 0.0
    assert skip_card["windows"][0]["pnl_policy_fee_adj"] == fee_adjust(
        None, None, None, filled=False
    )
    expected_fill = fee_adjust(1.0, 0.50, 1.0, filled=True)
    assert fill_card["fee_adj_pnl"] == expected_fill
    assert fill_card["windows"][0]["action"] == "fill"
    for card in (skip_card, fill_card):
        for row in card["windows"]:
            assert row["action"] in {"fill", "skip"}
            assert row["action"] != "fill_no"


def test_density_fail_on_n70_is_not_a_ttest(monkeypatch):
    def boom(*_a, **_k):
        raise AssertionError("density-fail is not a t-test vs δ")

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.rules.paired_t_against_floor",
        boom,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.rules.matched_exposure_permutation",
        boom,
    )
    policy = policy_by_id("P-SKIP-RICH-075")
    windows = [_window(posted_yes=0.75, window_id=f"s{i}") for i in range(9)]
    windows.extend(_window(posted_yes=0.50, window_id=f"f{i}") for i in range(61))
    card = replay(policy, windows)
    assert card["n"] == 70
    assert card["skip_count"] == 9
    assert card["density_fail"] is True
    assert card["undecidable"] is True
    assert card["card"] == "density_fail"
    assert "t-test" in card["lesson"]
    assert "clause_1_paired_t_vs_floor" not in card


def test_package_does_not_import_farm_honer_or_write_rules():
    for path in PKG.glob("*.py"):
        src = path.read_text(encoding="utf-8")
        assert "golf_offshoot.honer_15m" not in src
        assert "golf_offshoot.learning_lane_15m.farm" not in src
        assert "consult_honer" not in src
        assert "HONER-FAMILY-AMEND" not in src
        assert "paired_t_against_floor" not in src
        assert "open(" not in src or "RULES.json" not in src


def test_policies_are_independent_not_skip_together():
    """A coinflip skip can still be a rich fill. Not factory skip-together. Not 3^N."""
    mid = _window(posted_yes=0.50, yes_bid=0.49, yes_ask=0.51)
    assert express(policy_by_id("P-SKIP-COINFLIP"), mid)["action"] == "skip"
    assert express(policy_by_id("P-SKIP-RICH-075"), mid)["action"] == "fill"
    assert express(policy_by_id("P-SKIP-UNLESS-CHEAP-040"), mid)["action"] == "skip"
    assert express(policy_by_id("P-SKIP-WIDE-0400"), mid)["action"] == "fill"
    near = _window(posted_yes=0.50, yes_bid=0.49, yes_ask=0.51, last=0.50)
    assert express(policy_by_id("P-SKIP-LAST-VS-MID-0200"), near)["action"] == "fill"
    cards = replay_family([mid])
    assert [c["id"] for c in cards] == list(FROZEN_IDS)
    assert len(cards) == len(FROZEN_IDS)


def test_lessons_write_density_fail_row(tmp_path):
    policy = policy_by_id("P-SKIP-LAST-SECONDS-60")
    windows = [
        _window(
            posted_yes=0.60,
            recorded_pnl=0.0,
            close_at="2026-09-12T16:15:00-04:00",
            fill_at="2026-09-12T16:01:00-04:00",
            window_id=f"w{i}",
        )
        for i in range(70)
    ]
    card = replay(policy, windows)
    assert card["skip_count"] == 0
    assert card["density_fail"] is True
    dest = write_lessons([card], root=tmp_path)
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["lab_admits"] is False
    assert payload["trading_armed"] is False
    assert payload["rows"][0]["density_fail"] is True
    assert payload["rows"][0]["lesson"]


def test_run_search_on_fixture_books_does_not_write_rules(tmp_path):
    paper = tmp_path / "paper"
    paper.mkdir()
    (paper / "ledger.json").write_text("{}", encoding="utf-8")
    book = {
        "tournament_id": "KXBTC15M-26SEP121600__2026-09-12T19:45:00Z__2026-09-12T20:00:00Z",
        "settled_at": "2026-09-12T16:01:00-04:00",
        "settlement_pnl": 0.5,
        "settlement_winner": "kalshi:yes",
        "book": {
            "positions": [
                {
                    "player_id": "KXBTC15M-26SEP121600-00",
                    "entry_market_p": 0.60,
                }
            ]
        },
        "movements": [
            {
                "kind": "new_bet",
                "at": "2026-09-12T15:46:00-04:00",
                "player_id": "KXBTC15M-26SEP121600-00",
                "stake_after": 1.0,
                "model_win": 0.60,
                "reason_technical": "paper_mark=0.60 yes_bid=0.59 yes_ask=0.61",
            }
        ],
    }
    (
        paper
        / "KXBTC15M-26SEP121600__2026-09-12T19-45-00Z__2026-09-12T20-00-00Z.json"
    ).write_text(json.dumps(book), encoding="utf-8")
    rules_before = (
        Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_RULES.json"
    ).read_text(encoding="utf-8")
    out = run_search(paper_dir=paper, dest_root=tmp_path, write=True)
    assert out["n"] == 1
    assert len(out["cards"]) == len(FROZEN_IDS)
    after = (
        Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_RULES.json"
    ).read_text(encoding="utf-8")
    assert after == rules_before
    assert (tmp_path / "golf-offshoot" / "docs" / "P_FAMILY_LESSONS.json").is_file()
    assert (
        tmp_path
        / "golf-offshoot"
        / "data"
        / "learning_lane_15m"
        / "latest"
        / "policy_family_score.json"
    ).is_file()


def test_gather_carries_last_from_existing_fields_never_posted_yes(tmp_path):
    from golf_offshoot.policy_family.replay import gather_lineage_a_windows

    paper = tmp_path / "paper"
    paper.mkdir()
    book = {
        "tournament_id": "KXBTC15M-26SEP121600__2026-09-12T19:45:00Z__2026-09-12T20:00:00Z",
        "settled_at": "2026-09-12T16:01:00-04:00",
        "settlement_pnl": 0.5,
        "settlement_winner": "kalshi:yes",
        "book": {
            "positions": [
                {
                    "player_id": "KXBTC15M-26SEP121600-00",
                    "entry_market_p": 0.60,
                }
            ]
        },
        "movements": [
            {
                "kind": "new_bet",
                "at": "2026-09-12T15:46:00-04:00",
                "player_id": "KXBTC15M-26SEP121600-00",
                "stake_after": 1.0,
                "model_win": 0.60,
                "reason_technical": "paper_mark=0.60 yes_bid=0.59 yes_ask=0.61 last=0.40",
            }
        ],
    }
    (
        paper
        / "KXBTC15M-26SEP121600__2026-09-12T19-45-00Z__2026-09-12T20-00-00Z.json"
    ).write_text(json.dumps(book), encoding="utf-8")
    windows = gather_lineage_a_windows(paper)
    assert len(windows) == 1
    assert windows[0]["posted_yes"] == 0.60
    assert windows[0]["last"] == 0.40
    assert windows[0]["yes_bid"] == 0.59
    assert windows[0]["yes_ask"] == 0.61
    policy = policy_by_id("P-SKIP-LAST-VS-MID-0200")
    assert express(policy, windows[0])["action"] == "skip"
    book["movements"][0]["reason_technical"] = "paper_mark=0.60 yes_bid=0.59 yes_ask=0.61"
    (
        paper
        / "KXBTC15M-26SEP121600__2026-09-12T19-45-00Z__2026-09-12T20-00-00Z.json"
    ).write_text(json.dumps(book), encoding="utf-8")
    missing = gather_lineage_a_windows(paper)
    assert missing[0]["last"] is None
    assert missing[0]["posted_yes"] == 0.60
    assert express(policy, missing[0])["action"] == "fill"


def _seed_family_docs(tmp_path, *, lessons_rows=None, rule_ids=None):
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    src_docs = Path(__file__).resolve().parents[1] / "docs"
    (docs / "POLICY_FAMILY.json").write_text(
        (src_docs / "POLICY_FAMILY.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    burned = src_docs / "LEARNING_LANE_15M_BURNED_CLASSES.json"
    (docs / "LEARNING_LANE_15M_BURNED_CLASSES.json").write_text(
        burned.read_text(encoding="utf-8"), encoding="utf-8"
    )
    if lessons_rows is not None:
        (docs / "P_FAMILY_LESSONS.json").write_text(
            json.dumps({"rows": lessons_rows}), encoding="utf-8"
        )
    if rule_ids is not None:
        (docs / "LEARNING_LANE_15M_RULES.json").write_text(
            json.dumps({"rules": [{"id": ident} for ident in rule_ids]}),
            encoding="utf-8",
        )


def test_picker_file_order_unused_named_not_3n(tmp_path):
    from golf_offshoot.policy_family.picker import (
        MONEY_KEYS,
        next_named_from_files,
        picker_owed_from_files,
        stamp_picker,
        unused_named_from_files,
    )

    _seed_family_docs(tmp_path, lessons_rows=[], rule_ids=[])
    unused = unused_named_from_files(root=tmp_path)
    assert "P-FILL-ALL-YES" not in unused
    assert unused[0] == "P-SKIP-COINFLIP"
    assert unused == [
        "P-SKIP-COINFLIP",
        "P-SKIP-RICH-075",
        "P-SKIP-WIDE-0400",
        "P-SKIP-LAST-SECONDS-60",
        "P-SKIP-INELIGIBLE-CLOSED",
        "P-SKIP-STALE-QUOTE-180",
        "P-SKIP-UNLESS-CHEAP-040",
        "P-SKIP-LAST-VS-MID-0200",
    ]
    assert len(unused) == 8
    assert next_named_from_files(root=tmp_path) == "P-SKIP-COINFLIP"
    assert picker_owed_from_files(root=tmp_path) is True
    stamp = stamp_picker(root=tmp_path)
    assert stamp["kind"] == "P-FAMILY-SEARCH"
    assert stamp["owed"] is True
    assert stamp["next"] == "P-SKIP-COINFLIP"
    assert stamp["ping_lab"] is False
    assert stamp["lab_admits"] is False
    assert stamp["trading_armed"] is False
    assert stamp["reasons"] == ["unused_named"]
    assert "third_family" not in stamp
    for key in MONEY_KEYS:
        assert key not in stamp


def test_picker_retires_density_fail_and_does_not_confuse_factory_coinflip(tmp_path):
    from golf_offshoot.policy_family.picker import (
        next_named_from_files,
        unused_named_from_files,
    )

    _seed_family_docs(
        tmp_path,
        lessons_rows=[
            {"id": "P-FILL-ALL-YES", "card": "comparison_book"},
            {"id": "P-SKIP-COINFLIP", "card": "beats_fill_all"},
            {"id": "P-SKIP-RICH-075", "card": "park_vs_fill_all"},
            {"id": "P-SKIP-WIDE-0400", "card": "density_fail"},
            {"id": "P-SKIP-LAST-SECONDS-60", "card": "density_fail"},
            {"id": "P-SKIP-INELIGIBLE-CLOSED", "card": "density_fail"},
            {"id": "P-SKIP-STALE-QUOTE-180", "card": "untestable"},
            {"id": "P-SKIP-UNLESS-CHEAP-040", "card": "park_vs_fill_all"},
            {"id": "P-SKIP-LAST-VS-MID-0200", "card": "untestable"},
        ],
        rule_ids=["R-SKIP-COINFLIP", "R-BASELINE-FILL-ALL"],
    )
    unused = unused_named_from_files(root=tmp_path)
    assert unused == ["P-SKIP-COINFLIP"]
    assert next_named_from_files(root=tmp_path) == "P-SKIP-COINFLIP"
    _seed_family_docs(
        tmp_path,
        lessons_rows=[
            {"id": "P-FILL-ALL-YES", "card": "comparison_book"},
            {"id": "P-SKIP-COINFLIP", "card": "beats_fill_all"},
            {"id": "P-SKIP-RICH-075", "card": "park_vs_fill_all"},
            {"id": "P-SKIP-WIDE-0400", "card": "density_fail"},
            {"id": "P-SKIP-LAST-SECONDS-60", "card": "density_fail"},
            {"id": "P-SKIP-INELIGIBLE-CLOSED", "card": "density_fail"},
            {"id": "P-SKIP-STALE-QUOTE-180", "card": "untestable"},
            {"id": "P-SKIP-UNLESS-CHEAP-040", "card": "park_vs_fill_all"},
            {"id": "P-SKIP-LAST-VS-MID-0200", "card": "untestable"},
        ],
        rule_ids=["P-SKIP-COINFLIP"],
    )
    assert unused_named_from_files(root=tmp_path) == []
    assert next_named_from_files(root=tmp_path) is None


def test_live_files_leave_coinflip_unused_until_exact_p_id():
    from golf_offshoot.policy_family.picker import (
        next_named_from_files,
        picker_owed_from_files,
        retired_named_from_files,
        unused_named_from_files,
    )

    unused = unused_named_from_files()
    assert unused == ["P-SKIP-COINFLIP", "P-SKIP-UNLESS-CHEAP-040"]
    assert next_named_from_files() == "P-SKIP-COINFLIP"
    assert picker_owed_from_files() is True
    retired = retired_named_from_files()
    assert "P-SKIP-COINFLIP" not in retired
    assert "P-SKIP-UNLESS-CHEAP-040" not in retired
    assert "P-SKIP-LAST-VS-MID-0200" in retired
    assert "P-SKIP-RICH-075" in retired
    assert "P-SKIP-WIDE-0400" in retired
    assert "P-SKIP-STALE-QUOTE-180" in retired
    assert "P-FILL-ALL-YES" not in unused
    assert "P-FILL-ALL-YES" not in retired


def test_catalog_kind_is_not_a_farm_slot(tmp_path):
    from golf_offshoot.learning_lane_15m.evidence_bar import load_mechanism_catalog
    from golf_offshoot.learning_lane_15m.farm import unused_legal_kinds

    kinds = load_mechanism_catalog()["kinds"]
    pkind = next(row for row in kinds if row["id"] == "P-FAMILY-SEARCH")
    assert pkind.get("legal_now") is not True
    assert pkind.get("legal_only_when")
    would_farm = dict(pkind)
    would_farm["legal_now"] = True
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True)
    (docs / "LEARNING_LANE_15M_MECHANISM_CATALOG.json").write_text(
        json.dumps({"kinds": [would_farm]}), encoding="utf-8"
    )
    (docs / "LEARNING_LANE_15M_FARM.json").write_text('{"notebooks": []}', encoding="utf-8")
    (docs / "LEARNING_LANE_15M_RULES.json").write_text('{"rules": []}', encoding="utf-8")
    (docs / "LEARNING_LANE_15M_BURNED_CLASSES.json").write_text(
        '{"classes": []}', encoding="utf-8"
    )
    assert unused_legal_kinds(root=tmp_path) == []
    live_unused = unused_legal_kinds(
        root=tmp_path,
        catalog=load_mechanism_catalog(),
        farm={"notebooks": []},
        registry={"rules": []},
    )
    assert all(slot["kind"] != "P-FAMILY-SEARCH" for slot in live_unused)
