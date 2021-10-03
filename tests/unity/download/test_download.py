import re
import os
from pathlib import Path
import responses

from gribmagic.unity.enumerations.weather_models import WeatherModels
from gribmagic.unity.modules.config.constants import KEY_LOCAL_FILE_PATHS,\
    KEY_REMOTE_FILE_PATHS, KEY_LOCAL_STORE_FILE_PATHS
from gribmagic.unity.modules.download.download import __download_parallel, __download, \
    download

input_file = Path(f"{os.getcwd()}/.gribmagic-testdata/input/"
                  f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2")
output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/"
                   f"air_temperature_2m.grib2")


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
def test_download_store_bz2_sequential():

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
def test_download_store_bz2_parallel():

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


@responses.activate
def test_download_store_tar():

    input_file = Path(f"{os.getcwd()}/.gribmagic-testdata/input/harm40_v1_p1_2019061100-single.tar")
    output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/harmonie_knmi_20190611_00_0.grib")

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(input_file, "rb"),
        stream=True,
    )

    download(WeatherModels.HARMONIE_KNMI,
             {KEY_LOCAL_FILE_PATHS: [output_file],
              KEY_REMOTE_FILE_PATHS: [Path('test', 'mock')],
              KEY_LOCAL_STORE_FILE_PATHS: [Path('not', 'used', 'in', 'download')]})

    assert output_file.is_file() is True
    os.remove(output_file)
