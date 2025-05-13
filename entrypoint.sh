#!/bin/bash

echo "📦 Starting database setup..."

# Run database migrations (safe for dev and prod)
echo "📦 Running database migrations..."
flask db upgrade
echo "[✅] Migrations applied successfully."

# In development, create and seed dev.db only if it doesn't exist
if [ "$FLASK_ENV" = "development" ]; then
  if [ ! -f instance/dev.db ]; then
    echo "📦 No dev.db found. Creating and seeding now..."
    export PYTHONPATH=/code
    python seed/setup_admin_db.py
    python seed/setup_db.py
    echo "[✅] Seeding complete."
  else
    echo "✅ dev.db already exists. Skipping seeding."
  fi
fi

echo "🚀 Starting Gunicorn server..."
exec gunicorn run:app --bind 0.0.0.0:8000 --workers 4 --timeout 60
