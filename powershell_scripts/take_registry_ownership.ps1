$regPath = "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\GracePeriod"

try {
    $acl = Get-Acl -Path $regPath
    $admin = New-Object System.Security.Principal.NTAccount("Administrators")
    $acl.SetOwner($admin)
    Set-Acl -Path $regPath -AclObject $acl
    Write-Output "Registry owner 'Administrators' olarak değiştirildi."
} catch {
    Write-Output "Owner değiştirme hatası: $_"
}
