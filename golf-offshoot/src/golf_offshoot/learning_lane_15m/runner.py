"""Clerical learning runner. Dry-run until Founder arms it.

Reads ``roles_owed`` and may serve only a named whitelist of clerical jobs:
Illustrator re-render, Systems local export, generated digest figures, and
the hash-stamped Validator report. Judicial work (ADMIT, RUN-ONLY, closing
a park, lifting the HOLD, human Digestor caveats, Soften Critic) is never
on the list. Validator's presence here is a move across the trust boundary
from ``JUDICIAL_NEVER``, not an append.

Default mode is dry-run: log what would be served, serve nothing.

The kill switch is a file, ``latest/RUNNER_KILL``. The runner re-reads it at
the start of every pass. Touch the file to stop the runner mid-flight without
touching PaperWatch. Delete the file to let a later pass run. An env var is
not the switch.

Serve-on-proof: a role is marked served only after the artifact it was meant
to produce actually changed on disk. Exit code 0 is not proof. If the
artifact did not move, the role stays owed and the failure is logged.
Auto serve uses ``served_kind='auto'``. A human (or Systems export on the
watch) that changes an owned artifact clears the role with ``served_kind='human'``.
The two stay distinguishable forever.

``execute=True`` is a scratch-tree harness only. It requires ``root=`` pointing
off the real repo and never serves the live tree unarmed.

The runner exports locally. It does not ``git commit`` or ``git push``. Pages
stays a manual publish.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Callable, NamedTuple

from golf_offshoot.learning_lane_15m.learn import (
    load_wake_state,
    mark_roles_served,
    scan_learning_evidence,
)
from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    has_15m_root_override,
    latest_dir_15m,
)
from golf_offshoot.localtime import format_eastern, isoformat_now
from golf_offshoot.operator_surface.observability import (
    _lane_by_id,
    _lane_publish_fingerprint,
    material_publish_reasons,
    repo_root,
)

MODE_DRY = "dry-run"
MODE_OFF = "off"
MODE_ARMED = "armed"
ENV_MODE = "GOLF_OFFSHOOT_LEARNING_RUNNER"

KILL_NAME = "RUNNER_KILL"
ARM_NAME = "RUNNER_ARMED"

# Enumerate what this process may ever do. A blacklist is not acceptable.
# Trust-boundary move (not an append): validator leaves JUDICIAL_NEVER and
# joins the whitelist. Human digestor leaves the whitelist — its proof is
# the caveats file, not SOURCE as a whole. A figures generator that wrote
# SOURCE into the digestor slot would clear digestor every tick and undo #171.
CLERICAL_WHITELIST = (
    "illustrator",
    "systems",
    "digest-figures",
    "validator",
    # Mechanical half of the Critic: run the check suite, write the findings
    # artifact. The adversarial turn is soften-critic and stays judicial.
    "critic-invariants",
    # Generated learning card. Separate from digest-figures so a SOURCE-only
    # rewrite cannot clear a card owe (#171 lesson).
    "learning-card",
)
JUDICIAL_NEVER = (
    "operator",
    "lab",
    "digestor",
    "soften-critic",
    "chief-of-staff",
    "admit",
    "run-only",
    "park",
    "hold",
)

LOG_NAME = "learning_runner.jsonl"
FP_STORE_NAME = "role_artifact_fps.json"
BOARD_FP_NAME = "board_fingerprint.json"

#: Clock fields. A report that stamps itself on every write moves its own hash
#: on every write, and serve-on-proof then clears the role for having run.
VOLATILE_KEYS = (
    "ran_at",
    "checked_at",
    "validated_at",
    "generated_at",
    "stamped_at",
    "scored_at",
    "at",
    "at_text",
)

#: The SOURCE digest's own as-of lines. Same defect, in markdown.
_DIGEST_STAMP_LINE = re.compile(r"\*\*Evidence as-of:\*\*|hub `generated_at`")

DIGEST_ASOF_NAME = "digest_asof.json"
DIGEST_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST.md"
CAVEATS_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
PARK_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_METHOD_PARK.md"
MANIFEST_REL = Path("docs") / "observability-hub" / "data" / "manifest.json"
VALIDATOR_REPORT_REL = Path("docs") / "observability-hub" / "data" / "validator_report.json"
CRITIC_FINDINGS_REL = (
    Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_CRITIC_FINDINGS.json"
)
LEARNING_CARD_REL = (
    Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_LEARNING_CARD.md"
)
_CARD_STAMP_LINE = re.compile(r"^\*\*As-of:\*\*|^journal generated_at=", re.IGNORECASE)
PNG_REL = (
    Path("docs")
    / "observability-hub"
    / "data"
    / "charts"
    / "learning_lane_15m"
    / "paper_window_strip.png"
)


def runner_mode(raw: str | None = None) -> str:
    """Requested mode. The kill file overrides this to off on every pass."""
    value = str(raw if raw is not None else os.environ.get(ENV_MODE, MODE_DRY)).strip().lower()
    if value in {MODE_DRY, "dry", "dryrun"}:
        return MODE_DRY
    if value in {MODE_OFF, "kill", "killed", "stop"}:
        return MODE_OFF
    if value in {MODE_ARMED, "on", "live"}:
        return MODE_ARMED
    return MODE_DRY


def runner_log_path() -> Path:
    return latest_dir_15m() / LOG_NAME


def kill_switch_path() -> Path:
    return latest_dir_15m() / KILL_NAME


def arm_file_path() -> Path:
    return latest_dir_15m() / ARM_NAME


def kill_switch_active() -> bool:
    """Re-read from disk. Presence of the file is the switch."""
    return kill_switch_path().is_file()


def write_kill_switch() -> Path:
    path = kill_switch_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("off\n", encoding="utf-8")
    return path


def clear_kill_switch() -> None:
    path = kill_switch_path()
    if path.is_file():
        path.unlink()


def founder_has_armed() -> bool:
    return arm_file_path().is_file()


def write_arm_file() -> Path:
    path = arm_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "armed 2026-09-07\nwhitelist=illustrator,systems,digest-figures,validator\n"
        "publish=local-export-only\n",
        encoding="utf-8",
    )
    return path


def _is_real_repo(root: Path | None) -> bool:
    if root is None:
        return True
    try:
        return Path(root).resolve() == repo_root().resolve()
    except OSError:
        return False


def assert_scratch_execute(*, root: Path | None) -> None:
    """execute=True may never target the live tree."""
    if root is None:
        raise RuntimeError("execute=True requires root= pointing at a scratch tree")
    if _is_real_repo(root):
        raise RuntimeError("execute=True cannot serve the real repo unarmed")


def _append_log(entry: dict[str, Any]) -> Path:
    path = runner_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=True) + "\n")
    return path


def _owed_roles(state: dict[str, Any] | None) -> list[str]:
    if not state:
        return []
    names: list[str] = []
    for entry in state.get("roles_owed") or []:
        role = str(entry.get("role") or "").strip().lower()
        if role and role not in names:
            names.append(role)
    return names


def artifact_path(role: str, *, root: Path | None = None) -> Path:
    """What the worker writes. Human digestor writes caveats; figures write SOURCE."""
    if role == "digestor":
        # Leftover as-of stamp. It is not the proof and does not clear caveats.
        return latest_dir_15m() / DIGEST_ASOF_NAME
    base = root or repo_root()
    rel = {
        "illustrator": PNG_REL,
        "systems": MANIFEST_REL,
        "digest-figures": DIGEST_REL,
        "validator": VALIDATOR_REPORT_REL,
        "critic-invariants": CRITIC_FINDINGS_REL,
        "learning-card": LEARNING_CARD_REL,
        "operator": PARK_REL,
    }.get(role)
    if rel is None:
        raise ValueError(f"no clerical artifact for role {role!r}")
    return base / rel


def proof_artifact_path(role: str, *, root: Path | None = None) -> Path:
    """The file whose change clears the role.

    Human digestor is keyed on the standing caveats file, not SOURCE as a
    whole. A figures-only SOURCE rewrite must leave digestor owed. That is
    the #171 mechanic one layer up: an as-of (or generated-figures) write
    cannot clear a caveats obligation.
    """
    if role == "digestor":
        return (root or repo_root()) / CAVEATS_REL
    return artifact_path(role, root=root)


def owned_artifact_paths(role: str, *, root: Path | None = None) -> list[Path]:
    """Files whose change proves that role ran. Lab owns none."""
    if role == "digestor":
        return [proof_artifact_path(role, root=root)]
    if role in {
        "illustrator",
        "systems",
        "digest-figures",
        "validator",
        "critic-invariants",
        "learning-card",
        "operator",
    }:
        return [artifact_path(role, root=root)]
    return []


def _fingerprint_store_path() -> Path:
    return latest_dir_15m() / FP_STORE_NAME


def _systems_token(path: Path) -> str | None:
    payload = _load_json(path)
    if payload is None:
        return file_fingerprint(path)
    token = _lane_publish_fingerprint(_lane_by_id(payload, LANE_15M))
    return json.dumps(token, default=str, sort_keys=True)


def _legacy_digestor_source_store(prev: Any, *, root: Path | None = None) -> bool:
    """True when prev is the old SOURCE (or asof|SOURCE) store from #171.

    After the trust-boundary move, digestor proof is the caveats file. A leftover
    SOURCE fingerprint must not look like a caveats write and false-clear.
    """
    if not prev or not isinstance(prev, str):
        return False
    source_fp = file_fingerprint((root or repo_root()) / DIGEST_REL)
    if source_fp and (prev == source_fp or prev.endswith("|" + source_fp)):
        return True
    return "|" in prev


def _proof_changed(
    role: str,
    prev: Any,
    token: str | None,
    *,
    root: Path | None = None,
) -> bool:
    """True when the proof token moved. Leftover SOURCE stores never clear digestor."""
    if not prev or not token or prev == "missing":
        return False
    if prev == token:
        return False
    if role == "digestor" and _legacy_digestor_source_store(prev, root=root):
        return False
    return True


def critic_verdicts(payload: dict[str, Any] | None) -> str:
    """The verdicts and what they cover, without the clock.

    ``run_critic_invariants`` stamps ``ran_at`` and a per-row ``checked_at`` on
    every pass, so the raw file hash moves whether or not a single verdict
    moved — which clears ``critic-invariants`` every tick on a heartbeat.
    Systems has ``material_publish_reasons`` for exactly this; this is the same
    guard for the Critic's mechanical half.

    ``detail`` is **not** in the token. It was, and that defeated the whole
    guard: ``check_honesty_stamp_is_fresh`` wrote ``{int(age)}s old`` into its
    detail, so the token moved on every ~90s pass and the role went on clearing
    itself on a heartbeat through two rounds of fixing. Dropping it weakens no
    check — ``detail`` is a rendering of ``state`` and ``evidence`` — and that
    check has left the method suite anyway. ``desk_checks`` are excluded for the
    same reason: nothing that reads a clock may sit in a proof token.

    The reviewed **hash set** is part of the token, not just the checks. A run
    that reviews a newly-changed artifact has done real work even when every
    verdict reads the same, and leaving that unserved would deadlock the role:
    once the hash is reviewed, ``artifact_unreviewed`` stops firing and nothing
    would ever owe it again.
    """
    payload = payload or {}
    checks = [
        {"id": row.get("id"), "state": row.get("state")}
        for row in (payload.get("checks") or [])
    ]
    reviewed = sorted(str((row or {}).get("sha256") or "") for row in payload.get("reviewed") or [])
    return json.dumps(
        {"passed": payload.get("passed"), "checks": checks, "reviewed": reviewed},
        default=str,
        sort_keys=True,
    )


def _stripped_json_token(path: Path, volatile: tuple[str, ...]) -> str | None:
    """A JSON artifact's content with its clock fields removed.

    A report that stamps itself on every write moves its own hash on every
    write. Serve-on-proof then clears the role for having run, which is the
    defect ``material_publish_reasons`` was built for. This is the same guard,
    generalised.
    """
    payload = _load_json(path)
    if payload is None:
        return file_fingerprint(path)

    def _strip(node: Any) -> Any:
        if isinstance(node, dict):
            return {k: _strip(v) for k, v in sorted(node.items()) if k not in volatile}
        if isinstance(node, list):
            return [_strip(v) for v in node]
        return node

    return json.dumps(_strip(payload), default=str, sort_keys=True)


def _validator_token(path: Path) -> str | None:
    return _stripped_json_token(path, VOLATILE_KEYS)


def _digest_token(path: Path) -> str | None:
    """The SOURCE digest minus its own as-of lines.

    Regenerating the digest with no book movement rewrites its stamp, so the
    file hash moves and ``digest-figures`` clears on a heartbeat exactly the way
    the Critic did.
    """
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    kept = [
        line
        for line in text.splitlines()
        if not _DIGEST_STAMP_LINE.search(line)
    ]
    return hashlib.sha256("\n".join(kept).encode("utf-8")).hexdigest()


def _card_token(path: Path) -> str | None:
    """The learning card minus its as-of line. Same heartbeat guard as SOURCE."""
    if not path.is_file():
        return None
    kept = [
        line
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not _CARD_STAMP_LINE.search(line)
    ]
    return hashlib.sha256("\n".join(kept).encode("utf-8")).hexdigest()


def _critic_token(path: Path) -> str | None:
    payload = _load_json(path)
    if payload is None:
        return file_fingerprint(path)
    return critic_verdicts(payload)


def board_fingerprint_path() -> Path:
    return latest_dir_15m() / BOARD_FP_NAME


def _illustrator_token(path: Path) -> str | None:
    """The board's *content* fingerprint, written by the renderer, not the PNG bytes.

    ``illustrate.py`` stamps the render time into the PNG's metadata, so every
    re-render moves the file hash whether or not a single drawn row moved. The
    renderer writes a sidecar naming what it actually drew; that is the proof.
    No sidecar means no proof, so the role stays owed.
    """
    if not path.is_file():
        return None
    sidecar = _load_json(board_fingerprint_path())
    if not isinstance(sidecar, dict):
        return None
    drawn = sidecar.get("drawn")
    if not drawn:
        return None
    return json.dumps({"png": True, "drawn": drawn}, default=str, sort_keys=True)


class ClericalContract(NamedTuple):
    """What must be true before this role may be served by a machine.

    ``token`` must ignore clocks: a timestamp-only rewrite may not clear the
    role. ``negative_event`` is the event kind a *failing* artifact raises, so a
    ``passed: false`` result cannot be the end of it. ``event_source`` is the
    detector whose silence would otherwise leave the role un-owed, and which
    therefore has to report its own blindness. ``test_serve_on_proof.py``
    enforces all three over the whole whitelist; a role added here without them
    is a red build.
    """

    token: Callable[[Path], str | None]
    negative_event: str
    event_source: str


CLERICAL_CONTRACTS: dict[str, ClericalContract] = {
    "illustrator": ClericalContract(_illustrator_token, "detector_blind", "board_lag"),
    "systems": ClericalContract(_systems_token, "published_falsehood", "diff_scans"),
    "digest-figures": ClericalContract(
        _digest_token, "digest_contradicts_ledger", "diff_scans"
    ),
    "validator": ClericalContract(
        _validator_token, "validator_report_failing", "diff_scans"
    ),
    "critic-invariants": ClericalContract(
        _critic_token, "critic_findings_failing", "repo_events"
    ),
    "learning-card": ClericalContract(
        _card_token, "detector_blind", "learning_card_inputs"
    ),
}


def role_proof_token(role: str, *, root: Path | None = None) -> str | None:
    paths = owned_artifact_paths(role, root=root)
    if not paths:
        return None
    contract = CLERICAL_CONTRACTS.get(role)
    if contract is not None:
        return contract.token(paths[0])
    parts = [file_fingerprint(path) for path in paths]
    if any(part is None for part in parts):
        return None
    return "|".join(parts)


def file_fingerprint(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return f"{path.stat().st_size}:{digest}"


def plan_from_wake(state: dict[str, Any] | None) -> dict[str, Any]:
    owed = _owed_roles(state)
    would_serve = [role for role in CLERICAL_WHITELIST if role in owed]
    held_for_human = [role for role in owed if role not in CLERICAL_WHITELIST]
    return {
        "owed": owed,
        "would_serve": would_serve,
        "held_for_human": held_for_human,
        "whitelist": list(CLERICAL_WHITELIST),
        "judicial_never": list(JUDICIAL_NEVER),
    }


def _digest_asof_payload() -> dict[str, Any]:
    scan = scan_learning_evidence()
    pending = [
        str(row.get("ticker") or row.get("window_id") or "")
        for row in (scan.get("pending") or [])
        if isinstance(row, dict)
    ]
    missing = [
        str(row.get("ticker") or "")
        for row in (scan.get("paper_join_missing") or [])
        if isinstance(row, dict)
    ]
    settled = sorted(str(key) for key in (scan.get("settled") or {}))
    return {
        "lane": "learning_lane_15m",
        "framing": "clerical as-of stamp; not the SOURCE digest; not an ADMIT",
        "pending": pending,
        "paper_join_missing": missing,
        "settled": settled,
    }


def _default_do_illustrator() -> Path | None:
    from golf_offshoot.learning_lane_15m.illustrate import render_paper_window_strip

    return render_paper_window_strip()


def _default_do_systems() -> dict[str, str]:
    """Local export only. No git commit, no push. Pages stays a manual publish."""
    from golf_offshoot.operator_surface.observability import write_observability_exports

    return write_observability_exports()


def _default_do_digest_figures() -> Path:
    from golf_offshoot.learning_lane_15m.digest import write_digest

    return write_digest()


def _default_do_learning_card() -> Path:
    from golf_offshoot.learning_lane_15m.learning_card import write_learning_card

    return write_learning_card()


def _default_do_critic_invariants() -> Path:
    from golf_offshoot.learning_lane_15m.critic import write_critic_findings

    return write_critic_findings()


def _default_do_validator() -> Path:
    import subprocess
    import sys

    dest = artifact_path("validator")
    manifest = repo_root() / MANIFEST_REL
    script = repo_root() / "docs" / "observability-hub" / "validate_hub.py"
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(script), str(manifest), "--write-report", str(dest)],
        check=False,
    )
    return dest


def _default_do_digestor() -> Path:
    """Leftover as-of writer. Not on the whitelist; kept so hooks stay importable."""
    path = artifact_path("digestor")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_digest_asof_payload(), indent=2) + "\n", encoding="utf-8")
    return path


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def serve_role(
    role: str,
    *,
    do_work: Callable[[], Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """Run one clerical job. Mark served only if the artifact hash changed."""
    role = str(role).strip().lower()
    result: dict[str, Any] = {
        "role": role,
        "ok": False,
        "marked": False,
        "reason": "",
        "before": None,
        "after": None,
        "artifact": "",
    }
    if role not in CLERICAL_WHITELIST:
        result["reason"] = "not on the clerical whitelist"
        return result
    work_path = artifact_path(role, root=root)
    proof_path = proof_artifact_path(role, root=root)
    result["artifact"] = str(work_path)
    result["proof"] = str(proof_path)
    before = role_proof_token(role, root=root)
    before_raw = file_fingerprint(proof_path)
    result["before"] = before
    workers = {
        "illustrator": _default_do_illustrator,
        "systems": _default_do_systems,
        "digest-figures": _default_do_digest_figures,
        "validator": _default_do_validator,
        "critic-invariants": _default_do_critic_invariants,
        "learning-card": _default_do_learning_card,
    }
    worker = do_work or workers[role]
    try:
        worker()
    except Exception as exc:  # noqa: BLE001 — failure stays owed
        result["reason"] = f"work raised {type(exc).__name__}: {exc}"
        return result
    after = role_proof_token(role, root=root)
    after_raw = file_fingerprint(proof_path)
    result["after"] = after
    if after is None:
        wrote = after_raw is not None and after_raw != before_raw
        result["reason"] = (
            "worker wrote a non-proof file; role stays owed"
            if wrote
            else "artifact missing after work"
        )
        return result
    if before is not None and after == before:
        result["reason"] = "heartbeat; proof token unchanged; role stays owed"
        return result
    note = f"proof token changed {before} -> {after}"
    mark_roles_served([role], by="runner", note=note, served_kind="auto")
    result["ok"] = True
    result["marked"] = True
    result["reason"] = note
    result["served_kind"] = "auto"
    return result


def operator_write_addresses_owed(
    state: dict[str, Any] | None,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """Does this park write address what Operator was actually owed for?

    Operator used to clear whenever the method park changed, whoever changed it
    and for whatever reason. #174 edited the park to reconcile the Soften Critic
    Hard NO lists and cleared an Operator line raised by settles on 080745
    through 080830. Nothing had ruled on those windows.

    Shaped like ``material_publish_reasons``, which already prevents exactly
    this for Systems: the write clears Operator only when the new text names
    what Operator was owed for. **If it is unclear, Operator stays owed** — an
    exception class is never silently dropped to shorten the list.
    """
    entry = next(
        (
            row
            for row in ((state or {}).get("roles_owed") or [])
            if str(row.get("role") or "").strip().lower() == "operator"
        ),
        None,
    )
    reasons = [str(r) for r in ((entry or {}).get("reasons") or []) if str(r).strip()]
    if not reasons:
        return {
            "material": False,
            "why": (
                "park changed but the Operator owed line names no reason to match "
                "against; staying owed rather than clearing on an unrelated write"
            ),
            "matched": [],
            "reasons": [],
        }
    path = artifact_path("operator", root=root)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {
            "material": False,
            "why": "park file could not be read; Operator stays owed",
            "matched": [],
            "reasons": reasons,
        }
    # A reason reads like "new_settle KXBTC15M-26SEP080745-45" or
    # "park_aged R-SKIP-COINFLIP". The subject is what must appear.
    matched = []
    for reason in reasons:
        subject = reason.split(" ", 1)[1].strip() if " " in reason else reason.strip()
        if subject and subject in text:
            matched.append(reason)
    if matched:
        return {
            "material": True,
            "why": f"park write names {len(matched)} of {len(reasons)} owed reason(s)",
            "matched": matched,
            "reasons": reasons,
        }
    return {
        "material": False,
        "why": (
            "park changed but the new text names none of the "
            f"{len(reasons)} thing(s) Operator was owed for "
            f"({'; '.join(reasons[:3])}); nothing has ruled on them, so Operator stays owed"
        ),
        "matched": [],
        "reasons": reasons,
    }


def reconcile_owed_from_disk(*, root: Path | None = None) -> list[dict[str, Any]]:
    """Clear owed roles whose owned artifact changed, whoever changed it.

    First sight of a token is stored and does not clear. A later change marks
    ``served_kind=human`` unless the role is already gone (auto-served this pass).
    Roles with no owned artifact (lab) stay owed.
    Human digestor proof is the caveats file only. A SOURCE / figures write
    never clears it. Validator proof is the hash-stamped report.
    """
    if has_15m_root_override() and root is None:
        return []
    store_path = _fingerprint_store_path()
    previous: dict[str, Any] = {}
    if store_path.is_file():
        loaded = _load_json(store_path)
        if isinstance(loaded, dict):
            previous = loaded
    state = load_wake_state()
    owed = {
        str(entry.get("role") or "").strip().lower()
        for entry in ((state or {}).get("roles_owed") or [])
    }
    current: dict[str, str] = {}
    marked: list[dict[str, Any]] = []
    roles = (
        "illustrator",
        "systems",
        "digest-figures",
        "validator",
        "critic-invariants",
        "learning-card",
        "digestor",
        "operator",
    )
    for role in roles:
        token = role_proof_token(role, root=root)
        if token:
            current[role] = token
        prev = previous.get(role)
        if role in owed and _proof_changed(role, prev, token, root=root):
            if role == "operator":
                verdict = operator_write_addresses_owed(state, root=root)
                if not verdict["material"]:
                    marked.append(
                        {
                            "role": role,
                            "served_kind": None,
                            "held": True,
                            "note": verdict["why"],
                        }
                    )
                    continue
            note = f"owned artifact changed on disk ({prev[:24]} -> {token[:24]})"
            mark_roles_served([role], by="artifact-proof", note=note, served_kind="human")
            marked.append({"role": role, "served_kind": "human", "note": note})
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    return marked


def serve_owed_roles(
    *,
    state: dict[str, Any] | None = None,
    do_work: dict[str, Callable[[], Any]] | None = None,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    """Dispatch whitelist roles that are owed. Re-reads the kill file between roles."""
    plan = plan_from_wake(state if state is not None else load_wake_state())
    results: list[dict[str, Any]] = []
    hooks = do_work or {}
    for role in plan["would_serve"]:
        if kill_switch_active():
            results.append(
                {
                    "role": role,
                    "ok": False,
                    "marked": False,
                    "reason": "kill switch file appeared mid-pass",
                    "before": None,
                    "after": None,
                }
            )
            break
        results.append(serve_role(role, do_work=hooks.get(role), root=root))
    return results


def run_once(
    *,
    mode: str | None = None,
    now_iso: str | None = None,
    execute: bool = False,
    do_work: dict[str, Callable[[], Any]] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """One runner pass. Re-reads the kill file first. Default dry-run."""
    if execute:
        assert_scratch_execute(root=root)
    at = now_iso or isoformat_now()
    entry: dict[str, Any] = {
        "at": at,
        "at_text": format_eastern(at, with_seconds=True),
        "mode": MODE_DRY,
        "armed": False,
        "served": [],
        "failed": [],
        "would_serve": [],
        "held_for_human": [],
        "mark_roles_served_called": False,
        "note": "",
    }
    if kill_switch_active():
        entry["mode"] = MODE_OFF
        entry["note"] = "kill switch file present; runner stopped before reading roles_owed"
        _append_log(entry)
        return entry
    requested = runner_mode(mode)
    if requested == MODE_OFF:
        write_kill_switch()
        entry["mode"] = MODE_OFF
        entry["note"] = "kill switch file written; runner stopped before reading roles_owed"
        _append_log(entry)
        return entry
    if requested == MODE_ARMED and not founder_has_armed():
        entry["armed_refused"] = True
        entry["note"] = (
            "Founder has not armed this runner. Falling back to dry-run. "
            "No role was served."
        )
        requested = MODE_DRY
    if founder_has_armed() and requested != MODE_OFF:
        requested = MODE_ARMED
    state = load_wake_state()
    plan = plan_from_wake(state)
    entry["owed"] = plan["owed"]
    entry["would_serve"] = plan["would_serve"]
    entry["held_for_human"] = plan["held_for_human"]
    entry["artifacts"] = {role: str(artifact_path(role, root=root)) for role in plan["would_serve"]}
    should_execute = execute or (requested == MODE_ARMED and founder_has_armed())
    if should_execute:
        entry["mode"] = MODE_ARMED if founder_has_armed() else "execute"
        entry["armed"] = founder_has_armed()
        served_results = serve_owed_roles(state=state, do_work=do_work, root=root)
        entry["results"] = served_results
        entry["served"] = [row["role"] for row in served_results if row.get("marked")]
        entry["failed"] = [row["role"] for row in served_results if not row.get("marked")]
        entry["mark_roles_served_called"] = any(row.get("marked") for row in served_results)
        entry["note"] = entry["note"] or (
            "serve-on-proof: marked only when artifact hash changed; "
            "unchanged artifacts stay owed"
        )
    else:
        entry["mode"] = MODE_DRY
        entry["note"] = entry["note"] or (
            "dry-run: logged clerical work that would be served; served nothing; "
            "did not call mark_roles_served"
        )
    human = reconcile_owed_from_disk(root=root)
    if human:
        entry["human_cleared"] = [row["role"] for row in human]
        entry["mark_roles_served_called"] = True
        entry["served"] = list(entry.get("served") or []) + [
            row["role"] for row in human if row["role"] not in (entry.get("served") or [])
        ]
    _append_log(entry)
    return entry


def run_passes(
    n: int,
    *,
    mode: str | None = None,
    execute: bool = False,
    do_work: dict[str, Callable[[], Any]] | None = None,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    """Several passes. Re-reads the kill file at the start of each one."""
    out: list[dict[str, Any]] = []
    for _ in range(max(0, int(n))):
        if kill_switch_active():
            out.append(
                run_once(mode=MODE_DRY, execute=False, do_work=do_work, root=root)
            )
            break
        out.append(run_once(mode=mode, execute=execute, do_work=do_work, root=root))
        if out[-1].get("mode") == MODE_OFF:
            break
    return out


def run_forever(*, mode: str | None = None, interval_s: float | None = None) -> None:
    """One pass every watch tick until the kill file appears. No finite budget."""
    from golf_offshoot.learning_lane_15m.watch import watch_interval_s

    gap = watch_interval_s(interval_s)
    while True:
        entry = run_once(mode=mode)
        if entry.get("mode") == MODE_OFF:
            return
        time.sleep(max(5.0, gap))


def format_runner_line(entry: dict[str, Any]) -> str:
    mode = entry.get("mode")
    if mode == MODE_OFF:
        return f"learning runner  KILLED  {entry.get('at_text')}  {entry.get('note')}"
    would = ", ".join(entry.get("would_serve") or []) or "none"
    held = ", ".join(entry.get("held_for_human") or []) or "none"
    served = ", ".join(entry.get("served") or []) or "none"
    failed = ", ".join(entry.get("failed") or []) or "none"
    human = ", ".join(entry.get("human_cleared") or []) or "none"
    marked = "yes" if entry.get("mark_roles_served_called") else "no"
    return (
        f"learning runner  mode={mode}  would_serve={would}  "
        f"held_for_human={held}  served={served}  failed={failed}  "
        f"human_cleared={human}  mark_roles_served={marked}  {entry.get('at_text')}"
    )
