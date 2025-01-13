# Gunakan image Python yang ringan
FROM python:3.9-slim

# Tentukan working directory
WORKDIR /app

# Copy file requirements.txt ke dalam image
COPY requirements.txt ./

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file dari folder backend ke dalam image
COPY . .

# Expose port 5000 (default untuk Flask)
EXPOSE 5000

# Set environment variable untuk Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Jalankan aplikasi Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

