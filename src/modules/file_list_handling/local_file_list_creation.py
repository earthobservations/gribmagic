""" functions to create remote lists of rmote files that should be downloaded """
from datetime import datetime
from typing import Dict, List
import os

from pathlib import Path

from src.enumerations.weather_models import WeatherModels
from src.modules.config.configurations import MODEL_CONFIG
from src.modules.config.constants import KEY_VARIABLES, LOCAL_FILE_POSTFIX,\
    KEY_FORECAST_STEPS, KEY_GRIB_PACKAGE_TYPES, KEY_FILE_POSTFIX
from src.exceptions.grib_package_exception import GribPackageException


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
    model_config = MODEL_CONFIG[weather_model.value]
    base_path = Path(os.environ['BASE_STORE_DIR'])
    local_file_list = []
    for variable in model_config[KEY_VARIABLES]:
        local_file_list.append(
            Path(
                base_path,
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
    model_config = MODEL_CONFIG[weather_model.value]
    grib_packages = KEY_GRIB_PACKAGE_TYPES in list(model_config.keys())
    
    if grib_packages and weather_model not in [WeatherModels.AROME_METEO_FRANCE, WeatherModels.GEOS5]:
        raise GribPackageException(f"You have set grib_packages flag True, but "
                                   f"{weather_model.value} does not provide grib data in packages")
    elif grib_packages:
        iterator_values = model_config[KEY_GRIB_PACKAGE_TYPES]
    else:
        iterator_values = model_config[KEY_VARIABLES]
        
    base_path = Path(os.environ['BASE_STORE_DIR'])
    local_file_list = []
    for var in iterator_values:
        for forecast_step in model_config[KEY_FORECAST_STEPS][initialization_time]:
            local_file_list.append(
                Path(
                    base_path,
                    'tmp',
                    f"{weather_model.value}_{run_date.strftime('%Y%m%d')}_{str(initialization_time).zfill(2)}_{var}_{forecast_step}.{model_config[KEY_FILE_POSTFIX]}"
                    ))
    return local_file_list

