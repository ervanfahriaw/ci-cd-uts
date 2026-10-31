# Multi-stage/Minimalist Python runtime
FROM python:3.11-alpine

# Set direktori kerja
WORKDIR /app

# Atur environment variable agar log langsung keluar ke stdout
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    DATA_DIR=/var/lib/backend_data \
    DATA_FILE=/var/lib/backend_data/guestbook.json

# Salin source code aplikasi
COPY app.py /app/app.py

# Siapkan direktori penyimpanan volume
RUN mkdir -p /var/lib/backend_data

# Ekspos port backend API
EXPOSE 8000

# Jalankan server REST API
CMD ["python", "app.py"]
