# Gunakan image dasar Python
FROM python:3.8-slim

# Setel direktori kerja
WORKDIR /app

# Salin file requirements.txt dan instal dependensi
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin kode aplikasi
COPY . .

# Ekspos port 8080
EXPOSE 8080

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
