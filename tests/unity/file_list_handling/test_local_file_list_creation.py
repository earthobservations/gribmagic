from gribmagic.unity.modules.file_list_handling.local_file_list_creation import \
    build_local_file_list, build_local_store_file_list_for_variables, \
    _local_file_paths_for_harmonie
from unittest.mock import patch
from gribmagic.unity.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path
from gribmagic.unity.modules.config.constants import KEY_VARIABLES, KEY_GRIB_PACKAGE_TYPES, KEY_FORECAST_STEPS, \
    KEY_FILE_POSTFIX, KEY_URL_FILE


@patch(
    'gribmagic.unity.models.MODEL_CONFIG',
    {
        WeatherModels.DWD_ICON_EU.value:
            {
                KEY_URL_FILE: "icon-eu_europe_regular-lat-lon_{level_type}_{initialization_date}"
                              "{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2",
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_POSTFIX: 'grib',
            }
    }
)
def test_build_local_file_list_for_variables():
    to_test = build_local_file_list(WeatherModels.DWD_ICON_EU,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/dwd-icon-eu_20200610_00_air_temperature_2m_000.grib'),
                       Path('/app/data/dwd-icon-eu_20200610_00_air_temperature_2m_001.grib')]


@patch(
    'gribmagic.unity.models.MODEL_CONFIG',
    {
        WeatherModels.DWD_ICON_EU.value: {
            KEY_URL_FILE: "icon-eu_europe_regular-lat-lon_{level_type}_{initialization_date}"
                          "{initialization_time}_{forecast_step}_{variable_name_upper}.grib2.bz2",
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_FILE_POSTFIX: 'grib',
        }
    }
)
def test_build_local_store_file_list_for_variables():
    to_test = build_local_store_file_list_for_variables(WeatherModels.DWD_ICON_EU,
                                                        0,
                                                        datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/dwd-icon-eu/20200610_00/air_temperature_2m.nc')]


@patch(
    'gribmagic.unity.models.MODEL_CONFIG',
    {
        WeatherModels.METEO_FRANCE_AROME.value: {
            KEY_URL_FILE: "package={grib_package_type}&time={forecast_step}H&"
                          "referencetime={initialization_date}T{initialization_time}:00:00Z&format=grib2",
            KEY_VARIABLES: ['air_temperature_2m'],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_GRIB_PACKAGE_TYPES: ['Package1'],
            KEY_FILE_POSTFIX: 'grib',
        }
    }
)
def test_build_local_file_list_for_variables_grib_package():
    to_test = build_local_file_list(WeatherModels.METEO_FRANCE_AROME,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/meteo-france-arome_20200610_00_Package1_000.grib'),
                       Path('/app/data/meteo-france-arome_20200610_00_Package1_001.grib')]


@patch(
    'gribmagic.unity.models.MODEL_CONFIG',
    {
        WeatherModels.KNMI_HARMONIE.value:
            {
                KEY_URL_FILE: "harm40_{grib_package_type}_{initialization_time}.tar",
                KEY_VARIABLES: ['air_temperature_2m'],
                KEY_FORECAST_STEPS: {0: [0, 1]},
                KEY_FILE_POSTFIX: 'grib',
                KEY_GRIB_PACKAGE_TYPES: ['v1_p3']

            }
    }
)
def test_build_local_file_list_for_harmonie():
    to_test = build_local_file_list(WeatherModels.KNMI_HARMONIE,
                                    0,
                                    datetime(2020, 6, 10).date())
    assert to_test == [Path('/app/data/knmi-harmonie_20200610_00_0.grib'),
                       Path('/app/data/knmi-harmonie_20200610_00_1.grib')]


def test_local_file_paths_for_harmonie():
    to_test = _local_file_paths_for_harmonie(
        datetime(2020, 6, 10).date(),
        0,
        {
                    KEY_URL_FILE: "harm40_{grib_package_type}_{initialization_time}.tar",
                    KEY_VARIABLES: ['air_temperature_2m'],
                    KEY_FORECAST_STEPS: {0: [0, 1]},
                    KEY_FILE_POSTFIX: 'grib',
                    KEY_GRIB_PACKAGE_TYPES: ['v1_p3']
        }
    )

    assert to_test == [Path('/app/data/knmi-harmonie_20200610_00_0.grib'),
                       Path('/app/data/knmi-harmonie_20200610_00_1.grib')]
