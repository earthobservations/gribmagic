# -------------
# Configuration
# -------------

$(eval venvpath     := .venv)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval pytest       := $(venvpath)/bin/pytest)
$(eval black        := $(venvpath)/bin/black)
$(eval isort        := $(venvpath)/bin/isort)


MAGICS_PREFIX = /usr/local/opt/magics
PATH_TESTDATA_INPUT = $(PWD)/.gribmagic-testdata/input
PATH_TESTDATA_OUTPUT = $(PWD)/.gribmagic-testdata/output

testdata-download:
	mkdir -p $(PATH_TESTDATA_INPUT)
	mkdir -p $(PATH_TESTDATA_OUTPUT)
	wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2 \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber
	wget https://github.com/earthobservations/testdata/raw/main/data.knmi.nl/download/harmonie_arome_cy40_p1/0.2/harm40_v1_p1_2019061100-single.tar \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber
	wget https://github.com/earthobservations/testdata/raw/main/nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20211004/00/atmos/gfs.t00z.pgrb2.1p00.f000 \
	    --directory-prefix $(PATH_TESTDATA_INPUT) --no-clobber

testoutput-clean:
	rm $(PATH_TESTDATA_OUTPUT)/* || true

test: testdata-download testoutput-clean
	@$(pytest) -vvv tests

test-coverage: testdata-download testoutput-clean
	@$(pytest) -vvv tests \
		--cov=gribmagic \
		--cov-report=term-missing \
		--cov-report=xml

format:
	@$(pip) install --requirement=requirements-dev.txt --quiet
	$(isort) --profile=black gribmagic tests
	$(black) gribmagic tests

install-magics:
	mkdir -p tmp/download tmp/build/magics
	wget https://confluence.ecmwf.int/download/attachments/3473464/Magics-4.5.2-Source.tar.gz \
	    --directory-prefix=tmp/download --no-clobber
	cd tmp/download; tar -xzf Magics-4.5.2-Source.tar.gz
	cd tmp/build/magics; \
	    cmake -DCMAKE_INSTALL_PREFIX=$(MAGICS_PREFIX) ../../download/Magics-4.5.2-Source; \
	    make -j8 && make install

install-skinnywms-macos-10-13:
	wget https://files.pythonhosted.org/packages/e9/2f/28cdbfbf7165d89c4c574babe7ac12e994266e03fe3cae201d63cc0f471a/ecmwflibs-0.0.94-cp38-cp38-macosx_10_14_x86_64.whl
	mv ecmwflibs-0.0.94-cp38-cp38-macosx_10_14_x86_64.whl ecmwflibs-0.0.94-cp38-cp38-macosx_10_13_x86_64.whl
	pip install ecmwflibs-0.0.94-cp38-cp38-macosx_10_13_x86_64.whl
	pip install skinnywms
	pip uninstall ecmwflibs
	rm ecmwflibs-0.0.94-cp38-cp38-macosx_10_13_x86_64.whl

install-dwd-grib-downloader:
	git clone --branch=amo/develop https://github.com/earthobservations/dwd-grib-downloader tools/dwd-grib-downloader || \
	    (cd tools/dwd-grib-downloader && git pull)
