"""
Describe an example recipe for acquiring a subset of GRIB files.
"""
from demo.pipeline.pipeline import Recipe, Parameter

recipe = Recipe(
    model="icon",
    #grid="regular-lat-lon",
    grid=None,

    # Acquire assorted data
    parameters=[
        #Parameter(name="t", level="single-level"),
        Parameter(name="t", level="model-level"),
        Parameter(name="tot_prec", level="single-level"),
        Parameter(name="vmax_10m", level="single-level"),
    ],
    #parameter_options={"timesteps": range(0, 180 + 1), "levels": range(0, 90 + 1)},
    parameter_options={"timesteps": range(1, 78 + 1), "levels": [90]},
)
