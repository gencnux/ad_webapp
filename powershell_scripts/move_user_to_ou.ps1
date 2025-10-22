Import-Module ActiveDirectory

$user = Get-ADUser -Identity $username

if ($user -ne $null) {
    Move-ADObject -Identity $user.DistinguishedName -TargetPath "$targetOU"
    Write-Output "Kullanıcı '$username' başarıyla '$targetOU' OU'suna taşındı."
} else {
    Write-Output "Kullanıcı '$username' bulunamadı."
}
