"""
Describe an example recipe for acquiring a very small subset of GRIB files,
for testing purposes.
"""
from gribmagic.dwd.download import Parameter, Recipe

recipe = Recipe(
    model="icon",
    grid="icosahedral",
    parameters=[
        Parameter(name="t_2m", level="single-level"),
    ],
    parameter_options={"timesteps": range(0, 3)},
)
