 = 'FirasBotBackup'
 = Join-Path  'backup.ps1'
 = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -File """
 = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName  -Action  -Trigger  -Force
