#/bin/sh

set -e

PATH_RAW=.gribmagic-data/raw
PATH_SUBGRID=.gribmagic-data/subgrid

mkdir -p ${PATH_RAW}

# Acquire subset of data/
# Here: Wind - as defined per recipe.
python demo/pipeline/pipeline.py \
  --recipe="demo/pipeline/recipe.py" \
  --timestamp="2020122212" \
  --output="${PATH_RAW}"

# Extract area of interest.
# Here: Austria: West + Oststeiermark - as defined per bounding box.
python demo/grib_bbox.py \
  "${PATH_RAW}/**/*.grib2" --output=${PATH_SUBGRID} \
  --bbox=46.0 47.5 14.5 16.8 \
  --plot

# Display plot.
# open xxx
