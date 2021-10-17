import logging
import sys
from datetime import datetime

from dateutil.parser import parse


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
