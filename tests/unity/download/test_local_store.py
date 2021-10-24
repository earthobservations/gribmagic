import tempfile
from io import BytesIO

from gribmagic.unity.download.decoder import (
    decode_bunzip,
    decode_identity,
    decode_tarfile,
)
from tests.unity.fixtures import harmonie_input_file, icon_eu_input_file


def test_bunzip_store(tmpgribfile):
    with open(icon_eu_input_file, "rb") as file:
        test_data = file.read()
    decode_bunzip(BytesIO(test_data), tmpgribfile)
    assert tmpgribfile.is_file() is True


def test_identity_store(tmpgribfile):

    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(b"-" * 42)
    tmpfile.flush()

    with open(tmpfile.name, "rb") as file:
        test_data = file.read()
    decode_identity(BytesIO(test_data), tmpgribfile)
    assert tmpgribfile.is_file() is True


def test_tarfile_store(tmpgribfile):
    with open(harmonie_input_file, "rb") as file:
        test_data = file.read()

    decode_tarfile(BytesIO(test_data), [tmpgribfile])
    assert tmpgribfile.is_file() is True
