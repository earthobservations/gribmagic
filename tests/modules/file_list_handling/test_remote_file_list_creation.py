from src.modules.file_list_handling.remote_file_list_creation import \
    build_remote_file_lists_for_variable_files
from src.enumerations.weather_models import WeatherModels
from datetime import datetime
from pathlib import Path


def test_build_model_file_lists():
    to_test = build_remote_file_lists_for_variable_files(WeatherModels.TEST,
                           0,
                           datetime(2020, 6, 10).date())
    assert to_test == [Path('test1/test_remote_dir/00/t2m/test_remote_file_single-level_2020061000_000_T2M.grib2.bz2'),
                       Path('test1/test_remote_dir/00/t2m/test_remote_file_single-level_2020061000_001_T2M.grib2.bz2')]