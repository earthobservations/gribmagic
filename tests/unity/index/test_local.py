from pathlib import Path
from unittest.mock import patch

from gribmagic.unity.configuration.constants import (
    KEY_FILE_POSTFIX,
    KEY_FORECAST_STEPS,
    KEY_GRIB_PACKAGE_TYPES,
    KEY_URL_FILE,
    KEY_VARIABLES,
)
from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.index.local import (
    _local_file_paths_for_harmonie,
    build_local_file_list,
    build_local_store_file_list_for_variables,
)
from tests.unity.fixtures import recipe_arome, recipe_harmonie, recipe_icon


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {
        WeatherModel.DWD_ICON_EU.value: {
            KEY_URL_FILE: "icon-eu_europe_regular-lat-lon_{level_type}_{initialization_date}"
            "{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_FILE_POSTFIX: "grib",
        }
    },
)
def test_build_local_file_list_for_variables():
    to_test = build_local_file_list(recipe_icon)
    assert to_test == [
        Path("/app/data/dwd-icon-eu_20200610_00_air_temperature_2m_000.grib"),
        Path("/app/data/dwd-icon-eu_20200610_00_air_temperature_2m_001.grib"),
    ]


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {
        WeatherModel.DWD_ICON_EU.value: {
            KEY_URL_FILE: "icon-eu_europe_regular-lat-lon_{level_type}_{initialization_date}"
            "{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_FILE_POSTFIX: "grib",
        }
    },
)
def test_build_local_store_file_list_for_variables():
    to_test = build_local_store_file_list_for_variables(recipe_icon)
    assert to_test == [Path("/app/data/dwd-icon-eu/20200610_00/air_temperature_2m.nc")]


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {
        WeatherModel.METEO_FRANCE_AROME.value: {
            KEY_URL_FILE: "package={grib_package_type}&time={forecast_step}H&"
            "referencetime={initialization_date}T{initialization_time}:00:00Z&format=grib2",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_GRIB_PACKAGE_TYPES: ["Package1"],
            KEY_FILE_POSTFIX: "grib",
        }
    },
)
def test_build_local_file_list_for_variables_grib_package():
    to_test = build_local_file_list(recipe_arome)
    assert to_test == [
        Path("/app/data/meteo-france-arome_20200610_00_Package1_000.grib"),
        Path("/app/data/meteo-france-arome_20200610_00_Package1_001.grib"),
    ]


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {
        WeatherModel.KNMI_HARMONIE.value: {
            KEY_URL_FILE: "harm40_{grib_package_type}_{initialization_time}.tar",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_FILE_POSTFIX: "grib",
            KEY_GRIB_PACKAGE_TYPES: ["v1_p3"],
        }
    },
)
def test_build_local_file_list_for_harmonie():
    to_test = build_local_file_list(recipe_harmonie)
    assert to_test == [
        Path("/app/data/knmi-harmonie_20200610_00_0.grib"),
        Path("/app/data/knmi-harmonie_20200610_00_1.grib"),
    ]


def test_local_file_paths_for_harmonie():
    to_test = _local_file_paths_for_harmonie(
        recipe_harmonie,
        {
            KEY_URL_FILE: "harm40_{grib_package_type}_{initialization_time}.tar",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_FILE_POSTFIX: "grib",
            KEY_GRIB_PACKAGE_TYPES: ["v1_p3"],
        },
    )

    assert to_test == [
        Path("/app/data/knmi-harmonie_20200610_00_0.grib"),
        Path("/app/data/knmi-harmonie_20200610_00_1.grib"),
    ]
