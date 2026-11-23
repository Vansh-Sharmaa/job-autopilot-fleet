$task = Get-ScheduledTask -TaskName 'JobHuntingDailyFleet'
$task.Settings.StartWhenAvailable = $true
$task.Settings.AllowStartIfOnBatteries = $true
$task.Settings.DontStopIfGoingOnBatteries = $true
$task.Settings.RunOnlyIfNetworkAvailable = $true
Set-ScheduledTask -InputObject $task
Get-ScheduledTask -TaskName 'JobHuntingDailyFleet' | Select-Object -ExpandProperty Settings | Format-List WakeToRun, StartWhenAvailable, AllowStartIfOnBatteries, DontStopIfGoingOnBatteries, RunOnlyIfNetworkAvailable
