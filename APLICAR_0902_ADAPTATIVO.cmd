@echo off
setlocal
set "DEV=C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
set "PY=%DEV%\.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo ERRO: Python DEV nao encontrado em %PY%.
  exit /b 1
)
echo.
echo ===== NONIVERUS v0.9.0.2 / VERIFICACAO SEM ALTERACOES =====
"%PY%" "%~dp0patch_instalador_adaptativo.py" --project "%DEV%" --dry-run
if errorlevel 1 (
  echo.
  echo A verificacao falhou. Envia a mensagem antes de continuar.
  exit /b 1
)
echo.
echo ===== NONIVERUS v0.9.0.2 / APLICAR HOTFIX =====
"%PY%" "%~dp0patch_instalador_adaptativo.py" --project "%DEV%"
exit /b %ERRORLEVEL%
