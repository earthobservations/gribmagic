#!/usr/bin/env python
"""
Describe and invoke a downloading pipeline for GRIB data from DWD.

Inspired from ``test-download.sh`` by Michael Haberler.
See https://github.com/mhaberler/docker-dwd-open-data-downloader/commit/ff09dbc8.

Based upon DWD Open Data Downloader by Eduard Rosert and Björn Reetz,
with contributions by Michael Haberler.

- https://github.com/DeutscherWetterdienst/downloader
- https://github.com/EduardRosert/docker-dwd-open-data-downloader
- https://github.com/mhaberler/docker-dwd-open-data-downloader/tree/rewrite

Beforehand, install ``opendata-downloader.py`` by typing
``make install-dwd-grib-downloader`` within the toplevel directory.
It
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Parameter:
    name: str
    level: str
    options: dict = None


@dataclass
class Recipe:
    model: str
    grid: str
    parameters: List[Parameter]
    parameter_options: dict


def invoke():
    # TODO: Use recipe to build parameters for ``opendata-downloader.py`` and invoke it.
    pass


def process(recipe: Recipe):
    print(recipe)


def main():
    recipe = Recipe(
        model="icon-d2",
        grid="regular-lat-lon",
        parameters=[
            Parameter(name="vmax_10m", level="single-level"),
            Parameter(name="u", level="model-level", options={"levels": range(60, 62 + 1)}),
            Parameter(name="v", level="model-level", options={"levels": range(60, 62 + 1)}),
            Parameter(name="u", level="pressure-level", options={"levels": [950, 975]}),
            Parameter(name="v", level="pressure-level", options={"levels": [950, 975]}),
            # TODO
            # Parameter(name="hhl", level="time-invariant"),
        ],
        parameter_options={"timesteps": range(0, 2 + 1)},
    )
    process(recipe)


if __name__ == "__main__":
    main()
