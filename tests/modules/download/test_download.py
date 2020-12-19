import re
import os
from pathlib import Path
import responses

from gribmagic.enumerations.weather_models import WeatherModels
from gribmagic.modules.config.constants import KEY_LOCAL_FILE_PATHS,\
    KEY_REMOTE_FILE_PATHS, KEY_LOCAL_STORE_FILE_PATHS, KEY_COMPRESSION
from gribmagic.modules.download.download import __download_parallel, __download, \
    download, __download_tar_file
from gribmagic.modules.config.configurations import MODEL_CONFIG as test_config

test_config[WeatherModels.ICON_EU.value][KEY_COMPRESSION] = ''

input_file = f"{os.getcwd()}/tests/modules/download/fixtures/" \
             f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2"
output_file = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                   'air_temperature_2m.grib2')


@responses.activate
def test___download():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(input_file, "rb"),
        stream=True,
    )

    __download((WeatherModels.ICON_EU,
                output_file,
                Path('test', 'mock')))

    assert output_file.is_file() is True

    os.remove(output_file)


@responses.activate
def test___download_parallel():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(input_file, "rb"),
        stream=True,
    )

    __download_parallel([(WeatherModels.ICON_EU,
                output_file,
                Path('test', 'mock'))])

    assert output_file.is_file() is True

    os.remove(output_file)


@responses.activate
def test_download_store():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.ICON_EU,
             {KEY_LOCAL_FILE_PATHS: [output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert output_file.is_file() is True
    os.remove(output_file)


@responses.activate
def test_download_store_parallel():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.ICON_EU,
             {KEY_LOCAL_FILE_PATHS: [output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]},
             parallel_download=True)

    assert output_file.is_file() is True

    os.remove(output_file)

"""
@patch(
    'gribmagic.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"fixture.tar",
              'rb')
    )
)
@patch(
    'gribmagic.modules.download.download.MODEL_CONFIG',
    MagicMock(
        return_value=test_config
    )
)
def test_download_store_tarfile():
    tarfile_output = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                   'harmonie_knmi_20200711_00_0.grib')
    download(WeatherModels.HARMONIE_KNMI,
             {KEY_LOCAL_FILE_PATHS: [tarfile_output],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert tarfile_output.is_file() is True
    os.remove(tarfile_output)


@patch(
    'gribmagic.modules.download.download.urlopen',
    MagicMock(
        return_value=open(f"{os.getcwd()}/tests/modules/download/fixtures/"
              f"fixture.tar",
              'rb')
    )
)
def test___download_tar_file():
    tarfile_output = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures',
                   'harmonie_knmi_20200711_00_0.grib')
    __download_tar_file(WeatherModels.HARMONIE_KNMI, Path('test', 'mock'), [tarfile_output])

    assert tarfile_output.is_file() is True
    os.remove(tarfile_output)
"""
