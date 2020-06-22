FROM python:3.7.7-slim
MAINTAINER Daniel Lassahn <daniel.lassahn@meteointelligence.de>

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

RUN set -ex \
    && apt update \
    && apt install -y apt-transport-https curl

COPY ./requirements.txt /opt/requirements.txt

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

    && pip install -r /opt/requirements.txt \
    && apt-get remove -y $buildDeps \
    && apt-get autoremove -y


ENV PYTHONPATH "/app:/app"
ENV BASE_STORE_DIR "/app/data/"

ENV MODEL_CONFIG "/app/config/model_config.yml"
ENV MODEL_VARIABLES_MAPPING "/app/config/model_variables_mapping.yml"
ENV MODEL_VARIABLES_LEVELS_MAPPING "/app/config/model_variables_levels_mapping.yml"

WORKDIR /app
