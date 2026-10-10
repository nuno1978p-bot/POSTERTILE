@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL%==0 (set "PYTHON=py -3") else (set "PYTHON=python")
if not exist ".venv\Scripts\python.exe" (
  %PYTHON% -m venv .venv
  if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto :error
exit /b 0
:error
echo.
echo ERRO: verifica a instalacao do Python 3.10+ e a ligacao a Internet.
pause
exit /b 1
