#!/bin/sh

set -e

# Collect website static assets
python manage.py collectstatic --noinput

#Start Celery Workers
celery -A hub worker --config hub/celery.py --loglevel=DEBUG &

#Start Celery Beat
celery beat --config hub/celery.py -A hub -s /var/www/hub/logs/beat.db --loglevel=DEBUG