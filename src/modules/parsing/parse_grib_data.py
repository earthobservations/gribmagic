""" parses grib files """
from pathlib import Path
from typing import Dict, List, Union, Hashable

import cfgrib
import xarray

from src.enumerations.unified_forecast_variables import ForecastVariables
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS, \
    KEY_LEVEL_TYPE, KEY_LIST_INDEX

NOT_RELEVANT_ATTRIBUTES = ['time', 'latitude', 'longitude', 'valid_time',
                           'atmosphere', 'step', 'heightAboveGround',
                           'isobaricInPa', 'isobaricInPa', 'heightAboveSea',
                           'sigmaLayer', 'isothermZero', 'potentialVorticity',
                           'nominalTop', 'sigmaLayer', 'surface',
                           'pressureFromGroundLayer', 'tropopause', 'level',
                           'maxWind', 'sigma', 'entireAtmosphere',
                           'isobaricInhPa']


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
        [file for file in model_file_list[KEY_LOCAL_FILE_PATHS] if
         variable.value in str(file)]
    return xarray.open_mfdataset(variable_file_list, engine='cfgrib', combine='by_coords')


def open_grib_file(
        file_path: Path
) -> List[xarray.Dataset]:
    """
        Wrapper to open all variables available in grib file
    Args:
        file_path: Path to grib file

    Returns:
        In case of a multiple variables files a List of xarray.DataSets
        will be returned

    """
    return cfgrib.open_datasets(file_path)


def extract_variables_per_dataset_in_list(
        data: List[xarray.Dataset]
) -> Dict[Hashable, List[
    Union[Dict[str, Union[int, any]], Dict[str, Union[str, int]]]]]:
    """
    Creates a dictionary with the mapping of grib variables to
        level_type and place in the list
    Args:
        data:

    Returns:
        Dict with Level und Index information
    """
    variables_inventory = {}
    for idx, dat in enumerate(data):
        for item in dat.variables.items():
            if item[0] not in NOT_RELEVANT_ATTRIBUTES:
                try:
                    inventory_info = {
                        KEY_LEVEL_TYPE: dat[item[0]].attrs['GRIB_typeOfLevel'],
                        KEY_LIST_INDEX: idx}
                except KeyError:
                    inventory_info = {KEY_LEVEL_TYPE: '',
                                      KEY_LIST_INDEX: idx}
                if item[0] in variables_inventory.keys():
                    variables_inventory[item[0]].append(inventory_info)
                else:
                    variables_inventory[item[0]] = [inventory_info]
    return variables_inventory
