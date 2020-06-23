from src.modules.download.local_store import bunzip_store, store
from io import BytesIO
import os
from pathlib import Path

output_file = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures', 'test.grib2')
output_file_2 = Path(os.getcwd(), 'tests', 'modules', 'download', 'fixtures', 'test_2.grib2')


def test_bunzip_store():
    with open(f"{os.getcwd()}/tests/modules/download/fixtures/"
                        f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2", 'rb') as file:
        test_data = file.read()
    bunzip_store(BytesIO(test_data), output_file)
    assert output_file.is_file() is True


def test_store():
    with open(output_file, 'rb') as file:
        test_data = file.read()
    store(BytesIO(test_data), output_file_2)
    assert output_file_2.is_file() is True
    
    
def test_clean_up():
    os.remove(output_file)
    os.remove(output_file_2)
