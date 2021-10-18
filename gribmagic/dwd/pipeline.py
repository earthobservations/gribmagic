#!/usr/bin/env python
"""
Describe and invoke a downloading pipeline for GRIB data from DWD.

Inspired by ``test-download.sh`` by Michael Haberler.
See https://github.com/mhaberler/docker-dwd-open-data-downloader/commit/ff09dbc8.

Based upon DWD Open Data Downloader by Eduard Rosert and Björn Reetz,
with contributions by Michael Haberler and Andreas Motl.

- https://github.com/DeutscherWetterdienst/downloader
- https://github.com/EduardRosert/docker-dwd-open-data-downloader
- https://github.com/mhaberler/docker-dwd-open-data-downloader/tree/rewrite
- https://github.com/earthobservations/dwd-grib-downloader

Beforehand, install ``opendata-downloader.py`` by typing
``make install-dwd-grib-downloader`` within the toplevel directory.
It
"""
import logging
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import click

from gribmagic.util import load_module, setup_logging

HERE = Path(__file__)
GRIBMAGIC_PATH = HERE.parent.parent.parent

logger = logging.getLogger(__name__)


@dataclass
class Parameter:
    name: str
    level: str
    options: dict = field(default_factory=dict)


@dataclass
class Recipe:
    """
    Main recipe holder which describes the metadata needed
    to download a subset of GRIB files from DWD.

    """

    model: str
    grid: str
    parameters: List[Parameter]
    parameter_options: dict = None


class DwdDownloader:
    """
    Wrap access to ``opendata-downloader.py``.
    """

    def __init__(self, output: Path, timestamp: str = None):
        self.output = output
        self.timestamp = timestamp

        # Load ``opendata-downloader.py`` as module.
        self.dwdgrib = load_module(
            name="dwd.grib.downloader",
            path=GRIBMAGIC_PATH / "tools/dwd-grib-downloader/opendata-downloader.py",
        )

        # Configure downloader.
        self.dwdgrib.maxWorkers = 4
        self.dwdgrib.compressed = False

    def get_most_recent_timestamp(self, model: str, modelrun: str = None):
        """
        Part of the code from ``opendata-downloader.py``.

        :param model:
        :param modelrun:
        :return:
        """

        # wait 5 hrs (=300 minutes) after a model run for icon-eu data
        # and 1,5 hrs (=90 minute) for cosmo-d2, just to be sure
        selectedModel = self.dwdgrib.supportedModels[model.lower()]
        openDataDeliveryOffsetMinutes = selectedModel["openDataDeliveryOffsetMinutes"]
        modelIntervalHours = selectedModel["intervalHours"]
        latestTimestamp = self.dwdgrib.getMostRecentModelTimestamp(
            waitTimeMinutes=openDataDeliveryOffsetMinutes,
            modelIntervalHours=modelIntervalHours,
            modelrun=modelrun,
        )

        return latestTimestamp

    def download(
        self,
        model: str,
        grid: str,
        parameter: str,
        level: str,
        timesteps: List[int],
        levels: List[int] = None,
    ):
        """
        Invoke ``opendata-downloader.py`` program.

        :param model:
        :param grid:
        :param parameter:
        :param level:
        :param timesteps:
        :param levels:
        :return:
        """

        # Compute timestamp.
        timestamp = self.get_most_recent_timestamp(model=model, modelrun=self.timestamp)

        # Default for "single-level" parameters.
        if level == "single-level":
            levels = levels or [0]
        else:
            if not levels:
                raise ValueError(f"""Addressing "{level}"-type data needs "levels" parameter""")

        logger.info(f'Downloading to target directory "{self.output}"')

        results = self.dwdgrib.downloadGribDataSequence(
            model=model,
            flat=False,
            grid=grid,
            param=parameter,
            timeSteps=timesteps,
            timestamp=timestamp,
            levelRange=levels,
            levtype=level,
            destFilePath=str(self.output),
        )

        return results


def process(recipe: Recipe, timestamp: str, output: Path):
    """
    Process whole GRIB acquisition recipe.

    :param recipe:
    :param timestamp:
    :param output:
    :return:
    """
    downloader = DwdDownloader(output=output, timestamp=timestamp)
    for parameter in recipe.parameters:

        logger.info(f"Running acquisition for {parameter}")

        # Merge parameter options, item-level takes precedence.
        options_default = deepcopy(recipe.parameter_options)
        options_item = deepcopy(parameter.options)
        options_effective = options_default
        options_effective.update(options_item)

        # Invoke downloader.
        results = downloader.download(
            model=recipe.model,
            grid=recipe.grid,
            parameter=parameter.name,
            level=parameter.level,
            timesteps=options_effective.get("timesteps"),
            levels=options_effective.get("levels"),
        )

        yield results


@click.command(help="Download GRIB data from DWD.")
@click.option(
    "--recipe", type=click.Path(exists=True, file_okay=True), help="The recipe file", required=True
)
@click.option("--timestamp", type=str, help="The timestamp/modelrun", required=True)
@click.option(
    "--output",
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="The output directory",
    required=True,
)
def main(recipe: Path, timestamp: str, output: Path):

    # Setup logging.
    setup_logging(logging.DEBUG)

    recipe_module = load_module("gribmagic.recipe", recipe)
    recipe_instance = recipe_module.recipe
    logger.info(f"Invoking recipe: {recipe_instance}")

    results = process(recipe=recipe_instance, timestamp=timestamp, output=output)
    list(results)


if __name__ == "__main__":
    main()
