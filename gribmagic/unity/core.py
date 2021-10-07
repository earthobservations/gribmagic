""" pre defined pipelines for download """
from gribmagic.unity.modules.file_list_handling.file_list_handling import \
    build_model_file_lists
from gribmagic.unity.enumerations.weather_models import WeatherModels
from datetime import datetime
from gribmagic.unity.modules.time.time_parsing import \
    convert_iso_timestamp_to_date_time
from typing import Union
from gribmagic.unity.modules.download.download import download


def run_model_download(
        weather_model: Union[str, WeatherModels],
        initialization_timestamp: Union[str, datetime]
) -> None:
    """
    Run a full stack model download as defined in `model_config.yml`.

    Args:
        weather_model: is one of 
            - dwd-icon-global, dwd-icon-eu, dwd-icon-eu-eps
            - dwd-cosmo-d2, dwd-cosmo-d2-eps
            - ncep-gfs-025, meteo-france-arome, knmi-harmonie
        initialization_timestamp: 
            - nwp run initialization time

    Returns:
        Stores data on file system defined by environment variable "GM_DATA_PATH"
    """

    weather_model = WeatherModels(weather_model)

    if isinstance(initialization_timestamp, str):
        initialization_timestamp = convert_iso_timestamp_to_date_time(
            initialization_timestamp)
    model_file_list = build_model_file_lists(
        weather_model,
        initialization_timestamp.hour,
        initialization_timestamp.date())
    return download(weather_model, model_file_list, parallel_download=True)
