Import-Module ActiveDirectory

Get-ADUser -Filter {AdminCount -eq 1} -Server $domain |
Select-Object SamAccountName, DistinguishedName |
Out-String