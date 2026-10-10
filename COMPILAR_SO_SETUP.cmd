@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NONIVERUS - Compilar apenas instalador 0.8.1
if not exist "dist\NONIVERUS PosterTile\NONIVERUS PosterTile.exe" (
  echo FALTA o EXE actualizado. Executa CONSTRUIR_SETUP_WINDOWS.cmd.
  pause
  exit /b 2
)
powershell.exe -NoProfile -Command "if ((Get-Item -LiteralPath 'dist\NONIVERUS PosterTile\NONIVERUS PosterTile.exe').VersionInfo.FileVersion -ne '0.8.1.0') { exit 4 }"
if errorlevel 1 (
  echo O EXE existente nao tem versao 0.8.1.0.
  echo Recompila primeiro com CONSTRUIR_SETUP_WINDOWS.cmd.
  pause
  exit /b 3
)
set "ISCC="
if exist "D:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC=D:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC (
  echo Inno Setup nao encontrado. Usa CONSTRUIR_SETUP_WINDOWS.cmd.
  pause
  exit /b 1
)
if not exist release mkdir release
"%ISCC%" "installer\PosterTile.iss" > "release\inno-build-v081.log" 2>&1
if errorlevel 1 (
  echo Falha. Abre release\inno-build-v081.log.
  pause
  exit /b 1
)
if not exist "release\NONIVERUS_PosterTile_Setup_v0.8.1.exe" (
  echo Setup nao foi encontrado. Abre release\inno-build-v081.log.
  pause
  exit /b 1
)
echo OK: release\NONIVERUS_PosterTile_Setup_v0.8.1.exe
pause
