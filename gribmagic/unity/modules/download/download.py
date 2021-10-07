"""
Handle download of NWP data from remote servers.
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Tuple

import requests

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.models import WeatherModelSettings
from gribmagic.unity.modules.config.constants import (
    KEY_COMPRESSION,
    KEY_LOCAL_FILE_PATHS,
    KEY_REMOTE_FILE_PATHS,
)
from gribmagic.unity.modules.download.local_store import (
    bunzip_store,
    store,
    tarfile_store,
)

session = requests.Session()
logger = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_PARALLEL_PROCESSES = 4


def download(
    weather_model: WeatherModels,
    model_file_lists: Dict[str, List[str]],
    parallel_download: bool = False,
    n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES,
) -> None:
    """
    download weather forecasts
    """

    model = WeatherModelSettings(weather_model)

    if model.info[KEY_COMPRESSION] == "tar":
        return __download_tar_file(
            weather_model,
            model_file_lists[KEY_REMOTE_FILE_PATHS][0],
            model_file_lists[KEY_LOCAL_FILE_PATHS],
        )

    if parallel_download:
        download_specifications = [
            (weather_model, local_file_path, remote_file)
            for remote_file, local_file_path in zip(
                model_file_lists[KEY_REMOTE_FILE_PATHS],
                model_file_lists[KEY_LOCAL_FILE_PATHS],
            )
        ]
        return __download_parallel(download_specifications, n_processes)
    else:
        results = []
        for remote_file, local_file_path in zip(
            model_file_lists[KEY_REMOTE_FILE_PATHS],
            model_file_lists[KEY_LOCAL_FILE_PATHS],
        ):
            results.append(__download((weather_model, local_file_path, remote_file)))
            return results


def __download(download_specification: Tuple[WeatherModels, Path, str]) -> None:
    """
    base download function to manage single file download

    Args:
        download_specification: Tuple with
            - WeatherModels
            - local_file_path
            - remote_file_path

    Returns:
        Stores a file in temporary directory
    """

    weather_model = download_specification[0]
    model = WeatherModelSettings(weather_model)

    # Compute source URL and target file.
    url = download_specification[2]
    target_file = download_specification[1]

    if target_file.exists():
        logger.info(f"Skipping existing file {target_file}")
        return target_file

    logger.info(f"Downloading {url} to {target_file}")

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
    except Exception as ex:
        logger.warning(f"Accessing resource {url} failed: {ex}")
        return

    if not target_file.parent.is_dir():
        target_file.parent.mkdir(exist_ok=True)

    if model.info[KEY_COMPRESSION] == "bz2":
        bunzip_store(response.raw, target_file)
    else:
        store(response.raw, target_file)

    return target_file


def __download_parallel(
    download_specifications: List[Tuple[WeatherModels, Path, str]],
    n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES,
) -> None:
    """
    Script to run download in parallel
    Args:
        download_specifications: List of Tuple with
            - WeatherModels
            - local_file_path
            - remote_file_path
        n_processes: Number of parallel processes used for download
    Returns:
        None
    """
    with ThreadPoolExecutor(max_workers=n_processes) as executor:
        results = executor.map(__download, download_specifications)

    executor.shutdown(wait=True)
    return results


def __download_tar_file(
    weather_model: WeatherModels, url: str, local_file_list: List[Path]
) -> None:
    """
    Downloads a weather forecast package with one tar archive
    Args:
        weather_model:
        remote_file:
        local_file_list:

    Returns:
    """

    model = WeatherModelSettings(weather_model)

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
    except Exception as ex:
        logger.warning(f"Accessing resource {url} failed: {ex}")
        return

    return tarfile_store(response.raw, local_file_list)
