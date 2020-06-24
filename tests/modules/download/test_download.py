from unittest.mock import patch, MagicMock
import os
from pathlib import Path

from src.enumerations.weather_models import WeatherModels
from src.modules.config.constants import KEY_LOCAL_FILE_PATHS,\
    KEY_REMOTE_FILE_PATHS, KEY_LOCAL_STORE_FILE_PATHS
from src.modules.download.download import __download_parallel, __download, \
    download


output_file = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                   'air_temperature_2m.grib2')


@patch(
    'src.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb')
    )
)
def test___download():
    __download((WeatherModels.ICON_EU,
                output_file,
                Path('test', 'mock')))

    assert output_file.is_file() is True

    os.remove(output_file)


@patch(
    'src.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb')
    )
)
def test___download_parallel():
    __download_parallel([(WeatherModels.ICON_EU,
                output_file,
                Path('test', 'mock'))])

    assert output_file.is_file() is True

    os.remove(output_file)


@patch(
    'src.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb')
    )
)
def test_download_bunzip():
    download(WeatherModels.ICON_EU,
             {KEY_LOCAL_FILE_PATHS: [output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert output_file.is_file() is True

    os.remove(output_file)


@patch(
    'src.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2",
              'rb')
    )
)
def test_download_store():
    download(WeatherModels.ICON_EU,
             {KEY_LOCAL_FILE_PATHS: [output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert output_file.is_file() is True

    os.remove(output_file)
