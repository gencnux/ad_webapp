$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\GracePeriod"

try {
    $value = Get-ItemProperty -Path $regPath -Name "GracePeriod"
    if ($value.GracePeriod -eq $null) {
        Write-Output "GracePeriod değeri bulunamadı. Registry owner alınmalı ve değer oluşturulmalı."
        return
    }
    $seconds = [BitConverter]::ToInt32($value.GracePeriod, 0)
    $days = [math]::Round($seconds / 86400)
    Write-Output "Kalan RDS Grace süresi: $days gün"
} catch {
    Write-Output "GracePeriod anahtarı okunamadı: $_"
}
