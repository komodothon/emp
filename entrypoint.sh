#!/bin/bash

echo "📦 Seeding databases..."
rm -f instance/*.db
python setup_admin_db.py
python setup_db.py

echo "🚀 Starting Gunicorn server..."
exec gunicorn run:app --bind 0.0.0.0:8000 --workers 4 --timeout 60
