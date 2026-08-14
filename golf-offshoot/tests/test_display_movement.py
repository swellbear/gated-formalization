from datetime import datetime, timezone
from pathlib import Path

from golf_offshoot.audit.journal import build_audit, latest_pre_audit, save_audit
from golf_offshoot.models.enums import Horizon, RunMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore
from golf_offshoot.ranking.display import format_table, movement_note


def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    lo = max(0.0, central - 0.01)
    hi = min(1.0, central + 0.01)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(pid: str, name: str, rank: int, win: float) -> PlayerOutput:
    horizons = {
        Horizon.WIN: _hp(Horizon.WIN, win),
        Horizon.TOP_5: _hp(Horizon.TOP_5, min(1.0, win * 3)),
        Horizon.TOP_10: _hp(Horizon.TOP_10, min(1.0, win * 5)),
        Horizon.TOP_20: _hp(Horizon.TOP_20, min(1.0, win * 8)),
        Horizon.MAKE_CUT: _hp(Horizon.MAKE_CUT, 1.0),
    }
    bundle = ProbabilityBundle(player_id=pid, horizons=horizons, theta_mean=0.0, theta_sd=1.0)
    rel = ReliabilityScore(
        player_id=pid,
        score=0.7,
        data_density=0.5,
        data_quality=0.5,
        input_stability=0.5,
    )
    return PlayerOutput(player_id=pid, name=name, rank=rank, probabilities=bundle, reliability=rel)


def test_format_table_omits_movement_without_baseline():
    live = [_row("kita", "Kurt Kitayama", 3, 0.089)]
    text = format_table(live, n=1)
    assert "dWin" not in text
    assert "dRnk" not in text
    assert "Column index" in text
    assert "never auto-bets" in text


def test_format_table_movement_signs():
    pre = [
        _row("kita", "Kurt Kitayama", 18, 0.016),
        _row("fade", "Faded Name", 2, 0.120),
    ]
    live = [
        _row("kita", "Kurt Kitayama", 3, 0.089),
        _row("fade", "Faded Name", 10, 0.040),
        _row("new", "New In Field", 12, 0.030),
    ]
    text = format_table(live, n=3, baseline=pre)
    kita = [ln for ln in text.splitlines() if "Kitayama" in ln][0]
    fade = [ln for ln in text.splitlines() if "Faded" in ln][0]
    new = [ln for ln in text.splitlines() if "New" in ln][0]
    assert "+0.073" in kita
    assert "   18" in kita
    assert "  +15" in kita
    assert "-0.080" in fade
    assert "    2" in fade
    assert "   -8" in fade
    assert "n/a" in new
    assert "dWin" in text.splitlines()[0]
    assert "Pre#" in text.splitlines()[0]
    assert "dRnk" in text.splitlines()[0]
    assert "Column index" in text
    assert any(ln.strip().startswith("dWin") for ln in text.splitlines())


def test_movement_note_ascii():
    assert "Delta" not in movement_note("abc")
    assert "opening-line" in movement_note("abc")
    assert "ingest first" in movement_note(None)


def test_latest_pre_audit_skips_live_and_other_events(tmp_path: Path):
    older = build_audit("401811962", RunMode.PRE_TOURNAMENT, [], "h-old")
    newer = build_audit("401811962", RunMode.PRE_TOURNAMENT, [], "h-new")
    live = build_audit("401811962", RunMode.LIVE, [], "h-live")
    other = build_audit("other-event", RunMode.PRE_TOURNAMENT, [], "h-other")
    older.as_of = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    newer.as_of = datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc)
    live.as_of = datetime(2026, 8, 13, 18, 0, tzinfo=timezone.utc)
    save_audit(older, tmp_path)
    save_audit(newer, tmp_path)
    save_audit(live, tmp_path)
    save_audit(other, tmp_path)
    (tmp_path / "junk.json").write_text("{not audit}", encoding="utf-8")
    got = latest_pre_audit("401811962", tmp_path)
    assert got is not None
    assert got.run_id == newer.run_id
    assert latest_pre_audit("missing", tmp_path) is None
