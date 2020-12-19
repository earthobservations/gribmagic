from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from gribmagic.enumerations.weather_models import WeatherModels
from gribmagic.exceptions.wrong_weather_model_exception import \
    WrongWeatherModelException
from gribmagic.modules.config.constants import KEY_VARIABLES, KEY_GRIB_PACKAGE_TYPES, \
    KEY_FORECAST_STEPS, \
    KEY_DIRECTORY_TEMPLATE, KEY_REMOTE_SERVER, KEY_FILE_TEMPLATE, \
    KEY_INITIALIZATION_DATE_FORMAT, KEY_FORECAST_STEPS_STR_LEN
from gribmagic.modules.file_list_handling.remote_file_list_creation import \
    remote_files_grib_directories, \
    remote_files_grib_packages, \
    build_remote_file_list


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.ICON_EU.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_DIRECTORY_TEMPLATE: 'test_remote_dir/{initialization_time}/{variable_name_lower}',
                KEY_FILE_TEMPLATE: 'test_remote_file_{level_type}_{initialization_date}{initialization_time}_'
                                   '{forecast_step}_{variable_name_upper}.grib2.bz2',
                KEY_REMOTE_SERVER: 'test1',
                KEY_INITIALIZATION_DATE_FORMAT: '%Y%m%d',
            }}
)
def test_build_remote_model_file_lists():
    to_test = remote_files_grib_directories(WeatherModels.ICON_EU,
                                            0,
                                            datetime(2020, 6,
                                                                  10).date())
    assert to_test == [Path(
        'test1/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_000_T_2M.grib2.bz2'),
                       Path(
                           'test1/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_001_T_2M.grib2.bz2')]


def test_build_remote_model_file_lists_wrong_weather_model():
    with pytest.raises(WrongWeatherModelException) as exc:
        _ = remote_files_grib_directories(
            WeatherModels.AROME_METEO_FRANCE,
            0,
            datetime(2020, 6, 10).date())
    assert str(exc.value) == 'Weather model does not offer grib data directories'


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.AROME_METEO_FRANCE.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_TEMPLATE: 'test_remote_file_{initialization_date}{initialization_time}_'
                                   '{forecast_step}_{grib_package_type}.grib2.bz2',
                KEY_REMOTE_SERVER: 'test1',
                KEY_INITIALIZATION_DATE_FORMAT: '%Y%m%d',
                KEY_GRIB_PACKAGE_TYPES: ['Package1'],
                KEY_FORECAST_STEPS_STR_LEN: 2,
                KEY_DIRECTORY_TEMPLATE: ''
            }}
)
def test_build_remote_model_file_lists_for_package():
    to_test = remote_files_grib_packages(
        WeatherModels.AROME_METEO_FRANCE,
        0,
        datetime(2020, 6, 10).date())
    assert to_test == [
        Path('test1/test_remote_file_2020061000_00_Package1.grib2.bz2'),
        Path('test1/test_remote_file_2020061000_01_Package1.grib2.bz2')]


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.AROME_METEO_FRANCE.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_TEMPLATE: 'test_remote_file_{initialization_date}{initialization_time}_'
                                   '{forecast_step}_{grib_package_type}.grib2.bz2',
                KEY_REMOTE_SERVER: 'test1',
                KEY_INITIALIZATION_DATE_FORMAT: '%Y%m%d',
                KEY_GRIB_PACKAGE_TYPES: ['Package1'],
                KEY_FORECAST_STEPS_STR_LEN: 2,
                KEY_DIRECTORY_TEMPLATE: ''
            }}
)
def test_build_remote_file_list():
    to_test = build_remote_file_list(
        WeatherModels.AROME_METEO_FRANCE,
        0,
        datetime(2020, 6, 10).date())
    assert to_test == [
        Path('test1/test_remote_file_2020061000_00_Package1.grib2.bz2'),
        Path('test1/test_remote_file_2020061000_01_Package1.grib2.bz2')]


def test_build_remote_model_file_lists_for_package_wrong_model():
    with pytest.raises(WrongWeatherModelException) as excinfo:
        _ = remote_files_grib_packages(
            WeatherModels.ICON_EU, 0, datetime(2020, 6, 10).date())
    assert str(excinfo.value) == 'Weather model does not offer grib data packages'
