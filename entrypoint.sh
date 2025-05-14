#!/bin/bash

echo "📦 Starting database setup..."

# Only delete and recreate the DB in development
if [ "$FLASK_ENV" = "development" ]; then
  echo "Cleaning up old development database..."
  rm -f instanc/*.db
fi

# Initialise migrations folder if missing
if [ ! -d "migrations" ]; then
  echo " 'migrations/' folder not found. Running flask db init..."
  flask db init
fi

# Run database migrations (safe for dev and prod)
echo "📦 Running database migrations..."
flask db upgrade
echo "[✅] Migrations applied successfully."

# In development, create and seed dev.db only if it doesn't exist
if [ "$FLASK_ENV" = "development" ]; then
  echo "Seeding development database..."
  export PYTHONPATH=/code
  python seed/setup_admin_db.py
  python seed/setup_db.py
  python seed/mod_contr_end_date.py
  python seed/seed_salary_structure.py
  echo "[✅] Seeding complete."
fi

# Print that the server is starting
echo "🚀 Starting Gunicorn server..."
exec gunicorn run:app --bind 0.0.0.0:8000 --workers 4 --timeout 60
