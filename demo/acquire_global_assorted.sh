#/bin/sh

set -e

PATH_RAW=.gribmagic-data/raw

mkdir -p ${PATH_RAW}

export PYTHONPATH=$(pwd)
python demo/pipeline/pipeline.py \
  --recipe="demo/pipeline/recipe_global_assorted.py" \
  --timestamp="2021100312" \
  --output="${PATH_RAW}"
