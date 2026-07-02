param(
    [string]$TaskPrefix = "SAF-LTR",
    [string]$Cycle48hAt = "08:00",
    [string]$WeeklyAt = "09:00",
    [ValidateSet("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")]
    [string]$WeeklyDay = "Monday"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$runnerScript = Join-Path $repoRoot "tools\scheduler\run_ops_cycle.ps1"

if (-not (Test-Path $runnerScript)) {
    throw "Brak skryptu runner: $runnerScript"
}

$task48hName = "$TaskPrefix Ops Cycle 48h"
$taskWeeklyName = "$TaskPrefix Ops Cycle Weekly"

$incidentOwner = "Orkiestrator"
$incidentEta = "<=24h"
$incidentImpact = "Kontrola operacyjna SAF/LTR"

$action48hArgs = '-NoProfile -ExecutionPolicy Bypass -File "{0}" -Cycle 48h -IncidentOwner "{1}" -IncidentEta "{2}" -IncidentImpact "{3}"' -f $runnerScript, $incidentOwner, $incidentEta, $incidentImpact
$actionWeeklyArgs = '-NoProfile -ExecutionPolicy Bypass -File "{0}" -Cycle weekly -IncludeOwnerSummary -IncidentOwner "{1}" -IncidentEta "{2}" -IncidentImpact "{3}"' -f $runnerScript, $incidentOwner, $incidentEta, $incidentImpact

$action48h = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $action48hArgs
$actionWeekly = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $actionWeeklyArgs

$trigger48h = New-ScheduledTaskTrigger -Daily -DaysInterval 2 -At $Cycle48hAt
$triggerWeekly = New-ScheduledTaskTrigger -Weekly -WeeksInterval 1 -DaysOfWeek $WeeklyDay -At $WeeklyAt

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 6)

Register-ScheduledTask -TaskName $task48hName -Action $action48h -Trigger $trigger48h -Settings $settings -Description "SAF/LTR automated ops cycle every 48h" -Force | Out-Null
Register-ScheduledTask -TaskName $taskWeeklyName -Action $actionWeekly -Trigger $triggerWeekly -Settings $settings -Description "SAF/LTR weekly ops cycle + owner summary" -Force | Out-Null

Write-Output "[OK] Registered: $task48hName"
Write-Output "[OK] Registered: $taskWeeklyName"
