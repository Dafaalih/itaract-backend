# Stage 1: Build
FROM python:3.9-slim AS build-stage

# Set working directory
WORKDIR /app

# Copy the requirements file first (to leverage Docker cache)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Stage 2: Serve
FROM python:3.9-slim AS serve-stage

# Set working directory
WORKDIR /app

# Copy application files from build-stage
COPY --from=build-stage /app/ ./

# Set environment variable for production
ENV FLASK_ENV=production
ENV PORT=8080

# Expose the port Cloud Run expects (8080)
EXPOSE 8080

# Command to run the Flask app (or other Python app)
CMD ["python", "app.py"]
