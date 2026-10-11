param(
    [string]$Project = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
)
$ErrorActionPreference = "Stop"
$py = Join-Path $Project ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { throw "Python DEV não encontrado: $py" }
$patch = Join-Path $PSScriptRoot "patch_playful.py"
Write-Host "NONIVERUS Playful Studio v0.9.1 / V3 - verificacao" -ForegroundColor Cyan
& $py $patch --project $Project
if ($LASTEXITCODE -ne 0) { throw "Verificacao falhou. Nao aplicar." }
Write-Host "NONIVERUS Playful Studio v0.9.1 / V3 - aplicar" -ForegroundColor Cyan
& $py $patch --project $Project --apply
if ($LASTEXITCODE -ne 0) { throw "Aplicacao interrompida; verifica os ficheiros e a copia de seguranca." }
