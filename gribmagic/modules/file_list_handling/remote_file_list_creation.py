""" functions to create remote lists of remote files that should be downloaded """
from datetime import datetime
from typing import List

from pathlib import Path

from gribmagic.enumerations.weather_models import WeatherModels
from gribmagic.models import WeatherModelSettings
from gribmagic.modules.config.constants import KEY_FORECAST_STEPS, KEY_DIRECTORY_TEMPLATE, \
    KEY_FILE_TEMPLATE, KEY_REMOTE_SERVER, \
    KEY_INITIALIZATION_DATE_FORMAT, KEY_FORECAST_STEPS_STR_LEN
from gribmagic.exceptions.wrong_weather_model_exception import WrongWeatherModelException


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
    model = WeatherModelSettings(weather_model)
    if model.has_grib_packages:
        return remote_files_grib_packages(
            weather_model,
            initialization_time,
            run_date
        )
    else:
        return remote_files_grib_directories(
            weather_model,
            initialization_time,
            run_date
        )


def remote_files_grib_directories(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    This functions is a generic file path generator for
    remote grib files within different directories.

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of remote file paths

    """

    model = WeatherModelSettings(weather_model)

    # Sanity checks
    if model.has_grib_packages:
        raise WrongWeatherModelException("Weather model does not offer grib data directories")

    base_path = Path(model.info[KEY_REMOTE_SERVER])
    remote_file_list = []
    for variable in model.variables:
        for forecast_step in model.info[KEY_FORECAST_STEPS][initialization_time]:
            remote_file_list.append(
                Path(
                    base_path,
                    model.info[KEY_DIRECTORY_TEMPLATE].format(
                        initialization_time=str(initialization_time).zfill(2),
                        variable_name_lower=model.variable(variable),
                    ),
                    model.info[KEY_FILE_TEMPLATE].format(
                        level_type=model.level(variable),
                        initialization_date=run_date.strftime(model.info[KEY_INITIALIZATION_DATE_FORMAT]),
                        initialization_time=str(initialization_time).zfill(2),
                        forecast_step=str(forecast_step).zfill(3),
                        variable_name_upper=model.variable(variable).upper(),
                        variable_name_lower=model.variable(variable),
                    ))
            )
    return remote_file_list


def remote_files_grib_packages(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    This functions is a generic file path generator for
    remote grib files within one or more grib data packages.

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of remote file paths

    """

    model = WeatherModelSettings(weather_model)

    # Sanity checks
    if not model.has_grib_packages:
        raise WrongWeatherModelException("Weather model does not offer grib data packages")

    model_config = model.info

    base_path = Path(model.info[KEY_REMOTE_SERVER])
    remote_file_list = []
    for grib_package in model.grib_packages:
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
