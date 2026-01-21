#!/bin/sh
set -e

echo "â³ Waiting for PostgreSQL..."
sleep 5

echo "ðŸ“¦ Running Alembic migrations..."
alembic upgrade head

echo "ðŸš€ Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000