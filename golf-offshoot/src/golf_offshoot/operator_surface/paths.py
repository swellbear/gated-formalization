"""SoT root resolution. Env/config wins. Hardcoded /workspace is a local default only."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from golf_offshoot.data_feeds.http import package_data_dir

ENV_ARTIFACT_ROOT = "GOLF_OFFSHOOT_ARTIFACT_ROOT"
ENV_VIZ_ROOT = "GOLF_OFFSHOOT_VIZ_ROOT"
ENV_SHADOW_PATH = "GOLF_OFFSHOOT_SHADOW_PATH"

DEFAULT_EXTERNAL_ARTIFACT_ROOT = Path("/workspace/golf_offshoot_real_exports")
DEFAULT_EXTERNAL_VIZ_ROOT = Path("/workspace/illustrator_ops/golf_offshoot")
REPO_VIZ_FALLBACK = Path("docs") / "viz" / "golf_offshoot_dryrun_2026-09-07"
ILL_PNG_NAMES = (
    "shadow_honesty_strip.png",
    "calibration_weather.png",
    "wc1_dated_record.png",
)


class PathUnsafeError(ValueError):
    """Path failed the operator-surface safety check."""


@dataclass(frozen=True)
class ResolvedRoots:
    artifact_root: Path
    viz_root: Path
    shadow_path: Path
    artifact_source: str
    viz_source: str
    shadow_source: str


def package_root() -> Path:
    return package_data_dir().parent


def git_repo_root(start: Path | None = None) -> Path | None:
    cur = (start or package_root()).resolve()
    for _ in range(8):
        if (cur / ".git").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def viz_dir_has_pngs(root: Path) -> bool:
    return any((root / name).is_file() for name in ILL_PNG_NAMES)


def _repo_viz_candidates() -> list[tuple[Path, str]]:
    seen: set[Path] = set()
    out: list[tuple[Path, str]] = []
    repo = git_repo_root()
    for raw, label in (
        (package_root() / REPO_VIZ_FALLBACK, "repo_docs_viz"),
        ((repo / REPO_VIZ_FALLBACK) if repo is not None else None, "repo_root_docs_viz"),
    ):
        if raw is None:
            continue
        path = raw.resolve()
        if path in seen:
            continue
        seen.add(path)
        out.append((path, label))
    return out


def _expand(raw: str | Path) -> Path:
    return Path(os.path.expanduser(str(raw))).resolve()


def _env_path(name: str, environ: dict[str, str] | None = None) -> Path | None:
    env = environ if environ is not None else os.environ
    raw = (env.get(name) or "").strip()
    if not raw:
        return None
    return _expand(raw)


def resolve_artifact_root(*, explicit: Path | None = None, environ: dict[str, str] | None = None) -> tuple[Path, str]:
    """Prefer operator-configured root, then local dry-run SoT, then repo data/."""
    if explicit is not None:
        return _expand(explicit), "explicit"
    configured = _env_path(ENV_ARTIFACT_ROOT, environ)
    if configured is not None:
        return configured, f"env:{ENV_ARTIFACT_ROOT}"
    if DEFAULT_EXTERNAL_ARTIFACT_ROOT.is_dir():
        return DEFAULT_EXTERNAL_ARTIFACT_ROOT.resolve(), "external_dryrun"
    return package_data_dir().resolve(), "repo_data"


def resolve_viz_root(*, explicit: Path | None = None, environ: dict[str, str] | None = None) -> tuple[Path, str]:
    """Prefer env, then Illustrator shared dir, then committed dry-run fallbacks.

    Shared SoT `/workspace/illustrator_ops/golf_offshoot/` wins when it has Ill
    PNGs. An empty shared directory does not hide a fallback that actually has
    the charts. Repo fallbacks: `golf-offshoot/docs/viz/...` and repo-root
    `docs/viz/golf_offshoot_dryrun_2026-09-07/` (Illustrator PR #140).
    """
    if explicit is not None:
        return _expand(explicit), "explicit"
    configured = _env_path(ENV_VIZ_ROOT, environ)
    if configured is not None:
        return configured, f"env:{ENV_VIZ_ROOT}"
    discovered: list[tuple[Path, str]] = []
    if DEFAULT_EXTERNAL_VIZ_ROOT.is_dir():
        discovered.append((DEFAULT_EXTERNAL_VIZ_ROOT.resolve(), "illustrator_ops"))
    discovered.extend((path, label) for path, label in _repo_viz_candidates() if path.is_dir())
    with_pngs = [(path, label) for path, label in discovered if viz_dir_has_pngs(path)]
    if with_pngs:
        return with_pngs[0]
    if discovered:
        return discovered[0]
    return (package_data_dir() / "viz").resolve(), "repo_data_viz"


def resolve_shadow_path(
    artifact_root: Path,
    *,
    explicit: Path | None = None,
    environ: dict[str, str] | None = None,
) -> tuple[Path, str]:
    if explicit is not None:
        return _expand(explicit), "explicit"
    configured = _env_path(ENV_SHADOW_PATH, environ)
    if configured is not None:
        return configured, f"env:{ENV_SHADOW_PATH}"
    return (artifact_root / "shadow" / "advises.jsonl").resolve(), "artifact_root"


def resolve_roots(
    *,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
    shadow_path: Path | None = None,
    environ: dict[str, str] | None = None,
) -> ResolvedRoots:
    art, art_src = resolve_artifact_root(explicit=artifact_root, environ=environ)
    viz, viz_src = resolve_viz_root(explicit=viz_root, environ=environ)
    shadow, shadow_src = resolve_shadow_path(art, explicit=shadow_path, environ=environ)
    return ResolvedRoots(
        artifact_root=art,
        viz_root=viz,
        shadow_path=shadow,
        artifact_source=art_src,
        viz_source=viz_src,
        shadow_source=shadow_src,
    )


def safe_under(path: Path, root: Path) -> Path:
    """Resolve and require path to stay inside root. Blocks traversal."""
    root_r = _expand(root)
    if not path.is_absolute():
        candidate = (root_r / path).resolve()
    else:
        candidate = path.resolve()
    try:
        candidate.relative_to(root_r)
    except ValueError as exc:
        raise PathUnsafeError(f"path escapes root: {path}") from exc
    return candidate


def safe_existing_file(path: Path, root: Path) -> Path | None:
    try:
        candidate = safe_under(path, root)
    except PathUnsafeError:
        return None
    if candidate.is_file():
        return candidate
    return None
