import pytest

from tests.dwd.util import (
    previous_modelrun,
    run_icon_d2_vmax_recipe,
    run_icon_global_temp2m_recipe,
)


@pytest.mark.parametrize("run_recipe", [run_icon_d2_vmax_recipe, run_icon_global_temp2m_recipe])
def test_dwd_previous_modelrun_success(run_recipe):

    # Use the previous model run, 6 hours ago.
    modelrun = previous_modelrun()

    # Run data acquisition.
    results = run_recipe(modelrun)

    # Check outcome.
    outcome = all(outcome["file"] is not None for outcome in results)
    assert outcome is True


@pytest.mark.parametrize("run_recipe", [run_icon_d2_vmax_recipe, run_icon_global_temp2m_recipe])
def test_dwd_no_modelrun_success(run_recipe):

    # Run data acquisition.
    results = run_recipe(None)

    # Check outcome.
    outcome = all(outcome["file"] is not None for outcome in results)
    assert outcome is True


@pytest.mark.parametrize("run_recipe", [run_icon_d2_vmax_recipe, run_icon_global_temp2m_recipe])
def test_dwd_modelrun_expired(run_recipe):

    # Use a timestamp in the past, 2021-10-05T00
    modelrun = "2021100500"

    # Run data acquisition.
    results = run_recipe(modelrun)

    # Check outcome.
    outcome = any(outcome["file"] is not None for outcome in results)
    assert outcome is False
