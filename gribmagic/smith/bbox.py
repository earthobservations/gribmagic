"""
grib_bbox.py
Copyright (C) 2020  Andreas Motl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import dataclasses
import glob
import json
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import List

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup

logger = logging.getLogger(__name__)

"""
This programs supports the topic "Area of interest from GRIB files".
See https://github.com/earthobservations/gribmagic/blob/main/docs/area_of_interest.rst.
"""


@dataclasses.dataclass
class BBox:
    """
    This holds bounding box information.

    It has to factory methods to create a bounding box
    - ``from_country`` uses an ISO 2-letter country code
    - ``from_coordinates`` uses a 4-tuple (lat_min, lat_max, lon_min, lon_max)
    """

    latitude_min: float
    latitude_max: float
    longitude_min: float
    longitude_max: float

    @staticmethod
    def from_country(country_iso: str):
        """
        Create bounding box using 2-letter country code.

        :param country_iso: 2-letter country code
        :return: BBox instance
        """
        from country_bounding_boxes import country_subunits_by_iso_code

        # Lookup using "country_bounding_boxes"
        # responds with (lon1, lat1, lon2, lat2) tuple.
        countries = list(country_subunits_by_iso_code(country_iso))

        if not countries:
            raise ValueError(f"Unknown country iso code: {country_iso}")
        bbox = countries[0].bbox
        bbox = BBox(
            latitude_min=bbox[1],
            latitude_max=bbox[3],
            longitude_min=bbox[0],
            longitude_max=bbox[2],
        )
        return bbox

    @staticmethod
    def from_coordinates(bbox_tuple: tuple):
        """
        Create bounding box using 4-tuple.

        :param bbox_tuple: 4-tuple (lat_min, lat_max, lon_min, lon_max)
        :return: BBox instance
        """
        #
        bbox = BBox(*bbox_tuple)
        return bbox

    def to_tuple(self, lonlat: bool = False) -> tuple:
        """
        Return bounding box as 4-tuple, optionally swaps to longitude/latitude.

        :param lonlat: Whether to swap to lon/lat.
        :return: 4-tuple
        """
        if lonlat:
            # Return tuple like (lon_min, lon_max, lat_min, lat_max)
            # This is needed for CDO.
            bbox_tuple = (
                self.longitude_min,
                self.longitude_max,
                self.latitude_min,
                self.latitude_max,
            )
        else:
            # Return tuple like (lat_min, lat_max, lon_min, lon_max)
            bbox_tuple = dataclasses.astuple(self)
        return bbox_tuple

    def to_string(self, separator: str, lonlat: bool = False) -> str:
        """
        Return bounding box as 4-tuple, serialized to a string using given separator.
        Optionally swaps to longitude/latitude.

        :param separator: Separator character to use when joining tuple elements.
        :param lonlat: Whether to swap to lon/lat.
        :return:
        """
        bbox_tuple = self.to_tuple(lonlat=lonlat)
        return separator.join(map(str, bbox_tuple))


@dataclasses.dataclass
class ProcessingResult:
    """
    This holds information about the
    result from processing a single file.
    """

    input: Path
    output: Path = None
    plot: Path = None


class GRIBSubset:
    """
    The main workhorse to read a number of GRIB files and
    extract a subset by applying a bounding box.

    It can use different methods like
    - cdo-shellout
    - cdo-python
    - xarray

    As of today, Xarray's cfgrib backend (version 0.9.8.5) can
    not properly write GRIB output, so there is an option to work
    around that by using netCDF.
    """

    def __init__(
        self, input: List[Path], output: str, bbox: BBox, method: str, use_netcdf: bool, plot: bool
    ):
        """
        Create a new GRIBSubset instance.

        :param input: List of input filenames.
        :param output: Output directory. If this doesn't exist, it will be created beforehand.
        :param bbox: The BBox instance describing the area of interest.
        :param method: One of the methods how bbox'ing will take place.
        :param use_netcdf: Whether to process into netCDF.
        :param plot:
        """
        self.input = input
        self.output = output
        self.bbox = bbox
        self.method = method
        self.use_netcdf = use_netcdf
        self.do_plot = plot

        # Compute output folder.
        subdirectory = f'bbox_{self.bbox.to_string("_")}'
        self.outfolder = Path(self.output).joinpath(subdirectory)

    def process(self) -> List[ProcessingResult]:
        """
        Process all input files.

        :return: List of ``ProcessingResult`` instances
        """
        results: List[ProcessingResult] = []
        for infile in self.input:

            logger.info(f"Processing file {infile}")

            item = ProcessingResult(input=infile)

            # Render GRIB.
            gribfile_subgrid = self.extract_area(infile)
            item.output = gribfile_subgrid

            # Render PNG.
            if self.do_plot:
                try:
                    pngfile = self.plot(gribfile_subgrid)
                    item.plot = pngfile
                except Exception as ex:
                    logger.exception(f"Plotting failed: {ex}")
                    raise

            results.append(item)

        return results

    def extract_area(self, infile: Path) -> Path:
        """
        Main area subsetting method.

        :param infile: Path to input file
        :return: Path to output file
        """
        # Apply bounding box to GRIB file.
        if self.method == "cdo-shellout":
            payload = self.bbox_cdo_shellout(infile)
        elif self.method == "cdo-python":
            payload = self.bbox_cdo_python(infile)
        elif self.method == "xarray":
            payload = self.bbox_xarray(infile)

        # Prepare information about output file.
        if self.use_netcdf:
            folder = "netcdf"
            suffix = ".nc"
        else:
            folder = "grib"
            suffix = None

        # Compute output file location.
        outfolder = self.outfolder.joinpath(folder)
        outfolder.mkdir(parents=True, exist_ok=True)
        outfile = outfolder.joinpath(infile.name)
        if suffix:
            outfile = outfile.with_suffix(suffix)

        # Write output file.
        open(outfile, "wb").write(payload)

        return outfile

    def bbox_cdo_shellout(self, infile: Path) -> bytes:
        """
        Apply bounding box using "cdo".
        Here, we build the command ourselves.

        - https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial
        - https://github.com/mhaberler/docker-dwd-open-data-downloader/blob/003ab3f/extract/Makefile#L53-L62

        :param infile: Path to input file
        :return: Content of output file
        """
        # cdo -sellonlatbox,-180,180,0,90 <infile> <outfile>
        bbox_string = self.bbox.to_string(",", lonlat=True)
        tmpfile = tempfile.NamedTemporaryFile()

        # Compute output format.
        output_format = ""
        # FIXME: That would yield a netCDF file with parameter "2t" instead of "t2m".
        """
        if self.use_netcdf:
            output_format = "--format=nc4"
        """

        command = f"cdo --eccodes --cmor {output_format} sellonlatbox,{bbox_string} '{infile}' '{tmpfile.name}'"
        os.system(command)

        return self.to_grib_or_netcdf(tmpfile.name)

    def bbox_cdo_python(self, infile: Path) -> bytes:
        """
        Apply bounding box using "cdo".
        Here, we use the Python wrapper.

        - https://pypi.org/project/cdo/
        - https://code.mpimet.mpg.de/boards/1/topics/6392

        :param infile: Path to input file
        :return: Content of output file
        """
        import cdo

        bbox_string = self.bbox.to_string(",", lonlat=True)
        cdo = cdo.Cdo()
        # cdo.debug = True
        tmpfile = tempfile.NamedTemporaryFile()
        cdo.sellonlatbox(bbox_string, input=str(infile), output=tmpfile.name)
        return self.to_grib_or_netcdf(tmpfile.name)

    def to_grib_or_netcdf(self, gribfile: str) -> bytes:
        """
        Depending on the configuration of GRIBSubset,
        either return content of GRIB file or convert
        to netCDF-4 format with compression.

        This is needed because the ``--format=nc4`` option of ``cdo``
        would produce a netCDF-4 file with parameter "2t" instead of "t2m".

        :param gribfile: Path to input GRIB file
        :return: Content of output file
        """
        if self.use_netcdf:
            tmpfile_netcdf = tempfile.NamedTemporaryFile()
            command = f"grib_to_netcdf -k 4 -d 6 -o '{tmpfile_netcdf.name}' '{gribfile}'"
            os.system(command)
            outfile = tmpfile_netcdf.name
        else:
            outfile = gribfile

        return open(outfile, "rb").read()

    def bbox_xarray(self, infile: Path) -> bytes:
        """
        Apply bounding box using Xarray.

        - https://xarray.pydata.org/en/stable/generated/xarray.Dataset.where.html
        - https://stackoverflow.com/a/62209490

        FIXME: Needs a patch.
               Currently, Xarray will croak on indexing the Pandas datetime field
               when operating on GRIB2 files.

        :param infile: Path to input file
        :return: Content of output file
        """
        import cfgrib
        import xarray as xr

        ds = xr.open_dataset(infile, engine="cfgrib")
        result = ds.where(
            (ds.latitude >= self.bbox.latitude_min)
            & (ds.latitude <= self.bbox.latitude_max)
            & (ds.longitude >= self.bbox.longitude_min)
            & (ds.longitude <= self.bbox.longitude_max),
            drop=True,
        )
        tmpfile = tempfile.NamedTemporaryFile()
        if self.use_netcdf:
            result.to_netcdf(tmpfile.name)
        else:
            cfgrib.to_grib(result, tmpfile.name)
        return open(tmpfile.name, "rb").read()

    def plot(self, infile: Path) -> Path:
        """
        Plot the outcome using ECMWF Magics.

        TODO: Use custom ``magics.mmap()`` instead of
              ``subpage_map_area_name="central_europe"``
              for better zooming into the area of interest.

        :param infile: Path to input file
        :return: Path to output file
        """
        from Magics import macro as magics

        # Compute outfile location.
        outfolder = self.outfolder.joinpath("png")
        outfolder.mkdir(parents=True, exist_ok=True)
        outfile = outfolder.joinpath(infile.name)
        outfile_real = str(outfile) + ".png"

        # Setting of the output file name
        output = magics.output(
            output_name=str(outfile), output_formats=["png"], output_name_first_page_number="off"
        )

        # Import the data
        if self.use_netcdf:
            # When plotting netCDF, the variable name has to be given.
            netcdf_variable = get_netcdf_main_variable(infile)
            data = magics.mnetcdf(
                netcdf_filename=str(infile), netcdf_value_variable=netcdf_variable
            )
        else:
            data = magics.mgrib(grib_input_file_name=str(infile))

        # Apply an automatic styling
        contour = magics.mcont(contour_automatic_setting="ecmwf")
        coast = magics.mcoast()

        # Select area by coordinates
        # https://github.com/ecmwf/notebook-examples/blob/master/visualisation/tutorials/Subpage-Projections.ipynb
        projection = magics.mmap(
            subpage_map_library_area="on",
            subpage_map_area_name="central_europe",
            page_id_line="off",
        )
        """
        projection = magics.mmap(
            subpage_map_projection="cylindrical",
            subpage_lower_left_latitude=bbox[1] + 15,
            subpage_lower_left_longitude=bbox[0] - 15,
            subpage_upper_right_latitude=bbox[3] + 15,
            subpage_upper_right_longitude=bbox[2] - 15,
        )
        """

        # magics.plot(output, data, contour, projection, coast)
        # magics.plot(output, projection, coast)
        magics.plot(output, projection, data, contour, coast)

        return Path(outfile_real)


def get_netcdf_main_variable(filename: str) -> str:
    """
    Return first variable from netCDF file.
    This is usually what you want.

    Examples:

    >>> f.variables.keys()
    dict_keys(['t2m', 'time', 'step', 'heightAboveGround', 'latitude', 'longitude', 'valid_time'])

    >>> f.variables.keys()
    dict_keys(['u', 'time', 'step', 'isobaricInhPa', 'latitude', 'longitude', 'valid_time'])

    :param filename:
    :return:
    """
    import netCDF4

    nc = netCDF4.Dataset(filename)
    first_variable = list(nc.variables.keys())[0]
    nc.close()
    return first_variable


def setup_logging(level=logging.INFO) -> None:
    """
    Setup Python logging

    :param level:
    :return:
    """
    log_format = "%(asctime)-15s [%(name)-15s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


def json_serializer(obj):
    """
    JSON serializer for custom objects not serializable by default json code
    """

    if isinstance(obj, ProcessingResult):
        return dataclasses.asdict(obj)
    elif isinstance(obj, Path):
        return str(obj)


@click.command(
    help="""
    Extract area of interest from GRIB files using a bounding box.
    
    INPUT can be a single file or a list of files.
    
    For specifying the area of interest, either use "--country" or "--bbox".
    
    """
)
@click.argument("input", type=click.Path(file_okay=True, dir_okay=True), required=True, nargs=-1)
@click.option(
    "--output",
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="The output directory",
    required=True,
)
@optgroup.group("area", cls=RequiredMutuallyExclusiveOptionGroup, help="The area of interest")
@optgroup.option("--country", type=str, help="The country ISO code to derive a bounding box")
@optgroup.option(
    "--bbox",
    type=click.Tuple([float, float, float, float]),
    nargs=4,
    help="The bounding box. Use a space-separated list of 'lat_min lat_max lon_min lon_max'",
    default=(None, None, None, None),
)
@click.option(
    "--method",
    type=click.Choice(["cdo-shellout", "cdo-python", "xarray"], case_sensitive=False),
    help="Which bbox method to use, defaults to cdo-shellout",
    required=False,
    default="cdo-shellout",
)
@click.option("--use-netcdf", is_flag=True, help="Whether to use netCDF", required=False)
@click.option("--plot", is_flag=True, help="Whether to produce png plots", required=False)
def main(
    input: List[str],
    output: str,
    country: str,
    bbox: tuple,
    method: str,
    use_netcdf: bool,
    plot: bool,
):

    # Setup logging.
    setup_logging(level=logging.INFO)

    # Create bounding box from selected area of interest.
    if country:
        bbox = BBox.from_country(country)
    elif bbox:
        bbox = BBox.from_coordinates(bbox)
    logger.info(f"Using bounding box {bbox}")

    # Resolve wildcards from input parameter.
    input_paths = []
    for input_element in input:
        path = glob.glob(input_element, recursive=True)
        input_paths += path

    # Invoke the machinery.
    subgrid = GRIBSubset(
        input=map(Path, input_paths),
        output=output,
        bbox=bbox,
        method=method,
        use_netcdf=use_netcdf,
        plot=plot,
    )
    results = subgrid.process()

    # Report about the outcome.
    print(json.dumps(results, default=json_serializer, indent=4))


if __name__ == "__main__":
    main()
