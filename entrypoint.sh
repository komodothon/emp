#!/bin/bash

# Print starting point
echo "📦 Starting database setup..."

# Only delete and recreate the DB in development
if [ "$FLASK_ENV" = "development" ]; then
  echo "🧹 Cleaning up old development database..."
  rm -f instance/*.db
fi

# Run database migrations
echo "📦 Running database migrations..."
flask db upgrade
echo "[✅] Tables created successfully."

# Seed database only in development
if [ "$FLASK_ENV" = "development" ]; then
  echo "🌱 Seeding development database..."
  export PYTHONPATH=/code
  python seed/setup_admin_db.py
  python seed/setup_db.py
  echo "[✅] Seeding complete."
fi

# Print that the server is starting
echo "🚀 Starting Gunicorn server..."

# Start the Gunicorn server with specified options
exec gunicorn run:app --bind 0.0.0.0:8000 --workers 4 --timeout 60
