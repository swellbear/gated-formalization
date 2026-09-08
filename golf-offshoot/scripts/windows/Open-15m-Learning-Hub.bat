@echo off
setlocal EnableExtensions
title Golf Offshoot — 15m Kalshi Learning Hub
echo ========================================================================
echo   15-MIN KALSHI LEARNING LANE
echo   Trading NOT ARMED. Paper observation only.
echo   AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH
echo   Paper watch repeats researcher to systems. Founder does not click cycles.
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

echo Starting python -m golf_offshoot shell --lane learning_lane_15m
echo The hub is the browser page, not this window. Leave this console open.
%PY% -m golf_offshoot shell --host 127.0.0.1 --port 8765 --lane learning_lane_15m %*
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
  echo Hub exited with code %ERR%.
  pause
)
exit /b %ERR%
