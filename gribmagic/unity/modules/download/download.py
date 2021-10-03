"""
handle download of nwp from remote servers
"""
import logging
import requests
from pathlib import Path
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.models import WeatherModelSettings
from gribmagic.unity.modules.download.local_store import bunzip_store, store, tarfile_store
from gribmagic.unity.modules.config.constants import KEY_LOCAL_FILE_PATHS, \
    KEY_REMOTE_FILE_PATHS, KEY_COMPRESSION, KEY_REMOTE_SERVER_TYPE

session = requests.Session()
logger = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_PARALLEL_PROCESSES = 4


def download(
        weather_model: WeatherModels,
        model_file_lists: Dict[str, List[Path]],
        parallel_download: bool = False,
        n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES
) -> None:
    """
        download weather forecasts
    """

    model = WeatherModelSettings(weather_model)

    if model.info[KEY_COMPRESSION] == "tar":
        __download_tar_file(weather_model,
                            model_file_lists[KEY_REMOTE_FILE_PATHS][0],
                            model_file_lists[KEY_LOCAL_FILE_PATHS])
        return

    if parallel_download:
        download_specifications = \
            [(weather_model, local_file_path, remote_file)
             for remote_file, local_file_path in
             zip(model_file_lists[KEY_REMOTE_FILE_PATHS],
                 model_file_lists[KEY_LOCAL_FILE_PATHS])]
        __download_parallel(download_specifications, n_processes)
    else:
        for remote_file, local_file_path in zip(model_file_lists[KEY_REMOTE_FILE_PATHS],
                                                model_file_lists[KEY_LOCAL_FILE_PATHS]):
            __download((weather_model, local_file_path, remote_file))


def __download(
        download_specification: Tuple[WeatherModels, Path, Path]
) -> None:
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
    url = f"{model.info[KEY_REMOTE_SERVER_TYPE]}:" \
          f"//{download_specification[2]}"
    target_file = download_specification[1]

    if target_file.exists():
        return

    logger.info(f"Downloading {url} to {target_file}")

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
    except Exception as ex:
        logger.warning(f"Access failed: {ex}")
        return

    if not target_file.parent.is_dir():
        target_file.parent.mkdir()

    if model.info[KEY_COMPRESSION] == 'bz2':
        bunzip_store(response.raw, target_file)
    else:
        store(response.raw, target_file)


def __download_parallel(
        download_specifications: List[Tuple[WeatherModels, Path, Path]],
        n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES) -> None:
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
        executor.map(__download, download_specifications)

    executor.shutdown(wait=True)


def __download_tar_file(
        weather_model: WeatherModels,
        remote_file: Path,
        local_file_list: List[Path]
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

    url = f"{model.info[KEY_REMOTE_SERVER_TYPE]}:" \
          f"//{remote_file}"

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
    except Exception as ex:
        logger.warning(f"Access failed: {ex}")
        return

    tarfile_store(response.raw, local_file_list)
