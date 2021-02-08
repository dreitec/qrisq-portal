FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal

WORKDIR /qrisq

ADD requirements.txt /qrisq/

RUN pip install -r /qrisq/requirements.txt

COPY ./ /qrisq

ENTRYPOINT ["python", "manage.py", "migrate", "--no-input"]