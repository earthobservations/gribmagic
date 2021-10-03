#############
Xpublish demo
#############


*****
About
*****
Xpublish_ lets you serve/share/publish Xarray Datasets via a web application.

The data and/or metadata in the Xarray Datasets can be exposed in various
forms through pluggable REST API endpoints. Efficient, on-demand delivery
of large datasets may be enabled with Dask on the server-side.

.. _Xpublish: https://xpublish.readthedocs.io/


*****
Setup
*****
::

    # Server dependencies
    pip install xpublish

    # Client dependencies
    pip install fsspec aiohttp zarr


********
Synopsis
********

Server
======
::

    export GM_DATA_PATH=.gribmagic-data
    python demo/publishing/xpublish_server.py $GM_DATA_PATH/tmp/icon_eu_20201220_00_air_temperature_2m_000.grib2
    open http://localhost:9000/


Client
======
::

    python demo/publishing/xpublish_client.py



***************
Troubleshooting
***************

When serving a GRIB file acquired from DWD ICON-EU (``t2m``), Xpublish croaks like::

    INFO:     ::1:61041 - "GET /time/0 HTTP/1.1" 500 Internal Server Error
    ERROR:    Exception in ASGI application
    Traceback (most recent call last):

      File "/Users/amo/dev/earthobservations/gribmagic/.venv/lib/python3.8/site-packages/xpublish/routers/zarr.py", line 74, in get_variable_chunk
        data_chunk = get_data_chunk(da, chunk, out_shape=arr_meta['chunks'])
      File "/Users/amo/dev/earthobservations/gribmagic/.venv/lib/python3.8/site-packages/xpublish/utils/zarr.py", line 167, in get_data_chunk
        raise ValueError(
    ValueError: Invalid chunk_id for numpy array: 0. Should have been: ()

When serving a tutorial dataset, everything works flawlessly::

    python demo/publishing/xpublish_server.py
    python demo/publishing/xpublish_client.py
