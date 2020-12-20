""" pre defined pipelines for download """
from gribmagic.modules.file_list_handling.file_list_handling import \
    build_model_file_lists
from gribmagic.enumerations.weather_models import WeatherModels
from datetime import datetime
from gribmagic.modules.time.time_parsing import \
    convert_iso_timestamp_to_date_time
from typing import Union
from gribmagic.modules.download.download import download


def run_model_download(
        weather_model: Union[str, WeatherModels],
        initialization_timestamp: Union[str, datetime]
) -> None:
    """
    Pipeline to call all process to run a full stack model download as defined
        in the model_config.yaml

    example:

    python3 gribmagic/pipelines/run.py run_model_download icon_eu 2020-06-24T00:00:00Z

    Args:
        weather_model: is one of 
            - icon_global, icon_eu, icon_eu_eps
            - cosmo_d2, cosmo_d2_eps
            - ncep_gfs_025, arome_meteo_france, harmonie_knmi
        initialization_timestamp: 
            - nwp run initialization time

    Returns:
        Stores data on file system defined by env. var. BASE_STORE_DIR

    """

    weather_model = WeatherModels(weather_model)

    if isinstance(initialization_timestamp, str):
        initialization_timestamp = convert_iso_timestamp_to_date_time(
            initialization_timestamp)
    model_file_list = build_model_file_lists(
        weather_model,
        initialization_timestamp.hour,
        initialization_timestamp.date())
    download(weather_model, model_file_list, parallel_download=True)
