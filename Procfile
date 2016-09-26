web: newrelic-admin run-program gunicorn hub.wsgi --log-file -
worker: celery worker --app=hub -l info
