from src.enumerations.weather_models import WeatherModels
from src.modules.config.parse_configurations import parse_model_config, \
    parse_model_variables_levels_mapping, parse_model_variables_mapping


def test_parse_model_config():
    to_test = parse_model_config()[WeatherModels.AROME_METEO_FRANCE.value]
    assert to_test == {'remote_server': 'dcpc-nwp.meteo.fr/services', 'remote_server_type': 'http',
                       'initialization_times': [0, 3, 6, 12, 18], 'forecast_steps': {
            0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
            3: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
            6: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
            12: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
            18: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]},
                       'grib_package_types': ['HP', 'SP1', 'SP2', 'SP3'], 'variables': ['air_temperature_2m'],
                       'file_template': 'PS_GetCache_DCPCPreviNum?model=AROME&grid=0.01&package={grib_package_type}&time={forecast_step}H&referencetime={initialization_date}T{initialization_time}:00:00Z&format=grib2',
                       'initialization_date_format': '%Y-%m-%d',
                       'file_postfix': 'grib2',  'compression': ''}


def test_parse_model_variables_levels_mapping():
    to_test = parse_model_variables_levels_mapping()[WeatherModels.ICON_EU.value]
    assert to_test == {'air_temperature_2m': 'single-level', 'snow_height': 'single-level',
                       'max_wind_gust_10m': 'single-level', 'wind_u_10m': 'single-level', 'wind_v_10m': 'single-level',
                       'dewpoint_2m': 'single-level', 'total_precipitation': 'single-level',
                       'convective_snow': 'single-level', 'grid_scale_snow': 'single-level',
                       'convective_rain': 'single-level', 'grid_scale_rain': 'single-level',
                       'global_horizontal_irradiance': 'single-level', 'direct_normal_irradiance': 'single-level',
                       'diffuse_horizontal_irradiance': 'single-level', 'mixed_layer_cape': 'single-level',
                       'pressure_mean_sea_level': 'single-level', 'max_air_temperature_2m': 'single-level',
                       'min_air_temperature_2m': 'single-level', 'weather_synop_code': 'single-level',
                       'soil_temperature': 'single-level', 'total_cloud_cover': 'single-level',
                       'relative_humidity_2m': 'single-level', 'temperature': 'model-level', 'wind_u': 'model-level',
                       'wind_v': 'model-level', 'relative_humidity': 'pressure-level',
                       'geopotential_height': 'pressure-level', 'snowfall_height': 'single-level'}


def test_parse_model_variables_mapping():
    to_test = parse_model_variables_mapping()[WeatherModels.ICON_EU.value]
    assert to_test == {'albedo': 'alb_rad', 'air_temperature_2m': 't_2m', 'snow_height': 'h_snow',
                       'max_wind_gust_10m': 'vmax_10m', 'wind_u_10m': 'u_10m', 'wind_v_10m': 'v_10m',
                       'dewpoint_2m': 'td_2m', 'total_precipitation': 'tot_prec', 'convective_snow': 'snow_con',
                       'grid_scale_snow': 'snow_gsp', 'convective_rain': 'rain_con', 'grid_scale_rain': 'rain_gsp',
                       'global_horizontal_irradiance': 'asob_s', 'direct_normal_irradiance': 'aswdir_s',
                       'diffuse_horizontal_irradiance': 'aswdiff_s', 'mixed_layer_cape': 'cape_ml',
                       'pressure_mean_sea_level': 'pmsl', 'max_air_temperature_2m': 'tmax_2m',
                       'min_air_temperature_2m': 'tmin_2m', 'weather_synop_code': 'ww', 'soil_temperature': 't_g',
                       'total_cloud_cover': 'clct', 'relative_humidity_2m': 'relhum_2m', 'temperature': 't',
                       'wind_u': 'u', 'wind_v': 'v', 'geopotential_height': 'fi', 'snowfall_height': 'snowlmt',
                       'relative_humidity': 'relhum'}
