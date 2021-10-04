FROM python:3.9-slim
MAINTAINER Daniel Lassahn <daniel.lassahn@meteointelligence.de>

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

RUN set -ex \
    && apt update \
    && apt install -y apt-transport-https curl

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
    && apt-get remove -y $buildDeps \
    && apt-get autoremove -y

# Copy working dir, modulo .dockerignore'ed files.
COPY . /tmp
RUN pip install /tmp

# Purge /tmp directory.
RUN rm -r /tmp/*

RUN mkdir /var/spool/gribmagic
ENV GM_DATA_PATH "/var/spool/gribmagic"
ENV ECCODES_DEFINITION_PATH=/app/eccodes/definitions:/usr/share/eccodes/definitions
