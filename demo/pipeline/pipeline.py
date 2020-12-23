#!/usr/bin/env python
"""
Describe and invoke a downloading pipeline for GRIB data from DWD.

Inspired from ``test-download.sh`` by Michael Haberler.
See https://github.com/mhaberler/docker-dwd-open-data-downloader/commit/ff09dbc8.

Based upon DWD Open Data Downloader by Eduard Rosert and Björn Reetz,
with contributions by Michael Haberler.

- https://github.com/DeutscherWetterdienst/downloader
- https://github.com/EduardRosert/docker-dwd-open-data-downloader
- https://github.com/mhaberler/docker-dwd-open-data-downloader/tree/rewrite

Beforehand, install ``opendata-downloader.py`` by typing
``make install-dwd-grib-downloader`` within the toplevel directory.
It
"""
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import click

from demo.pipeline.util import setup_logging, load_module


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
    parameter_options: dict


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
            path="./tools/dwd-grib-downloader/opendata-downloader.py")

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
            waitTimeMinutes=openDataDeliveryOffsetMinutes, modelIntervalHours=modelIntervalHours, modelrun=modelrun)

        return latestTimestamp

    def download(self, model: str, grid: str, parameter: str, level: str, time_steps: List[int], levels: List[int] = None):
        """
        Invoke ``opendata-downloader.py`` program.

        :param model:
        :param grid:
        :param parameter:
        :param level:
        :param time_steps:
        :param levels:
        :return:
        """

        # Compute timestamp.
        timestamp = self.get_most_recent_timestamp(model=model, modelrun=self.timestamp)

        # Default for "single-level" parameters.
        levels = levels or [0]

        self.dwdgrib.downloadGribDataSequence(
            model=model,
            flat=False,
            grid=grid,
            param=parameter,
            timeSteps=time_steps,
            timestamp=timestamp,
            levelRange=levels,
            levtype=level,
            destFilePath=str(self.output))


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
        downloader.download(
            model=recipe.model,
            grid=recipe.grid,
            parameter=parameter.name,
            level=parameter.level,
            time_steps=recipe.parameter_options["timesteps"],
            levels=parameter.options.get("levels")
        )


@click.command(help="Download GRIB data from DWD.")
@click.option("--recipe",
              type=click.Path(exists=True, file_okay=True),
              help="The recipe file",
              required=True)
@click.option("--timestamp",
              type=str,
              help="The timestamp/modelrun",
              required=True)
@click.option("--output",
              type=click.Path(exists=False, file_okay=False, dir_okay=True),
              help="The output directory",
              required=True)
def main(recipe: Path, timestamp: str, output: Path):

    # Setup logging.
    setup_logging(logging.DEBUG)

    recipe_module = load_module("gribmagic.recipe", recipe)
    recipe_instance = recipe_module.recipe

    process(recipe=recipe_instance, timestamp=timestamp, output=output)


if __name__ == "__main__":
    main()
