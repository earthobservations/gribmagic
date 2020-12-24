################################
Area of interest from GRIB files
################################


************
Introduction
************
The `UERRA user training material <http://www.uerra.eu/component/dpattachments/?task=attachment.download&id=357>`_
talks about how to select areas of interest from GRIB files in sections:

- 4. How to cut area of interest?
- 5. How to find right coordinates?

 For computation of regular longitudes and latitudes a Python script of ECMWF can be used.

- https://confluence.ecmwf.int/display/ECC/grib_iterator
- https://confluence.ecmwf.int/display/ECC/grib_nearest

Those two example programs might be helpful::

    python demo/grib_iterator.py .gribmagic-data/tmp/icon_eu_20201219_00_air_temperature_2m_000.grib2
    python demo/grib_nearest.py .gribmagic-data/tmp/icon_eu_20201219_00_air_temperature_2m_000.grib2

.. info::

    See also `Extract data from GRIB/NetCDF for a specific location and time`_.

.. _Extract data from GRIB/NetCDF for a specific location and time: https://confluence.ecmwf.int/pages/viewpage.action?pageId=81014955


************
Bounding box
************

Background
==========
Michael Haberler contributed a `subgrid extraction Makefile`_ which
selects an area from a GRIB file by filtering using a bounding box.
Thanks a stack!

Inspired by that, we created a standalone self-contained implementation
in Python called ``grib_bbox.py``.

.. _subgrid extraction Makefile: https://github.com/mhaberler/docker-dwd-open-data-downloader/commit/af818d72cb2ec608d5850858f3fb28dee79712a8


Synopsis
========
Obtain subset area using bounding box, with plotting::

    # Install cdo.
    brew install cdo

    # For plotting, install Magics.
    # See ``magics.rst``.

    export MAGPLUS_HOME=/usr/local/opt/magics
    export INFILE=.gribmagic-data/tmp/icon_eu_20201220_00_air_temperature_2m_000.grib2
    export OUTDIR=.gribmagic-data/subgrid

    # Austria
    python demo/grib_bbox.py ${INFILE} --output=${OUTDIR} --country=AT --plot

    # Austria: West + Oststeiermark
    python demo/grib_bbox.py ${INFILE} --output=${OUTDIR} --bbox=46.0,47.5,14.5,16.8 --plot

    # Use Xarray for applying the bounding box
    python demo/grib_bbox.py ${INFILE} --output=${OUTDIR} --bbox=46.0 47.5 14.5 16.8 --plot --use-netcdf --method=xarray
