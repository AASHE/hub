#!/bin/sh

set -e

# Migrate Django after each build
python manage.py migrate --fake-initial

# Collect website static assets
python manage.py collectstatic --noinput

# Start Django
gunicorn --bind :$PORT -w 2 --timeout 30 hub.wsgi:application