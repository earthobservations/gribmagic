import logging
import sys


def setup_logging(level=logging.INFO) -> None:
    log_format = "%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)
