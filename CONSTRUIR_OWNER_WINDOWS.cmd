@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NONIVERUS - Build OWNER v0.9.0
echo NONIVERUS POSTERTILE - OWNER
echo.
if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv ".venv"
    if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt -r requirements_authority.txt "pyinstaller>=6,<7"
if errorlevel 1 goto :error
".venv\Scripts\python.exe" build_editions.py owner
if errorlevel 1 goto :error
echo.
echo Build terminado. Confirmar ambos os instaladores antes de partilhar.
pause
exit /b 0
:error
echo.
echo BUILD FALHOU. Nao distribuas nenhum instalador antigo.
pause
exit /b 1
