import re
from pathlib import Path
from typing import Generator

import pytest
import responses

from gribmagic.unity.configuration.constants import (
    KEY_LOCAL_FILE_PATHS,
    KEY_LOCAL_STORE_FILE_PATHS,
    KEY_REMOTE_FILE_PATHS,
)
from gribmagic.unity.download.engine import (
    __download,
    __download_parallel,
    run_download,
)
from gribmagic.unity.enumerations import WeatherModel
from gribmagic.unity.model import DownloadItem
from tests.unity.fixtures import gfs_input_file, harmonie_input_file, icon_eu_input_file


@pytest.fixture
def test_item(tmpgribfile) -> Generator[DownloadItem, None, None]:
    item = DownloadItem(
        model=WeatherModel.DWD_ICON_EU, local_file=tmpgribfile, remote_url="http://test/mock"
    )
    yield item


@responses.activate
def test___download(test_item):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    __download(test_item)

    assert test_item.local_file.is_file() is True


@responses.activate
def test___download_parallel(test_item):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    __download_parallel([test_item])

    assert test_item.local_file.is_file() is True


@responses.activate
def test_download_store_bz2_sequential(tmpgribfile):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    run_download(
        WeatherModel.DWD_ICON_EU,
        {
            KEY_LOCAL_FILE_PATHS: [tmpgribfile],
            KEY_REMOTE_FILE_PATHS: ["http://test/mock"],
            KEY_LOCAL_STORE_FILE_PATHS: [Path("not", "used", "in", "download")],
        },
    )

    assert tmpgribfile.is_file() is True


@responses.activate
def test_download_store_bz2_parallel(tmpgribfile):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(icon_eu_input_file, "rb"),
        stream=True,
    )

    run_download(
        WeatherModel.DWD_ICON_EU,
        {
            KEY_LOCAL_FILE_PATHS: [tmpgribfile],
            KEY_REMOTE_FILE_PATHS: ["http://test/mock"],
            KEY_LOCAL_STORE_FILE_PATHS: [Path("not", "used", "in", "download")],
        },
        parallel_download=True,
    )

    assert tmpgribfile.is_file() is True


@responses.activate
def test_download_store_tar(tmpgribfile):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(harmonie_input_file, "rb"),
        stream=True,
    )

    run_download(
        WeatherModel.KNMI_HARMONIE,
        {
            KEY_LOCAL_FILE_PATHS: [tmpgribfile],
            KEY_REMOTE_FILE_PATHS: ["http://test/mock"],
            KEY_LOCAL_STORE_FILE_PATHS: [Path("not", "used", "in", "download")],
        },
    )

    assert tmpgribfile.is_file() is True


@responses.activate
def test_download_store_uncompressed(tmpgribfile):

    responses.add(
        method=responses.GET,
        url=re.compile(".*"),
        body=open(gfs_input_file, "rb"),
        stream=True,
    )

    run_download(
        WeatherModel.NCEP_GFS_100,
        {
            KEY_LOCAL_FILE_PATHS: [tmpgribfile],
            KEY_REMOTE_FILE_PATHS: ["http://test/mock"],
            KEY_LOCAL_STORE_FILE_PATHS: [Path("not", "used", "in", "download")],
        },
    )

    assert tmpgribfile.is_file() is True
