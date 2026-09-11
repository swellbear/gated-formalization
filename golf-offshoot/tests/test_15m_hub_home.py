"""15m glance home lock + this-lane doing/thinking/learning. Not go-live."""

from http.client import HTTPConnection
from threading import Thread
from types import SimpleNamespace
import json

from golf_offshoot.learning_lane_15m.paper import save_ledger
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.watch import write_watch_status
from golf_offshoot.operator_surface.app import (
    _sync_paper_watch,
    _watch_state,
    _window_summary_15m,
    build_surface,
    render_html,
)
from golf_offshoot.operator_surface.modes import NOT_ARMED, PAPER_ONLY
from golf_offshoot.operator_surface.lane_15m_home import golf_status_tile_model
from golf_offshoot.strategy.paper_ledger import PaperLedger


def _page(tmp_path, **kwargs):
    return render_html(
        build_surface(
            artifact_root=tmp_path,
            viz_root=tmp_path / "viz",
            lane="learning_lane_15m",
            **kwargs,
        )
    )


def _golf(tmp_path):
    return render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))


def test_15m_chrome_is_not_golf_named(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
        golf = _golf(tmp_path)
    finally:
        set_15m_root_override(None)
    header = page[page.index("<header") : page.index("</header>")]
    assert "KXBTC15M paper watch" in header
    assert "PHASE 1 OBSERVATION" not in header
    assert "Update live ranks" not in page
    assert "Pull latest data" not in page[page.index("<main") : page.index('id="tab-ops"')]
    assert "Fetch KXBTC15M" in page
    assert "Paper cycle" in page
    assert "Extra cycle" in page
    assert "Update live ranks" in golf
    assert "PHASE 1 OBSERVATION" in golf


def test_glance_strip_watch_window_pending_pnl(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        write_watch_status(
            {
                "running": True,
                "last_ok": True,
                "cycles": 4,
                "last_summary": "paper tick ok",
                "lane": "learning_lane_15m",
            }
        )
        led = PaperLedger(starting_bankroll=100.0, bankroll=95.59, betting_pnl=-4.41)
        save_ledger(led)
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    assert 'id="glance-strip"' in page
    assert 'data-watch="on"' in page
    assert "Watch on" in page
    assert 'class="settle"' not in page
    assert "watch-on" in page
    assert "lineage A P/L $-4.41" in page
    assert "bankroll $95.59" in page
    assert "KXBTC15M" in page
    assert 'data-kind="pending"' in page or 'data-kind="pending-none"' in page
    assert 'data-kind="missing-join"' in page or 'data-kind="missing-none"' in page


def test_healthy_watch_is_not_crimson_fail(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        write_watch_status({"running": True, "last_ok": True, "cycles": 1, "last_summary": "ok"})
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    assert 'data-watch="on"' in page
    assert "WATCH ON" not in page
    assert 'class="settle"' not in page
    assert ".chip.watch-on { background: #1f5c3a" in page


def test_journal_is_exceptions_not_dump(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    assert 'id="exceptions-fold"' in page
    assert "Exceptions — open book / last joins" in page
    assert "Full tape (not the glance)" in page
    assert "What the last run did" not in page
    assert "Last operator cycle" not in page
    assert "15-min Kalshi journal" not in page
    assert "<details" in page


def test_png_caption_matches_pnl_board(monkeypatch, tmp_path):
    png = tmp_path / "board.png"
    png.write_bytes(b"\x89PNG\r\n")
    monkeypatch.setattr("golf_offshoot.operator_surface.lane_15m_home.chart_15m_path", lambda: png)
    monkeypatch.setattr("golf_offshoot.operator_surface.app._chart_15m_path", lambda: png)
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    assert "paper PnL" in page
    assert "never summed" in page
    assert "Missing join" in page or "missing paper join" in page
    assert "No bankroll, payout or PnL is drawn" not in page
    assert "No golf WC1" in page


def test_15m_script_does_not_reload_on_generation(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    assert "var is15 = document.body.classList.contains('lane-15m')" in page
    assert "applyHome(s.home)" in page
    # Golf still reloads on generation; 15m returns after the patch.
    assert "if (s.generation !== gen) location.reload()" in page
    home_idx = page.index("applyHome(s.home)")
    golf_reload = page.index("if (s.generation !== gen) location.reload()")
    assert home_idx < golf_reload
    assert "return;" in page[home_idx:golf_reload]


def test_market_lock_obvious_paper_subtle(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    header = page[page.index("<header") : page.index("</header>")]
    assert 'class="market-lock"' in header
    assert 'class="lock-ticker">KXBTC15M' in header
    assert "market lock" in header
    assert 'class="trust"' in header
    assert "Paper · not armed" in header
    assert 'data-market="KXBTC15M"' in page
    assert 'data-lane="learning_lane_15m"' in page
    assert NOT_ARMED in page
    assert PAPER_ONLY in page
    assert 'value="deposit"' not in page
    assert 'value="arm"' not in page


def test_thin_tabs_on_home(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    for label in ("Home", "Scoreboard", "Lab", "Ops", "Bot-hub"):
        assert label in page
    assert 'class="thin-tabs"' in page
    assert 'data-tab="home"' in page
    assert 'id="tab-home"' in page
    assert "tab-panel active" in page
    assert 'data-density="cockpit"' in page
    assert 'data-density="glance"' in page
    assert "gpf-15m-tab" in page
    assert "'1':'home'" in page
    assert "'2':'scoreboard'" in page
    assert page.index('class="thin-tabs"') < page.index('class="panel chart-panel"')
    assert "cockpit-only" in page
    assert ".cockpit-only { display: none; }" in page


def test_golf_control_does_not_stop_paperwatch(monkeypatch):
    created = []

    class FakeWatch:
        def __init__(self, **kwargs):
            created.append(self)
            self.started = 0
            self.stopped = 0
            self.on_cycle = kwargs.get("on_cycle")

        def start(self):
            self.started += 1

        def stop_watch(self):
            self.stopped += 1

        def status(self):
            return {"running": True, "cycles": 1, "last_ok": True}

    monkeypatch.setattr("golf_offshoot.operator_surface.app.PaperWatch", FakeWatch)
    state = {
        "lane": "learning_lane_15m",
        "surface": {"last_run": None},
        "paper_watch": None,
        "paper_watch_keep": False,
    }
    _sync_paper_watch(state)
    assert len(created) == 1
    assert created[0].started == 1
    assert created[0].stopped == 0
    state["lane"] = "golf"
    _sync_paper_watch(state)
    assert created[0].stopped == 0
    assert state["paper_watch_keep"] is True
    golf_only = {
        "lane": "golf",
        "surface": {"last_run": None},
        "paper_watch": None,
        "paper_watch_keep": False,
    }
    _sync_paper_watch(golf_only)
    assert golf_only.get("paper_watch") is None


def test_paperwatch_is_the_loop_copy(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    assert "PaperWatch remains the loop" in page or "PaperWatch is the loop" in page
    assert "Buttons are extras" in page or "buttons are extras" in page.lower()
    assert "stop PaperWatch" in page


def test_this_lane_doing_thinking_learning(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        write_watch_status({"running": True, "last_ok": True, "cycles": 2, "last_summary": "join ok"})
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    start = page.index('id="lane-now"')
    end = page.index("</div>", start) + len("</div>")
    if 'id="lane-tiles"' in page:
        end = page.index('id="lane-tiles"')
    now = page[start:end]
    assert "Doing</span>" in now
    assert "Thinking</span>" in now
    assert "Learning</span>" in now
    assert "PaperWatch is the loop" in now
    assert "golf" not in now.lower()
    assert "role roster" not in page.lower()


def test_missing_join_is_not_counted_as_pending():
    rows = [
        SimpleNamespace(
            ticker="KXBTC15M-26SEP071500-00",
            settle_status="finalized",
            kalshi_result="",
            paper_join=False,
            missing_join=True,
        ),
        SimpleNamespace(
            ticker="KXBTC15M-26SEP071900-00",
            settle_status="SETTLE_PENDING",
            kalshi_result="",
            paper_join=True,
            missing_join=False,
        ),
    ]
    counts, windows = _window_summary_15m(rows)
    assert "SETTLE_PENDING 1" in counts
    assert "missing paper join 1" in counts
    assert "KXBTC15M-26SEP071500-00 · missing paper join" in windows
    assert "KXBTC15M-26SEP071500-00 · SETTLE_PENDING" not in windows
    assert "KXBTC15M-26SEP071900-00 · SETTLE_PENDING" in windows


def test_api_watch_includes_15m_home_and_no_generation_bump_on_cycle(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        from golf_offshoot.operator_surface.app import OperatorHandler, _HubServer

        state = {
            "event_id": "",
            "artifact_root": tmp_path,
            "viz_root": tmp_path / "viz",
            "odds_book": "auto",
            "lane": "learning_lane_15m",
            "generation": 0,
            "reload_kind": "watch",
            "watch_cycles": 3,
            "paper_watch_keep": True,
            "paper_watch": None,
            "surface": build_surface(
                artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="learning_lane_15m"
            ),
        }
        payload = _watch_state(state)
        assert payload["generation"] == 0
        assert payload["kind"] == "watch"
        assert payload["home"]["lane"] == "learning_lane_15m"
        assert payload["home"]["series"] == "KXBTC15M"
        assert payload["home"]["trading_armed"] is False
        assert "glance_html" in payload["home"]
        assert "session_html" in payload["home"]
        assert "now_html" in payload["home"]
        assert "tiles_html" in payload["home"]
        assert "roles_html" in payload["home"]
        assert "ops_watch_html" in payload["home"]
        assert "cockpit_html" in payload["home"]
        httpd = _HubServer(("127.0.0.1", 0), OperatorHandler)
        httpd.surface_state = state
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = httpd.server_address[:2]
            conn = HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/api/watch")
            body = conn.getresponse().read().decode("utf-8")
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()
        assert '"generation": 0' in body
        assert '"lane": "learning_lane_15m"' in body
        assert "glance_html" in body
        assert "tiles_html" in body
        assert "roles_html" in body
    finally:
        set_15m_root_override(None)


def test_golf_status_tile_copies_stamp_not_a_cockpit():
    stamp = """
| Operator idle until Founder GO? | **Y** (WC3+ only on a new settled week) |
| Lab WC1 | **ADMITTED** dated record — FAIL / park unproven · edge **not established** |
"""
    data = golf_status_tile_model(stamp)
    assert data["lane"] == "golf"
    assert data["status"] == "idle ON"
    assert "WC1 FAIL / park unproven" in data["note"]
    assert "edge not established" in data["note"]
    empty = golf_status_tile_model("")
    assert empty["status"] == "stamp not on this tree"
    assert "cockpit" in empty["note"]


def test_other_lanes_are_status_tiles_not_golf_cockpit(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _page(tmp_path)
        golf = _golf(tmp_path)
    finally:
        set_15m_root_override(None)
    assert 'id="lane-tiles"' in page
    assert 'data-lane="golf"' in page
    end = page.index('id="role-strip"') if 'id="role-strip"' in page else page.index("<main")
    tiles = page[page.index('id="lane-tiles"') : end]
    assert "idle ON" in tiles
    assert "WC1 FAIL / park unproven" in tiles
    assert "edge not established" in tiles
    assert "Update live ranks" not in tiles
    assert "Pull latest data" not in tiles
    assert "Ranked table" not in tiles
    assert "viz-slot-wc1" not in tiles
    assert "wc1_dated_record" not in tiles
    assert "<section" not in tiles
    assert "cockpit" not in tiles.lower()
    assert "KXBTC15M" not in tiles
    assert "ETH" not in tiles
    assert 'id="lane-tiles"' not in golf
    assert tiles.count('class="lane-tile"') == 1
    # Glance home still has the market lock; tiles must not become a second board.
    header = page[page.index("<header") : page.index("</header>")]
    assert 'class="lock-ticker">KXBTC15M' in header
    assert 'data-market="KXBTC15M"' in page


def _write_wake(tmp_path, **payload):
    latest = tmp_path / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    (latest / "learning_wake.json").write_text(json.dumps(payload), encoding="utf-8")


def test_role_strip_collapsed_unless_owed(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _write_wake(
            tmp_path,
            roles_owed=[],
            served=[],
            updated_at="2026-09-11T11:00:00-04:00",
        )
        idle_page = _page(tmp_path)
        _write_wake(
            tmp_path,
            roles_owed=[{"role": "digestor", "age_text": "12m"}],
            served=[{"role": "systems", "served_at": "2026-09-11T10:40:00-04:00"}],
            updated_at="2026-09-11T11:00:00-04:00",
        )
        owed_page = _page(tmp_path)
        golf = _golf(tmp_path)
    finally:
        set_15m_root_override(None)
    idle = idle_page[idle_page.index('id="role-strip"') : idle_page.index("<main")]
    owed = owed_page[owed_page.index('id="role-strip"') : owed_page.index("<main")]
    assert '<details class="role-strip-details">' in idle
    assert '<details class="role-strip-details" open>' not in idle
    assert "idle · last tick" in idle
    assert "last tick 2026-09-11 11:00 EDT" in idle
    assert '<details class="role-strip-details" open>' in owed
    assert "owed digestor 12m" in owed
    assert "last served: systems" in owed
    assert 'href="#lane-now"' in owed
    assert 'data-tab="lab"' in owed
    assert 'data-density="cockpit"' in owed
    assert "<ul" not in owed
    assert "for:" not in owed
    assert "role roster" not in owed_page.lower()
    assert "crew roster" not in owed_page.lower()
    assert 'id="role-strip"' not in golf
    stack = owed_page[owed_page.index("<header") : owed_page.index("<main")]
    assert "<section" not in stack
    assert stack.count("class=\"panel\"") == 0


def test_preview_launcher_runs_this_checkout_not_master():
    from golf_offshoot.operator_surface.paths import package_root

    root = package_root()
    bat = (root / "Open-15m-Hub-PREVIEW.bat").read_text(encoding="utf-8")
    url = (root / "Open-15m-Hub-PREVIEW.url").read_text(encoding="utf-8")
    lower = bat.lower()
    assert "--lane learning_lane_15m" in bat
    assert "--host 127.0.0.1" in bat
    assert "--port 8765" in bat
    assert "PREVIEW" in bat
    assert "NOT ARMED" in bat
    assert "src\\golf_offshoot" in bat
    assert "git checkout" not in lower
    assert "git pull" not in lower
    assert "gated-formalization-master-hub" not in lower
    assert "not master" in lower or "does not touch master" in lower
    assert "InternetShortcut" in url
    assert "http://127.0.0.1:8765" in url


def test_doing_thinking_learning_uses_wake_when_present(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        write_watch_status(
            {
                "running": True,
                "last_ok": True,
                "cycles": 9,
                "last_summary": "paper tick ok",
                "last_at": "2026-09-11T12:00:00-04:00",
                "interval_s": 90,
            }
        )
        _write_wake(
            tmp_path,
            updated_at="2026-09-11T12:01:00-04:00",
            scan={
                "pending": [
                    {
                        "ticker": "KXBTC15M-26SEP111215-15",
                        "reason": "wait for Kalshi result",
                    }
                ],
                "paper_join_missing": [
                    {
                        "ticker": "KXBTC15M-26SEP071500-00",
                        "reason": "official result present; paper book not on this tree",
                    }
                ],
            },
            new_events=[
                {
                    "kind": "new_settle",
                    "ticker": "KXBTC15M-26SEP111200-00",
                    "detail": "official Kalshi result=yes via latest/journal.json",
                    "at": "2026-09-11T12:00:00-04:00",
                }
            ],
            events=[],
            roles_owed=[{"role": "digestor", "age_text": "4m", "reasons": ["new official settle"]}],
        )
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    now = page[page.index('id="lane-now"') : page.index('id="lane-tiles"')]
    assert "Watch on" in now
    assert "last cycle 2026-09-11 12:00 EDT" in now
    assert "SETTLE_PENDING KXBTC15M-26SEP111215-15" in now
    assert "wait for Kalshi result" in now
    assert "missing paper join KXBTC15M-26SEP071500-00" in now
    assert "new_settle KXBTC15M-26SEP111200-00" in now
    assert "owed digestor 4m" in now
    assert "now-sub" in now
    assert "cadence ~90s" in now
    assert "cockpit-only" in now


def test_views_are_thin_but_real(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        led = PaperLedger(starting_bankroll=100.0, bankroll=95.59, betting_pnl=-4.41)
        save_ledger(led)
        _write_wake(
            tmp_path,
            updated_at="2026-09-11T12:01:00-04:00",
            scan={"pending": [], "paper_join_missing": []},
            roles_owed=[],
            lab_gate={
                "lab_owed": False,
                "why": "honesty gate has not passed -- test",
                "boxes": [{"box": "Lineage story readable", "state": "PASS"}],
                "note": "Lab never self-admits.",
            },
        )
        page = _page(tmp_path)
    finally:
        set_15m_root_override(None)
    score = page[page.index('id="tab-scoreboard"') : page.index('id="tab-lab"')]
    lab = page[page.index('id="tab-lab"') : page.index('id="tab-ops"')]
    ops = page[page.index('id="tab-ops"') : page.index('id="tab-bot-hub"')]
    bot = page[page.index('id="tab-bot-hub"') :]
    assert "Lineage A (this tree)" in score
    assert "never added together" in score
    assert "missing paper join" in score
    assert "Fee-accurate" not in lab
    assert "RUN-ONLY" in lab
    assert "NOT owed" in lab
    assert "Honesty stamp" in lab
    assert "PaperWatch remains the loop" in ops
    assert "Watch" in ops
    assert "Fetch KXBTC15M" in ops
    assert "last tick 2026-09-11 12:01 EDT" in bot
    assert "roles owed: none" in bot
    assert "trading_armed=false" in bot
    assert 'id="cockpit-rail"' in page
    assert 'class="tape-card"' in page
    assert 'id="session-strip"' in page
    header = page[page.index("<header") : page.index("</header>")]
    assert 'class="lock-ticker">KXBTC15M' in header
    assert 'value="arm"' not in page
    assert 'value="deposit"' not in page


def test_session_strip_copies_open_book_and_folds_exceptions(tmp_path):
    from datetime import datetime, timezone

    from golf_offshoot.learning_lane_15m.paper import save_book
    from golf_offshoot.models.enums import BetType
    from golf_offshoot.models.strategy import PortfolioState, StrategyPosition
    from golf_offshoot.strategy.paper_book import PaperBookFile

    set_15m_root_override(tmp_path)
    try:
        save_book(
            PaperBookFile(
                tournament_id="KXBTC15M-26SEP111215__2026-09-11T16:00:00Z__2026-09-11T16:15:00Z",
                tournament_name="KXBTC15M",
                bankroll=100.0,
                book=PortfolioState(
                    bankroll=100.42,
                    positions=[
                        StrategyPosition(
                            position_id="paper-settled",
                            player_id="KXBTC15M-26SEP111215-15",
                            player_name="YES KXBTC15M-26SEP111215-15",
                            bet_type=BetType.WIN,
                            stake=1.0,
                            decimal_odds=2.0,
                            entry_edge=0.0,
                            entry_model_p=0.5,
                            entry_market_p=0.5,
                            fill_price=0.5,
                        )
                    ],
                ),
                settled_at=datetime(2026, 9, 11, 16, 15, tzinfo=timezone.utc),
                settlement_pnl=0.42,
            )
        )
        save_book(
            PaperBookFile(
                tournament_id="KXBTC15M-26SEP111230__2026-09-11T16:15:00Z__2026-09-11T16:30:00Z",
                tournament_name="KXBTC15M",
                bankroll=100.0,
                book=PortfolioState(
                    bankroll=100.0,
                    positions=[
                        StrategyPosition(
                            position_id="paper-open",
                            player_id="KXBTC15M-26SEP111230-30",
                            player_name="YES KXBTC15M-26SEP111230-30",
                            bet_type=BetType.WIN,
                            stake=1.0,
                            decimal_odds=2.105,
                            entry_edge=0.0,
                            entry_model_p=0.475,
                            entry_market_p=0.475,
                            fill_price=0.475,
                        )
                    ],
                ),
            )
        )
        page = _page(tmp_path)
        golf = _golf(tmp_path)
    finally:
        set_15m_root_override(None)
    session = page[page.index('id="session-strip"') : page.index('id="lane-now"')]
    assert "KXBTC15M-26SEP111230-30" in session
    assert "open paper YES $1.00 @ 0.475" in session
    assert "not an order" in session
    assert "display only, not settle" in session
    assert "data-close-epoch" in session
    now = page[page.index('id="lane-now"') : page.index('id="lane-tiles"')]
    assert "open paper YES $1.00 @ 0.475" in now
    assert "not a live bid/ask" in now
    assert "last joined KXBTC15M-26SEP111215-15 pnl=+0.42" in now
    assert 'id="exceptions-fold"' in page
    fold = page[page.index('id="exceptions-fold"') : page.index('id="tab-scoreboard"')]
    assert " open>" not in fold
    assert 'class="tape-card"' in page
    assert "gpf-15m-tab" in page
    assert "paintClocks" in page
    assert 'id="session-strip"' not in golf
    header = page[page.index("<header") : page.index("</header>")]
    assert 'class="lock-ticker">KXBTC15M' in header
    assert 'value="arm"' not in page
    assert 'value="deposit"' not in page


