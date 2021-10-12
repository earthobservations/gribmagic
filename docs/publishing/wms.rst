##############
SkinnyWMS demo
##############


*****
About
*****
SkinnyWMS_ is a lightweight `Web Map Service (WMS)`_ server for serving
maps of netCDF and GRIB data.

It will help you to visualise your NetCDF and Grib Data. The principle
is simple: Skinny will browse the directory or the single file passed
as command line argument, and try to interpret all NetCDF or GRIB files.

.. _SkinnyWMS: https://github.com/ecmwf/skinnywms
.. _Web Map Service (WMS): https://en.wikipedia.org/wiki/Web_Map_Service


*****
Setup
*****

Install ECMWF Magics
====================
SkinnyWMS depends on the ECMWF Magics library, see ``magics.rst``.

Install SkinnyWMS
=================
::

    # Server dependencies
    pip install skinnywms

    # Client dependencies
    pip install owslib


When still on macOS 10.13 (High Sierra), use::

    install-skinnywms-macos-10-13


********
Synopsis
********

Server
======
::

    export MAGPLUS_HOME=/usr/local/opt/magics
    skinny-wms --path=.gribmagic-data/raw
    open http://localhost:5000/


Client
======
::

    python demo/publishing/wms_client.py


***************
Troubleshooting
***************
::

    Traceback (most recent call last):
      File "/Users/amo/dev/earthobservations/gribmagic/.venv/lib/python3.8/site-packages/owslib/map/wms111.py", line 447, in __init__
        float(b.attrib['minx']),
    ValueError: could not convert string to float: ''

::

    <!-- http://127.0.0.1:5000/wms?service=WMS&request=GetCapabilities&version=1.1.1 -->
    <Layer>
      <BoundingBox CRS="EPSG:4326" minx="" miny="" maxx="" maxy=""/>
      <BoundingBox CRS="EPSG:3857" minx="" miny="" maxx="" maxy=""/>
      <BoundingBox CRS="EPSG:32661" minx="" miny="" maxx="" maxy=""/>
    </Layer>

    <!-- https://www.pegelonline.wsv.de/webservices/gis/wms/aktuell/nswhsw?request=GetCapabilities&service=WMS&version=1.1.1 -->
    <Layer>
      <BoundingBox SRS="EPSG:31467"
                   minx="3.25047e+06" miny="5.22116e+06" maxx="3.94202e+06" maxy="6.1139e+06" />
    </Layer>
