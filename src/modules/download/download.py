"""
handle download of nwp from remote servers
"""
from pathlib import Path
from urllib.request import urlopen
from io import BytesIO
from typing import Dict, List, Tuple
from multiprocessing import Pool


from src.enumerations.weather_models import WeatherModels
from src.modules.download.local_store import bunzip_store, store, tarfile_store
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS, \
    KEY_REMOTE_FILE_PATHS, KEY_COMPRESSION, KEY_REMOTE_SERVER_TYPE
from src.modules.config.configurations import MODEL_CONFIG

DEFAULT_NUMBER_OF_PARALLEL_PROCESSES = 2


def download(
        weather_model: WeatherModels,
        model_file_lists: Dict[str, List[Path]],
        parallel_download: bool = False,
        n_processes: int = DEFAULT_NUMBER_OF_PARALLEL_PROCESSES
) -> None:
    """
        download weather forecasts
    """
    if weather_model == WeatherModels.HARMONIE_KNMI:
        __download_tar_file(weather_model,
                            model_file_lists[KEY_REMOTE_FILE_PATHS][0],
                            model_file_lists[KEY_LOCAL_FILE_PATHS])
        return None

    if parallel_download:
        download_specifications = \
            [(weather_model, local_file_path, remote_file)
             for remote_file, local_file_path in
             zip(model_file_lists[KEY_REMOTE_FILE_PATHS],
                 model_file_lists[KEY_LOCAL_FILE_PATHS])]
        __download_parallel(download_specifications, n_processes)
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
    weather_model = download_specification[0].value
    downloaded_file = urlopen(
        f"{MODEL_CONFIG[weather_model.value][KEY_REMOTE_SERVER_TYPE]}:"
        f"//{download_specification[2]}")

    if not download_specification[1].parent.is_dir(): download_specification[1].parent.mkdir()

    if MODEL_CONFIG[weather_model][KEY_COMPRESSION] == 'bz2':
        bunzip_store(BytesIO(downloaded_file.read()), download_specification[1])
    else:
        store(downloaded_file, download_specification[1])


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
    pool = Pool(processes=n_processes)
    pool.map(__download, download_specifications)


def __download_tar_file(
        weather_model: WeatherModels,
        remote_file: Path,
        local_file_list: List[Path]
) -> None:
    """

    Args:
        weather_model:
        remote_file:
        local_file_list:

    Returns:

    """
    downloaded_file = urlopen(
        f"{MODEL_CONFIG[weather_model.value][KEY_REMOTE_SERVER_TYPE]}:"
        f"//{remote_file}")
    tarfile_store(downloaded_file, local_file_list)
