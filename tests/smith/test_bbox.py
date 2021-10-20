import json

from click.testing import CliRunner

from gribmagic.commands import cli


def test_bbox_plain_success(tmpdir, capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_d2_vmax10m.py",
            f"--output={tmpdir}/raw",
        ],
    )
    assert result.exit_code == 0

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
            f"{tmpdir}/raw/icon-d2/**/*regular-lat-lon*.grib2",
            f"--output={tmpdir}/subgrid",
        ],
    )
    assert result.exit_code == 0

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


def test_bbox_plot_success(tmpdir, capsys):
    runner = CliRunner()

    # Acquire data.
    result = runner.invoke(
        cli,
        [
            "dwd",
            "acquire",
            "--recipe=tests/dwd/recipe_icon_d2_vmax10m.py",
            f"--output={tmpdir}/raw",
        ],
    )
    assert result.exit_code == 0

    # Run bbox on data.
    result = runner.invoke(
        cli,
        [
            "smith",
            "bbox",
            "--country=AT",
            f"{tmpdir}/raw/icon-d2/**/*regular-lat-lon*.grib2",
            f"--output={tmpdir}/subgrid",
            "--plot",
        ],
    )
    assert result.exit_code == 0

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
