""" pre defined pipelines for download """
from datetime import datetime
from pathlib import Path
from typing import Union

from gribmagic.unity.download.engine import run_download
from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.index import make_fileindex
from gribmagic.unity.model import AcquisitionRecipe
from gribmagic.util import parse_timestamp


def run_model_download(
    weather_model: Union[str, WeatherModel],
    initialization_timestamp: Union[str, datetime],
    target_directory: Union[str, Path],
) -> None:
    """
    Run a full stack model download as defined in `model_config.yml`.

    Args:
        :param weather_model: One of `WeatherModel`.
        :param initialization_timestamp: NWP run initialization time.
        :param target_directory: Where to store data into.

    Returns:
        Download weather forecast data and store into filesystem.
    """

    weather_model = WeatherModel(weather_model)

    if isinstance(initialization_timestamp, str):
        initialization_timestamp = parse_timestamp(initialization_timestamp)

    recipe = AcquisitionRecipe(
        model=weather_model, timestamp=initialization_timestamp, target=target_directory
    )
    model_file_list = make_fileindex(recipe)
    return run_download(weather_model, model_file_list, parallel_download=True)
