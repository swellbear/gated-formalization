import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.consult_honer import compose_and_skip, express_frozen_honer
from golf_offshoot.learning_lane_15m.paper import consult_registry, load_decisions, paper_autobet_open_markets
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, set_15m_root_override
from golf_offshoot.learning_lane_15m.rules import decide


FACTORY_FILL = {
    "rule_id": "R-SKIP-2TO1-FAVORITE",
    "action": "fill",
    "reason": "factory fill",
    "eligible": True,
    "execution": True,
}
FACTORY_SKIP = {
    "rule_id": "R-SKIP-2TO1-FAVORITE",
    "action": "skip",
    "reason": "factory skip",
    "eligible": True,
    "execution": True,
}
SRC = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot"


def test_compose_dark_missing_snapshot_returns_same_object():
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=None)
    assert out is FACTORY_FILL
    assert out["action"] == "fill"
    assert "consult" not in out


def test_compose_enabled_false_does_not_skip():
    snap = {"consult_enabled": False, "family": "H-SKIP-RICH-YES", "theta": 0.10}
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=snap)
    assert out is FACTORY_FILL
    assert out["action"] == "fill"


def test_compose_string_true_is_not_enabled():
    snap = {"consult_enabled": "true", "family": "H-SKIP-RICH-YES", "theta": 0.10}
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=snap)
    assert out is FACTORY_FILL


def test_and_skip_factory_skip_stays_skip():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES", "theta": 0.99}
    out = compose_and_skip(FACTORY_SKIP, posted_yes=0.40, snapshot=snap)
    assert out is FACTORY_SKIP
    assert out["action"] == "skip"
    assert out["reason"] == "factory skip"


def test_and_skip_honer_skip_wins_on_factory_fill():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES", "theta": 0.75}
    out = compose_and_skip(dict(FACTORY_FILL), posted_yes=0.80, snapshot=snap)
    assert out["action"] == "skip"
    assert "honer consult" in out["reason"]
    assert out["consult"] == "honer_and_skip"
    assert FACTORY_FILL["action"] == "fill"


def test_and_skip_honer_fill_keeps_factory_fill():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES", "theta": 0.90}
    base = dict(FACTORY_FILL)
    out = compose_and_skip(base, posted_yes=0.50, snapshot=snap)
    assert out is base
    assert out["action"] == "fill"


def test_spread_family_skips_wide_book():
    snap = {
        "consult_enabled": True,
        "family": "H-SKIP-WIDE-SPREAD",
        "theta": 0.99,
        "delta": 0.03,
    }
    out = compose_and_skip(dict(FACTORY_FILL), posted_yes=0.40, spread=0.05, snapshot=snap)
    assert out["action"] == "skip"
    action, _reason = express_frozen_honer(snap, posted_yes=0.40, spread=0.01)
    assert action == "fill"


def test_thin_book_consult_skip_when_enabled_snapshot():
    snap = {
        "consult_enabled": True,
        "family": "H-SKIP-THIN-BOOK",
        "theta": 0.90,
        "delta": 0.04,
        "gamma": 0.01,
    }
    missing = compose_and_skip(dict(FACTORY_FILL), posted_yes=0.40, spread=None, snapshot=snap)
    assert missing["action"] == "skip"
    assert "thin quotes" in missing["reason"]
    tight = compose_and_skip(dict(FACTORY_FILL), posted_yes=0.40, spread=0.00, snapshot=snap)
    assert tight["action"] == "skip"
    assert "gamma" in tight["reason"]
    action, _reason = express_frozen_honer(snap, posted_yes=0.40, spread=0.05)
    assert action == "fill"


def test_freeze_hash_omits_gamma_when_absent():
    from golf_offshoot.learning_lane_15m.consult_honer import freeze_hash

    family1 = {
        "frozen_family": "H-SKIP-RICH-YES",
        "frozen_theta": 0.81,
        "declared_at": "2026-09-09T15:44:00-04:00",
    }
    assert "gamma" not in family1
    assert freeze_hash(family1) == freeze_hash(dict(family1))
    with_gamma = dict(family1)
    with_gamma["frozen_gamma"] = 0.01
    assert freeze_hash(with_gamma) != freeze_hash(family1)


def test_consult_registry_dark_matches_decide(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        rule = {
            "id": "R-SKIP-2TO1-FAVORITE",
            "declared_at": "2026-09-08T16:53:00-04:00",
            "kind": "selection",
            "selects": True,
            "execution": True,
            "params": {"favorite_odds": 2},
        }
        decided = decide(rule, posted_yes=0.50, close_at="2026-09-08T17:00:00-04:00")
        composed = consult_registry(
            rule, posted_yes=0.50, close_at="2026-09-08T17:00:00-04:00"
        )
        assert composed == decided
    finally:
        set_15m_root_override(None)


def test_paper_autobet_ignores_live_honer_theta_when_consult_off(tmp_path, monkeypatch):
    from golf_offshoot.data_feeds.kalshi_15m import parse_event, parse_market
    from golf_offshoot.honer_15m.paths import set_honer_root_override

    event = {
        "event_ticker": "KXBTC15M-26SEP071400",
        "series_ticker": "KXBTC15M",
        "title": "BTC 15 min",
        "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
    }
    open_raw = {
        "ticker": "KXBTC15M-26SEP071415-15",
        "event_ticker": "KXBTC15M-26SEP071415",
        "status": "active",
        "result": "",
        "yes_ask_dollars": "0.4000",
        "yes_bid_dollars": "0.3800",
        "title": "BTC price up in next 15 mins?",
    }
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_honer_root_override(tmp_path / "honer_15m")
    try:
        latest = latest_dir_15m()
        (latest / "honer_consult.json").write_text(
            json.dumps(
                {
                    "consult_enabled": False,
                    "family": "H-SKIP-RICH-YES",
                    "theta": 0.10,
                    "delta": 0.0,
                }
            ),
            encoding="utf-8",
        )
        honer_latest = tmp_path / "honer_15m" / "latest"
        honer_latest.mkdir(parents=True, exist_ok=True)
        (honer_latest / "theta.json").write_text(
            json.dumps({"theta": 0.10}), encoding="utf-8"
        )
        rule = {
            "id": "R-SKIP-2TO1-FAVORITE",
            "declared_at": "2026-09-08T16:53:00-04:00",
            "kind": "selection",
            "selects": True,
            "execution": True,
            "params": {"favorite_odds": 2},
        }
        market = parse_market(open_raw, event=parse_event(event))
        fills = paper_autobet_open_markets([market], rule=rule)
        assert len(fills) == 1
        assert load_decisions()[market["ticker"]]["action"] == "fill"
        assert "consult" not in load_decisions()[market["ticker"]]
    finally:
        set_15m_root_override(None)
        set_honer_root_override(None)


def test_enabled_missing_theta_returns_factory_verdict():
    snap = {"consult_enabled": True, "family": "H-SKIP-RICH-YES"}
    out = compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=snap)
    assert out is FACTORY_FILL
    assert out["action"] == "fill"


def test_write_consult_candidate_stays_dark(tmp_path):
    from golf_offshoot.learning_lane_15m.consult_honer import write_consult_candidate

    dest = tmp_path / "honer_consult.json"
    snap = write_consult_candidate(
        {
            "frozen_family": "H-SKIP-RICH-YES",
            "frozen_theta": 0.81,
            "frozen_delta": 0.04,
            "declared_at": "2026-09-10T14:00:00-04:00",
        },
        dest=dest,
        consult_enabled=False,
    )
    assert snap["consult_enabled"] is False
    assert snap["live_theta_never_consults"] is True
    assert "theta.json" not in str(snap.get("source") or "")
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["consult_enabled"] is False
    assert compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=payload) is FACTORY_FILL


def test_enable_gates_fail_without_surviving_score(tmp_path):
    from golf_offshoot.learning_lane_15m.consult_honer import (
        consult_enable_gates,
        write_consult_candidate,
    )

    exam = {
        "frozen_family": "H-SKIP-RICH-YES",
        "frozen_theta": 0.81,
        "frozen_delta": 0.04,
        "declared_at": "2026-09-10T14:00:00-04:00",
    }
    snap = write_consult_candidate(exam, dest=tmp_path / "honer_consult.json")
    gates = consult_enable_gates(
        exam=exam,
        score={},
        honer_bar={"fee_omitted": True},
        snapshot=snap,
        invariants={"passed": False},
    )
    by_id = {g["id"]: g["ok"] for g in gates}
    assert by_id["fee_apply"] is False
    assert by_id["exam_not_dead"] is False
    assert by_id["honer_invariants"] is False
    assert all(g.get("ok") for g in gates) is False


def test_maybe_sync_does_not_enable_without_score(tmp_path, monkeypatch):
    from golf_offshoot.learning_lane_15m import consult_honer as ch

    exam = {
        "open": True,
        "frozen_family": "H-SKIP-RICH-YES",
        "frozen_theta": 0.81,
        "frozen_delta": 0.04,
        "declared_at": "2026-09-10T14:00:00-04:00",
    }
    monkeypatch.setattr(ch, "load_honer_exam", lambda: exam)
    monkeypatch.setattr(ch, "load_honer_exam_score", lambda: {})
    dest = tmp_path / "honer_consult.json"
    out = ch.maybe_sync_and_enable(dest=dest)
    assert out["wrote_candidate"] is True
    assert out["consult_enabled"] is False
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["consult_enabled"] is False
    assert compose_and_skip(FACTORY_FILL, posted_yes=0.90, snapshot=payload) is FACTORY_FILL


def test_factory_paper_and_rules_do_not_import_honer_package():
    paper = (SRC / "learning_lane_15m" / "paper.py").read_text(encoding="utf-8")
    rules = (SRC / "learning_lane_15m" / "rules.py").read_text(encoding="utf-8")
    consult = (SRC / "learning_lane_15m" / "consult_honer.py").read_text(encoding="utf-8")
    assert "golf_offshoot.honer_15m" not in paper
    assert "golf_offshoot.honer_15m" not in rules
    assert "golf_offshoot.honer_15m" not in consult
    assert "theta.json" not in consult or "Never reads" in consult
    assert "R-SKIP-HOUR-CLOSE" not in consult


FEE_SHA = "a" * 64
EXAM = {
    "frozen_family": "H-SKIP-RICH-YES",
    "frozen_theta": 0.81,
    "frozen_delta": 0.04,
    "declared_at": "2026-09-10T14:00:00-04:00",
}
SURVIVING_SCORE = {"outcome": "completed_unscored", "survives": True}
LIVE_BAR = {
    "fee_omitted": False,
    "honer_fee_apply": {"schedule_sha256": FEE_SHA},
}


def _seated(rule_id: str, *, execution: bool = True) -> dict:
    return {"id": rule_id, "selects": True, "execution": execution}


def _write_l1(root, rule_id: str, *, passes: bool) -> Path:
    dest = (
        root
        / "golf-offshoot"
        / "docs"
        / f"LEARNING_LANE_15M_SCORECARD_{rule_id}_L1.json"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps({"passes_every_binding_clause": passes}),
        encoding="utf-8",
    )
    return dest


def _gate_ok(gates, gate_id: str) -> bool:
    by_id = {g["id"]: g["ok"] for g in gates}
    return bool(by_id[gate_id])


def test_enable_refused_while_seated_first_70_open(tmp_path):
    from golf_offshoot.learning_lane_15m.consult_honer import (
        consult_enable_gates,
        write_consult_candidate,
    )

    snap = write_consult_candidate(EXAM, dest=tmp_path / "honer_consult.json")
    gates = consult_enable_gates(
        exam=EXAM,
        score=SURVIVING_SCORE,
        honer_bar=LIVE_BAR,
        snapshot=snap,
        invariants={"passed": True},
        executing=_seated("R-SKIP-HOUR-CLOSE"),
        root=tmp_path,
    )
    assert _gate_ok(gates, "exam_not_dead") is True
    assert _gate_ok(gates, "executing_l1_closed") is False
    assert _gate_ok(gates, "executing_is_keeper") is False
    assert all(g.get("ok") for g in gates) is False


def test_enable_refused_when_seated_l1_failed_or_execution_dropped(tmp_path):
    from golf_offshoot.learning_lane_15m.consult_honer import (
        consult_enable_gates,
        write_consult_candidate,
    )

    snap = write_consult_candidate(EXAM, dest=tmp_path / "honer_consult.json")
    _write_l1(tmp_path, "R-SKIP-HOUR-CLOSE", passes=False)
    failed = consult_enable_gates(
        exam=EXAM,
        score=SURVIVING_SCORE,
        honer_bar=LIVE_BAR,
        snapshot=snap,
        invariants={"passed": True},
        executing=_seated("R-SKIP-HOUR-CLOSE"),
        root=tmp_path,
    )
    assert _gate_ok(failed, "executing_l1_closed") is True
    assert _gate_ok(failed, "executing_is_keeper") is False

    _write_l1(tmp_path, "R-SKIP-HOUR-CLOSE", passes=True)
    dropped = consult_enable_gates(
        exam=EXAM,
        score=SURVIVING_SCORE,
        honer_bar=LIVE_BAR,
        snapshot=snap,
        invariants={"passed": True},
        executing=_seated("R-SKIP-HOUR-CLOSE", execution=False),
        root=tmp_path,
    )
    assert _gate_ok(dropped, "executing_is_keeper") is False
    assert all(g.get("ok") for g in dropped) is False


def test_enable_allowed_for_keeper_and_surviving_freeze(tmp_path, monkeypatch):
    from golf_offshoot.learning_lane_15m import consult_honer as ch

    monkeypatch.setattr(ch, "load_honer_exam", lambda: EXAM)
    dest = tmp_path / "honer_consult.json"
    _write_l1(tmp_path, "R-SKIP-HOUR-CLOSE", passes=True)
    out = ch.maybe_sync_and_enable(
        dest=dest,
        score=SURVIVING_SCORE,
        honer_bar=LIVE_BAR,
        invariants={"passed": True},
        executing=_seated("R-SKIP-HOUR-CLOSE"),
        root=tmp_path,
    )
    assert out["consult_enabled"] is True
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["consult_enabled"] is True
    assert dest == tmp_path / "honer_consult.json"


def test_enable_gates_same_for_non_hour_id(tmp_path):
    from golf_offshoot.learning_lane_15m.consult_honer import (
        consult_enable_gates,
        write_consult_candidate,
    )

    snap = write_consult_candidate(EXAM, dest=tmp_path / "honer_consult.json")
    _write_l1(tmp_path, "R-SKIP-CIVIL-BOUNDARIES", passes=True)
    gates = consult_enable_gates(
        exam=EXAM,
        score=SURVIVING_SCORE,
        honer_bar=LIVE_BAR,
        snapshot=snap,
        invariants={"passed": True},
        executing=_seated("R-SKIP-CIVIL-BOUNDARIES"),
        root=tmp_path,
    )
    by_id = {g["id"]: g["ok"] for g in gates}
    assert by_id["executing_l1_closed"] is True
    assert by_id["executing_is_keeper"] is True
    assert all(g.get("ok") for g in gates) is True


def test_leash_scores_then_enables(monkeypatch):
    from golf_offshoot.learning_lane_15m.leash import run_leash_tick

    order: list[str] = []

    def score():
        order.append("score")
        return {"wrote": False}

    def look_push():
        order.append("look_push")
        return {"pushed": False, "reason": "unarmed"}

    def fetch():
        order.append("fetch")
        return {"ok": True}

    def observe():
        order.append("observe")
        return {"ok": True, "dropped": []}

    def farm():
        order.append("farm")
        return {"wrote": False}

    def farm_menu():
        order.append("farm_menu")
        return {"dated": [], "seat_required": False}

    def enable():
        order.append("enable")
        return {"consult_enabled": False}

    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.maybe_score_executing",
        score,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.look_push.maybe_push_look",
        look_push,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.sibling_sync.maybe_fetch_origin_farm",
        fetch,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.sibling_sync.maybe_observe_sibling_execution",
        observe,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.clerical_score.maybe_score_farm",
        farm,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.farm.run_farm_menu",
        farm_menu,
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.consult_honer.maybe_sync_and_enable",
        enable,
    )
    out = run_leash_tick()
    assert order == [
        "score",
        "look_push",
        "fetch",
        "observe",
        "farm",
        "farm_menu",
        "enable",
    ]
    assert out["clerical_score"]["wrote"] is False
    assert out["farm"]["wrote"] is False
    assert out["farm_menu"]["seat_required"] is False
    assert out["consult"]["consult_enabled"] is False

