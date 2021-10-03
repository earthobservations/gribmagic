from gribmagic.unity.modules.download.local_store import bunzip_store, store, tarfile_store
from io import BytesIO
import os
from pathlib import Path


input_file_bz2 = Path(f"{os.getcwd()}/.gribmagic-testdata/input/"
                      f"icon-eu_europe_regular-lat-lon_single-level_2020062300_000_T_2M.grib2.bz2")
input_file_tar = Path(f"{os.getcwd()}/.gribmagic-testdata/input/harm40_v1_p1_2019061100-single.tar")

output_file = Path(f"{os.getcwd()}/.gribmagic-testdata/output/test.grib2")
output_file_2 = Path(f"{os.getcwd()}/.gribmagic-testdata/output/test_2.grib2")
tarfile_output = Path(f"{os.getcwd()}/.gribmagic-testdata/output/harmonie_knmi_20200711_00_0.grib")


def test_bunzip_store():
    with open(input_file_bz2, 'rb') as file:
        test_data = file.read()
    bunzip_store(BytesIO(test_data), output_file)
    assert output_file.is_file() is True


def test_store():
    with open(output_file, 'rb') as file:
        test_data = file.read()
    store(BytesIO(test_data), output_file_2)
    assert output_file_2.is_file() is True


def test_tarfile_store():
    with open(input_file_tar, 'rb') as file:
        test_data = file.read()

    tarfile_store(BytesIO(test_data), [tarfile_output])
    assert tarfile_output.is_file() is True


def test_clean_up():
    os.remove(output_file)
    os.remove(output_file_2)
    os.remove(tarfile_output)
