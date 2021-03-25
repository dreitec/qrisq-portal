FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update &&\
    apk add --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev libressl-dev jpeg-dev zlib-dev \
    geos-dev gdal-dev python3-dev postgresql-dev cargo

WORKDIR /qrisq

RUN pip install --upgrade pip

ADD requirements.txt /qrisq/

RUN pip install -r /qrisq/requirements.txt

COPY ./ /qrisq