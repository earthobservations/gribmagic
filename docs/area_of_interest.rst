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

> For computation of regular longitudes and latitudes a Python script of ECMWF can be used.

- https://confluence.ecmwf.int/display/ECC/grib_iterator
- https://confluence.ecmwf.int/display/ECC/grib_nearest


********
Examples
********
Those two example programs might be helpful already.
::

    python demo/grib_iterator.py .gribmagic-data/tmp/icon_eu_20201219_00_air_temperature_2m_000.grib2
    python demo/grib_nearest.py .gribmagic-data/tmp/icon_eu_20201219_00_air_temperature_2m_000.grib2
