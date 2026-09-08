# Register a logon task that starts the 15m hub and restarts it on failure.
# Publishing is still manual. This only keeps PaperWatch alive.
# Run once from an elevated or same-user PowerShell:
#   powershell -ExecutionPolicy Bypass -File golf-offshoot/scripts/windows/Register-15m-Learning-Hub-Task.ps1

$ErrorActionPreference = "Stop"
$taskName = "GatedFormalization-15mLearningHub"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$starter = Join-Path $here "Start-15m-Learning-Hub-Autostart.bat"
if (-not (Test-Path -LiteralPath $starter)) {
    throw "Missing starter: $starter"
}

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Start the 15m learning hub at logon. Paper observation only. Trading NOT ARMED. Restart on failure so tonight does not depend on an open console.</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$starter</Command>
      <WorkingDirectory>$here</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$tmp = Join-Path $env:TEMP "gpf-15m-hub-task.xml"
Set-Content -LiteralPath $tmp -Value $xml -Encoding Unicode
schtasks.exe /Create /TN $taskName /XML $tmp /F
if ($LASTEXITCODE -ne 0) {
    throw "schtasks failed with exit $LASTEXITCODE"
}
Write-Host "Registered $taskName at logon with restart-on-failure (1 min, 3 times)."
Write-Host "Starter: $starter"
Write-Host "This does not publish Pages. The public page is not self-maintaining."
