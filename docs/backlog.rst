#################
GribMagic backlog
#################


******
Prio 1
******
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
- [o] Maybe use model name as subdirectory for storing data
- [o] Large code refactoring
- [o] Improve README
- [o] Improve sandbox (just type ``make test``)
- [o] CI: Add test matrix for Python 3.7, 3.8 and 3.9
- [o] Add type hints for return values from "download-xyz" functions
- [o] Release on PyPI


******
Prio 2
******
- [o] Ask Daniel for missing commits aac0f51, 6eac45e, 95c0662 re. "Fix KNMI download via API"
- [o] ``--dry-run`` parameter, just printing the URLs
- [o] Integrate dwd-data-downloader
- [o] Add CLI module based on Typer
- [o] Unlock ICON-D2
- [o] Download only specific parameters

- [o] Implement "model-level" downloads (#2)
- [o] Implement "model-level" vs. "pressure-level" downloads (#3)
- [o] Implement "regular-lat-lon" vs. "rotated-lat-lon" downloads (#4)
- [o] Notify upstream about troubles with SkinnyWMS and Xpublish

- [o] Regridding
  - https://github.com/jbusecke/cmip6_preprocessing/issues/38

- [o] Improve documentation
    - https://www.nco.ncep.noaa.gov/pmb/products/gfs/
    - http://dcpc-nwp.meteo.fr/
    - https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gefs.php
    - https://en.wikipedia.org/wiki/National_Centers_for_Environmental_Prediction
    - https://gsl.noaa.gov/focus-areas/unified_forecast_system
    - https://vlab.noaa.gov/web/environmental-modeling-center/unified-forecast-system
    - https://ufscommunity.org/
    - https://ufscommunity.org/about/what-is-ufs/
    - https://ufscommunity.org/news/srwa/

- [o] Complete products
    - AROME has more grid resolutions

- [o] Add more models
    - https://de.wikipedia.org/wiki/Numerische_Wettervorhersage#Modelle


******
Prio 3
******
- [o] Scheduling
- [o] Unlock ERA5 and TIGGE
- [o] Convert to JSON or CSV
    - https://github.com/DeutscherWetterdienst/python-eccodes#example-4-extract-data-from-grib-file-as-json
    - https://github.com/DeutscherWetterdienst/python-eccodes#example-3-extract-data-from-grib-file-as-csv
    - https://confluence.ecmwf.int/display/CKB/How+to+convert+GRIB+to+CSV
- [o] Convert to netCDF
- [o] Integrate regridding
    - https://github.com/DeutscherWetterdienst/regrid
    - https://confluence.ecmwf.int/display/CKB/How+to+plot+GRIB+files+with+Python+and+matplotlib
- [o] Include Magics, CDO and more into Docker image
    - https://code.mpimet.mpg.de/projects/cdo
    - https://github.com/DeutscherWetterdienst/python-eccodes
- [o] Add plotting with cf-plot.
    - https://ajheaps.github.io/cf-plot/
    - https://github.com/ajheaps/cf-plot
- [o] Movies
  - https://github.com/jbusecke/xmovie


*****
Ideas
*****
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
