from golf_offshoot.audit.journal import build_audit
from golf_offshoot.demo import demo_tournament
from golf_offshoot.models.enums import Horizon, RunMode
from golf_offshoot.models.schemas import HorizonProbability, PlayerOutput, ProbabilityBundle, ReliabilityScore, TournamentRunResult
from golf_offshoot.ranking.export_table import write_ranked_table_files
import pytest


def _pdf_visible_text(path) -> str:
    fitz = pytest.importorskip("fitz")
    doc = fitz.open(path)
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()

def _hp(horizon: Horizon, central: float) -> HorizonProbability:
    lo = max(0.0, central - 0.01)
    hi = min(1.0, central + 0.01)
    return HorizonProbability(horizon=horizon, central=central, low=lo, high=hi)


def _row(pid: str, name: str, rank: int, win: float, flags: list[str] | None = None) -> PlayerOutput:
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
    return PlayerOutput(
        player_id=pid,
        name=name,
        rank=rank,
        probabilities=bundle,
        reliability=rel,
        flags=list(flags or []),
    )


def _result(rows, mode=RunMode.LIVE):
    t = demo_tournament()
    audit = build_audit(t.tournament_id, mode, rows, "h")
    return TournamentRunResult(
        run_id=audit.run_id,
        tournament=t,
        mode=mode,
        ranked=rows,
        audit=audit,
    )


def test_ranked_export_pdf_html_txt(tmp_path):
    live_rows = [
        _row("kita", "Kurt Kitayama", 3, 0.089),
        _row("hoj", "Rasmus Hojgaard", 12, 0.030),
    ]
    pre_rows = [_row("kita", "Kurt Kitayama", 18, 0.016)]
    result = _result(live_rows)
    paths = write_ranked_table_files(
        result,
        baseline=pre_rows,
        caption="movement vs pre-tournament snapshot test-run",
        directory=tmp_path,
    )
    text = paths.txt.read_text(encoding="utf-8")
    assert "Kurt Kitayama" in text
    assert "Column index" in text
    html = paths.html.read_text(encoding="utf-8")
    assert "<table class=\"field\">" in html
    assert "<th" in html
    assert "Kurt Kitayama" in html
    assert "Column index" in html
    pdf = paths.pdf.read_bytes()
    assert pdf.startswith(b"%PDF")
    assert b"/Type /Page" in pdf or b"/Type/Page" in pdf
    extracted = _pdf_visible_text(paths.pdf)
    assert "Kitayama" in extracted
    assert "Column index" in extracted
    assert "0.089  [" in extracted
    assert result.run_id.replace(":", "-") in paths.pdf.name or result.run_id in paths.pdf.name


def test_ranked_export_paginates_long_field(tmp_path):
    rows = [_row(f"p{i:03d}", f"Player {i:03d}", i + 1, max(0.001, 0.08 - i * 0.001)) for i in range(80)]
    result = _result(rows, mode=RunMode.PRE_TOURNAMENT)
    paths = write_ranked_table_files(result, directory=tmp_path)
    pdf = paths.pdf.read_bytes()
    assert pdf.startswith(b"%PDF")
    assert pdf.count(b"/Type /Page") >= 2
    html = paths.html.read_text(encoding="utf-8")
    assert "Player 000" in html
    assert "Player 079" in html


def test_pdf_uses_fpdf2_and_landscape_letter(tmp_path):
    import fpdf
    from fpdf import FPDF

    assert hasattr(FPDF, "table")
    assert str(getattr(fpdf, "__version__", "0")).startswith("2.")
    paths = write_ranked_table_files(_result([_row("a", "Ludvig Åberg", 1, 0.021)]), directory=tmp_path)
    pdf = paths.pdf.read_bytes()
    assert b"/MediaBox [0 0 792.00 612.00]" in pdf or b"/MediaBox[0 0 792" in pdf
    extracted = _pdf_visible_text(paths.pdf)
    assert "Åberg" in extracted or "Aberg" in extracted
    assert "0.021  [" in extracted
    assert "Column index" in extracted
    html = paths.html.read_text(encoding="utf-8")
    assert "0.021  [0.01-0.03]" in html


def test_pdf_glossary_stays_left_after_full_live_field(tmp_path):
    fitz = pytest.importorskip("fitz")
    live = []
    pre = []
    for i in range(69):
        flags = ["thin_sample_overconfidence", "sparse_data"] if i % 7 == 4 else (["sparse_data"] if i % 5 == 0 else [])
        live.append(_row(f"p{i:03d}", f"Player {i:03d}", i + 1, max(0.001, 0.12 - i * 0.0017), flags=flags))
        pre.append(_row(f"p{i:03d}", f"Player {i:03d}", (i * 3) % 69 + 1, 0.02))
    paths = write_ranked_table_files(
        _result(live),
        baseline=pre,
        caption="movement vs pre-tournament snapshot test-run",
        directory=tmp_path,
    )
    doc = fitz.open(paths.pdf)
    try:
        assert doc[0].rect.width > doc[0].rect.height
        after_index = False
        left_hits = {k: 0 for k in ("Player", "Win", "Flags", "Note", "n/a", "dWin")}
        orphans = []
        for page in doc:
            for x0, _y0, _x1, _y1, word, *_rest in page.get_text("words"):
                if word == "Column" and not after_index:
                    after_index = True
                    continue
                if after_index and word in left_hits:
                    if x0 < 110:
                        left_hits[word] += 1
                    elif x0 > 500:
                        orphans.append((page.number + 1, word, round(x0, 1)))
        assert after_index
        assert left_hits["Player"] >= 1
        assert left_hits["Note"] >= 1
        assert left_hits["n/a"] >= 1
        assert orphans == []
        last = doc[-1].get_text()
        assert "never auto-bet" in last
        assert len(last) > 180
        assert "thin sample overconfidence" in "\n".join(p.get_text() for p in doc)
    finally:
        doc.close()
