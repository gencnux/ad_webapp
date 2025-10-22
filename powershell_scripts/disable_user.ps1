Import-Module ActiveDirectory

$user = Get-ADUser -Identity $username -Properties Enabled

if ($user.Enabled -eq $false) {
    Write-Output "Kullanıcı zaten devre dışı."
} else {
    Disable-ADAccount -Identity $username
    Write-Output "Kullanıcı '$username' devre dışı bırakıldı."
}
