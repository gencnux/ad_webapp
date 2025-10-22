Invoke-Command -ComputerName "172.24.115.121" -ScriptBlock {
    param([string]$svc)
    Restart-Service -Name $svc -Force
} -ArgumentList "Spooler"