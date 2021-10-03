""" command line entry points for nwp data download """
import sys
import fire
import logging
from gribmagic.unity.pipelines.pipelines import run_model_download

logger = logging.getLogger(__name__)


# The logging has to be configured on the module level
# in order to make it apply in ProcessPoolExecutor contexts.
# https://stackoverflow.com/a/49791106
def setup_logging(level=logging.INFO) -> None:
    log_format = "%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


setup_logging()


def main():
    logger.info("Starting GribMagic")
    fire.Fire({
        'run_model_download': run_model_download
    })


if __name__ == '__main__':
    main()
