""" functions to create remote lists of rmote files that should be downloaded """
from datetime import datetime
from typing import Dict, List

from pathlib import Path

from src.enumerations.weather_models import WeatherModels
from src.modules.config.configurations import MODEL_CONFIG, MODEL_VARIABLES_MAPPING, MODEL_VARIABLES_LEVELS_MAPPING
from src.modules.config.constants import KEY_FORECAST_STEPS, KEY_DIRECTORY_TEMPLATE, \
    KEY_FILE_TEMPLATE, KEY_REMOTE_SERVER, KEY_REMOTE_SERVER_TYPE, KEY_VARIABLES, \
    KEY_INITIALIZATION_DATE_FORMAT


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
