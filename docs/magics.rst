######
Magics
######


*****
About
*****
Magics is ECMWF's meteorological plotting software.

Magics supports the plotting of contours, wind fields, observations,
satellite images, symbols, text, axis and graphs (including boxplots).
Data fields to be plotted may be presented in various formats, for
instance GRIB 1 and 2 code data, gaussian grid, regularly spaced grid
and fitted data. GRIB data is handled via ECMWF's ecCodes software.

Input data can also be in BUFR and NetCDF format or retrieved from an
ODB database. The produced meteorological plots can be saved in various
formats, such as PostScript, EPS, PDF, GIF, PNG and SVG.

Magics uses the Terralib library in cooperation with Brazil's INPE.

- https://confluence.ecmwf.int/display/MAGP
- https://pypi.org/project/Magics/


*****
Setup
*****
::

    brew install eccodes
    wget https://confluence.ecmwf.int/download/attachments/3473464/Magics-4.5.2-Source.tar.gz
    tar -xzf Magics-4.5.2-Source.tar.gz

    cd /tmp/build
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local/opt/magics ~/Downloads/Magics-4.5.2-Source
    make -j8
    make install


****
Demo
****
::

    pip install Magics

    export MAGPLUS_HOME=/usr/local/opt/magics
    python -m Magics selfcheck

    wget http://download.ecmwf.int/test-data/magics/2m_temperature.grib
    python demo/magics.py 2m_temperature.grib
    open magics.png
