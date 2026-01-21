FROM python:3.10-slim

# Prevent Python .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
# - gcc, libpq-dev → psycopg2
# - postgresql-client → pg_isready (CRITICAL)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code (includes start.sh)
COPY . .

# Ensure startup script is executable
RUN chmod +x /app/start.sh

# Run startup script via POSIX shell
CMD ["/bin/sh", "/app/start.sh"]
