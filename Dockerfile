FROM python:slim

ENV PYTHONBUFFERED=1

WORKDIR usr/src/app

COPY . .
RUN apt-get update && apt-get install gcc libpq-dev python3-dev -y

RUN pip install -r requirements.txt



