param(
    [ValidateSet("pr", "48h", "weekly")]
    [string]$Cycle = "48h",
    [switch]$IncludeOwnerSummary,
    [string]$IncidentOwner = "Orkiestrator",
    [string]$IncidentEta = "TBD",
    [string]$IncidentImpact = "TBD"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $repoRoot

$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

$logPath = Join-Path $repoRoot "docs\operations\scheduler_runs.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"[$timestamp] START cycle=$Cycle ownerSummary=$IncludeOwnerSummary" | Out-File -FilePath $logPath -Encoding utf8 -Append

& $pythonExe "tools/ops_cycle_runner.py" "--cycle" $Cycle "--incident-owner" $IncidentOwner "--incident-eta" $IncidentEta "--incident-impact" $IncidentImpact
$cycleExit = $LASTEXITCODE

$summaryExit = 0
$escalationExit = 0

if ($IncludeOwnerSummary.IsPresent) {
    & $pythonExe "tools/owner_weekly_summary.py"
    $summaryExit = $LASTEXITCODE

    if ($Cycle -eq "weekly") {
        & $pythonExe "tools/escalation_queue_manager.py" "list" "--status" "open"
        $escalationExit = $LASTEXITCODE
        $timestampEsc = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        "[$timestampEsc] GOVERNANCE cycle=$Cycle escalation_open_report_exit=$escalationExit" | Out-File -FilePath $logPath -Encoding utf8 -Append
    }
}

$finalExit = if ($cycleExit -ne 0) {
    $cycleExit
} elseif ($summaryExit -ne 0) {
    $summaryExit
} else {
    $escalationExit
}
$timestampEnd = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"[$timestampEnd] END cycle=$Cycle exit=$finalExit" | Out-File -FilePath $logPath -Encoding utf8 -Append

exit $finalExit
