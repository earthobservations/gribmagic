"""
Invoke the tests in this file using::

    pytest -vvv -m "bbox and unit"
"""
import re
from pathlib import Path

import cfgrib
import pytest
import xarray as xr
from funcy import project

from gribmagic.smith.bbox import BBox, GRIBSubset, ProcessingResult
from tests.unity.fixtures import icon_global_input_file


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_constructor_success():
    BBox(latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147)


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_constructor_failure():
    with pytest.raises(TypeError) as ex:
        BBox(latitude_min=46.399, latitude_max=49.001, longitude_max=17.147)
    assert ex.match(
        re.escape("__init__() missing 1 required positional argument: 'longitude_min'")
    )


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_from_country_success():
    bbox = BBox.from_country("AT")
    assert bbox == BBox(
        latitude_min=46.3997070312,
        latitude_max=49.0011230469,
        longitude_min=9.5240234375,
        longitude_max=17.1473632813,
    )


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_from_country_failure():
    with pytest.raises(ValueError) as ex:
        BBox.from_country("FOO")
    assert ex.match("Unknown country iso code: FOO")


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_from_coordinates_success():
    bbox = BBox.from_coordinates((46.399, 49.001, 9.524, 17.147))
    assert bbox == BBox(
        latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147
    )


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_from_coordinates_failure():
    with pytest.raises(TypeError) as ex:
        BBox.from_coordinates((46.399, 49.001, 9.524))
    assert ex.match(
        re.escape("__init__() missing 1 required positional argument: 'longitude_max'")
    )


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_to_tuple_regular_success():
    bbox = BBox(
        latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147
    )
    assert bbox.to_tuple() == (46.399, 49.001, 9.524, 17.147)


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_to_tuple_lonlat_success():
    bbox = BBox(
        latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147
    )
    assert bbox.to_tuple(lonlat=True) == (9.524, 17.147, 46.399, 49.001)


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_to_string_regular_success():
    bbox = BBox(
        latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147
    )
    assert bbox.to_string(separator=",") == "46.399,49.001,9.524,17.147"


@pytest.mark.bbox
@pytest.mark.unit
def test_bbox_to_string_lonlat_success():
    bbox = BBox(
        latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147
    )
    assert bbox.to_string(separator=",", lonlat=True) == "9.524,17.147,46.399,49.001"


@pytest.mark.bbox
@pytest.mark.unit
@pytest.mark.parametrize("method", ["cdo-shellout", "cdo-python", "xarray"])
def test_gribsubset_success(gm_data_path, method):

    if method == "xarray":
        raise pytest.xfail("Method 'xarray' is currently broken")

    # Check dimensions if input file.
    ds_in: xr.Dataset = cfgrib.open_file(icon_global_input_file)
    assert ds_in.dimensions == {"latitude": 721, "longitude": 1440}

    input_paths = [icon_global_input_file]
    output = gm_data_path
    bbox = BBox(
        latitude_min=46.399, latitude_max=49.001, longitude_min=9.524, longitude_max=17.147
    )
    use_netcdf = False
    plot = False

    subgrid = GRIBSubset(
        input=map(Path, input_paths),
        output=output,
        bbox=bbox,
        method=method,
        use_netcdf=use_netcdf,
        plot=plot,
    )
    results = subgrid.process()

    assert len(results) == 1
    result: ProcessingResult = results[0]

    # Verify process metadata.
    assert result.input.match(
        "icon-global_regular-lat-lon_air-temperature_level-90.grib2"
    ), result.input
    assert result.output.match(
        "bbox_46.399_49.001_9.524_17.147/grib/icon-global_regular-lat-lon_air-temperature_level-90.grib2"
    ), result.input
    assert result.plot is None

    # Verify output GRIB file.

    ds_out: xr.Dataset = cfgrib.open_file(result.output)

    reference = {
        "GRIB_edition": 2,
        "GRIB_centre": "edzw",
        "GRIB_centreDescription": "Offenbach ",
        "GRIB_subCentre": 255,
        "Conventions": "CF-1.7",
        "institution": "Offenbach ",
    }
    attributes = project(ds_out.attributes, reference.keys())
    assert attributes == reference

    # Check dimensions if output file.
    assert ds_out.dimensions == {"latitude": 11, "longitude": 30}

    assert ds_out.encoding["encode_cf"] == ("parameter", "time", "geography", "vertical")

    assert list(ds_out.variables) == [
        "time",
        "step",
        "generalVerticalLayer",
        "latitude",
        "longitude",
        "valid_time",
        "t",
    ]
    assert ds_out.variables["time"].data == 1628251200
    assert len(ds_out.variables["latitude"].data) == 11
    assert len(ds_out.variables["longitude"].data) == 30

    elements = ds_out.variables["t"].data.build_array()
    assert len(elements) == 11
