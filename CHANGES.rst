###################
GribMagic changelog
###################


in progress
===========
- CI: Parallelize test execution using `pytest-xdist`


2021-10-24 0.2.0
================
- [dwd] Integrate DWD GRIB Downloader as ``gribmagic dwd acquire`` subcommand
- [dwd] Add command to install the DWD GRIB Downloader at runtime:
  ``gribmagic install dwd-grib-downloader``.
- [dwd] Accept ``gribmagic dwd acquire`` without ``--timestamp`` parameter.
  When the timestamp is omitted, the most recent available modelrun is used.
- [tool] Add subcommand ``gribmagic smith bbox``, in order to extract an area of
  interest from GRIB files using a bounding box, or a two-letter country code.
- [tool] Add subcommand ``gribmagic smith regrid``, in order to transform DWD ICON's
  icosahedral-gridded files into regular grids in ``long1`` format.


2021-10-18 0.1.0
================
- Remove ecCodes definitions files
- Remove large test fixture files
- CI: Run software tests on GHA
- Fix parallel downloads wrt. to unit tests
- Working on some demo programs
- Improve core download routine
- Rename toplevel package namespace
- Refactor access to weather model definition into single model class
- Streamline sanity checking for remote grib directories vs. packages
- DWD ICON: Rename parameter "aswdiff_s" to "aswdifd_s"
- Add demo programs to get nearest grid point(s) to given geolocation
- Slightly refactor GribMagic data model
- Refine processing for tar archive based data and tests for KNMI HARMONIE
- Improve error reporting for incomplete mappings
- ICON-EU-EPS: Adjust variables list
    - Has no "surface_specific_humidity"
    - Has only "max_wind_gust_10m"
- COSMO-D2: Adjust variables list
    - Has no "convective_snow" and "convective_rain"
- ICON-EU-EPS: Adjustments to weather model settings
    - Has no "*_rain" parameters
      This has neither "convective_rain" nor "grid_scale_rain"
    - Add mapping entry to variables->levels mapping
- Move original gribmagic implementation to gribmagic.unity
- Fix acquisition for NOAA NCEP GFS
- Add acquisition for NOAA NCEP GFS data in 0.5 and 1.0 degree resolutions
- Return results from downloader routines in order to be able to verify it
- Improve testing
- Improve documentation
- Get rid of "tmp" subdirectory within target directory
- Refactor remote URL model configuration and building
- More consistent naming for data source labels
- Run "isort" and "black"
- Add "gribmagic unity list" subcommand
- Obtain target directory from command line parameter "--target"
- Large module refactoring
- Improve project infrastructure
- Resolve "download_specification" tuple into dataclass


2020-08-13 0.0.0
================
- Initial commit
- Add tests and fix bug with key naming
- Improve download and add parallel downloading
- CI: Add testing and code coverage reporting
- Add software tests for important subsystems
- Correct Enumeration of cosmo-d2
- Add model "meteo-france-arome"
- Add inheritance for config
- Add model "icon-global"
- Add more variables and models
- Add GFS model download
- Add first thoughts about harmonie arome
- Add additional eccodes definitions
- Add variable mapping for KNMI harmonie and add eccodes defintions path
- Add handling of multiple variables files
- Introduce ThreadPoolExecutor
- Various small adaptions for EPS download from german weather service
- Using ProccessPoolExecutor instead of ThreadPoolExecutor
- Adjust AROME download
