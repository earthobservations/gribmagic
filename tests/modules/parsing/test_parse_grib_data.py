import numpy as np
import os
from io import BytesIO
from pathlib import Path

from src.modules.download.local_store import bunzip_store
from src.modules.parsing.parse_grib_data import concatenate_all_variable_files, \
    open_grib_file, extract_variables_per_dataset_in_list
from src.enumerations.unified_forecast_variables import ForecastVariables
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS, \
    KEY_LIST_INDEX, KEY_LEVEL_TYPE

output_file = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                   'air_temperature_2m.grib2')

with open(f"{os.getcwd()}/tests/modules/download/fixtures/"
          f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
          'rb') as file:
    test_data = file.read()


def test_concatenate_all_variable_files():

    bunzip_store(BytesIO(test_data), output_file)

    dataset = concatenate_all_variable_files(
        {KEY_LOCAL_FILE_PATHS: [output_file]},
        ForecastVariables.AIR_TEMPERATURE_2M)
    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64('2020-06-23T00:00:00.000000000')
    assert dataset.step.values == np.timedelta64(0)

    os.remove(output_file)


def test_open_grib_file_one_variable():

    bunzip_store(BytesIO(test_data), output_file)
    dataset = open_grib_file(output_file)[0]

    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64('2020-06-23T00:00:00.000000000')
    assert dataset.step.values == np.timedelta64(0)


def test_extract_variables_per_dataset_in_list():

    bunzip_store(BytesIO(test_data), output_file)
    dataset = open_grib_file(output_file)
    variables_inventory = extract_variables_per_dataset_in_list(dataset)

    assert variables_inventory == {
        't2m':
            [{
                KEY_LIST_INDEX: 0,
                KEY_LEVEL_TYPE: 'heightAboveGround'}]
    }

    os.remove(output_file)
