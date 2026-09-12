"""Hub HTML. Lane chrome is always visible. Journals and viz stay lane-scoped."""

from __future__ import annotations

import html
from pathlib import Path

from golf_offshoot.learning_lane_15m.paper import (
    format_15m_ledger,
    format_15m_observation_board,
    latest_shadow_lines,
    load_ledger,
)
from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    artifact_root_15m,
    golf_data_root,
    golf_paper_dir,
    golf_shadow_dir,
)
from golf_offshoot.operator_surface.lanes import (
    DEFAULT_LANE,
    SELECTOR_FIELD,
    lane_header_name,
    lane_journal_label,
    parse_lane,
)

HARD_NOS = (
    "PHASE 1 OBSERVATION",
    "Trading NOT ARMED",
    "PAPER OBSERVATION ONLY",
    "AI: NO CASH IN/OUT",
)

GOLF_VIZ_SLOTS = ("WC1", "Ill")


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _banner_bits(lane: str) -> str:
    bits = [f"<span class='badge'>{_esc(b)}</span>" for b in HARD_NOS]
    if lane == LANE_15M:
        bits.append("<span class='badge learning'>LEARNING LANE</span>")
    return "\n".join(bits)


def _selector(lane: str) -> str:
    golf_on = "aria-pressed='true' class='lane-btn active'" if lane != LANE_15M else "class='lane-btn'"
    m15_on = "aria-pressed='true' class='lane-btn active'" if lane == LANE_15M else "class='lane-btn'"
    return f"""
<form class="lane-form" method="get" action="">
  <fieldset>
    <legend>Mode</legend>
    <button type="submit" name="{SELECTOR_FIELD}" value="golf" {golf_on}>Golf Phase 1</button>
    <button type="submit" name="{SELECTOR_FIELD}" value="learning_lane_15m" {m15_on}>15-min Kalshi (learning)</button>
  </fieldset>
</form>
"""


def _golf_journal_html() -> str:
    paper = golf_paper_dir()
    shadow = golf_shadow_dir()
    ledger = paper / "ledger.json"
    advises = shadow / "advises.jsonl"
    ledger_note = "golf ledger present" if ledger.is_file() else "golf ledger not yet available"
    shadow_note = "golf shadow present" if advises.is_file() else "golf shadow not yet available"
    return f"""
<section class="journal" data-journal="golf">
  <h2>Journal: golf</h2>
  <p class="scope">Artifact root: {_esc(golf_data_root())}</p>
  <p>{_esc(ledger_note)}</p>
  <p>{_esc(shadow_note)}</p>
  <p>Golf totals stay on this lane only. Not combined with 15m.</p>
</section>
"""


def _m15_journal_html() -> str:
    led = load_ledger()
    body = format_15m_observation_board() if led.entries else format_15m_ledger(led)
    shadow = latest_shadow_lines(8)
    shadow_html = (
        "<pre>" + _esc("\n".join(shadow)) + "</pre>"
        if shadow
        else "<p>15m shadow not yet available</p>"
    )
    return f"""
<section class="journal" data-journal="15m">
  <h2>Journal: 15m</h2>
  <p class="scope">Artifact root: {_esc(artifact_root_15m())}</p>
  <p>Public viewer (read-only):
  <a href="https://swellbear.github.io/gated-formalization/observability-hub/">observability-hub</a></p>
  <pre>{_esc(body)}</pre>
  <h3>Shadow (15m only)</h3>
  {shadow_html}
  <p>No combined golf+15m totals. No Kalshi cash in or out. Charts stay not yet available until Illustrator has a real PNG.</p>
</section>
"""


def _learning_card_html() -> str:
    """Render the generated card. Missing stays missing — no invented fallback."""
    from golf_offshoot.learning_lane_15m.learning_card import (
        MISSING_HUB_COPY,
        card_path,
    )

    path = card_path()
    if not path.is_file():
        body = f'<p class="empty">{_esc(MISSING_HUB_COPY)}</p>'
    else:
        body = f"<pre>{_esc(path.read_text(encoding='utf-8', errors='replace'))}</pre>"
    return f"""
<section class="learning-card">
  <h2>What is on trial</h2>
  {body}
</section>
"""


def _viz_html(lane: str) -> str:
    if lane == LANE_15M:
        return f"""
{_learning_card_html()}
<section class="viz" data-lane="learning_lane_15m">
  <h2>Viz wall</h2>
  <p class="empty">not yet available — 15-min lane is observation-only. No golf WC1 / Ill charts here.</p>
</section>
"""
    slots = "\n".join(
        f"<article class='slot'><h3>{_esc(name)}</h3><p>golf viz slot</p></article>"
        for name in GOLF_VIZ_SLOTS
    )
    return f"""
<section class="viz" data-lane="golf">
  <h2>Viz wall</h2>
  {slots}
</section>
"""


def render_hub(lane: str | None = None, *, query: dict | None = None) -> str:
    """Systems-owned hub HTML. Default lane is golf."""
    if query is not None:
        active = parse_lane(query.get(SELECTOR_FIELD) if hasattr(query, "get") else None)
    else:
        active = parse_lane(lane)
    name = lane_header_name(active)
    journal = lane_journal_label(active)
    extra = " LEARNING LANE." if active == LANE_15M else ""
    copy = (
        "15-min Kalshi is a learning lane for the shared operating loop "
        "(ingest, live prices, paper autobet, settle join). "
        "It is not live trading and not a golf WC1 edge."
        if active == LANE_15M
        else "Golf Phase 1 stays observation-only. Trading is not armed."
    )
    journal_html = _m15_journal_html() if active == LANE_15M else _golf_journal_html()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Hub — {_esc(name)}</title>
  <style>
    body {{ font-family: sans-serif; margin: 1.2rem; background: #111; color: #f4f1ea; }}
    header {{ border-bottom: 2px solid #c9a227; padding-bottom: 0.8rem; }}
    .lane-name {{ font-size: 1.6rem; margin: 0.4rem 0; }}
    .badge {{ display: inline-block; margin: 0.15rem 0.25rem 0.15rem 0; padding: 0.2rem 0.45rem;
              border: 1px solid #e3c56b; color: #e3c56b; font-size: 0.8rem; }}
    .badge.learning {{ border-color: #7ec8e3; color: #7ec8e3; }}
    .lane-btn {{ margin-right: 0.4rem; padding: 0.45rem 0.8rem; }}
    .lane-btn.active {{ background: #c9a227; color: #111; font-weight: 700; }}
    .empty {{ border: 1px dashed #888; padding: 0.8rem; }}
    .learning-card {{ border: 1px solid #7ec8e3; padding: 0.8rem; margin: 0.8rem 0; }}
    .slot {{ border: 1px solid #444; padding: 0.6rem; margin: 0.4rem 0; }}
    pre {{ white-space: pre-wrap; }}
  </style>
</head>
<body data-lane="{_esc(active)}" data-journal="{_esc(journal)}">
  <header>
    <p class="eyebrow">Operator hub · Systems-owned</p>
    <h1 class="lane-name">Active lane: {_esc(name)}</h1>
    {_selector(active)}
    <p class="hard-nos">{_banner_bits(active)}</p>
    <p>{_esc(copy)}{extra}</p>
  </header>
  {journal_html}
  {_viz_html(active)}
  <section class="shareable">
    <h2>Shareable observability</h2>
    <p>Read-only feed for the public hub. Local ingest / live / paper autobet / settle stay on this operator shell.</p>
    <p><a href="docs/observability/observability.json">docs/observability/observability.json</a></p>
  </section>
</body>
</html>
"""


def write_hub_html(dest: Path, *, lane: str = DEFAULT_LANE) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render_hub(lane), encoding="utf-8")
    return dest
