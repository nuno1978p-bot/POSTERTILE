# NONIVERUS PosterTile v0.9.0.2 — instaladores capazes de mostrar "Atualizar".
[CmdletBinding()]
param([string]$Dev = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV")

$ErrorActionPreference = "Stop"
$Expected = [ordered]@{
    "build_editions.py" = "62C0BB29F6CA98D53362DBC7C0268BFFE01BA0FE22E55E9A7991D7C4A64F06E8"
    "installer\PosterTile_owner.iss" = "F6AD8F98307020CFFFC016EA196AF790370B1233443CFAC7D1FDE48F6B5C244A"
    "installer\PosterTile_preview.iss" = "6170EC8C89BC06ED5210DCFFE4296747FB7A39791EF0BC8C053703C492E272A7"
    "main.py" = "C2A54ECCA264C1EFEA6B2123F37F317D14B05839BD08926E7D28B95EEC1CC3A8"
    "ui\Main.qml" = "B6FF7C07C03F80E0FF883847211FF6BEDF6569E2E0487600ABF642F7202D8D0E"
    "version_info.txt" = "26B2AD768D6431C690E639533824F44B288F8FE62ACA8259D5C74CCC4E5ECC3F"
}

if (!(Test-Path -LiteralPath (Join-Path $Dev "build_editions.py"))) {
    throw "Nao encontrei o projeto DEV: $Dev"
}

# Todas as validacoes ANTES de copiar; recusa sobrescrever fontes inesperadas.
foreach ($entry in $Expected.GetEnumerator()) {
    $file = $entry.Key
    $source = Join-Path $PSScriptRoot $file
    $target = Join-Path $Dev $file
    if (!(Test-Path -LiteralPath $source)) { throw "Ficheiro do patch em falta: $file" }
    if (!(Test-Path -LiteralPath $target)) { throw "Ficheiro DEV em falta: $file" }
    $actual = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
    if ($actual -ne $entry.Value) {
        throw "O ficheiro $file difere do hotfix v0.9.0.1. Nao foi substituido. Pede uma atualizacao personalizada."
    }
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupRoot = Join-Path $env:LOCALAPPDATA ("NONIVERUS\PosterTile\build_backups\InstallerUpdate_v0902_" + $timestamp)

foreach ($entry in $Expected.GetEnumerator()) {
    $file = $entry.Key
    $dest = Join-Path $Dev $file
    $source = Join-Path $PSScriptRoot $file
    $backup = Join-Path $backupRoot $file
    New-Item -ItemType Directory -Path (Split-Path -Parent $backup) -Force | Out-Null
    Copy-Item -LiteralPath $dest -Destination $backup -Force
    Copy-Item -LiteralPath $source -Destination $dest -Force
    Write-Host "Atualizado: $file"
}

Write-Host ""
Write-Host "Patch v0.9.0.2 aplicado. Owner e Preview continuam separados." -ForegroundColor Green
Write-Host "Backup do codigo anterior: $backupRoot"
Write-Host "IMPORTANTE: Nao voltes a executar license_authority.py init."
Write-Host "Para gerar instaladores novos, executa CONSTRUIR_OWNER_WINDOWS.cmd e CONSTRUIR_PREVIEW_WINDOWS.cmd."
