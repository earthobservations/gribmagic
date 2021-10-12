from unittest.mock import patch

import pytest

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.exceptions.wrong_weather_model_exception import (
    WrongWeatherModelException,
)
from gribmagic.unity.modules.config.constants import (
    KEY_FORECAST_STEPS,
    KEY_FORECAST_STEPS_STR_LEN,
    KEY_GRIB_PACKAGE_TYPES,
    KEY_INITIALIZATION_DATE_FORMAT,
    KEY_URL_BASE,
    KEY_URL_FILE,
    KEY_URL_PATH,
    KEY_VARIABLES,
)
from gribmagic.unity.modules.file_list_handling.remote_file_list_creation import (
    build_remote_file_list,
    remote_files_grib_directories,
    remote_files_grib_packages,
)
from tests.unity.fixtures import recipe_arome, recipe_icon


@patch(
    "gribmagic.unity.models.MODEL_CONFIG",
    {
        WeatherModels.DWD_ICON_EU.value: {
            KEY_URL_BASE: "http://foobar.example.org",
            KEY_URL_PATH: "test_remote_dir/{initialization_time}/{variable_name_lower}",
            KEY_URL_FILE: "test_remote_file_{level_type}_{initialization_date}{initialization_time}_"
            "{forecast_step}_{variable_name_upper}.grib2.bz2",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_INITIALIZATION_DATE_FORMAT: "%Y%m%d",
        }
    },
)
def test_build_remote_model_file_lists():
    to_test = remote_files_grib_directories(recipe_icon)
    assert to_test == [
        "http://foobar.example.org/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_000_T_2M.grib2.bz2",
        "http://foobar.example.org/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_001_T_2M.grib2.bz2",
    ]


def test_build_remote_model_file_lists_wrong_weather_model():
    with pytest.raises(WrongWeatherModelException) as exc:
        _ = remote_files_grib_directories(recipe_arome)
    assert str(exc.value) == "Weather model does not offer grib data directories"


@patch(
    "gribmagic.unity.models.MODEL_CONFIG",
    {
        WeatherModels.METEO_FRANCE_AROME.value: {
            KEY_URL_BASE: "http://foobar.example.org",
            KEY_URL_PATH: "",
            KEY_URL_FILE: "test_remote_file_{initialization_date}{initialization_time}_"
            "{forecast_step}_{grib_package_type}.grib2.bz2",
            KEY_INITIALIZATION_DATE_FORMAT: "%Y%m%d",
            KEY_GRIB_PACKAGE_TYPES: ["Package1"],
            KEY_FORECAST_STEPS_STR_LEN: 2,
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
        }
    },
)
def test_build_remote_model_file_lists_for_package():
    to_test = remote_files_grib_packages(recipe_arome)
    assert to_test == [
        "http://foobar.example.org/test_remote_file_2020061000_00_Package1.grib2.bz2",
        "http://foobar.example.org/test_remote_file_2020061000_01_Package1.grib2.bz2",
    ]


@patch(
    "gribmagic.unity.models.MODEL_CONFIG",
    {
        WeatherModels.METEO_FRANCE_AROME.value: {
            KEY_URL_BASE: "http://foobar.example.org",
            KEY_URL_PATH: "",
            KEY_URL_FILE: "test_remote_file_{initialization_date}{initialization_time}_"
            "{forecast_step}_{grib_package_type}.grib2.bz2",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_INITIALIZATION_DATE_FORMAT: "%Y%m%d",
            KEY_GRIB_PACKAGE_TYPES: ["Package1"],
            KEY_FORECAST_STEPS_STR_LEN: 2,
        }
    },
)
def test_build_remote_file_list():
    to_test = build_remote_file_list(recipe_arome)
    assert to_test == [
        "http://foobar.example.org/test_remote_file_2020061000_00_Package1.grib2.bz2",
        "http://foobar.example.org/test_remote_file_2020061000_01_Package1.grib2.bz2",
    ]


def test_build_remote_model_file_lists_for_package_wrong_model():
    with pytest.raises(WrongWeatherModelException) as excinfo:
        _ = remote_files_grib_packages(recipe_icon)
    assert str(excinfo.value) == "Weather model does not offer grib data packages"
