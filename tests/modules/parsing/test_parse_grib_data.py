import numpy as np
import os
from io import BytesIO
from pathlib import Path

from src.modules.download.local_store import bunzip_store
from src.modules.parsing.parse_grib_data import concatenate_all_variable_files
from src.enumerations.unified_forecast_variables import ForecastVariables
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS


def test_concatenate_all_variable_files():
    output_file = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                       'air_temperature_2m.grib2')
    with open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb') as file:
        test_data = file.read()
    bunzip_store(BytesIO(test_data), output_file)

    dataset = concatenate_all_variable_files(
        {KEY_LOCAL_FILE_PATHS: [output_file]},
        ForecastVariables.AIR_TEMPERATURE_2M)
    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64('2020-06-23T00:00:00.000000000')
    assert dataset.step.values == np.timedelta64(0)

    os.remove(output_file)
