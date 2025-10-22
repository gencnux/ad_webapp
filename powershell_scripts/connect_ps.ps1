

Write-Output "🔧 WinRM bağlantı konfigürasyonu başlatılıyor..."

# 1. WinRM servisini başlat
Start-Service WinRM -ErrorAction SilentlyContinue

# 2. TrustedHosts listesine IP ekle
Set-Item -Path WSMan:\localhost\Client\TrustedHosts -Value $targetHost -Force

# 3. Bağlantı testi
$ping = Test-Connection -ComputerName $targetHost -Count 2 -Quiet
$wsman = Test-WSMan -ComputerName $targetHost -ErrorAction SilentlyContinue

if ($ping -and $wsman) {
    Write-Output "✅ Bağlantı başarılı: $targetHost"
    Write-Output "💡 Komutu masaüstünüzde çalıştırabilirsiniz:"
    Write-Output "Enter-PSSession -ComputerName $targetHost -Credential (Get-Credential)"
} else {
    Write-Output "❌ Bağlantı sağlanamadı. WinRM veya ağ yapılandırması eksik olabilir."
}
