import dataclasses
import logging
from datetime import datetime
from pathlib import Path

from gribmagic.unity.enumerations import WeatherModel

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class AcquisitionRecipe:

    # Define the weather model.
    model: WeatherModel

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


@dataclasses.dataclass
class DownloadItem:
    """
    The download specification.
    """

    model: WeatherModel
    local_file: Path
    remote_url: str
