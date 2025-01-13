# Gunakan Python slim sebagai base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin file aplikasi ke container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Eksekusi aplikasi
CMD ["python", "app.py"]
