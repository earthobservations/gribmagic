"""Command line entry points for NWP data download"""
from datetime import datetime
from typing import Union

import click
import logging

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.core import run_model_download
from gribmagic.util import setup_logging

logger = logging.getLogger(__name__)


# The logging has to be configured on the module level
# in order to make it apply in ProcessPoolExecutor contexts.
# https://stackoverflow.com/a/49791106
setup_logging()


@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option("--model", required=True, help="The weather model name.")
@click.option("--timestamp", required=True, help="The initialization timestamp.")
def unity(model: Union[str, WeatherModels], timestamp: Union[str, datetime]):
    logger.info("Starting GribMagic")
    run_model_download(weather_model=model, initialization_timestamp=timestamp)
