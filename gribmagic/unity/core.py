""" pre defined pipelines for download """
from datetime import datetime
from pathlib import Path
from typing import Union

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.models import AcquisitionRecipe
from gribmagic.unity.modules.download.download import download
from gribmagic.unity.modules.file_list_handling.file_list_handling import (
    build_model_file_lists,
)
from gribmagic.unity.modules.time.time_parsing import convert_iso_timestamp_to_date_time


def run_model_download(
    weather_model: Union[str, WeatherModels],
    initialization_timestamp: Union[str, datetime],
    target_directory: Union[str, Path],
) -> None:
    """
    Run a full stack model download as defined in `model_config.yml`.

    Args:
        :param weather_model: One of `WeatherModels`.
        :param initialization_timestamp: NWP run initialization time.
        :param target_directory: Where to store data into.

    Returns:
        Download weather forecast data and store into filesystem.
    """

    weather_model = WeatherModels(weather_model)

    if isinstance(initialization_timestamp, str):
        initialization_timestamp = convert_iso_timestamp_to_date_time(
            initialization_timestamp
        )

    recipe = AcquisitionRecipe(
        model=weather_model, timestamp=initialization_timestamp, target=target_directory
    )
    model_file_list = build_model_file_lists(recipe)
    return download(weather_model, model_file_list, parallel_download=True)
