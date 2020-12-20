download-testdata:
	rm tests/modules/download/fixtures/* || true
	wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2 \
	    --directory-prefix tests/modules/download/fixtures/

test: download-testdata
	pytest tests