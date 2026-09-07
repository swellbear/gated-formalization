"""Desktop launcher helpers. Observation hub only. Never cash. Never a trade."""

from __future__ import annotations

from pathlib import Path

from golf_offshoot.operator_surface.modes import CASH_BADGE, NOT_ARMED, PAPER_ONLY, PHASE_1_OBSERVATION
from golf_offshoot.operator_surface.paths import package_root

SHORTCUT_STEM = "Golf Offshoot Phase 1 Hub"
WINDOWS_OPEN_BAT = Path("scripts") / "windows" / "Open-Phase1-Hub.bat"
WINDOWS_INSTALL_PS1 = Path("scripts") / "windows" / "Install-Desktop-Shortcut.ps1"
WINDOWS_INSTALL_BAT = Path("scripts") / "windows" / "Install-Desktop-Shortcut.bat"
UNIX_OPEN_SH = Path("scripts") / "open-phase1-hub.sh"


def launcher_paths(root: Path | None = None) -> dict[str, Path]:
    base = root or package_root()
    return {
        "open_hub_bat": base / WINDOWS_OPEN_BAT,
        "install_ps1": base / WINDOWS_INSTALL_PS1,
        "install_bat": base / WINDOWS_INSTALL_BAT,
        "open_hub_sh": base / UNIX_OPEN_SH,
    }


def write_desktop_launcher(*, desktop: Path, root: Path | None = None) -> Path:
    """Write a clickable Desktop launcher that starts the local Phase 1 hub.

    Windows: a `.bat` next to an optional `.lnk` created by the PowerShell
    installer. Other platforms: a `.desktop` / `.command` style shell wrapper.
    Does not bind remotely. Does not move cash.
    """
    base = root or package_root()
    paths = launcher_paths(base)
    desktop.mkdir(parents=True, exist_ok=True)
    dest = desktop / f"{SHORTCUT_STEM}.bat"
    dest.write_text(
        "\r\n".join(
            [
                "@echo off",
                f"rem {PHASE_1_OBSERVATION}. Trading {NOT_ARMED}. {PAPER_ONLY}.",
                f"rem {CASH_BADGE}.",
                f'call "{paths["open_hub_bat"]}" %*',
                "",
            ]
        ),
        encoding="utf-8",
    )
    unix = desktop / f"{SHORTCUT_STEM}.command"
    unix.write_text(
        "\n".join(
            [
                "#!/bin/sh",
                f"# {PHASE_1_OBSERVATION}. Trading {NOT_ARMED}. {PAPER_ONLY}.",
                f"# {CASH_BADGE}.",
                f'exec "{paths["open_hub_sh"]}" "$@"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    try:
        unix.chmod(unix.stat().st_mode | 0o111)
    except OSError:
        pass
    return dest
