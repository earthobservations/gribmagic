""" Create lists of remote and local files """
from pathlib import Path
from typing import Dict, List, Union

from gribmagic.unity.models import AcquisitionRecipe
from gribmagic.unity.modules.config.constants import (
    KEY_LOCAL_FILE_PATHS,
    KEY_LOCAL_STORE_FILE_PATHS,
    KEY_REMOTE_FILE_PATHS,
)
from gribmagic.unity.modules.file_list_handling.local_file_list_creation import (
    build_local_file_list,
    build_local_store_file_list_for_variables,
)
from gribmagic.unity.modules.file_list_handling.remote_file_list_creation import (
    build_remote_file_list,
)


def build_model_file_lists(
    recipe: AcquisitionRecipe,
) -> Dict[str, List[Union[str, Path]]]:
    """
    Build a dictionary with local and remote file paths for the given model.

    Returns:
        Dictionary with lists for
            - local storing
            - intermediate local store
            - remote file path for downloading

    """

    return {
        KEY_LOCAL_STORE_FILE_PATHS: build_local_store_file_list_for_variables(recipe),
        KEY_LOCAL_FILE_PATHS: build_local_file_list(recipe),
        KEY_REMOTE_FILE_PATHS: build_remote_file_list(recipe),
    }
