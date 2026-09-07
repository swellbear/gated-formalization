"""Loud mode walls. MOCK/DEMO is never operating evidence. Trading is never armed."""

from __future__ import annotations

from dataclasses import dataclass, field

MODE_OPERATING = "operating"
MODE_MOCK = "mock_demo"

PHASE_1_OBSERVATION = "PHASE 1 OBSERVATION"
LIVE_DATA = "LIVE DATA"
NOT_TRADING = "NOT TRADING"
NOT_ARMED = "NOT ARMED"
CASH_BADGE = "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH"
MOCK_BANNER = "OFFLINE DEMO — MOCK DATA"
PAPER_ONLY = "PAPER OBSERVATION ONLY"
AI_NO_CASH = "AI: NO CASH IN/OUT"

_MOCK_MARKERS = (
    "OFFLINE DEMO — MOCK DATA",
    "OFFLINE DEMO -- MOCK DATA",
    "OFFLINE DEMO",
    "MOCK DATA",
    "MOCK / PAPER",
    "PAPER / MOCK",
)


@dataclass(frozen=True)
class ModeWalls:
    mode: str
    title: str
    lines: tuple[str, ...]
    badges: tuple[str, ...]
    is_mock: bool
    trading_armed: bool = False
    cash_human_only: bool = True
    notes: tuple[str, ...] = field(default_factory=tuple)

    def render_text(self) -> str:
        bar = "=" * 72
        body = "\n".join(f"  {line}" for line in self.lines)
        badge = "  ·  ".join(self.badges)
        return f"{bar}\n  {self.title}\n{body}\n  {badge}\n{bar}"


def is_mock_or_demo_text(text: str | None) -> bool:
    blob = (text or "").upper()
    if not blob:
        return False
    return any(marker.upper() in blob for marker in _MOCK_MARKERS)


def build_mode_walls(*, mock: bool = False, live_data: bool = False) -> ModeWalls:
    """Always-on walls. Trading stays NOT ARMED. Cash stays human-only."""
    if mock:
        return ModeWalls(
            mode=MODE_MOCK,
            title=MOCK_BANNER,
            lines=(
                "This is a labeled mock/demo path.",
                "It is not live, not historical, and not operating evidence.",
                "Do not read ranks, edges, or honesty strips from this mode.",
                f"{CASH_BADGE}",
            ),
            badges=(MOCK_BANNER, "NOT OPERATING EVIDENCE", CASH_BADGE),
            is_mock=True,
            notes=("barred from edge/honesty displays",),
        )
    live_line = (
        f"{LIVE_DATA} — ESPN/book feeds on the operating path. This is not a trade ticket."
        if live_data
        else "Operating path. Rankings are observation, not clearance to bet."
    )
    return ModeWalls(
        mode=MODE_OPERATING,
        title=PHASE_1_OBSERVATION,
        lines=(
            live_line,
            f"Trading is {NOT_ARMED}. No place / cancel / auto-bet / one-tap bet.",
            f"Paper bankroll auto-apply is {PAPER_ONLY}. It is not trading armed.",
            f"{CASH_BADGE}",
            "Kalshi is future public-read language only. No account, key, or wallet scope.",
        ),
        badges=(
            PHASE_1_OBSERVATION,
            LIVE_DATA if live_data else "OPERATING PATH",
            NOT_ARMED,
            PAPER_ONLY,
            CASH_BADGE,
        ),
        is_mock=False,
    )
