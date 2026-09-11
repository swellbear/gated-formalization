"""decide_golf: complete-gate screen. Stake lives in allocate. Skip is a recorded decision."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from golf_offshoot.golf_kalshi.brain import PlayerBrain, p_for_market
from golf_offshoot.golf_kalshi.fees import edge_after_fee, quote_snapshot, taker_fee
from golf_offshoot.golf_kalshi.matcher import extract_player_name, match_market_player, quarantine_row
from golf_offshoot.golf_kalshi.paper import halt_new_fills
from golf_offshoot.golf_kalshi.recipe import LISTED_HAIRCUT, WalletRecipe, recipe_v1
from golf_offshoot.golf_kalshi.sleeves import classify_sleeve
from golf_offshoot.localtime import isoformat_now


@dataclass
class GolfDecision:
    action: str
    reason: str
    stake: float = 0.0
    sleeve: str = "week"
    player_id: str | None = None
    player_name: str = ""
    model_p: float | None = None
    yes_ask: float | None = None
    fee: float | None = None
    edge_after_fee: float | None = None
    quote: dict[str, Any] = field(default_factory=dict)
    quarantine: dict[str, str] | None = None
    ticker: str = ""
    market: dict[str, Any] = field(default_factory=dict)
    field_source: str = ""
    tour_haircut: float = 1.0

    @property
    def fill(self) -> bool:
        return self.action == "fill"

    @property
    def worthy(self) -> bool:
        return self.action in {"fill", "worthy"}


def _skip(
    reason: str,
    market: dict[str, Any],
    *,
    sleeve: str = "week",
    player_id: str | None = None,
    player_name: str = "",
    model_p: float | None = None,
    quarantine: dict[str, str] | None = None,
    yes_ask: float | None = None,
    field_source: str = "",
) -> GolfDecision:
    declared = isoformat_now()
    return GolfDecision(
        action="skip",
        reason=reason,
        sleeve=sleeve,
        player_id=player_id,
        player_name=player_name or extract_player_name(market),
        model_p=model_p,
        yes_ask=yes_ask if yes_ask is not None else market.get("yes_ask"),
        quote=quote_snapshot(market, stake=0.0, fee=None, declared_at=declared),
        quarantine=quarantine,
        ticker=str(market.get("ticker") or ""),
        market=market,
        field_source=field_source,
    )


def _field_source(
    market: dict[str, Any],
    brain: PlayerBrain | None,
    field_source: str,
    tour_haircut: float,
) -> tuple[str, float]:
    from golf_offshoot.golf_kalshi.espn_bind import event_key_for

    event_key = event_key_for(market)
    src = field_source
    if not src and brain is not None and hasattr(brain, "field_source"):
        try:
            src = str(brain.field_source(event_key) or "")
        except Exception:
            src = ""
    haircut = float(tour_haircut)
    if src == "kalshi_listed" and haircut == 1.0:
        haircut = LISTED_HAIRCUT
    return src, haircut


def screen_golf(
    market: dict[str, Any],
    book: dict[str, Any],
    recipe: WalletRecipe | None = None,
    brain: PlayerBrain | None = None,
    *,
    budget_blocked: bool = False,
    live_scale: float = 1.0,
    tour_haircut: float = 1.0,
    field_source: str = "",
    halt_fills: bool = True,
) -> GolfDecision:
    """Complete gate. Does not attach money. Does not place orders."""
    del live_scale
    rec = recipe or recipe_v1()
    sleeve = classify_sleeve(market)
    ticker = str(market.get("ticker") or "")
    yes_ask = market.get("yes_ask")
    src, haircut = _field_source(market, brain, field_source, tour_haircut)
    if halt_fills:
        halted, halt_why = halt_new_fills(book, rec)
        if halted:
            return _skip(f"halt:{halt_why}", market, sleeve=sleeve, yes_ask=yes_ask, field_source=src)
    if budget_blocked:
        return _skip("budget", market, sleeve=sleeve, yes_ask=yes_ask, field_source=src)
    if yes_ask is None:
        return _skip("no_quote", market, sleeve=sleeve, field_source=src)
    try:
        yes_f = float(yes_ask)
    except (TypeError, ValueError):
        return _skip("no_quote", market, sleeve=sleeve, field_source=src)
    if yes_f <= 0 or yes_f >= 1:
        return _skip("no_quote", market, sleeve=sleeve, field_source=src)
    if not market.get("fee_multiplier_present") or market.get("fee_multiplier") is None:
        return _skip("no_fee_multiplier", market, sleeve=sleeve, yes_ask=yes_f, field_source=src)
    if brain is None:
        return _skip("no_field", market, sleeve=sleeve, yes_ask=yes_f, field_source=src)
    from golf_offshoot.golf_kalshi.espn_bind import event_key_for

    event_key = event_key_for(market)
    candidates = brain.field_candidates(event_key)
    if not candidates:
        q = quarantine_row(market, reason="no_field")
        return _skip("no_field", market, sleeve=sleeve, yes_ask=yes_f, quarantine=q, field_source=src)
    player_id = match_market_player(market, candidates)
    name = extract_player_name(market)
    if not player_id:
        q = quarantine_row(market, reason="unmatched")
        return _skip(
            "unmatched",
            market,
            sleeve=sleeve,
            player_name=name,
            yes_ask=yes_f,
            quarantine=q,
            field_source=src,
        )
    raw_p = p_for_market(brain, player_id, market)
    if raw_p is None:
        return _skip(
            "no_model_p",
            market,
            sleeve=sleeve,
            player_id=player_id,
            player_name=name,
            yes_ask=yes_f,
            field_source=src,
        )
    model_p = float(raw_p) * float(haircut)
    probe = rec.min_stake
    if float(model_p) - yes_f < rec.min_edge:
        return _skip(
            "no_edge",
            market,
            sleeve=sleeve,
            player_id=player_id,
            player_name=name,
            model_p=model_p,
            yes_ask=yes_f,
            field_source=src,
        )
    fee = taker_fee(yes_f, probe, fee_multiplier=market.get("fee_multiplier"))
    if fee is None:
        return _skip(
            "no_fee_multiplier",
            market,
            sleeve=sleeve,
            player_id=player_id,
            player_name=name,
            model_p=model_p,
            yes_ask=yes_f,
            field_source=src,
        )
    edge = edge_after_fee(float(model_p), yes_f, probe, fee_multiplier=market.get("fee_multiplier"))
    if edge is None or edge <= 0:
        return _skip(
            "no_edge",
            market,
            sleeve=sleeve,
            player_id=player_id,
            player_name=name,
            model_p=model_p,
            yes_ask=yes_f,
            field_source=src,
        )
    declared = isoformat_now()
    return GolfDecision(
        action="worthy",
        reason="edge_after_fee",
        stake=0.0,
        sleeve=sleeve,
        player_id=player_id,
        player_name=name,
        model_p=float(model_p),
        yes_ask=yes_f,
        fee=fee,
        edge_after_fee=edge,
        quote=quote_snapshot(market, stake=0.0, fee=fee, declared_at=declared),
        ticker=ticker,
        market=market,
        field_source=src,
        tour_haircut=haircut,
    )


def decide_golf(
    market: dict[str, Any],
    book: dict[str, Any],
    recipe: WalletRecipe | None = None,
    brain: PlayerBrain | None = None,
    *,
    budget_blocked: bool = False,
    live_scale: float = 1.0,
    tour_haircut: float = 1.0,
    field_source: str = "",
) -> GolfDecision:
    """Consult the advisor. Skip when the brain cannot see. Size via allocate."""
    rec = recipe or recipe_v1()
    screened = screen_golf(
        market,
        book,
        rec,
        brain,
        budget_blocked=budget_blocked,
        live_scale=live_scale,
        tour_haircut=tour_haircut,
        field_source=field_source,
    )
    if not screened.worthy:
        return screened
    from golf_offshoot.golf_kalshi.allocate import attach_stake

    return attach_stake(screened, book, rec, live_scale=live_scale)
