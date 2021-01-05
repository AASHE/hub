#!/bin/sh

set -e

# Migrate thumbnails
python manage.py makemigrations thumbnail
python manage.py migrate thumbnail

# Migrate Django after each build
python manage.py migrate

# Collect website static assets
python manage.py collectstatic --noinput

# Start Django
gunicorn --bind :$PORT -w 2 --timeout 30 hub.wsgi:application