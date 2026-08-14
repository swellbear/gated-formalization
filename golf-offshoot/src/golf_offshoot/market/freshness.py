"""Live vs pre odds freshness. Stale coupons are labeled; too-old live prices are suppressed."""

from __future__ import annotations

from golf_offshoot.config import ODDS_LIVE_MAX_STALE_SECONDS, ODDS_TTL_LIVE_SECONDS, ODDS_TTL_PRE_SECONDS
from golf_offshoot.data_feeds.base import unavailable_quality
from golf_offshoot.models.schemas import DataQuality, MarketQuote


def odds_ttl_seconds(*, live: bool) -> float:
    return ODDS_TTL_LIVE_SECONDS if live else ODDS_TTL_PRE_SECONDS


def apply_odds_freshness(
    quotes: list[MarketQuote],
    quality: DataQuality,
    *,
    live: bool,
) -> tuple[list[MarketQuote], DataQuality]:
    """If a live refresh fails, do not silently treat an old Winner coupon as current.

    - Cache hit within the mode TTL: pass through, timestamps preserved.
    - Network failed, disk snapshot younger than ODDS_LIVE_MAX_STALE_SECONDS: keep
      quotes, mark STALE_FALLBACK, cut quality.
    - Older than that on a live pass: return no quotes for edges and mark unavailable.
    """
    ttl = odds_ttl_seconds(live=live)
    notes = (quality.notes or "").rstrip()
    policy = f"odds_ttl_policy={'live' if live else 'pre'}_{int(ttl)}s"
    if policy not in notes:
        notes = f"{notes}; {policy}".strip("; ")
    age_s = float(quality.lag_hours or 0.0) * 3600.0
    stale = "STALE_FALLBACK" in notes
    quality = quality.model_copy(update={"notes": notes, "lag_hours": quality.lag_hours})
    if not quotes or quality.missing:
        return quotes, quality
    if live and (stale or age_s > ODDS_LIVE_MAX_STALE_SECONDS):
        if age_s > ODDS_LIVE_MAX_STALE_SECONDS:
            q = unavailable_quality(
                quality.source_name or "market_odds",
                (
                    f"EDGES_SUPPRESSED_STALE: live odds refresh failed or coupon fetch age "
                    f"{age_s:.0f}s exceeds {int(ODDS_LIVE_MAX_STALE_SECONDS)}s. "
                    f"Prices not used for edges/strategy. prior={notes}"
                ),
            )
            q.as_of = quality.as_of
            q.lag_hours = quality.lag_hours
            q.n_observations = quality.n_observations
            return [], q
        quality = quality.model_copy(
            update={
                "score": min(quality.score, 0.55),
                "notes": notes + "; confidence_cut=stale_live_coupon",
            }
        )
    return quotes, quality
