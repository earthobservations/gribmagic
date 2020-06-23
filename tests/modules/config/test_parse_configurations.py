from src.enumerations.weather_models import WeatherModels
from src.modules.config.parse_configurations import parse_model_config, \
    parse_model_variables_levels_mapping, parse_model_variables_mapping


def test_parse_model_config():
    to_test = parse_model_config()[WeatherModels.TEST.value]
    assert to_test == {'remote_server': 'test1', 'remote_server_type': 'https',
                       'initialization_times': [0],
                       'forecast_steps': {0: [0, 1]},
                       'variables': ['air_temperature_2m'],
                       'directory_template': 'test_remote_dir/{initialization_time}/{variable_name_lower}',
                       'file_template': 'test_remote_file_{level_type}_{initialization_date}{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2',
                       'file_postfix': '.grib2',
                       'initialization_date_format': '%Y%m%d',
                       'compression': ''}


def test_parse_model_variables_levels_mapping():
    to_test = parse_model_variables_levels_mapping()[WeatherModels.TEST.value]
    assert to_test == {'air_temperature_2m': 'single-level'}


def test_parse_model_variables_mapping():
    to_test = parse_model_variables_mapping()[WeatherModels.TEST.value]
    assert to_test == {'air_temperature_2m': 't2m'}
