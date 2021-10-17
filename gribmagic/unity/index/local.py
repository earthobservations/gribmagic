""" Create lists of files to download into local filesystem """
from pathlib import Path
from typing import Dict, List

from gribmagic.unity.configuration.constants import (
    KEY_FILE_POSTFIX,
    KEY_FORECAST_STEPS,
    KEY_GRIB_PACKAGE_TYPES,
    KEY_URL_FILE,
    LOCAL_FILE_POSTFIX,
)
from gribmagic.unity.configuration.model import WeatherModelSettings
from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.model import AcquisitionRecipe


def build_local_store_file_list_for_variables(recipe: AcquisitionRecipe) -> List[Path]:
    """
    Generic file path generator for persisting local netCDF files.

    Returns:
        List of local store file paths

    """
    model = WeatherModelSettings(recipe.model)
    local_file_list = []
    for variable in model.variables:
        local_file_list.append(
            Path(
                recipe.target,
                recipe.model.value,
                f"{recipe.run_date.strftime('%Y%m%d')}_{str(recipe.run_hour).zfill(2)}",
                f"{variable}.{LOCAL_FILE_POSTFIX}",
            )
        )
    return local_file_list


def build_local_file_list(recipe: AcquisitionRecipe) -> List[Path]:
    """
    Generic file path generator for downloaded GRIB data per each variable.

    Returns:
        List of temporary locally stored files

    """
    model = WeatherModelSettings(recipe.model)

    if recipe.model == WeatherModel.KNMI_HARMONIE:
        return _local_file_paths_for_harmonie(recipe, model.info)
    elif model.has_grib_packages:
        variables_iterator = model.info[KEY_GRIB_PACKAGE_TYPES]
    else:
        variables_iterator = model.variables

    return _build_local_file_list_with_variables_iterator(recipe, variables_iterator, model.info)


def _build_local_file_list_with_variables_iterator(
    recipe: AcquisitionRecipe,
    variables_iterator: List[str],
    model_config,
) -> List[Path]:
    local_file_list = []
    for var in variables_iterator:
        if "{forecast_step}" in model_config[KEY_URL_FILE]:
            for forecast_step in model_config[KEY_FORECAST_STEPS][recipe.run_hour]:
                local_file_list.append(
                    Path(
                        recipe.target,
                        f"{recipe.model.value}_{recipe.run_date.strftime('%Y%m%d')}_"
                        f"{str(recipe.run_hour).zfill(2)}_{var}_"
                        f"{str(forecast_step).zfill(3)}.{model_config[KEY_FILE_POSTFIX]}",
                    )
                )
        else:
            # This code path probably has been used for KNMI Harmonie.
            # However, raw files are only available via API these days.
            local_file_list.append(
                Path(
                    recipe.target,
                    f"{recipe.model.value}_{recipe.run_date.strftime('%Y%m%d')}_"
                    f"{str(recipe.run_hour).zfill(2)}_{var}."
                    f"{model_config[KEY_FILE_POSTFIX]}",
                )
            )
    return local_file_list


def _local_file_paths_for_harmonie(
    recipe: AcquisitionRecipe, model_config: Dict[str, any]
) -> List[Path]:
    """
    Local file path generator for HARMONIE model.
    """
    local_file_list = []
    for forecast_step in model_config[KEY_FORECAST_STEPS][recipe.run_hour]:
        local_file_list.append(
            Path(
                recipe.target,
                f"{WeatherModel.KNMI_HARMONIE.value}_{recipe.run_date.strftime('%Y%m%d')}_"
                f"{str(recipe.run_hour).zfill(2)}_{forecast_step}."
                f"{model_config[KEY_FILE_POSTFIX]}",
            )
        )
    return local_file_list
