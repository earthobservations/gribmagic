import json

from click.testing import CliRunner

from gribmagic.commands import cli


def test_bbox_plain_success(capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_d2_vmax10m.py",
            "--output=.gribmagic-data/raw",
        ],
    )

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
            ".gribmagic-data/raw/icon-d2/**/*regular-lat-lon*.grib2",
            "--output=.gribmagic-data/subgrid",
        ],
    )

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


def test_bbox_plot_success(capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_d2_vmax10m.py",
            "--output=.gribmagic-data/raw",
        ],
    )

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
            ".gribmagic-data/raw/icon-d2/**/*regular-lat-lon*.grib2",
            "--output=.gribmagic-data/subgrid",
            "--plot",
        ],
    )

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
