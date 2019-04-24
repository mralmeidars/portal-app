FROM python:3.7.0-alpine3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache g++ gcc libxslt-dev

RUN mkdir /portal
WORKDIR /portal
COPY requirements /portal

RUN pip install -r requirements --user --no-warn-script-location

COPY . /portal/
