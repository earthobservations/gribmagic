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

# import cfgrib
#
# data = cfgrib.open_datasets('')
#
# variables_inventory = {}
# for idx, dat in enumerate(data):
#     for item in dat.variables.items():
#         if item[0] not in ['time', 'latitude', 'longitude', 'valid_time', 'atmosphere', 'step', 'heightAboveGround','isobaricInPa', 'isobaricInPa', 'heightAboveSea', 'hybrid', 'isothermZero',  'potentialVorticity', 'nominalTop', 'sigmaLayer','surface',   'pressureFromGroundLayer',  'tropopause','level',   'maxWind',   'sigma']:
#             try:
#                 inventory_info = {'level_type': dat[item[0]].attrs['GRIB_typeOfLevel'],
#                                                     'list_index': idx}
#             except KeyError:
#                 inventory_info = {'level_type': '',
#                                   'list_index': idx}
#             if item[0] in variables_inventory.keys():
#                 variables_inventory[item[0]].append(inventory_info)
#             else:
#                 variables_inventory[item[0]] = [inventory_info]