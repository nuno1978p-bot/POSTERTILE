@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NONIVERUS - Compilar executavel Windows
echo ======================================================
echo  NONIVERUS POSTERTILE LUXURY STUDIO v0.8.1
echo  Compilacao Windows - EXE sem Python externo
echo ======================================================
echo.
if not exist ".venv\Scripts\python.exe" (
   where py >nul 2>&1
   if not errorlevel 1 (
       py -3 -m venv .venv
   ) else (
       python -m venv .venv
   )
)
if not exist ".venv\Scripts\python.exe" goto :error
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt pyinstaller
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onefile --windowed ^
 --name "NONIVERUS PosterTile" ^
 --icon "assets\branding\postertile_icon.ico" ^
 --version-file "version_info.txt" ^
 --add-data "ui;ui" ^
 --add-data "assets;assets" ^
 --hidden-import PySide6.QtQuick ^
 --hidden-import PySide6.QtQml ^
 main.py
if errorlevel 1 goto :error
if not exist "dist\NONIVERUS PosterTile.exe" goto :error
echo.
echo OK: dist\NONIVERUS PosterTile.exe
echo Podes copiar este EXE para outro PC Windows compativel.
echo Nao necessita de Python instalado nesse PC.
echo.
pause
exit /b 0
:error
echo.
echo FALHA na compilacao. Consulta mensagens acima.
echo E necessario compilar em WINDOWS, com Python 3.10+ e Internet na primeira compilacao.
pause
exit /b 1
