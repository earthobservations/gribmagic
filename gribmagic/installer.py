import logging
import os
from pathlib import Path
from typing import List

import appdirs
import click

logger = logging.getLogger(__name__)


@click.command(help="Install helper programs.")
@click.argument("packages", nargs=-1)
def main(packages: List[str]):
    for package in packages:
        install_package(package)


DWD_GRIB_DOWNLOADER_PATH = (
    Path(appdirs.user_data_dir("gribmagic", "earthobservations")) / "dwd-grib-downloader"
)


def install_package(name: str):
    if name == "dwd-grib-downloader":
        logger.info(f"Installing '{name}' to '{DWD_GRIB_DOWNLOADER_PATH}'")
        command = f"""
        test -d '{DWD_GRIB_DOWNLOADER_PATH}' && 
            (cd '{DWD_GRIB_DOWNLOADER_PATH}' && git pull) || 
            git clone --branch=amo/develop https://github.com/earthobservations/dwd-grib-downloader '{DWD_GRIB_DOWNLOADER_PATH}' 
        """.strip()
        os.system(command)

    elif name == "dwd-grid-information":
        from gribmagic.smith.regrid.engine import GridTransformationLibrary
        from gribmagic.smith.regrid.model import GRID_METADATA_PATH

        logger.info(f"Installing grid information files to '{GRID_METADATA_PATH}'")
        for item in GridTransformationLibrary.description_weight_files:
            item.install()
        for item in GridTransformationLibrary.grid_files:
            item.install()

    else:
        raise ValueError(f"Unknown package {name}")
