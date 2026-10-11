param(
    [string]$ProjectPath = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
)

$ErrorActionPreference = "Stop"
$python = Join-Path $ProjectPath ".venv\Scripts\python.exe"
$patch = Join-Path $PSScriptRoot "patch_responsive_0912.py"
$qml = Join-Path $ProjectPath "ui\Main.qml"

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Python DEV não encontrado: $python"
}
if (-not (Test-Path -LiteralPath $qml -PathType Leaf)) {
    throw "QML não encontrado: $qml"
}
if (-not (Test-Path -LiteralPath $patch -PathType Leaf)) {
    throw "Patch não encontrado: $patch"
}

Write-Host "NONIVERUS Playful Studio - v0.9.1.2" -ForegroundColor Cyan
Write-Host "Verificação sem alterações..." -ForegroundColor Cyan

& $python $patch --project $ProjectPath --check
if ($LASTEXITCODE -ne 0) {
    throw "Verificação falhou. NENHUM ficheiro foi modificado."
}

Write-Host "A aplicar atualização pontual..." -ForegroundColor Cyan
& $python $patch --project $ProjectPath --apply
if ($LASTEXITCODE -ne 0) {
    throw "Aplicação interrompida. Revê a mensagem apresentada."
}

Write-Host "CONCLUÍDO: arranque maximizado e painel Playful responsivo." -ForegroundColor Green
Write-Host "Testar: .\.venv\Scripts\python.exe main.py" -ForegroundColor Green
