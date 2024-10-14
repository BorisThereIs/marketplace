# syntax=docker/dockerfile:1

FROM postgres:12.20-alpine

COPY ./db.dump .

COPY ./docker/db/.env .

COPY ./docker/db/init_db.sh /docker-entrypoint-initdb.d/

