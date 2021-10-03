FROM python:3.8.6-slim
MAINTAINER Daniel Lassahn <daniel.lassahn@meteointelligence.de>

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

RUN set -ex \
    && apt update \
    && apt install -y apt-transport-https curl

COPY ./requirements.txt /opt/requirements.txt
COPY ./requirements-dev.txt /opt/requirements-dev.txt

WORKDIR /tmp
RUN set -ex \
    && buildDeps=' \
        libnetcdf-dev \
        libhdf5-dev \
        build-essential \
        libbz2-dev \
    ' \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        cdo \
        curl \
        libeccodes0 \
        wget \
        bzip2 \
    \
    && pip install --requirement=/opt/requirements.txt --requirement=/opt/requirements-dev.txt \
    && apt-get remove -y $buildDeps \
    && apt-get autoremove -y

ENV PYTHONPATH "/app:/app"
ENV GM_DATA_PATH "/app/data/"

ENV ECCODES_DEFINITION_PATH=/app/eccodes/definitions:/usr/share/eccodes/definitions

WORKDIR /app
