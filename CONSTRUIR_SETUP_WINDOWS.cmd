@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NONIVERUS - Construir EXE e Setup v0.8.12

echo ======================================================
echo NONIVERUS POSTERTILE - BUILD WINDOWS v0.8.12
echo ======================================================
echo.
if not exist "main.py" goto :missing
if not exist "ui\Main.qml" goto :missing
if not exist "assets\branding\postertile_icon.ico" goto :missing

if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>&1
  if not errorlevel 1 (
    py -3 -m venv ".venv"
  ) else (
    python -m venv ".venv"
  )
)
if not exist ".venv\Scripts\python.exe" goto :venvfail
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt "pyinstaller>=6,<7"
if errorlevel 1 goto :error

".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onedir --windowed ^
 --name "NONIVERUS PosterTile" ^
 --icon "assets\branding\postertile_icon.ico" ^
 --version-file "version_info.txt" ^
 --add-data "ui;ui" ^
 --add-data "assets;assets" ^
 --collect-all "PySide6.QtQml" ^
 --hidden-import "PySide6.QtQuick" ^
 --hidden-import "PySide6.QtQuickControls2" ^
 --hidden-import "PySide6.QtQuickWidgets" ^
 main.py
if errorlevel 1 goto :error
if not exist "dist\NONIVERUS PosterTile\NONIVERUS PosterTile.exe" goto :error

echo.
echo EXE criado em dist\NONIVERUS PosterTile\
echo.
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "D:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe" set "ISCC=D:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
if not defined ISCC (
  for %%I in (ISCC.exe) do if not "%%~$PATH:I"=="" set "ISCC=%%~$PATH:I"
)
if not defined ISCC goto :inno_missing
"%ISCC%" "installer\PosterTile.iss"
if errorlevel 1 goto :error
if not exist "release\NONIVERUS_PosterTile_Setup_v0.8.12.exe" goto :error
echo.
echo SETUP CRIADO: release\NONIVERUS_PosterTile_Setup_v0.8.12.exe
echo.
echo Antes da distribuicao publica: testar num PC limpo e rever licencas.
pause
exit /b 0

:inno_missing
echo.
echo EXE em pasta OK. Instalador NAO criado: Inno Setup 6 em falta.
echo Instala Inno Setup 6 e executa este script novamente.
echo Podes abrir installer\PosterTile.iss no Inno Setup e compilar.
pause
exit /b 2

:missing
echo Faltam ficheiros de origem. Extrai o ZIP completo.
goto :error
:venvfail
echo Falhou criacao de ambiente Python para BUILD.
goto :error
:error
echo.
echo BUILD FALHOU. Nao distribuas um instalador antigo.
pause
exit /b 1
