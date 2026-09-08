@echo off
setlocal EnableExtensions
title Golf Offshoot — 15m hub autostart
cd /d "%~dp0..\.."
if exist "src\golf_offshoot" set "PYTHONPATH=%CD%\src;%PYTHONPATH%"

rem Do not start a second hub. One process on 8765.
netstat -ano | findstr /R /C:":8765 .*LISTENING" >nul
if not errorlevel 1 (
  echo 15m hub already listening on 127.0.0.1:8765 — not starting another.
  exit /b 0
)

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY (
  where python >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo Python 3 is not on PATH.
  exit /b 1
)

echo Starting 15m hub headless. Trading NOT ARMED. Paper observation only.
%PY% -m golf_offshoot shell --host 127.0.0.1 --port 8765 --lane learning_lane_15m --no-browser
exit /b %ERRORLEVEL%
