# Use Python 3.14 slim image to match local dev (model was pickled with 3.14)
FROM python:3.14-slim

# App lives in /app with the "backend" package preserved:
#   /app/backend/api.py, /app/backend/artifacts/...
WORKDIR /app

# Install system dependencies (gcc for builds, curl for health checks)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into /app/backend so "from backend.schemas import ..." works
COPY . ./backend/

# Expose port (Railway injects $PORT; 8000 is the local default)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run the application (serve.py reads $PORT itself — no shell expansion needed)
CMD ["python", "backend/serve.py"]
