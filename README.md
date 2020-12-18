# GribMagic - generic weather forecast downloader 

The target of the GribMagic project is to unify the download process of grib1/grib2 and netcdf data from numerical weather prediction models. Step by step all public available weather models will be implemented. The data unifying process will be optional. 

This is a Work in Progress. We are happy if you are willing to contribute.

![CI](https://github.com/earthobservations/GribMagic/workflows/CI/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/earthobservations/GribMagic/branch/main/graph/badge.svg)](https://codecov.io/gh/earthobservations/GribMagic)
![python](https://img.shields.io/badge/Python-3.7-green.svg)

# Setting up and installation

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

### Required Installations
t.b.c


### Using Docker

To use the weather_forecast_downloader in a Docker container, you just have to build the image from this project

```
docker build -t "grib_magic_image" .
```

To run the tests in the given environment, just call 

```
docker run -ti -v $(pwd):/app grib_magic_image:latest pytest tests/
```
from the main directory. To work in an iPython shell you just have to change the command `pytest tests/` to `ipython`.

 
