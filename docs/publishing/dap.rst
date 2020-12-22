########
DAP demo
########


*****
About
*****
The Data Access Protocol (DAP) is intended to enable remote,
selective data-retrieval as an easily invoked Web service.
The protocol is layered on top of HTTP and its current
specification is DAP4_. DAP is used specifically in Earth sciences.

OPeNDAP_ stands for "Open-source Project for a Network Data Access Protocol".
OPeNDAP is both the name of a non-profit organization and the commonly-used
name of a protocol which the OPeNDAP organization has developed.

The `Hyrax Data Server`_ is the next generation DAP server from OPeNDAP.
It utilizes a modular design that employs a light weight Java servlet (OLFS)
to provide the public-accessible client interface and a backend daemon (BES)
to handle the heavy lifting.

Pydap_ is an implementation of the OPeNDAP/DODS protocol, written from
scratch in pure python. You can use pydap to access scientific data
on the internet without having to download it; instead, you work with
special array and iterable objects that download data on-the-fly as
necessary, saving bandwidth and time.

.. _DAP4: https://docs.opendap.org/index.php/DAP4_Specification
.. _OPeNDAP: https://en.wikipedia.org/wiki/OPeNDAP
.. _Hyrax Data Server: https://www.opendap.org/software/hyrax-data-server
.. _Pydap: https://github.com/pydap/pydap


*****
Setup
*****
We recommend the Pydap fork by `@jblarsen`_. It doesn't have any troubles.
::

    # Client dependencies
    pip install git+https://github.com/jblarsen/pydap.git#egg=pydap[handlers.netcdf]

    # Server dependencies
    pip install git+https://github.com/jblarsen/pydap.git#egg=pydap[server,handlers.netcdf] gunicorn==19.10.0

.. _@jblarsen: https://github.com/jblarsen


********
Synopsis
********


Data format
===========
DAP works with netCDF (``.nc``) and DMR++ (``.dmrpp``) files,
so GRIB files will have to be converted beforehand.

ECMWF's `ecCodes software`_ ships appropriate tools,
specifically grib_to_netcdf_. See also `How to convert GRIB to netCDF`_.
::

    export BASE_STORE_DIR=.gribmagic-data
    grib_to_netcdf -k 4 \
        -o ${BASE_STORE_DIR}/netcdf/icon_eu_20201220_00_air_temperature_2m_000.nc \
        ${BASE_STORE_DIR}/tmp/icon_eu_20201220_00_air_temperature_2m_000.grib2

.. _ecCodes software: https://confluence.ecmwf.int/display/ECC
.. _How to convert GRIB to netCDF: https://confluence.ecmwf.int/display/OIFS/How+to+convert+GRIB+to+netCDF
.. _grib_to_netcdf: https://confluence.ecmwf.int/display/ECC/grib_to_netcdf


Server (Hyrax)
==============
In this example, we are using the `Hyrax Docker`_ distribution.

Run::

    export BASE_STORE_DIR=.gribmagic-data

    docker run \
        --rm --interactive --tty \
        --publish 4000:8080 \
        --env NCWMS_BASE=http://localhost:4000 \
        --volume $(pwd)/${BASE_STORE_DIR}/netcdf:/usr/share/hyrax \
        opendap/hyrax:latest

    open http://localhost:4000/

.. _Hyrax Docker: https://github.com/OPENDAP/hyrax-docker


Server (Pydap)
==============
::

    export BASE_STORE_DIR=.gribmagic-data
    pydap --data=${BASE_STORE_DIR}/netcdf --port=4000


Client (Xarray)
===============
::

    # Hyrax server
    python demo/publishing/dap_client_xarray.py http://localhost:4000/opendap/icon_eu_20201220_00_air_temperature_2m_000.nc

    # Pydap server
    python demo/publishing/dap_client_xarray.py http://localhost:4000/icon_eu_20201220_00_air_temperature_2m_000.nc


Client (Pydap)
==============
::

    # Hyrax server
    python demo/publishing/dap_client_pydap.py http://localhost:4000/opendap/icon_eu_20201220_00_air_temperature_2m_000.nc

    # Pydap server
    python demo/publishing/dap_client_pydap.py http://localhost:4000/icon_eu_20201220_00_air_temperature_2m_000.nc


*********
Resources
*********
More client examples written in Python based on Xarray can be found at:
https://github.com/OPENDAP/hyrax/tree/master/python-xarray


***************
Troubleshooting
***************

TLDR; Just use the fork maintained by `@jblarsen`_.

.. seealso::

    https://github.com/pydap/pydap/issues/212#issuecomment-748651835


Details
=======

https://github.com/pydap/pydap/issues/167::

    UnicodeDecodeError: 'ascii' codec can't decode byte 0x8b in position 1: ordinal not in range(128)

https://github.com/pydap/pydap/issues/197::

    pydap.exceptions.ExtensionNotSupportedError: 'No handler available for file /path/to/icon_eu_20201220_00_air_temperature_2m_000.nc.'

https://github.com/pydap/pydap/issues/217::

    ValueError: cannot reshape array of size 16 into shape (1,657,1097)



*********
Resources
*********
This topic is also discussed at:
- https://github.com/earthobservations/wetterdienst/discussions/287#discussioncomment-223753 ff.
