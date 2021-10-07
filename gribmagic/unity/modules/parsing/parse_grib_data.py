""" parses grib files """
from pathlib import Path
from typing import Dict, Hashable, List, Union

import cfgrib
import xarray

from gribmagic.unity.enumerations.unified_forecast_variables import ForecastVariables
from gribmagic.unity.modules.config.constants import (
    KEY_LEVEL_TYPE,
    KEY_LIST_INDEX,
    KEY_LOCAL_FILE_PATHS,
)

NOT_RELEVANT_ATTRIBUTES = [
    "time",
    "latitude",
    "longitude",
    "valid_time",
    "atmosphere",
    "step",
    "heightAboveGround",
    "isobaricInPa",
    "isobaricInPa",
    "heightAboveSea",
    "sigmaLayer",
    "isothermZero",
    "potentialVorticity",
    "nominalTop",
    "sigmaLayer",
    "surface",
    "pressureFromGroundLayer",
    "tropopause",
    "level",
    "maxWind",
    "sigma",
    "entireAtmosphere",
    "isobaricInhPa",
]


def concatenate_all_variable_files(
    model_file_list: Dict[str, List[Path]], variable: ForecastVariables
) -> xarray.Dataset:
    """
    concatenate all files for one variable into one
    Args:
        model_file_list: Dict with file lists
        variable:

    Returns:
        Dataset for ForecastVariables along all Forecast Horizons
    """
    variable_file_list = [
        file
        for file in model_file_list[KEY_LOCAL_FILE_PATHS]
        if variable.value in str(file)
    ]
    return xarray.open_mfdataset(
        variable_file_list, engine="cfgrib", combine="by_coords"
    )


def open_grib_file(file_path: Path) -> List[xarray.Dataset]:
    """
        Wrapper to open all variables available in grib file
    Args:
        file_path: Path to grib file

    Returns:
        In case of a multiple variables files a List of xarray.DataSets
        will be returned

    """
    return cfgrib.open_datasets(file_path)


def create_inventory(
    dataset: List[xarray.Dataset],
) -> Dict[
    Hashable, List[Union[Dict[str, Union[int, any]], Dict[str, Union[str, int]]]]
]:
    """
    Create a dictionary mapping GRIB variables to level_type and index in the list.
    Args:
        dataset:

    Returns:
        Dict with Level und Index information
    """
    variables_inventory = {}
    for idx, dat in enumerate(dataset):
        for item in dat.variables.items():
            varname, xelement = item
            if varname not in NOT_RELEVANT_ATTRIBUTES:
                variables_inventory.setdefault(varname, [])
                inventory_info = {
                    KEY_LEVEL_TYPE: dat[varname].attrs["GRIB_typeOfLevel"],
                    KEY_LIST_INDEX: idx,
                }
                variables_inventory[varname].append(inventory_info)
    return variables_inventory
