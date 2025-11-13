# Use a stable lightweight Python base image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Copy pre-trained model (if stored separately)
# COPY models/ models/

# Expose Flask/Gunicorn port
EXPOSE 8080

# Use Gunicorn to serve Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "application:app"]
