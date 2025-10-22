$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\GracePeriod"

try {
    Remove-ItemProperty -Path $regPath -Name "GracePeriod" -ErrorAction Stop
    Write-Output "GracePeriod registry değeri başarıyla silindi."
} catch {
    Write-Output "Silme hatası: $_"
}
