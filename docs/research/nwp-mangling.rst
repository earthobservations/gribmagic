#################
NWP data mangling
#################



********
Decoding
********
- https://confluence.ecmwf.int/display/ECC/High-level+Pythonic+Interface+in+ecCodes


**********
Conversion
**********
- https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial
- https://github.com/DeutscherWetterdienst/python-eccodes#example-4-extract-data-from-grib-file-as-json
- https://github.com/f24-it-services/grib2json


**********
Processing
**********

Extraction and manipulation
===========================
Utils on top of pygrib for extracting metadata and manipulating grib files.

-- https://github.com/innovationgarage/gributils


Regridding
==========
- https://www.dwd.de/DE/leistungen/opendata/help/modelle/Opendata_cdo_EN.pdf?__blob=publicationFile
- https://github.com/DeutscherWetterdienst/regrid
- https://code.mpimet.mpg.de/projects/cdo
- https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/
- https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/wgrib2m.html
- https://xesmf.readthedocs.io/
  https://github.com/esmf-org/esmf/blob/develop/src/addon/ESMPy/README.md#regridding-overview
  https://github.com/JiaweiZhuang/xESMF
  https://github.com/esmf-org/esmf
  https://web.archive.org/web/20170609183629/https://earthsystemcog.org/projects/cog/
- http://www.matteodefelice.name/post/c3s-multimodel/
- https://confluence.ecmwf.int/display/CKB/Transformation+or+regridding+of+ECMWF+Reanalyses+data
- https://climatedataguide.ucar.edu/climate-data-tools-and-analysis/regridding-overview


Geographical area of interest
=============================
- http://www.uerra.eu/component/dpattachments/?task=attachment.download&id=357
- https://confluence.ecmwf.int/display/CUSF/New+geographical+area+selection+widget+for+the+CAMS+Global+reanalysis+%28EAC4%29+data
- https://confluence.ecmwf.int/rest/ecmwfjsd/1.0/exporthtml/page?pageId=7374660
- https://confluence.ecmwf.int/display/ECC/GRIB+examples
- https://sites.ecmwf.int/docs/eccodes/group__iterators.html
- https://confluence.ecmwf.int/display/ECC/grib_iterator
- https://confluence.ecmwf.int/display/ECC/grib_iterator_bitmap


*************
Remote access
*************
- https://github.com/pangeo-data/pangeo-datastore/tree/master/intake-catalogs
- https://colab.research.google.com/drive/19iEVxE_9QoTeg4st7MmucHJUmO93NXHp#scrollTo=OhT9-yB2OziD
- https://medium.com/pangeo/cloud-performant-netcdf4-hdf5-with-zarr-fsspec-and-intake-3d3a3e7cb935
- https://github.com/ecmwf/cfgrib/issues/189
