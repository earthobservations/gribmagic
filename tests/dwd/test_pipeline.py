from tests.dwd.util import (
    previous_modelrun,
    run_icon_d2_vmax_recipe,
    run_icon_global_temp2m_recipe,
)


def test_dwd_icon_d2_success():

    # Use the previous model run, 6 hours ago.
    modelrun = previous_modelrun()

    # Run data acquisition.
    results = run_icon_d2_vmax_recipe(modelrun)

    # Check outcome.
    outcome = all(outcome["file"] is not None for outcome in results)
    assert outcome is True


def test_dwd_icon_d2_modelrun_expired():

    # Use a timestamp in the past, 2021-10-05T00
    modelrun = "2021100500"

    # Run data acquisition.
    results = run_icon_d2_vmax_recipe(modelrun)

    # Check outcome.
    outcome = any(outcome["file"] is not None for outcome in results)
    assert outcome is False


def test_dwd_icon_global_success():

    # Use the previous model run, 6 hours ago.
    modelrun = previous_modelrun()

    # Run data acquisition.
    results = run_icon_global_temp2m_recipe(modelrun)

    # Check outcome.
    outcome = all(outcome["file"] is not None for outcome in results)
    assert outcome is True


def test_dwd_icon_global_modelrun_expired():

    # Use a timestamp in the past, 2021-10-05T00
    modelrun = "2021100500"

    # Run data acquisition.
    results = run_icon_global_temp2m_recipe(modelrun)

    # Check outcome.
    outcome = any(outcome["file"] is not None for outcome in results)
    assert outcome is False
