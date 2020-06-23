from src.modules.file_list_handling.file_list_handling import build_model_file_lists
from src.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path


def test_build_model_file_lists():
    to_test = build_model_file_lists(WeatherModels.TEST,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == \
           {'local_file_paths': [Path('/app/data/tmp/test_model_20200610_00_air_temperature_2m_0.grib'),
                               Path('/app/data/tmp/test_model_20200610_00_air_temperature_2m_1.grib')],
            'remote_file_paths': [Path('test1/test_remote_dir/00/t2m/test_remote_file_single-level_2020061000_000_T2M.grib2.bz2'),
                                  Path('test1/test_remote_dir/00/t2m/test_remote_file_single-level_2020061000_001_T2M.grib2.bz2')],
            'local_store_file_paths': [Path('/app/data/test_model/20200610_00/air_temperature_2m.nc')]
            }
