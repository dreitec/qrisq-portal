# QRisq Backend 

## Logger Setup

1. Create 'logs' folder in the project directory 
2. Create 'qrisq.log' file inside logs folder

## Setup Local Server (Linux Machine)

1. Setup virtual environment in the project directory
```sh
python -m venv venv
source venv/bin/activate
```

2. Install Dependencies
```sh
pip install -r requirements.txt
```

3. Copy .env.local as .env and Update DB CREDENTIALS

4. Migrate Database tables and Run server
```sh
python manage.py migrate
python manage.py runserver
```

5. Seed Subscription Plan
```
python manage.py seedsubscriptions
```

6. Create SuperAdmin
```
python manage.py createsuperuser
```

## Setup Local Server using Docker and Docker-compose

1. Copy .env.local as .env

2. Build docker image
```
docker-compose build
```

3. Run server
```
docker-compose up
```

or Run server in background
```
docker-compose up -d
```

4. Seed SubscriptionPlans and Create super admin (Make sure docker images are running)
```sh
docker-compose exec api python manage.py seedsubscriptions
docker-compose exec api python manage.py createsuperuser
```

5. Stop server if server run in background
```
docker-compose stop
```

6. Remove docker images along with volumes
```
docker-compose down --volume
```

