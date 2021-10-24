from pathlib import Path
from typing import List

import cfgrib
import pytest
import xarray as xr

from gribmagic.smith.regrid.engine import GridTransformationLibrary, RegridTransformer
from gribmagic.smith.regrid.model import GridKind
from gribmagic.smith.util import ProcessingResult
from tests.unity.fixtures import (
    icon_global_icosahedral_input_file,
    icon_global_icosahedral_regridded_output_filename,
)


@pytest.mark.regrid
@pytest.mark.unit
def test_regrid_success(gm_data_path, tmpdir):

    # Check dimensions and grid type of input file.
    ds_in: xr.Dataset = cfgrib.open_dataset(icon_global_icosahedral_input_file)
    assert ds_in.dims == {"values": 2949120}
    assert ds_in.variables["gust"].attrs["GRIB_gridType"] == "unstructured_grid"

    # Load grid transformation asset files.
    gridlib = GridTransformationLibrary()
    gridinfo = gridlib.get_info(kind="global", resolution_dw=0.25)

    # Transform grid / regrid.
    transformer = RegridTransformer(
        gridinfo=gridinfo, input=[icon_global_icosahedral_input_file], output=tmpdir
    )
    transformer.setup()
    results: List[ProcessingResult] = transformer.process()

    # Check output filename.
    item = results[0]
    assert item.output.match(icon_global_icosahedral_regridded_output_filename)
    assert item.output.exists()

    # Check dimensions and grid type of output file.
    ds_out: xr.Dataset = cfgrib.open_dataset(item.output)
    assert ds_out.dims == {"latitude": 721, "longitude": 1440}
    assert ds_out.variables["gust"].attrs["GRIB_gridType"] == "regular_ll"

    # Check variables.
    assert "latitude" in ds_out.variables
    assert "longitude" in ds_out.variables
    assert "gust" in ds_out.variables

    # Check coordinate ranges.
    assert min(ds_out.variables["latitude"].data) == -90
    assert max(ds_out.variables["latitude"].data) == +90
    assert min(ds_out.variables["longitude"].data) == -180
    assert max(ds_out.variables["longitude"].data) == 179.75

    # Check parameter values.
    assert len(ds_out.variables["gust"]) == 721


@pytest.mark.regrid
@pytest.mark.unit
def test_regrid_dryrun_success(gm_data_path, tmpdir):

    # Check dimensions and grid type of input file.
    # ds_in: xr.Dataset = cfgrib.open_dataset(icon_global_icosahedral_input_file)
    # assert ds_in.dims == {"values": 2949120}
    # assert ds_in.variables["gust"].attrs["GRIB_gridType"] == "unstructured_grid"

    # Load grid transformation asset files.
    gridlib = GridTransformationLibrary()
    gridinfo = gridlib.get_info(kind="global", resolution_dw=0.25)

    # Transform grid / regrid.
    transformer = RegridTransformer(
        gridinfo=gridinfo, input=[icon_global_icosahedral_input_file], output=tmpdir, dry_run=True
    )
    # transformer.setup()
    results: List[ProcessingResult] = transformer.process()

    # Check output filename.
    item = results[0]
    assert item.output.match(icon_global_icosahedral_regridded_output_filename)
    assert not item.output.exists()


def test_kind_from_model():

    gtl = GridTransformationLibrary()

    kind = gtl.kind_from_model(model="GLOBAL", resolution=0.125)
    assert kind == GridKind.ICON_GLOBAL2WORLD_0125

    kind = gtl.kind_from_model(model="GLOBAL", resolution=0.250)
    assert kind == GridKind.ICON_GLOBAL2WORLD_025

    kind = gtl.kind_from_model(model="EU", resolution=0.125)
    assert kind == GridKind.ICON_GLOBAL2EUAU_0125

    kind = gtl.kind_from_model(model="EU", resolution=0.250)
    assert kind == GridKind.ICON_GLOBAL2EUAU_025

    with pytest.raises(ValueError) as ex:
        gtl.kind_from_model(model="global", resolution=0.123)
    assert ex.match("Unknown grid resolution requested")

    with pytest.raises(ValueError) as ex:
        gtl.kind_from_model(model="eu", resolution=0.123)
    assert ex.match("Unknown grid resolution requested")

    with pytest.raises(ValueError) as ex:
        gtl.kind_from_model(model="foobar", resolution=0.123)
    assert ex.match("Unknown grid kind requested")
