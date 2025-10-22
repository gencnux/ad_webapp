# PowerShell Web Dashboard

Bu proje, Active Directory ortamında çalışan PowerShell komutlarını web arayüzü üzerinden çalıştırmak için geliştirilmiş bir Django tabanlı yönetim panelidir. LDAP ile domain entegrasyonu sağlar, sade ve sürdürülebilir bir yapıya sahiptir.

## 🚀 Özellikler

- Django + Gunicorn + Nginx mimarisi
- LDAP ile domain kullanıcı doğrulama
- PowerShell komutlarını web üzerinden çalıştırma
- Bootstrap destekli sade arayüz
- Dockerize edilmiş yapı
- CI/CD pipeline ile otomatik build ve deploy

## 🛠️ Kurulum

### 1. Docker ile çalıştırmak için:

bash
git clone https://github.com/caglar/powershell_web.git
cd powershell_web
docker compose up -d

### 2. Manuel çalıştırmak için
python -m venv venv310
source venv310/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
=======
```bash
git clone https://github.com/caglar/powershell_web.git
cd powershell_web
docker compose up -d
Test: CI/CD pipeline tetikleniyor...
