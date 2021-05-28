# QRisq Backend

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

## Setup Local Server using Docker and Docker-compose

1. Copy .env.local as .env

2. Build docker image
```sh
docker-compose build
```

3. Run server
```sh
docker-compose up
```

or Run server in background
```sh
docker-compose up -d
```

4. Stop server if server run in background
```sh
docker-compose stop
```

5. Remove docker images along with volumes
```sh
docker-compose down --volume
```
