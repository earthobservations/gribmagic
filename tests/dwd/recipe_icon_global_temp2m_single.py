"""
Describe an example recipe for acquiring only a single GRIB file,
for testing purposes.

Because the regridding process is quite expensive, let's limit it
to be performed on one file only, in order to save resources.
"""
from gribmagic.dwd.download import Parameter, Recipe

recipe = Recipe(
    model="icon",
    grid="icosahedral",
    parameters=[
        Parameter(name="t_2m", level="single-level"),
    ],
    parameter_options={"timesteps": range(0, 1)},
)
