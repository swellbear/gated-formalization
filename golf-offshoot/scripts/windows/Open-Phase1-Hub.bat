@echo off
setlocal EnableExtensions
title Golf Offshoot — Phase 1 Observation Hub
echo ========================================================================
echo   PHASE 1 OBSERVATION
echo   Trading NOT ARMED. Paper bankroll auto-apply is PAPER OBSERVATION ONLY.
echo   AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH
echo   Local hub only. Phone is notify-first. No remote trading UI.
echo ========================================================================
cd /d "%~dp0..\.."
if exist "src\golf_offshoot" set "PYTHONPATH=%CD%\src;%PYTHONPATH%"

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY (
  where python >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo Python 3 is not on PATH. Install Python 3, then run this again.
  pause
  exit /b 1
)

echo Starting python -m golf_offshoot shell on http://127.0.0.1:8765
echo The hub is the browser page, not this window. Leave this console open.
echo After git pull / artifact updates the hub reloads itself.
%PY% -m golf_offshoot shell --host 127.0.0.1 --port 8765 %*
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
  echo Hub exited with code %ERR%.
  pause
)
exit /b %ERR%
