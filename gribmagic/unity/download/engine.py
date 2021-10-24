"""
Handle download of NWP data from remote servers.
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List

import requests

from gribmagic.unity.configuration.constants import (
    KEY_COMPRESSION,
    KEY_LOCAL_FILE_PATHS,
    KEY_REMOTE_FILE_PATHS,
)
from gribmagic.unity.configuration.model import WeatherModelSettings
from gribmagic.unity.download.decoder import (
    decode_bunzip,
    decode_identity,
    decode_tarfile,
)
from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.model import DownloadItem

session = requests.Session()
logger = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_PARALLEL_PROCESSES = 4


def run_download(
    weather_model: WeatherModel,
    model_file_lists: Dict[str, List[str]],
    parallel_download: bool = False,
    n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES,
) -> None:
    """
    Download weather forecasts data.
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
            DownloadItem(model=weather_model, local_file=local_file_path, remote_url=remote_file)
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
            item = DownloadItem(
                model=weather_model, local_file=local_file_path, remote_url=remote_file
            )
            results.append(__download(item))
            return results


def __download(item: DownloadItem) -> None:
    """
    base download function to manage single file download

    Args:
        download_specification: Tuple with
            - WeatherModel
            - local_file_path
            - remote_file_path

    Returns:
        Stores a file in temporary directory
    """

    model = WeatherModelSettings(item.model)

    # Compute source URL and target file.
    url = item.remote_url
    target_file = Path(item.local_file)

    if target_file.exists():
        logger.info(f"Skipping existing file {target_file}")
        return target_file

    logger.info(f"Downloading {url} to {target_file}")

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
    except Exception as ex:
        logger.warning(f"Failed accessing resource {url}: {ex}")
        return

    if not target_file.parent.is_dir():
        target_file.parent.mkdir(exist_ok=True)

    if model.info[KEY_COMPRESSION] == "bz2":
        decode_bunzip(response.raw, target_file)
    else:
        decode_identity(response.raw, target_file)

    return target_file


def __download_parallel(
    download_specifications: List[DownloadItem],
    n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES,
) -> None:
    """
    Script to run download in parallel
    Args:
        download_specifications: List of Tuple with
            - WeatherModel
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
    weather_model: WeatherModel, url: str, local_file_list: List[Path]
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
        logger.warning(f"Failed accessing resource {url}: {ex}")
        return

    return decode_tarfile(response.raw, local_file_list)
