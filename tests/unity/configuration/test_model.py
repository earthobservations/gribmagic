import logging
import re
from copy import deepcopy
from unittest.mock import patch

import pytest

from gribmagic.unity.configuration import MODEL_CONFIG
from gribmagic.unity.configuration.constants import KEY_VARIABLES
from gribmagic.unity.configuration.model import WeatherModelSettings
from gribmagic.unity.enumerations import WeatherModel

model_config_blacklist = deepcopy(MODEL_CONFIG[WeatherModel.DWD_ICON_EU.value])
model_config_blacklist.update(
    {KEY_VARIABLES: ["temperature", "wind_u", "wind_v", "relative_humidity"]}
)


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {WeatherModel.DWD_ICON_EU.value: model_config_blacklist},
)
def test_model_dwd_blacklist(caplog):
    model = WeatherModelSettings(WeatherModel.DWD_ICON_EU)

    with caplog.at_level(logging.DEBUG):
        assert model.variables == []

    assert "DWD ICON: Parameter 'temperature' (model-level) not implemented yet" in caplog.messages
    assert "DWD ICON: Parameter 'wind_u' (model-level) not implemented yet" in caplog.messages
    assert "DWD ICON: Parameter 'wind_v' (model-level) not implemented yet" in caplog.messages
    assert (
        "DWD ICON: Parameter 'relative_humidity' (pressure-level) not implemented yet"
        in caplog.messages
    )


def test_model_no_configuration():

    with pytest.raises(KeyError) as ex:
        model = WeatherModelSettings(WeatherModel.UNKNOWN)

    assert ex.match(re.escape("Model WeatherModel.UNKNOWN has no configuration"))


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {"unknown": MODEL_CONFIG[WeatherModel.DWD_ICON_EU.value]},
)
def test_model_variables_mapping_missing():

    model = WeatherModelSettings(WeatherModel.UNKNOWN)

    with pytest.raises(KeyError) as ex:
        model.variable("foobar")

    assert ex.match(re.escape("WeatherModel.UNKNOWN has no variable mapping"))


def test_model_variable_not_mapped():
    model = WeatherModelSettings(WeatherModel.DWD_ICON_EU)

    with pytest.raises(KeyError) as ex:
        model.variable("foobar")

    assert ex.match(re.escape("WeatherModel.DWD_ICON_EU lacks variable mapping for 'foobar'"))


@patch(
    "gribmagic.unity.configuration.model.MODEL_CONFIG",
    {"unknown": MODEL_CONFIG[WeatherModel.DWD_ICON_EU.value]},
)
def test_model_levels_mapping_missing():

    model = WeatherModelSettings(WeatherModel.UNKNOWN)

    with pytest.raises(KeyError) as ex:
        model.level("bazqux")

    assert ex.match(re.escape("WeatherModel.UNKNOWN has no variable->level mapping"))


def test_model_level_not_mapped():
    model = WeatherModelSettings(WeatherModel.DWD_ICON_EU)

    with pytest.raises(KeyError) as ex:
        model.level("bazqux")

    assert ex.match(
        re.escape("WeatherModel.DWD_ICON_EU lacks variable->level mapping for 'bazqux'")
    )
