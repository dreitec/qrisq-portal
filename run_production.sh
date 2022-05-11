#!/bin/sh

python manage.py wait_for_db && \
    python manage.py migrate --no-input && \
    python manage.py migrate storm --database=storm --no-input && \
    python manage.py collectstatic --no-input && \
    gunicorn --workers=4 qrisq_api.wsgi:application --bind 0.0.0.0:8000 --timeout 120