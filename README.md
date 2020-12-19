# GribMagic - generic weather forecast downloader 

The goal of the GribMagic project is to unify the download process of
public grib1/grib2 and netcdf data of numerical weather prediction models
from different organizations and data providers.

The data unifying process is optional.

This is a Work in Progress. We are happy if you are willing to contribute.

![CI](https://github.com/earthobservations/gribmagic/workflows/Tests/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/earthobservations/gribmagic/branch/main/graph/badge.svg)](https://codecov.io/gh/earthobservations/gribmagic)
![python](https://img.shields.io/badge/Python-3.7,%203.8-green.svg)

# Development

## Setup

Install the [ecCodes package by ECMWF](https://confluence.ecmwf.int/display/ECC).
```
brew install eccodes
```

Install Python packages.
```
virtualenv .venv --python=python3.8
source .venv/bin/activate
pip install --requirement requirements.txt --requirement requirements-dev.txt
```

## Run tests
```
make test
```

# Configuration

### Environment variables
To use this project you have to define the following environment variables:
```
BASE_STORE_DIR={PATH_TO_PROJECT}/data

MODEL_CONFIG={PATH_TO_PROJECT}/config/model_config.yml"
MODEL_VARIABLES_MAPPING={PATH_TO_PROJECT}/config/model_variables_mapping.yml"
MODEL_VARIABLES_LEVELS_MAPPING={PATH_TO_PROJECT}/config/model_variables_levels_mapping.yml"

ECCODES_DEFINITION_PATH=/usr/share/eccodes/definitions:/usr/local/opt/eccodes/share/eccodes/definitions
```
The **BASE_STORE_DIR** points to the project intern **data** directory per default. 


# Using Docker

To use gribmagic in a Docker container, you have to build the Docker image like
```
docker build -t "gribmagic" .
```

To run the tests in the given environment, just call
```
docker run -ti -v $(pwd):/app gribmagic:latest pytest tests/
```
from the main directory. To work in an iPython shell, you have to change the command `pytest tests/` to `ipython`.
