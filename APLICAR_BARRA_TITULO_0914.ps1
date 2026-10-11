$ErrorActionPreference = "Stop"
$projeto = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
$python = Join-Path $projeto ".venv\Scripts\python.exe"
$script = Join-Path $PSScriptRoot "patch_titlebar.py"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Python DEV nao encontrado: $python"
}
if (-not (Test-Path -LiteralPath $script)) {
    throw "Ficheiro patch_titlebar.py nao encontrado."
}

Write-Host "NONIVERUS v0.9.1.4 - Simulacao segura" -ForegroundColor Cyan
& $python $script $projeto --check
if ($LASTEXITCODE -ne 0) { throw "Verificacao falhou. Nao foi alterado qualquer ficheiro." }

Write-Host "NONIVERUS v0.9.1.4 - Aplicacao" -ForegroundColor Cyan
& $python $script $projeto
if ($LASTEXITCODE -ne 0) { throw "Hotfix nao concluido. Consulta a mensagem acima." }
Write-Host "Pronto para testar a janela no Windows." -ForegroundColor Green
