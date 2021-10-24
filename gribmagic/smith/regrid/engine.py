import logging
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, List, Union

from cdo import Cdo
from numpy.distutils.misc_util import as_list

from gribmagic.smith.regrid.model import (
    GridDescriptionWeight,
    GridFile,
    GridInformation,
    GridKind,
    logger,
)
from gribmagic.smith.util import FileProcessor, ProcessingResult

logger = logging.getLogger(__name__)


class GridTransformationLibrary:
    """
    Die notwendigen Dateien zur Transformation von ICON-Daten vom nativen
    Dreiecksgitter in ein reguläres Lat/Lon-Gitter (Gitterinformationsdatei des
    globalen Modells ICON, die Gitterbeschreibungen und die berechneten
    Interpolationsgewichte):

        ICON_GLOBAL2WORLD_0125_EASY.tar.bz2
        ICON_GLOBAL2WORLD_025_EASY.tar.bz2
        ICON_GLOBAL2EUAU_025_EASY.tar.bz2
        ICON_GLOBAL2EUAU_0125_EASY.tar.bz2
        icon_grid_0026_R03B07_G.bz2

    Für weitere Informationen verweisen wir auf:

        https://www.dwd.de/DE/leistungen/opendata/hilfe.html#doc625266bodyText13
        https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_DE.pdf?__blob=publicationFile
        https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_EN.pdf?__blob=publicationFile

    Informationen über die entsprechenden Ressourcen finden sich auf dem DWD Open Data Server unter:

        https://opendata.dwd.de/weather/lib/README.txt
        https://opendata.dwd.de/weather/lib/cdo/
        http://icon-downloads.zmaw.de/dwd_grids.xml
    """

    description_weight_files = [
        GridDescriptionWeight(
            kind=GridKind.ICON_GLOBAL2WORLD_0125,
            resolution=0.125,
            url="https://opendata.dwd.de/weather/lib/cdo/ICON_GLOBAL2WORLD_0125_EASY.tar.bz2",
            description="target_grid_world_0125.txt",
            weights="weights_icogl2world_0125.nc",
        ),
        GridDescriptionWeight(
            kind=GridKind.ICON_GLOBAL2WORLD_025,
            resolution=0.250,
            url="https://opendata.dwd.de/weather/lib/cdo/ICON_GLOBAL2WORLD_025_EASY.tar.bz2",
            description="target_grid_world_025.txt",
            weights="weights_icogl2world_025.nc",
        ),
        GridDescriptionWeight(
            kind=GridKind.ICON_GLOBAL2EUAU_0125,
            resolution=0.125,
            url="https://opendata.dwd.de/weather/lib/cdo/ICON_GLOBAL2EUAU_0125_EASY.tar.bz2",
            description="target_grid_EUAU_0125.txt",
            weights="weights_icogl2world_0125_EUAU.nc",
        ),
        GridDescriptionWeight(
            kind=GridKind.ICON_GLOBAL2EUAU_025,
            resolution=0.250,
            url="https://opendata.dwd.de/weather/lib/cdo/ICON_GLOBAL2EUAU_025_EASY.tar.bz2",
            description="target_grid_EUAU_025.txt",
            weights="weights_icogl2world_025_EUAU.nc",
        ),
    ]

    grid_files = [
        GridFile(
            kinds=[GridKind.ICON_GLOBAL2WORLD_0125, GridKind.ICON_GLOBAL2WORLD_025],
            resolution=13,
            url="https://opendata.dwd.de/weather/lib/cdo/icon_grid_0026_R03B07_G.nc.bz2",
            identifier="R03B07_G",
            description="Global R03B07 grid. 13 km resolution.",
        ),
        GridFile(
            kinds=[GridKind.ICON_GLOBAL2WORLD_0125, GridKind.ICON_GLOBAL2WORLD_025],
            resolution=40,
            url="https://opendata.dwd.de/weather/lib/cdo/icon_grid_0024_R02B06_G.nc.bz2",
            identifier="R02B06_G",
            description="Global R02B06 grid. 40 km resolution.",
        ),
        GridFile(
            kinds=[GridKind.ICON_GLOBAL2EUAU_0125, GridKind.ICON_GLOBAL2EUAU_025],
            resolution=20,
            url="https://opendata.dwd.de/weather/lib/cdo/icon_grid_0028_R02B07_N02.nc.bz2",
            identifier="R02B07_N02",
            description="Regional R02B07 grid (Europe). 20 km resolution.",
        ),
        GridFile(
            kinds=Any,
            resolution=2,
            url="https://opendata.dwd.de/weather/lib/cdo/icon_grid_0047_R19B07_L.nc.bz2",
            identifier="R19B07_L",
            description="Limited area grid (Germany): Enhanced COSMO-D2 area with 2 km resolution.",
        ),
    ]

    def get_info(
        self, kind: Union[GridKind, str], resolution_dw: float, resolution_grid: int = None
    ):
        """
        Get composite information needed for a transformation/regridding process.
        That is, the grid itself accompanied by its description/weight information.

        :param kind: Any of GridKind
        :param resolution_dw: A resolution in degrees (0.125 or 0.250) for the icosahedral data.
                              This is needed for selecting the right description & weight info.
        :param resolution_grid: A resolution in kilometres (13, 40, 20, 2) for the latlon-gridded data.
                                This is needed for selecting the grid info.
        :return:
        """
        kind = self.kind_from_model(model=kind, resolution=resolution_dw)
        info = GridInformation(
            description_weight=self.get_description_weight(kind=kind, resolution=resolution_dw),
            grid=self.get_grid(kind=kind, resolution=resolution_grid),
        )
        return info

    def get_description_weight(self, kind: GridKind, resolution: float = None):
        for description_weight in self.description_weight_files:
            if description_weight.kind == kind:
                if resolution is None or description_weight.resolution == resolution:
                    return description_weight

    def get_grid(self, kind: GridKind, resolution: int = None):
        for grid_file in self.grid_files:
            if kind is Any or kind in grid_file.kinds:
                if resolution is None or grid_file.resolution == resolution:
                    return grid_file

    @staticmethod
    def kind_from_model(model: str, resolution: float):

        model = model.lower()

        # TODO: Improve heuristics.
        if "global" in model or model == "icon":
            if resolution == 0.125:
                kind = GridKind.ICON_GLOBAL2WORLD_0125
            elif resolution == 0.250:
                kind = GridKind.ICON_GLOBAL2WORLD_025
            else:
                raise ValueError("Unknown grid resolution requested")

        # TODO: Improve heuristics.
        elif "eu" in model:
            if resolution == 0.125:
                kind = GridKind.ICON_GLOBAL2EUAU_0125
            elif resolution == 0.250:
                kind = GridKind.ICON_GLOBAL2EUAU_025
            else:
                raise ValueError("Unknown grid resolution requested")
        else:
            raise ValueError("Unknown grid kind requested")
        return kind


class RegridTransformer:
    """
    Perform grid transformation and coordinate rearrangement on GRIB data.

    This is suitable for bringing ICON GLOBAL NWP data into the form of a regular grid.

    1. Transform from "icosahedral" to "regular-lat-lon" grid.
        - https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial#Interpolation
        - https://www.dwd.de/DWD/forschung/nwv/fepub/icon_database_main.pdf
        - https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_DE.pdf?__blob=publicationFile
        - https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_EN.pdf?__blob=publicationFile
        - https://opendata.dwd.de/weather/lib/cdo/

    2. Rearrange coordinates data from longitude 0 to 360 degrees (long3) to -180 to 180 degrees (long1).
        - https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial#Basic-Usage
        - https://confluence.ecmwf.int/pages/viewpage.action?pageId=149337515
        - https://gis.stackexchange.com/questions/201789/verifying-formula-that-will-convert-longitude-0-360-to-180-to-180
    """

    def __init__(
        self, gridinfo: GridInformation, input: List[Path], output: Path, dry_run: bool = False
    ):
        self.gridinfo = gridinfo
        self.input = map(Path, as_list(input))
        self.output = Path(output)
        self.dry_run = dry_run
        with redirect_stdout(sys.stderr):
            self.cdo = Cdo(logging=True, debug=False)

    def setup(self):
        logger.info(
            f'Using grid information "{self.gridinfo.grid.description}" with "{self.gridinfo.description_weight.description}" and "{self.gridinfo.description_weight.weights}"'
        )
        if not self.dry_run:
            self.gridinfo.description_weight.install()
            self.gridinfo.grid.install()

    def process(self) -> List[ProcessingResult]:
        """
        Process all input files.

        :return: List of ``ProcessingResult`` instances
        """

        processor = FileProcessor(input=self.input, method=self.step)
        return processor.resolve().run()

    def step(self, item: ProcessingResult) -> None:

        filename = item.input.stem
        item.output = self.output / f"{filename}-latlon-long1.grib2"

        logger.info(f"Invoke regridding on {filename}")

        if self.dry_run:
            return

        if item.output.exists():
            logger.debug(f"[rearr] Skipping existing file: {item.output}")
            return

        tmpfile = tempfile.NamedTemporaryFile(prefix=f"{filename}-latlon-long3_", suffix=".grib2")

        # 1. Transform from "icosahedral" to "regular-lat-lon" grid.
        long3file = Path(tmpfile.name)

        logger.info(f"""[remap] Transforming from "icosahedral" to "regular-lat-lon" grid""")
        logger.debug(f"[remap] Processing infile={item.input}, outfile={long3file}")

        if not self.dry_run:
            self.cdo.remap(
                f'"{self.gridinfo.description_weight.description_file}"',
                f'"{self.gridinfo.description_weight.weights_file}"',
            ).setgrid(
                f'"{self.gridinfo.grid.gridfile}"',
                input=str(item.input),
                output=str(long3file),
            )

            # .setmisstoc(0) \

        # 2. Rearrange coordinates data from longitude 0 to 360 degrees (long3) to -180 to 180 degrees (long1).
        infile = long3file
        logger.info('[rearr] Rearranging coordinates from "long3" to "long1"')
        logger.debug(f"[rearr] Processing infile={infile}, outfile={long3file}")

        self.output.mkdir(parents=True, exist_ok=True)

        self.cdo.sellonlatbox(-180, 180, -90, 90, input=str(infile), output=str(item.output))

        logger.info(f"[rearr] Regridded file is {long3file}")
