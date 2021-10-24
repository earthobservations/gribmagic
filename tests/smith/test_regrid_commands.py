"""
Invoke the tests in this file using::

    pytest -vvv -m "regrid and command"
"""
import json

import pytest
from click.testing import CliRunner

from gribmagic.commands import cli


@pytest.mark.regrid
@pytest.mark.command
def test_regrid_basic_success(gm_data_path, capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_global_temp2m_single.py",
        ],
    )
    assert result.exit_code == 0, result.output

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "regrid",
            f"{gm_data_path}/icon/**/*icon_global_icosahedral*.grib2",
        ],
    )
    assert result.exit_code == 0, result.output

    # Sanitize output.
    output = result.output.replace("-->> Could not load netCDF4! <<--", "")

    # Check results.
    report = json.loads(output)
    assert len(report) == 1

    first_item = report[0]

    assert "input" in first_item
    assert "output" in first_item

    assert first_item["input"].endswith(".grib2")
    assert first_item["output"].endswith(".grib2")
    assert "-latlon-long1" in first_item["output"]


@pytest.mark.regrid
@pytest.mark.command
def test_regrid_basic_input_files_failure(gm_data_path, capsys):
    runner = CliRunner()

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "regrid",
        ],
    )
    assert result.exit_code == 2, result.output
    assert "Error: Missing argument 'INPUT...'" in result.output
