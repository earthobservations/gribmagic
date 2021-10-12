import dataclasses
import logging
from datetime import datetime
from pathlib import Path

from cachetools import cachedmethod

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.modules.config.configurations import (
    MODEL_CONFIG,
    MODEL_VARIABLES_LEVELS_MAPPING,
    MODEL_VARIABLES_MAPPING,
)
from gribmagic.unity.modules.config.constants import (
    KEY_GRIB_PACKAGE_TYPES,
    KEY_VARIABLES,
)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class AcquisitionRecipe:

    # Define the weather model.
    model: WeatherModels

    # Timestamp of forecast run.
    timestamp: datetime

    # Destination directory.
    target: Path

    @property
    def run_date(self) -> datetime.date:
        """
        Date when forecast started.
        """
        return self.timestamp.date()

    @property
    def run_hour(self) -> int:
        """
        Time of the day when forecast started.
        """
        return self.timestamp.hour


class WeatherModelSettings:

    cache = {}

    def __init__(self, model: WeatherModels):
        self.model = model
        try:
            self.info = MODEL_CONFIG[self.model.value]
        except KeyError:
            raise KeyError(f"Model {self.model} has no configuration")
        self.variables_map = MODEL_VARIABLES_MAPPING.get(self.model.value)
        self.levels_map = MODEL_VARIABLES_LEVELS_MAPPING.get(self.model.value)

    @property
    def has_grib_packages(self):
        return KEY_GRIB_PACKAGE_TYPES in self.info

    @property
    def grib_packages(self):
        return self.info[KEY_GRIB_PACKAGE_TYPES]

    def variable(self, variable):
        if self.variables_map is None:
            raise KeyError(f"{self.model} has no variable mapping")
        if variable not in self.variables_map:
            raise KeyError(f"{self.model} lacks variable mapping for '{variable}'")
        return self.variables_map[variable]

    def level(self, variable):
        if self.levels_map is None:
            raise KeyError(f"{self.model} has no variable->level mapping")
        if variable not in self.levels_map:
            raise KeyError(
                f"{self.model} lacks variable->level mapping for '{variable}'"
            )
        return self.levels_map[variable]

    @property
    # Caching is problematic, because it will interfere with individual mocking when testing.
    # @cachedmethod(lambda self: self.cache)
    def variables(self):
        return list(self.generate_variables())

    def generate_variables(self):

        dwd_models = [
            WeatherModels.DWD_ICON_GLOBAL,
            WeatherModels.DWD_ICON_EU,
            WeatherModels.DWD_ICON_EU_EPS,
            WeatherModels.DWD_COSMO_D2,
            WeatherModels.DWD_COSMO_D2_EPS,
        ]
        dwd_blocklist = ["temperature", "wind_u", "wind_v", "relative_humidity"]

        for variable in self.info[KEY_VARIABLES]:
            logger.info(f"{self.model}: Accessing parameter '{variable}'")
            if self.model in dwd_models and variable in dwd_blocklist:
                variable_level = self.level(variable)
                logger.warning(
                    f"DWD ICON: Parameter '{variable}' ({variable_level}) not implemented yet"
                )
                continue
            yield variable
