# Packs finished VCMI portrait folders from ../build into downloads/*.zip.
# Does not touch game installs or work/ pipeline files.
# Usage (from repo root or from mods-site/):  powershell -File mods-site/scripts/pack-downloads.ps1

$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteRoot = Split-Path -Parent $here
$repoRoot = Split-Path -Parent $siteRoot
$downloads = Join-Path $siteRoot 'downloads'
$stagingRoot = Join-Path $siteRoot '_zip-staging'

# Factions with a fan-facing package in build/. Specials stay off until built.
$packs = @(
    @{ Build = 'vcmi-hero-portraits-tower-v1';       ZipFolder = 'heroes3-new-design-portraits-tower-v1' },
    @{ Build = 'vcmi-hero-portraits-necropolis-v1';  ZipFolder = 'heroes3-new-design-portraits-necropolis-v1' },
    @{ Build = 'vcmi-hero-portraits-castle-v1';      ZipFolder = 'heroes3-new-design-portraits-castle-v1' },
    @{ Build = 'vcmi-hero-portraits-rampart-v1';     ZipFolder = 'heroes3-new-design-portraits-rampart-v1' },
    @{ Build = 'vcmi-hero-portraits-inferno-v1';     ZipFolder = 'heroes3-new-design-portraits-inferno-v1' },
    @{ Build = 'vcmi-hero-portraits-dungeon-v1';     ZipFolder = 'heroes3-new-design-portraits-dungeon-v1' },
    @{ Build = 'vcmi-hero-portraits-stronghold-v1';  ZipFolder = 'heroes3-new-design-portraits-stronghold-v1' },
    @{ Build = 'vcmi-hero-portraits-fortress-v1';    ZipFolder = 'heroes3-new-design-portraits-fortress-v1' },
    @{ Build = 'vcmi-hero-portraits-conflux-v1';     ZipFolder = 'heroes3-new-design-portraits-conflux-v1' },
    @{ Build = 'vcmi-hero-portraits-factory-v1';     ZipFolder = 'heroes3-new-design-portraits-factory-v1' },
    @{ Build = 'vcmi-hero-portraits-cove-v1';        ZipFolder = 'heroes3-new-design-portraits-cove-v1' },
    @{ Build = 'vcmi-hero-portraits-bulwark-v1';     ZipFolder = 'heroes3-new-design-portraits-bulwark-v1' }
)

New-Item -ItemType Directory -Force -Path $downloads | Out-Null
if (Test-Path $stagingRoot) { Remove-Item -Recurse -Force $stagingRoot }
New-Item -ItemType Directory -Force -Path $stagingRoot | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem

foreach ($pack in $packs) {
    $src = Join-Path $repoRoot ("build\" + $pack.Build)
    $modJson = Join-Path $src 'mod.json'
    if (-not (Test-Path $modJson)) {
        Write-Host ("SKIP (no mod.json): " + $pack.Build)
        continue
    }

    $stage = Join-Path $stagingRoot $pack.ZipFolder
    New-Item -ItemType Directory -Force -Path $stage | Out-Null
    Copy-Item -Path (Join-Path $src '*') -Destination $stage -Recurse -Force

    $zipPath = Join-Path $downloads ($pack.ZipFolder + '.zip')
    if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $stage,
        $zipPath,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $true
    )

    $mb = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
    Write-Host ("ZIP " + $pack.ZipFolder + ".zip  " + $mb + " MB")
}

Remove-Item -Recurse -Force $stagingRoot

$exportSprites = Join-Path $here 'export-roster-sprites.py'
if (Test-Path $exportSprites) {
    python $exportSprites
}

Write-Host 'Done.'
