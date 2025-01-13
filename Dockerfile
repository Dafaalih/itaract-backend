# Gunakan image dasar Python
FROM python:3.9-slim

# Tetapkan working directory
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek ke dalam container
COPY . .

# Ekspose port 8080
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "app.py"]
