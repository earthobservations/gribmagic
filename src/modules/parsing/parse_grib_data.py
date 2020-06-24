""" parses grib files """
from typing import Dict, List
from pathlib import Path
import xarray

from src.enumerations.unified_forecast_variables import ForecastVariables
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS


def concatenate_all_variable_files(
        model_file_list: Dict[str, List[Path]],
        variable: ForecastVariables) -> xarray.Dataset:
    """
    concatenate all files for one variable into one
    Args:
        model_file_list: Dict with file lists
        variable:

    Returns:
        Dataset for ForecastVariables along all Forecast Horizons
    """
    variable_file_list = \
        [file for file in model_file_list[KEY_LOCAL_FILE_PATHS] if variable.value in str(file)]
    return xarray.open_mfdataset(variable_file_list, engine='cfgrib')
