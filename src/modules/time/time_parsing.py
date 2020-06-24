""" generic time parsing function """
from datetime import datetime
from dateutil.parser import parse


def convert_iso_timestamp_to_date_time(value: str) -> datetime:
    """
    Convert string in ISO8601/RFC3339-format to timezone aware datetime object

    Args:
        value: string of timestamp in ISO8601/RFC3339-format
    Returns: timezone aware datetime object
    """
    timestamp = parse(value)
    if timestamp.tzinfo is None or \
            timestamp.tzinfo.utcoffset(timestamp) is None:
        raise ValueError("Timestamp is not timezone aware")
    else:
        return timestamp
