# Writes js/mods-data.js from mods.json so the site works from file:// (no fetch).
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteRoot = Split-Path -Parent $here
$jsonPath = Join-Path $siteRoot 'mods.json'
$outPath = Join-Path $siteRoot 'js\mods-data.js'

$utf8 = New-Object System.Text.UTF8Encoding $false
$json = [System.IO.File]::ReadAllText($jsonPath, $utf8).TrimEnd()
$header = "/* Generated from mods.json. Edit mods.json, then run this script. */`r`n"
$body = $header + "window.H3ND_MODS = " + $json + ";`r`n"
[System.IO.File]::WriteAllText($outPath, $body, $utf8)
Write-Host "Wrote js/mods-data.js"
