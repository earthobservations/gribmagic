from src.modules.file_list_handling.local_file_list_creation import \
    build_local_file_list_for_variables, build_local_store_file_list_for_variables
from src.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path


def test_build_local_file_list_for_variables():
    to_test = build_local_file_list_for_variables(WeatherModels.TEST,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/tmp/test_model_20200610_00_air_temperature_2m_0.grib'),
                               Path('/app/data/tmp/test_model_20200610_00_air_temperature_2m_1.grib')]


def test_build_local_store_file_list_for_variables():
    to_test = build_local_store_file_list_for_variables(WeatherModels.TEST,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/test_model/20200610_00/air_temperature_2m.nc')]
