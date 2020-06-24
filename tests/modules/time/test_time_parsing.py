from datetime import datetime
import pytz

import pytest

from src.modules.time.time_parsing import convert_iso_timestamp_to_date_time


def test_convert_iso_to_date_time_valid():
    assert datetime(2019, 9, 30, 5, 30, 0, tzinfo=pytz.utc) == \
           convert_iso_timestamp_to_date_time("2019-09-30T05:30:00+00:00")


def test_convert_iso_to_date_time_invalid():
    with pytest.raises(ValueError):
        assert datetime(2019, 9, 30, 5, 30, 0, tzinfo=pytz.utc) == \
               convert_iso_timestamp_to_date_time("2019-09-30T05:30:00")
