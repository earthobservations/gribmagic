<div align="center">

# GribMagic - generic weather forecast downloader

![CI](https://github.com/earthobservations/gribmagic/workflows/Tests/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/earthobservations/gribmagic/branch/main/graph/badge.svg)](https://codecov.io/gh/earthobservations/gribmagic)
![python](https://img.shields.io/pypi/pyversions/gribmagic.svg)
![version](https://img.shields.io/pypi/v/gribmagic.svg)
![license](https://img.shields.io/pypi/l/gribmagic.svg)
![status](https://img.shields.io/pypi/status/gribmagic.svg)
![downloads](https://img.shields.io/pypi/dm/gribmagic.svg)


![image](https://user-images.githubusercontent.com/453543/102729922-fb641c80-4332-11eb-835d-b022fc5290d9.png)

<div align="right" style="width: 350px">

_Simulations are believed by no one except those 
who conducted them._

_Experimental results are believed by everyone except
those who conducted them._

ANONYMOUS

</div>

</div>

## About
The goal of the GribMagic project is to unify the download process of
public GRIB1/GRIB2 and netCDF data from numerical weather prediction 
models originating from different organizations and data providers.

This is a work in progress, as such GribMagic is currently considered to
be beta software. As this is an early-stage project, contributions are
highly appreciated.


## Setup

Install the [ecCodes package by ECMWF](https://confluence.ecmwf.int/display/ECC).
```
# Debian Linux
apt-get install libeccodes0

# macOS/Homebrew
brew install eccodes
```

Install GribMagic Python package.
```
pip install gribmagic --upgrade
```


## Run GribMagic Unity program

### Ad hoc usage
```
# List labels of available models.
gribmagic unity list

# Acquire data.
gribmagic unity acquire --model=dwd-icon-eu --timestamp=2021-10-03T00:00:00Z --target=.gribmagic-data
```

### Configuration
To optionally adjust configuration settings, you can define the following environment variables:
```
GM_DATA_PATH={PATH_TO_PROJECT}/data

GM_MODEL_CONFIG={PATH_TO_PROJECT}/config/model_config.yml"
GM_MODEL_VARIABLES_MAPPING={PATH_TO_PROJECT}/config/model_variables_mapping.yml"
GM_MODEL_VARIABLES_LEVELS_MAPPING={PATH_TO_PROJECT}/config/model_variables_levels_mapping.yml"

ECCODES_DEFINITION_PATH=/usr/share/eccodes/definitions:/usr/local/opt/eccodes/share/eccodes/definitions
```


## Run DWD GRIB Downloader program
```
# Install DWD GRIB Downloader program.
gribmagic install dwd-grib-downloader

# Acquire wind-specific parameters from ICON-D2.
wget https://raw.githubusercontent.com/earthobservations/gribmagic/98da3fd4f/examples/dwd/recipe_d2_wind.py
gribmagic dwd acquire --recipe=recipe_d2_wind.py --timestamp="2021101800" --output=.gribmagic-data

# Acquire assorted parameters from ICON-GLOBAL.
wget https://raw.githubusercontent.com/earthobservations/gribmagic/98da3fd4f/examples/dwd/recipe_global_assorted.py
gribmagic dwd acquire --recipe=recipe_global_assorted.py --timestamp="2021101800" --output=.gribmagic-data
```


## Run program in Docker

To use GribMagic in a Docker container, you have to build the Docker image like
```
docker build --tag gribmagic .
```

and then invoke it like
```
docker run -it --volume=$PWD/.gribmagic-data:/var/spool/gribmagic gribmagic:latest gribmagic unity acquire --model=dwd-icon-eu --timestamp=2021-10-03T00:00:00Z
```

## Development

### Acquire source code
```
git clone https://github.com/earthobservations/gribmagic
cd gribmagic
```

### Run software tests
```
# Run all tests.
make test

# All tests, with code coverage report.
make test-coverage
```

---

#### Content attributions
The copyright of data sets, images and pictograms are held by their respective owners, unless otherwise noted. 

##### Banner image
- 2 metre temperature from ECMWF, rendered using Magics.
  - Source: MARS labelling or ensemble forecast data (2013-03-25)
  - URL:    http://download.ecmwf.int/test-data/magics/2m_temperature.grib
