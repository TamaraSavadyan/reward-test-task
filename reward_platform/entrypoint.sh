#!/bin/bash

# Exit on error
set -e

# Create static directory if it doesn't exist
mkdir -p /app/staticfiles
chmod -R 755 /app/staticfiles

# Collect static files
python manage.py collectstatic --noinput --clear

# Run database migrations
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn reward_platform.wsgi:application --bind 0.0.0.0:8000 