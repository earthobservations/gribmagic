""" functions to create remote lists of rmote files that should be downloaded """
from datetime import datetime
from typing import Dict, List
import os

from pathlib import Path

from src.enumerations.weather_models import WeatherModels
from src.modules.config.configurations import MODEL_CONFIG
from src.modules.config.constants import KEY_VARIABLES, LOCAL_FILE_POSTFIX, KEY_FORECAST_STEPS


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


def build_local_file_list_for_variables(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> List[Path]:
    """
    Generic file path generator for intermediate storing downloaded grib data 

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        List of temporary locally stored files 

    """
    model_config = MODEL_CONFIG[weather_model.value]
    base_path = Path(os.environ['BASE_STORE_DIR'])
    local_file_list = []
    for variable in model_config[KEY_VARIABLES]:
        for forecast_step in model_config[KEY_FORECAST_STEPS][initialization_time]:
            local_file_list.append(
                Path(
                    base_path,
                    'tmp',
                    f"{weather_model.value}_{run_date.strftime('%Y%m%d')}_{str(initialization_time).zfill(2)}_{variable}_{forecast_step}.grib"
                    ))
    return local_file_list
