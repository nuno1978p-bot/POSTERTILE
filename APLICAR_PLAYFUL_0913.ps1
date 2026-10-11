$ErrorActionPreference = "Stop"
$project = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV"
$python = Join-Path $project ".venv\Scripts\python.exe"
$patch = Join-Path $PSScriptRoot "patch_playful_responsive_0913.py"

if (!(Test-Path -LiteralPath $python)) {
    throw "Ambiente Python nao encontrado: $python"
}
if (!(Test-Path -LiteralPath $patch)) {
    throw "Ficheiro de correcao nao encontrado: $patch"
}

Write-Host "`nNONIVERUS Playful Studio v0.9.1.3 — verificacao" -ForegroundColor Cyan
& $python $patch --project $project --check
if ($LASTEXITCODE -ne 0) {
    throw "A verificacao falhou. Nao foram efetuadas alteracoes. Envia a mensagem de erro."
}
Write-Host "`nNONIVERUS Playful Studio v0.9.1.3 — aplicar" -ForegroundColor Cyan
& $python $patch --project $project --apply
if ($LASTEXITCODE -ne 0) {
    throw "A atualizacao nao foi concluida. Envia a mensagem de erro."
}
Write-Host "`nCorrecao v0.9.1.3 concluida. Testa o programa antes de compilar." -ForegroundColor Green
