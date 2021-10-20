import os
from datetime import datetime
from pathlib import Path

from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.model import AcquisitionRecipe

recipe_icon = AcquisitionRecipe(
    model=WeatherModel.DWD_ICON_EU,
    timestamp=datetime(2020, 6, 10, 0, 0),
    target="/app/data",
)
recipe_arome = AcquisitionRecipe(
    model=WeatherModel.METEO_FRANCE_AROME,
    timestamp=datetime(2020, 6, 10, 0, 0),
    target="/app/data",
)
recipe_harmonie = AcquisitionRecipe(
    model=WeatherModel.KNMI_HARMONIE,
    timestamp=datetime(2020, 6, 10, 0, 0),
    target="/app/data",
)


testdata_path = Path(f"{os.getcwd()}/.gribmagic-testdata")

icon_global_input_file = (
    testdata_path / "input" / "icon-global_regular-lat-lon_air-temperature_level-90.grib2"
)

icon_eu_input_file = (
    testdata_path
    / "input/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2"
)
icon_eu_output_file = testdata_path / "output/air_temperature_2m.grib2"

harmonie_input_file = testdata_path / "input/harm40_v1_p1_2019061100-single.tar"
harmonie_output_file = testdata_path / "output/knmi-harmonie_20200711_00_0.grib"

gfs_input_file = testdata_path / "input/gfs.t00z.pgrb2.1p00.f000"
gfs_output_file = testdata_path / "output/ncep-gfs-100_20211004_00__000.grib2"
