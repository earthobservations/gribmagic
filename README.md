<div align="center">

# GribMagic - generic weather forecast downloader

![CI](https://github.com/earthobservations/gribmagic/workflows/Tests/badge.svg?branch=main)
![codecov](https://codecov.io/gh/earthobservations/gribmagic/branch/main/graph/badge.svg)](https://codecov.io/gh/earthobservations/gribmagic)
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


## Development

### Setup

Install the [ecCodes package by ECMWF](https://confluence.ecmwf.int/display/ECC).
```
# Debian Linux
apt-get install libeccodes0

# macOS/Homebrew
brew install eccodes
```

Install Python packages.
```
git clone https://github.com/earthobservations/gribmagic
cd gribmagic
python3 -m venv .venv
source .venv/bin/activate
pip install --editable=.[test]
```

### Run tests
```
make test
```


## Run program

### Ad hoc usage
```
export GM_DATA_PATH=.gribmagic-data
gribmagic unity --model=icon_eu --timestamp=2021-10-03T00:00:00Z
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
The **GM_DATA_PATH** points to the project intern **data** directory per default. 


## Run program in Docker

To use gribmagic in a Docker container, you have to build the Docker image like
```
docker build --tag gribmagic .
```

and then invoke it like
```
docker run -it --volume=$PWD/.gribmagic-data:/var/spool/gribmagic gribmagic:latest gribmagic unity --model=icon_eu --timestamp=2021-10-03T00:00:00Z
```

---

#### Content attributions
The copyright of data sets, images and pictograms are held by their respective owners, unless otherwise noted. 

##### Banner image
- 2 metre temperature from ECMWF, rendered using Magics.
  - Source: MARS labelling or ensemble forecast data (2013-03-25)
  - URL:    http://download.ecmwf.int/test-data/magics/2m_temperature.grib
