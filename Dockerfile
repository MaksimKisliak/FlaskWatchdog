# Use the official Python base image (updated to 3.11)
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (required for some Python packages)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better Docker layer caching
COPY requirements-prod.txt .

# Install the Python dependencies (production only)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-prod.txt

# Copy the .env.development file into the container
COPY .env.development /app/.env

# Copy the rest of the application files into the container
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port that the app will run on
EXPOSE 5000

# Define environment variable
ENV NAME World
ENV PYTHONUNBUFFERED=1

LABEL maintainer="Maksim Kisliak <makskislyak@gmail.com>"
LABEL version="2.0"
LABEL description="FlaskWatchdog - Phase 2 Backend Updates"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=2)" || exit 1

# Start the Gunicorn server
CMD ["gunicorn", "--config", "gunicorn.py", "run:app"]
