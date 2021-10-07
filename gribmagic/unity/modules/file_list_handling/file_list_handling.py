""" functions to create remote lists of remote files that should be downloaded """
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.modules.config.constants import KEY_LOCAL_FILE_PATHS, \
    KEY_REMOTE_FILE_PATHS, KEY_LOCAL_STORE_FILE_PATHS
from gribmagic.unity.modules.file_list_handling.local_file_list_creation import \
    build_local_file_list, \
    build_local_store_file_list_for_variables
from gribmagic.unity.modules.file_list_handling.remote_file_list_creation import \
    build_remote_file_list


def build_model_file_lists(
        weather_model: WeatherModels,
        initialization_time: int,
        run_date: datetime.date
) -> Dict[str, List[Union[str, Path]]]:
    """
    builds a Dictionary with local and remote file paths for the given model

    Args:
        weather_model: defines the weather model 
        initialization_time: time of the day when forecast started
        run_date: date when forecast started

    Returns:
        Dict with lists for 
            - local storing
            - intermediate local store 
            - remote file path for downloading

    """
    return {
        KEY_LOCAL_STORE_FILE_PATHS: build_local_store_file_list_for_variables(
            weather_model,
            initialization_time,
            run_date),
        KEY_LOCAL_FILE_PATHS: build_local_file_list(
            weather_model,
            initialization_time,
            run_date),
        KEY_REMOTE_FILE_PATHS: build_remote_file_list(
            weather_model,
            initialization_time,
            run_date)
    }
