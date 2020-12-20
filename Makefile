TESTDATA_PATH = $(PWD)/.gribmagic-testdata

download-testdata:
	mkdir -p $(TESTDATA_PATH)
	wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2 \
	    --directory-prefix $(TESTDATA_PATH) --no-clobber
	wget https://github.com/earthobservations/testdata/raw/main/data.knmi.nl/download/harmonie_arome_cy40_p1/0.2/harm40_v1_p1_2019061100-single.tar \
	    --directory-prefix $(TESTDATA_PATH) --no-clobber

test: download-testdata
	rm tests/modules/download/fixtures/* || true
	pytest tests
