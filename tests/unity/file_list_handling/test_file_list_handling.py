from gribmagic.unity.modules.file_list_handling.file_list_handling import build_model_file_lists
from unittest.mock import patch
from gribmagic.unity.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path
from gribmagic.unity.modules.config.constants import KEY_VARIABLES, KEY_FORECAST_STEPS, \
    KEY_DIRECTORY_TEMPLATE, KEY_REMOTE_SERVER, KEY_FILE_TEMPLATE, KEY_INITIALIZATION_DATE_FORMAT, KEY_FILE_POSTFIX


@patch(
    'gribmagic.unity.models.MODEL_CONFIG',
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
                KEY_FILE_POSTFIX: 'grib'
            }}
)
@patch(
    'gribmagic.unity.models.MODEL_CONFIG',
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
                KEY_FILE_POSTFIX: 'grib'
            }}
)
def test_build_model_file_lists():
    to_test = build_model_file_lists(WeatherModels.ICON_EU,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == \
           {'local_file_paths': [Path('/app/data/tmp/icon_eu_20200610_00_air_temperature_2m_000.grib'),
                                 Path('/app/data/tmp/icon_eu_20200610_00_air_temperature_2m_001.grib')],
            'remote_file_paths': [Path('test1/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_000_T_2M.grib2.bz2'),
                                  Path('test1/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_001_T_2M.grib2.bz2')],
            'local_store_file_paths': [Path('/app/data/icon_eu/20200610_00/air_temperature_2m.nc')]
            }
