# Creates a Desktop shortcut to the Phase 1 observation hub.
# Trading stays NOT ARMED. AI never deposits / withdraws / transfers cash.
# Does not require Tailscale or a phone UI.

$ErrorActionPreference = "Stop"
$HubBat = Join-Path $PSScriptRoot "Open-Phase1-Hub.bat"
if (-not (Test-Path -LiteralPath $HubBat)) {
    throw "Missing launcher: $HubBat"
}
$OffshootRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Desktop = [Environment]::GetFolderPath("Desktop")
if (-not $Desktop) {
    $Desktop = Join-Path $env:USERPROFILE "Desktop"
}
New-Item -ItemType Directory -Force -Path $Desktop | Out-Null
$LnkPath = Join-Path $Desktop "Golf Offshoot Phase 1 Hub.lnk"

$Wsh = New-Object -ComObject WScript.Shell
$Shortcut = $Wsh.CreateShortcut($LnkPath)
$Shortcut.TargetPath = $HubBat
$Shortcut.WorkingDirectory = $OffshootRoot
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Phase 1 observation hub. Trading NOT ARMED. PAPER OBSERVATION ONLY. AI never moves cash."
$Py = $null
foreach ($name in @("py", "python")) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source) {
        $Py = $cmd.Source
        break
    }
}
if ($Py) {
    $Shortcut.IconLocation = "$Py,0"
}
$Shortcut.Save()

Write-Host "Created Desktop shortcut:"
Write-Host "  $LnkPath"
Write-Host "Target:"
Write-Host "  $HubBat"
Write-Host "PHASE 1 OBSERVATION. Trading NOT ARMED. PAPER OBSERVATION ONLY."
Write-Host "AI NEVER DEPOSITS / WITHDRAWS / TRANSFERS CASH."
