#!/bin/bash

docker-compose up -d
docker-compose exec api python manage.py makemigrations
docker-compose stop