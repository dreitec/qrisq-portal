FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update &&\
    apk add --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev libressl-dev jpeg-dev zlib-dev \
    geos-dev gdal-dev python3-dev postgresql-dev cargo

RUN pip install --upgrade pip

WORKDIR /qrisq

ADD requirements.txt /qrisq/

RUN pip install -r /qrisq/requirements.txt

COPY ./ /qrisq

RUN pip install gunicorn

EXPOSE 8000

ENTRYPOINT ["sh", "/qrisq/run_production.sh"]