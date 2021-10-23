#################
GribMagic backlog
#################


******
Prio 1
******
- [o] Complete pipeline demos
- [o] Integrate regridding
    - https://github.com/jbusecke/cmip6_preprocessing/issues/38
    - https://github.com/DeutscherWetterdienst/regrid
    - https://confluence.ecmwf.int/display/CKB/How+to+plot+GRIB+files+with+Python+and+matplotlib
- [o] Maybe use model name as subdirectory for storing data
- [o] Ask Daniel for missing commits aac0f51, 6eac45e, 95c0662 re. "Fix KNMI download via API"
- [o] Implement "model-level" downloads (#2)
- [o] Implement "model-level" vs. "pressure-level" downloads (#3)
- [o] Implement "regular-lat-lon" vs. "rotated-lat-lon" downloads (#4)
- [o] Automatically build and publish Docker images
- [o] Integrate dwd-data-downloader
- [o] Fill gaps from some products
    - AROME has more grid resolutions

- [o] ``gribmagic info``::

        - Versions of Numpy, cfgrib, xarray, Dask
        - Magics version: Magics.version().decode()
        - cdo and eccodes versions
- [o] Load asset files from different directory than ``appdirs_user()``.
- [o] GFS API: https://github.com/jagoosw/getgfs



******
Prio 2
******
- [o] Add ``gribmagic install magics``
- [o] Integrate ``demo/grib_bbox.py``
- [o] Add type hints for return values from "download-xyz" functions
- [o] ``--dry-run`` parameter, just printing the index files and URLs
- [o] Notify upstream about troubles with SkinnyWMS and Xpublish
- [o] Improve documentation
    - https://www.nco.ncep.noaa.gov/pmb/products/gfs/
    - http://dcpc-nwp.meteo.fr/
    - https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gefs.php
    - https://en.wikipedia.org/wiki/National_Centers_for_Environmental_Prediction
- [o] Add more NWP models
    - https://de.wikipedia.org/wiki/Numerische_Wettervorhersage#Modelle
    - UFS
        - https://gsl.noaa.gov/focus-areas/unified_forecast_system
        - https://vlab.noaa.gov/web/environmental-modeling-center/unified-forecast-system
        - https://ufscommunity.org/
        - https://ufscommunity.org/about/what-is-ufs/
        - https://ufscommunity.org/news/srwa/
    - Unlock ERA5 and TIGGE
- [o] Implement ``gribmagic/unity/modules/parsing/unify_data.py``
- [o] What about https://opendata.dwd.de/weather/lib/grib/eccodes_definitions.edzw-2.22.1-1.tar.bz2 ?
- [o] Elevation data from https://github.com/bopen/elevation?


******
Prio 3
******
- [o] Convert to JSON or CSV
    - https://github.com/DeutscherWetterdienst/python-eccodes#example-4-extract-data-from-grib-file-as-json
    - https://github.com/DeutscherWetterdienst/python-eccodes#example-3-extract-data-from-grib-file-as-csv
    - https://confluence.ecmwf.int/display/CKB/How+to+convert+GRIB+to+CSV
- [o] Convert to netCDF
- [o] Include Magics, CDO and more into Docker image
    - https://code.mpimet.mpg.de/projects/cdo
    - https://github.com/DeutscherWetterdienst/python-eccodes


*****
Ideas
*****
- [o] Add plotting with cf-plot.
    - https://ajheaps.github.io/cf-plot/
    - https://github.com/ajheaps/cf-plot
- [o] Movies
  - https://github.com/jbusecke/xmovie
- [o] Alerts
  - https://community.windy.com/topic/9760/would-you-like-to-receive-windy-alerts-as-push-notifications-to-your-mobile-device?lang=en-US
  - https://community.windy.com/topic/8268/windy-alert-notification-for-cap-alerts-weather-warnings
- [o] Process data with WebAssembly program
- [o] Look at OEP/RLI
    - https://github.com/OpenEnergyPlatform/data-preprocessing/issues/47
    - https://github.com/OpenEnergyPlatform/data-preprocessing/blob/review/openfred/data-review/climate.openfred_weatherdata_locations.json
- [o] Look at atlite
    - https://github.com/PyPSA/atlite
- [o] Improve plotting
  https://github.com/willyhagi/climate-data-science/blob/master/Python-Scripts/cartopy_plot.py


****
Done
****
- [x] Add CLI module based on Click
- [x] Fix mismatching mappings
- [x] Add some demo programs for data (re-)publishing
- [x] Add demo program for selecting area of interest based on bounding box
- [x] Inline default mapping YAML files into package
- [x] Improve test coverage and reactivate Codecov uploads
- [x] Get rid of ``tmp`` subdirectory
- [x] Get rid of ``remote_server_type``
- [x] Flip "Product » Provider" to "Provider » Product"
- [x] Run ``isort`` and ``black``
- [x] Obtain target directory from command line parameter
- [x] Large code refactoring
- [x] Resolve download_specification[0] / [1] / [2]
- [x] Improve README
- [x] Improve sandbox (just type ``make test``)
- [x] CI: Add test matrix for Python 3.7, 3.8 and 3.9
- [x] Release on PyPI
- [x] Integrate ``demo/pipeline/pipeline.py``, the wrapper around ``opendata-downloader.py``
      into ``gribmagic.dwd`` module and as ``gribmagic dwd acquire`` subcommand.
- [x] Unlock ICON-D2
- [x] Download only specific parameters
- [x] Use most recent modelrun
