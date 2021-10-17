from datetime import datetime

import pytest
import pytz

from gribmagic.util import parse_timestamp


def test_convert_iso_to_date_time_valid():
    assert datetime(2019, 9, 30, 5, 30, 0, tzinfo=pytz.utc) == parse_timestamp(
        "2019-09-30T05:30:00+00:00"
    )


def test_convert_iso_to_date_time_invalid():
    with pytest.raises(ValueError):
        assert datetime(2019, 9, 30, 5, 30, 0, tzinfo=pytz.utc) == parse_timestamp(
            "2019-09-30T05:30:00"
        )
