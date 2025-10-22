Import-Module ActiveDirectory

$user = Get-ADUser -Identity $username -Properties Enabled

if ($user.Enabled -eq $true) {
    Write-Output "Kullanıcı zaten aktif."
} else {
    Enable-ADAccount -Identity $username
    Write-Output "Kullanıcı '$username' tekrar etkinleştirildi."
}