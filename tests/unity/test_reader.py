import os
from io import BytesIO

import numpy as np

from gribmagic.unity.configuration.constants import (
    KEY_LEVEL_TYPE,
    KEY_LIST_INDEX,
    KEY_LOCAL_FILE_PATHS,
)
from gribmagic.unity.download.decoder import decode_bunzip
from gribmagic.unity.enumerations import ForecastVariables
from gribmagic.unity.reader import (
    concatenate_all_variable_files,
    create_inventory,
    open_grib_file,
)
from tests.unity.fixtures import icon_eu_input_file, icon_eu_output_file

with open(icon_eu_input_file, "rb") as file:
    test_data = file.read()


def test_concatenate_all_variable_files():

    decode_bunzip(BytesIO(test_data), icon_eu_output_file)

    dataset = concatenate_all_variable_files(
        {KEY_LOCAL_FILE_PATHS: [icon_eu_output_file]},
        ForecastVariables.AIR_TEMPERATURE_2M,
    )
    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64("2020-06-23T00:00:00.000000000")
    assert dataset.step.values == np.timedelta64(0)

    os.remove(icon_eu_output_file)


def test_open_grib_file_one_variable():

    decode_bunzip(BytesIO(test_data), icon_eu_output_file)
    dataset = open_grib_file(icon_eu_output_file)[0]

    assert dataset.latitude.shape == (657,)
    assert dataset.longitude.shape == (1097,)

    assert dataset.time.values == np.datetime64("2020-06-23T00:00:00.000000000")
    assert dataset.step.values == np.timedelta64(0)


def test_create_inventory():

    decode_bunzip(BytesIO(test_data), icon_eu_output_file)
    dataset = open_grib_file(icon_eu_output_file)
    variables_inventory = create_inventory(dataset)

    assert variables_inventory == {
        "t2m": [{KEY_LIST_INDEX: 0, KEY_LEVEL_TYPE: "heightAboveGround"}]
    }

    os.remove(icon_eu_output_file)
