"""Quarantined replay scorer: R-SKIP-COINFLIP vs fill-all on lineage A.

Does not change fills. Does not bind the bar. Does not increment
``trials_to_date``. Writes gitignored ``latest/score_15m.json`` (and a
matching Operator-note-shaped markdown). Never ``manifest.json``.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar
from golf_offshoot.learning_lane_15m.paths import (
    assert_not_golf_path,
    latest_dir_15m,
    paper_dir_15m,
)
from golf_offshoot.learning_lane_15m.rules import decide, load_rules
from golf_offshoot.localtime import isoformat_now, to_eastern

SKIP_RULE_ID = "R-SKIP-COINFLIP"
BASELINE_RULE_ID = "R-BASELINE-FILL-ALL"
SCORE_JSON_NAME = "score_15m.json"
SCORE_NOTE_NAME = "score_15m.md"

LINEAGE_B = "KXBTC15M-26SEP071445-45"
GAP_TICKER = "KXBTC15M-26SEP072245"
MISSING_JOIN = "KXBTC15M-26SEP071500-00"

_NON_BOOK = frozenset(
    {
        "ledger.json",
        "watch_learning_lane_15m.json",
        "watch.json",
        SCORE_JSON_NAME,
        SCORE_NOTE_NAME,
    }
)

_GAP_TOKEN = "072245"
_MISSING_TOKEN = "071500"
_LINEAGE_B_TOKEN = "071445"


def ceil_cent(amount: float) -> float:
    """Round up to the cent — RUN-ONLY PROPOSED 01 / bar draft rounding.

    ``round`` first so ``0.02065 * 100`` does not arrive as ``2.0649999999999995``.
    """
    return math.ceil(round(float(amount) * 100.0, 9)) / 100.0


def fee_for_fill(
    posted_yes: float,
    stake: float = 1.0,
    *,
    k: float = 0.07,
) -> float:
    """Entry-side taker fee: ``ceil_cent(k * stake * (1 - posted_yes))``."""
    return ceil_cent(float(k) * float(stake) * (1.0 - float(posted_yes)))


def fee_adjust(
    recorded_pnl: float,
    posted_yes: float,
    stake: float = 1.0,
    *,
    filled: bool = True,
    k: float = 0.07,
) -> float:
    """Recorded (zero-fee) pnl minus the entry fee. A skip is 0."""
    if not filled:
        return 0.0
    return round(float(recorded_pnl) - fee_for_fill(posted_yes, stake, k=k), 2)


def _as_dt(value: str) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return to_eastern(datetime.fromisoformat(text))


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _fee_k(bar: dict[str, Any]) -> float:
    fee = bar.get("fee_hurdle") or {}
    value = fee.get("k")
    if value is None:
        raise ValueError("evidence bar records no fee_hurdle.k")
    return float(value)


def _stake_usd(bar: dict[str, Any]) -> float:
    fee = bar.get("fee_hurdle") or {}
    value = fee.get("stake_usd")
    return float(value) if value is not None else 1.0


def _first_look_n(bar: dict[str, Any]) -> int:
    return int((bar.get("looks") or {}).get("first_look_n") or 40)


def _rule_by_id(registry: dict[str, Any], rule_id: str) -> dict[str, Any]:
    for row in registry.get("rules") or []:
        if isinstance(row, dict) and str(row.get("id") or "") == rule_id:
            return row
    raise ValueError(f"{rule_id} is not in the registry")


def close_at_from_window_id(window_id: str) -> str | None:
    """UTC close from ``event__open_utc__close_utc``. None if the book has no bounds."""
    parts = str(window_id or "").split("__")
    if len(parts) >= 3 and parts[-1].strip():
        return parts[-1].strip()
    return None


def _identity_text(payload: dict[str, Any], path: Path) -> str:
    bits = [path.name, str(payload.get("tournament_id") or "")]
    for mv in payload.get("movements") or []:
        if isinstance(mv, dict):
            bits.append(str(mv.get("player_id") or ""))
            bits.append(str(mv.get("player_name") or ""))
    book = payload.get("book") if isinstance(payload.get("book"), dict) else {}
    for pos in book.get("positions") or []:
        if isinstance(pos, dict):
            bits.append(str(pos.get("player_id") or ""))
    return " ".join(bits)


def _ticker_from_book(payload: dict[str, Any], path: Path) -> str:
    for mv in payload.get("movements") or []:
        if isinstance(mv, dict) and mv.get("player_id"):
            return str(mv.get("player_id"))
    tid = str(payload.get("tournament_id") or path.stem)
    return tid.split("__", 1)[0]


def exclusion_reason(text: str) -> str | None:
    blob = str(text or "")
    if _LINEAGE_B_TOKEN in blob or LINEAGE_B in blob:
        return "lineage B; never in n or mean"
    if _GAP_TOKEN in blob:
        return "072245 gap; not invented"
    if _MISSING_TOKEN in blob:
        return "missing paper join; no invented pnl"
    return None


def posted_yes_from_book(payload: dict[str, Any]) -> float | None:
    for mv in payload.get("movements") or []:
        if not isinstance(mv, dict):
            continue
        raw = mv.get("model_win")
        if raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if 0.0 < value < 1.0:
            return value
    book = payload.get("book") if isinstance(payload.get("book"), dict) else {}
    for pos in book.get("positions") or []:
        if not isinstance(pos, dict):
            continue
        for key in ("fill_price", "entry_market_p", "entry_model_p"):
            raw = pos.get(key)
            if raw is None:
                continue
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            if 0.0 < value < 1.0:
                return value
    return None


def stake_from_book(payload: dict[str, Any], *, default: float = 1.0) -> float:
    for mv in payload.get("movements") or []:
        if not isinstance(mv, dict):
            continue
        raw = mv.get("stake_after")
        if raw is None:
            raw = mv.get("stake_delta")
        if raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value > 0:
            return value
    return float(default)


def _journal_tickers() -> list[str]:
    path = latest_dir_15m() / "journal.json"
    payload = _read_json(path)
    out: list[str] = []
    for row in payload.get("windows") or []:
        if not isinstance(row, dict):
            continue
        ticker = str(row.get("ticker") or "")
        if ticker:
            out.append(ticker)
    return out


def _paper_books() -> list[tuple[Path, dict[str, Any]]]:
    root = paper_dir_15m()
    if not root.is_dir():
        return []
    out: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.glob("*.json")):
        if path.name.lower() in _NON_BOOK:
            continue
        payload = _read_json(path)
        if payload:
            out.append((path, payload))
    return out


def _student_t_sf(t: float, df: float) -> float:
    """P(T > t) for Student's t. Stdlib; no scipy."""
    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    x = df / (df + float(t) * float(t))
    tail = 0.5 * _betainc(df / 2.0, 0.5, x)
    return tail if t > 0 else 1.0 - tail


def _betacf(a: float, b: float, x: float) -> float:
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-16:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + b * math.log(1.0 - x)
        + a * math.log(x)
    ) * _betacf(b, a, 1.0 - x) / b


def paired_t_mean_le_zero(d: list[float]) -> dict[str, Any]:
    """One-sided paired t-test, H0: mean(d) <= 0. The draft bar's clause (1)."""
    n = len(d)
    if n < 2:
        return {"n": n, "mean_d": None, "p_value": None, "t": None}
    mean = sum(d) / n
    var = sum((v - mean) ** 2 for v in d) / (n - 1)
    sd = math.sqrt(var)
    se = sd / math.sqrt(n) if sd else 0.0
    t = mean / se if se else 0.0
    return {
        "n": n,
        "mean_d": round(mean, 6),
        "sd_d": round(sd, 6),
        "se": round(se, 6),
        "t": round(t, 6),
        "p_value": round(_student_t_sf(t, n - 1), 8) if se else None,
        "h0": "mean(d) <= 0",
    }


def format_operator_note(payload: dict[str, Any]) -> str:
    """Operator-note-shaped quarantine. Not an ADMIT. binding: false."""
    n = payload.get("n_eligible")
    scored = payload.get("scored")
    lines = [
        "# Operator note — replay score (quarantined)",
        "",
        "**Not an ADMIT.** Not Softened. Not a dated record. Not a dashboard figure.",
        f"**Lane:** `learning_lane_15m` · series `KXBTC15M` · `lab_admits={payload.get('lab_admits')}`",
        f"**Binding?** **{payload.get('binding')}.** Draft bar. This write does not bind it.",
        f"**Evidence:** replay ≠ lived. `execution={payload.get('execution')}`.",
        f"**trials_to_date:** {payload.get('trials_to_date')} (not incremented).",
        f"**n eligible:** {n} · **scored:** {scored}",
        "",
        "Fee-accurate figures live in this note / `latest/score_15m.json` only.",
        "They do not go in `manifest.json`, the digest, the hub, or `records[]`.",
        "",
        "Lineage B is never in n or mean. `072245` and missing joins are not invented.",
        "Wake remains a doorbell. Paper fills are unchanged.",
        "Trading **NOT ARMED**.",
    ]
    if not scored:
        lines.extend(
            [
                "",
                f"n < {payload.get('first_look_n')}: **not scored** (count only; no peeking t-test).",
            ]
        )
    return "\n".join(lines) + "\n"


def score_replay(*, now_iso: str | None = None) -> dict[str, Any]:
    """Replay R-SKIP-COINFLIP vs fill-all. Count-only when n < first_look_n."""
    registry = load_rules()
    bar = load_evidence_bar()
    skip_rule = _rule_by_id(registry, SKIP_RULE_ID)
    k = _fee_k(bar)
    stake_default = _stake_usd(bar)
    first_look_n = _first_look_n(bar)
    trials = int(registry.get("trials_to_date") or 0)
    lab_admits = bool(registry.get("lab_admits"))
    binding = bool(bar.get("binding"))
    delta = float((bar.get("distinguishable") or {}).get("effect_floor_usd_per_window") or 0.28)
    alpha = 0.05 / (trials + 1)

    excluded: list[dict[str, str]] = []
    seen_excluded: set[str] = set()

    def _note_excluded(ticker: str, reason: str) -> None:
        key = f"{ticker}|{reason}"
        if key in seen_excluded:
            return
        seen_excluded.add(key)
        excluded.append({"ticker": ticker, "reason": reason})

    for ticker in _journal_tickers():
        reason = exclusion_reason(ticker)
        if reason:
            _note_excluded(ticker, reason)

    ineligible_n = 0
    eligible_meta: list[dict[str, Any]] = []
    for path, payload in _paper_books():
        ticker = _ticker_from_book(payload, path)
        ident = _identity_text(payload, path)
        reason = exclusion_reason(ident) or exclusion_reason(ticker)
        if reason:
            _note_excluded(ticker, reason)
            continue
        close_at = close_at_from_window_id(str(payload.get("tournament_id") or ""))
        if not close_at:
            continue
        if not payload.get("settled_at"):
            continue
        if payload.get("settlement_pnl") is None:
            continue
        try:
            _as_dt(close_at)
        except ValueError:
            continue
        posted = posted_yes_from_book(payload)
        if posted is None:
            continue
        verdict = decide(skip_rule, posted_yes=posted, close_at=close_at)
        if not verdict.get("eligible") or verdict.get("action") == "ineligible":
            ineligible_n += 1
            continue
        if verdict.get("action") not in {"skip", "fill"}:
            continue
        eligible_meta.append(
            {
                "ticker": ticker,
                "window_id": str(payload.get("tournament_id") or path.stem),
                "close_at": close_at,
                "close_dt": _as_dt(close_at),
                "posted_yes": posted,
                "recorded_pnl": float(payload["settlement_pnl"]),
                "stake": stake_from_book(payload, default=stake_default),
                "verdict": verdict,
            }
        )

    eligible_meta.sort(key=lambda row: (row["close_dt"], row["ticker"]))
    n_eligible = len(eligible_meta)
    held_out_ids = [row["window_id"] for row in eligible_meta[first_look_n:]]
    payload: dict[str, Any] = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "series": "KXBTC15M",
        "rule_id": SKIP_RULE_ID,
        "baseline_rule_id": BASELINE_RULE_ID,
        "scored_at": now_iso or isoformat_now(),
        "binding": binding,
        "admit": False,
        "lab_admits": lab_admits,
        "trading_armed": False,
        "never_auto_bet": True,
        "replay": True,
        "lived": False,
        "execution": bool(skip_rule.get("execution")),
        "replay_vs_lived": "replay ≠ lived",
        "trials_to_date": trials,
        "trials_to_date_incremented": False,
        "first_look_n": first_look_n,
        "n_eligible": n_eligible,
        "n_ineligible": ineligible_n,
        "n_held_out": len(held_out_ids),
        "held_out_window_ids": held_out_ids,
        "eligible_window_ids": [row["window_id"] for row in eligible_meta],
        "excluded": excluded,
        "fee_hurdle": {
            "k": k,
            "stake_usd": stake_default,
            "rounding": "ceil to the cent",
            "formula": "fee = ceil_cent(k * stake * (1 - posted_yes))",
            "display": (
                "fee-accurate figures live in the score note / Operator note only; "
                "never hub, digest, manifest, records[]"
            ),
        },
        "framing": (
            "Quarantined replay arithmetic. Not an ADMIT, not edge, not a "
            "track record, not lived execution, not a hub figure."
        ),
    }

    if n_eligible < first_look_n:
        payload["scored"] = False
        payload["reason"] = (
            f"n={n_eligible} < {first_look_n}; not scored (count only; no peeking t-test)"
        )
        return payload

    l1 = eligible_meta[:first_look_n]
    rows: list[dict[str, Any]] = []
    for row in l1:
        action = str(row["verdict"]["action"])
        skip = action == "skip"
        base_adj = fee_adjust(
            row["recorded_pnl"], row["posted_yes"], row["stake"], filled=True, k=k
        )
        rule_adj = 0.0 if skip else base_adj
        fee = 0.0 if skip else fee_for_fill(row["posted_yes"], row["stake"], k=k)
        d_i = round(rule_adj - base_adj, 2)
        rows.append(
            {
                "window_id": row["window_id"],
                "ticker": row["ticker"],
                "close_at": row["close_at"],
                "posted_yes": row["posted_yes"],
                "action": action,
                "reason": row["verdict"]["reason"],
                "evidence": "replay",
                "recorded_pnl": round(row["recorded_pnl"], 2),
                "fee": fee,
                "pnl_baseline_fee_adj": base_adj,
                "pnl_rule_fee_adj": rule_adj,
                "d": d_i,
            }
        )

    d = [float(r["d"]) for r in rows]
    rule_side = [float(r["pnl_rule_fee_adj"]) for r in rows]
    t_test = paired_t_mean_le_zero(d)
    mean_rule = sum(rule_side) / len(rule_side)
    mean_d = sum(d) / len(d)
    p_value = t_test.get("p_value")
    payload.update(
        {
            "scored": True,
            "look": "L1",
            "n": len(rows),
            "windows": rows,
            "skip_count": sum(1 for r in rows if r["action"] == "skip"),
            "t_test": t_test,
            "alpha": alpha,
            "alpha_formula": "0.05 / (trials_to_date + 1)",
            "effect_floor_usd_per_window": delta,
            "mean_d": round(mean_d, 6),
            "mean_pnl_rule_fee_adj": round(mean_rule, 6),
            "passes_t": bool(p_value is not None and p_value < alpha),
            "passes_effect_floor": mean_d >= delta,
            "positive_side": mean_rule > 0,
            "l2_peeked": False,
        }
    )
    return payload


def write_score(*, now_iso: str | None = None) -> tuple[dict[str, Any], dict[str, str]]:
    """Write quarantined JSON + Operator note under ``latest/``. Not manifest.json."""
    payload = score_replay(now_iso=now_iso)
    latest = latest_dir_15m()
    json_path = latest / SCORE_JSON_NAME
    note_path = latest / SCORE_NOTE_NAME
    assert_not_golf_path(json_path)
    assert_not_golf_path(note_path)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    note_path.write_text(format_operator_note(payload), encoding="utf-8")
    return payload, {"json": str(json_path), "note": str(note_path)}
