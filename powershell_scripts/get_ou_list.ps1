Import-Module ActiveDirectory

Get-ADOrganizationalUnit -Filter * |
Select-Object -ExpandProperty DistinguishedName
