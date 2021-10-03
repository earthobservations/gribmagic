"""
Describe an example recipe for acquiring a subset of GRIB files.

Inspired from ``test-download.sh`` by Michael Haberler.
See https://github.com/mhaberler/docker-dwd-open-data-downloader/commit/ff09dbc8.
"""
from demo.pipeline.pipeline import Recipe, Parameter

recipe = Recipe(
    model="icon-d2",
    grid="regular-lat-lon",

    # Acquire wind data
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
