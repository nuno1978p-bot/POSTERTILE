# NONIVERUS PosterTile v0.9.0.1 — atualizacao segura do codigo DEV
[CmdletBinding()]
param([string]$Dev = "C:\NONIVERUS\NONIVERUS_POSTERTILE_DEV")

$ErrorActionPreference = "Stop"
$files = @(
    "ui\Main.qml",
    "build_editions.py",
    "main.py",
    "version_info.txt",
    "installer\PosterTile_owner.iss",
    "installer\PosterTile_preview.iss"
)

if (!(Test-Path -LiteralPath (Join-Path $Dev "main.py"))) {
    throw "Pasta DEV nao encontrada: $Dev"
}

foreach ($file in $files) {
    if (!(Test-Path -LiteralPath (Join-Path $PSScriptRoot $file))) {
        throw "Ficheiro do hotfix em falta: $file"
    }
    if (!(Test-Path -LiteralPath (Join-Path $Dev $file))) {
        throw "Ficheiro original em falta: $file"
    }
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backup = Join-Path $Dev ("_hotfix_backups\ControlCenter_v090_" + $stamp)
foreach ($file in $files) {
    $old = Join-Path $Dev $file
    $new = Join-Path $PSScriptRoot $file
    $backupFile = Join-Path $backup $file
    $parent = Split-Path -Parent $backupFile
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    Copy-Item -LiteralPath $old -Destination $backupFile -Force
    Copy-Item -LiteralPath $new -Destination $old -Force
    Write-Host "Atualizado: $file"
}
Write-Host ""
Write-Host "HOTFIX v0.9.0.1 aplicado." -ForegroundColor Green
Write-Host "Copia de seguranca: $backup"
Write-Host "Proximo comando: cd $Dev"
Write-Host "Depois: .\CONSTRUIR_PREVIEW_WINDOWS.cmd"
