import os
import tempfile
from io import BytesIO

from gribmagic.unity.download.decoder import (
    decode_bunzip,
    decode_identity,
    decode_tarfile,
)
from tests.unity.fixtures import (
    harmonie_input_file,
    harmonie_output_file,
    icon_eu_input_file,
    testdata_path,
)

output_file = testdata_path / "output/test.grib2"


def test_bunzip_store():
    with open(icon_eu_input_file, "rb") as file:
        test_data = file.read()
    decode_bunzip(BytesIO(test_data), output_file)
    assert output_file.is_file() == True
    os.remove(output_file)


def test_identity_store():

    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(b"-" * 42)
    tmpfile.flush()

    with open(tmpfile.name, "rb") as file:
        test_data = file.read()
    decode_identity(BytesIO(test_data), output_file)
    assert output_file.is_file() == True
    os.remove(output_file)


def test_tarfile_store():
    with open(harmonie_input_file, "rb") as file:
        test_data = file.read()

    decode_tarfile(BytesIO(test_data), [harmonie_output_file])
    assert harmonie_output_file.is_file() == True
    os.remove(harmonie_output_file)
