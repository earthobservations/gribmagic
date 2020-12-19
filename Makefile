export BASE_STORE_DIR=/app/data
export MODEL_CONFIG=config/model_config.yml
export MODEL_VARIABLES_MAPPING=config/model_variables_mapping.yml
export MODEL_VARIABLES_LEVELS_MAPPING=config/model_variables_levels_mapping.yml

download-testdata:
	rm tests/modules/download/fixtures/*
	wget https://github.com/earthobservations/testdata/raw/main/opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2 \
	    --directory-prefix tests/modules/download/fixtures/

test: download-testdata
	pytest tests
