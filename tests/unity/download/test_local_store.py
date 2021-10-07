import tempfile

from gribmagic.unity.modules.download.local_store import bunzip_store, store, tarfile_store
from io import BytesIO
import os
from pathlib import Path

from tests.unity.fixtures import icon_eu_input_file, harmonie_input_file, harmonie_output_file

output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/test.grib2")


def test_bunzip_store():
    with open(icon_eu_input_file, 'rb') as file:
        test_data = file.read()
    bunzip_store(BytesIO(test_data), output_file)
    assert output_file.is_file() is True
    os.remove(output_file)


def test_store():

    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(b"-" * 42)
    tmpfile.flush()

    with open(tmpfile.name, 'rb') as file:
        test_data = file.read()
    store(BytesIO(test_data), output_file)
    assert output_file.is_file() is True
    os.remove(output_file)


def test_tarfile_store():
    with open(harmonie_input_file, 'rb') as file:
        test_data = file.read()

    tarfile_store(BytesIO(test_data), [harmonie_output_file])
    assert harmonie_output_file.is_file() is True
    os.remove(harmonie_output_file)
