#/bin/sh
# Acquire a subset of NWP data from DWD and extract an area of interest defined
# by a bounding box or country code.
#
# Installation notes:
# - Data acquisition from DWD needs the DWD GRIB Downloader.
#   To install it, invoke `gribmagic install dwd-grib-downloader`.
# - Plotting needs a `Magics` installation. To install it, invoke
#   `make magics-install`.

set -e

PATH_RAW=.gribmagic-data/raw
PATH_SUBGRID=.gribmagic-data/subgrid

mkdir -p ${PATH_RAW}

# Acquire subset of data/
# Here: Wind - as defined per recipe.
function acquire() {
    echo "Downloading files"
    gribmagic dwd acquire \
      --recipe="examples/dwd/recipe_d2_wind.py" \
      --output="${PATH_RAW}"
}

# Extract area of interest.
# Here: Austria: West + Oststeiermark - as defined per bounding box.
function subgrid() {
    echo "Applying bounding box"
    export MAGPLUS_HOME=/usr/local/opt/magics-4.9.3
    gribmagic smith bbox \
      "${PATH_RAW}/**/*regular-lat-lon*.grib2" --output=${PATH_SUBGRID} \
      --bbox=46.0 47.5 14.5 16.8 \
      --plot

    #   --use-netcdf \
}

acquire
subgrid

# Display plot.
# open xxx
