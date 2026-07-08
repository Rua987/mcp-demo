# Reproducible CE x Godot live demo (T3MP3ST-style receipts).
# Prerequisites: Godot editor open on mcp-demo, MCP plugin connected, game in play (F5).
#
# Usage:
#   .\scripts\ce_live_demo.ps1
#   .\scripts\ce_live_demo.ps1 -WriteTarget 2 -SkipPytest

param(
    [int]$WriteTarget = 2,
    [switch]$SkipPytest,
    [switch]$SkipWrite
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Pipe = "\\.\pipe\CE_MCP_Bridge_v99"
$CeExe = "C:\Program Files\Cheat Engine\Cheat Engine.exe"
$Autorun = "C:\Program Files\Cheat Engine\autorun\linus_mcp_bridge.lua"
$LinusBridge = "C:\Users\admin\temple-iam-gpu-agents\tools\cheatengine-mcp\MCP_Server\ce_mcp_bridge.lua"

Write-Host "== CE live demo (mcp-demo) =="

if (-not (Test-Path $Autorun)) {
    $lua = "dofile([[$LinusBridge]])`n"
    [System.IO.File]::WriteAllText($Autorun, $lua)
    Write-Host "OK   CE autorun installed"
}

if (-not (Test-Path $Pipe)) {
    Write-Host "CE pipe absent — starting Cheat Engine..."
    Get-Process -Name "cheatengine*" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep 2
    Start-Process $CeExe
    $ready = $false
    for ($i = 0; $i -lt 25; $i++) {
        Start-Sleep 2
        if (Test-Path $Pipe) { $ready = $true; break }
    }
    if (-not $ready) {
        Write-Host "FAIL CE pipe not ready after 50s"
        exit 1
    }
    Write-Host "OK   CE pipe ready"
} else {
    Write-Host "OK   CE pipe present"
}

$godot = Get-Process -Name "Godot_v4.6.1-stable_win64" -ErrorAction SilentlyContinue
if (-not $godot) {
    Write-Host "WARN Godot editor not running — open mcp-demo in Godot + F5 play"
} else {
    Write-Host "OK   Godot PID $($godot.Id)"
}

Set-Location $Root
$pyArgs = @("scripts/ce_live_demo.py", "--write-target", $WriteTarget)
if ($SkipPytest) { $pyArgs += "--skip-pytest" }
if ($SkipWrite) { $pyArgs += "--skip-write" }

python @pyArgs
exit $LASTEXITCODE
