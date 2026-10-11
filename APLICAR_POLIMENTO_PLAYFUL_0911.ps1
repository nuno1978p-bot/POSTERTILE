$ErrorActionPreference = "Stop"
$project = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
$python = Join-Path $project ".venv\Scripts\python.exe"
$script = Join-Path $PSScriptRoot "patch_playful_polish.py"
if (!(Test-Path $python)) { throw "Python DEV nao encontrado: $python" }
if (!(Test-Path $script)) { throw "Hotfix nao encontrado: $script" }
Write-Host "=== NONIVERUS v0.9.1.1 — VERIFICAR ===" -ForegroundColor Cyan
& $python $script --project $project --check
if ($LASTEXITCODE -ne 0) { throw "Verificacao falhou. O projeto nao foi alterado." }
Write-Host "=== NONIVERUS v0.9.1.1 — APLICAR ===" -ForegroundColor Cyan
& $python $script --project $project --apply
if ($LASTEXITCODE -ne 0) { throw "Aplicacao interrompida em seguranca." }
Write-Host "PRONTO: abre a app DEV para validar a dashboard." -ForegroundColor Green
