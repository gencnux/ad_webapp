COMMANDS = [
   {
    "id": "disable_user",
    "name": "Kullanıcıyı Devre Dışı Bırak",
    "description": "Belirtilen kullanıcıyı Active Directory'de devre dışı bırakır.",
    "parameters": [
        {"name": "username", "label": "Kullanıcı Adı", "type": "text"}
    ],
    "script_file": "disable_user.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"],
    "category": "Kullanıcı Yönetimi",
    "icon": "fa-user-slash",
    "help_url": "https://docs.microsoft.com/en-us/powershell/module/activedirectory/disable-adaccount",
    "test_safe": False,
},
    {
        "id": "restart_service",
        "name": "Servisi Yeniden Başlat",
        "description": "Sunucudaki servisi yeniden başlatır.",
        "parameters": [
            {"name": "hostname", "label": "Sunucu Adı/IP", "type": "text"},
            {"name": "servicename", "label": "Servis Adı", "type": "text"}
        ],
        "script_file": "restart_service.ps1",
        "allowed_groups": ["IT_ADMIN", "Domain Admins"]
    },
    {
        "id": "admincount",
        "name": "AdminCount=1 Kullanıcıları Listele",
        "description": "Belirtilen domain'de AdminCount=1 olan kullanıcıları listeler.",
        "parameters": [
            {"name": "domain", "label": "Domain Adı", "type": "text"}
        ],
        "script_file": "admincount.ps1",
        "allowed_groups": ["Domain Admins", "IT_ADMIN", "IT_DESK"]
},
{
    "id": "enable_user",
    "name": "Kullanıcıyı Etkinleştir",
    "description": "Devre dışı olan kullanıcıyı tekrar aktif hale getirir.",
    "parameters": [
        {"name": "username", "label": "Kullanıcı Adı", "type": "text"}
    ],
    "script_file": "enable_user.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"]
    
},
{
    "id": "move_user_to_ou",
    "name": "Kullanıcıyı OU'ya Taşı",
    "description": "Belirtilen kullanıcıyı hedef OU'ya taşır.",
    "parameters": [
        {"name": "username", "label": "Kullanıcı Adı", "type": "text"},
        {"name": "targetOU", "label": "Hedef OU (DN formatında)", "type": "text"}
    ],
    "script_file": "move_user_to_ou.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"]
},
{
    "id": "take_registry_ownership",
    "name": "RDS Registry Owner'ı Al",
    "description": "GracePeriod anahtarının owner'ını Administrators olarak değiştirir.",
    "parameters": [
        {"name": "target", "label": "Sunucu IP veya Hostname", "type": "text"}
    ],
    "script_file": "take_registry_ownership.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"]
},
{
    "id": "check_rds_license",
    "name": "RDS Lisans Süresini Kontrol Et",
    "description": "RDS sunucusunun kalan lisanssız çalışma süresini gösterir.",
    "parameters": [
        {"name": "target", "label": "Sunucu IP veya Hostname", "type": "text"}
    ],
    "script_file": "check_rds_license.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"]
},
{
    "id": "delete_grace_period",
    "name": "RDS GracePeriod Değerini Sil",
    "description": "RDS lisans süresini uzatmak için GracePeriod registry değerini siler.",
    "parameters": [
        {"name": "target", "label": "Sunucu IP veya Hostname", "type": "text"}
    ],
    "script_file": "delete_grace_period_value.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"]
},
{
    "id": "extend_rds_grace",
    "name": "RDS Grace Period Süresini Uzat",
    "description": "RDS sunucusunun lisanssız çalışma süresini gün cinsinden uzatır. Registry yedeği alınır.",
    "parameters": [
        {"name": "target", "label": "Sunucu IP veya Hostname", "type": "text"},
        {"name": "days", "label": "Kaç Gün Uzatılsın?", "type": "number"}
    ],
    "script_file": "extend_rds_grace_period.ps1",
    "allowed_groups": ["Domain Admins", "IT_ADMIN"]
},
{
    "id": "connect_rdp",
    "name": "RDP ile Bağlan",
    "description": "RDP komutunu oluşturur ve kopyalanabilir şekilde sunar.",
    "parameters": [{"name": "targetHost", "label": "Sunucu IP veya Hostname"}],
    "allowed_groups": ["Domain Admins", "IT_ADMIN"],
    "script_file": "connect_rdp.ps1",
    "category": "Bağlantı",
    "icon": "fa-desktop"
},
{
    "id": "connect_ps",
    "name": "PowerShell ile Bağlan",
    "description": "PowerShell komutunu oluşturur ve kopyalanabilir şekilde sunar.",
    "parameters": [{"name": "targetHost", "label": "Sunucu IP veya Hostname"}],
    "allowed_groups": ["Domain Admins", "IT_ADMIN"],
    "script_file": "connect_ps.ps1",
    "category": "Bağlantı",
    "icon": "fa-terminal"
},
{
        "id": "unlock_user",
        "name": "Kilitlenmiş Kullanıcıyı Aç",
        "description": "Active Directory'de kilitlenmiş bir kullanıcı hesabını açar.",
        "category": "Kullanıcı Yönetimi",
        "icon": "fa-unlock",
        "allowed_groups": ["IT_ADMIN", "Domain Admins"],
        "parameters": [
            {"name": "username", "label": "Kullanıcı Adı"}
        ],
        "script": 'Import-Module ActiveDirectory; Unlock-ADAccount -Identity "{username}"',
        "test_safe": False
    },

  {
    "id": "get_netbios_status",
    "name": "NetBIOS Durumunu Listele",
    "description": "Tüm ağ adaptörlerinde NetBIOS bileşeninin bağlı olup olmadığını listeler.",
    "category": "Ağ Yönetimi",
    "icon": "fa-list",
    "allowed_groups": ["IT_ADMIN", "Domain Admins"],
    "parameters": [
        {"name": "target", "label": "Hedef Sunucu IP veya Hostname"}
    ],
    "script": "Get-NetAdapterBinding | Select-Object Name, DisplayName, ComponentID, Enabled",
    "test_safe": True
},
{
    "id": "disable_netbios_registry",
    "name": "NetBIOS'u Registry Üzerinden Kapat",
    "description": "Uzak sunucuda tüm arabirimlerde NetBIOS'u registry üzerinden devre dışı bırakır.",
    "category": "Ağ Yönetimi",
    "icon": "fa-shield-alt",
    "allowed_groups": ["IT_ADMIN", "Domain Admins"],
    "parameters": [
        {"name": "target", "label": "Hedef Sunucu IP veya Hostname"}
    ],
    "script": """
$regPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\NetBT\\Parameters\\Interfaces"
$interfaces = Get-ChildItem -Path $regPath -ErrorAction Stop
if (-not $interfaces) { throw "Ağ arabirimi bulunamadı" }
foreach ($interface in $interfaces) {
    Set-ItemProperty -Path "$regPath\\$($interface.PSChildName)" -Name "NetbiosOptions" -Value 2 -ErrorAction Stop
}
""",
    "test_safe": False
},
{
    "id": "add_trusted_host",
    "name": "IP'yi TrustedHosts Listesine Ekle",
    "description": "WinRM bağlantısı için IP adresini TrustedHosts listesine ekler.",
    "category": "WinRM Yönetimi",
    "icon": "fa-network-wired",
    "allowed_groups": ["IT_ADMIN", "Domain Admins"],
    "parameters": [
        {"name": "ip", "label": "IP Adresi"}
    ],
    "script": "Set-Item WSMan:\\localhost\\Client\\TrustedHosts -Value \"{ip}\"",
    "test_safe": False
}



]

