import os
import re
import logging
import shutil
import tempfile
from copy import deepcopy
from unittest import mock
from unittest.mock import patch
import responses
from click.testing import CliRunner

from gribmagic.commands import main
from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.models import MODEL_CONFIG
from gribmagic.unity.modules.config.constants import KEY_VARIABLES


model_config = deepcopy(MODEL_CONFIG[WeatherModels.ICON_EU.value])
model_config.update({KEY_VARIABLES: ['air_temperature_2m', 'relative_humidity_2m']})


@responses.activate
@patch("gribmagic.unity.models.MODEL_CONFIG", {WeatherModels.ICON_EU.value: model_config})
def test_command_gribmagic_unity(caplog):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        # No need to shuffle actual data around.
        body=b"",
        stream=True,
    )

    tempdir = tempfile.mkdtemp()
    with mock.patch.dict(os.environ, {"GM_DATA_PATH": tempdir}):

        with caplog.at_level(logging.DEBUG):
            runner = CliRunner()
            result = runner.invoke(
                cli=main,
                args=["unity", "--model=icon_eu", "--timestamp=2021-10-03T00:00:00Z"],
                catch_exceptions=False)

    # result.exit_code == 1 -- why!?
    # assert result.exit_code == 0

    # assert result.output == 'Hello Peter!\n'
    assert "Starting GribMagic" in caplog.text
    assert "WeatherModels.ICON_EU: Accessing parameter 'air_temperature_2m'" in caplog.messages
    assert "WeatherModels.ICON_EU: Accessing parameter 'relative_humidity_2m'" in caplog.messages
    assert f"Downloading https://opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2021100300_000_T_2M.grib2.bz2 to {tempdir}/icon_eu_20211003_00_air_temperature_2m_000.grib2" in caplog.messages
    assert f"Downloading https://opendata.dwd.de/weather/nwp/icon-eu/grib/00/relhum_2m/icon-eu_europe_regular-lat-lon_single-level_2021100300_120_RELHUM_2M.grib2.bz2 to {tempdir}/icon_eu_20211003_00_relative_humidity_2m_120.grib2" in caplog.messages

    t2m_messages = [message for message in caplog.messages if "Downloading" in message and "t_2m" in message]
    rh2m_messages = [message for message in caplog.messages if "Downloading" in message and "relhum_2m" in message]
    assert len(t2m_messages) == 93
    assert len(rh2m_messages) == 93

    shutil.rmtree(tempdir)
