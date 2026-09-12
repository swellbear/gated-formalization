"""8765 paint: chrome only. Does not invent numbers or merge books."""

from pathlib import Path

from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.operator_surface.app import HARD_NO_STRIP, build_surface, render_html
from golf_offshoot.operator_surface.desk import DESK_CSS, DESK_JS


def _pages(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        golf = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))
        page = render_html(
            build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="learning_lane_15m")
        )
    finally:
        set_15m_root_override(None)
    return golf, page


def test_paint_chrome_is_sticky_and_quiet(tmp_path):
    golf, page = _pages(tmp_path)
    css = DESK_CSS.read_text(encoding="utf-8")
    js = DESK_JS.read_text(encoding="utf-8")
    assert "class=\"desk-chrome\"" in golf
    assert "class=\"desk-chrome\"" in page
    assert "class=\"desk-nav\"" in golf
    assert ".desk-chrome" in css
    assert "position: sticky" in css
    assert "--book-factory" in css
    assert "--book-golf" in css
    assert "--book-honer" in css
    assert "cursor: zoom-in" in css
    assert ".lightbox.full img" in css
    assert 'aria-current' in js
    assert HARD_NO_STRIP not in golf
    assert HARD_NO_STRIP not in page


def test_paint_keeps_three_books_separate(tmp_path):
    golf, page = _pages(tmp_path)
    home_15 = page[page.index("desk-view-home") : page.index("desk-view-scoreboard")]
    score_15 = page[page.index("desk-view-scoreboard") : page.index("desk-view-lab")]
    lab_15 = page[page.index("desk-view-lab") : page.index("desk-view-ops")]
    honer_15 = page[page.index("desk-view-honer") :]
    home_g = golf[golf.index("desk-view-home") : golf.index("desk-view-scoreboard")]
    honer_g = golf[golf.index("desk-view-honer") : golf.index("desk-view-museum")]

    assert 'data-book="factory"' in home_15
    assert 'data-book="clock"' in home_15
    assert 'id="factory-home"' in home_15
    assert 'data-book="golf"' not in home_15
    assert 'data-book="factory"' in score_15
    assert 'data-book="lab"' in lab_15
    assert 'class="learning-card"' in lab_15
    assert 'data-book="honer"' in honer_15
    assert "Do not add bankrolls" in page
    assert "books do not merge" in honer_15.lower() or "Do not add these bankrolls" in honer_15

    assert 'data-book="golf"' in home_g
    assert 'id="golf-kalshi"' in home_g
    assert 'data-book="factory"' not in home_g
    assert 'data-book="honer"' in honer_g
    assert "Live/entry $" in home_g
    assert "Factory — fill-all baseline" in home_15
    assert "Factory — live 70" not in page


def test_paint_does_not_move_honesty_copy(tmp_path):
    golf, page = _pages(tmp_path)
    home_15 = page[page.index("desk-view-home") : page.index("desk-view-scoreboard")]
    ops_15 = page[page.index("desk-view-ops") : page.index("desk-view-farm")]
    assert "Pages can lag this gym export" in ops_15
    assert "This 8765 book is the live book" in ops_15
    assert "Pages can lag this gym export" not in home_15
    assert 'id="trial-glance"' in home_15
    assert 'class="learning-card"' not in home_15
    assert 'value="golf"' in golf and 'value="learning_lane_15m"' in golf
    assert 'value="15m"' not in golf
    for action in ("ingest", "live", "shadow", "loop", "refresh"):
        assert f'value="{action}"' in golf
        assert f'value="{action}"' in page
    assert "New fills: event dollars" in golf


def test_paint_does_not_import_loop_math():
    root = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot"
    desk = (root / "operator_surface" / "desk.py").read_text(encoding="utf-8")
    css = DESK_CSS.read_text(encoding="utf-8")
    js = DESK_JS.read_text(encoding="utf-8")
    blob = desk + css + js
    for needle in ("allocate", "recipe.py", "farm.py", "honer_15m.exam", "rules.decide"):
        assert needle not in blob
