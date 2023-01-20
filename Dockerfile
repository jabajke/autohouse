FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR usr/src/app

COPY requirements.txt .

RUN apt-get update && apt-get install gcc libpq-dev python3-dev -y
RUN pip install -r requirements.txt

COPY . .




