$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument '/c "D:\opencode stuff\job-agents\start_autopilot.bat"'
$triggerDaily = New-ScheduledTaskTrigger -Daily -At 9:00AM
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -RunOnlyIfNetworkAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "JobHuntingDailyFleet" -Action $action -Trigger @($triggerDaily, $triggerLogon) -Settings $settings -Description "Automated daily job applications fleet for Vansh Sharma" -Force
