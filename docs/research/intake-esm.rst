##########
intake-esm
##########


*****
About
*****
``intake-esm`` is a data cataloging utility built on top
of intake, pandas, and xarray, and it’s pretty awesome!


*******
Details
*******
Computer simulations of the Earth’s climate and weather generate huge amounts
of data. These data are often persisted on HPC systems or in the cloud across
multiple data assets of a variety of formats (netCDF, zarr, etc…).

Finding, investigating, loading these data assets into compute-ready data
containers costs time and effort. The data user needs to know what data sets
are available, the attributes describing each data set, before loading a specific
data set and analyzing it.

Finding, investigating, loading these assets into data array containers such as
xarray can be a daunting task due to the large number of files a user may be
interested in. Intake-esm aims to address these issues by providing necessary
functionality for searching, discovering, data access/loading.


*********
Resources
*********
- https://intake-esm.readthedocs.io/
- https://github.com/intake/intake-esm
- https://github.com/NCAR/esm-collection-spec

Available catalogs
==================
- https://github.com/intake/intake-examples
- https://github.com/NCAR/intake-esm-datastore
- https://github.com/pangeo-data/pangeo-datastore


****
More
****
Intake-esm Release 2020.3.16
- https://ncar.github.io/xdev/posts/intake-esm-2020316/

Tech Talks: Intake - Taking the pain out of data access (2020-09-29)
- https://mpimet.mpg.de/en/science/seminars/seminar-detail?tx_seminars_pi1%5BshowUid%5D=2005
