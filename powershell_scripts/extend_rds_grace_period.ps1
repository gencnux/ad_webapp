$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\GracePeriod"
$backupPath = "C:\RDS_Grace_Backup.reg"

try {
    reg export "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\GracePeriod" $backupPath /y
    Write-Output "BACKUP_PATH:$backupPath"
    $hexDays = [System.BitConverter]::GetBytes($days * 86400)
    Set-ItemProperty -Path $regPath -Name "GracePeriod" -Value $hexDays
    Write-Output "RDS Grace Period süresi $days gün olarak ayarlandı."
} catch {
    Write-Output "İşlem hatası: $_"
}
