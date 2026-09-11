"""Golf (Kalshi) glance chrome. Not go-live. Does not invent pnl."""

from http.client import HTTPConnection
from threading import Thread
import json

from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.operator_surface.app import (
    OperatorHandler,
    build_surface,
    render_html,
)
from golf_offshoot.operator_surface.lane_golf_home import (
    BOOK_MISSING,
    FARM_IDLE,
    HONER_IDLE,
    set_golf_kalshi_root_override,
)
from http.server import ThreadingHTTPServer


def _golf(tmp_path, **kwargs):
    return render_html(
        build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf", **kwargs)
    )


def test_golf_chrome_is_kalshi_gym_not_phase1(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _golf(tmp_path)
    finally:
        set_15m_root_override(None)
    header = page[page.index("<header") : page.index("</header>")]
    assert "Golf (Kalshi) paper watch" in header
    assert "PHASE 1 OBSERVATION" not in header
    assert "Paper · not armed" in header
    assert "gym lock" in header
    assert 'data-market="golf-kalshi"' in page
    assert 'data-lane="golf"' in page
    assert "Golf Kalshi tick" in page
    assert "Tournament id (ESPN)" not in page
    assert "Update live ranks" not in page
    assert 'id="golf-farm"' in page
    assert "Golf Farm" in page
    assert "Golf Honer" in page
    assert FARM_IDLE in page
    assert HONER_IDLE in page
    assert "Previous golf claim" in page
    assert "WC1 dated record" in page
    assert page.index('id="tab-home"') < page.index('id="viz-wall"')
    assert "do not add honer bankrolls to Lineage A" in page
    assert "KXBTC15M" not in page[page.index('id="tab-home"') : page.index('id="tab-scoreboard"')]


def test_golf_glance_does_not_invent_pnl(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        page = _golf(tmp_path)
    finally:
        set_15m_root_override(None)
    assert BOOK_MISSING in page or "P/L not on file — none invented" in page
    assert "lineage A P/L" not in page[page.index('id="glance-strip"') : page.index('id="session-strip"')]
    assert 'data-kind="golf-pnl"' in page
    assert "Watch off" in page or 'data-watch="off"' in page
    assert 'class="settle"' in page
    glance = page[page.index('id="glance-strip"') : page.index('id="session-strip"')]
    assert 'class="settle"' not in glance


def test_golf_copies_book_files_when_present(tmp_path):
    gym = tmp_path / "golf_kalshi"
    (gym / "latest").mkdir(parents=True)
    (gym / "paper").mkdir(parents=True)
    (gym / "latest" / "snapshot.json").write_text(
        json.dumps(
            {
                "running": True,
                "watch_at": "2026-09-11 12:55 EDT",
                "tickets_n": 12,
                "pnl": 0.0,
                "bankroll": 1000.0,
                "fees": 13.41,
                "halt": False,
                "field_hunt": "bound 28 · brain 2 · deferred 26",
                "recipe": "golf-kalshi-recipe-v1.1 · brain keep_expert",
                "tickets": [
                    {
                        "player": "Antoine Rozner",
                        "market": "Antoine Rozner finishes top 10",
                        "sleeve": "week",
                        "stake": 25.0,
                        "quote": 0.01,
                        "status": "SETTLE_PENDING",
                    }
                ],
                "sleeves": [{"name": "This week", "used": 200.0, "cap": 1000.0}],
            }
        ),
        encoding="utf-8",
    )
    set_golf_kalshi_root_override(gym)
    set_15m_root_override(tmp_path)
    try:
        page = _golf(tmp_path)
    finally:
        set_golf_kalshi_root_override(None)
        set_15m_root_override(None)
    glance = page[page.index('id="glance-strip"') : page.index('id="session-strip"')]
    assert "Watch on" in glance
    assert "paper tickets 12" in glance
    assert "P/L $0.00" in glance
    assert "bankroll $1000.00" in glance
    assert "Halt no" in glance
    assert "Antoine Rozner" in page
    assert "golf-kalshi-recipe-v1.1" in page
    assert "This week" in page
    assert "KXBTC15M" not in glance


def test_golf_ops_does_not_dump_15m_ledger(tmp_path):
    from golf_offshoot.operator_surface.runner import RunRecord

    rec = RunRecord(
        command="watch",
        ok=True,
        event_id="KXBTC15M",
        paper="PAPER LEDGER  journal=15m\nbankroll=$82.38  P/L $-17.62",
        extras={"lane": "learning_lane_15m"},
    )
    set_15m_root_override(tmp_path)
    try:
        page = render_html(
            build_surface(
                artifact_root=tmp_path,
                viz_root=tmp_path / "viz",
                lane="golf",
                last_run=rec,
            )
        )
    finally:
        set_15m_root_override(None)
    ops = page[page.index('id="tab-ops"') : page.index('id="tab-farm"')]
    assert "journal=15m" not in ops
    assert "bankroll=$82.38" not in ops
    assert "never dump the 15m ledger" in ops or "Last shell cycle was the 15m" in ops


def test_golf_catalog_route_is_honest_when_missing(tmp_path):
    state = {
        "event_id": "",
        "artifact_root": tmp_path,
        "viz_root": tmp_path / "viz",
        "odds_book": "auto",
        "lane": "golf",
        "surface": build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"),
        "generation": 0,
        "reload_kind": "ok",
    }
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), OperatorHandler)
    httpd.surface_state = state  # type: ignore[attr-defined]
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = httpd.server_address[:2]
        conn = HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/golf-catalog/series?ticker=KXPGATOP10")
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
        assert resp.status == 503
        assert "not on this checkout" in body
        conn.request("GET", "/api/watch")
        watch = json.loads(conn.getresponse().read().decode("utf-8"))
        assert watch["lane"] == "golf"
        assert "glance_html" in watch["home"]
        assert "Golf (Kalshi)" in watch["home"]["glance_html"]
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
