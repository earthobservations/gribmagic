#/bin/sh

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
      --timestamp="2021101712" \
      --output="${PATH_RAW}"
}

# Extract area of interest.
# Here: Austria: West + Oststeiermark - as defined per bounding box.
function subgrid() {
    echo "Applying bounding box"
    export MAGPLUS_HOME=/usr/local/opt/magics
    python demo/grib_bbox.py \
      "${PATH_RAW}/**/*regular-lat-lon*.grib2" --output=${PATH_SUBGRID} \
      --bbox=46.0 47.5 14.5 16.8 \
      --plot

    #   --use-netcdf \
}

acquire
subgrid

# Display plot.
# open xxx
