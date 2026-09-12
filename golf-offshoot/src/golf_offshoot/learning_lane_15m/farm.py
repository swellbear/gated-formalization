"""Discovery farm: isolated notebooks on the shared tape.

Never imports honer_15m. Does not steal the selecting chair. Does not
sort keepers by pnl. Does not arm. Not an ADMIT.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.repo_paths import repo_root

FARM_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_FARM.json"
CATALOG_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_MECHANISM_CATALOG.json"
REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
BURNED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_BURNED_CLASSES.json"
EXHAUSTED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_FARM_MENU_EXHAUSTED.json"
SCORECARD_DIR_REL = Path("golf-offshoot") / "docs"
HONER_LATEST_REL = Path("golf-offshoot") / "data" / "honer_15m" / "latest"
HONER_CATALOG_REL = Path("golf-offshoot") / "docs" / "HONER_15M_CATALOG.json"

QUARTET_MINUTES = (0, 15, 30, 45)
HONER_KIND_PREFIX = "HONER-"
FAMILY_AMEND_KIND = "HONER-FAMILY-AMEND"
DATED_HONER_FAMILIES = 2
REASON_CATALOG_EXHAUSTED = "catalog_exhausted"
REASON_EXAM_DEAD = "completed_dead"
FORBIDDEN_FARM_IDS = frozenset({"R-SKIP-COINFLIP", "R-SKIP-2TO1-FAVORITE"})
CLONE_JACCARD = 0.9


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def farm_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / FARM_REL


def exhausted_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / EXHAUSTED_REL


def load_farm(*, root: Path | None = None) -> dict[str, Any]:
    payload = _load_json(farm_path(root=root))
    if not payload:
        return {"schema": 1, "lane": "learning_lane_15m", "notebooks": []}
    notebooks = payload.get("notebooks")
    if not isinstance(notebooks, list):
        payload["notebooks"] = []
    return payload


def load_catalog(*, root: Path | None = None) -> dict[str, Any]:
    return _load_json((root or repo_root()) / CATALOG_REL)


def load_registry(*, root: Path | None = None, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    if registry is not None:
        return registry
    return _load_json((root or repo_root()) / REGISTRY_REL)


def menu_exhausted(*, root: Path | None = None) -> bool:
    payload = _load_json(exhausted_path(root=root))
    return payload.get("exhausted") is True


def write_menu_exhausted(reason: str, *, root: Path | None = None) -> dict[str, Any]:
    payload = {"exhausted": True, "reason": str(reason or ""), "lane": "learning_lane_15m"}
    path = exhausted_path(root=root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def farm_scorecard_path(notebook_id: str, *, root: Path | None = None) -> Path:
    return (root or repo_root()) / SCORECARD_DIR_REL / f"LEARNING_LANE_15M_SCORECARD_{notebook_id}_FARM.json"


def notebook_as_rule(notebook: dict[str, Any]) -> dict[str, Any]:
    params = notebook.get("params") if isinstance(notebook.get("params"), dict) else {}
    return {
        "id": str(notebook.get("id") or ""),
        "declared_at": str(notebook.get("declared_at") or ""),
        "kind": "selection",
        "selects": True,
        "execution": False,
        "params": dict(params),
        "class": str(notebook.get("kind") or ""),
    }


def _clock_minutes(row: dict[str, Any]) -> list[int] | None:
    from golf_offshoot.learning_lane_15m.rules import clock_skip_minutes

    return clock_skip_minutes(notebook_as_rule(row) if "params" in row else row)


def clone_overlap(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    skip_left: set[str] | None = None,
    skip_right: set[str] | None = None,
) -> bool:
    """True when two notebooks skip the same product set. Does not read pnl."""
    a = _clock_minutes(left)
    b = _clock_minutes(right)
    if a is not None and b is not None:
        return set(a) == set(b)
    if skip_left is not None and skip_right is not None:
        if not skip_left and not skip_right:
            return True
        union = skip_left | skip_right
        if not union:
            return True
        jaccard = len(skip_left & skip_right) / float(len(union))
        return jaccard >= CLONE_JACCARD
    return False


def _used_singleton_minutes(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> set[int]:
    used: set[int] = set()
    reg = load_registry(root=root, registry=registry)
    for row in reg.get("rules") or []:
        if not isinstance(row, dict) or not row.get("selects"):
            continue
        minutes = _clock_minutes(row)
        if minutes is not None and len(minutes) == 1:
            used.add(int(minutes[0]))
    payload = farm if farm is not None else load_farm(root=root)
    for row in payload.get("notebooks") or []:
        if not isinstance(row, dict):
            continue
        minutes = _clock_minutes(row)
        if minutes is not None and len(minutes) == 1:
            used.add(int(minutes[0]))
    return used


def _minutes_used(
    want: set[int],
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> bool:
    reg = load_registry(root=root, registry=registry)
    for row in list(reg.get("rules") or []) + list((farm or load_farm(root=root)).get("notebooks") or []):
        if not isinstance(row, dict):
            continue
        minutes = _clock_minutes(row)
        if minutes is not None and set(minutes) == want:
            return True
    return False


def _civil_used(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> bool:
    return _minutes_used({0, 30}, root=root, registry=registry, farm=farm)


def _quarter_used(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> bool:
    return _minutes_used({15, 45}, root=root, registry=registry, farm=farm)


def _hour_first_half_used(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> bool:
    return _minutes_used({15, 30}, root=root, registry=registry, farm=farm)


def _clock_singleton_executing(*, root: Path | None = None, registry: dict[str, Any] | None = None) -> bool:
    """True when a one-minute clock selection still has the chair."""
    from golf_offshoot.learning_lane_15m.rules import active_execution_rule, clock_skip_minutes

    try:
        seated = active_execution_rule(root=root, registry=registry)
    except (ValueError, OSError):
        return False
    if not seated or seated.get("selects") is not True:
        return False
    if seated.get("execution") is not True:
        return False
    minutes = clock_skip_minutes(seated)
    return minutes is not None and len(minutes) == 1


def _kind_is_honer(kind_id: str) -> bool:
    return str(kind_id or "").startswith(HONER_KIND_PREFIX)


def _honer_latest(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / HONER_LATEST_REL


def honer_family_amend_reasons(*, root: Path | None = None) -> list[str]:
    """File labels that owe the amend: honer library and exam JSON, read as files.

    ``catalog_exhausted`` off ``library.json``; ``completed_dead`` off a library row
    or ``exam_score.json``. Catalog prose does not decide, and no ledger, exam ``d``,
    or gross pnl is opened.
    """
    latest = _honer_latest(root=root)
    library = _load_json(latest / "library.json")
    reasons: list[str] = []
    if library.get("catalog_exhausted") is True:
        reasons.append(REASON_CATALOG_EXHAUSTED)
    dead = any(
        isinstance(row, dict) and str(row.get("outcome") or "") == REASON_EXAM_DEAD
        for row in library.get("rows") or []
    )
    if not dead:
        dead = str(_load_json(latest / "exam_score.json").get("outcome") or "") == REASON_EXAM_DEAD
    if dead:
        reasons.append(REASON_EXAM_DEAD)
    return reasons


def honer_family_amend_taken(*, root: Path | None = None) -> bool:
    """True once a third family is dated in the honer catalog. The doorbell is answered."""
    payload = _load_json((root or repo_root()) / HONER_CATALOG_REL)
    items = [
        row for row in payload.get("items") or [] if isinstance(row, dict) and row.get("id")
    ]
    return len(items) > DATED_HONER_FAMILIES


def honer_family_amend_legal_now(*, root: Path | None = None) -> bool:
    """``HONER-FAMILY-AMEND.legal_now``, off honer files rather than the catalog note."""
    if honer_family_amend_taken(root=root):
        return False
    return bool(honer_family_amend_reasons(root=root))


def owed_non_farm_kinds(
    *,
    root: Path | None = None,
    catalog: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Catalog kinds that are legal now but are never farm notebooks.

    Today that is the honer family amend: Lab dates it on the honer organ, so it
    stays out of ``unused_legal_kinds``, but it is still the named next kind.
    """
    cat = catalog if catalog is not None else load_catalog(root=root)
    kinds = cat.get("kinds") if isinstance(cat.get("kinds"), list) else []
    burned = burned_ids(root=root)
    out: list[dict[str, Any]] = []
    for kind in kinds:
        if not isinstance(kind, dict) or str(kind.get("id") or "") != FAMILY_AMEND_KIND:
            continue
        if FAMILY_AMEND_KIND in burned:
            continue
        reasons = honer_family_amend_reasons(root=root)
        if not reasons or honer_family_amend_taken(root=root):
            continue
        out.append({"kind": FAMILY_AMEND_KIND, "legal_now": True, "reasons": reasons})
    return out


def unused_legal_kinds(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
    catalog: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Legal unused farm slots. Clock minutes are expanded; honer kinds are not farmed."""
    cat = catalog if catalog is not None else load_catalog(root=root)
    kinds = cat.get("kinds") if isinstance(cat.get("kinds"), list) else []
    if not kinds:
        return []
    payload = farm if farm is not None else load_farm(root=root)
    out: list[dict[str, Any]] = []
    clock_executing = _clock_singleton_executing(root=root, registry=registry)
    used_minutes = _used_singleton_minutes(root=root, registry=registry, farm=payload)
    for kind in kinds:
        if not isinstance(kind, dict):
            continue
        kid = str(kind.get("id") or "")
        if not kid or _kind_is_honer(kid):
            continue
        if kid in burned_ids(root=root):
            continue
        if kind.get("legal_only_when"):
            continue
        if kid == "CLOCK-CLOSE-MINUTE":
            if kind.get("legal_now") is not True:
                continue
            for minute in QUARTET_MINUTES:
                if minute in used_minutes:
                    continue
                out.append(
                    {
                        "kind": kid,
                        "params": {"skip_close_minute": minute},
                        "expected_skip_rate": 0.25,
                    }
                )
            continue
        if kid == "CLOCK-CIVIL-BOUNDARIES":
            if clock_executing:
                continue
            if _civil_used(root=root, registry=registry, farm=payload):
                continue
            out.append(
                {
                    "kind": kid,
                    "params": {"skip_close_minutes": [0, 30]},
                    "expected_skip_rate": 0.5,
                }
            )
            continue
        if kid == "CLOCK-QUARTER-BOUNDARIES":
            if kind.get("legal_now") is not True:
                continue
            if _quarter_used(root=root, registry=registry, farm=payload):
                continue
            out.append(
                {
                    "kind": kid,
                    "params": {"skip_close_minutes": [15, 45]},
                    "expected_skip_rate": 0.5,
                }
            )
            continue
        if kid == "CLOCK-HOUR-FIRST-HALF":
            if kind.get("legal_now") is not True:
                continue
            if _hour_first_half_used(root=root, registry=registry, farm=payload):
                continue
            out.append(
                {
                    "kind": kid,
                    "params": {"skip_close_minutes": [15, 30]},
                    "expected_skip_rate": 0.5,
                }
            )
            continue
        if kind.get("legal_now") is True:
            out.append({"kind": kid, "params": dict(kind.get("params") or {}), "expected_skip_rate": kind.get("expected_skip_rate")})
    return out


def first_look_n(*, root: Path | None = None) -> int:
    from golf_offshoot.learning_lane_15m.evidence_bar import load_evidence_bar

    try:
        bar = load_evidence_bar(root=root)
        return int((bar.get("looks") or {}).get("first_look_n") or 70)
    except Exception:  # noqa: BLE001
        return 70


def load_farm_scorecard(notebook_id: str, *, root: Path | None = None) -> dict[str, Any]:
    return _load_json(farm_scorecard_path(notebook_id, root=root))


def keeper_notebooks(
    *,
    root: Path | None = None,
    farm: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    payload = farm if farm is not None else load_farm(root=root)
    keepers: list[dict[str, Any]] = []
    for row in payload.get("notebooks") or []:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("id") or "")
        if not rid or rid in FORBIDDEN_FARM_IDS:
            continue
        if row.get("execution") is True:
            continue
        card = load_farm_scorecard(rid, root=root)
        if card.get("passes_every_binding_clause") is True:
            keepers.append(row)
    keepers.sort(
        key=lambda row: (
            str(row.get("declared_at") or ""),
            str(row.get("kind") or ""),
            json.dumps(row.get("params") or {}, sort_keys=True),
            str(row.get("id") or ""),
        )
    )
    return keepers


def next_promote(
    *,
    root: Path | None = None,
    farm: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    keepers = keeper_notebooks(root=root, farm=farm)
    return keepers[0] if keepers else None


def live_look_closed(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> bool:
    """True when L1 exists and the selecting chair is parked.

    An L1 file is the grade sheet, not an empty chair. Mid-look (still
    executing) is not closed. Empty chair with no parked L1 is F_continuation.
    """
    from golf_offshoot.learning_lane_15m.clerical_score import FORBIDDEN_SCORE_IDS, scorecard_path

    payload = registry if registry is not None else _load_json((root or repo_root()) / REGISTRY_REL)
    selecting = [
        row
        for row in (payload.get("rules") or [])
        if isinstance(row, dict)
        and row.get("selects") is True
        and str(row.get("kind") or "").strip().lower() == "selection"
    ]
    occupying = []
    parked_l1 = False
    for row in selecting:
        rid = str(row.get("id") or "")
        if not rid or rid in FORBIDDEN_SCORE_IDS:
            continue
        if row.get("execution") is True:
            occupying.append(rid)
            continue
        if scorecard_path(rid, root=root, look="L1").is_file():
            parked_l1 = True
    if occupying:
        return False
    return parked_l1


def promote_gates(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    closed = live_look_closed(root=root, registry=registry)
    head = next_promote(root=root, farm=farm)
    gates = [
        {"id": "live_l1_closed", "ok": closed},
        {"id": "not_mid_look", "ok": closed},
        {
            "id": "head_is_keeper",
            "ok": head is not None and str(head.get("id") or "") not in FORBIDDEN_FARM_IDS,
        },
    ]
    return gates


def promote_ready(*, root: Path | None = None, registry: dict[str, Any] | None = None, farm: dict[str, Any] | None = None) -> bool:
    return all(g.get("ok") for g in promote_gates(root=root, registry=registry, farm=farm))


def product_skip_kinds(lane: str = "learning_lane_15m") -> tuple[str, ...]:
    """Named skip families this gym can farm. A later series supplies its own menu."""
    if str(lane or "") == "learning_lane_15m":
        return (
            "CLOCK-CLOSE-MINUTE",
            "CLOCK-CIVIL-BOUNDARIES",
            "CLOCK-QUARTER-BOUNDARIES",
            "CLOCK-HOUR-FIRST-HALF",
        )
    return ()


def burned_ids(*, root: Path | None = None) -> set[str]:
    payload = _load_json((root or repo_root()) / BURNED_REL)
    out: set[str] = set()
    for row in payload.get("classes") or []:
        if not isinstance(row, dict) or not row.get("burned"):
            continue
        cid = str(row.get("id") or "").strip()
        if cid:
            out.add(cid)
        for alias in row.get("aliases") or []:
            text = str(alias or "").strip()
            if text:
                out.add(text)
    return out


def skips_whole_quartet(slot: dict[str, Any]) -> bool:
    """True when a notebook ANDs every close minute of the quartet into its skip set.

    Skipping {0, 15, 30, 45} fills nothing, so the card can never be a look at a
    skip against a fill. Product structure only; no card, no tape, no pnl.
    """
    minutes = _clock_minutes(slot)
    if minutes is None:
        return False
    return set(minutes) >= set(QUARTET_MINUTES)


def refuse_reason(
    slot: dict[str, Any],
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> str:
    """Why this notebook must not be dated. Empty string means legal."""
    from golf_offshoot.learning_lane_15m.rules import expected_skip_rate, min_expected_skip_rate

    kind = str(slot.get("kind") or "")
    if not kind:
        return "kind is missing"
    if _kind_is_honer(kind):
        return "honer kinds stay the skip-on-mark organ"
    if kind in burned_ids(root=root):
        return f"burned {kind}"
    if skips_whole_quartet(slot):
        return "fill-none: AND-skip of the whole quartet leaves no filled window"
    params = slot.get("params") if isinstance(slot.get("params"), dict) else {}
    probe = notebook_as_rule(
        {
            "id": str(slot.get("id") or "F-PROBE"),
            "kind": kind,
            "params": params,
            "declared_at": "2099-01-01T00:00:00-04:00",
        }
    )
    named = expected_skip_rate(probe)
    raw_rate = slot.get("expected_skip_rate")
    if named is None and raw_rate is None:
        return "cannot name expected_skip_rate from product structure"
    try:
        rate = float(named if named is not None else raw_rate)
    except (TypeError, ValueError):
        return "cannot name expected_skip_rate from product structure"
    floor = min_expected_skip_rate(root=root)
    if rate < floor:
        return f"density {rate} below {floor}"
    payload = farm if farm is not None else load_farm(root=root)
    others: list[dict[str, Any]] = []
    for row in load_registry(root=root, registry=registry).get("rules") or []:
        if isinstance(row, dict) and row.get("selects"):
            others.append(row)
    for row in payload.get("notebooks") or []:
        if isinstance(row, dict):
            others.append(row)
    for other in others:
        if str(other.get("id") or "") == str(slot.get("id") or ""):
            continue
        if clone_overlap(slot, other):
            return "clone of an existing farm or live skip set"
    return ""


def save_farm(payload: dict[str, Any], *, root: Path | None = None) -> dict[str, Any]:
    """Write farm JSON. Every notebook stays execution false."""
    notebooks: list[dict[str, Any]] = []
    for row in payload.get("notebooks") or []:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        item["execution"] = False
        item["selects"] = True
        notebooks.append(item)
    out = {
        "schema": int(payload.get("schema") or 1),
        "lane": str(payload.get("lane") or "learning_lane_15m"),
        "series": str(payload.get("series") or "KXBTC15M"),
        "note": str(
            payload.get("note")
            or "Discovery farm. Notebooks are execution false. Not live. Not an ADMIT."
        ),
        "notebooks": notebooks,
    }
    path = farm_path(root=root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def date_notebooks(
    slots: list[dict[str, Any]],
    *,
    declared_at: str,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Append legal unused slots. Never sets execution true. Skips refused rows."""
    payload = load_farm(root=root)
    notebooks = list(payload.get("notebooks") or [])
    added: list[dict[str, Any]] = []
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        reason = refuse_reason(slot, root=root, registry=registry, farm=payload)
        if reason:
            continue
        kind = str(slot.get("kind") or "")
        params = dict(slot.get("params") or {})
        nid = str(slot.get("id") or "").strip()
        if not nid:
            minute = params.get("skip_close_minute")
            minutes = params.get("skip_close_minutes")
            if minute is not None:
                nid = f"F-{kind}-{int(minute)}"
            elif minutes is not None:
                nid = f"F-{kind}-{'-'.join(str(int(x)) for x in minutes)}"
            else:
                nid = f"F-{kind}-{len(notebooks) + 1}"
        if any(str(row.get("id") or "") == nid for row in notebooks):
            continue
        row = {
            "id": nid,
            "kind": kind,
            "params": params,
            "declared_at": str(declared_at),
            "execution": False,
            "selects": True,
        }
        notebooks.append(row)
        payload["notebooks"] = notebooks
        added.append(row)
    payload["notebooks"] = notebooks
    save_farm(payload, root=root)
    return added


def date_unused_legal(
    *,
    declared_at: str,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    slots = unused_legal_kinds(root=root, registry=registry)
    added = date_notebooks(slots, declared_at=declared_at, root=root, registry=registry)
    maybe_stamp_menu_exhausted(root=root, registry=registry)
    return added


def clock_menu_empty(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> bool:
    """True when no unused slot is left in any named clock family."""
    named = set(product_skip_kinds())
    unused = unused_legal_kinds(root=root, registry=registry, farm=farm)
    return not any(str(slot.get("kind") or "") in named for slot in unused)


def maybe_stamp_menu_exhausted(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Write ``FARM_MENU_EXHAUSTED`` when the quartet is spent and produced no keeper.

    Keeper count is a binding-clause verdict off the farm cards, never a pnl rank.
    Idempotent: an existing stamp is left alone. Returns the payload it wrote.
    """
    if menu_exhausted(root=root):
        return None
    if keeper_notebooks(root=root, farm=farm):
        return None
    if not clock_menu_empty(root=root, registry=registry, farm=farm):
        return None
    return write_menu_exhausted(
        "keepers 0 and no unused clock slot left in the quartet menu",
        root=root,
    )


def farm_hunger(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    farm: dict[str, Any] | None = None,
) -> bool:
    """True when Lab still has farm work: unused slots, or a file-owed honer amend.

    Zero keepers with an empty clock menu is exhaustion, not hunger — another clock
    clone is not the next kind there.
    """
    unused = unused_legal_kinds(root=root, registry=registry, farm=farm)
    if unused:
        return True
    cat = load_catalog(root=root)
    if not (cat.get("kinds") or []):
        return False
    if owed_non_farm_kinds(root=root, catalog=cat):
        return True
    if menu_exhausted(root=root):
        return False
    return bool(keeper_notebooks(root=root, farm=farm))


def notebook_window_count(notebook: dict[str, Any], *, windows: list[dict[str, Any]] | None = None) -> int:
    if windows is not None:
        return len(windows)
    return 0


def progress_meter(n: int, need: int) -> str:
    need = max(int(need) or 70, 1)
    n = max(int(n), 0)
    return f"{min(n, need)}/{need}"


def progress_pct(n: int, need: int) -> int:
    need = max(int(need) or 70, 1)
    n = max(int(n), 0)
    return int(min(n, need) * 100 / need)


def settled_n(notebook: dict[str, Any], *, root: Path | None = None) -> int:
    """Settled windows after declared_at, from the FARM card or the shared tape."""
    rid = str(notebook.get("id") or "")
    card = load_farm_scorecard(rid, root=root) if rid else {}
    try:
        n = int(card.get("n") or 0)
    except (TypeError, ValueError):
        n = 0
    if n:
        return n
    try:
        from golf_offshoot.learning_lane_15m.clerical_score import gather_tape_windows

        return len(gather_tape_windows(notebook_as_rule(notebook)))
    except Exception:  # noqa: BLE001 — missing tape is n=0, not invented bars
        return 0


_CLAUSE_FACE = (
    ("clause_1_paired_t_vs_floor", "1"),
    ("clause_4_positive_side", "4"),
    ("clause_5_matched_exposure", "5"),
)


def farm_card_why(card: dict[str, Any]) -> str:
    """Skip rate and which binding clauses failed. No farm pnl figures."""
    if not card:
        return ""
    bits: list[str] = []
    try:
        rate = float(card.get("skip_rate"))
    except (TypeError, ValueError):
        rate = None
    if rate is not None:
        bits.append(f"skip {round(rate * 100)}%")
    else:
        skip_count = card.get("skip_count")
        n = card.get("n")
        if skip_count is not None and n:
            bits.append(f"skip {skip_count}/{n}")
    failed: list[str] = []
    passed: list[str] = []
    for key, label in _CLAUSE_FACE:
        row = card.get(key)
        if not isinstance(row, dict) or "passes" not in row:
            continue
        if row.get("passes") is True:
            passed.append(label)
        elif row.get("passes") is False:
            failed.append(label)
    if failed:
        bits.append("clauses " + ",".join(failed) + " fail")
    elif passed:
        bits.append("clauses pass")
    return " · ".join(bits)


def _join_why(*parts: str) -> str:
    return " · ".join(part for part in parts if part)


def notebook_face(
    notebook: dict[str, Any],
    *,
    root: Path | None = None,
    farm: dict[str, Any] | None = None,
    need: int | None = None,
    n: int | None = None,
) -> tuple[str, str]:
    """Status plus one-line why. Collecting / score owed / parked / keeper / queued. Not live."""
    rid = str(notebook.get("id") or "")
    card = load_farm_scorecard(rid, root=root) if rid else {}
    need_n = int(need if need is not None else first_look_n(root=root))
    bar = farm_card_why(card)
    if card.get("passes_every_binding_clause") is True:
        keepers = keeper_notebooks(root=root, farm=farm)
        head = keepers[0] if keepers else None
        if head and str(head.get("id") or "") == rid:
            return "keeper", _join_why(bar, "eligible · not live")
        return "queued", _join_why(bar, "eligible · not live")
    if card and card.get("passes_every_binding_clause") is False:
        return "parked", _join_why(bar, "not a keeper")
    if n is None:
        n = settled_n(notebook, root=root)
    if n >= need_n and not card:
        return "score owed", f"{need_n} reached · farm card not written"
    if n >= need_n and card:
        return "waiting", bar or "farm card present"
    return "collecting", ""


def notebook_status(
    notebook: dict[str, Any],
    *,
    root: Path | None = None,
    farm: dict[str, Any] | None = None,
    need: int | None = None,
) -> str:
    """collecting / score owed / keeper / queued / parked. Not live."""
    status, _why = notebook_face(notebook, root=root, farm=farm, need=need)
    return status
