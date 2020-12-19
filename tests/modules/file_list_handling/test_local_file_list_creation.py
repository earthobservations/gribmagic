from gribmagic.modules.file_list_handling.local_file_list_creation import \
    build_local_file_list, build_local_store_file_list_for_variables, \
    _local_file_paths_for_harmonie
from unittest.mock import patch
from gribmagic.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path
import pytest
from gribmagic.exceptions.grib_package_exception import GribPackageException
from gribmagic.modules.config.constants import KEY_VARIABLES, KEY_GRIB_PACKAGE_TYPES, KEY_FORECAST_STEPS, \
    KEY_FILE_POSTFIX, KEY_FILE_TEMPLATE


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.ICON_EU.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_POSTFIX: 'grib',
                KEY_FILE_TEMPLATE: "icon-eu_europe_regular-lat-lon_{level_type}_{initialization_date}"
                                   "{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2"
            }}
)
def test_build_local_file_list_for_variables():
    to_test = build_local_file_list(WeatherModels.ICON_EU,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/tmp/icon_eu_20200610_00_air_temperature_2m_000.grib'),
                       Path('/app/data/tmp/icon_eu_20200610_00_air_temperature_2m_001.grib')]


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.ICON_EU.value: {
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_FILE_POSTFIX: 'grib',
            KEY_FILE_TEMPLATE: "icon-eu_europe_regular-lat-lon_{level_type}_{initialization_date}"
                               "{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2"
        }}
)
def test_build_local_store_file_list_for_variables():
    to_test = build_local_store_file_list_for_variables(WeatherModels.ICON_EU,
                                                        0,
                                                        datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/icon_eu/20200610_00/air_temperature_2m.nc')]


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.AROME_METEO_FRANCE.value: {
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_GRIB_PACKAGE_TYPES: ['Package1'],
            KEY_FILE_POSTFIX: 'grib',
            KEY_FILE_TEMPLATE: "package={grib_package_type}&time={forecast_step}H&referencetime"
                               "={initialization_date}T{initialization_time}:00:00Z&format=grib2"
        }}
)
def test_build_local_file_list_for_variables_grib_package():
    to_test = build_local_file_list(WeatherModels.AROME_METEO_FRANCE,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/tmp/arome_meteo_france_20200610_00_Package1_000.grib'),
                       Path('/app/data/tmp/arome_meteo_france_20200610_00_Package1_001.grib')]


@patch(
    'gribmagic.models.MODEL_CONFIG',
    {
        WeatherModels.HARMONIE_KNMI.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_POSTFIX: 'grib',
                KEY_FILE_TEMPLATE: "harm40_{grib_package_type}_{initialization_time}.tar",
                KEY_GRIB_PACKAGE_TYPES: ['v1_p3']

            }}
)
def test_build_local_file_list_for_harmonie():
    to_test = build_local_file_list(WeatherModels.HARMONIE_KNMI,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/tmp/harmonie_knmi_20200610_00_0.grib'),
                       Path('/app/data/tmp/harmonie_knmi_20200610_00_1.grib')]


def test__local_file_paths_for_harmonie():
    to_test = _local_file_paths_for_harmonie(
        datetime(2020, 6, 10).date(),
        0,
        {

                    KEY_VARIABLES: ['air_temperature_2m'],
                    KEY_FORECAST_STEPS: {0: [0, 1]},
                    KEY_FILE_POSTFIX: 'grib',
                    KEY_FILE_TEMPLATE: "harm40_{grib_package_type}_{initialization_time}.tar",
                    KEY_GRIB_PACKAGE_TYPES: ['v1_p3']}
    )

    assert to_test == [Path('/app/data/tmp/harmonie_knmi_20200610_00_0.grib'),
                       Path('/app/data/tmp/harmonie_knmi_20200610_00_1.grib')]
