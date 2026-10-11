param(
    [string]$Projeto = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
)

$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "patch_theme_header_0915.py"

if (-not (Test-Path -LiteralPath $script)) {
    throw "O script da correção não foi encontrado."
}
if (-not (Test-Path -LiteralPath (Join-Path $Projeto "ui\Main.qml"))) {
    throw "O projeto DEV ou o ficheiro ui\Main.qml não foi encontrado: $Projeto"
}

# Preferir a venv DEV, mas usar a venv estável se a DEV não existir.
$py = Join-Path $Projeto ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $py)) {
    $py = "C:\NONIVERUS\NONIVERUS_POSTERTILE\.venv\Scripts\python.exe"
}
if (-not (Test-Path -LiteralPath $py)) {
    throw "Python não encontrado nas venv DEV/estável. Não foi feita qualquer alteração."
}

Write-Host "`n===== NONIVERUS v0.9.1.5 / VERIFICAÇÃO SEM ALTERAÇÕES =====" -ForegroundColor Cyan
& $py $script --project $Projeto --check
if ($LASTEXITCODE -ne 0) {
    throw "VERIFICAÇÃO FALHOU. Não foi feita qualquer alteração."
}

Write-Host "`n===== NONIVERUS v0.9.1.5 / APLICAR =====" -ForegroundColor Cyan
& $py $script --project $Projeto --apply
if ($LASTEXITCODE -ne 0) {
    throw "Aplicação interrompida. Verifica a mensagem acima e o backup, se existir."
}
Write-Host "`nSUCESSO: O cabeçalho está pronto para testar na aplicação DEV." -ForegroundColor Green
Write-Host "Para abrir: & `"$py`" `"$Projeto\main.py`""
