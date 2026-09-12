@echo off
setlocal EnableExtensions
title KXBTC15M PREVIEW hub — draft, not master, not armed
echo ========================================================================
echo   KXBTC15M PREVIEW HUB
echo   Draft PR checkout only. Does NOT switch git branches.
echo   Does NOT touch master. Not go-live. Trading NOT ARMED.
echo   Paper observation only. PaperWatch is the loop.
echo   Copy Open-15m-Hub-PREVIEW.url to Desktop to open the page.
echo   Keep THIS .bat in the PR golf-offshoot folder so it runs this checkout.
echo ========================================================================

cd /d "%~dp0"
if not exist "src\golf_offshoot" (
  echo This launcher must stay in the PR golf-offshoot folder next to src\.
  echo It will not git-checkout another tree and will not start master.
  echo Copy Open-15m-Hub-PREVIEW.url to Desktop to open http://127.0.0.1:8765
  echo after the hub from THIS checkout is running.
  pause
  exit /b 1
)

rem One process on 8765. Do not start a second hub.
netstat -ano | findstr /R /C:":8765 .*LISTENING" >nul
if not errorlevel 1 (
  echo Preview hub already listening on 127.0.0.1:8765 — not starting another.
  echo Open http://127.0.0.1:8765  ^(or the .url on your Desktop^).
  pause
  exit /b 0
)

set "PYTHONPATH=%CD%\src;%PYTHONPATH%"

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
echo Preview: http://127.0.0.1:8765
echo The hub is the browser page, not this window. Leave this console open.
%PY% -m golf_offshoot shell --host 127.0.0.1 --port 8765 --lane learning_lane_15m %*
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
  echo Hub exited with code %ERR%.
  pause
)
exit /b %ERR%
