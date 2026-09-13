"""F-SKIP-FOREIGN-HORIZON: fill YES or skip. Never fill NO. Not seated."""

from __future__ import annotations

from typing import Any

from golf_offshoot.factory_overlay.library import FOREIGN_HORIZON_ID, FactoryOverlayError
from golf_offshoot.golf_kalshi.sleeves import classify_sleeve, market_horizon

ACTION_FILL = "fill"
ACTION_SKIP = "skip"
POLICY_ID = FOREIGN_HORIZON_ID
FIFTEEN_M_IN_PLAY = "KXBTC15M"
GOLF_FOREIGN_SLEEVE = "slow"
GOLF_FOREIGN_HORIZON = "season"
_EMPTY = {"", "none", "null", "n/a"}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _blank(value: Any) -> str:
    text = _text(value)
    if text.lower() in _EMPTY:
        return ""
    return text


def _verdict(action: str, reason: str) -> dict[str, str]:
    if action not in {ACTION_FILL, ACTION_SKIP}:
        raise FactoryOverlayError(f"{POLICY_ID} expressed {action!r}; only fill or skip")
    return {"policy_id": POLICY_ID, "action": action, "reason": reason, "side": "yes"}


def _nested_market(row: dict[str, Any]) -> dict[str, Any]:
    market = row.get("market")
    return market if isinstance(market, dict) else {}


def _series(row: dict[str, Any]) -> str:
    for key in ("series", "series_ticker"):
        text = _blank(row.get(key))
        if text:
            return text
    market = _nested_market(row)
    for key in ("series_ticker", "series"):
        text = _blank(market.get(key))
        if text:
            return text
    ticker = _blank(row.get("ticker") or row.get("window_id") or row.get("event_ticker"))
    upper = ticker.upper()
    if upper.startswith("KXBTC15M"):
        return FIFTEEN_M_IN_PLAY
    return ""


def _lane(row: dict[str, Any]) -> str:
    lane = _blank(row.get("lane")).lower()
    if lane in {"learning_lane_15m", "15m", "kxbtc15m"}:
        return "15m"
    if lane in {"golf_kalshi", "golf"}:
        return "golf"
    series = _series(row).upper()
    if series == FIFTEEN_M_IN_PLAY or series.startswith("KXBTC15M"):
        return "15m"
    ticker = _blank(row.get("ticker") or row.get("window_id")).upper()
    if ticker.startswith("KXBTC15M"):
        return "15m"
    if _blank(row.get("sleeve")) or _blank(row.get("market_horizon")) or _blank(row.get("horizon")):
        return "golf"
    if (
        _blank(row.get("title"))
        or _blank(row.get("event_title"))
        or _blank(row.get("yes_sub_title"))
        or _nested_market(row)
    ):
        return "golf"
    return "unknown"


def _horizon_fields(row: dict[str, Any]) -> tuple[str, str]:
    observed = _blank(
        row.get("horizon")
        or row.get("settlement_horizon")
        or row.get("market_horizon")
    )
    in_play = _blank(row.get("in_play_class") or row.get("in_play_horizon"))
    market = _nested_market(row)
    if not observed:
        observed = _blank(
            market.get("horizon")
            or market.get("settlement_horizon")
            or market.get("market_horizon")
        )
    if not in_play:
        in_play = _blank(market.get("in_play_class") or market.get("in_play_horizon"))
    return observed, in_play


def _golf_sleeve_and_horizon(row: dict[str, Any]) -> tuple[str, str]:
    sleeve = _blank(row.get("sleeve"))
    horizon = _blank(row.get("market_horizon") or row.get("horizon") or row.get("settlement_horizon"))
    market = _nested_market(row)
    if not sleeve:
        sleeve = _blank(market.get("sleeve"))
    if not horizon:
        horizon = _blank(
            market.get("market_horizon") or market.get("horizon") or market.get("settlement_horizon")
        )
    title = _blank(row.get("title") or market.get("title"))
    probe = market or {
        key: row[key]
        for key in ("title", "event_title", "yes_sub_title", "series_ticker", "ticker", "event_ticker")
        if key in row
    }
    if (not sleeve or not horizon) and (probe or title):
        if not sleeve:
            sleeve = classify_sleeve(market or None, title=title)
        if not horizon:
            horizon = market_horizon(market or None, title=title)
    return sleeve, horizon


def _fifteen_m_series_token(series: str) -> str:
    token = series.strip()
    if not token:
        return ""
    if "-" in token and token.upper().startswith("KXBTC15M-"):
        return FIFTEEN_M_IN_PLAY
    return token


def express(policy: dict[str, Any], row: dict[str, Any] | None) -> dict[str, str]:
    """Fill YES or skip. Missing horizon fills. Never invents a skip or a NO."""
    ident = str((policy or {}).get("id") or "")
    if ident != POLICY_ID:
        raise FactoryOverlayError(f"no expression for {ident or 'missing id'}")
    window = row if isinstance(row, dict) else {}
    observed, in_play = _horizon_fields(window)
    if observed and in_play:
        if observed.lower() != in_play.lower():
            return _verdict(
                ACTION_SKIP,
                f"horizon {observed} is not in-play class {in_play}",
            )
        return _verdict(ACTION_FILL, f"horizon {observed} is the in-play class")
    lane = _lane(window)
    if lane == "15m":
        series = _fifteen_m_series_token(_series(window))
        if not series:
            return _verdict(ACTION_FILL, "missing series; fill YES")
        if series.upper() == FIFTEEN_M_IN_PLAY:
            return _verdict(ACTION_FILL, "KXBTC15M is the in-play 15m class")
        return _verdict(ACTION_SKIP, f"series {series} is not the in-play 15m class")
    if lane == "golf":
        sleeve, horizon = _golf_sleeve_and_horizon(window)
        if not sleeve and not horizon:
            return _verdict(ACTION_FILL, "missing sleeve and horizon; fill YES")
        if sleeve == GOLF_FOREIGN_SLEEVE:
            return _verdict(ACTION_SKIP, "golf sleeve slow is foreign to fast+week")
        if horizon == GOLF_FOREIGN_HORIZON:
            return _verdict(ACTION_SKIP, "golf horizon season is foreign to fast+week")
        return _verdict(ACTION_FILL, "golf horizon is in-play (fast or week)")
    return _verdict(ACTION_FILL, "missing horizon; fill YES")


def decide(row: dict[str, Any] | None = None) -> dict[str, str]:
    """Convenience for the frozen name. Does not seat. Never fill NO."""
    return express({"id": POLICY_ID}, row or {})
