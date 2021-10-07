"""Command line entry points for NWP data download"""
import logging
from datetime import datetime
from typing import Union

import click

from gribmagic.unity.core import run_model_download
from gribmagic.unity.enumerations.weather_models import WeatherModels
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
    results = run_model_download(
        weather_model=model, initialization_timestamp=timestamp
    )

    # If a func call raises an exception, then that exception will be raised
    # when its value is retrieved from the iterator.
    # https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.map
    list(results)
