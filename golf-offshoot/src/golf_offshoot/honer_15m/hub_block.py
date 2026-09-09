"""8765 sandbox copy. No combined bankroll. No winner vs Lineage A."""

from __future__ import annotations

import html

from golf_offshoot.honer_15m.books import load_ledger
from golf_offshoot.honer_15m.freeze import load_exam_state
from golf_offshoot.honer_15m.theta import load_theta
from golf_offshoot.honer_15m.watch import load_watch_status

NEAR_2TO1 = 2.0 / 3.0


def sandbox_html() -> str:
    theta = load_theta()
    search = load_ledger("search")
    exam_led = load_ledger("exam")
    exam = load_exam_state()
    watch = load_watch_status()
    th = float(theta.get("theta") or 0)
    near = abs(th - NEAR_2TO1) < 0.02
    label = (
        f"θ={th:.3f} (near live 2/3 — this is the honer book, not a retune of R-SKIP-2TO1-FAVORITE)"
        if near
        else f"θ={th:.3f}"
    )
    exam_line = "exam idle"
    if exam.get("parked"):
        exam_line = f"exam parked: {exam.get('park_reason') or 'futility'}"
    elif exam.get("open"):
        exam_line = (
            f"exam open n={int(exam.get('n') or 0)}/70 frozen_θ={exam.get('frozen_theta')}"
        )
    elif exam.get("completed"):
        exam_line = f"exam complete n={int(exam.get('n') or 0)}"
    return (
        '<section class="panel honer-sandbox">'
        "<h2>honer_15m sandbox</h2>"
        '<p class="help">honer_15m sandbox — not Lineage A, not a keep, books do not merge, zero-fee. '
        "Trading NOT ARMED. Skips are rows. Do not add these bankrolls to Lineage A.</p>"
        f"<pre>{html.escape(label)}\n"
        f"search bankroll={float(search.get('bankroll') or 0):.2f} "
        f"betting_pnl={float(search.get('betting_pnl') or 0):+.2f} "
        f"skips={int(search.get('skips') or 0)} fills={int(search.get('fills') or 0)}\n"
        f"exam bankroll={float(exam_led.get('bankroll') or 0):.2f} "
        f"betting_pnl={float(exam_led.get('betting_pnl') or 0):+.2f} "
        f"skips={int(exam_led.get('skips') or 0)} fills={int(exam_led.get('fills') or 0)}\n"
        f"{exam_line}\n"
        f"watch running={watch.get('running')} cycles={watch.get('cycles')} "
        f"{watch.get('last_summary') or ''}</pre>"
        "</section>"
    )
