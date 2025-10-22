# Temel Python imajı
FROM python:3.10-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Gereksinim dosyasını kopyala ve kur
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Proje dosyalarını kopyala
COPY . /app/

# Static dosyaları topla
RUN python manage.py collectstatic --noinput

# Gunicorn ile başlat
CMD ["gunicorn", "powershell_web.wsgi:application", "--bind", "0.0.0.0:8000"]

