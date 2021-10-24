import dataclasses
import logging
from enum import Enum
from pathlib import Path
from typing import List

import appdirs

from gribmagic.util import run_command

logger = logging.getLogger(__name__)

GRID_METADATA_PATH = (
    Path(appdirs.user_data_dir("gribmagic", "earthobservations")) / "metadata" / "grid"
)


class GridKind(Enum):
    ICON_GLOBAL2WORLD_0125 = "ICON_GLOBAL2WORLD_0125"
    ICON_GLOBAL2WORLD_025 = "ICON_GLOBAL2WORLD_025"
    ICON_GLOBAL2EUAU_0125 = "ICON_GLOBAL2EUAU_0125"
    ICON_GLOBAL2EUAU_025 = "ICON_GLOBAL2EUAU_025"


@dataclasses.dataclass
class GridDescriptionWeight:
    kind: GridKind
    url: str
    resolution: float
    description: str
    weights: str

    def __post_init__(self):
        self.name = Path(self.url).name.replace(".tar.bz2", "")
        self.basedir = GRID_METADATA_PATH / self.name
        self.description_file = self.basedir / self.description
        self.weights_file = self.basedir / self.weights

    def install(self, force=False):
        """
        Ensure auxiliary data needed for regridding is present.
        """

        if not force and (self.weights_file.exists() and self.description_file.exists()):
            logger.info(f"Grid description and weight files for {self.name} already downloaded")
            return

        logger.info(f"Installing grid description and weight files {self.name} from {self.url}")

        run_command(f"""wget --continue --directory-prefix='{GRID_METADATA_PATH}' {self.url}""")

        run_command(
            f"""test ! -d '{self.basedir}' && tar -C '{GRID_METADATA_PATH}' -xjf '{self.basedir}.tar.bz2'"""
        )


@dataclasses.dataclass
class GridFile:
    """
    - http://icon-downloads.zmaw.de/dwd_grids.xml
    - https://code.mpimet.mpg.de/boards/1/topics/5490
    """

    kinds: List[GridKind]
    # Resolution in km
    resolution: int
    url: str
    identifier: str
    description: str

    def __post_init__(self):
        self.name = Path(self.url).name.replace(".bz2", "")
        self.basedir = GRID_METADATA_PATH
        self.gridfile = self.basedir / self.name

    def install(self, force=False):
        """
        Ensure auxiliary data needed for regridding is present.
        """

        if not force and (self.gridfile.exists()):
            logger.info(f"Grid information files for {self.name} already downloaded")
            return

        logger.info(f"Installing grid information files {self.name} from {self.url}")

        run_command(f"""wget --continue --directory-prefix='{GRID_METADATA_PATH}' {self.url}""")

        run_command(f"""test ! -f '{self.gridfile}' && bunzip2 '{self.gridfile}.bz2'""")


@dataclasses.dataclass
class GridInformation:
    description_weight: GridDescriptionWeight
    grid: GridFile
