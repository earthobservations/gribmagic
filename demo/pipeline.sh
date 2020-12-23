#/bin/sh

set -e

outfolder=.gribmagic-data/raw
mkdir -p ${outfolder}

python demo/pipeline/pipeline.py \
  --recipe="demo/pipeline/recipe.py" \
  --timestamp="2020122212" \
  --output="${outfolder}"
