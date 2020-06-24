from src.modules.file_list_handling.remote_file_list_creation import \
    build_remote_file_lists_for_variable_files, build_remote_file_lists_for_package_files
from src.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path
import pytest
from src.exceptions.wrong_weather_model_exception import WrongWeatherModelException
from unittest.mock import patch
from src.modules.config.constants import KEY_VARIABLES, KEY_GRIB_PACKAGE_TYPES, KEY_FORECAST_STEPS, \
    KEY_DIRECTORY_TEMPLATE, KEY_REMOTE_SERVER, KEY_FILE_TEMPLATE, KEY_INITIALIZATION_DATE_FORMAT


@patch(
    'src.modules.file_list_handling.remote_file_list_creation.MODEL_CONFIG',
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
    to_test = build_remote_file_lists_for_variable_files(WeatherModels.ICON_EU,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == [Path('test1/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_000_T_2M.grib2.bz2'),
                       Path('test1/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_001_T_2M.grib2.bz2')]


def test_build_remote_model_file_lists_wrong_weather_model():
    with pytest.raises(WrongWeatherModelException) as exc:
        _ = build_remote_file_lists_for_variable_files(WeatherModels.AROME_METEO_FRANCE,
                                                             0,
                                                             datetime(2020, 6, 10).date())
    assert str(exc.value) == 'Please choose one of [icon_global, icon_eu, cosmo_d2]'


@patch(
    'src.modules.file_list_handling.remote_file_list_creation.MODEL_CONFIG',
    {
        WeatherModels.AROME_METEO_FRANCE.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_TEMPLATE: 'test_remote_file_{initialization_date}{initialization_time}_'
                                   '{forecast_step}_{grib_package_type}.grib2.bz2',
                KEY_REMOTE_SERVER: 'test1',
                KEY_INITIALIZATION_DATE_FORMAT: '%Y%m%d',
                KEY_GRIB_PACKAGE_TYPES: ['Package1']
            }}
)
def test_build_remote_model_file_lists_for_package():
    to_test = build_remote_file_lists_for_package_files(WeatherModels.AROME_METEO_FRANCE,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == [Path('test1/test_remote_file_2020061000_00_Package1.grib2.bz2'),
                       Path('test1/test_remote_file_2020061000_01_Package1.grib2.bz2')]
