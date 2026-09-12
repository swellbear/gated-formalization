"""Honer method invariants. Own artifact. Not on the factory clerical whitelist."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from golf_offshoot.honer_15m.freeze import exam_is_open, load_exam_state
from golf_offshoot.honer_15m.keep import can_keep, load_bar
from golf_offshoot.honer_15m.paths import assert_honer_path, last_tick_path
from golf_offshoot.honer_15m.policy import FREEZE_RULE, load_policy
from golf_offshoot.honer_15m.theta import load_theta
from golf_offshoot.localtime import now

PASS = "PASS"
FAIL = "FAIL"
PKG = Path(__file__).resolve().parent
SRC_ROOT = PKG.parent
DOCS = Path(__file__).resolve().parents[3] / "docs"
MONEY_KEYS = frozenset({"pnl", "d", "bankroll", "winner"})
FORBIDDEN_IMPORTS = {
    "golf_offshoot.learning_lane_15m.paper",
    "golf_offshoot.learning_lane_15m.rules",
    "golf_offshoot.learning_lane_15m.learn",
    "golf_offshoot.learning_lane_15m.watch",
    "golf_offshoot.learning_lane_15m.illustrate",
    "golf_offshoot.learning_lane_15m.runner",
    "golf_offshoot.learning_lane_15m.crew_tick",
    "golf_offshoot.learning_lane_15m.evidence_bar",
    "golf_offshoot.learning_lane_15m.standing",
}
#: Score-time fee_adjust only. Not a live-book import.
ALLOWED_EVIDENCE_BAR_FILES = frozenset({"fee.py", "score.py"})


def _check(check_id: str, title: str, ok: bool, detail: str, evidence: Any = None) -> dict[str, Any]:
    return {
        "id": check_id,
        "title": title,
        "state": PASS if ok else FAIL,
        "detail": detail,
        "evidence": evidence if evidence is not None else {},
    }


def _honer_py_files() -> list[Path]:
    return sorted(p for p in PKG.glob("*.py") if p.is_file())


def _check_no_live_15m_writes() -> dict[str, Any]:
    last: dict[str, Any] = {}
    path = last_tick_path()
    if path.is_file():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                last = payload
        except (OSError, ValueError):
            last = {}
    wrote = bool(last.get("wrote_learning_lane_15m"))
    return _check(
        "no_live_15m_writes",
        "Honer tick wrote no learning_lane_15m path",
        not wrote,
        "last_tick.wrote_learning_lane_15m is false" if not wrote else "honer claimed a live-15m write",
        {"wrote_learning_lane_15m": wrote},
    )


def _check_picker_signatures() -> dict[str, Any]:
    banned = {"pnl", "d", "ledger"}
    found: list[str] = []
    for name in ("picker.py", "brains.py"):
        src = (PKG / name).read_text(encoding="utf-8")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args + node.args.kwonlyargs:
                    if arg.arg in banned:
                        found.append(f"{name}:{node.name}.{arg.arg}")
    ok = not found
    return _check(
        "picker_no_money_params",
        "Picker signatures have no pnl/d/ledger parameters",
        ok,
        "picker is file-order only" if ok else f"banned params: {found}",
        {"found": found},
    )


def _check_forbidden_imports() -> dict[str, Any]:
    hits: list[str] = []
    for path in _honer_py_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in FORBIDDEN_IMPORTS:
                if (
                    node.module == "golf_offshoot.learning_lane_15m.evidence_bar"
                    and path.name in ALLOWED_EVIDENCE_BAR_FILES
                ):
                    continue
                hits.append(f"{path.name}:{node.module}")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in FORBIDDEN_IMPORTS:
                        if (
                            alias.name == "golf_offshoot.learning_lane_15m.evidence_bar"
                            and path.name in ALLOWED_EVIDENCE_BAR_FILES
                        ):
                            continue
                        hits.append(f"{path.name}:{alias.name}")
    ok = not hits
    return _check(
        "forbidden_factory_imports",
        "Forbidden factory imports still absent",
        ok,
        "honer_15m does not import live factory modules" if ok else f"imports: {hits}",
        {"hits": hits},
    )


def _check_code_pkg_dirs() -> dict[str, Any]:
    from golf_offshoot.operator_surface.reload import _CODE_PKG_DIRS

    ok = "honer_15m" not in _CODE_PKG_DIRS
    return _check(
        "code_pkg_dirs_omit_honer",
        "_CODE_PKG_DIRS still omits honer_15m",
        ok,
        "hub re-exec does not watch honer as factory code" if ok else "honer_15m was added to _CODE_PKG_DIRS",
        {"dirs": list(_CODE_PKG_DIRS)},
    )


def _check_hub_html_no_winner() -> dict[str, Any]:
    from golf_offshoot.honer_15m.hub_block import sandbox_html

    html = sandbox_html().lower()
    hits = [word for word in ("combined", "winner") if word in html]
    ok = not hits
    return _check(
        "hub_html_no_combined",
        "Hub honer HTML has no combined/winner",
        ok,
        "actions-only contrast" if ok else f"banned words: {hits}",
        {"hits": hits},
    )


def _freeze_ready_source() -> str:
    src = (PKG / "freeze.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "freeze_ready":
            segment = ast.get_source_segment(src, node)
            if segment:
                return segment
            start = node.lineno - 1
            end = node.end_lineno or node.lineno
            return "\n".join(src.splitlines()[start:end])
    return src


def _check_in_band_freeze() -> dict[str, Any]:
    pol = load_policy()
    st = load_theta()
    body = _freeze_ready_source()
    uses_in_band = "in_band_settled" in body
    uses_raw_n = "search_settled_since_freeze" in body
    rule_ok = str(st.get("freeze_rule") or pol.get("freeze_rule")) == FREEZE_RULE
    ok = rule_ok and uses_in_band and not uses_raw_n
    return _check(
        "freeze_rule_in_band_v1",
        "freeze_rule is in_band_v1 and freeze_ready does not read raw all-settle as the n-gate",
        ok,
        f"freeze_rule={st.get('freeze_rule')} in_band={uses_in_band} raw_n={uses_raw_n}",
        {"freeze_rule": st.get("freeze_rule"), "uses_in_band": uses_in_band, "uses_raw_n": uses_raw_n},
    )


def _check_retired_cannot_freeze() -> dict[str, Any]:
    src = (PKG / "freeze.py").read_text(encoding="utf-8")
    ok = "is_retired" in src and "is_spent" in src
    return _check(
        "retired_spent_cannot_freeze",
        "Retired/spent vectors cannot freeze",
        ok,
        "freeze_ready consults library retired/spent" if ok else "retired/spent veto missing",
        {},
    )


def _check_one_exam() -> dict[str, Any]:
    state = load_exam_state()
    open_flag = bool(state.get("open")) and not state.get("parked")
    ok = (1 if open_flag else 0) <= 1
    if open_flag != exam_is_open() and open_flag:
        ok = False
    return _check(
        "one_exam_open_max",
        "One exam open max",
        ok,
        "at most one open exam" if ok else "exam state is inconsistent",
        {"open": open_flag},
    )


def _check_fee_and_keep() -> dict[str, Any]:
    bar = load_bar()
    keep = can_keep(bar)
    from golf_offshoot.honer_15m.keep import keep_blocked_reason

    reason = keep_blocked_reason(bar)
    omitted = bool(bar.get("fee_omitted", True))
    apply = bar.get("honer_fee_apply") if isinstance(bar.get("honer_fee_apply"), dict) else {}
    sha = str(apply.get("schedule_sha256") or "")
    if omitted:
        ok = (not keep) and reason == "fee omitted"
        detail = "can_keep is false while fee is omitted" if ok else "keep lock failed"
    else:
        ok = (not keep) and reason != "fee omitted" and len(sha) == 64
        detail = (
            "fee applied; keep closed until honer bar binds"
            if ok
            else "fee-apply keep lock failed"
        )
    return _check(
        "keep_closed_until_bind",
        "Keep-lock closed until honer bar bind; fee-apply does not open keep",
        ok,
        detail,
        {"fee_omitted": omitted, "can_keep": keep, "reason": reason, "apply_sha_len": len(sha)},
    )


def _check_http_fetches() -> dict[str, Any]:
    fetches = None
    path = last_tick_path()
    if path.is_file():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            fetches = payload.get("http_fetches") if isinstance(payload, dict) else None
        except (OSError, ValueError):
            fetches = None
    ok = fetches == 0
    return _check(
        "honer_http_fetches_zero",
        "Honer tick http_fetches == 0",
        ok,
        "subscriber only" if ok else f"http_fetches={fetches}",
        {"http_fetches": fetches},
    )


def _check_disagreement_no_money() -> dict[str, Any]:
    from golf_offshoot.two_brains.paths import journal_path

    hits: list[str] = []
    path = journal_path()
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if not isinstance(row, dict):
                continue
            for key in MONEY_KEYS:
                if key in row:
                    hits.append(key)
    ok = not hits
    return _check(
        "disagreement_no_money",
        "Disagreement rows contain none of {pnl,d,bankroll,winner}",
        ok,
        "actions only" if ok else f"money keys: {sorted(set(hits))}",
        {"hits": sorted(set(hits))},
    )


def _check_catalog_file_order() -> dict[str, Any]:
    from golf_offshoot.honer_15m.catalog import catalog_ids, load_catalog, next_family

    payload = load_catalog()
    file_ids = [str(item.get("id")) for item in payload.get("items") or [] if isinstance(item, dict)]
    ids = catalog_ids()
    chained: list[str] = []
    if ids:
        chained.append(ids[0])
        nxt = next_family(ids[0])
        while nxt:
            chained.append(nxt)
            nxt = next_family(nxt)
    ok = ids == file_ids and chained == file_ids
    return _check(
        "catalog_file_order",
        "Catalog file order is picker order (not sorted by tape)",
        ok,
        "next_family follows file order" if ok else f"file={file_ids} picker={ids}",
        {"file_ids": file_ids, "picker_ids": ids},
    )


def _check_clip_brains_file_order() -> dict[str, Any]:
    from golf_offshoot.honer_15m.brains import planned_brain_items, spec_matches_clip
    from golf_offshoot.honer_15m.catalog import load_catalog
    from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD

    items = planned_brain_items()
    ids = [str(row["id"]) for row in items]
    f1 = [row for row in items if str(row.get("family")) == FAMILY_RICH]
    f2 = [row for row in items if str(row.get("family")) == FAMILY_SPREAD]
    activates = [
        str(item.get("activate") or "start")
        for item in (load_catalog().get("items") or [])
        if isinstance(item, dict)
    ]
    ok = (
        spec_matches_clip()
        and len(f1) == 19
        and len(f2) == 11
        and ids[:19] == [str(row["id"]) for row in f1]
        and ids[19:] == [str(row["id"]) for row in f2]
        and all(token == "start" for token in activates)
        and "pnl" not in " ".join(ids)
    )
    return _check(
        "clip_brains_file_order",
        "Clip menu is family then clip, 19+11, both families start",
        ok,
        "19 family-1 + 11 family-2, spec matches, activate=start" if ok else f"ids={len(ids)}",
        {"n": len(ids), "f1": len(f1), "f2": len(f2), "spec_ok": spec_matches_clip()},
    )


def run_invariants() -> dict[str, Any]:
    checks = [
        _check_no_live_15m_writes(),
        _check_picker_signatures(),
        _check_forbidden_imports(),
        _check_code_pkg_dirs(),
        _check_hub_html_no_winner(),
        _check_in_band_freeze(),
        _check_retired_cannot_freeze(),
        _check_one_exam(),
        _check_fee_and_keep(),
        _check_http_fetches(),
        _check_disagreement_no_money(),
        _check_catalog_file_order(),
        _check_clip_brains_file_order(),
    ]
    payload = {
        "lane": "honer_15m",
        "at": now().isoformat(),
        "passed": all(row["state"] == PASS for row in checks),
        "checks": checks,
        "not_on_factory_whitelist": True,
    }
    from golf_offshoot.honer_15m.paths import invariants_path

    path = invariants_path()
    assert_honer_path(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def format_invariants(payload: dict[str, Any] | None = None) -> str:
    data = payload if payload is not None else run_invariants()
    lines = ["honer invariants  not factory whitelist"]
    for row in data.get("checks") or []:
        lines.append(f"  {row.get('state')}  {row.get('id')}  {row.get('detail')}")
    lines.append("passed" if data.get("passed") else "FAILED")
    return "\n".join(lines)
