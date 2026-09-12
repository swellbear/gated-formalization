"""hub-1: 15m shell glance residual wording. Display only. Trading NOT ARMED."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

from golf_offshoot.learning_lane_15m.learn import MISSING_JOIN_BANNER
from golf_offshoot.learning_lane_15m.paper import save_book
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, set_15m_root_override
from golf_offshoot.models.strategy import PortfolioState
from golf_offshoot.operator_surface.app import (
    GLANCE_NO_PNL,
    GLANCE_ROLES_REQUEST,
    build_surface,
    render_html,
)
from golf_offshoot.operator_surface.runner import OperatorSafetyError, refuse_forbidden
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement

JOINED = "KXBTC15M-26SEP071545-45"
JOINED_EVENT = "KXBTC15M-26SEP071545"
OLDER_JOIN = "KXBTC15M-26SEP071530-30"
OLDER_EVENT = "KXBTC15M-26SEP071530"
PENDING = "KXBTC15M-26SEP071900-00"
MISSING = "KXBTC15M-26SEP071500-00"
LINEAGE_B = "KXBTC15M-26SEP071445-45"
LINEAGE_B_PNL = "+1.67"
THIS_BOOK_PNL = 0.42
OLDER_BOOK_PNL = 0.10

APP_PY = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "operator_surface" / "app.py"


def _attr(page: str, name: str, kind: str) -> str:
    match = re.search(
        rf'<{name}[^>]*data-kind="{re.escape(kind)}"[^>]*>(.*?)</{name}>',
        page,
        flags=re.DOTALL,
    )
    assert match, f"missing {name} data-kind={kind}"
    return match.group(0)


def _glance(page: str) -> str:
    start = page.index('<div class="glance" id="glance-15m">')
    lin = page.index('data-kind="lineage"', start)
    end = page.index("</div>", page.index("</p>", lin))
    return page[start : end + len("</div>")]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _book(*, event: str, ticker: str, settled_at, pnl) -> None:
    rec = PaperBookFile(
        tournament_id=event,
        tournament_name=event,
        bankroll=100.0,
        book=PortfolioState(bankroll=100.0, session_label="learning_lane_15m"),
        paper_observation_only=True,
        never_auto_bet=True,
        settled_at=settled_at,
        settlement_pnl=pnl,
        movements=[
            PaperMovement(
                movement_id=f"mv-{ticker}",
                kind="new_bet",
                player_id=ticker,
                player_name="YES",
            )
        ],
    )
    save_book(rec)


def _wake(*, pending: str, missing: str, roles: list[str]) -> None:
    _write_json(
        latest_dir_15m() / "learning_wake.json",
        {
            "lane": "learning_lane_15m",
            "roles_owed": [{"role": role} for role in roles],
            "scan": {
                "pending": [
                    {
                        "ticker": pending,
                        "window_id": pending.rsplit("-", 1)[0],
                        "kind": "awaiting_kalshi_result",
                    }
                ],
                "paper_join_missing": [
                    {
                        "ticker": missing,
                        "official_result": "yes",
                        "paper_book_on_tree": False,
                        "paper_pnl": None,
                        "state": "official result present; paper book not on this tree",
                    }
                ],
                "published_only": [
                    {
                        "ticker": LINEAGE_B,
                        "paper_outcome": "paper_win",
                        "published_paper_pnl": LINEAGE_B_PNL,
                    }
                ],
            },
        },
    )


def _watch(*, running: bool) -> None:
    _write_json(
        latest_dir_15m() / "watch.json",
        {
            "lane": "learning_lane_15m",
            "running": running,
            "cycles": 4,
            "last_ok": True,
            "last_summary": "pending=1",
        },
    )


@pytest.fixture()
def lane(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        yield tmp_path
    finally:
        set_15m_root_override(None)


def _page(tmp_path: Path, *, lane: str = "learning_lane_15m") -> str:
    return render_html(
        build_surface(
            artifact_root=tmp_path,
            viz_root=tmp_path / "viz",
            lane=lane,
        )
    )


def test_glance_is_above_the_fold_with_watch_on(lane, tmp_path):
    _watch(running=True)
    _wake(pending=PENDING, missing=MISSING, roles=["digestor"])
    _book(
        event=JOINED_EVENT,
        ticker=JOINED,
        settled_at=datetime(2026, 9, 7, 16, 0, tzinfo=timezone.utc),
        pnl=THIS_BOOK_PNL,
    )
    page = _page(tmp_path)
    assert page.index('id="glance-15m"') < page.index("Charts first")
    assert page.index("WATCH ON") < page.index("Charts first")
    assert page.index("WATCH ON") < page.index("What you can do here")
    glance = _glance(page)
    assert 'data-watch="on"' in glance
    assert "WATCH OFF" not in glance


def test_settle_pending_is_not_the_missing_paper_join(lane, tmp_path):
    _watch(running=True)
    _wake(pending=PENDING, missing=MISSING, roles=["operator"])
    page = _page(tmp_path)
    pending = _attr(page, "div", "pending")
    missing = _attr(page, "div", "missing-join")
    assert PENDING in pending
    assert MISSING not in pending
    assert "SETTLE_PENDING" in pending
    assert "Not a missing paper join" in pending
    assert MISSING in missing
    assert PENDING not in missing
    assert MISSING_JOIN_BANNER in missing
    assert "SETTLE_PENDING" not in missing
    assert GLANCE_NO_PNL in missing
    assert "not a pending window" in missing


def test_last_joined_pnl_is_that_book_only_not_lineage_b(lane, tmp_path):
    _watch(running=False)
    _wake(pending=PENDING, missing=MISSING, roles=[])
    _book(
        event=OLDER_EVENT,
        ticker=OLDER_JOIN,
        settled_at=datetime(2026, 9, 7, 15, 45, tzinfo=timezone.utc),
        pnl=OLDER_BOOK_PNL,
    )
    _book(
        event=JOINED_EVENT,
        ticker=JOINED,
        settled_at=datetime(2026, 9, 7, 16, 0, tzinfo=timezone.utc),
        pnl=THIS_BOOK_PNL,
    )
    page = _page(tmp_path)
    joined = _attr(page, "div", "last-joined")
    lineage = _attr(page, "p", "lineage")
    assert JOINED in joined
    assert "pnl=+0.42" in joined
    assert "copied from that book only" in joined
    assert "+0.10" not in joined
    assert LINEAGE_B_PNL not in joined
    assert "+2.09" not in joined
    assert "+0.52" not in joined
    assert LINEAGE_B in lineage
    assert LINEAGE_B_PNL in lineage
    assert "never summed" in lineage
    assert "not summed into last joined" in lineage
    assert "WATCH OFF" in page


def test_no_settled_book_says_no_pnl_on_disk(lane, tmp_path):
    _watch(running=False)
    page = _page(tmp_path)
    joined = _attr(page, "div", "last-joined")
    assert GLANCE_NO_PNL in joined
    assert "pnl=+0.00" not in joined
    assert "pnl=+0" not in joined


def test_settled_book_without_pnl_does_not_invent_zero(lane, tmp_path):
    _watch(running=False)
    _book(
        event=JOINED_EVENT,
        ticker=JOINED,
        settled_at=datetime(2026, 9, 7, 16, 0, tzinfo=timezone.utc),
        pnl=None,
    )
    page = _page(tmp_path)
    joined = _attr(page, "div", "last-joined")
    assert JOINED in joined
    assert GLANCE_NO_PNL in joined
    assert "pnl=+0.00" not in joined


def test_roles_owed_are_requests_not_completions(lane, tmp_path):
    _watch(running=True)
    _wake(pending=PENDING, missing=MISSING, roles=["digestor", "operator"])
    page = _page(tmp_path)
    roles = _attr(page, "p", "roles-owed")
    assert "roles owed: digestor, operator" in roles
    assert GLANCE_ROLES_REQUEST in roles
    assert "served" not in roles.lower()
    assert "completed" not in roles.lower()


def test_15m_glance_has_no_wc1_ill_and_golf_keeps_those_boards(lane, tmp_path):
    _watch(running=True)
    _wake(pending=PENDING, missing=MISSING, roles=["systems"])
    page = _page(tmp_path)
    glance = _glance(page)
    assert "WC1" not in glance
    assert "Ill" not in glance
    assert 'id="viz-slot-wc1_dated_record"' not in page
    assert 'id="viz-slot-shadow_honesty_strip"' not in page
    golf = _page(tmp_path, lane="golf")
    assert 'id="glance-15m"' not in golf
    assert "WATCH ON" not in golf
    assert "WC1 dated record" in golf


def test_no_new_post_selector_unchanged_forbidden_still_refuse(lane, tmp_path):
    _watch(running=True)
    page = _page(tmp_path)
    assert page.count('method="post"') == 1
    assert 'action="/run"' in page
    assert 'action="/glance"' not in page
    assert "innerHTML" not in page
    assert 'value="golf"' in page
    assert 'value="learning_lane_15m"' in page
    assert 'value="15m"' not in page
    for value in ("ingest", "live", "shadow", "loop", "refresh"):
        assert f'value="{value}"' in page
    for banned in ("deposit", "withdraw", "arm", "place", "kalshi-auth", "paper-deposit"):
        assert f'name="{banned}"' not in page
        assert f'value="{banned}"' not in page
    src = APP_PY.read_text(encoding="utf-8")
    assert "golf_kalshi" not in src
    assert "honer_15m" not in src
    assert "learning_lane_15m.farm" not in src
    assert "el.innerHTML" not in src
    assert ".innerHTML" not in src
    for action in ("deposit", "withdraw", "arm", "place", "kalshi-auth"):
        with pytest.raises(OperatorSafetyError):
            refuse_forbidden(action)


def test_paper_watch_stays_15m_only(lane):
    from golf_offshoot.operator_surface.app import _sync_paper_watch

    class FakeWatch:
        def __init__(self) -> None:
            self.started = 0
            self.stopped = 0

        def start(self) -> None:
            self.started += 1

        def stop_watch(self) -> None:
            self.stopped += 1

    fake = FakeWatch()
    state = {"paper_watch": fake, "lane": "golf"}
    _sync_paper_watch(state)
    assert fake.started == 0
    assert fake.stopped == 1
    state["lane"] = "learning_lane_15m"
    _sync_paper_watch(state)
    assert fake.started == 1
    state["lane"] = "15m"
    _sync_paper_watch(state)
    assert fake.started == 1
    assert fake.stopped == 2
