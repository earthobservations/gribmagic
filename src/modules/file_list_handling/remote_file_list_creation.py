""" functions to create remote lists of rmote files that should be downloaded """
from datetime import datetime
from typing import List

from pathlib import Path

from src.enumerations.weather_models import WeatherModels
from src.modules.config.configurations import MODEL_CONFIG, MODEL_VARIABLES_MAPPING, MODEL_VARIABLES_LEVELS_MAPPING
from src.modules.config.constants import KEY_FORECAST_STEPS, KEY_DIRECTORY_TEMPLATE, \
    KEY_FILE_TEMPLATE, KEY_REMOTE_SERVER, KEY_GRIB_PACKAGE_TYPES, KEY_VARIABLES, \
    KEY_INITIALIZATION_DATE_FORMAT, KEY_FORECAST_STEPS_STR_LEN
from src.exceptions.wrong_weather_model_exception import WrongWeatherModelException


def build_remote_file_list(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    selects the right remote_file_path generation function
    
    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of remote file paths

    """
    if KEY_GRIB_PACKAGE_TYPES in list(MODEL_CONFIG[weather_model.value]):
        return build_remote_file_lists_for_package_files(
            weather_model,
            initialization_time,
            run_date
        )
    else:
        return build_remote_file_lists_for_variable_files(
            weather_model,
            initialization_time,
            run_date
        )


def build_remote_file_lists_for_variable_files(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    This functions is a generic file path generator for remote grib files divided in variable directories

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of remote file paths

    """
    if weather_model not in [WeatherModels.ICON_GLOBAL, WeatherModels.COSMO_D2, WeatherModels.ICON_EU]:
        raise WrongWeatherModelException('Please choose one of [icon_global, icon_eu, cosmo_d2]')

    model_config = MODEL_CONFIG[weather_model.value]
    base_path = Path(model_config[KEY_REMOTE_SERVER])
    remote_file_list = []
    for variable in model_config[KEY_VARIABLES]:
        for forecast_step in model_config[KEY_FORECAST_STEPS][initialization_time]:
            remote_file_list.append(
                Path(
                    base_path,
                    model_config[KEY_DIRECTORY_TEMPLATE].format(
                        initialization_time=str(initialization_time).zfill(2),
                        variable_name_lower=MODEL_VARIABLES_MAPPING[weather_model.value][variable],
                    ),
                    model_config[KEY_FILE_TEMPLATE].format(
                        level_type=MODEL_VARIABLES_LEVELS_MAPPING[weather_model.value][variable],
                        initialization_date=run_date.strftime(model_config[KEY_INITIALIZATION_DATE_FORMAT]),
                        initialization_time=str(initialization_time).zfill(2),
                        forecast_step=str(forecast_step).zfill(3),
                        variable_name_upper=MODEL_VARIABLES_MAPPING[weather_model.value][variable].upper()
                    ))
            )
    return remote_file_list


def build_remote_file_lists_for_package_files(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    This functions is a generic file path generator for remote grib files
    divided in one or more grib data packages

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of remote file paths

    """
    if weather_model not in [WeatherModels.AROME_METEO_FRANCE,
                             WeatherModels.GEOS5,
                             WeatherModels.GFS_025,
                             WeatherModels.HARMONIE_KNMI]:
        raise WrongWeatherModelException('Please choose one of [arome_meteo_france, geos5, gfs, harmonie_knmi]')

    model_config = MODEL_CONFIG[weather_model.value]
    base_path = Path(model_config[KEY_REMOTE_SERVER])
    remote_file_list = []
    for grib_package in model_config[KEY_GRIB_PACKAGE_TYPES]:
        if KEY_FORECAST_STEPS[:-1] in model_config[KEY_FILE_TEMPLATE]:
            for forecast_step in model_config[KEY_FORECAST_STEPS][initialization_time]:
                remote_file_list.append(
                    Path(
                        base_path,
                        model_config[KEY_DIRECTORY_TEMPLATE].format(
                            initialization_date=run_date.strftime(model_config[KEY_INITIALIZATION_DATE_FORMAT]),
                            initialization_time=str(initialization_time).zfill(2),
                        ),
                        model_config[KEY_FILE_TEMPLATE].format(
                            grib_package_type=grib_package,
                            initialization_date=run_date.strftime(model_config[KEY_INITIALIZATION_DATE_FORMAT]),
                            initialization_time=str(initialization_time).zfill(2),
                            forecast_step=str(forecast_step).zfill(model_config[KEY_FORECAST_STEPS_STR_LEN]),
                        ))
                )
        else:
            remote_file_list.append(
                Path(
                    base_path,
                    model_config[KEY_DIRECTORY_TEMPLATE].format(
                        initialization_date=run_date.strftime(
                            model_config[KEY_INITIALIZATION_DATE_FORMAT]),
                        initialization_time=str(initialization_time).zfill(2),
                    ),
                    model_config[KEY_FILE_TEMPLATE].format(
                        grib_package_type=grib_package,
                        initialization_date=run_date.strftime(
                            model_config[KEY_INITIALIZATION_DATE_FORMAT]),
                        initialization_time=str(initialization_time).zfill(2),
                    ))
            )
    return remote_file_list
