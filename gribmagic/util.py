import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dateutil.parser import parse

logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO) -> None:
    log_format = "%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


def parse_timestamp(value: str) -> datetime:
    """
    Convert string in ISO8601/RFC3339-format to timezone aware datetime object

    Args:
        value: string of timestamp in ISO8601/RFC3339-format
    Returns: timezone aware datetime object
    """
    timestamp = parse(value)
    if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
        raise ValueError("Timestamp is not timezone aware")
    else:
        return timestamp


def load_module(name: str, path: str):
    """
    Import Python module from file.

    This is needed because we can't import
    ``opendata-downloader.py`` as a module directly.

    However, we also use it for loading the recipe at runtime.

    :param name:
    :param path:
    :return:
    """

    # Use absolute path.
    modulefile = Path(path).absolute()

    # Extend module search path.
    modulepath = Path(modulefile).parent.absolute()

    # Satisfy importing of ``extendedformatter.py``.
    # No module named 'extendedformatter'
    sys.path.append(str(modulepath))

    # Satisfy reading of ``models.json``.
    current_dir = os.getcwd()
    os.chdir(modulepath)

    # Import module.
    # https://stackoverflow.com/a/67692
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, modulefile)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Restore working directory.
    os.chdir(current_dir)

    return mod


def run_command(command):
    logger.debug(f"Running command: {command}")
    exitcode = os.WEXITSTATUS(os.system(command))
    assert exitcode == 0, exitcode
