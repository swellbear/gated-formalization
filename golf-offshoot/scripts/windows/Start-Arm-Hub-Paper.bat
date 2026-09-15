@echo off
setlocal EnableExtensions
title ARM hub — paper watch (NOT ARMED)
echo ========================================================================
echo   ARM HUB  (separate from the 15m learning-lane hub)
echo   Trading NOT ARMED. Paper $500 accumulate.
echo   Unattended Python. No bot in the loop. Never port 8765.
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

echo Starting python -m golf_offshoot arm-hub --watch
echo Leave this console open. To stop: python -m golf_offshoot arm-hub --kill
%PY% -m golf_offshoot arm-hub --watch %*
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
  echo ARM hub exited with code %ERR%.
  pause
)
exit /b %ERR%
