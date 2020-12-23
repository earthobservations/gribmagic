import logging
import os
import sys
from pathlib import Path


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

    # Satisy importing of ``extendedformatter.py``.
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


def setup_logging(level=logging.INFO) -> None:
    """
    Setup Python logging

    :param level:
    :return:
    """
    log_format = "%(asctime)-15s [%(name)-15s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)
