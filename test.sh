#!/bin/bash

docker-compose up -d
docker-compose exec api python manage.py test
docker-compose stop