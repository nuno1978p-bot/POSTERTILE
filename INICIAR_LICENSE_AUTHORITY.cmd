@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Ambiente Python nao encontrado. Executa CONSTRUIR_OWNER_WINDOWS.cmd.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" license_authority.py status
".venv\Scripts\python.exe" license_authority.py gui
if errorlevel 1 pause
