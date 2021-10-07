import numpy as np
import os
from io import BytesIO

from gribmagic.unity.modules.download.local_store import bunzip_store
from gribmagic.unity.modules.parsing.parse_grib_data import concatenate_all_variable_files, \
    open_grib_file, create_inventory
from gribmagic.unity.enumerations.unified_forecast_variables import ForecastVariables
from gribmagic.unity.modules.config.constants import KEY_LOCAL_FILE_PATHS, \
    KEY_LIST_INDEX, KEY_LEVEL_TYPE
from tests.unity.fixtures import icon_eu_input_file, icon_eu_output_file

with open(icon_eu_input_file, 'rb') as file:
    test_data = file.read()


def test_concatenate_all_variable_files():

    bunzip_store(BytesIO(test_data), icon_eu_output_file)

    dataset = concatenate_all_variable_files(
        {KEY_LOCAL_FILE_PATHS: [icon_eu_output_file]},
        ForecastVariables.AIR_TEMPERATURE_2M)
    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64('2020-06-23T00:00:00.000000000')
    assert dataset.step.values == np.timedelta64(0)

    os.remove(icon_eu_output_file)


def test_open_grib_file_one_variable():

    bunzip_store(BytesIO(test_data), icon_eu_output_file)
    dataset = open_grib_file(icon_eu_output_file)[0]

    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64('2020-06-23T00:00:00.000000000')
    assert dataset.step.values == np.timedelta64(0)


def test_create_inventory():

    bunzip_store(BytesIO(test_data), icon_eu_output_file)
    dataset = open_grib_file(icon_eu_output_file)
    variables_inventory = create_inventory(dataset)

    assert variables_inventory == {
        't2m':
            [{
                KEY_LIST_INDEX: 0,
                KEY_LEVEL_TYPE: 'heightAboveGround'}]
    }

    os.remove(icon_eu_output_file)
