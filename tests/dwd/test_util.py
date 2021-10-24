from freezegun import freeze_time

from tests.dwd.util import previous_modelrun


@freeze_time("2012-01-14T18:21:34Z")
def test_previous_modelrun_standard():
    assert previous_modelrun() == "2012011412"


@freeze_time("2012-01-14T02:00:00Z")
def test_previous_modelrun_day_before_turnover():
    assert previous_modelrun() == "2012011318"


@freeze_time("2012-01-14T03:00:00Z")
def test_previous_modelrun_day_after_turnover():
    assert previous_modelrun() == "2012011400"
