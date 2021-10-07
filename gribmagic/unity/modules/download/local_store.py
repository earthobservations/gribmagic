""" functions to decompress dowloaded files """
import bz2
import shutil
import tarfile
from io import BytesIO
from pathlib import Path
from typing import List


def bunzip_store(file: BytesIO, local_intermediate_file: Path):
    with bz2.BZ2File(file) as fr, local_intermediate_file.open(mode="wb") as fw:
        shutil.copyfileobj(fr, fw)


def store(file: BytesIO, local_intermediate_file: Path):
    with file as in_stream, local_intermediate_file.open("wb") as out_file:
        shutil.copyfileobj(in_stream, out_file)


def tarfile_store(file: BytesIO, local_intermediate_files: List[Path]):
    tmpfile = BytesIO()
    while True:
        s = file.read(16384)
        if not s:
            break
        tmpfile.write(s)
    file.close()
    tmpfile.seek(0)
    with tarfile.open(fileobj=tmpfile, mode="r:") as in_stream:
        for idx, member in enumerate(in_stream.getmembers()):
            shutil.copyfileobj(
                in_stream.extractfile(member), local_intermediate_files[idx].open("wb")
            )
