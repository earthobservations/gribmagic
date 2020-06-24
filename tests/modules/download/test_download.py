import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import os
from io import BytesIO
from pathlib import Path

from src.modules.parsing.parse_grib_data import concatenate_all_variable_files
from src.enumerations.unified_forecast_variables import ForecastVariables
from src.enumerations.weather_models import WeatherModels
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS
from src.modules.download.download import __download_parallel, __download


output_file = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                   'air_temperature_2m.grib2')


@patch(
    'src.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb')
    )
)
def test___download():
    __download((WeatherModels.ICON_EU,
                output_file,
                Path('test', 'mock')))

    assert output_file.is_file() is True

    os.remove(output_file)


@patch(
    'src.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb')
    )
)
def test___download_parallel():
    __download_parallel([(WeatherModels.ICON_EU,
                output_file,
                Path('test', 'mock'))])

    assert output_file.is_file() is True

    os.remove(output_file)
