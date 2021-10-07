""" functions to create remote lists of remote files that should be downloaded """
from datetime import datetime
from typing import Dict, List
import os

from pathlib import Path

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.models import WeatherModelSettings
from gribmagic.unity.modules.config.constants import LOCAL_FILE_POSTFIX,\
    KEY_FORECAST_STEPS, KEY_GRIB_PACKAGE_TYPES, KEY_FILE_POSTFIX, \
    KEY_FILE_TEMPLATE


def build_local_store_file_list_for_variables(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    Generic file path generator for persisting local netcdf files

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of local store file paths

    """
    model = WeatherModelSettings(weather_model)
    data_path = Path(os.environ['GM_DATA_PATH'])
    local_file_list = []
    for variable in model.variables:
        local_file_list.append(
            Path(
                data_path,
                weather_model.value,
                f"{run_date.strftime('%Y%m%d')}_{str(initialization_time).zfill(2)}",
                f"{variable}.{LOCAL_FILE_POSTFIX}"
        ))
    return local_file_list


def build_local_file_list(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date,
) -> List[Path]:
    """
    Generic file path generator downloaded grib data per each variable

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of temporary locally stored files 

    """
    model = WeatherModelSettings(weather_model)

    if weather_model == WeatherModels.HARMONIE_KNMI:
        return _local_file_paths_for_harmonie(
            run_date,
            initialization_time,
            model.info
        )
    elif model.has_grib_packages:
        variables_iterator = model.info[KEY_GRIB_PACKAGE_TYPES]
    else:
        variables_iterator = model.variables

    return _build_local_file_list_with_variables_iterator(
        weather_model,
        run_date,
        initialization_time,
        variables_iterator,
        model.info)


def _build_local_file_list_with_variables_iterator(
        weather_model: WeatherModels,
        run_date: datetime,
        initialization_time: int,
        variables_iterator: List[str],
        model_config
) -> List[Path]:
    data_path = Path(os.environ['GM_DATA_PATH'])
    local_file_list = []
    for var in variables_iterator:
        if "{forecast_step}" in model_config[KEY_FILE_TEMPLATE]:
            for forecast_step in model_config[KEY_FORECAST_STEPS][initialization_time]:
                local_file_list.append(
                    Path(
                        data_path,
                        'tmp',
                        f"{weather_model.value}_{run_date.strftime('%Y%m%d')}_"
                        f"{str(initialization_time).zfill(2)}_{var}_"
                        f"{str(forecast_step).zfill(3)}.{model_config[KEY_FILE_POSTFIX]}"
                    ))
        else:
            # This code path probably has been used for KNMI Harmonie.
            # However, raw files are only available via API these days.
            local_file_list.append(
                Path(
                    data_path,
                    'tmp',
                    f"{weather_model.value}_{run_date.strftime('%Y%m%d')}_"
                    f"{str(initialization_time).zfill(2)}_{var}."
                    f"{model_config[KEY_FILE_POSTFIX]}"
                ))
    return local_file_list


def _local_file_paths_for_harmonie(
        run_date: datetime,
        initialization_time: int,
        model_config: Dict[str, any]
) -> List[Path]:
    """
    special local file path generator for HARMONIE model
    Args:
        run_date:
        initialization_time:
        model_config:

    Returns:

    """
    data_path = Path(os.environ['GM_DATA_PATH'])
    local_file_list = []
    for forecast_step in model_config[KEY_FORECAST_STEPS][initialization_time]:
        local_file_list.append(
            Path(
                data_path,
                'tmp',
                f"{WeatherModels.HARMONIE_KNMI.value}_{run_date.strftime('%Y%m%d')}_"
                f"{str(initialization_time).zfill(2)}_{forecast_step}."
                f"{model_config[KEY_FILE_POSTFIX]}"
                ))
    return local_file_list
