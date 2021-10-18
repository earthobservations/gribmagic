#/bin/sh

set -e

PATH_RAW=.gribmagic-data/raw

mkdir -p ${PATH_RAW}

gribmagic dwd acquire \
  --recipe="examples/dwd/recipe_global_assorted.py" \
  --timestamp="2021101712" \
  --output="${PATH_RAW}"
