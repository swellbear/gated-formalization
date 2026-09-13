"""Replay frozen P-* names vs fill-all after fees.

Lineage A settled 15m paper books only. Dual lineage is never summed.
Skip books 0 on both sides. Density-fail is a successful search outcome.
Does not write the factory rule registry. Does not ping Lab.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.evidence_bar import FEE_ADJUST_PATH, fee_adjust
from golf_offshoot.learning_lane_15m.rules import DEFAULT_FIRST_LOOK_N, lived_skip_density
from golf_offshoot.localtime import isoformat_now
from golf_offshoot.policy_family.express import ACTION_FILL, ACTION_SKIP, express
from golf_offshoot.policy_family.library import (
    ALLOWED_SERIES,
    COMPARISON_ID,
    FROZEN_IDS,
    LAST_VS_MID_ID,
    PolicyFamilyError,
    STALE_QUOTE_ID,
    lessons_path,
    load_library,
    policy_by_id,
    score_path,
)
from golf_offshoot.repo_paths import repo_root

_BIDASK_RE = re.compile(
    r"yes_bid=(?P<bid>\S+)\s+yes_ask=(?P<ask>\S+)",
    re.IGNORECASE,
)
_LAST_RE = re.compile(
    r"(?:^|\s)(?:last_price_dollars|last_price|last)=(?P<last>\S+)",
    re.IGNORECASE,
)
_LAST_KEYS = ("last", "last_price", "last_price_dollars")
_SKIP_FILES = frozenset({"ledger.json", "rule_decisions.json"})


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _series_ok(ticker: str, window_id: str) -> bool:
    blob = f"{ticker} {window_id}"
    return ALLOWED_SERIES in blob


def _parse_bid_ask(text: str) -> tuple[float | None, float | None]:
    match = _BIDASK_RE.search(str(text or ""))
    if not match:
        return None, None

    def _one(raw: str) -> float | None:
        token = str(raw or "").strip()
        if token.lower() in {"none", "null", "n/a", ""}:
            return None
        try:
            return float(token)
        except (TypeError, ValueError):
            return None

    return _one(match.group("bid")), _one(match.group("ask"))


def _last_from_mapping(blob: Any) -> float | None:
    """Last from fields already present. Never posted_yes / paper_mark."""
    if not isinstance(blob, dict):
        return None
    for key in _LAST_KEYS:
        raw = blob.get(key)
        if raw is None or raw == "":
            continue
        token = str(raw).strip()
        if token.lower() in {"none", "null", "n/a"}:
            continue
        try:
            return float(token)
        except (TypeError, ValueError):
            continue
    return None


def _last_from_reason(text: str) -> float | None:
    match = _LAST_RE.search(str(text or ""))
    if not match:
        return None
    token = str(match.group("last") or "").strip()
    if token.lower() in {"none", "null", "n/a", ""}:
        return None
    try:
        return float(token)
    except (TypeError, ValueError):
        return None


def _carry_last(
    *,
    decided: dict[str, Any],
    payload: dict[str, Any],
    move: dict[str, Any],
    bus: Any,
) -> float | None:
    """Last already on this book's decision / quote_bus / reason. Do not invent."""
    blobs: list[Any] = [decided, payload, move]
    if isinstance(bus, dict):
        blobs.append(bus)
    for blob in blobs:
        found = _last_from_mapping(blob)
        if found is not None:
            return found
        if not isinstance(blob, dict):
            continue
        for nested_key in ("quote_bus", "quote_snapshot"):
            found = _last_from_mapping(blob.get(nested_key))
            if found is not None:
                return found
    return _last_from_reason(str(move.get("reason_technical") or ""))


def _kalshi_from_winner(raw: Any) -> str:
    text = str(raw or "").strip().lower()
    if text in {"yes", "no"}:
        return text
    if text.startswith("kalshi:"):
        tail = text.split(":", 1)[-1].strip()
        if tail in {"yes", "no"}:
            return tail
    return ""


def load_kalshi_results(settlements_dir: Path | None) -> dict[str, str]:
    """Official Kalshi yes/no from settlements/*.json. Never invent. Never lineage B."""
    out: dict[str, str] = {}
    if settlements_dir is None or not settlements_dir.is_dir():
        return out
    for path in settlements_dir.glob("*.json"):
        payload = _load_json(path)
        result = str(payload.get("kalshi_result") or payload.get("result") or "").strip().lower()
        ticker = str(payload.get("ticker") or "")
        if result in {"yes", "no"} and ticker:
            out[ticker] = result
        for row in payload.get("rows") or []:
            if not isinstance(row, dict):
                continue
            r = str(row.get("kalshi_result") or "").strip().lower()
            t = str(row.get("ticker") or "")
            if r in {"yes", "no"} and t:
                out[t] = r
    return out


def _first_new_bet(payload: dict[str, Any]) -> dict[str, Any]:
    for row in payload.get("movements") or []:
        if isinstance(row, dict) and str(row.get("kind") or "") == "new_bet":
            return row
    return {}


def _positions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    book = payload.get("book") or {}
    rows = book.get("positions") if isinstance(book, dict) else None
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    return []


def gather_lineage_a_windows(
    paper_dir: Path,
    *,
    settlements_dir: Path | None = None,
    decisions: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Settled lineage-A paper books with a Kalshi result and a recorded pnl.

    Does not read the published hub manifest (lineage B). Does not backfill
    gaps. Unmeasured (result, no book) is not a loss and is not a row.
    """
    results = load_kalshi_results(settlements_dir)
    if decisions is None:
        blob = _load_json(paper_dir / "rule_decisions.json")
        decisions = blob.get("decisions") if isinstance(blob.get("decisions"), dict) else {}
    windows: list[dict[str, Any]] = []
    if not paper_dir.is_dir():
        return windows
    for path in sorted(paper_dir.glob("*.json")):
        if path.name in _SKIP_FILES:
            continue
        payload = _load_json(path)
        if not payload.get("settled_at"):
            continue
        raw_pnl = payload.get("settlement_pnl")
        if not isinstance(raw_pnl, (int, float)):
            continue
        positions = _positions(payload)
        move = _first_new_bet(payload)
        ticker = str(
            (positions[0].get("player_id") if positions else "")
            or move.get("player_id")
            or payload.get("tournament_id")
            or path.stem
        )
        window_id = str(payload.get("tournament_id") or ticker)
        if not _series_ok(ticker, window_id):
            continue
        decided = decisions.get(ticker) if isinstance(decisions.get(ticker), dict) else {}
        close_at = str(decided.get("close_at") or "")
        if not close_at:
            tid = str(payload.get("tournament_id") or "")
            parts = tid.split("__")
            if len(parts) >= 3:
                close_at = parts[-1]
        posted = decided.get("posted_yes")
        if posted is None and positions:
            posted = positions[0].get("entry_market_p")
        if posted is None:
            posted = move.get("model_win")
        try:
            posted_f = float(posted)
        except (TypeError, ValueError):
            continue
        fill_at = str(
            decided.get("at")
            or move.get("at")
            or payload.get("locked_at")
            or ""
        )
        result = _kalshi_from_winner(payload.get("settlement_winner"))
        if result not in {"yes", "no"}:
            result = results.get(ticker) or results.get(str(decided.get("ticker") or ""))
        if result not in {"yes", "no"}:
            continue
        bid, ask = _parse_bid_ask(str(move.get("reason_technical") or ""))
        stake = decided.get("stake")
        if not isinstance(stake, (int, float)):
            stake = move.get("stake_after") or 1.0
        quote_age = decided.get("quote_age_s")
        if quote_age is None:
            quote_age = decided.get("quote_bus_age_s")
        if quote_age is None:
            quote_age = payload.get("quote_age_s")
        quote_fetched = (
            decided.get("quote_fetched_at")
            or decided.get("quote_snapshot_at")
            or payload.get("quote_fetched_at")
        )
        bus = decided.get("quote_bus") or payload.get("quote_bus")
        if quote_fetched is None and isinstance(bus, dict):
            quote_fetched = bus.get("fetched_at") or bus.get("quote_fetched_at")
        if quote_age is None and isinstance(bus, dict):
            quote_age = bus.get("quote_age_s") or bus.get("age_s")
        last = _carry_last(decided=decided, payload=payload, move=move, bus=bus)
        windows.append(
            {
                "window_id": window_id,
                "ticker": ticker,
                "close_at": close_at,
                "fill_at": fill_at,
                "decision_at": fill_at,
                "posted_yes": posted_f,
                "yes_bid": bid,
                "yes_ask": ask,
                "last": last,
                "recorded_pnl": float(raw_pnl),
                "stake": float(stake or 1.0),
                "kalshi_result": result,
                "settled_at": str(payload.get("settled_at") or ""),
                "quote_age_s": quote_age,
                "quote_fetched_at": quote_fetched,
                "quote_bus": bus if isinstance(bus, dict) else None,
            }
        )
    windows.sort(key=lambda row: (str(row.get("close_at") or ""), str(row.get("ticker") or "")))
    return windows


def _fee_adj(window: dict[str, Any], *, filled: bool) -> float:
    # Always the gym evidence-bar fee. Library tmp roots are not a second fee.
    if not filled:
        return fee_adjust(None, None, None, filled=False)
    return fee_adjust(
        float(window["recorded_pnl"]),
        float(window["posted_yes"]),
        float(window.get("stake") or 1.0),
        filled=True,
    )


def _lesson_line(card: dict[str, Any]) -> str:
    ident = str(card.get("id") or "")
    kind = str(card.get("card") or "")
    if kind == "comparison_book":
        return (
            "Comparison book. Same gross pnl recipe as factory fill-all, then "
            "fee_adjust. Not an ADMIT."
        )
    if kind in {"density_fail", "undecidable"}:
        density = card.get("density") or {}
        reason = str(density.get("reason") or "density-fail")
        return (
            f"Search done: {reason}. Not a t-test vs δ. Do not retune {ident}."
        )
    if kind == "untestable":
        n = int(card.get("n") or 0)
        skip_count = int(card.get("skip_count") or 0)
        if ident == LAST_VS_MID_ID:
            return (
                f"Search done: skip never fired (skip_count {skip_count}/{n}). "
                "Missing last or missing mid fills; skip 0 is untestable, not a "
                "reason to retune 0.02. Not a t-test vs δ."
            )
        return (
            f"Search done: skip never fired (skip_count {skip_count}/{n}). "
            f"Healthy quote bus / missing age is untestable, not a reason to "
            f"retune 180. Not a t-test vs δ."
        )
    if kind == "count_only":
        n = int(card.get("n") or 0)
        skip_count = int(card.get("skip_count") or 0)
        return (
            f"Count-only: n {n} < first_look_n {DEFAULT_FIRST_LOOK_N}. "
            f"skip_count {skip_count}/{n}. Not scored. Not a t-test vs δ. "
            f"Do not retune {ident}."
        )
    if kind == "park_vs_fill_all":
        return (
            f"skip_count clears the 10/n floor but fee-adj selected-fill pnl "
            f"does not beat P-FILL-ALL-YES. Parked on this lessons file. "
            f"Not a factory PARK. Not Operator."
        )
    if kind == "beats_fill_all":
        return (
            "Fee-adj selected-fill pnl beats P-FILL-ALL-YES on this book. "
            "Lesson only. Lab still gates later naming / exam / seating. "
            "Do not ping Lab."
        )
    return f"{ident}: search card written. Not an ADMIT."


def replay(
    policy: dict[str, Any],
    windows: list[dict[str, Any]],
    *,
    fill_all_pnl: float | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """One named policy vs fill-all after fees. Not a t-test. Not an ADMIT."""
    ident = str(policy.get("id") or "")
    rows: list[dict[str, Any]] = []
    selected = 0.0
    baseline = 0.0
    skip_count = 0
    for window in windows:
        verdict = express(policy, window)
        if verdict["action"] not in {ACTION_FILL, ACTION_SKIP}:
            raise PolicyFamilyError(f"{ident} produced {verdict['action']}; fill-NO does not exist")
        skip = verdict["action"] == ACTION_SKIP
        if skip:
            skip_count += 1
        adj = _fee_adj(window, filled=not skip)
        base = _fee_adj(window, filled=True)
        selected += adj
        baseline += base
        rows.append(
            {
                "window_id": window.get("window_id") or "",
                "action": verdict["action"],
                "reason": verdict["reason"],
                "pnl_policy_fee_adj": adj,
                "pnl_fill_all_fee_adj": base,
            }
        )
    n = len(windows)
    selected = round(selected, 4)
    baseline = round(float(fill_all_pnl) if fill_all_pnl is not None else baseline, 4)
    expected = policy.get("expected_skip_rate")
    try:
        expected_f = float(expected) if expected is not None else None
    except (TypeError, ValueError):
        expected_f = None
    density = lived_skip_density(skip_count, n, expected_rate=expected_f)
    density_fail = not bool(density["passes"])
    undecidable = bool(density["undecidable"])
    beats = selected > baseline
    if ident == COMPARISON_ID:
        card_kind = "comparison_book"
        density_fail = False
        undecidable = False
        beats = False
    elif n < DEFAULT_FIRST_LOOK_N:
        card_kind = "count_only"
        beats = False
    elif ident in {STALE_QUOTE_ID, LAST_VS_MID_ID} and skip_count == 0:
        card_kind = "untestable"
        beats = False
    elif density_fail or undecidable:
        card_kind = "density_fail" if density_fail else "undecidable"
        beats = False
    elif beats:
        card_kind = "beats_fill_all"
    else:
        card_kind = "park_vs_fill_all"
    card = {
        "schema": 1,
        "id": ident,
        "framing": "Search card, not an ADMIT, not a factory PARK, not a Lab ping.",
        "n": n,
        "skip_count": skip_count,
        "skip_rate": round(skip_count / n, 6) if n else 0.0,
        "expected_skip_rate": expected_f,
        "fee_adjust": FEE_ADJUST_PATH,
        "fee_adj_pnl": selected,
        "fill_all_fee_adj_pnl": baseline,
        "beats_fill_all": bool(beats) if ident != COMPARISON_ID else False,
        "density": density,
        "density_fail": bool(density_fail),
        "undecidable": bool(undecidable),
        "card": card_kind,
        "trading_armed": False,
        "lab_admits": False,
        "windows": rows,
    }
    card["lesson"] = _lesson_line(card)
    return card


def replay_family(
    windows: list[dict[str, Any]],
    *,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    """Independent cards in file order. Not skip-together. Not 3^N."""
    load_library(root=root)
    cards = []
    for ident in FROZEN_IDS:
        policy = policy_by_id(ident, root=root)
        cards.append(replay(policy, windows, root=root))
    return cards


def _lessons_payload(cards: list[dict[str, Any]], *, n: int) -> dict[str, Any]:
    rows = []
    for card in cards:
        density = card.get("density") or {}
        rows.append(
            {
                "id": card.get("id"),
                "skip_count": card.get("skip_count"),
                "n": card.get("n"),
                "density_passes": bool((density.get("passes") if card.get("id") != COMPARISON_ID else True)),
                "density_fail": bool(card.get("density_fail")),
                "undecidable": bool(card.get("undecidable")),
                "fee_adj_pnl": card.get("fee_adj_pnl"),
                "fill_all_fee_adj_pnl": card.get("fill_all_fee_adj_pnl"),
                "beats_fill_all": bool(card.get("beats_fill_all")),
                "card": card.get("card"),
                "lesson": card.get("lesson"),
            }
        )
    return {
        "schema": 1,
        "lane": "learning_lane_15m",
        "series": ALLOWED_SERIES,
        "family": "P-FAMILY-SEARCH",
        "framing": (
            "Searcher lessons. Density-fail is a lesson. Beats fill-all on this "
            "book is a lesson, not a Lab ping and not a seated row. Not an ADMIT."
        ),
        "lab_admits": False,
        "trading_armed": False,
        "lineage": "A",
        "n": n,
        "fee_adjust": FEE_ADJUST_PATH,
        "updated_at": isoformat_now(),
        "rows": rows,
    }


def write_lessons(cards: list[dict[str, Any]], *, root: Path | None = None) -> Path:
    dest = lessons_path(root=root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    n = int(cards[0]["n"]) if cards else 0
    dest.write_text(json.dumps(_lessons_payload(cards, n=n), indent=2) + "\n", encoding="utf-8")
    return dest


def write_score(cards: list[dict[str, Any]], *, root: Path | None = None, dest: Path | None = None) -> Path:
    path = dest if dest is not None else score_path(root=root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "series": ALLOWED_SERIES,
        "family": "P-FAMILY-SEARCH",
        "framing": "Gitignored search score. Not an ADMIT. Not a factory L1.",
        "lab_admits": False,
        "trading_armed": False,
        "fee_adjust": FEE_ADJUST_PATH,
        "scored_at": isoformat_now(),
        "cards": [
            {k: v for k, v in card.items() if k != "windows"}
            for card in cards
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def run_search(
    *,
    paper_dir: Path,
    settlements_dir: Path | None = None,
    root: Path | None = None,
    dest_root: Path | None = None,
    score_dest: Path | None = None,
    write: bool = True,
) -> dict[str, Any]:
    """Replay frozen P-* names on lineage-A books. Does not flip execution. Does not ping Lab."""
    windows = gather_lineage_a_windows(paper_dir, settlements_dir=settlements_dir)
    cards = replay_family(windows, root=root)
    out: dict[str, Any] = {
        "n": len(windows),
        "cards": cards,
        "lessons": None,
        "score": None,
    }
    if write:
        write_root = dest_root if dest_root is not None else root
        out["lessons"] = str(write_lessons(cards, root=write_root))
        out["score"] = str(write_score(cards, root=write_root, dest=score_dest))
    return out
