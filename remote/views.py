import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .commands import COMMANDS
from .models import CommandLog
import winrm

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def view_logs(request):
    logs = CommandLog.objects.order_by("-timestamp")[:50]
    return render(request, "remote/logs.html", {"logs": logs})

@login_required
def my_logs(request):
    user = request.user
    query = request.GET.get("q", "").strip()
    logs = CommandLog.objects.filter(user=user).order_by("-timestamp")
    if query:
        logs = logs.filter(command_id__icontains=query)
    return render(request, "remote/my_logs.html", {"logs": logs, "query": query})

def parse_table_output(raw_text):
    lines = raw_text.strip().splitlines()
    if len(lines) < 2:
        return None
    headers = lines[0].split()
    data_lines = lines[1:]
    rows = []
    for line in data_lines:
        parts = line.split(None, len(headers) - 1)
        if len(parts) == len(headers):
            rows.append(dict(zip(headers, parts)))
    return headers, rows

def fetch_ou_list():
    try:
        session = winrm.Session(
            'http://172.24.115.255:5985/wsman',
            auth=('svc_powershell', 'Pssw0rd'),
            transport='ntlm'
        )
        result = session.run_ps("""
Import-Module ActiveDirectory
Get-ADOrganizationalUnit -Filter * | Select-Object -ExpandProperty DistinguishedName
""")
        raw = result.std_out.decode('utf-8', errors='ignore')
        return [line.strip() for line in raw.splitlines() if line.strip()]
    except Exception as e:
        print("OU listesi alınamadı:", e)
        return []

@login_required
def run_script(request):
    user = request.user
    user_groups = user.ldap_user.group_names if hasattr(user, "ldap_user") else []
    is_admin = "Domain Admins" in user_groups or "IT_ADMIN" in user_groups

    user_info = {
        "username": user.username,
        "groups": user_groups
    }

    favorite_ids = request.session.get("favorite_commands", [])
    visible_commands = [cmd for cmd in COMMANDS if any(g in user_groups for g in cmd["allowed_groups"])]
    favorite_commands = [cmd for cmd in visible_commands if cmd["id"] in favorite_ids]

    user_data = []
    if is_admin:
        all_users = User.objects.all().order_by("username")
        for u in all_users:
            groups = u.ldap_user.group_names if hasattr(u, "ldap_user") else []
            user_data.append({"username": u.username, "groups": groups})

    selected_command = None
    output = ""
    table_data = None
    ou_list = []
    backup_path = None

    # Favori ekleme/çıkarma
    if request.method == "POST" and "toggle_favorite" in request.POST:
        fav_id = request.POST.get("toggle_favorite")
        if fav_id in favorite_ids:
            favorite_ids.remove(fav_id)
        else:
            favorite_ids.append(fav_id)
        request.session["favorite_commands"] = favorite_ids
        return redirect("dashboard")

    # Sadece form açma isteği (komut çalıştırma değil)
    if request.method == "POST" and "command_id" in request.POST and "open_form" in request.POST:
        command_id = request.POST.get("command_id")
        selected_command = next((cmd for cmd in visible_commands if cmd["id"] == command_id), None)

    # Komut çalıştırma
    elif request.method == "POST" and "command_id" in request.POST:
        command_id = request.POST.get("command_id")
        selected_command = next((cmd for cmd in visible_commands if cmd["id"] == command_id), None)

        if selected_command:
            params = {p["name"]: request.POST.get(p["name"], "") for p in selected_command["parameters"]}

            # ✅ Eksik parametre kontrolü
            missing_params = [p["name"] for p in selected_command["parameters"] if not request.POST.get(p["name"])]
            if missing_params:
                output = f"⚠️ Eksik parametre: {', '.join(missing_params)}. Komut çalıştırılmadı."
            else:
                if selected_command["id"] == "move_user_to_ou":
                    ou_list = fetch_ou_list()

                target_host = params.get("target") or "172.24.115.255"
                test_mode = request.POST.get("test_mode") == "on"

                if test_mode and not selected_command.get("test_safe", False):
                    output = "⚠️ Bu komut test modunda çalıştırılamaz. Gerçek etki yaratabilir."
                else:
                    ps_script = ""
                    if "script_file" in selected_command:
                        script_path = os.path.join(settings.BASE_DIR, "powershell_scripts", selected_command["script_file"])
                        try:
                            with open(script_path, "r") as f:
                                ps_template = f.read()
                        except Exception as e:
                            ps_template = 'Write-Output "Script dosyası okunamadı."'
                        ps_script = ps_template
                        for key, value in params.items():
                            ps_script = ps_script.replace(f"${key}", value)
                    elif "script" in selected_command:
                        ps_script = selected_command["script"]
                        for key, value in params.items():
                            ps_script = ps_script.replace(f"{{key}}", value)

                    try:
                        session = winrm.Session(
                            f"http://{target_host}:5985/wsman",
                            auth=('svc_powershell', 'Pssw0rd'),
                            transport='ntlm'
                        )
                        result = session.run_ps(ps_script)
                        raw_output = result.std_out.decode('utf-8', errors='ignore') + result.std_err.decode('utf-8', errors='ignore')
                        clean_output = raw_output.split("#< CLIXML")[0].strip()
                        output = "[TEST MODU]\n" + clean_output if test_mode else clean_output
                        table_data = parse_table_output(output)

                        if "BACKUP_PATH:" in output:
                            for line in output.splitlines():
                                if line.startswith("BACKUP_PATH:"):
                                    backup_path = line.replace("BACKUP_PATH:", "").strip()

                    except Exception as e:
                        output = f"Komut çalıştırma hatası: {str(e)}"

                    try:
                        CommandLog.objects.create(
                            user=user,
                            command_id=selected_command["id"],
                            parameters=str(params),
                            output=output
                        )
                    except Exception as e:
                        print("Loglama hatası:", e)

    return render(request, "remote/run_script.html", {
        "commands": visible_commands,
        "selected_command": selected_command,
        "output": output,
        "table_data": table_data,
        "ou_list": ou_list,
        "backup_path": backup_path,
        "is_admin": is_admin,
        "user_info": user_info,
        "favorite_commands": favorite_commands,
        "favorite_ids": favorite_ids,
        "user_logs": CommandLog.objects.filter(user=user).order_by("-timestamp")[:10],
        "user_data": user_data
    })


@login_required
def manage_users(request):
    user = request.user
    user_groups = user.ldap_user.group_names if hasattr(user, "ldap_user") else []
    is_admin = "Domain Admins" in user_groups or "IT_ADMIN" in user_groups

    if not is_admin:
        return render(request, "remote/access_denied.html")
    
    message = None  # Hata verdiği için eklendi.

    if request.method == "POST":
        target_username = request.POST.get("target_user")
        new_groups = request.POST.get("new_groups", "").split(",")
        new_groups = [g.strip() for g in new_groups if g.strip()]

        try:
            # 🔧 Gerçek LDAP güncellemesi
            session = winrm.Session(
                'http://172.24.115.255:5985/wsman',
                auth=('svc_powershell', 'Pssw0rd'),
                transport='ntlm'
            )

            # Önce tüm gruplardan çıkar
            cleanup_script = f"""
Import-Module ActiveDirectory
$groups = Get-ADUser "{target_username}" -Properties MemberOf | Select-Object -ExpandProperty MemberOf
foreach ($g in $groups) {{
    Remove-ADGroupMember -Identity $g -Members "{target_username}" -Confirm:$false
}}
"""
            session.run_ps(cleanup_script)

            # Sonra yeni gruplara ekle
            for group in new_groups:
                add_script = f"""
Import-Module ActiveDirectory
Add-ADGroupMember -Identity "{group}" -Members "{target_username}"
"""
                session.run_ps(add_script)

            message = f"{target_username} kullanıcısı şu gruplara eklendi: {', '.join(new_groups)}"

        except Exception as e:
            message = f"LDAP güncelleme hatası: {str(e)}"

    all_users = User.objects.all().order_by("username")
    user_data = []
    for u in all_users:
        groups = u.ldap_user.group_names if hasattr(u, "ldap_user") else []
        user_data.append({
            "username": u.username,
            "groups": groups
        })

    return render(request, "remote/manage_users.html", {
        "user_data": user_data,
        "message": message
    })