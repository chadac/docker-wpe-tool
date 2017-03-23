FROM python:3.6.0-alpine

LABEL authors="Chad Crawford, Jason Bennefield"
LABEL version="0.1"
LABEL description="Manages WPEngine installations for our website."

## VOLUME ["/app/volume"]

ADD requirements.txt /app/requirements.txt
RUN apk add --update alpine-sdk openssl-dev libffi-dev python3-dev &&\
    pip install -r /app/requirements.txt &&\
    apk del alpine-sdk

## Add the entrypoint script
ADD entrypoint.py /app/entrypoint.py
RUN chmod 777 /app/entrypoint.py

## Add library stuff
ADD scripts /app/scripts
ADD lib /app/lib

## Add the Wordpress template files
ADD wp-template /app/wp-template

## Set the working directory to our app directory
WORKDIR /app
