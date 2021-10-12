"""Command line entry points for NWP data download"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Union

import click

from gribmagic.unity.core import run_model_download
from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.modules.config.parse_configurations import parse_model_config
from gribmagic.util import setup_logging

logger = logging.getLogger(__name__)


# The logging has to be configured on the module level
# in order to make it apply in ProcessPoolExecutor contexts.
# https://stackoverflow.com/a/49791106
setup_logging()


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.group(help="Unified NWP data downloader")
@click.pass_context
def unity(ctx):
    pass


@unity.command(name="list", help="List available NWP data labels")
def unity_list():
    model_config = parse_model_config()
    labels = [label for label in model_config.keys() if not label.endswith("-base")]
    print(json.dumps(labels, indent=4))


@unity.command(name="acquire", help="Acquire NWP data")
@click.option("--model", required=True, help="The weather model name.")
@click.option("--timestamp", required=True, help="The initialization timestamp.")
@click.option(
    "--target", required=True, envvar="GM_DATA_PATH", help="The target directory."
)
def unity_acquire(
    model: Union[str, WeatherModels],
    timestamp: Union[str, datetime],
    target: Union[str, Path],
):
    logger.info("Starting GribMagic")
    results = run_model_download(
        weather_model=model, initialization_timestamp=timestamp, target_directory=target
    )

    # If a func call raises an exception, then that exception will be raised
    # when its value is retrieved from the iterator.
    # https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.map
    list(results)
