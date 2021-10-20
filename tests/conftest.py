import os
from unittest import mock

import pytest

if "GM_DATA_PATH" in os.environ:
    del os.environ["GM_DATA_PATH"]


@pytest.fixture
def gm_data_path(tmpdir):
    with mock.patch.dict("os.environ", {"GM_DATA_PATH": str(tmpdir)}):
        yield tmpdir
