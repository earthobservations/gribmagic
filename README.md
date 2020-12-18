# GribMagic - generic weather forecast downloader 

The target of the GribMagic project is to unify the download process of grib1/grib2 and netcdf data from numerical weather prediction models. Step by step all public available weather models will be implemented. The data unifying process will be optional. 

This is a Work in Progress. We are happy if you are willing to contribute.

![CI](https://github.com/earthobservations/GribMagic/workflows/CI/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/earthobservations/GribMagic/branch/main/graph/badge.svg)](https://codecov.io/gh/earthobservations/GribMagic)
![python](https://img.shields.io/badge/Python-3.7,%203.8-green.svg)

# Development

## Setup

Install [ecCodes package by ECMWF](https://confluence.ecmwf.int/display/ECC).
```
brew install eccodes
```

Install Python packages.
```
virtualenv .venv --python=python3.8
source .venv/bin/activate
pip install --requirement requirements.txt
```

## Run tests

### Acquire test data
```
wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2 --directory-prefix tests/modules/download/fixtures/
```

```
export BASE_STORE_DIR=.gribmagic-data
export MODEL_CONFIG=config/model_config.yml
export MODEL_VARIABLES_MAPPING=config/model_variables_mapping.yml
export MODEL_VARIABLES_LEVELS_MAPPING=config/model_variables_levels_mapping.yml
pytest tests
```

# Configuration

### Environement Variables
To use this project you have to define the following environment variables:
```
MODEL_CONFIG={PATH_TO_PROJECT}/config/model_config.yml"
MODEL_VARIABLES_MAPPING={PATH_TO_PROJECT}/config/model_variables_mapping.yml"
MODEL_VARIABLES_LEVELS_MAPPING={PATH_TO_PROJECT}/config/model_variables_levels_mapping.yml"

BASE_STORE_DIR={PATH_TO_PROJECT}/data
ECCODES_DEFINITION_PATH={PATH_TO_PROJECT}/eccodes_defintions/defintions:/usr/share/eccodes/definitions

```
The **BASE_STORE_DIR** points to the project intern **data** directory per default. 


# Using Docker

To use the weather_forecast_downloader in a Docker container, you just have to build the image from this project

```
docker build -t "grib_magic_image" .
```

To run the tests in the given environment, just call 

```
docker run -ti -v $(pwd):/app grib_magic_image:latest pytest tests/
```
from the main directory. To work in an iPython shell you just have to change the command `pytest tests/` to `ipython`.

 
