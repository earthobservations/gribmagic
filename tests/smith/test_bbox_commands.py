"""
Invoke the tests in this file using::

    pytest -vvv -m "bbox and command"
"""
import json

import pytest
from click.testing import CliRunner

from gribmagic.commands import cli


@pytest.mark.bbox
@pytest.mark.command
def test_bbox_basic_success(gm_data_path, capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_d2_vmax10m.py",
        ],
    )
    assert result.exit_code == 0, result.output

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
            f"{gm_data_path}/icon-d2/**/*regular-lat-lon*.grib2",
        ],
    )
    assert result.exit_code == 0, result.output

    # Check results.
    report = json.loads(result.output)
    assert len(report) == 3

    first_item = report[0]

    assert "input" in first_item
    assert "output" in first_item
    assert "plot" in first_item

    assert first_item["input"].endswith(".grib2")
    assert "bbox_" in first_item["output"]
    assert first_item["plot"] is None


@pytest.mark.bbox
@pytest.mark.command
def test_bbox_basic_no_area_failure(gm_data_path, capsys):
    runner = CliRunner()

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            f"{gm_data_path}/icon-d2/**/*regular-lat-lon*.grib2",
        ],
    )
    assert result.exit_code == 2, result.output
    assert (
        "Error: Missing one of the required mutually exclusive options from 'area' option group"
        in result.output
    )


@pytest.mark.bbox
@pytest.mark.command
def test_bbox_basic_input_files_failure(gm_data_path, capsys):
    runner = CliRunner()

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
        ],
    )
    assert result.exit_code == 2, result.output
    assert "Error: Missing argument 'INPUT...'" in result.output


@pytest.mark.bbox
@pytest.mark.command
def test_bbox_plot_success(gm_data_path, capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_d2_vmax10m.py",
        ],
    )
    assert result.exit_code == 0, result.output

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
            f"{gm_data_path}/icon-d2/**/*regular-lat-lon*.grib2",
            "--plot",
        ],
    )
    assert result.exit_code == 0, result.output

    # Check results.
    report = json.loads(result.output)
    assert len(report) == 3

    first_item = report[0]

    assert "input" in first_item
    assert "output" in first_item
    assert "plot" in first_item

    assert first_item["input"].endswith(".grib2")
    assert "bbox_" in first_item["output"]
    assert first_item["plot"].endswith(".png")
