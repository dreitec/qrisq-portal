#!/bin/bash

docker-compose up -d
docker-compose exec api python manage.py seedsubscriptions
docker-compose exec api python manage.py createsuperuser
docker-compose stop