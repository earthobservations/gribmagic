""" Create remote lists of remote files that should be downloaded """
from typing import List

from gribmagic.unity.exceptions.wrong_weather_model_exception import (
    WrongWeatherModelException,
)
from gribmagic.unity.models import AcquisitionRecipe, WeatherModelSettings
from gribmagic.unity.modules.config.constants import (
    KEY_FORECAST_STEPS,
    KEY_FORECAST_STEPS_STR_LEN,
    KEY_INITIALIZATION_DATE_FORMAT,
    KEY_URL_BASE,
    KEY_URL_FILE,
    KEY_URL_PATH,
)


def build_remote_file_list(recipe: AcquisitionRecipe) -> List[str]:
    """
    Select the right `remote_file_path` generation function.

    Returns:
        List of remote file paths
    """
    model = WeatherModelSettings(recipe.model)
    if model.has_grib_packages:
        return remote_files_grib_packages(recipe)
    else:
        return remote_files_grib_directories(recipe)


def remote_files_grib_directories(recipe: AcquisitionRecipe) -> List[str]:
    """
    Generic file path generator for remote GRIB files within different directories.

    Returns:
        List of remote file paths
    """

    model = WeatherModelSettings(recipe.model)

    # Sanity checks
    if model.has_grib_packages:
        raise WrongWeatherModelException(
            "Weather model does not offer grib data directories"
        )

    baseurl = model.info[KEY_URL_BASE]
    remote_file_list = []
    for variable in model.variables:
        for forecast_step in model.info[KEY_FORECAST_STEPS][recipe.run_hour]:
            url_template = urljoin(
                baseurl, model.info[KEY_URL_PATH], model.info[KEY_URL_FILE]
            )
            tplvars = dict(
                level_type=model.level(variable),
                initialization_date=recipe.run_date.strftime(
                    model.info[KEY_INITIALIZATION_DATE_FORMAT]
                ),
                initialization_time=str(recipe.run_hour).zfill(2),
                forecast_step=str(forecast_step).zfill(3),
                variable_name_upper=model.variable(variable).upper(),
                variable_name_lower=model.variable(variable),
            )
            url = url_template.format(**tplvars)
            remote_file_list.append(url)
    return remote_file_list


def remote_files_grib_packages(recipe: AcquisitionRecipe) -> List[str]:
    """
    Generic file path generator for remote GRIB files within one or more GRIB data package(s).

    Returns:
        List of remote file paths
    """

    model = WeatherModelSettings(recipe.model)

    # Sanity checks
    if not model.has_grib_packages:
        raise WrongWeatherModelException(
            "Weather model does not offer grib data packages"
        )

    model_config = model.info

    baseurl = model.info[KEY_URL_BASE]
    remote_file_list = []
    for grib_package in model.grib_packages:
        if "{forecast_step}" in model_config[KEY_URL_FILE]:
            for forecast_step in model_config[KEY_FORECAST_STEPS][recipe.run_hour]:
                url_template = urljoin(
                    baseurl, model.info[KEY_URL_PATH], model.info[KEY_URL_FILE]
                )
                tplvars = dict(
                    grib_package_type=grib_package,
                    initialization_date=recipe.run_date.strftime(
                        model_config[KEY_INITIALIZATION_DATE_FORMAT]
                    ),
                    initialization_time=str(recipe.run_hour).zfill(2),
                    forecast_step=str(forecast_step).zfill(
                        model_config[KEY_FORECAST_STEPS_STR_LEN]
                    ),
                )
                url = url_template.format(**tplvars)
                remote_file_list.append(url)
        else:
            # This code path probably has been used for KNMI Harmonie.
            # However, raw files are only available via API these days.
            url_template = urljoin(
                baseurl, model.info[KEY_URL_PATH], model.info[KEY_URL_FILE]
            )
            tplvars = dict(
                initialization_date=recipe.run_date.strftime(
                    model_config[KEY_INITIALIZATION_DATE_FORMAT]
                ),
                initialization_time=str(recipe.run_hour).zfill(2),
            )
            url = url_template.format(**tplvars)
            remote_file_list.append(url)
    return remote_file_list


def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.

    https://stackoverflow.com/a/11326230
    """
    # Filter out empty URL fragments.
    args = [x for x in args if x]
    return "/".join(map(lambda x: str(x).rstrip("/"), args))
