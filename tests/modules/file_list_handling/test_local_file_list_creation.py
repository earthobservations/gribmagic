from src.modules.file_list_handling.local_file_list_creation import \
    build_local_file_list, build_local_store_file_list_for_variables
from unittest.mock import patch, MagicMock
from src.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path
import pytest
from src.exceptions.grib_package_exception import GribPackageException
from src.modules.config.constants import KEY_VARIABLES, KEY_GRIB_PACKAGE_TYPES, KEY_FORECAST_STEPS


@patch(
    'src.modules.file_list_handling.local_file_list_creation.MODEL_CONFIG',
    {
        WeatherModels.ICON_EU.value:
            {
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]}
            }}
)
def test_build_local_file_list_for_variables():
    to_test = build_local_file_list(WeatherModels.ICON_EU,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/tmp/icon_eu_20200610_00_air_temperature_2m_0.grib'),
                       Path('/app/data/tmp/icon_eu_20200610_00_air_temperature_2m_1.grib')]


@patch(
    'src.modules.file_list_handling.local_file_list_creation.MODEL_CONFIG',
    {
        WeatherModels.ICON_EU.value: {
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [0, 1]}
        }}
)
def test_build_local_store_file_list_for_variables():
    to_test = build_local_store_file_list_for_variables(WeatherModels.ICON_EU,
                                                        0,
                                                        datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/icon_eu/20200610_00/air_temperature_2m.nc')]


@patch(
    'src.modules.file_list_handling.local_file_list_creation.MODEL_CONFIG',
    {
        WeatherModels.ICON_EU.value: {
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [1, 2]},
            KEY_GRIB_PACKAGE_TYPES: ['Package1']
        }}
)
def test_build_local_file_list_for_variables_not_grib_package():
    with pytest.raises(GribPackageException) as exc:
        _ = build_local_file_list(WeatherModels.ICON_EU,
                                  0,
                                  datetime(2020, 6, 10).date())
    assert str(exc.value) == f"You have set grib_packages flag True, but " \
                             f"{WeatherModels.ICON_EU.value} does not provide grib data in packages"


@patch(
    'src.modules.file_list_handling.local_file_list_creation.MODEL_CONFIG',
    {
        WeatherModels.AROME_METEO_FRANCE.value: {
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_GRIB_PACKAGE_TYPES: ['Package1']
        }}
)
def test_build_local_file_list_for_variables_grib_package():
    to_test = build_local_file_list(WeatherModels.AROME_METEO_FRANCE,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/tmp/arome_meteo_france_20200610_00_Package1_0.grib'),
                       Path('/app/data/tmp/arome_meteo_france_20200610_00_Package1_1.grib')]
