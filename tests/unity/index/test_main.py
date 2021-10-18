from pathlib import Path
from unittest.mock import patch

from gribmagic.unity.configuration.constants import (
    KEY_FILE_POSTFIX,
    KEY_FORECAST_STEPS,
    KEY_INITIALIZATION_DATE_FORMAT,
    KEY_URL_BASE,
    KEY_URL_FILE,
    KEY_URL_PATH,
    KEY_VARIABLES,
)
from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.index import make_fileindex
from tests.unity.fixtures import recipe_icon


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {
        WeatherModel.DWD_ICON_EU.value: {
            KEY_URL_BASE: "http://foobar.example.org",
            KEY_URL_PATH: "test_remote_dir/{initialization_time}/{variable_name_lower}",
            KEY_URL_FILE: "test_remote_file_{level_type}_{initialization_date}{initialization_time}_"
            "{forecast_step}_{variable_name_upper}.grib2.bz2",
            KEY_VARIABLES: ["air_temperature_2m"],
            KEY_FORECAST_STEPS: {0: [0, 1]},
            KEY_INITIALIZATION_DATE_FORMAT: "%Y%m%d",
            KEY_FILE_POSTFIX: "grib",
        }
    },
)
def test_make_fileindex():
    to_test = make_fileindex(recipe_icon)
    assert to_test == {
        "local_file_paths": [
            Path("/app/data/dwd-icon-eu_20200610_00_air_temperature_2m_000.grib"),
            Path("/app/data/dwd-icon-eu_20200610_00_air_temperature_2m_001.grib"),
        ],
        "remote_file_paths": [
            "http://foobar.example.org/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_000_T_2M.grib2.bz2",
            "http://foobar.example.org/test_remote_dir/00/t_2m/test_remote_file_single-level_2020061000_001_T_2M.grib2.bz2",
        ],
        "local_store_file_paths": [
            Path("/app/data/dwd-icon-eu/20200610_00/air_temperature_2m.nc")
        ],
    }
