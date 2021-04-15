FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update &&\
    apk add --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev libressl-dev jpeg-dev zlib-dev \
    geos-dev gdal-dev python3-dev postgresql-dev cargo

RUN adduser -D qrisq

ENV HOME /home/qrisq

ENV PATH "$PATH:/home/qrisq/.local/bin"

USER qrisq

WORKDIR /qrisq

RUN pip install --upgrade pip

ADD requirements.txt /qrisq/

RUN --mount=type=cache,target=/root/.cache \
    pip install -r /qrisq/requirements.txt

COPY ./ /qrisq