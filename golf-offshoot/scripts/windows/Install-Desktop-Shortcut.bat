@echo off
setlocal EnableExtensions
title Install Golf Offshoot Phase 1 Hub shortcut
echo Creating a Desktop shortcut to the Phase 1 observation hub.
echo Trading NOT ARMED. PAPER OBSERVATION ONLY.
echo AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Desktop-Shortcut.ps1"
if errorlevel 1 (
  echo Shortcut installer failed. You can still double-click Open-Phase1-Hub.bat
  echo at golf-offshoot\scripts\windows\Open-Phase1-Hub.bat
  pause
  exit /b 1
)
echo Done. Look on your Desktop for "Golf Offshoot Phase 1 Hub".
pause
