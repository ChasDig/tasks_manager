#!/bin/sh
set -e

echo "🔄 Run migrations..."
alembic upgrade head

echo "🚀 Run app..."
exec uvicorn run:app --host 0.0.0.0 --port "$TASK_MANAGER_SERVICE_PORT" --workers $TASK_MANAGER_SERVICE_WORKERS
