# Windows Phase 1 hub launcher

Primary machine path. Double-click starts the local observation hub and opens the browser. Trading stays **NOT ARMED**. Paper auto-apply is **PAPER OBSERVATION ONLY**. AI never deposits / withdraws / transfers cash.

## Clickable files

| Path | What it does |
|------|----------------|
| `golf-offshoot/scripts/windows/Open-Phase1-Hub.bat` | Starts `python -m golf_offshoot shell --host 127.0.0.1 --port 8765` and lets the shell open `http://127.0.0.1:8765`. Keep the window open. |
| `golf-offshoot/scripts/windows/Install-Desktop-Shortcut.bat` | Double-click this once. It runs the PowerShell installer. |
| `golf-offshoot/scripts/windows/Install-Desktop-Shortcut.ps1` | Writes `Desktop\Golf Offshoot Phase 1 Hub.lnk` pointing at `Open-Phase1-Hub.bat`. |

Do not hand-wire a shortcut unless the installer cannot run. If PowerShell is blocked, copy `Open-Phase1-Hub.bat` to your Desktop.

## First-time install

1. From Explorer: `golf-offshoot\scripts\windows\Install-Desktop-Shortcut.bat`
2. Double-click **Golf Offshoot Phase 1 Hub** on the Desktop
3. Leave the console window open while you use the hub

Python 3 must be on `PATH` (`py -3` or `python`).

## Phone

Phase 1 phone access is **notify-first** (`NTFY_TOPIC` completion ping). There is no remote phone UI, no Tailscale requirement, and no one-tap bet from a phone.
