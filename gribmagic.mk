#MAGICS_VERSION ?= 4.2.6
#MAGICS_VERSION ?= 4.5.2
MAGICS_VERSION ?= 4.9.3
MAGICS_PREFIX = /usr/local/opt/magics-${MAGICS_VERSION}
PATH_TESTDATA_INPUT = $(PWD)/.gribmagic-testdata/input
PATH_TESTDATA_OUTPUT = $(PWD)/.gribmagic-testdata/output

testdata-download:
	@echo "===================="
	@echo "Downloading testdata"
	@echo "===================="
	mkdir -p $(PATH_TESTDATA_INPUT)
	mkdir -p $(PATH_TESTDATA_OUTPUT)
	wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon/grib/18/t/icon-global_regular-lat-lon_air-temperature_level-90.grib2 \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber
	wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2 \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber
	wget https://github.com/earthobservations/testdata/raw/main/data.knmi.nl/download/harmonie_arome_cy40_p1/0.2/harm40_v1_p1_2019061100-single.tar \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber
	wget https://github.com/earthobservations/testdata/raw/main/nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20211004/00/atmos/gfs.t00z.pgrb2.1p00.f000 \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber
	@echo

testoutput-clean:
	@echo "===================="
	@echo "Cleaning output data"
	@echo "===================="
	rm $(PATH_TESTDATA_OUTPUT)/* || true
	@echo

magics-install:
	# Downloads and install Magics release from https://confluence.ecmwf.int/display/MAGP/Releases.
	# Needs `apt-get install --yes build-essential cmake libeccodes-dev libeccodes-tools libproj-dev libexpat-dev libcairo2-dev libpangocairo-1.0-0`.
	$(eval TMP := tmp/magics)
	mkdir -p ${TMP}/download ${TMP}/build/${MAGICS_VERSION}
	wget https://confluence.ecmwf.int/download/attachments/3473464/Magics-${MAGICS_VERSION}-Source.tar.gz \
	    --directory-prefix=${TMP}/download --no-clobber
	cd ${TMP}/download; \
	    tar -xzf Magics-${MAGICS_VERSION}-Source.tar.gz
	cd ${TMP}/build/${MAGICS_VERSION}; \
	    cmake \
	        -DCMAKE_INSTALL_PREFIX=${MAGICS_PREFIX} \
	        -DPYTHON_EXECUTABLE=$(shell which python3) \
	        -DENABLE_TESTS=off \
	        ../../download/Magics-${MAGICS_VERSION}-Source; \
	    make -j8 && make install

magics-info:
	@echo "=================="
	@echo "Magics information"
	@echo "=================="

	@printf "Selfcheck: "
	@$(python) -m Magics selfcheck || true
	@printf ""

	@printf "Version: "
	@$(python) -c "import Magics; print(Magics.version().decode())" || true
	@printf ""

	@printf "Module: "
	@$(python) -c "import Magics; print(Magics.__file__)" || true
	@printf ""

	@printf "Library: "
	@$(python) -c "import Magics; print(Magics.dll)" || true
	@printf ""

	@echo

install-skinnywms-macos-10-13:
	wget https://files.pythonhosted.org/packages/e9/2f/28cdbfbf7165d89c4c574babe7ac12e994266e03fe3cae201d63cc0f471a/ecmwflibs-0.0.94-cp38-cp38-macosx_10_14_x86_64.whl
	mv ecmwflibs-0.0.94-cp38-cp38-macosx_10_14_x86_64.whl ecmwflibs-0.0.94-cp38-cp38-macosx_10_13_x86_64.whl
	pip install ecmwflibs-0.0.94-cp38-cp38-macosx_10_13_x86_64.whl
	pip install skinnywms
	pip uninstall ecmwflibs
	rm ecmwflibs-0.0.94-cp38-cp38-macosx_10_13_x86_64.whl
