import os
from pathlib import Path

icon_eu_input_file = Path(f"{os.getcwd()}/.gribmagic-testdata/input/"
                          f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2")
icon_eu_output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/"
                           f"air_temperature_2m.grib2")

harmonie_input_file = Path(f"{os.getcwd()}/.gribmagic-testdata/input/harm40_v1_p1_2019061100-single.tar")
harmonie_output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/harmonie_knmi_20200711_00_0.grib")

gfs_input_file = Path(f"{os.getcwd()}/.gribmagic-testdata/input/gfs.t00z.pgrb2.1p00.f000")
gfs_output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/ncep_gfs_100_20211004_00__000.grib2")
