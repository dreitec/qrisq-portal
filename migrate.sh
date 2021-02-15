#!/bin/bash

docker-compose up -d
docker-compose exec api python manage.py migrate
docker-compose stop