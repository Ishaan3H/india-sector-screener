@echo off
REM Rebuild the Indian market weekly sector screener (Windows).
REM
REM   run_weekly.bat
REM
REM Fetches fresh prices, recomputes the sector table, and regenerates
REM index.html. data.json is only overwritten on a successful fetch, so a failed
REM run leaves the previous week's page intact rather than blanking it.
setlocal

cd /d "%~dp0"

REM Prefer the py launcher; fall back to python on PATH.
where py >nul 2>&1 && (set PY=py) || (set PY=python)

%PY% --version >nul 2>&1
if errorlevel 1 (
  echo.
  echo ERROR: Python was not found.
  echo Install it from https://www.python.org/downloads/windows/
  echo and make sure "Add python.exe to PATH" is ticked during setup.
  echo.
  exit /b 1
)

echo [%date% %time%] fetching prices ...
%PY% screener.py
if errorlevel 1 exit /b 1

echo [%date% %time%] rendering page ...
%PY% render.py
if errorlevel 1 exit /b 1

%PY% -c "import json; d=json.load(open('data.json',encoding='utf-8')); print(); print('Week %%s -> %%s (baseline %%s), %%d stocks' %% (d['week_start'], d['week_end'], d['baseline'], d['universe_size'])); [print('  %%d. %%-26s %%+6.2f%%%%  best %%s %%+.1f%%%%' %% (i, s['sector'], s['week'], s['best'], s['best_week'])) for i, s in enumerate(d['sectors'][:3], 1)]"

echo.
echo [%date% %time%] done -^> %cd%\index.html
echo Open it with:  start index.html
endlocal
