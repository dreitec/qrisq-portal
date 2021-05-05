#!/bin/sh

python manage.py wait_for_db && python manage.py migrate && gunicorn qrisq_api.wsgi:application --bind 0.0.0.0:8000