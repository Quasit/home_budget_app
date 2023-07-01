# syntax=docker/dockerfile:1


FROM python:3.9-slim

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY . .
EXPOSE 5000
RUN chmod +x /usr/src/app/start.sh
CMD [ "/usr/src/app/start.sh" ]