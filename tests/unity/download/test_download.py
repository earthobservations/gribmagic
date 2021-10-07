import re
import os
from pathlib import Path
import responses

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.modules.config.constants import KEY_LOCAL_FILE_PATHS,\
    KEY_REMOTE_FILE_PATHS, KEY_LOCAL_STORE_FILE_PATHS
from gribmagic.unity.modules.download.download import __download_parallel, __download, \
    download
from tests.unity.fixtures import \
    icon_eu_input_file, icon_eu_output_file, \
    harmonie_input_file, harmonie_output_file, \
    gfs_input_file, gfs_output_file


@responses.activate
def test___download():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    __download((WeatherModels.ICON_EU,
                icon_eu_output_file,
                Path('test', 'mock')))

    assert icon_eu_output_file.is_file() is True

    os.remove(icon_eu_output_file)


@responses.activate
def test___download_parallel():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    __download_parallel([(WeatherModels.ICON_EU,
                icon_eu_output_file,
                Path('test', 'mock'))])

    assert icon_eu_output_file.is_file() is True

    os.remove(icon_eu_output_file)


@responses.activate
def test_download_store_bz2_sequential():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.ICON_EU,
             {KEY_LOCAL_FILE_PATHS: [icon_eu_output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert icon_eu_output_file.is_file() is True
    os.remove(icon_eu_output_file)


@responses.activate
def test_download_store_bz2_parallel():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.ICON_EU,
             {KEY_LOCAL_FILE_PATHS: [icon_eu_output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]},
             parallel_download=True)

    assert icon_eu_output_file.is_file() is True

    os.remove(icon_eu_output_file)


@responses.activate
def test_download_store_tar():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(harmonie_input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.HARMONIE_KNMI,
             {KEY_LOCAL_FILE_PATHS: [harmonie_output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert harmonie_output_file.is_file() is True
    os.remove(harmonie_output_file)


@responses.activate
def test_download_store_uncompressed():

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(gfs_input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.GFS_100,
             {KEY_LOCAL_FILE_PATHS: [gfs_output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert gfs_output_file.is_file() is True
    os.remove(gfs_output_file)
