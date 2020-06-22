"""
handle download of nwp from remote servers
"""
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from io import BytesIO
from typing import Dict, List


from src.enumerations.weather_models import WeatherModels
from src.modules.download.local_store import bunzip_store, store
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS, KEY_REMOTE_FILE_PATHS, KEY_COMPRESSION, KEY_REMOTE_SERVER_TYPE
from src.modules.config.configurations import MODEL_CONFIG


def download(
        weather_model: WeatherModels,
        model_file_lists: Dict[str, List[Path]]
) -> None:
    """
        Basic download function
    """
    for remote_file, local_file_path in zip(model_file_lists[KEY_REMOTE_FILE_PATHS],
                                            model_file_lists[KEY_LOCAL_FILE_PATHS]):
        
        downloaded_file = urlopen(f"{MODEL_CONFIG[weather_model.value][KEY_REMOTE_SERVER_TYPE]}://{remote_file}")
        
        if not local_file_path.parent.is_dir(): local_file_path.parent.mkdir()
        
        if MODEL_CONFIG[weather_model.value][KEY_COMPRESSION] == 'bz2':
            bunzip_store(BytesIO(downloaded_file.read()), local_file_path)
        else:
            store(downloaded_file, local_file_path)
